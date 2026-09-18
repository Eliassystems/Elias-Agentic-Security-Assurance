from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONTROL_DIR = ROOT / "03_controls"

if str(CONTROL_DIR) not in sys.path:

    sys.path.insert(
        0,
        str(CONTROL_DIR),
    )


from easa_f16_execution import (  # noqa: E402
    ConsequentialTool,
    ExecutionAuthority,
    F16ExecutionGate,
    F16_ACTION,
    F16_OTHER_TOOL,
    F16_PRIMARY_TOOL,
)


SCALE_LADDER = [
    10,
    25,
    50,
    100,
    250,
    500,
    1000,
]


ATTEMPT_CLASSES = [
    "AUTHORIZED",
    "NO_AUTHORITY",
    "PRESENTER_IDENTITY_MISMATCH",
    "TOOL_IDENTITY_MISMATCH",
    "PRECONSUMED_AUTHORITY_REPLAY",
]


MAX_WORKER_CEILING = 64


EVIDENCE_DIR = (
    ROOT
    / "05_evidence"
    / "EASA-F16"
)


SUMMARY_PATH = (
    EVIDENCE_DIR
    / "EASA-F16-SUMMARY.json"
)


STAGE_PATHS = {
    threshold: (
        EVIDENCE_DIR
        / f"EASA-F16-N{threshold}-STAGE.json"
    )
    for threshold in SCALE_LADDER
}


def utc_now() -> str:

    return datetime.now(
        timezone.utc
    ).isoformat()


