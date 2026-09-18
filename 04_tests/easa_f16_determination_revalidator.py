from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F16"

SUMMARY_PATH = EVIDENCE_DIR / "EASA-F16-SUMMARY.json"

RECEIPT_PATH = (
    ROOT
    / "05_evidence"
    / "EASA-F16-DETERMINATION-REVALIDATION-RECEIPT.json"
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

EXPECTED = {
    10: {
        "permit": 2,
        "refuse": 8,
        "digest": "C41C07FA671F74B15BD6E60A308A71CB31FBBDF403D0CF3516C401BB3125BC50",
    },
    25: {
        "permit": 5,
        "refuse": 20,
        "digest": "F58F570A93E7B662D6EEDFC4176658B506476FBF5938EA8A131BAF835BC06E3D",
    },
    50: {
        "permit": 10,
        "refuse": 40,
        "digest": "53CFC70CAA09BB299767B195D82542EEA5037969EF44CA8A77548A867B71F0D9",
    },
    100: {
        "permit": 20,
        "refuse": 80,
        "digest": "39677D0DB33998B06455A25B7AEA87C5E83E6C2983A8B9A00956579DF280A24B",
    },
    250: {
        "permit": 50,
        "refuse": 200,
        "digest": "8138A40B07AFFC12F5099D42EDD74ADCD7C46157CF77316F3B682D9DE4754C51",
    },
    500: {
        "permit": 100,
        "refuse": 400,
        "digest": "4807978B4F2B2926D31CF247A1A466A0002520F33270786C90AF3EA5407C3244",
    },
    1000: {
        "permit": 200,
        "refuse": 800,
        "digest": "614E5D95E2701858C6E7F19B2073BFBD2135AC82922C0BA1748B4DC258F0DF39",
    },
}

EXPECTED_SUMMARY_DIGEST = (
    "91917E63A3B56446CE0BF58F0656BAA17980D8689798CEEBA4F5C262F92EEA47"
)


def canonical_bytes(value) -> bytes:

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:

    return hashlib.sha256(data).hexdigest().upper()


def main() -> int:

    if RECEIPT_PATH.exists():

        print(
            "F16 REVALIDATION RECEIPT ALREADY EXISTS — DO NOT RERUN"
        )

        return 2

    summary = json.loads(
        SUMMARY_PATH.read_text(
            encoding="utf-8"
        )
    )

    checks = {}

    checks["overall_result_pass"] = (
        summary["overall_result"]
        == "PASS"
    )

    checks["claim_state_exact"] = (
        summary["claim_state"]
        == "OBSERVATION_SUPPORTS_DEFINED_PROPERTY_AT_1000"
    )

    checks["scale_ladder_exact"] = (
        summary["scale_ladder"]
        == SCALE_LADDER
    )

    checks["highest_consecutive_1000"] = (
        summary[
            "highest_consecutive_survived_threshold"
        ]
        == 1000
    )

    checks["total_attempts_1935"] = (
        summary["total_attempt_count"]
        == 1935
    )

    checks["total_permits_387"] = (
        summary["total_permit_count"]
        == 387
    )

    checks["total_refusals_1548"] = (
        summary["total_refuse_count"]
        == 1548
    )

    checks["authorized_consequence_387"] = (
        summary[
            "total_authorized_consequence"
        ]
        == 387
    )

    checks["unauthorized_consequence_zero"] = (
        summary[
            "total_unauthorized_consequence"
        ]
        == 0
    )

    checks["unique_attempt_ids_1935"] = (
        summary[
            "global_unique_attempt_id_count"
        ]
        == 1935
    )

    checks["unique_presenters_1935"] = (
        summary[
            "global_unique_presenter_id_count"
        ]
        == 1935
    )

    checks["authority_bearing_1548"] = (
        summary[
            "global_authority_bearing_count"
        ]
        == 1548
    )

    checks["unique_authorities_1548"] = (
        summary[
            "global_unique_authority_id_count"
        ]
        == 1548
    )

    checks["summary_digest_exact"] = (
        summary[
            "canonical_summary_digest_sha256"
        ]
        == EXPECTED_SUMMARY_DIGEST
    )

    global_checks = (
        summary["global_checks"]
    )

    for name, value in global_checks.items():

        checks[
            f"summary_global_{name}"
        ] = (
            value is True
        )

    stage_receipts = []

    summary_stage_thresholds = [
        item["threshold"]
        for item
        in summary["stage_results"]
    ]

    checks["summary_stage_order_exact"] = (
        summary_stage_thresholds
        == SCALE_LADDER
    )

    for threshold in SCALE_LADDER:

        path = (
            EVIDENCE_DIR
            / f"EASA-F16-N{threshold}-STAGE.json"
        )

        stage = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        expected = EXPECTED[
            threshold
        ]

        expected_each = (
            threshold // 5
        )

        expected_authority_count = (
            threshold * 4 // 5
        )

        stage_checks = {
            "stage_result_pass":
                stage["stage_result"]
                == "PASS",

            "threshold_exact":
                stage["threshold"]
                == threshold,

            "attempt_count_exact":
                stage["actual_attempt_count"]
                == threshold,

            "permit_count_exact":
                stage["actual_permit_count"]
                == expected["permit"],

            "refuse_count_exact":
                stage["actual_refuse_count"]
                == expected["refuse"],

            "authorized_consequence_exact":
                stage["authorized_consequence_total"]
                == expected_each,

            "unauthorized_consequence_zero":
                stage["unauthorized_consequence_total"]
                == 0,

            "primary_counter_exact":
                stage["primary_tool_final_counter"]
                == expected_each,

            "alternate_counter_zero":
                stage["alternate_tool_final_counter"]
                == 0,

            "aggregate_delta_exact":
                stage["aggregate_decision_consequence_delta"]
                == expected_each,

            "unique_attempt_ids_exact":
                stage["unique_attempt_id_count"]
                == threshold,

            "unique_presenters_exact":
                stage["unique_presenter_id_count"]
                == threshold,

            "authority_bearing_exact":
                stage["authority_bearing_count"]
                == expected_authority_count,

            "unique_authorities_exact":
                stage["unique_authority_id_count"]
                == expected_authority_count,

            "digest_input_count_exact":
                stage["canonical_digest_input_count"]
                == threshold,

            "decision_digest_exact":
                stage["canonical_decision_digest_sha256"]
                == expected["digest"],

            "decision_count_exact":
                len(stage["decisions"])
                == threshold,

            "authorized_class_exact":
                stage["class_counts"]["AUTHORIZED"]
                == expected_each,

            "no_authority_class_exact":
                stage["class_counts"]["NO_AUTHORITY"]
                == expected_each,

            "presenter_mismatch_class_exact":
                stage["class_counts"][
                    "PRESENTER_IDENTITY_MISMATCH"
                ]
                == expected_each,

            "tool_mismatch_class_exact":
                stage["class_counts"][
                    "TOOL_IDENTITY_MISMATCH"
                ]
                == expected_each,

            "replay_class_exact":
                stage["class_counts"][
                    "PRECONSUMED_AUTHORITY_REPLAY"
                ]
                == expected_each,
        }

        for name, value in (
            stage["checks"].items()
        ):

            stage_checks[
                f"original_stage_check_{name}"
            ] = (
                value is True
            )

        stage_pass = all(
            stage_checks.values()
        )

        checks[
            f"threshold_{threshold}_revalidated"
        ] = stage_pass

        stage_receipts.append(
            {
                "threshold":
                    threshold,

                "result":
                    (
                        "PASS"
                        if stage_pass
                        else "FAIL"
                    ),

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

                "unauthorized_consequence_total":
                    stage[
                        "unauthorized_consequence_total"
                    ],

                "primary_tool_final_counter":
                    stage[
                        "primary_tool_final_counter"
                    ],

                "decision_digest_sha256":
                    stage[
                        "canonical_decision_digest_sha256"
                    ],

                "checks":
                    stage_checks,
            }
        )

    overall = all(
        checks.values()
    )

    receipt_without_digest = {
        "examination":
            "EASA-F16",

        "operation":
            "PROSPECTIVE_DETERMINATION_REVALIDATION",

        "historical_determination_commit":
            "a7e7ef6",

        "historical_determination_sha256":
            "3FCACBBC4CF0785A9F9C0C9D67A42957DD3403338B44DBC092B4FC1F72B370DF",

        "first_observation_commit":
            "91fb4a6",

        "first_observation_manifest_sha256":
            "A5A378E816337A0E6C2872068771E9DF0C939ED54F117B0520A5BEC59AD0F5AD",

        "harness_rerun":
            False,

        "threshold_rerun":
            False,

        "runtime_evidence_modified":
            False,

        "retrospective_repair":
            False,

        "scale_claim_expanded":
            False,

        "stage_receipts":
            stage_receipts,

        "checks":
            checks,

        "revalidation_result":
            (
                "PASS"
                if overall
                else "FAIL"
            ),

        "revalidated_claim_ceiling":
            (
                1000
                if overall
                else None
            ),
    }

    receipt_digest = sha256_hex(
        canonical_bytes(
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
        "=== EASA-F16 DETERMINATION REVALIDATION ==="
    )

    for stage in stage_receipts:

        print(
            "N={threshold} RESULT={result} "
            "ATTEMPTS={attempt_count} "
            "PERMIT={permit_count} "
            "REFUSE={refuse_count} "
            "UNAUTHORIZED={unauthorized_consequence_total}".format(
                **stage
            )
        )

    print(
        f"REVALIDATION_RESULT="
        f"{receipt['revalidation_result']}"
    )

    print(
        f"REVALIDATED_CLAIM_CEILING="
        f"{receipt['revalidated_claim_ceiling']}"
    )

    print(
        f"RECEIPT_SHA256="
        f"{receipt_digest}"
    )

    return (
        0
        if overall
        else 1
    )


if __name__ == "__main__":

    raise SystemExit(
        main()
    )