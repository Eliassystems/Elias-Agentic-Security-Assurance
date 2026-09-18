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

from easa_f11_delegation import (  # noqa: E402
    F11_ADMIN_WRITE,
    F11_STANDARD_WRITE,
    TOOL_F11_HIGH,
    TOOL_F11_STANDARD,
    DelegatedAuthority,
    DelegationGate,
    LineageState,
)
from easa_f11_execution import (  # noqa: E402
    ConsequentialTool,
    LineageExecutionGate,
)


EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F11"

ROOT_PATH = (
    EVIDENCE_DIR / "EASA-F11-ROOT-STATE.json"
)

AB_PATH = (
    EVIDENCE_DIR / "EASA-F11-DELEGATION-A-B.json"
)

ATTACK_ACTION_PATH = (
    EVIDENCE_DIR / "EASA-F11-ATTACK-ACTION-SCOPE.json"
)

ATTACK_TOOL_PATH = (
    EVIDENCE_DIR / "EASA-F11-ATTACK-TOOL-SCOPE.json"
)

ATTACK_CEILING_PATH = (
    EVIDENCE_DIR / "EASA-F11-ATTACK-LOCAL-CEILING.json"
)

ATTACK_DEPTH_PATH = (
    EVIDENCE_DIR / "EASA-F11-ATTACK-DELEGATION-DEPTH.json"
)

BC_PATH = (
    EVIDENCE_DIR / "EASA-F11-DELEGATION-B-C.json"
)

CD_PATH = (
    EVIDENCE_DIR / "EASA-F11-ATTACK-C-D.json"
)

EXECUTION_PATH = (
    EVIDENCE_DIR / "EASA-F11-LINEAGE-EXECUTION.json"
)