def write_json(
    path: Path,
    value: dict,
) -> None:

    path.write_text(
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def canonical_json_bytes(
    value,
) -> bytes:

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode(
        "utf-8"
    )


def sha256_hex(
    data: bytes,
) -> str:

    return hashlib.sha256(
        data
    ).hexdigest().upper()


def sequence_for(
    index: int,
) -> str:

    return f"{index + 1:04d}"


def make_attempt(
    *,
    threshold: int,
    attempt_index: int,
    gate: F16ExecutionGate,
    primary_tool: ConsequentialTool,
    alternate_tool: ConsequentialTool,
):

    sequence = sequence_for(
        attempt_index
    )

    attempt_id = (
        f"F16-N{threshold}"
        f"-ATTEMPT-{sequence}"
    )

    presenter = (
        f"AGENT_F16-N{threshold}"
        f"-{sequence}"
    )

    authority_id = (
        f"AUTH_F16-N{threshold}"
        f"-{sequence}"
    )

    mismatch_subject = (
        f"OTHER_AGENT_F16-N{threshold}"
        f"-{sequence}"
    )

    class_index = (
        attempt_index % 5
    )

    attempt_class = (
        ATTEMPT_CLASSES[
            class_index
        ]
    )

    authority = None

    presented_tool = primary_tool

    if attempt_class == "AUTHORIZED":

        authority = ExecutionAuthority(
            authority_id=authority_id,
            subject_identity=presenter,
            authorized_action=F16_ACTION,
            authorized_tool_identity=(
                F16_PRIMARY_TOOL
            ),
            valid=True,
            consumed=False,
        )

    elif attempt_class == "NO_AUTHORITY":

        authority = None

    elif (
        attempt_class
        == "PRESENTER_IDENTITY_MISMATCH"
    ):

        authority = ExecutionAuthority(
            authority_id=authority_id,
            subject_identity=(
                mismatch_subject
            ),
            authorized_action=F16_ACTION,
            authorized_tool_identity=(
                F16_PRIMARY_TOOL
            ),
            valid=True,
            consumed=False,
        )

    elif (
        attempt_class
        == "TOOL_IDENTITY_MISMATCH"
    ):

        authority = ExecutionAuthority(
            authority_id=authority_id,
            subject_identity=presenter,
            authorized_action=F16_ACTION,
            authorized_tool_identity=(
                F16_PRIMARY_TOOL
            ),
            valid=True,
            consumed=False,
        )

        presented_tool = (
            alternate_tool
        )

    elif (
        attempt_class
        == "PRECONSUMED_AUTHORITY_REPLAY"
    ):

        authority = ExecutionAuthority(
            authority_id=authority_id,
            subject_identity=presenter,
            authorized_action=F16_ACTION,
            authorized_tool_identity=(
                F16_PRIMARY_TOOL
            ),
            valid=True,
            consumed=True,
        )

    else:

        raise RuntimeError(
            "F16_UNKNOWN_ATTEMPT_CLASS"
        )

    return gate.attempt(
        threshold=threshold,
        attempt_index=attempt_index,
        attempt_id=attempt_id,
        attempt_class=attempt_class,
        presenter_identity=presenter,
        authority=authority,
        requested_action=F16_ACTION,
        presented_tool=presented_tool,
    )


def all_equal(
    values,
    expected,
) -> bool:

    return all(
        value == expected
        for value in values
    )


def run_threshold(
    threshold: int,
) -> dict:

    expected_each = (
        threshold // 5
    )

    max_workers = min(
        MAX_WORKER_CEILING,
        threshold,
    )

    primary_tool = ConsequentialTool(
        F16_PRIMARY_TOOL
    )

    alternate_tool = ConsequentialTool(
        F16_OTHER_TOOL
    )

    gate = F16ExecutionGate()

    completion_order = []

    with ThreadPoolExecutor(
        max_workers=max_workers,
        thread_name_prefix=(
            f"F16N{threshold}"
        ),
    ) as executor:

        futures = [
            executor.submit(
                make_attempt,
                threshold=threshold,
                attempt_index=index,
                gate=gate,
                primary_tool=primary_tool,
                alternate_tool=alternate_tool,
            )
            for index in range(
                threshold
            )
        ]

        for future in as_completed(
            futures
        ):

            completion_order.append(
                future.result()
            )

    canonical_decisions = sorted(
        completion_order,
        key=lambda decision:
            decision.attempt_id,
    )

    decision_records = [
        asdict(decision)
        for decision
        in canonical_decisions
    ]

    digest_input = (
        canonical_json_bytes(
            decision_records
        )
    )

    decision_digest = (
        sha256_hex(
            digest_input
        )
    )

    class_counts = Counter(
        decision.attempt_class
        for decision
        in canonical_decisions
    )

    reason_counts = Counter(
        decision.reason
        for decision
        in canonical_decisions
    )

    permits = [
        decision
        for decision
        in canonical_decisions
        if decision.verdict
        == "PERMIT"
    ]

    refusals = [
        decision
        for decision
        in canonical_decisions
        if decision.verdict
        == "REFUSE"
    ]

    authorized = [
        decision
        for decision
        in canonical_decisions
        if decision.attempt_class
        == "AUTHORIZED"
    ]

    no_authority = [
        decision
        for decision
        in canonical_decisions
        if decision.attempt_class
        == "NO_AUTHORITY"
    ]

    presenter_mismatch = [
        decision
        for decision
        in canonical_decisions
        if decision.attempt_class
        == "PRESENTER_IDENTITY_MISMATCH"
    ]

    tool_mismatch = [
        decision
        for decision
        in canonical_decisions
        if decision.attempt_class
        == "TOOL_IDENTITY_MISMATCH"
    ]

    replay = [
        decision
        for decision
        in canonical_decisions
        if decision.attempt_class
        == "PRECONSUMED_AUTHORITY_REPLAY"
    ]

    negatives = (
        no_authority
        + presenter_mismatch
        + tool_mismatch
        + replay
    )

    attempt_ids = [
        decision.attempt_id
        for decision
        in canonical_decisions
    ]

    presenter_ids = [
        decision.presenter_identity
        for decision
        in canonical_decisions
    ]

    authority_ids = [
        decision.authority_id
        for decision
        in canonical_decisions
        if decision.authority_present
    ]

    canonical_record_strings = [
        canonical_json_bytes(
            record
        )
        for record
        in decision_records
    ]

    checks = {

        "attempt_count_exact":
            len(
                canonical_decisions
            ) == threshold,

        "decision_record_count_exact":
            len(
                decision_records
            ) == threshold,

        "unique_attempt_ids_exact":
            len(
                set(
                    attempt_ids
                )
            ) == threshold,

        "unique_presenter_ids_exact":
            len(
                set(
                    presenter_ids
                )
            ) == threshold,

        "class_authorized_exact":
            class_counts[
                "AUTHORIZED"
            ] == expected_each,

        "class_no_authority_exact":
            class_counts[
                "NO_AUTHORITY"
            ] == expected_each,

        "class_presenter_mismatch_exact":
            class_counts[
                "PRESENTER_IDENTITY_MISMATCH"
            ] == expected_each,

        "class_tool_mismatch_exact":
            class_counts[
                "TOOL_IDENTITY_MISMATCH"
            ] == expected_each,

        "class_replay_exact":
            class_counts[
                "PRECONSUMED_AUTHORITY_REPLAY"
            ] == expected_each,

        "permit_count_exact":
            len(
                permits
            ) == expected_each,

        "refuse_count_exact":
            len(
                refusals
            ) == (
                threshold
                - expected_each
            ),

        "authorized_all_permit":
            all_equal(
                [
                    item.verdict
                    for item
                    in authorized
                ],
                "PERMIT",
            ),

        "authorized_reason_exact":
            all_equal(
                [
                    item.reason
                    for item
                    in authorized
                ],
                "AUTHORIZED",
            ),

        "authorized_delta_exact":
            sum(
                item.consequence_delta
                for item
                in authorized
            ) == expected_each,

        "authorized_started_unconsumed":
            all_equal(
                [
                    item.authority_consumed_before
                    for item
                    in authorized
                ],
                False,
            ),

        "authorized_consumed_after":
            all_equal(
                [
                    item.authority_consumed_after
                    for item
                    in authorized
                ],
                True,
            ),

        "no_authority_all_refuse":
            all_equal(
                [
                    item.verdict
                    for item
                    in no_authority
                ],
                "REFUSE",
            ),

        "no_authority_reason_exact":
            all_equal(
                [
                    item.reason
                    for item
                    in no_authority
                ],
                "EXECUTION_AUTHORITY_NOT_PRESENT",
            ),

        "no_authority_zero_delta":
            sum(
                item.consequence_delta
                for item
                in no_authority
            ) == 0,

        "presenter_mismatch_all_refuse":
            all_equal(
                [
                    item.verdict
                    for item
                    in presenter_mismatch
                ],
                "REFUSE",
            ),

        "presenter_mismatch_reason_exact":
            all_equal(
                [
                    item.reason
                    for item
                    in presenter_mismatch
                ],
                "PRESENTER_IDENTITY_MISMATCH",
            ),

        "presenter_mismatch_zero_delta":
            sum(
                item.consequence_delta
                for item
                in presenter_mismatch
            ) == 0,

        "presenter_mismatch_unconsumed":
            all_equal(
                [
                    item.authority_consumed_after
                    for item
                    in presenter_mismatch
                ],
                False,
            ),

        "tool_mismatch_all_refuse":
            all_equal(
                [
                    item.verdict
                    for item
                    in tool_mismatch
                ],
                "REFUSE",
            ),

        "tool_mismatch_reason_exact":
            all_equal(
                [
                    item.reason
                    for item
                    in tool_mismatch
                ],
                "TOOL_IDENTITY_MISMATCH",
            ),

        "tool_mismatch_zero_delta":
            sum(
                item.consequence_delta
                for item
                in tool_mismatch
            ) == 0,

        "tool_mismatch_unconsumed":
            all_equal(
                [
                    item.authority_consumed_after
                    for item
                    in tool_mismatch
                ],
                False,
            ),

        "replay_all_refuse":
            all_equal(
                [
                    item.verdict
                    for item
                    in replay
                ],
                "REFUSE",
            ),

        "replay_reason_exact":
            all_equal(
                [
                    item.reason
                    for item
                    in replay
                ],
                "EXECUTION_AUTHORITY_ALREADY_CONSUMED",
            ),

        "replay_zero_delta":
            sum(
                item.consequence_delta
                for item
                in replay
            ) == 0,

        "replay_consumed_before":
            all_equal(
                [
                    item.authority_consumed_before
                    for item
                    in replay
                ],
                True,
            ),

        "replay_consumed_after":
            all_equal(
                [
                    item.authority_consumed_after
                    for item
                    in replay
                ],
                True,
            ),

        "unauthorized_consequence_zero":
            sum(
                item.consequence_delta
                for item
                in negatives
            ) == 0,

        "primary_tool_counter_exact":
            primary_tool
            .consequence_counter
            == expected_each,

        "alternate_tool_counter_zero":
            alternate_tool
            .consequence_counter
            == 0,

        "aggregate_delta_equals_primary_counter":
            sum(
                item.consequence_delta
                for item
                in canonical_decisions
            )
            ==
            primary_tool
            .consequence_counter,

        "authority_ids_unique":
            len(
                authority_ids
            )
            ==
            len(
                set(
                    authority_ids
                )
            ),

        "no_duplicate_decision_records":
            len(
                canonical_record_strings
            )
            ==
            len(
                set(
                    canonical_record_strings
                )
            ),

        "canonical_digest_input_count_exact":
            len(
                decision_records
            )
            == threshold,

        "canonical_digest_present":
            len(
                decision_digest
            ) == 64,

        "refusal_reason_no_authority_exact_count":
            reason_counts[
                "EXECUTION_AUTHORITY_NOT_PRESENT"
            ] == expected_each,

        "refusal_reason_presenter_mismatch_exact_count":
            reason_counts[
                "PRESENTER_IDENTITY_MISMATCH"
            ] == expected_each,

        "refusal_reason_tool_mismatch_exact_count":
            reason_counts[
                "TOOL_IDENTITY_MISMATCH"
            ] == expected_each,

        "refusal_reason_replay_exact_count":
            reason_counts[
                "EXECUTION_AUTHORITY_ALREADY_CONSUMED"
            ] == expected_each,
    }

    stage_pass = all(
        checks.values()
    )

    stage = {

        "examination":
            "EASA-F16",

        "property":
            "BOUNDED_SCALE_PRESERVATION",

        "threshold":
            threshold,

        "max_workers":
            max_workers,

        "sequence_width":
            4,

        "expected_each_class":
            expected_each,

        "expected_permit_count":
            expected_each,

        "expected_refuse_count":
            threshold
            - expected_each,

        "expected_primary_tool_counter":
            expected_each,

        "expected_alternate_tool_counter":
            0,

        "expected_unauthorized_consequence_total":
            0,

        "actual_attempt_count":
            len(
                canonical_decisions
            ),

        "actual_permit_count":
            len(
                permits
            ),

        "actual_refuse_count":
            len(
                refusals
            ),

        "class_counts":
            dict(
                sorted(
                    class_counts.items()
                )
            ),

        "reason_counts":
            dict(
                sorted(
                    reason_counts.items()
                )
            ),

        "unique_attempt_id_count":
            len(
                set(
                    attempt_ids
                )
            ),

        "unique_presenter_id_count":
            len(
                set(
                    presenter_ids
                )
            ),

        "authority_bearing_count":
            len(
                authority_ids
            ),

        "unique_authority_id_count":
            len(
                set(
                    authority_ids
                )
            ),

        "primary_tool_final_counter":
            primary_tool
            .consequence_counter,

        "alternate_tool_final_counter":
            alternate_tool
            .consequence_counter,

        "authorized_consequence_total":
            sum(
                item.consequence_delta
                for item
                in authorized
            ),

        "unauthorized_consequence_total":
            sum(
                item.consequence_delta
                for item
                in negatives
            ),

        "aggregate_decision_consequence_delta":
            sum(
                item.consequence_delta
                for item
                in canonical_decisions
            ),

        "canonical_decision_order":
            "ATTEMPT_ID_ASCENDING",

        "canonical_json_key_order":
            "SORTED",

        "canonical_json_separators":
            "COMPACT",

        "canonical_encoding":
            "UTF-8",

        "canonical_bom":
            "ABSENT",

        "canonical_decision_digest_sha256":
            decision_digest,

        "canonical_digest_input_count":
            len(
                decision_records
            ),

        "checks":
            checks,

        "stage_result":
            (
                "PASS"
                if stage_pass
                else "FAIL"
            ),

        "decisions":
            decision_records,
    }

    write_json(
        STAGE_PATHS[
            threshold
        ],
        stage,
    )

    return stage


def main() -> int:

    expected_paths = (
        list(
            STAGE_PATHS.values()
        )
        + [
            SUMMARY_PATH,
        ]
    )

    existing = [
        str(path)
        for path
        in expected_paths
        if path.exists()
    ]

    if existing:

        print(
            "F16 FIRST-OBSERVATION EVIDENCE "
            "ALREADY EXISTS — STOP"
        )

        for path in existing:

            print(path)

        return 2

    EVIDENCE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    observation_time = (
        utc_now()
    )

    stages = []

    for threshold in SCALE_LADDER:

        stage = run_threshold(
            threshold
        )

        stages.append(
            stage
        )

        print(
            "F16 THRESHOLD "
            f"{threshold}: "
            f"{stage['stage_result']}"
        )

    stage_results = [
        {
            "threshold":
                stage[
                    "threshold"
                ],

            "stage_result":
                stage[
                    "stage_result"
                ],

            "attempt_count":
                stage[
                    "actual_attempt_count"
                ],

            "permit_count":
                stage[
                    "actual_permit_count"
                ],

            "refuse_count":
                stage[
                    "actual_refuse_count"
                ],

            "authorized_consequence_total":
                stage[
                    "authorized_consequence_total"
                ],

            "unauthorized_consequence_total":
                stage[
                    "unauthorized_consequence_total"
                ],

            "primary_tool_final_counter":
                stage[
                    "primary_tool_final_counter"
                ],

            "alternate_tool_final_counter":
                stage[
                    "alternate_tool_final_counter"
                ],

            "canonical_decision_digest_sha256":
                stage[
                    "canonical_decision_digest_sha256"
                ],
        }
        for stage in stages
    ]

    highest_consecutive = None

    for stage in stages:

        if (
            stage["stage_result"]
            == "PASS"
        ):

            highest_consecutive = (
                stage["threshold"]
            )

        else:

            break

    total_attempts = sum(
        stage[
            "actual_attempt_count"
        ]
        for stage in stages
    )

    total_permits = sum(
        stage[
            "actual_permit_count"
        ]
        for stage in stages
    )

    total_refusals = sum(
        stage[
            "actual_refuse_count"
        ]
        for stage in stages
    )

    total_authorized_consequence = sum(
        stage[
            "authorized_consequence_total"
        ]
        for stage in stages
    )

    total_unauthorized_consequence = sum(
        stage[
            "unauthorized_consequence_total"
        ]
        for stage in stages
    )

    all_attempt_ids = [
        decision[
            "attempt_id"
        ]
        for stage in stages
        for decision in stage[
            "decisions"
        ]
    ]

    all_presenter_ids = [
        decision[
            "presenter_identity"
        ]
        for stage in stages
        for decision in stage[
            "decisions"
        ]
    ]

    all_authority_ids = [
        decision[
            "authority_id"
        ]
        for stage in stages
        for decision in stage[
            "decisions"
        ]
        if decision[
            "authority_present"
        ]
    ]

    expected_authority_count = (
        1548
    )

    global_checks = {

        "stage_order_exact":
            [
                stage[
                    "threshold"
                ]
                for stage in stages
            ]
            == SCALE_LADDER,

        "all_seven_stages_present":
            len(
                stages
            ) == 7,

        "all_stages_pass":
            all(
                stage[
                    "stage_result"
                ] == "PASS"
                for stage in stages
            ),

        "total_attempts_1935":
            total_attempts
            == 1935,

        "total_permits_387":
            total_permits
            == 387,

        "total_refusals_1548":
            total_refusals
            == 1548,

        "total_authorized_consequence_387":
            total_authorized_consequence
            == 387,

        "total_unauthorized_consequence_zero":
            total_unauthorized_consequence
            == 0,

        "highest_consecutive_1000":
            highest_consecutive
            == 1000,

        "global_attempt_ids_unique":
            len(
                all_attempt_ids
            )
            ==
            len(
                set(
                    all_attempt_ids
                )
            )
            ==
            1935,

        "global_presenter_ids_unique":
            len(
                all_presenter_ids
            )
            ==
            len(
                set(
                    all_presenter_ids
                )
            )
            ==
            1935,

        "global_authority_ids_unique":
            len(
                all_authority_ids
            )
            ==
            len(
                set(
                    all_authority_ids
                )
            )
            ==
            expected_authority_count,

        "all_stage_digests_present":
            all(
                len(
                    stage[
                        "canonical_decision_digest_sha256"
                    ]
                ) == 64
                for stage in stages
            ),
    }

    overall_pass = all(
        global_checks.values()
    )

    summary_without_digest = {

        "examination":
            "EASA-F16",

        "property":
            "BOUNDED_SCALE_PRESERVATION",

        "observation_time_utc":
            observation_time,

        "scale_ladder":
            SCALE_LADDER,

        "worker_pool_ceiling":
            MAX_WORKER_CEILING,

        "stage_results":
            stage_results,

        "highest_consecutive_survived_threshold":
            highest_consecutive,

        "total_attempt_count":
            total_attempts,

        "total_permit_count":
            total_permits,

        "total_refuse_count":
            total_refusals,

        "total_authorized_consequence":
            total_authorized_consequence,

        "total_unauthorized_consequence":
            total_unauthorized_consequence,

        "global_unique_attempt_id_count":
            len(
                set(
                    all_attempt_ids
                )
            ),

        "global_unique_presenter_id_count":
            len(
                set(
                    all_presenter_ids
                )
            ),

        "global_authority_bearing_count":
            len(
                all_authority_ids
            ),

        "global_unique_authority_id_count":
            len(
                set(
                    all_authority_ids
                )
            ),

        "global_checks":
            global_checks,

        "overall_result":
            (
                "PASS"
                if overall_pass
                else "FAIL"
            ),

        "claim_state":
            (
                "OBSERVATION_SUPPORTS_DEFINED_PROPERTY_AT_1000"
                if overall_pass
                else
                "CLAIM_LIMITED_TO_HIGHEST_CONSECUTIVE_SURVIVED_THRESHOLD"
            ),
    }

    summary_digest = (
        sha256_hex(
            canonical_json_bytes(
                summary_without_digest
            )
        )
    )

    summary = dict(
        summary_without_digest
    )

    summary[
        "canonical_summary_digest_sha256"
    ] = summary_digest

    write_json(
        SUMMARY_PATH,
        summary,
    )

    print(
        "=== EASA-F16 FIRST OBSERVATION ==="
    )

    print(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
    )

    return (
        0
        if overall_pass
        else 1
    )


if __name__ == "__main__":

    raise SystemExit(
        main()
    )