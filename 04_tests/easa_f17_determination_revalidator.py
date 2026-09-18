from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EVIDENCE_DIR = (
    ROOT
    / "05_evidence"
    / "EASA-F17"
)

SUMMARY_PATH = (
    EVIDENCE_DIR
    / "EASA-F17-SUMMARY.json"
)

COMPOSITE_PATH = (
    EVIDENCE_DIR
    / "EASA-F17-COMPOSITE-EVIDENCE.json"
)

TRANSITIONS_PATH = (
    EVIDENCE_DIR
    / "EASA-F17-STATE-TRANSITIONS.json"
)

HISTORICAL_DETERMINATION_PATH = (
    ROOT
    / "05_evidence"
    / "EASA-F17-DETERMINATION.md"
)

FIRST_OBSERVATION_MANIFEST_PATH = (
    ROOT
    / "05_evidence"
    / "EASA-F17-FIRST-OBSERVATION-MANIFEST.txt"
)

RECEIPT_PATH = (
    ROOT
    / "05_evidence"
    / "EASA-F17-DETERMINATION-REVALIDATION-RECEIPT.json"
)


EXPECTED_HISTORICAL_DETERMINATION_SHA256 = (
    "A42E4755955CEB788E0B62FF105A0C30909FD8839C6C137647D8B81B2CF659F4"
)

EXPECTED_MANIFEST_SHA256 = (
    "52C7FD4DD20F092B44E0B389237373874BB756258419004AC249D7A5355BE49D"
)

EXPECTED_COMPOSITE_DIGEST = (
    "29497241D5232EBE34F322CC779231F1E7B6B14131CC11003E92C73628C57960"
)

EXPECTED_SUMMARY_DIGEST = (
    "AC0A6EE6876174E540FEB2A16CE441EEE27441B72BE77383F5F0211A87397977"
)


EXPECTED_REASON_COUNTS = {
    "EXECUTION_AUTHORITY_NOT_PRESENT": 2,
    "PRESENTER_IDENTITY_MISMATCH": 1,
    "TOOL_IDENTITY_MISMATCH": 1,
    "EXECUTION_SCOPE_NOT_AUTHORIZED": 2,
    "EXECUTION_AUTHORITY_ALREADY_CONSUMED": 2,
    "EXECUTION_AUTHORITY_EPOCH_CHANGED": 1,
    "HUMAN_AUTHORITY_REQUIRED": 1,
    "DELEGATION_SCOPE_AMPLIFICATION": 1,
    "PEER_STATE_STALE": 1,
    "CURRENT_RESOLUTION_UNAVAILABLE": 1,
    "RESOLVER_STATE_CONFLICT": 1,
    "RESOLVED_STATE_NOT_ADMISSIBLE": 1,
}


EXPECTED_ATTEMPTS = {
    "F17-C01-ATTEMPT":
        ("PERMIT", "AUTHORIZED", 1),

    "F17-C02-ATTEMPT":
        ("PERMIT", "AUTHORIZED", 1),

    "F17-C03-ATTEMPT":
        ("REFUSE", "EXECUTION_AUTHORITY_NOT_PRESENT", 0),

    "F17-C04-ATTEMPT":
        ("REFUSE", "PRESENTER_IDENTITY_MISMATCH", 0),

    "F17-C05-ATTEMPT":
        ("REFUSE", "TOOL_IDENTITY_MISMATCH", 0),

    "F17-C06-ATTEMPT":
        ("REFUSE", "EXECUTION_SCOPE_NOT_AUTHORIZED", 0),

    "F17-C07-ATTEMPT":
        ("REFUSE", "EXECUTION_AUTHORITY_ALREADY_CONSUMED", 0),

    "F17-C08-ATTEMPT":
        ("REFUSE", "EXECUTION_AUTHORITY_EPOCH_CHANGED", 0),

    "F17-C09-ATTEMPT":
        ("REFUSE", "HUMAN_AUTHORITY_REQUIRED", 0),

    "F17-C10-ATTEMPT":
        ("REFUSE", "EXECUTION_SCOPE_NOT_AUTHORIZED", 0),

    "F17-C11-ATTEMPT":
        ("REFUSE", "DELEGATION_SCOPE_AMPLIFICATION", 0),

    "F17-C12-ATTEMPT":
        ("REFUSE", "EXECUTION_AUTHORITY_NOT_PRESENT", 0),

    "F17-C13-ATTEMPT":
        ("REFUSE", "PEER_STATE_STALE", 0),

    "F17-C14-ATTEMPT":
        ("REFUSE", "CURRENT_RESOLUTION_UNAVAILABLE", 0),

    "F17-C15A-ATTEMPT":
        ("REFUSE", "RESOLVER_STATE_CONFLICT", 0),

    "F17-C15B-ATTEMPT":
        ("REFUSE", "RESOLVED_STATE_NOT_ADMISSIBLE", 0),

    "F17-C17-ATTEMPT":
        ("PERMIT", "AUTHORIZED", 1),
}


