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
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONTROL_DIR = ROOT / "03_controls"

if str(CONTROL_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(CONTROL_DIR),
    )


from easa_f16_x100k_execution import (  # noqa: E402
    ACTION,
    ALTERNATE_TOOL,
    PRIMARY_TOOL,
    ConsequentialTool,
    ExecutionAuthority,
    X100KExecutionGate,
)


EXAMINATION = "EASA-F16-X100K"

POPULATION = 100_000

MAX_WORKERS = 64

EXPECTED_PER_CLASS = 20_000

EXPECTED_PERMITS = 20_000

EXPECTED_REFUSALS = 80_000

EXPECTED_AUTHORIZED_CONSEQUENCE = 20_000

EXPECTED_UNAUTHORIZED_CONSEQUENCE = 0


CLASS_NAMES = (
    "AUTHORIZED",
    "NO_AUTHORITY",
    "PRESENTER_IDENTITY_MISMATCH",
    "TOOL_IDENTITY_MISMATCH",
    "PRECONSUMED_AUTHORITY_REPLAY",
)


EXPECTED_CLASS_COUNTS = {
    name: EXPECTED_PER_CLASS
    for name in CLASS_NAMES
}


EXPECTED_REFUSAL_REASON_COUNTS = {
    "EXECUTION_AUTHORITY_NOT_PRESENT":
        EXPECTED_PER_CLASS,

    "PRESENTER_IDENTITY_MISMATCH":
        EXPECTED_PER_CLASS,

    "TOOL_IDENTITY_MISMATCH":
        EXPECTED_PER_CLASS,

    "EXECUTION_AUTHORITY_ALREADY_CONSUMED":
        EXPECTED_PER_CLASS,
}


EVIDENCE_DIR = (
    ROOT
    / "05_evidence"
    / "EASA-F16-X100K"
)

DECISIONS_PATH = (
    EVIDENCE_DIR
    / "EASA-F16-X100K-DECISIONS.json"
)

SUMMARY_PATH = (
    EVIDENCE_DIR
    / "EASA-F16-X100K-SUMMARY.json"
)


