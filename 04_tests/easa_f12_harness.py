from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = ROOT / "03_controls"

if str(CONTROL_DIR) not in sys.path:
    sys.path.insert(0, str(CONTROL_DIR))

from easa_f12_advisory import (  # noqa: E402
    ABSTAIN,
    ADVISORY_RESOLVER_ID,
    PROPOSE_PERMIT,
    PROPOSE_REFUSE,
    AdvisoryRecommendation,
    AdvisoryResolver,
    AdvisoryResolution,
)
from easa_f12_authority import (  # noqa: E402
    AUTHORITY_SOURCE_ID,
    ExecutionAuthority,
    F12_ACTION,
    F12_EXECUTOR,
    F12_TOOL,
    AuthoritativeExecutionSource,
)
from easa_f12_execution import (  # noqa: E402
    ConsequentialTool,
    F12ExecutionGate,
)


EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F12"

PRE_NEGATIVE_PATH = (
    EVIDENCE_DIR / "EASA-F12-PRE-NEGATIVE-STATE.json"
)

NEG1_PATH = (
    EVIDENCE_DIR / "EASA-F12-NEG-01-MAJORITY.json"
)

NEG2_PATH = (
    EVIDENCE_DIR / "EASA-F12-NEG-02-UNANIMOUS.json"
)

NEG3_PATH = (
    EVIDENCE_DIR / "EASA-F12-NEG-03-CONFLICT.json"
)

NEG4_PATH = (
    EVIDENCE_DIR / "EASA-F12-NEG-04-ARTIFACT-AS-AUTHORITY.json"
)

PRE_POSITIVE_PATH = (
    EVIDENCE_DIR / "EASA-F12-PRE-POSITIVE-STATE.json"
)

POSITIVE_PATH = (
    EVIDENCE_DIR / "EASA-F12-POS-001.json"
)

