from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

DEFINITION_PATH = (
    ROOT
    / "02_threat_models"
    / "EASA-F16-X10K-DEFINITION.md"
)

DEFINITION_HASH_RECORD_PATH = (
    ROOT
    / "05_evidence"
    / "EASA-F16-X10K-DEFINITION-HASH.txt"
)

EXECUTION_PATH = (
    ROOT
    / "03_controls"
    / "easa_f16_x10k_execution.py"
)

HARNESS_PATH = (
    ROOT
    / "04_tests"
    / "easa_f16_x10k_harness.py"
)

IMPLEMENTATION_BINDING_PATH = (
    ROOT
    / "05_evidence"
    / "EASA-F16-X10K-IMPLEMENTATION-BINDING.txt"
)

RECEIPT_PATH = (
    ROOT
    / "05_evidence"
    / "EASA-F16-X10K-IMPLEMENTATION-PREFLIGHT-RECEIPT.json"
)


EXPECTED_DEFINITION_SHA256 = (
    "AD62614FD95CD50F96A4637F20BD149778219575F39424C3B3C1875BA6B65DA0"
)

EXPECTED_DEFINITION_HASH_RECORD_SHA256 = (
    "7AAA230A19D68FFC4FC6A764E0533FDF46EAA0140B1FB3B055AFC9781C40E18B"
)

EXPECTED_EXECUTION_SHA256 = (
    "05072A05339230428EBAE388F213F3D1BE5AFF8768B93DC7D547F6013998BC61"
)

EXPECTED_HARNESS_SHA256 = (
    "99D90356E1F814D12429699028F1BE1E1953E84ED5A6856780B4190A97F72EA9"
)

EXPECTED_BINDING_SHA256 = (
    "829B292FC88ED5567965357EF158BE2DEAB30855BC264217B80EB24BBE732AB7"
)


REQUIRED_LITERALS = (
    "POPULATION = 10_000",
    "MAX_WORKERS = 64",
    "EXPECTED_PER_CLASS = 2_000",
    "EXPECTED_PERMITS = 2_000",
    "EXPECTED_REFUSALS = 8_000",
    "ThreadPoolExecutor",
    "max_workers=MAX_WORKERS",
    "AUTHORIZED",
    "NO_AUTHORITY",
    "PRESENTER_IDENTITY_MISMATCH",
    "TOOL_IDENTITY_MISMATCH",
    "PRECONSUMED_AUTHORITY_REPLAY",
    "EXECUTION_AUTHORITY_NOT_PRESENT",
    "EXECUTION_AUTHORITY_ALREADY_CONSUMED",
    "TOOL_F16_X10K_PRIMARY",
    "TOOL_F16_X10K_OTHER",
    "F16_X10K_BOUNDED_SCALE_WRITE",
    "F16X10K-ATTEMPT",
    "AGENT_F16X10K",
    "AUTH_F16X10K",
    "canonical_decision_digest_sha256",
    "canonical_summary_digest_sha256",
    "OBSERVATION_SUPPORTS_DEFINED_PROPERTY_AT_N_10000",
    "unauthorized_consequence_zero",
    "unique_attempt_ids_10000",
    "unique_presenter_ids_10000",
    "unique_authority_ids_8000",
)


FORBIDDEN_RUNTIME_MARKERS = (
    "EASA-F16-X10K-DECISIONS.json",
    "EASA-F16-X10K-SUMMARY.json",
)


def sha256_file(path: Path) -> str:

    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest().upper()


def canonical_bytes(value) -> bytes:

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")


