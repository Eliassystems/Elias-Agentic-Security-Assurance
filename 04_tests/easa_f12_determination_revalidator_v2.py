from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

RECEIPT_PATH = (
    ROOT
    / "05_evidence"
    / "EASA-F12-DETERMINATION-REVALIDATION.json"
)


EXPECTED_HASHES = {
    "02_threat_models/EASA-F12-DEFINITION.md":
        "CFA01585A264EDFA7764F468AA336580A8BB249584798452B3ADC72A8BC029CF",

    "05_evidence/EASA-F12-DEFINITION-HASH.txt":
        "8D98179C55E13562E6BAF7F261CB8D78E3047411FCD9F69D53D6CB0EEA8FE267",

    "03_controls/easa_f12_advisory.py":
        "65347083A77CE12EECD3E2F0647C5F1F31CED3419DA057B9E936E5EF217E5AE6",

    "03_controls/easa_f12_authority.py":
        "00EB85819CACA553C9BEFBF131E3CB92FFCDEA75E2E54BB0B05516796560D688",

    "03_controls/easa_f12_execution.py":
        "44B49CA0B978B4FC1BB7E46B5D1A3CFCDAAB9445D7D971F16BE0000D4BEAC437",

    "04_tests/easa_f12_harness.py":
        "193C2783E65897A7443B2397002D6616A667EF22111A3A2C8783238917EA7979",

    "05_evidence/EASA-F12-IMPLEMENTATION-BINDING.txt":
        "71FFFCD194CC00981AD489E3FE4A169E0DA14178F078E5BE64743545C0DADC37",

    "05_evidence/EASA-F12/EASA-F12-FIRST-OBSERVATION-CONSOLE.txt":
        "77A6FFFC24C9C8D37B09E72B3CB49780C8D3BDD890B7B34DAFDBC0E042BB7978",

    "05_evidence/EASA-F12/EASA-F12-NEG-01-MAJORITY.json":
        "0CCEBE3130FA34087555CFC71A83519E405B9D1C171BB3E2411062B20C80EA76",

    "05_evidence/EASA-F12/EASA-F12-NEG-02-UNANIMOUS.json":
        "CE0EA8BD3F4F3F78013E3109FA2BE2E327C7F2FBD40F4B7BFA9D44FA2F644803",

    "05_evidence/EASA-F12/EASA-F12-NEG-03-CONFLICT.json":
        "6BF6440998012829F6F34A6DDF12F112A5B7375C6721CABA081C566B9124B4A9",

    "05_evidence/EASA-F12/EASA-F12-NEG-04-ARTIFACT-AS-AUTHORITY.json":
        "25E721DDCE5594FA92D16AC60099B5BC31652745CF90FFC3D32A38718C81E191",

    "05_evidence/EASA-F12/EASA-F12-POS-001.json":
        "3F1AC49AB88E98E203E031ADE31893BCD42FA39034068F1E1E8BDEB4F865DC4C",

    "05_evidence/EASA-F12/EASA-F12-PRE-NEGATIVE-STATE.json":
        "694367407F8E0D26A7C8B15AAB44A5547505B654334F5CBA6C1A655983185B62",

    "05_evidence/EASA-F12/EASA-F12-PRE-POSITIVE-STATE.json":
        "F3592CBDDAC0850692D5BFFBDD4E3B154C57225051C7954A64B367F7D4198B8D",

    "05_evidence/EASA-F12/EASA-F12-SUMMARY.json":
        "2ADD0505515130BFB892B1B3EF8D9232EA0009D26B52D469400E570717FF2693",

    "05_evidence/EASA-F12-FIRST-OBSERVATION-MANIFEST.txt":
        "FC0DD6CF90B2410987237E788ED41B1B4388A565690F049C5FABC8E51FDF4E76",

    "05_evidence/EASA-F12-DETERMINATION.md":
        "35863A8DBFEEF223C6FC2790E6D5EE0EB018009797FA8F5CF24516F92D41F960",
}


def sha256_file(relative_path: str) -> str:
    path = ROOT / relative_path
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def load_json(relative_path: str) -> dict:
    return json.loads(
        (ROOT / relative_path).read_text(encoding="utf-8")
    )