def sha256_file(
    path: Path,
) -> str:

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest().upper()


def canonical_bytes(
    value,
) -> bytes:

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sha256_canonical(
    value,
) -> str:

    return hashlib.sha256(
        canonical_bytes(value)
    ).hexdigest().upper()


def main() -> int:

    if RECEIPT_PATH.exists():

        print(
            "F17 REVALIDATION RECEIPT ALREADY EXISTS — DO NOT RERUN"
        )

        return 2

    summary = json.loads(
        SUMMARY_PATH.read_text(
            encoding="utf-8"
        )
    )

    composite = json.loads(
        COMPOSITE_PATH.read_text(
            encoding="utf-8"
        )
    )

    transitions = json.loads(
        TRANSITIONS_PATH.read_text(
            encoding="utf-8"
        )
    )

    decisions = composite[
        "decisions"
    ]

    witnesses = composite[
        "witnesses"
    ]

    checks: dict[str, bool] = {}

    # --------------------------------------------------------
    # HISTORICAL BYTE IDENTITIES
    # --------------------------------------------------------

    checks[
        "historical_determination_sha256_exact"
    ] = (
        sha256_file(
            HISTORICAL_DETERMINATION_PATH
        )
        ==
        EXPECTED_HISTORICAL_DETERMINATION_SHA256
    )

    checks[
        "first_observation_manifest_sha256_exact"
    ] = (
        sha256_file(
            FIRST_OBSERVATION_MANIFEST_PATH
        )
        ==
        EXPECTED_MANIFEST_SHA256
    )

    # --------------------------------------------------------
    # SUMMARY STANDING
    # --------------------------------------------------------

    checks[
        "summary_examination_exact"
    ] = (
        summary["examination"]
        == "EASA-F17"
    )

    checks[
        "summary_result_pass"
    ] = (
        summary["overall_result"]
        == "PASS"
    )

    checks[
        "summary_claim_state_exact"
    ] = (
        summary["claim_state"]
        ==
        "OBSERVATION_SUPPORTS_DEFINED_COMPOSITE_PROPERTY"
    )

    checks[
        "case_count_17"
    ] = (
        summary["case_count"]
        == 17
    )

    checks[
        "attempt_count_19"
    ] = (
        summary["attempt_count"]
        == 19
    )

    checks[
        "decision_count_19"
    ] = (
        summary["decision_count"]
        == 19
    )

    checks[
        "witness_count_19"
    ] = (
        summary["witness_count"]
        == 19
    )

    checks[
        "permit_count_4"
    ] = (
        summary["permit_count"]
        == 4
    )

    checks[
        "refuse_count_15"
    ] = (
        summary["refuse_count"]
        == 15
    )

    checks[
        "authorized_consequence_4"
    ] = (
        summary[
            "authorized_consequence_total"
        ]
        == 4
    )

    checks[
        "unauthorized_consequence_zero"
    ] = (
        summary[
            "unauthorized_consequence_total"
        ]
        == 0
    )

    checks[
        "primary_counter_4"
    ] = (
        summary[
            "primary_tool_final_counter"
        ]
        == 4
    )

    checks[
        "alternate_counter_zero"
    ] = (
        summary[
            "alternate_tool_final_counter"
        ]
        == 0
    )

    checks[
        "case16_permit_1"
    ] = (
        summary[
            "case16_permit_count"
        ]
        == 1
    )

    checks[
        "case16_refuse_1"
    ] = (
        summary[
            "case16_refuse_count"
        ]
        == 1
    )

    checks[
        "case16_delta_1"
    ] = (
        summary[
            "case16_consequence_delta"
        ]
        == 1
    )

    checks[
        "case16_shared_authority_consumed"
    ] = (
        summary[
            "case16_shared_authority_consumed"
        ]
        is True
    )

    checks[
        "unique_attempt_ids_19"
    ] = (
        summary[
            "unique_attempt_id_count"
        ]
        == 19
    )

    checks[
        "unique_decision_ids_19"
    ] = (
        summary[
            "unique_decision_id_count"
        ]
        == 19
    )

    checks[
        "unique_witness_ids_19"
    ] = (
        summary[
            "unique_witness_id_count"
        ]
        == 19
    )

    for (
        name,
        value,
    ) in summary[
        "checks"
    ].items():

        checks[
            f"historical_summary_check_{name}"
        ] = (
            value is True
        )

    # --------------------------------------------------------
    # REFUSAL DISTRIBUTION
    # --------------------------------------------------------

    checks[
        "refusal_reason_counts_exact"
    ] = (
        summary[
            "refusal_reason_counts"
        ]
        ==
        EXPECTED_REASON_COUNTS
    )

    # --------------------------------------------------------
    # ATTEMPT-LEVEL DETERMINATION
    # --------------------------------------------------------

    decision_by_attempt = {
        decision["attempt_id"]:
            decision
        for decision
        in decisions
    }

    witness_by_attempt = {
        witness["attempt_id"]:
            witness
        for witness
        in witnesses
    }

    checks[
        "decision_object_count_19"
    ] = (
        len(decisions)
        == 19
    )

    checks[
        "witness_object_count_19"
    ] = (
        len(witnesses)
        == 19
    )

    for (
        attempt_id,
        expected,
    ) in EXPECTED_ATTEMPTS.items():

        decision = (
            decision_by_attempt.get(
                attempt_id
            )
        )

        checks[
            f"{attempt_id}_decision_present"
        ] = (
            decision is not None
        )

        if decision is not None:

            checks[
                f"{attempt_id}_verdict_exact"
            ] = (
                decision["verdict"]
                == expected[0]
            )

            checks[
                f"{attempt_id}_reason_exact"
            ] = (
                decision["reason"]
                == expected[1]
            )

            checks[
                f"{attempt_id}_delta_exact"
            ] = (
                decision[
                    "consequence_delta"
                ]
                == expected[2]
            )

    # --------------------------------------------------------
    # CASE-16 AGGREGATE
    # --------------------------------------------------------

    c16 = [
        decision
        for decision in decisions
        if decision["case_id"]
        ==
        "F17-C16-CONCURRENT-SINGLE-CONSUMPTION"
    ]

    c16_permits = [
        decision
        for decision in c16
        if decision["verdict"]
        == "PERMIT"
    ]

    c16_refusals = [
        decision
        for decision in c16
        if decision["verdict"]
        == "REFUSE"
    ]

    checks[
        "case16_decision_count_2"
    ] = (
        len(c16)
        == 2
    )

    checks[
        "case16_exactly_one_permit"
    ] = (
        len(c16_permits)
        == 1
    )

    checks[
        "case16_exactly_one_refuse"
    ] = (
        len(c16_refusals)
        == 1
    )

    checks[
        "case16_refusal_reason_exact"
    ] = (
        len(c16_refusals)
        == 1
        and
        c16_refusals[0]["reason"]
        ==
        "EXECUTION_AUTHORITY_ALREADY_CONSUMED"
    )

    checks[
        "case16_aggregate_delta_1"
    ] = (
        sum(
            item[
                "consequence_delta"
            ]
            for item in c16
        )
        == 1
    )

    # --------------------------------------------------------
    # WITNESS CORRESPONDENCE
    # --------------------------------------------------------

    correspondence_ok = (
        len(decision_by_attempt)
        == 19
        and
        len(witness_by_attempt)
        == 19
    )

    if correspondence_ok:

        for attempt_id in (
            decision_by_attempt
        ):

            decision = (
                decision_by_attempt[
                    attempt_id
                ]
            )

            witness = (
                witness_by_attempt.get(
                    attempt_id
                )
            )

            if witness is None:

                correspondence_ok = False
                break

            if (
                witness[
                    "decision_id"
                ]
                !=
                decision[
                    "decision_id"
                ]
            ):

                correspondence_ok = False
                break

            if (
                witness["verdict"]
                !=
                decision["verdict"]
            ):

                correspondence_ok = False
                break

            if (
                witness["reason"]
                !=
                decision["reason"]
            ):

                correspondence_ok = False
                break

            if (
                witness[
                    "consequence_delta"
                ]
                !=
                decision[
                    "consequence_delta"
                ]
            ):

                correspondence_ok = False
                break

            if (
                witness[
                    "governing_epoch"
                ]
                !=
                decision[
                    "authoritative_epoch"
                ]
            ):

                correspondence_ok = False
                break

    checks[
        "decision_witness_correspondence_exact"
    ] = (
        correspondence_ok
    )

    # --------------------------------------------------------
    # STATE TRANSITIONS
    # --------------------------------------------------------

    transition_objects = (
        transitions[
            "transitions"
        ]
    )

    checks[
        "transition_count_2"
    ] = (
        len(
            transition_objects
        )
        == 2
    )

    checks[
        "transition_1_to_2_exact"
    ] = (
        len(
            transition_objects
        )
        == 2
        and
        transition_objects[0][
            "before"
        ][
            "epoch"
        ]
        == 1
        and
        transition_objects[0][
            "after"
        ][
            "epoch"
        ]
        == 2
    )

    checks[
        "transition_2_to_3_exact"
    ] = (
        len(
            transition_objects
        )
        == 2
        and
        transition_objects[1][
            "before"
        ][
            "epoch"
        ]
        == 2
        and
        transition_objects[1][
            "after"
        ][
            "epoch"
        ]
        == 3
    )

    # --------------------------------------------------------
    # INDEPENDENT CANONICAL DIGEST RECOMPUTATION
    # --------------------------------------------------------

    pairs = [
        {
            "decision":
                decision,

            "witness":
                witness,
        }
        for (
            decision,
            witness,
        )
        in zip(
            decisions,
            witnesses,
        )
    ]

    recomputed_composite_digest = (
        sha256_canonical(
            pairs
        )
    )

    summary_without_digest = (
        dict(
            summary
        )
    )

    declared_summary_digest = (
        summary_without_digest.pop(
            "canonical_summary_digest_sha256"
        )
    )

    recomputed_summary_digest = (
        sha256_canonical(
            summary_without_digest
        )
    )

    checks[
        "recomputed_composite_digest_exact"
    ] = (
        recomputed_composite_digest
        ==
        EXPECTED_COMPOSITE_DIGEST
    )

    checks[
        "declared_composite_digest_exact"
    ] = (
        composite[
            "canonical_composite_digest_sha256"
        ]
        ==
        EXPECTED_COMPOSITE_DIGEST
    )

    checks[
        "summary_composite_digest_exact"
    ] = (
        summary[
            "canonical_composite_digest_sha256"
        ]
        ==
        EXPECTED_COMPOSITE_DIGEST
    )

    checks[
        "recomputed_summary_digest_exact"
    ] = (
        recomputed_summary_digest
        ==
        EXPECTED_SUMMARY_DIGEST
    )

    checks[
        "declared_summary_digest_exact"
    ] = (
        declared_summary_digest
        ==
        EXPECTED_SUMMARY_DIGEST
    )

    overall_pass = all(
        checks.values()
    )

    receipt_without_digest = {
        "examination":
            "EASA-F17",

        "operation":
            "PROSPECTIVE_DETERMINATION_REVALIDATION",

        "historical_determination_commit":
            "6b7bff2",

        "historical_determination_sha256":
            EXPECTED_HISTORICAL_DETERMINATION_SHA256,

        "first_observation_commit":
            "ad80e8c",

        "first_observation_manifest_sha256":
            EXPECTED_MANIFEST_SHA256,

        "historical_first_observation_result":
            summary[
                "overall_result"
            ],

        "historical_claim_state":
            summary[
                "claim_state"
            ],

        "recomputed_composite_digest_sha256":
            recomputed_composite_digest,

        "recomputed_summary_digest_sha256":
            recomputed_summary_digest,

        "harness_rerun":
            False,

        "case_rerun":
            False,

        "runtime_evidence_modified":
            False,

        "historical_determination_modified":
            False,

        "retrospective_repair":
            False,

        "checks":
            checks,

        "revalidation_result":
            (
                "PASS"
                if overall_pass
                else "FAIL"
            ),

        "revalidated_composite_property":
            (
                "SUPPORTED_WITHIN_FROZEN_SCOPE"
                if overall_pass
                else
                "NOT_REVALIDATED"
            ),
    }

    receipt_digest = (
        sha256_canonical(
            receipt_without_digest
        )
    )

    receipt = dict(
        receipt_without_digest
    )

    receipt[
        "canonical_revalidation_receipt_sha256"
    ] = receipt_digest

    RECEIPT_PATH.write_text(
        json.dumps(
            receipt,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        "=== EASA-F17 DETERMINATION REVALIDATION ==="
    )

    print(
        "HISTORICAL_DETERMINATION=6b7bff2"
    )

    print(
        "FIRST_OBSERVATION=ad80e8c"
    )

    print(
        "RECOMPUTED_COMPOSITE_DIGEST="
        f"{recomputed_composite_digest}"
    )

    print(
        "RECOMPUTED_SUMMARY_DIGEST="
        f"{recomputed_summary_digest}"
    )

    print(
        "REVALIDATION_RESULT="
        f"{receipt['revalidation_result']}"
    )

    print(
        "REVALIDATED_COMPOSITE_PROPERTY="
        f"{receipt['revalidated_composite_property']}"
    )

    print(
        "RECEIPT_SHA256="
        f"{receipt_digest}"
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