def main() -> int:

    if RECEIPT_PATH.exists():

        print(
            "10K IMPLEMENTATION PREFLIGHT RECEIPT ALREADY EXISTS — DO NOT RERUN"
        )

        return 2

    execution_raw = EXECUTION_PATH.read_text(
        encoding="utf-8"
    )

    harness_raw = HARNESS_PATH.read_text(
        encoding="utf-8"
    )

    combined_raw = (
        execution_raw
        + "\n"
        + harness_raw
    )

    checks: dict[str, bool] = {}

    # --------------------------------------------------------
    # FROZEN BYTE IDENTITIES
    # --------------------------------------------------------

    checks[
        "definition_sha256_exact"
    ] = (
        sha256_file(
            DEFINITION_PATH
        )
        ==
        EXPECTED_DEFINITION_SHA256
    )

    checks[
        "definition_hash_record_sha256_exact"
    ] = (
        sha256_file(
            DEFINITION_HASH_RECORD_PATH
        )
        ==
        EXPECTED_DEFINITION_HASH_RECORD_SHA256
    )

    checks[
        "execution_sha256_exact"
    ] = (
        sha256_file(
            EXECUTION_PATH
        )
        ==
        EXPECTED_EXECUTION_SHA256
    )

    checks[
        "harness_sha256_exact"
    ] = (
        sha256_file(
            HARNESS_PATH
        )
        ==
        EXPECTED_HARNESS_SHA256
    )

    checks[
        "binding_sha256_exact"
    ] = (
        sha256_file(
            IMPLEMENTATION_BINDING_PATH
        )
        ==
        EXPECTED_BINDING_SHA256
    )

    # --------------------------------------------------------
    # AST VALIDATION
    # --------------------------------------------------------

    execution_ast_ok = True
    harness_ast_ok = True

    try:
        ast.parse(
            execution_raw
        )
    except SyntaxError:
        execution_ast_ok = False

    try:
        ast.parse(
            harness_raw
        )
    except SyntaxError:
        harness_ast_ok = False

    checks[
        "execution_ast_parse_pass"
    ] = execution_ast_ok

    checks[
        "harness_ast_parse_pass"
    ] = harness_ast_ok

    # --------------------------------------------------------
    # STATIC CONTRACT LITERALS
    # --------------------------------------------------------

    literal_results = {}

    for literal in REQUIRED_LITERALS:

        present = (
            literal
            in combined_raw
        )

        literal_results[
            literal
        ] = present

        checks[
            "literal::"
            + literal
        ] = present

    # --------------------------------------------------------
    # STRUCTURAL HARNESS CHECKS
    # --------------------------------------------------------

    checks[
        "population_exact_10000"
    ] = (
        "POPULATION = 10_000"
        in harness_raw
    )

    checks[
        "max_workers_exact_64"
    ] = (
        "MAX_WORKERS = 64"
        in harness_raw
    )

    checks[
        "threadpool_uses_frozen_max_workers"
    ] = (
        "max_workers=MAX_WORKERS"
        in harness_raw
    )

    checks[
        "attempt_loop_uses_population"
    ] = (
        "for index in range("
        in harness_raw
        and
        "POPULATION"
        in harness_raw
    )

    checks[
        "class_assignment_modulo_5_present"
    ] = (
        "attempt_index % 5"
        in harness_raw
    )

    checks[
        "canonical_sort_by_attempt_id_present"
    ] = (
        "key=lambda decision:"
        in harness_raw
        and
        "decision.attempt_id"
        in harness_raw
    )

    checks[
        "decision_digest_generation_present"
    ] = (
        "decision_digest"
        in harness_raw
        and
        "canonical_bytes("
        in harness_raw
    )

    checks[
        "summary_digest_generation_present"
    ] = (
        "summary_digest"
        in harness_raw
    )

    # --------------------------------------------------------
    # FIRST-OBSERVATION ANTI-RERUN GUARD
    # --------------------------------------------------------

    checks[
        "evidence_existence_guard_present"
    ] = (
        "if existing:"
        in harness_raw
        and
        "return 2"
        in harness_raw
    )

    for marker in FORBIDDEN_RUNTIME_MARKERS:

        checks[
            "runtime_path_declared::"
            + marker
        ] = (
            marker
            in harness_raw
        )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    overall_pass = all(
        checks.values()
    )

    receipt_without_digest = {
        "examination":
            "EASA-F16-X10K",

        "operation":
            "PROSPECTIVE_IMPLEMENTATION_PREFLIGHT_REVALIDATION",

        "historical_implementation_commit":
            "4dd956d",

        "historical_definition_commit":
            "e2929da",

        "historical_runtime_executed":
            False,

        "implementation_modified":
            False,

        "harness_modified":
            False,

        "retrospective_repair":
            False,

        "literal_results":
            literal_results,

        "checks":
            checks,

        "preflight_result":
            (
                "PASS"
                if overall_pass
                else "FAIL"
            ),

        "execution_authorization":
            (
                "AUTHORIZED_TO_PROCEED_TO_SINGLE_HISTORICAL_OBSERVATION"
                if overall_pass
                else
                "HOLD"
            ),
    }

    receipt_digest = hashlib.sha256(
        canonical_bytes(
            receipt_without_digest
        )
    ).hexdigest().upper()

    receipt = dict(
        receipt_without_digest
    )

    receipt[
        "canonical_preflight_receipt_sha256"
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
        "=== EASA-F16-X10K IMPLEMENTATION PREFLIGHT ==="
    )

    print(
        "HISTORICAL_IMPLEMENTATION=4dd956d"
    )

    print(
        "RUNTIME_EXECUTED=False"
    )

    print(
        "IMPLEMENTATION_MODIFIED=False"
    )

    print(
        "AST_EXECUTION_PASS="
        f"{execution_ast_ok}"
    )

    print(
        "AST_HARNESS_PASS="
        f"{harness_ast_ok}"
    )

    print(
        "REQUIRED_LITERAL_COUNT="
        f"{len(REQUIRED_LITERALS)}"
    )

    print(
        "REQUIRED_LITERALS_PRESENT="
        f"{sum(literal_results.values())}"
    )

    print(
        "PREFLIGHT_RESULT="
        f"{receipt['preflight_result']}"
    )

    print(
        "EXECUTION_AUTHORIZATION="
        f"{receipt['execution_authorization']}"
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