def main() -> int:

    hash_checks: dict[str, bool] = {}

    for relative_path, expected_hash in EXPECTED_HASHES.items():

        path = ROOT / relative_path

        if not path.is_file():
            hash_checks[f"exists::{relative_path}"] = False
            continue

        actual_hash = sha256_file(relative_path)

        hash_checks[f"sha256::{relative_path}"] = (
            actual_hash == expected_hash
        )

    pre_negative = load_json(
        "05_evidence/EASA-F12/EASA-F12-PRE-NEGATIVE-STATE.json"
    )

    neg1 = load_json(
        "05_evidence/EASA-F12/EASA-F12-NEG-01-MAJORITY.json"
    )

    neg2 = load_json(
        "05_evidence/EASA-F12/EASA-F12-NEG-02-UNANIMOUS.json"
    )

    neg3 = load_json(
        "05_evidence/EASA-F12/EASA-F12-NEG-03-CONFLICT.json"
    )

    neg4 = load_json(
        "05_evidence/EASA-F12/EASA-F12-NEG-04-ARTIFACT-AS-AUTHORITY.json"
    )

    pre_positive = load_json(
        "05_evidence/EASA-F12/EASA-F12-PRE-POSITIVE-STATE.json"
    )

    positive = load_json(
        "05_evidence/EASA-F12/EASA-F12-POS-001.json"
    )

    summary = load_json(
        "05_evidence/EASA-F12/EASA-F12-SUMMARY.json"
    )

    checks: dict[str, bool] = {}

    def check(name: str, condition: object) -> None:
        checks[name] = bool(condition)

    # ========================================================
    # SUMMARY / IDENTITY
    # ========================================================

    check(
        "SummaryPass",
        summary["overall_result"] == "PASS",
    )

    check(
        "SummarySupportsDefinedProperty",
        summary["claim_state"]
        == "OBSERVATION_SUPPORTS_DEFINED_PROPERTY",
    )

    check(
        "ResolverIdentityCorrect",
        summary["advisory_resolver_identity"]
        == "ADVISORY_RESOLVER_F12",
    )

    check(
        "AuthoritySourceIdentityCorrect",
        summary["authority_source_identity"]
        == "AUTHORITY_SOURCE_F12",
    )

    check(
        "ResolverDistinctFromAuthoritySource",
        summary["advisory_resolver_identity"]
        != summary["authority_source_identity"],
    )

    check(
        "QuorumThresholdTwo",
        summary["advisory_quorum_threshold"] == 2,
    )

    # ========================================================
    # PRE-NEGATIVE
    # ========================================================

    check(
        "ThreeDistinctAdvisoryAgents",
        set(pre_negative["agent_identities"])
        == {"AGENT_A", "AGENT_B", "AGENT_C"},
    )

    check(
        "PreNegativeNoAuthorityIssued",
        pre_negative["authority_source"]["issued_count"] == 0
        and pre_negative["authority_source"]["issued_authority_ids"] == [],
    )

    check(
        "PreNegativeExecutionAuthorityAbsent",
        pre_negative["execution_authority_exists"] is False,
    )

    check(
        "PreNegativeToolCounterZero",
        pre_negative["tool_consequence_counter"] == 0,
    )

    check(
        "GateRequiresExecutionAuthority",
        pre_negative["execution_gate_policy"][
            "requires_execution_authority"
        ] is True,
    )

    check(
        "GateExpectedSourceCorrect",
        pre_negative["execution_gate_policy"][
            "expected_authority_source_identity"
        ] == "AUTHORITY_SOURCE_F12",
    )

    # ========================================================
    # NEGATIVE 1 — MAJORITY
    # ========================================================

    check(
        "Neg1RecommendationsCorrect",
        neg1["recommendation_map"]
        == {
            "AGENT_A": "PROPOSE_PERMIT",
            "AGENT_B": "PROPOSE_PERMIT",
            "AGENT_C": "PROPOSE_REFUSE",
        },
    )

    check(
        "Neg1CountsCorrect",
        neg1["resolution"]["permit_count"] == 2
        and neg1["resolution"]["refuse_count"] == 1
        and neg1["resolution"]["abstain_count"] == 0,
    )

    check(
        "Neg1QuorumMet",
        neg1["resolution"]["advisory_quorum_met"] is True,
    )

    check(
        "Neg1MajorityPermit",
        neg1["resolution"]["advisory_majority"]
        == "PROPOSE_PERMIT",
    )

    check(
        "Neg1NotUnanimous",
        neg1["resolution"]["unanimous"] is False,
    )

    check(
        "Neg1OutcomeCorrect",
        neg1["resolution"]["collective_outcome"]
        == "ADVISORY_MAJORITY_PERMIT",
    )

    check(
        "Neg1ArtifactStillAdvisory",
        neg1["resolution"]["artifact_type"]
        == "ADVISORY_RESOLUTION",
    )

    check(
        "Neg1SourceUnchanged",
        neg1["authority_source_unchanged"] is True
        and neg1["authority_source_before"]["issued_count"] == 0
        and neg1["authority_source_after"]["issued_count"] == 0,
    )

    check(
        "Neg1GateUnchanged",
        neg1["gate_policy_unchanged"] is True,
    )

    check(
        "Neg1RefusedNoAuthority",
        neg1["execution"]["verdict"] == "REFUSE"
        and neg1["execution"]["reason"]
        == "EXECUTION_AUTHORITY_NOT_PRESENT"
        and neg1["execution"]["execution_authority_present"] is False
        and neg1["execution"]["consequence_delta"] == 0,
    )

    # ========================================================
    # NEGATIVE 2 — UNANIMOUS
    # ========================================================

    check(
        "Neg2RecommendationsAllPermit",
        neg2["recommendation_map"]
        == {
            "AGENT_A": "PROPOSE_PERMIT",
            "AGENT_B": "PROPOSE_PERMIT",
            "AGENT_C": "PROPOSE_PERMIT",
        },
    )

    check(
        "Neg2CountsCorrect",
        neg2["resolution"]["permit_count"] == 3
        and neg2["resolution"]["refuse_count"] == 0
        and neg2["resolution"]["abstain_count"] == 0,
    )

    check(
        "Neg2QuorumMet",
        neg2["resolution"]["advisory_quorum_met"] is True,
    )

    check(
        "Neg2UnanimousPermit",
        neg2["resolution"]["unanimous"] is True
        and neg2["resolution"]["advisory_majority"]
        == "PROPOSE_PERMIT"
        and neg2["resolution"]["collective_outcome"]
        == "ADVISORY_UNANIMOUS_PERMIT",
    )

    check(
        "Neg2SourceUnchanged",
        neg2["authority_source_unchanged"] is True
        and neg2["authority_source_before"]["issued_count"] == 0
        and neg2["authority_source_after"]["issued_count"] == 0,
    )

    check(
        "Neg2GateUnchanged",
        neg2["gate_policy_unchanged"] is True,
    )

    check(
        "Neg2RefusedNoAuthority",
        neg2["execution"]["verdict"] == "REFUSE"
        and neg2["execution"]["reason"]
        == "EXECUTION_AUTHORITY_NOT_PRESENT"
        and neg2["execution"]["consequence_delta"] == 0,
    )

    # ========================================================
    # NEGATIVE 3 — CONFLICT
    # ========================================================

    check(
        "Neg3RecommendationsCorrect",
        neg3["recommendation_map"]
        == {
            "AGENT_A": "PROPOSE_PERMIT",
            "AGENT_B": "PROPOSE_REFUSE",
            "AGENT_C": "ABSTAIN",
        },
    )

    check(
        "Neg3CountsCorrect",
        neg3["resolution"]["permit_count"] == 1
        and neg3["resolution"]["refuse_count"] == 1
        and neg3["resolution"]["abstain_count"] == 1,
    )

    check(
        "Neg3NoMajority",
        neg3["resolution"]["advisory_majority"] is None,
    )

    check(
        "Neg3ConflictUnresolved",
        neg3["resolution"]["unanimous"] is False
        and neg3["resolution"]["collective_outcome"]
        == "ADVISORY_CONFLICT_UNRESOLVED",
    )

    check(
        "Neg3SourceUnchanged",
        neg3["authority_source_unchanged"] is True
        and neg3["authority_source_before"]["issued_count"] == 0
        and neg3["authority_source_after"]["issued_count"] == 0,
    )

    check(
        "Neg3GateUnchanged",
        neg3["gate_policy_unchanged"] is True,
    )

    check(
        "Neg3RefusedNoAuthority",
        neg3["execution"]["verdict"] == "REFUSE"
        and neg3["execution"]["reason"]
        == "EXECUTION_AUTHORITY_NOT_PRESENT"
        and neg3["execution"]["consequence_delta"] == 0,
    )

    # ========================================================
    # NEGATIVE 4 — ADVISORY ARTIFACT SUBSTITUTION
    # ========================================================

    check(
        "Neg4ArtifactIsAdvisoryResolution",
        neg4["artifact_presented"]["artifact_type"]
        == "ADVISORY_RESOLUTION"
        and neg4["artifact_runtime_type"]
        == "AdvisoryResolution",
    )

    check(
        "Neg4NotExecutionAuthority",
        neg4["artifact_is_execution_authority"] is False,
    )

    check(
        "Neg4SourceUnchanged",
        neg4["authority_source_unchanged"] is True
        and neg4["authority_source_before"]["issued_count"] == 0
        and neg4["authority_source_after"]["issued_count"] == 0,
    )

    check(
        "Neg4GateUnchanged",
        neg4["gate_policy_unchanged"] is True,
    )

    check(
        "Neg4RefusedNonAuthorityArtifact",
        neg4["execution"]["candidate_artifact_type"]
        == "ADVISORY_RESOLUTION"
        and neg4["execution"]["execution_authority_present"] is False
        and neg4["execution"]["verdict"] == "REFUSE"
        and neg4["execution"]["reason"]
        == "NON_AUTHORITY_ARTIFACT"
        and neg4["execution"]["consequence_delta"] == 0,
    )

    check(
        "Neg4ToolCounterUnchanged",
        neg4["tool_counter_before"] == 0
        and neg4["tool_counter_after"] == 0,
    )

    # ========================================================
    # PRE-POSITIVE TEMPORAL BOUNDARY
    # ========================================================

    check(
        "NegativesCompleteBeforePositive",
        pre_positive["negative_cases_complete"] is True,
    )

    check(
        "AuthF12PosAbsentBeforePositive",
        pre_positive["auth_f12_pos_exists"] is False,
    )

    check(
        "IssuedCountStillZeroBeforePositive",
        pre_positive["authority_source"]["issued_count"] == 0,
    )

    check(
        "ToolCounterStillZeroBeforePositive",
        pre_positive["tool_consequence_counter"] == 0,
    )

    # ========================================================
    # POSITIVE
    # ========================================================

    check(
        "PositiveSameAdvisoryPatternAsNeg1",
        positive["recommendation_map"]
        == neg1["recommendation_map"],
    )

    check(
        "PositiveSourceZeroBeforeIssue",
        positive["authority_source_before_issue"]["issued_count"]
        == 0,
    )

    check(
        "PositiveSourceIssuedExactlyOne",
        positive["authority_source_after_issue"]["issued_count"]
        == 1
        and positive["authority_source_after_issue"][
            "issued_authority_ids"
        ] == ["AUTH_F12_POS"],
    )

    check(
        "PositiveIssuerComponentAuthoritative",
        positive["authority_constitution"]["issuer_component"]
        == "AuthoritativeExecutionSource"
        and positive["authority_constitution"]["issuer_identity"]
        == "AUTHORITY_SOURCE_F12",
    )

    check(
        "PositiveAdvisoryNotSuppliedToIssuer",
        positive["authority_constitution"][
            "advisory_resolution_supplied_to_issuer"
        ] is False,
    )

    authority_before = positive["authority_before_execution"]
    execution = positive["execution"]
    authority_after = positive["authority_after_execution"]

    check(
        "PositiveAuthorityCorrect",
        authority_before["artifact_type"]
        == "EXECUTION_AUTHORITY"
        and authority_before["authority_id"]
        == "AUTH_F12_POS"
        and authority_before["issuer_identity"]
        == "AUTHORITY_SOURCE_F12"
        and authority_before["subject_identity"]
        == "EXECUTOR_F12"
        and authority_before["authorized_action"]
        == "F12_PRIVILEGED_WRITE"
        and authority_before["bound_tool_identity"]
        == "TOOL_F12"
        and authority_before["valid"] is True
        and authority_before["consumed"] is False,
    )

    check(
        "PositiveExecutionCorrect",
        execution["candidate_artifact_type"]
        == "EXECUTION_AUTHORITY"
        and execution["execution_authority_present"] is True
        and execution["authority_id"] == "AUTH_F12_POS"
        and execution["authority_issuer_identity"]
        == "AUTHORITY_SOURCE_F12"
        and execution["verdict"] == "PERMIT"
        and execution["reason"] == "AUTHORIZED"
        and execution["authority_consumed_before"] is False
        and execution["authority_consumed_after"] is True
        and execution["consequence_delta"] == 1,
    )

    check(
        "PositiveAuthorityConsumedAfter",
        authority_after["consumed"] is True,
    )

    check(
        "FinalToolCounterOne",
        positive["final_tool_consequence_counter"] == 1
        and summary["final_tool_consequence_counter"] == 1,
    )

    # ========================================================
    # AGGREGATE SUMMARY
    # ========================================================

    check(
        "NegativeTotalDeltaZero",
        summary["negative_total_consequence_delta"] == 0,
    )

    check(
        "AuthorityCountBeforePositiveZero",
        summary["authority_count_before_positive"] == 0,
    )

    check(
        "SummaryMajorityCorrect",
        summary["negative_cases"]["majority"]
        == {
            "collective_outcome":
                "ADVISORY_MAJORITY_PERMIT",
            "verdict":
                "REFUSE",
            "reason":
                "EXECUTION_AUTHORITY_NOT_PRESENT",
            "consequence_delta":
                0,
        },
    )

    check(
        "SummaryUnanimousCorrect",
        summary["negative_cases"]["unanimous"]
        == {
            "collective_outcome":
                "ADVISORY_UNANIMOUS_PERMIT",
            "verdict":
                "REFUSE",
            "reason":
                "EXECUTION_AUTHORITY_NOT_PRESENT",
            "consequence_delta":
                0,
        },
    )

    check(
        "SummaryConflictCorrect",
        summary["negative_cases"]["conflict"]
        == {
            "collective_outcome":
                "ADVISORY_CONFLICT_UNRESOLVED",
            "verdict":
                "REFUSE",
            "reason":
                "EXECUTION_AUTHORITY_NOT_PRESENT",
            "consequence_delta":
                0,
        },
    )

    check(
        "SummaryArtifactCorrect",
        summary["negative_cases"]["artifact_as_authority"]
        == {
            "artifact_type":
                "ADVISORY_RESOLUTION",
            "verdict":
                "REFUSE",
            "reason":
                "NON_AUTHORITY_ARTIFACT",
            "consequence_delta":
                0,
        },
    )

    check(
        "SummaryPositiveCorrect",
        summary["positive_authority"]["authority_id"]
        == "AUTH_F12_POS"
        and summary["positive_authority"]["issuer_identity"]
        == "AUTHORITY_SOURCE_F12"
        and summary["positive_authority"]["subject_identity"]
        == "EXECUTOR_F12"
        and summary["positive_authority"]["verdict"]
        == "PERMIT"
        and summary["positive_authority"]["reason"]
        == "AUTHORIZED"
        and summary["positive_authority"]["consequence_delta"]
        == 1
        and summary["positive_authority"]["consumed_after"]
        is True,
    )

    preserved_harness_checks = summary.get("checks", {})

    preserved_harness_checks_all_true = (
        bool(preserved_harness_checks)
        and all(
            value is True
            for value in preserved_harness_checks.values()
        )
    )

    check(
        "PreservedHarnessChecksAllTrue",
        preserved_harness_checks_all_true,
    )

    all_hashes_verified = all(hash_checks.values())
    all_checks_passed = all(checks.values())

    overall_pass = (
        all_hashes_verified
        and all_checks_passed
        and preserved_harness_checks_all_true
    )

    receipt = {
        "examination":
            "EASA-F12",

        "record_type":
            "DETERMINATION_REVALIDATION",

        "revalidation_time_utc":
            datetime.now(timezone.utc).isoformat(),

        "revalidation_scope":
            "ADJUDICATION_ONLY_NO_HARNESS_RERUN",

        "definition_commit":
            "8479e92",

        "implementation_commit":
            "94c740d",

        "first_observation_commit":
            "7464615",

        "original_determination_commit":
            "0c183d8",

        "original_determination_sha256":
            "35863A8DBFEEF223C6FC2790E6D5EE0EB018009797FA8F5CF24516F92D41F960",

        "original_adjudication_issue":
            (
                "The interactive PowerShell determination command "
                "encountered a parser error while constituting the "
                "$checks hashtable. The historical determination commit "
                "is preserved unchanged. This revalidation independently "
                "re-adjudicates the already-frozen evidence."
            ),

        "first_observation_rerun":
            False,

        "hash_verification":
            hash_checks,

        "all_frozen_hashes_verified":
            all_hashes_verified,

        "independent_checks":
            checks,

        "all_independent_checks_passed":
            all_checks_passed,

        "preserved_harness_checks_all_true":
            preserved_harness_checks_all_true,

        "overall_result":
            "PASS" if overall_pass else "FAIL",

        "standing":
            (
                "F12_BOUNDED_DETERMINATION_REVALIDATED"
                if overall_pass
                else
                "F12_BOUNDED_DETERMINATION_NOT_REVALIDATED"
            ),
    }

    RECEIPT_PATH.write_text(
        json.dumps(
            receipt,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )

    print("=== EASA-F12 DETERMINATION REVALIDATION ===")
    print(
        json.dumps(
            receipt,
            indent=2,
            sort_keys=True,
        )
    )

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())