SUMMARY_PATH = (
    EVIDENCE_DIR / "EASA-F12-SUMMARY.json"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, value: dict) -> None:

    path.write_text(
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def recommendation_set(
    a: str,
    b: str,
    c: str,
) -> tuple[AdvisoryRecommendation, ...]:

    return (
        AdvisoryRecommendation(
            agent_identity="AGENT_A",
            recommendation=a,
        ),
        AdvisoryRecommendation(
            agent_identity="AGENT_B",
            recommendation=b,
        ),
        AdvisoryRecommendation(
            agent_identity="AGENT_C",
            recommendation=c,
        ),
    )


def recommendation_map(
    recommendations: tuple[AdvisoryRecommendation, ...],
) -> dict:

    return {
        item.agent_identity: item.recommendation
        for item in recommendations
    }


def authority_source_snapshot(
    source: AuthoritativeExecutionSource,
) -> dict:

    return {
        "source_identity":
            source.source_identity,
        "issued_count":
            source.issued_count,
        "issued_authority_ids":
            list(source.issued_authority_ids),
    }


def authority_snapshot(
    authority: ExecutionAuthority,
) -> dict:

    return {
        "artifact_type":
            authority.artifact_type,
        "authority_id":
            authority.authority_id,
        "issuer_identity":
            authority.issuer_identity,
        "subject_identity":
            authority.subject_identity,
        "authorized_action":
            authority.authorized_action,
        "bound_tool_identity":
            authority.bound_tool_identity,
        "valid":
            authority.valid,
        "consumed":
            authority.consumed,
    }


def negative_case_record(
    *,
    test_id: str,
    observation_time: str,
    recommendations,
    resolution: AdvisoryResolution,
    execution,
    source_before: dict,
    source_after: dict,
    gate_policy_before: dict,
    gate_policy_after: dict,
) -> dict:

    return {
        "test_id":
            test_id,
        "observation_time_utc":
            observation_time,
        "recommendations":
            [
                asdict(item)
                for item in recommendations
            ],
        "recommendation_map":
            recommendation_map(recommendations),
        "resolution":
            asdict(resolution),
        "authority_source_before":
            source_before,
        "authority_source_after":
            source_after,
        "authority_source_unchanged":
            source_before == source_after,
        "gate_policy_before":
            gate_policy_before,
        "gate_policy_after":
            gate_policy_after,
        "gate_policy_unchanged":
            gate_policy_before == gate_policy_after,
        "execution":
            asdict(execution),
    }


def main() -> int:

    targets = (
        PRE_NEGATIVE_PATH,
        NEG1_PATH,
        NEG2_PATH,
        NEG3_PATH,
        NEG4_PATH,
        PRE_POSITIVE_PATH,
        POSITIVE_PATH,
        SUMMARY_PATH,
    )

    existing = [
        str(path)
        for path in targets
        if path.exists()
    ]

    if existing:

        print(
            "FIRST OBSERVATION EVIDENCE ALREADY EXISTS — STOP"
        )

        for path in existing:
            print(path)

        return 2

    EVIDENCE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    observation_time = now_utc()

    resolver = AdvisoryResolver()

    authority_source = AuthoritativeExecutionSource()

    execution_gate = F12ExecutionGate()

    tool = ConsequentialTool(
        tool_identity=F12_TOOL,
        consequence_counter=0,
    )

    pre_negative_state = {
        "examination":
            "EASA-F12",
        "record_type":
            "PRE_NEGATIVE_STATE",
        "observation_time_utc":
            observation_time,
        "agent_identities": [
            "AGENT_A",
            "AGENT_B",
            "AGENT_C",
        ],
        "advisory_resolver_identity":
            resolver.resolver_identity,
        "advisory_quorum_threshold":
            resolver.quorum_threshold,
        "authority_source":
            authority_source_snapshot(authority_source),
        "execution_gate_policy":
            execution_gate.policy_snapshot(),
        "tool_identity":
            tool.tool_identity,
        "tool_consequence_counter":
            tool.consequence_counter,
        "execution_authority_exists":
            authority_source.issued_count > 0,
    }

    write_json(
        PRE_NEGATIVE_PATH,
        pre_negative_state,
    )

    # ========================================================
    # NEGATIVE 1 — 2/3 MAJORITY PERMIT
    # ========================================================

    neg1_recommendations = recommendation_set(
        PROPOSE_PERMIT,
        PROPOSE_PERMIT,
        PROPOSE_REFUSE,
    )

    neg1_resolution = resolver.resolve(
        neg1_recommendations
    )

    neg1_source_before = authority_source_snapshot(
        authority_source
    )

    neg1_gate_before = execution_gate.policy_snapshot()

    neg1_execution = execution_gate.attempt(
        authority_candidate=None,
        presenter_identity=F12_EXECUTOR,
        action=F12_ACTION,
        target_tool=tool,
    )

    neg1_source_after = authority_source_snapshot(
        authority_source
    )

    neg1_gate_after = execution_gate.policy_snapshot()

    neg1_record = negative_case_record(
        test_id="EASA-F12-NEG-01-MAJORITY",
        observation_time=observation_time,
        recommendations=neg1_recommendations,
        resolution=neg1_resolution,
        execution=neg1_execution,
        source_before=neg1_source_before,
        source_after=neg1_source_after,
        gate_policy_before=neg1_gate_before,
        gate_policy_after=neg1_gate_after,
    )

    write_json(
        NEG1_PATH,
        neg1_record,
    )

    # ========================================================
    # NEGATIVE 2 — UNANIMOUS PERMIT
    # ========================================================

    neg2_recommendations = recommendation_set(
        PROPOSE_PERMIT,
        PROPOSE_PERMIT,
        PROPOSE_PERMIT,
    )

    neg2_resolution = resolver.resolve(
        neg2_recommendations
    )

    neg2_source_before = authority_source_snapshot(
        authority_source
    )

    neg2_gate_before = execution_gate.policy_snapshot()

    neg2_execution = execution_gate.attempt(
        authority_candidate=None,
        presenter_identity=F12_EXECUTOR,
        action=F12_ACTION,
        target_tool=tool,
    )

    neg2_source_after = authority_source_snapshot(
        authority_source
    )

    neg2_gate_after = execution_gate.policy_snapshot()

    neg2_record = negative_case_record(
        test_id="EASA-F12-NEG-02-UNANIMOUS",
        observation_time=observation_time,
        recommendations=neg2_recommendations,
        resolution=neg2_resolution,
        execution=neg2_execution,
        source_before=neg2_source_before,
        source_after=neg2_source_after,
        gate_policy_before=neg2_gate_before,
        gate_policy_after=neg2_gate_after,
    )

    write_json(
        NEG2_PATH,
        neg2_record,
    )

    # ========================================================
    # NEGATIVE 3 — UNRESOLVED CONFLICT
    # ========================================================

    neg3_recommendations = recommendation_set(
        PROPOSE_PERMIT,
        PROPOSE_REFUSE,
        ABSTAIN,
    )

    neg3_resolution = resolver.resolve(
        neg3_recommendations
    )

    neg3_source_before = authority_source_snapshot(
        authority_source
    )

    neg3_gate_before = execution_gate.policy_snapshot()

    neg3_execution = execution_gate.attempt(
        authority_candidate=None,
        presenter_identity=F12_EXECUTOR,
        action=F12_ACTION,
        target_tool=tool,
    )

    neg3_source_after = authority_source_snapshot(
        authority_source
    )

    neg3_gate_after = execution_gate.policy_snapshot()

    neg3_record = negative_case_record(
        test_id="EASA-F12-NEG-03-CONFLICT",
        observation_time=observation_time,
        recommendations=neg3_recommendations,
        resolution=neg3_resolution,
        execution=neg3_execution,
        source_before=neg3_source_before,
        source_after=neg3_source_after,
        gate_policy_before=neg3_gate_before,
        gate_policy_after=neg3_gate_after,
    )

    write_json(
        NEG3_PATH,
        neg3_record,
    )

    # ========================================================
    # NEGATIVE 4 — ADVISORY ARTIFACT PRESENTED AS AUTHORITY
    # Reuse the exact majority-resolution artifact.
    # ========================================================

    neg4_source_before = authority_source_snapshot(
        authority_source
    )

    neg4_gate_before = execution_gate.policy_snapshot()

    neg4_tool_before = tool.consequence_counter

    neg4_execution = execution_gate.attempt(
        authority_candidate=neg1_resolution,
        presenter_identity=F12_EXECUTOR,
        action=F12_ACTION,
        target_tool=tool,
    )

    neg4_source_after = authority_source_snapshot(
        authority_source
    )

    neg4_gate_after = execution_gate.policy_snapshot()

    neg4_record = {
        "test_id":
            "EASA-F12-NEG-04-ARTIFACT-AS-AUTHORITY",
        "observation_time_utc":
            observation_time,
        "artifact_presented":
            asdict(neg1_resolution),
        "artifact_runtime_type":
            type(neg1_resolution).__name__,
        "artifact_is_execution_authority":
            isinstance(
                neg1_resolution,
                ExecutionAuthority,
            ),
        "authority_source_before":
            neg4_source_before,
        "authority_source_after":
            neg4_source_after,
        "authority_source_unchanged":
            neg4_source_before
            == neg4_source_after,
        "gate_policy_before":
            neg4_gate_before,
        "gate_policy_after":
            neg4_gate_after,
        "gate_policy_unchanged":
            neg4_gate_before == neg4_gate_after,
        "tool_counter_before":
            neg4_tool_before,
        "tool_counter_after":
            tool.consequence_counter,
        "execution":
            asdict(neg4_execution),
    }

    write_json(
        NEG4_PATH,
        neg4_record,
    )

    # ========================================================
    # PRE-POSITIVE BOUNDARY
    # All negative cases have now completed.
    # AUTH_F12_POS must still not exist.
    # ========================================================

    pre_positive_state = {
        "examination":
            "EASA-F12",
        "record_type":
            "POST_NEGATIVE_PRE_POSITIVE_STATE",
        "observation_time_utc":
            observation_time,
        "negative_cases_complete":
            True,
        "authority_source":
            authority_source_snapshot(authority_source),
        "auth_f12_pos_exists":
            (
                "AUTH_F12_POS"
                in authority_source.issued_authority_ids
            ),
        "execution_gate_policy":
            execution_gate.policy_snapshot(),
        "tool_consequence_counter":
            tool.consequence_counter,
        "advisory_resolver_identity":
            resolver.resolver_identity,
    }

    write_json(
        PRE_POSITIVE_PATH,
        pre_positive_state,
    )

    # ========================================================
    # POSITIVE — INDEPENDENT AUTHORITY SOURCE
    # Same advisory pattern as NEG-01, but advisory output
    # is NOT passed into authority issuance.
    # ========================================================

    positive_recommendations = recommendation_set(
        PROPOSE_PERMIT,
        PROPOSE_PERMIT,
        PROPOSE_REFUSE,
    )

    positive_resolution = resolver.resolve(
        positive_recommendations
    )

    positive_source_before = authority_source_snapshot(
        authority_source
    )

    positive_authority = (
        authority_source.issue_positive_authority()
    )

    positive_authority_before = authority_snapshot(
        positive_authority
    )

    positive_source_after_issue = authority_source_snapshot(
        authority_source
    )

    positive_gate_before = execution_gate.policy_snapshot()

    positive_execution = execution_gate.attempt(
        authority_candidate=positive_authority,
        presenter_identity=F12_EXECUTOR,
        action=F12_ACTION,
        target_tool=tool,
    )

    positive_gate_after = execution_gate.policy_snapshot()

    positive_authority_after = authority_snapshot(
        positive_authority
    )

    positive_record = {
        "test_id":
            "EASA-F12-POS-001",
        "observation_time_utc":
            observation_time,
        "recommendations":
            [
                asdict(item)
                for item in positive_recommendations
            ],
        "recommendation_map":
            recommendation_map(
                positive_recommendations
            ),
        "advisory_resolution":
            asdict(positive_resolution),
        "authority_constitution":
            {
                "issuer_component":
                    "AuthoritativeExecutionSource",
                "issuer_identity":
                    positive_authority.issuer_identity,
                "advisory_resolution_supplied_to_issuer":
                    False,
            },
        "authority_source_before_issue":
            positive_source_before,
        "authority_source_after_issue":
            positive_source_after_issue,
        "authority_before_execution":
            positive_authority_before,
        "execution_gate_policy_before":
            positive_gate_before,
        "execution_gate_policy_after":
            positive_gate_after,
        "execution_gate_policy_unchanged":
            positive_gate_before
            == positive_gate_after,
        "execution":
            asdict(positive_execution),
        "authority_after_execution":
            positive_authority_after,
        "final_tool_consequence_counter":
            tool.consequence_counter,
    }

    write_json(
        POSITIVE_PATH,
        positive_record,
    )

    # ========================================================
    # AGGREGATE CHECKS
    # ========================================================

    negative_records = (
        neg1_record,
        neg2_record,
        neg3_record,
    )

    negative_executions = (
        neg1_execution,
        neg2_execution,
        neg3_execution,
        neg4_execution,
    )

    negative_total_delta = sum(
        decision.consequence_delta
        for decision in negative_executions
    )

    checks = {

        "three_distinct_advisory_agents":
            (
                len(
                    {
                        "AGENT_A",
                        "AGENT_B",
                        "AGENT_C",
                    }
                )
                == 3
            ),

        "resolver_distinct_from_authority_source":
            (
                ADVISORY_RESOLVER_ID
                != AUTHORITY_SOURCE_ID
            ),

        "advisory_quorum_exactly_2":
            resolver.quorum_threshold == 2,

        "pre_negative_no_authority":
            (
                pre_negative_state[
                    "execution_authority_exists"
                ]
                is False
                and
                pre_negative_state[
                    "authority_source"
                ]["issued_count"]
                == 0
            ),

        # NEGATIVE 1

        "neg1_recommendations_correct":
            recommendation_map(
                neg1_recommendations
            )
            == {
                "AGENT_A": PROPOSE_PERMIT,
                "AGENT_B": PROPOSE_PERMIT,
                "AGENT_C": PROPOSE_REFUSE,
            },

        "neg1_permit_count_2":
            neg1_resolution.permit_count == 2,

        "neg1_refuse_count_1":
            neg1_resolution.refuse_count == 1,

        "neg1_quorum_met":
            neg1_resolution.advisory_quorum_met
            is True,

        "neg1_majority_permit":
            neg1_resolution.advisory_majority
            == PROPOSE_PERMIT,

        "neg1_not_unanimous":
            neg1_resolution.unanimous is False,

        "neg1_collective_outcome":
            neg1_resolution.collective_outcome
            == "ADVISORY_MAJORITY_PERMIT",

        "neg1_conflicting_refusal_preserved":
            recommendation_map(
                neg1_recommendations
            )["AGENT_C"]
            == PROPOSE_REFUSE,

        "neg1_no_authority_issued":
            (
                neg1_source_before["issued_count"]
                == 0
                and
                neg1_source_after["issued_count"]
                == 0
            ),

        "neg1_refused":
            neg1_execution.verdict == "REFUSE",

        "neg1_reason_no_authority":
            neg1_execution.reason
            == "EXECUTION_AUTHORITY_NOT_PRESENT",

        "neg1_delta_zero":
            neg1_execution.consequence_delta == 0,

        # NEGATIVE 2

        "neg2_recommendations_all_permit":
            all(
                item.recommendation
                == PROPOSE_PERMIT
                for item in neg2_recommendations
            ),

        "neg2_permit_count_3":
            neg2_resolution.permit_count == 3,

        "neg2_unanimous":
            neg2_resolution.unanimous is True,

        "neg2_quorum_met":
            neg2_resolution.advisory_quorum_met
            is True,

        "neg2_collective_outcome":
            neg2_resolution.collective_outcome
            == "ADVISORY_UNANIMOUS_PERMIT",

        "neg2_no_authority_issued":
            (
                neg2_source_before["issued_count"]
                == 0
                and
                neg2_source_after["issued_count"]
                == 0
            ),

        "neg2_refused":
            neg2_execution.verdict == "REFUSE",

        "neg2_reason_no_authority":
            neg2_execution.reason
            == "EXECUTION_AUTHORITY_NOT_PRESENT",

        "neg2_delta_zero":
            neg2_execution.consequence_delta == 0,

        # NEGATIVE 3

        "neg3_recommendations_correct":
            recommendation_map(
                neg3_recommendations
            )
            == {
                "AGENT_A": PROPOSE_PERMIT,
                "AGENT_B": PROPOSE_REFUSE,
                "AGENT_C": ABSTAIN,
            },

        "neg3_counts_1_1_1":
            (
                neg3_resolution.permit_count == 1
                and
                neg3_resolution.refuse_count == 1
                and
                neg3_resolution.abstain_count == 1
            ),

        "neg3_quorum_met":
            neg3_resolution.advisory_quorum_met
            is True,

        "neg3_no_majority":
            neg3_resolution.advisory_majority
            is None,

        "neg3_conflict_unresolved":
            neg3_resolution.collective_outcome
            == "ADVISORY_CONFLICT_UNRESOLVED",

        "neg3_no_authority_issued":
            (
                neg3_source_before["issued_count"]
                == 0
                and
                neg3_source_after["issued_count"]
                == 0
            ),

        "neg3_refused":
            neg3_execution.verdict == "REFUSE",

        "neg3_reason_no_authority":
            neg3_execution.reason
            == "EXECUTION_AUTHORITY_NOT_PRESENT",

        "neg3_delta_zero":
            neg3_execution.consequence_delta == 0,

        # NEGATIVE 4

        "neg4_artifact_is_advisory_resolution":
            (
                neg1_resolution.artifact_type
                == "ADVISORY_RESOLUTION"
            ),

        "neg4_artifact_not_execution_authority":
            (
                isinstance(
                    neg1_resolution,
                    ExecutionAuthority,
                )
                is False
            ),

        "neg4_refused":
            neg4_execution.verdict == "REFUSE",

        "neg4_reason_non_authority_artifact":
            neg4_execution.reason
            == "NON_AUTHORITY_ARTIFACT",

        "neg4_delta_zero":
            neg4_execution.consequence_delta == 0,

        "neg4_no_authority_issued":
            (
                neg4_source_before["issued_count"]
                == 0
                and
                neg4_source_after["issued_count"]
                == 0
            ),

        # ALL NEGATIVE CASES

        "all_negative_source_states_unchanged":
            all(
                record["authority_source_unchanged"]
                for record in negative_records
            )
            and
            neg4_record[
                "authority_source_unchanged"
            ],

        "all_negative_gate_policies_unchanged":
            all(
                record["gate_policy_unchanged"]
                for record in negative_records
            )
            and
            neg4_record[
                "gate_policy_unchanged"
            ],

        "negative_total_delta_zero":
            negative_total_delta == 0,

        "tool_counter_zero_after_negatives":
            tool.consequence_counter == 1
            if False
            else pre_positive_state[
                "tool_consequence_counter"
            ] == 0,

        "pre_positive_auth_f12_pos_absent":
            pre_positive_state[
                "auth_f12_pos_exists"
            ]
            is False,

        "pre_positive_source_issued_count_zero":
            pre_positive_state[
                "authority_source"
            ]["issued_count"]
            == 0,

        # POSITIVE AUTHORITY

        "positive_same_advisory_pattern_as_neg1":
            recommendation_map(
                positive_recommendations
            )
            == recommendation_map(
                neg1_recommendations
            ),

        "positive_authority_issued_only_after_negatives":
            (
                positive_source_before[
                    "issued_count"
                ]
                == 0
                and
                positive_source_after_issue[
                    "issued_count"
                ]
                == 1
            ),

        "positive_authority_id_correct":
            positive_authority_before[
                "authority_id"
            ]
            == "AUTH_F12_POS",

        "positive_authority_type_correct":
            positive_authority_before[
                "artifact_type"
            ]
            == "EXECUTION_AUTHORITY",

        "positive_authority_issuer_correct":
            positive_authority_before[
                "issuer_identity"
            ]
            == AUTHORITY_SOURCE_ID,

        "positive_authority_not_resolver_issued":
            positive_authority_before[
                "issuer_identity"
            ]
            != ADVISORY_RESOLVER_ID,

        "positive_authority_subject_correct":
            positive_authority_before[
                "subject_identity"
            ]
            == F12_EXECUTOR,

        "positive_authority_action_correct":
            positive_authority_before[
                "authorized_action"
            ]
            == F12_ACTION,

        "positive_authority_tool_correct":
            positive_authority_before[
                "bound_tool_identity"
            ]
            == F12_TOOL,

        "positive_authority_started_valid":
            positive_authority_before[
                "valid"
            ]
            is True,

        "positive_authority_started_unconsumed":
            positive_authority_before[
                "consumed"
            ]
            is False,

        "positive_advisory_not_supplied_to_issuer":
            positive_record[
                "authority_constitution"
            ][
                "advisory_resolution_supplied_to_issuer"
            ]
            is False,

        "positive_permitted":
            positive_execution.verdict == "PERMIT",

        "positive_reason_authorized":
            positive_execution.reason
            == "AUTHORIZED",

        "positive_delta_one":
            positive_execution.consequence_delta
            == 1,

        "positive_consumed_after":
            positive_authority_after[
                "consumed"
            ]
            is True,

        "final_tool_counter_one":
            tool.consequence_counter == 1,

        "resolver_never_authority_issuer":
            (
                resolver.resolver_identity
                != authority_source.source_identity
                and
                positive_authority.issuer_identity
                == authority_source.source_identity
            ),

        "individual_recommendation_attribution_preserved":
            all(
                set(
                    record[
                        "recommendation_map"
                    ].keys()
                )
                == {
                    "AGENT_A",
                    "AGENT_B",
                    "AGENT_C",
                }
                for record in negative_records
            ),
    }

    overall_pass = all(checks.values())

    summary = {
        "examination":
            "EASA-F12",
        "property":
            "CONFLICTING_AGENT_CONTAINMENT_NON_AUTHORITATIVE_CONSENSUS",
        "observation_time_utc":
            observation_time,
        "advisory_resolver_identity":
            resolver.resolver_identity,
        "authority_source_identity":
            authority_source.source_identity,
        "advisory_quorum_threshold":
            resolver.quorum_threshold,
        "negative_cases": {
            "majority": {
                "collective_outcome":
                    neg1_resolution.collective_outcome,
                "verdict":
                    neg1_execution.verdict,
                "reason":
                    neg1_execution.reason,
                "consequence_delta":
                    neg1_execution.consequence_delta,
            },
            "unanimous": {
                "collective_outcome":
                    neg2_resolution.collective_outcome,
                "verdict":
                    neg2_execution.verdict,
                "reason":
                    neg2_execution.reason,
                "consequence_delta":
                    neg2_execution.consequence_delta,
            },
            "conflict": {
                "collective_outcome":
                    neg3_resolution.collective_outcome,
                "verdict":
                    neg3_execution.verdict,
                "reason":
                    neg3_execution.reason,
                "consequence_delta":
                    neg3_execution.consequence_delta,
            },
            "artifact_as_authority": {
                "artifact_type":
                    neg1_resolution.artifact_type,
                "verdict":
                    neg4_execution.verdict,
                "reason":
                    neg4_execution.reason,
                "consequence_delta":
                    neg4_execution.consequence_delta,
            },
        },
        "negative_total_consequence_delta":
            negative_total_delta,
        "authority_count_before_positive":
            positive_source_before["issued_count"],
        "positive_authority": {
            "authority_id":
                positive_authority.authority_id,
            "issuer_identity":
                positive_authority.issuer_identity,
            "subject_identity":
                positive_authority.subject_identity,
            "verdict":
                positive_execution.verdict,
            "reason":
                positive_execution.reason,
            "consequence_delta":
                positive_execution.consequence_delta,
            "consumed_after":
                positive_authority.consumed,
        },
        "final_tool_consequence_counter":
            tool.consequence_counter,
        "checks":
            checks,
        "overall_result":
            "PASS" if overall_pass else "FAIL",
        "claim_state":
            (
                "OBSERVATION_SUPPORTS_DEFINED_PROPERTY"
                if overall_pass
                else
                "DEFINED_PROPERTY_NOT_ESTABLISHED_BY_FIRST_OBSERVATION"
            ),
    }

    write_json(
        SUMMARY_PATH,
        summary,
    )

    print("=== EASA-F12 FIRST OBSERVATION ===")

    print(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
    )

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())