def canonical_bytes(
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


def write_json(
    path: Path,
    value,
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


def frozen_identity(
    prefix: str,
    display_sequence: int,
) -> str:

    return (
        f"{prefix}-"
        f"{display_sequence:06d}"
    )


def run_attempt(
    *,
    attempt_index: int,
    gate: X100KExecutionGate,
    primary_tool: ConsequentialTool,
    alternate_tool: ConsequentialTool,
):

    display_sequence = (
        attempt_index + 1
    )

    attempt_id = frozen_identity(
        "F16X100K-ATTEMPT",
        display_sequence,
    )

    presenter_identity = frozen_identity(
        "AGENT_F16X100K",
        display_sequence,
    )

    authority_id = frozen_identity(
        "AUTH_F16X100K",
        display_sequence,
    )

    attempt_class = CLASS_NAMES[
        attempt_index % 5
    ]

    authority = None

    presented_tool = primary_tool

    if attempt_class == "AUTHORIZED":

        authority = ExecutionAuthority(
            authority_id=authority_id,
            subject_identity=presenter_identity,
            authorized_action=ACTION,
            authorized_tool_identity=PRIMARY_TOOL,
            valid=True,
            consumed=False,
        )

    elif attempt_class == "NO_AUTHORITY":

        authority = None

    elif (
        attempt_class
        ==
        "PRESENTER_IDENTITY_MISMATCH"
    ):

        authority = ExecutionAuthority(
            authority_id=authority_id,
            subject_identity=frozen_identity(
                "BOUND_AGENT_F16X100K",
                display_sequence,
            ),
            authorized_action=ACTION,
            authorized_tool_identity=PRIMARY_TOOL,
            valid=True,
            consumed=False,
        )

    elif (
        attempt_class
        ==
        "TOOL_IDENTITY_MISMATCH"
    ):

        authority = ExecutionAuthority(
            authority_id=authority_id,
            subject_identity=presenter_identity,
            authorized_action=ACTION,
            authorized_tool_identity=PRIMARY_TOOL,
            valid=True,
            consumed=False,
        )

        presented_tool = alternate_tool

    elif (
        attempt_class
        ==
        "PRECONSUMED_AUTHORITY_REPLAY"
    ):

        authority = ExecutionAuthority(
            authority_id=authority_id,
            subject_identity=presenter_identity,
            authorized_action=ACTION,
            authorized_tool_identity=PRIMARY_TOOL,
            valid=True,
            consumed=True,
        )

    else:

        raise RuntimeError(
            "F16_X100K_CLASS_NOT_FROZEN"
        )

    return gate.attempt(
        attempt_index=attempt_index,
        display_sequence=display_sequence,
        attempt_id=attempt_id,
        attempt_class=attempt_class,
        presenter_identity=presenter_identity,
        authority=authority,
        requested_action=ACTION,
        presented_tool=presented_tool,
    )


def main() -> int:

    expected_paths = [
        DECISIONS_PATH,
        SUMMARY_PATH,
    ]

    existing = [
        str(path)
        for path in expected_paths
        if path.exists()
    ]

    if existing:

        print(
            "EASA-F16-X100K FIRST-OBSERVATION "
            "EVIDENCE ALREADY EXISTS â€” STOP"
        )

        for path in existing:
            print(path)

        return 2

    EVIDENCE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    primary_tool = ConsequentialTool(
        PRIMARY_TOOL
    )

    alternate_tool = ConsequentialTool(
        ALTERNATE_TOOL
    )

    gate = X100KExecutionGate()

    completion_order = []

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS,
        thread_name_prefix="F16X100K",
    ) as executor:

        futures = [
            executor.submit(
                run_attempt,
                attempt_index=index,
                gate=gate,
                primary_tool=primary_tool,
                alternate_tool=alternate_tool,
            )
            for index in range(
                POPULATION
            )
        ]

        for future in as_completed(
            futures
        ):

            completion_order.append(
                future.result()
            )

    ordered_decisions = sorted(
        completion_order,
        key=lambda decision:
            decision.attempt_id,
    )

    decisions = [
        asdict(decision)
        for decision
        in ordered_decisions
    ]

    decision_digest = (
        sha256_hex(
            canonical_bytes(
                decisions
            )
        )
    )

    class_counts = Counter(
        item[
            "attempt_class"
        ]
        for item in decisions
    )

    verdict_counts = Counter(
        item[
            "verdict"
        ]
        for item in decisions
    )

    refusal_reason_counts = Counter(
        item[
            "reason"
        ]
        for item in decisions
        if item[
            "verdict"
        ]
        == "REFUSE"
    )

    attempt_ids = [
        item[
            "attempt_id"
        ]
        for item in decisions
    ]

    presenter_ids = [
        item[
            "presenter_identity"
        ]
        for item in decisions
    ]

    authority_ids = [
        item[
            "authority_id"
        ]
        for item in decisions
        if item[
            "authority_id"
        ]
        is not None
    ]

    authorized_decisions = [
        item
        for item in decisions
        if item[
            "attempt_class"
        ]
        == "AUTHORIZED"
    ]

    negative_decisions = [
        item
        for item in decisions
        if item[
            "attempt_class"
        ]
        != "AUTHORIZED"
    ]

    no_authority_decisions = [
        item
        for item in decisions
        if item[
            "attempt_class"
        ]
        == "NO_AUTHORITY"
    ]

    identity_mismatch_decisions = [
        item
        for item in decisions
        if item[
            "attempt_class"
        ]
        ==
        "PRESENTER_IDENTITY_MISMATCH"
    ]

    tool_mismatch_decisions = [
        item
        for item in decisions
        if item[
            "attempt_class"
        ]
        ==
        "TOOL_IDENTITY_MISMATCH"
    ]

    replay_decisions = [
        item
        for item in decisions
        if item[
            "attempt_class"
        ]
        ==
        "PRECONSUMED_AUTHORITY_REPLAY"
    ]

    authorized_consequence_total = sum(
        item[
            "consequence_delta"
        ]
        for item in authorized_decisions
    )

    unauthorized_consequence_total = sum(
        item[
            "consequence_delta"
        ]
        for item in negative_decisions
    )

    canonical_order_exact = (
        attempt_ids
        ==
        sorted(
            attempt_ids
        )
    )

    authorized_exact = all(
        (
            item[
                "verdict"
            ]
            == "PERMIT"
        )
        and
        (
            item[
                "reason"
            ]
            == "AUTHORIZED"
        )
        and
        (
            item[
                "consequence_delta"
            ]
            == 1
        )
        and
        (
            item[
                "authority_consumed_before"
            ]
            is False
        )
        and
        (
            item[
                "authority_consumed_after"
            ]
            is True
        )
        for item in authorized_decisions
    )

    no_authority_exact = all(
        (
            item[
                "verdict"
            ]
            == "REFUSE"
        )
        and
        (
            item[
                "reason"
            ]
            ==
            "EXECUTION_AUTHORITY_NOT_PRESENT"
        )
        and
        (
            item[
                "consequence_delta"
            ]
            == 0
        )
        and
        (
            item[
                "authority_present"
            ]
            is False
        )
        and
        (
            item[
                "authority_id"
            ]
            is None
        )
        for item in no_authority_decisions
    )

    identity_mismatch_exact = all(
        (
            item[
                "verdict"
            ]
            == "REFUSE"
        )
        and
        (
            item[
                "reason"
            ]
            ==
            "PRESENTER_IDENTITY_MISMATCH"
        )
        and
        (
            item[
                "consequence_delta"
            ]
            == 0
        )
        and
        (
            item[
                "authority_consumed_before"
            ]
            is False
        )
        and
        (
            item[
                "authority_consumed_after"
            ]
            is False
        )
        for item in identity_mismatch_decisions
    )

    tool_mismatch_exact = all(
        (
            item[
                "verdict"
            ]
            == "REFUSE"
        )
        and
        (
            item[
                "reason"
            ]
            ==
            "TOOL_IDENTITY_MISMATCH"
        )
        and
        (
            item[
                "consequence_delta"
            ]
            == 0
        )
        and
        (
            item[
                "presented_tool_identity"
            ]
            == ALTERNATE_TOOL
        )
        and
        (
            item[
                "authority_consumed_before"
            ]
            is False
        )
        and
        (
            item[
                "authority_consumed_after"
            ]
            is False
        )
        for item in tool_mismatch_decisions
    )

    replay_exact = all(
        (
            item[
                "verdict"
            ]
            == "REFUSE"
        )
        and
        (
            item[
                "reason"
            ]
            ==
            "EXECUTION_AUTHORITY_ALREADY_CONSUMED"
        )
        and
        (
            item[
                "consequence_delta"
            ]
            == 0
        )
        and
        (
            item[
                "authority_consumed_before"
            ]
            is True
        )
        and
        (
            item[
                "authority_consumed_after"
            ]
            is True
        )
        for item in replay_decisions
    )

    checks = {

        "population_100000":
            len(
                decisions
            )
            == 100_000,

        "decision_count_100000":
            len(
                decisions
            )
            == 100_000,

        "max_workers_64":
            MAX_WORKERS
            == 64,

        "class_count_exact":
            dict(
                class_counts
            )
            ==
            EXPECTED_CLASS_COUNTS,

        "authorized_count_20000":
            len(
                authorized_decisions
            )
            == 20_000,

        "no_authority_count_20000":
            len(
                no_authority_decisions
            )
            == 20_000,

        "identity_mismatch_count_20000":
            len(
                identity_mismatch_decisions
            )
            == 20_000,

        "tool_mismatch_count_20000":
            len(
                tool_mismatch_decisions
            )
            == 20_000,

        "replay_count_20000":
            len(
                replay_decisions
            )
            == 20_000,

        "permit_count_20000":
            verdict_counts[
                "PERMIT"
            ]
            == EXPECTED_PERMITS,

        "refuse_count_80000":
            verdict_counts[
                "REFUSE"
            ]
            == EXPECTED_REFUSALS,

        "refusal_reason_counts_exact":
            dict(
                refusal_reason_counts
            )
            ==
            EXPECTED_REFUSAL_REASON_COUNTS,

        "authorized_behavior_exact":
            authorized_exact,

        "no_authority_behavior_exact":
            no_authority_exact,

        "identity_mismatch_behavior_exact":
            identity_mismatch_exact,

        "tool_mismatch_behavior_exact":
            tool_mismatch_exact,

        "replay_behavior_exact":
            replay_exact,

        "authorized_consequence_20000":
            authorized_consequence_total
            ==
            EXPECTED_AUTHORIZED_CONSEQUENCE,

        "unauthorized_consequence_zero":
            unauthorized_consequence_total
            ==
            EXPECTED_UNAUTHORIZED_CONSEQUENCE,

        "primary_tool_counter_20000":
            primary_tool
            .consequence_counter
            == 20_000,

        "alternate_tool_counter_zero":
            alternate_tool
            .consequence_counter
            == 0,

        "unique_attempt_ids_100000":
            len(
                set(
                    attempt_ids
                )
            )
            == 100_000,

        "unique_presenter_ids_100000":
            len(
                set(
                    presenter_ids
                )
            )
            == 100_000,

        "authority_bearing_count_80000":
            len(
                authority_ids
            )
            == 80_000,

        "unique_authority_ids_80000":
            len(
                set(
                    authority_ids
                )
            )
            == 80_000,

        "canonical_order_attempt_id":
            canonical_order_exact,

        "decision_digest_present":
            len(
                decision_digest
            )
            == 64,
    }

    overall_pass = all(
        checks.values()
    )

    summary_without_digest = {

        "examination":
            EXAMINATION,

        "property":
            "BOUNDED_AUTHORIZATION_REFUSAL_PRESERVATION_AT_N_100000",

        "target_population":
            POPULATION,

        "max_workers":
            MAX_WORKERS,

        "class_counts":
            dict(
                sorted(
                    class_counts.items()
                )
            ),

        "attempt_count":
            len(
                decisions
            ),

        "decision_count":
            len(
                decisions
            ),

        "permit_count":
            verdict_counts[
                "PERMIT"
            ],

        "refuse_count":
            verdict_counts[
                "REFUSE"
            ],

        "authorized_consequence_total":
            authorized_consequence_total,

        "unauthorized_consequence_total":
            unauthorized_consequence_total,

        "primary_tool_final_counter":
            primary_tool
            .consequence_counter,

        "alternate_tool_final_counter":
            alternate_tool
            .consequence_counter,

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

        "authority_bearing_attempt_count":
            len(
                authority_ids
            ),

        "unique_authority_id_count":
            len(
                set(
                    authority_ids
                )
            ),

        "refusal_reason_counts":
            dict(
                sorted(
                    refusal_reason_counts.items()
                )
            ),

        "canonical_order":
            "ATTEMPT_ID_ASCENDING",

        "canonical_decision_digest_sha256":
            decision_digest,

        "checks":
            checks,

        "overall_result":
            (
                "PASS"
                if overall_pass
                else "FAIL"
            ),

        "claim_state":
            (
                "OBSERVATION_SUPPORTS_DEFINED_PROPERTY_AT_N_100000"
                if overall_pass
                else
                "DEFINED_PROPERTY_AT_N_100000_NOT_ESTABLISHED_BY_FIRST_OBSERVATION"
            ),
    }

    summary_digest = (
        sha256_hex(
            canonical_bytes(
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

    decisions_evidence = {
        "examination":
            EXAMINATION,

        "target_population":
            POPULATION,

        "max_workers":
            MAX_WORKERS,

        "canonical_order":
            "ATTEMPT_ID_ASCENDING",

        "canonical_encoding":
            "UTF-8",

        "canonical_bom":
            "ABSENT",

        "canonical_json_key_order":
            "SORTED",

        "canonical_json_separators":
            "COMPACT",

        "canonical_decision_digest_sha256":
            decision_digest,

        "decisions":
            decisions,
    }

    write_json(
        DECISIONS_PATH,
        decisions_evidence,
    )

    write_json(
        SUMMARY_PATH,
        summary,
    )

    print(
        "=== EASA-F16-X100K FIRST OBSERVATION ==="
    )

    print(
        f"TARGET_POPULATION="
        f"{POPULATION}"
    )

    print(
        f"MAX_WORKERS="
        f"{MAX_WORKERS}"
    )

    print(
        f"ATTEMPT_COUNT="
        f"{summary['attempt_count']}"
    )

    print(
        f"DECISION_COUNT="
        f"{summary['decision_count']}"
    )

    print(
        f"AUTHORIZED_COUNT="
        f"{summary['class_counts']['AUTHORIZED']}"
    )

    print(
        f"NO_AUTHORITY_COUNT="
        f"{summary['class_counts']['NO_AUTHORITY']}"
    )

    print(
        "PRESENTER_IDENTITY_MISMATCH_COUNT="
        f"{summary['class_counts']['PRESENTER_IDENTITY_MISMATCH']}"
    )

    print(
        f"TOOL_IDENTITY_MISMATCH_COUNT="
        f"{summary['class_counts']['TOOL_IDENTITY_MISMATCH']}"
    )

    print(
        f"PRECONSUMED_REPLAY_COUNT="
        f"{summary['class_counts']['PRECONSUMED_AUTHORITY_REPLAY']}"
    )

    print(
        f"PERMIT_COUNT="
        f"{summary['permit_count']}"
    )

    print(
        f"REFUSE_COUNT="
        f"{summary['refuse_count']}"
    )

    print(
        "AUTHORIZED_CONSEQUENCE_TOTAL="
        f"{summary['authorized_consequence_total']}"
    )

    print(
        "UNAUTHORIZED_CONSEQUENCE_TOTAL="
        f"{summary['unauthorized_consequence_total']}"
    )

    print(
        "PRIMARY_TOOL_FINAL_COUNTER="
        f"{summary['primary_tool_final_counter']}"
    )

    print(
        "ALTERNATE_TOOL_FINAL_COUNTER="
        f"{summary['alternate_tool_final_counter']}"
    )

    print(
        "UNIQUE_ATTEMPT_IDS="
        f"{summary['unique_attempt_id_count']}"
    )

    print(
        "UNIQUE_PRESENTER_IDS="
        f"{summary['unique_presenter_id_count']}"
    )

    print(
        "AUTHORITY_BEARING_ATTEMPTS="
        f"{summary['authority_bearing_attempt_count']}"
    )

    print(
        "UNIQUE_AUTHORITY_IDS="
        f"{summary['unique_authority_id_count']}"
    )

    print(
        "DECISION_DIGEST_SHA256="
        f"{summary['canonical_decision_digest_sha256']}"
    )

    print(
        "SUMMARY_DIGEST_SHA256="
        f"{summary['canonical_summary_digest_sha256']}"
    )

    print(
        "ALL_CHECKS_TRUE="
        f"{all(checks.values())}"
    )

    print(
        f"OVERALL_RESULT="
        f"{summary['overall_result']}"
    )

    print(
        f"CLAIM_STATE="
        f"{summary['claim_state']}"
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