SUMMARY_PATH = (
    EVIDENCE_DIR / "EASA-F11-SUMMARY.json"
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


def authority_snapshot(
    authority: DelegatedAuthority,
) -> dict:

    return {
        "authority_id": authority.authority_id,
        "subject_identity": authority.subject_identity,
        "parent_authority_id":
            authority.parent_authority_id,
        "lineage_id":
            authority.lineage.lineage_id,
        "lineage_consequence_ceiling":
            authority.lineage.consequence_ceiling,
        "lineage_consequence_count":
            authority.lineage.consequence_count,
        "authorized_actions":
            sorted(authority.authorized_actions),
        "authorized_tools":
            sorted(authority.authorized_tools),
        "local_consequence_ceiling":
            authority.local_consequence_ceiling,
        "local_consequence_count":
            authority.local_consequence_count,
        "delegation_depth_remaining":
            authority.delegation_depth_remaining,
        "authority_epoch":
            authority.authority_epoch,
        "valid":
            authority.valid,
    }


def delegation_record(
    *,
    test_id: str,
    observation_time: str,
    parent_before: dict,
    parent_after: dict,
    result,
) -> dict:

    child = result.child_authority

    return {
        "test_id": test_id,
        "observation_time_utc":
            observation_time,
        "parent_before":
            parent_before,
        "parent_after":
            parent_after,
        "parent_unchanged":
            parent_before == parent_after,
        "decision":
            asdict(result.decision),
        "child_authority":
            (
                authority_snapshot(child)
                if child is not None
                else None
            ),
    }


def execution_record(
    *,
    test_id: str,
    observation_time: str,
    result,
) -> dict:

    return {
        "test_id":
            test_id,
        "observation_time_utc":
            observation_time,
        **asdict(result),
    }


def main() -> int:

    targets = (
        ROOT_PATH,
        AB_PATH,
        ATTACK_ACTION_PATH,
        ATTACK_TOOL_PATH,
        ATTACK_CEILING_PATH,
        ATTACK_DEPTH_PATH,
        BC_PATH,
        CD_PATH,
        EXECUTION_PATH,
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

    lineage = LineageState(
        lineage_id="LINEAGE_F11_001",
        consequence_ceiling=4,
        consequence_count=0,
    )

    root = DelegatedAuthority(
        authority_id="AUTH_F11_A_ROOT",
        subject_identity="AGENT_A",
        parent_authority_id=None,
        lineage=lineage,
        authorized_actions=frozenset(
            {
                F11_STANDARD_WRITE,
                F11_ADMIN_WRITE,
            }
        ),
        authorized_tools=frozenset(
            {
                TOOL_F11_STANDARD,
                TOOL_F11_HIGH,
            }
        ),
        local_consequence_ceiling=4,
        local_consequence_count=0,
        delegation_depth_remaining=2,
        authority_epoch=1,
        valid=True,
    )

    root_record = {
        "examination":
            "EASA-F11",
        "record_type":
            "ROOT_AUTHORITY_STATE",
        "observation_time_utc":
            observation_time,
        "root_authority":
            authority_snapshot(root),
    }

    write_json(
        ROOT_PATH,
        root_record,
    )

    delegation_gate = DelegationGate()

    # ========================================================
    # VALID A -> B
    # ========================================================

    root_before_ab = authority_snapshot(root)

    ab_result = delegation_gate.delegate(
        parent=root,
        child_authority_id="AUTH_F11_B",
        child_subject_identity="AGENT_B",
        child_actions=frozenset(
            {F11_STANDARD_WRITE}
        ),
        child_tools=frozenset(
            {TOOL_F11_STANDARD}
        ),
        child_local_consequence_ceiling=2,
        child_delegation_depth_remaining=1,
    )

    root_after_ab = authority_snapshot(root)

    ab_record = delegation_record(
        test_id="EASA-F11-DELEGATION-A-B",
        observation_time=observation_time,
        parent_before=root_before_ab,
        parent_after=root_after_ab,
        result=ab_result,
    )

    write_json(
        AB_PATH,
        ab_record,
    )

    if ab_result.child_authority is None:

        summary = {
            "examination": "EASA-F11",
            "property":
                "DELEGATION_CHAIN_NON_AMPLIFICATION",
            "overall_result": "FAIL",
            "claim_state":
                "DEFINED_PROPERTY_NOT_ESTABLISHED_BY_FIRST_OBSERVATION",
            "failure_reason":
                "VALID_A_TO_B_DELEGATION_NOT_ISSUED",
        }

        write_json(
            SUMMARY_PATH,
            summary,
        )

        print(
            json.dumps(
                summary,
                indent=2,
                sort_keys=True,
            )
        )

        return 1

    authority_b = ab_result.child_authority

    # ========================================================
    # B ATTACK 1 — ACTION AMPLIFICATION
    # ========================================================

    b_before_action = authority_snapshot(
        authority_b
    )

    action_attack = delegation_gate.delegate(
        parent=authority_b,
        child_authority_id="AUTH_F11_BAD_ACTION",
        child_subject_identity="AGENT_C",
        child_actions=frozenset(
            {
                F11_STANDARD_WRITE,
                F11_ADMIN_WRITE,
            }
        ),
        child_tools=frozenset(
            {TOOL_F11_STANDARD}
        ),
        child_local_consequence_ceiling=1,
        child_delegation_depth_remaining=0,
    )

    b_after_action = authority_snapshot(
        authority_b
    )

    action_record = delegation_record(
        test_id="EASA-F11-ATTACK-ACTION-SCOPE",
        observation_time=observation_time,
        parent_before=b_before_action,
        parent_after=b_after_action,
        result=action_attack,
    )

    write_json(
        ATTACK_ACTION_PATH,
        action_record,
    )

    # ========================================================
    # B ATTACK 2 — TOOL AMPLIFICATION
    # ========================================================

    b_before_tool = authority_snapshot(
        authority_b
    )

    tool_attack = delegation_gate.delegate(
        parent=authority_b,
        child_authority_id="AUTH_F11_BAD_TOOL",
        child_subject_identity="AGENT_C",
        child_actions=frozenset(
            {F11_STANDARD_WRITE}
        ),
        child_tools=frozenset(
            {
                TOOL_F11_STANDARD,
                TOOL_F11_HIGH,
            }
        ),
        child_local_consequence_ceiling=1,
        child_delegation_depth_remaining=0,
    )

    b_after_tool = authority_snapshot(
        authority_b
    )

    tool_record = delegation_record(
        test_id="EASA-F11-ATTACK-TOOL-SCOPE",
        observation_time=observation_time,
        parent_before=b_before_tool,
        parent_after=b_after_tool,
        result=tool_attack,
    )

    write_json(
        ATTACK_TOOL_PATH,
        tool_record,
    )

    # ========================================================
    # B ATTACK 3 — LOCAL CEILING AMPLIFICATION
    # ========================================================

    b_before_ceiling = authority_snapshot(
        authority_b
    )

    ceiling_attack = delegation_gate.delegate(
        parent=authority_b,
        child_authority_id="AUTH_F11_BAD_CEILING",
        child_subject_identity="AGENT_C",
        child_actions=frozenset(
            {F11_STANDARD_WRITE}
        ),
        child_tools=frozenset(
            {TOOL_F11_STANDARD}
        ),
        child_local_consequence_ceiling=3,
        child_delegation_depth_remaining=0,
    )

    b_after_ceiling = authority_snapshot(
        authority_b
    )

    ceiling_record = delegation_record(
        test_id="EASA-F11-ATTACK-LOCAL-CEILING",
        observation_time=observation_time,
        parent_before=b_before_ceiling,
        parent_after=b_after_ceiling,
        result=ceiling_attack,
    )

    write_json(
        ATTACK_CEILING_PATH,
        ceiling_record,
    )

    # ========================================================
    # B ATTACK 4 — DELEGATION DEPTH AMPLIFICATION
    # ========================================================

    b_before_depth = authority_snapshot(
        authority_b
    )

    depth_attack = delegation_gate.delegate(
        parent=authority_b,
        child_authority_id="AUTH_F11_BAD_DEPTH",
        child_subject_identity="AGENT_C",
        child_actions=frozenset(
            {F11_STANDARD_WRITE}
        ),
        child_tools=frozenset(
            {TOOL_F11_STANDARD}
        ),
        child_local_consequence_ceiling=1,
        child_delegation_depth_remaining=1,
    )

    b_after_depth = authority_snapshot(
        authority_b
    )

    depth_record = delegation_record(
        test_id="EASA-F11-ATTACK-DELEGATION-DEPTH",
        observation_time=observation_time,
        parent_before=b_before_depth,
        parent_after=b_after_depth,
        result=depth_attack,
    )

    write_json(
        ATTACK_DEPTH_PATH,
        depth_record,
    )

    # ========================================================
    # VALID B -> C
    # ========================================================

    b_before_bc = authority_snapshot(
        authority_b
    )

    bc_result = delegation_gate.delegate(
        parent=authority_b,
        child_authority_id="AUTH_F11_C",
        child_subject_identity="AGENT_C",
        child_actions=frozenset(
            {F11_STANDARD_WRITE}
        ),
        child_tools=frozenset(
            {TOOL_F11_STANDARD}
        ),
        child_local_consequence_ceiling=1,
        child_delegation_depth_remaining=0,
    )

    b_after_bc = authority_snapshot(
        authority_b
    )

    bc_record = delegation_record(
        test_id="EASA-F11-DELEGATION-B-C",
        observation_time=observation_time,
        parent_before=b_before_bc,
        parent_after=b_after_bc,
        result=bc_result,
    )

    write_json(
        BC_PATH,
        bc_record,
    )

    if bc_result.child_authority is None:

        summary = {
            "examination": "EASA-F11",
            "property":
                "DELEGATION_CHAIN_NON_AMPLIFICATION",
            "overall_result": "FAIL",
            "claim_state":
                "DEFINED_PROPERTY_NOT_ESTABLISHED_BY_FIRST_OBSERVATION",
            "failure_reason":
                "VALID_B_TO_C_DELEGATION_NOT_ISSUED",
        }

        write_json(
            SUMMARY_PATH,
            summary,
        )

        print(
            json.dumps(
                summary,
                indent=2,
                sort_keys=True,
            )
        )

        return 1

    authority_c = bc_result.child_authority

    same_lineage_object = (
        root.lineage is authority_b.lineage
        and root.lineage is authority_c.lineage
    )

    # ========================================================
    # C ATTACK 5 — UNAUTHORIZED FURTHER DELEGATION
    # ========================================================

    c_before_cd = authority_snapshot(
        authority_c
    )

    cd_attack = delegation_gate.delegate(
        parent=authority_c,
        child_authority_id="AUTH_F11_D",
        child_subject_identity="AGENT_D",
        child_actions=frozenset(
            {F11_STANDARD_WRITE}
        ),
        child_tools=frozenset(
            {TOOL_F11_STANDARD}
        ),
        child_local_consequence_ceiling=1,
        child_delegation_depth_remaining=0,
    )

    c_after_cd = authority_snapshot(
        authority_c
    )

    cd_record = delegation_record(
        test_id="EASA-F11-ATTACK-C-D",
        observation_time=observation_time,
        parent_before=c_before_cd,
        parent_after=c_after_cd,
        result=cd_attack,
    )

    write_json(
        CD_PATH,
        cd_record,
    )

    # ========================================================
    # VERIFY NO DELEGATION ATTACK PRODUCED TOOL CONSEQUENCE
    # ========================================================

    standard_tool = ConsequentialTool(
        tool_identity=TOOL_F11_STANDARD,
        supported_actions=frozenset(
            {F11_STANDARD_WRITE}
        ),
    )

    high_tool = ConsequentialTool(
        tool_identity=TOOL_F11_HIGH,
        supported_actions=frozenset(
            {
                F11_STANDARD_WRITE,
                F11_ADMIN_WRITE,
            }
        ),
    )

    tool_counters_before_execution = {
        "standard":
            standard_tool.consequence_counter,
        "high":
            high_tool.consequence_counter,
    }

    # ========================================================
    # LINEAGE EXECUTION
    # ========================================================

    execution_gate = LineageExecutionGate()

    execution_results = []

    c1 = execution_gate.attempt(
        authority=authority_c,
        presenter_identity="AGENT_C",
        action=F11_STANDARD_WRITE,
        target_tool=standard_tool,
    )

    execution_results.append(
        execution_record(
            test_id="EASA-F11-EXEC-C-001",
            observation_time=observation_time,
            result=c1,
        )
    )

    b1 = execution_gate.attempt(
        authority=authority_b,
        presenter_identity="AGENT_B",
        action=F11_STANDARD_WRITE,
        target_tool=standard_tool,
    )

    execution_results.append(
        execution_record(
            test_id="EASA-F11-EXEC-B-001",
            observation_time=observation_time,
            result=b1,
        )
    )

    b2 = execution_gate.attempt(
        authority=authority_b,
        presenter_identity="AGENT_B",
        action=F11_STANDARD_WRITE,
        target_tool=standard_tool,
    )

    execution_results.append(
        execution_record(
            test_id="EASA-F11-EXEC-B-002",
            observation_time=observation_time,
            result=b2,
        )
    )

    a1 = execution_gate.attempt(
        authority=root,
        presenter_identity="AGENT_A",
        action=F11_STANDARD_WRITE,
        target_tool=standard_tool,
    )

    execution_results.append(
        execution_record(
            test_id="EASA-F11-EXEC-A-001",
            observation_time=observation_time,
            result=a1,
        )
    )

    a2 = execution_gate.attempt(
        authority=root,
        presenter_identity="AGENT_A",
        action=F11_STANDARD_WRITE,
        target_tool=standard_tool,
    )

    execution_results.append(
        execution_record(
            test_id="EASA-F11-EXEC-A-LINEAGE-CEILING",
            observation_time=observation_time,
            result=a2,
        )
    )

    execution_record_value = {
        "examination":
            "EASA-F11",
        "record_type":
            "LINEAGE_EXECUTION",
        "observation_time_utc":
            observation_time,
        "same_lineage_runtime_object":
            same_lineage_object,
        "tool_counters_before_execution":
            tool_counters_before_execution,
        "execution_results":
            execution_results,
        "final_authorities": {
            "root":
                authority_snapshot(root),
            "b":
                authority_snapshot(authority_b),
            "c":
                authority_snapshot(authority_c),
        },
        "final_lineage": {
            "lineage_id":
                lineage.lineage_id,
            "consequence_ceiling":
                lineage.consequence_ceiling,
            "consequence_count":
                lineage.consequence_count,
        },
        "final_tool_counters": {
            "standard":
                standard_tool.consequence_counter,
            "high":
                high_tool.consequence_counter,
        },
    }

    write_json(
        EXECUTION_PATH,
        execution_record_value,
    )

    # ========================================================
    # AGGREGATE CHECKS
    # ========================================================

    rejected_b_records = (
        action_record,
        tool_record,
        ceiling_record,
        depth_record,
    )

    rejected_b_results = (
        action_attack,
        tool_attack,
        ceiling_attack,
        depth_attack,
    )

    checks = {

        "root_subject_agent_a":
            root.subject_identity == "AGENT_A",

        "root_actions_correct":
            root.authorized_actions
            == frozenset(
                {
                    F11_STANDARD_WRITE,
                    F11_ADMIN_WRITE,
                }
            ),

        "root_tools_correct":
            root.authorized_tools
            == frozenset(
                {
                    TOOL_F11_STANDARD,
                    TOOL_F11_HIGH,
                }
            ),

        "root_local_ceiling_4":
            root.local_consequence_ceiling == 4,

        "root_depth_2":
            root.delegation_depth_remaining == 2,

        "root_lineage_correct":
            root.lineage.lineage_id
            == "LINEAGE_F11_001",

        "root_lineage_ceiling_4":
            root.lineage.consequence_ceiling == 4,

        "ab_delegation_permitted":
            ab_result.decision.verdict == "PERMIT",

        "ab_child_issued":
            ab_result.child_authority is not None,

        "b_subject_agent_b":
            authority_b.subject_identity == "AGENT_B",

        "b_actions_exact":
            authority_b.authorized_actions
            == frozenset({F11_STANDARD_WRITE}),

        "b_tools_exact":
            authority_b.authorized_tools
            == frozenset({TOOL_F11_STANDARD}),

        "b_local_ceiling_2":
            authority_b.local_consequence_ceiling == 2,

        "b_depth_1":
            authority_b.delegation_depth_remaining == 1,

        "b_lineage_correct":
            authority_b.lineage.lineage_id
            == "LINEAGE_F11_001",

        "action_amplification_refused":
            action_attack.decision.verdict
            == "REFUSE",

        "action_amplification_reason":
            action_attack.decision.reason
            == "DELEGATION_ACTION_SCOPE_AMPLIFICATION",

        "action_amplification_no_child":
            action_attack.child_authority is None,

        "tool_amplification_refused":
            tool_attack.decision.verdict
            == "REFUSE",

        "tool_amplification_reason":
            tool_attack.decision.reason
            == "DELEGATION_TOOL_SCOPE_AMPLIFICATION",

        "tool_amplification_no_child":
            tool_attack.child_authority is None,

        "ceiling_amplification_refused":
            ceiling_attack.decision.verdict
            == "REFUSE",

        "ceiling_amplification_reason":
            ceiling_attack.decision.reason
            == "DELEGATION_CONSEQUENCE_CEILING_AMPLIFICATION",

        "ceiling_amplification_no_child":
            ceiling_attack.child_authority is None,

        "depth_amplification_refused":
            depth_attack.decision.verdict
            == "REFUSE",

        "depth_amplification_reason":
            depth_attack.decision.reason
            == "DELEGATION_DEPTH_AMPLIFICATION",

        "depth_amplification_no_child":
            depth_attack.child_authority is None,

        "all_rejected_b_requests_preserve_parent":
            all(
                record["parent_unchanged"]
                for record
                in rejected_b_records
            ),

        "bc_delegation_permitted":
            bc_result.decision.verdict == "PERMIT",

        "bc_child_issued":
            bc_result.child_authority is not None,

        "c_subject_agent_c":
            authority_c.subject_identity == "AGENT_C",

        "c_actions_exact":
            authority_c.authorized_actions
            == frozenset({F11_STANDARD_WRITE}),

        "c_tools_exact":
            authority_c.authorized_tools
            == frozenset({TOOL_F11_STANDARD}),

        "c_local_ceiling_1":
            authority_c.local_consequence_ceiling == 1,

        "c_depth_0":
            authority_c.delegation_depth_remaining == 0,

        "c_lineage_correct":
            authority_c.lineage.lineage_id
            == "LINEAGE_F11_001",

        "cd_delegation_refused":
            cd_attack.decision.verdict == "REFUSE",

        "cd_reason_no_delegation_authority":
            cd_attack.decision.reason
            == "DELEGATION_AUTHORITY_NOT_PRESENT",

        "cd_no_child_issued":
            cd_attack.child_authority is None,

        "cd_rejection_preserves_c":
            cd_record["parent_unchanged"] is True,

        "same_lineage_runtime_object":
            same_lineage_object,

        "delegation_attacks_produced_no_tool_consequence":
            (
                tool_counters_before_execution["standard"] == 0
                and
                tool_counters_before_execution["high"] == 0
            ),

        "c_first_permitted":
            c1.verdict == "PERMIT",

        "c_first_authorized":
            c1.reason == "AUTHORIZED",

        "c_local_count_after_1":
            c1.local_count_after == 1,

        "lineage_after_c_1":
            c1.lineage_count_after == 1,

        "b_first_permitted":
            b1.verdict == "PERMIT",

        "b_second_permitted":
            b2.verdict == "PERMIT",

        "b_local_count_after_2":
            b2.local_count_after == 2,

        "lineage_after_b_3":
            b2.lineage_count_after == 3,

        "a_first_permitted":
            a1.verdict == "PERMIT",

        "a_local_count_after_1":
            a1.local_count_after == 1,

        "lineage_after_a_4":
            a1.lineage_count_after == 4,

        "a_second_refused":
            a2.verdict == "REFUSE",

        "a_second_lineage_reason":
            a2.reason
            == "LINEAGE_CONSEQUENCE_CEILING_EXHAUSTED",

        "a_second_delta_zero":
            a2.consequence_delta == 0,

        "a_local_not_exhausted_at_lineage_refusal":
            (
                a2.local_count_before
                < a2.local_ceiling
            ),

        "final_lineage_count_4":
            lineage.consequence_count == 4,

        "final_lineage_ceiling_4":
            lineage.consequence_ceiling == 4,

        "standard_tool_final_counter_4":
            standard_tool.consequence_counter == 4,

        "high_tool_final_counter_0":
            high_tool.consequence_counter == 0,

        "root_local_count_1":
            root.local_consequence_count == 1,

        "b_local_count_2":
            authority_b.local_consequence_count == 2,

        "c_local_count_1":
            authority_c.local_consequence_count == 1,

        "valid_children_no_broader_than_parent":
            (
                authority_b.authorized_actions.issubset(
                    root.authorized_actions
                )
                and
                authority_b.authorized_tools.issubset(
                    root.authorized_tools
                )
                and
                authority_b.local_consequence_ceiling
                <= root.local_consequence_ceiling
                and
                authority_b.delegation_depth_remaining
                < root.delegation_depth_remaining
                and
                authority_c.authorized_actions.issubset(
                    authority_b.authorized_actions
                )
                and
                authority_c.authorized_tools.issubset(
                    authority_b.authorized_tools
                )
                and
                authority_c.local_consequence_ceiling
                <= authority_b.local_consequence_ceiling
                and
                authority_c.delegation_depth_remaining
                < authority_b.delegation_depth_remaining
            ),

        "delegation_did_not_multiply_lineage_budget":
            (
                root.lineage is authority_b.lineage
                and
                root.lineage is authority_c.lineage
                and
                root.lineage.consequence_ceiling == 4
                and
                root.lineage.consequence_count == 4
            ),
    }

    overall_pass = all(checks.values())

    summary = {
        "examination":
            "EASA-F11",
        "property":
            "DELEGATION_CHAIN_NON_AMPLIFICATION",
        "observation_time_utc":
            observation_time,
        "root_authority":
            "AUTH_F11_A_ROOT",
        "valid_delegation_chain": [
            "AUTH_F11_A_ROOT",
            "AUTH_F11_B",
            "AUTH_F11_C",
        ],
        "lineage_id":
            lineage.lineage_id,
        "lineage_consequence_ceiling":
            lineage.consequence_ceiling,
        "lineage_consequence_count":
            lineage.consequence_count,
        "same_lineage_runtime_object":
            same_lineage_object,
        "rejected_delegation_reasons": [
            action_attack.decision.reason,
            tool_attack.decision.reason,
            ceiling_attack.decision.reason,
            depth_attack.decision.reason,
            cd_attack.decision.reason,
        ],
        "valid_execution_verdicts": {
            "c1": c1.verdict,
            "b1": b1.verdict,
            "b2": b2.verdict,
            "a1": a1.verdict,
        },
        "lineage_ceiling_challenge": {
            "verdict": a2.verdict,
            "reason": a2.reason,
            "consequence_delta":
                a2.consequence_delta,
            "local_count_before":
                a2.local_count_before,
            "local_ceiling":
                a2.local_ceiling,
            "lineage_count_before":
                a2.lineage_count_before,
            "lineage_ceiling":
                a2.lineage_ceiling,
        },
        "final_local_counts": {
            "A":
                root.local_consequence_count,
            "B":
                authority_b.local_consequence_count,
            "C":
                authority_c.local_consequence_count,
        },
        "final_tool_counters": {
            "standard":
                standard_tool.consequence_counter,
            "high":
                high_tool.consequence_counter,
        },
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

    print("=== EASA-F11 FIRST OBSERVATION ===")
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