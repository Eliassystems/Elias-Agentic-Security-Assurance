from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = ROOT / "03_controls"

if str(CONTROL_DIR) not in sys.path:
    sys.path.insert(0, str(CONTROL_DIR))

from easa_f10_control import (  # noqa: E402
    F10_ACTION,
    TOOL_HIGH,
    TOOL_LOW,
    TOOL_PEER,
    ConsequentialTool,
    ContainmentExecutionGate,
    ExecutionAuthority,
    GovernanceState,
)


EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F10"

PRE_STATE_PATH = (
    EVIDENCE_DIR / "EASA-F10-PRE-ATTACK-STATE.json"
)

BORROWED_PATH = (
    EVIDENCE_DIR / "EASA-F10-ATTACK-BORROWED-001.json"
)

STALE_PATH = (
    EVIDENCE_DIR / "EASA-F10-ATTACK-STALE-001.json"
)

ESCALATION_PATH = (
    EVIDENCE_DIR / "EASA-F10-ATTACK-ESCALATION-001.json"
)

POST_ATTACK_STATE_PATH = (
    EVIDENCE_DIR / "EASA-F10-POST-ATTACK-STATE.json"
)

PEER_POSITIVE_PATH = (
    EVIDENCE_DIR / "EASA-F10-PEER-POS-001.json"
)

LOW_POSITIVE_PATH = (
    EVIDENCE_DIR / "EASA-F10-LOW-POS-001.json"
)

SUMMARY_PATH = (
    EVIDENCE_DIR / "EASA-F10-SUMMARY.json"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def authority_snapshot(authority: ExecutionAuthority) -> dict:
    return {
        "authority_id": authority.authority_id,
        "subject_identity": authority.subject_identity,
        "authority_epoch": authority.authority_epoch,
        "bound_tool_identity": authority.bound_tool_identity,
        "authorized_actions": sorted(authority.authorized_actions),
        "valid": authority.valid,
        "consumed": authority.consumed,
    }


def governance_snapshot(governance: GovernanceState) -> dict:
    return {
        "current_epoch": governance.current_epoch,
        "revoked_epochs": sorted(governance.revoked_epochs),
    }


def tool_snapshot(tools: dict[str, ConsequentialTool]) -> dict:
    return {
        name: {
            "tool_identity": tool.tool_identity,
            "consequence_counter": tool.consequence_counter,
        }
        for name, tool in tools.items()
    }


def result_record(
    *,
    test_id: str,
    observation_time: str,
    result,
) -> dict:

    return {
        "test_id": test_id,
        "observation_time_utc": observation_time,
        "presenter_identity": result.presenter_identity,
        "authority_id": result.authority_id,
        "authority_subject_identity":
            result.authority_subject_identity,
        "authority_epoch": result.authority_epoch,
        "authority_tool_identity":
            result.authority_tool_identity,
        "target_tool_identity":
            result.target_tool_identity,
        "action": result.action,
        "governing_current_epoch":
            result.governing_current_epoch,
        "authority_epoch_revoked":
            result.authority_epoch_revoked,
        "verdict": result.verdict,
        "reason": result.reason,
        "authority_consumed_before":
            result.authority_consumed_before,
        "authority_consumed_after":
            result.authority_consumed_after,
        "consequence_before":
            result.consequence_before,
        "consequence_after":
            result.consequence_after,
        "consequence_delta":
            result.consequence_delta,
    }


def main() -> int:

    targets = (
        PRE_STATE_PATH,
        BORROWED_PATH,
        STALE_PATH,
        ESCALATION_PATH,
        POST_ATTACK_STATE_PATH,
        PEER_POSITIVE_PATH,
        LOW_POSITIVE_PATH,
        SUMMARY_PATH,
    )

    existing = [
        str(path)
        for path in targets
        if path.exists()
    ]

    if existing:

        print("FIRST OBSERVATION EVIDENCE ALREADY EXISTS — STOP")

        for path in existing:
            print(path)

        return 2

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    observation_time = now_utc()

    governance = GovernanceState(
        current_epoch=2,
        revoked_epochs={1},
    )

    tools = {
        "PEER": ConsequentialTool(TOOL_PEER),
        "LOW": ConsequentialTool(TOOL_LOW),
        "HIGH": ConsequentialTool(TOOL_HIGH),
    }

    peer_authority = ExecutionAuthority(
        authority_id="AUTH_F10_PEER_A",
        subject_identity="AGENT_A",
        authority_epoch=2,
        bound_tool_identity=TOOL_PEER,
        authorized_actions=frozenset({F10_ACTION}),
        valid=True,
        consumed=False,
    )

    stale_authority = ExecutionAuthority(
        authority_id="AUTH_F10_X_STALE_E1",
        subject_identity="AGENT_X",
        authority_epoch=1,
        bound_tool_identity=TOOL_LOW,
        authorized_actions=frozenset({F10_ACTION}),
        valid=True,
        consumed=False,
    )

    low_authority = ExecutionAuthority(
        authority_id="AUTH_F10_X_LOW_E2",
        subject_identity="AGENT_X",
        authority_epoch=2,
        bound_tool_identity=TOOL_LOW,
        authorized_actions=frozenset({F10_ACTION}),
        valid=True,
        consumed=False,
    )

    # Exact runtime references are retained for post-attack reuse.
    peer_attack_reference = peer_authority
    peer_positive_reference = peer_authority

    low_escalation_reference = low_authority
    low_positive_reference = low_authority

    same_peer_runtime_object = (
        peer_attack_reference is peer_positive_reference
        and peer_attack_reference is peer_authority
    )

    same_low_runtime_object = (
        low_escalation_reference is low_positive_reference
        and low_escalation_reference is low_authority
    )

    pre_attack_state = {
        "examination": "EASA-F10",
        "record_type": "PRE_ATTACK_STATE",
        "observation_time_utc": observation_time,
        "compromised_agent": "AGENT_X",
        "legitimate_peer": "AGENT_A",
        "governance": governance_snapshot(governance),
        "authorities": {
            "peer": authority_snapshot(peer_authority),
            "stale": authority_snapshot(stale_authority),
            "low": authority_snapshot(low_authority),
        },
        "tools": tool_snapshot(tools),
        "same_peer_runtime_object_reserved_for_reuse":
            same_peer_runtime_object,
        "same_low_runtime_object_reserved_for_reuse":
            same_low_runtime_object,
    }

    write_json(PRE_STATE_PATH, pre_attack_state)

    gate = ContainmentExecutionGate()

    # ========================================================
    # ATTACK 1 — BORROWED PEER AUTHORITY
    # ========================================================

    peer_before_borrowed = authority_snapshot(peer_authority)

    borrowed_result = gate.attempt(
        governance=governance,
        authority=peer_attack_reference,
        presenter_identity="AGENT_X",
        action=F10_ACTION,
        target_tool=tools["PEER"],
    )

    peer_after_borrowed = authority_snapshot(peer_authority)

    borrowed_record = result_record(
        test_id="EASA-F10-ATTACK-BORROWED-001",
        observation_time=observation_time,
        result=borrowed_result,
    )

    borrowed_record.update(
        {
            "attack_path": "BORROWED_PEER_AUTHORITY",
            "compromised_agent": "AGENT_X",
            "authority_owner": "AGENT_A",
            "peer_authority_before":
                peer_before_borrowed,
            "peer_authority_after":
                peer_after_borrowed,
            "peer_authority_unchanged":
                peer_before_borrowed
                == peer_after_borrowed,
            "same_authority_reserved_for_peer_positive":
                same_peer_runtime_object,
        }
    )

    write_json(BORROWED_PATH, borrowed_record)

    # ========================================================
    # ATTACK 2 — STALE EPOCH-1 AUTHORITY
    # ========================================================

    stale_before = authority_snapshot(stale_authority)

    stale_result = gate.attempt(
        governance=governance,
        authority=stale_authority,
        presenter_identity="AGENT_X",
        action=F10_ACTION,
        target_tool=tools["LOW"],
    )

    stale_after = authority_snapshot(stale_authority)

    stale_record = result_record(
        test_id="EASA-F10-ATTACK-STALE-001",
        observation_time=observation_time,
        result=stale_result,
    )

    stale_record.update(
        {
            "attack_path": "SUPERSEDED_EPOCH_AUTHORITY",
            "authority_before": stale_before,
            "authority_after": stale_after,
            "authority_unchanged":
                stale_before == stale_after,
        }
    )

    write_json(STALE_PATH, stale_record)

    # ========================================================
    # ATTACK 3 — TOOL PRIVILEGE ESCALATION
    # ========================================================

    low_before_escalation = authority_snapshot(low_authority)

    escalation_result = gate.attempt(
        governance=governance,
        authority=low_escalation_reference,
        presenter_identity="AGENT_X",
        action=F10_ACTION,
        target_tool=tools["HIGH"],
    )

    low_after_escalation = authority_snapshot(low_authority)

    escalation_record = result_record(
        test_id="EASA-F10-ATTACK-ESCALATION-001",
        observation_time=observation_time,
        result=escalation_result,
    )

    escalation_record.update(
        {
            "attack_path": "HIGH_TOOL_ESCALATION",
            "authority_before":
                low_before_escalation,
            "authority_after":
                low_after_escalation,
            "authority_unchanged":
                low_before_escalation
                == low_after_escalation,
            "same_authority_reserved_for_low_positive":
                same_low_runtime_object,
        }
    )

    write_json(ESCALATION_PATH, escalation_record)

    # ========================================================
    # POST-ATTACK / PRE-POSITIVE STATE
    # ========================================================

    post_attack_state = {
        "examination": "EASA-F10",
        "record_type":
            "POST_ATTACK_PRE_POSITIVE_STATE",
        "observation_time_utc": observation_time,
        "governance": governance_snapshot(governance),
        "authorities": {
            "peer": authority_snapshot(peer_authority),
            "stale": authority_snapshot(stale_authority),
            "low": authority_snapshot(low_authority),
        },
        "tools": tool_snapshot(tools),
        "same_peer_runtime_object":
            same_peer_runtime_object,
        "same_low_runtime_object":
            same_low_runtime_object,
    }

    write_json(
        POST_ATTACK_STATE_PATH,
        post_attack_state,
    )

    # ========================================================
    # POST-ATTACK PEER INTEGRITY POSITIVE
    # EXACT SAME AUTHORITY OBJECT
    # ========================================================

    peer_positive_result = gate.attempt(
        governance=governance,
        authority=peer_positive_reference,
        presenter_identity="AGENT_A",
        action=F10_ACTION,
        target_tool=tools["PEER"],
    )

    peer_positive_record = result_record(
        test_id="EASA-F10-PEER-POS-001",
        observation_time=observation_time,
        result=peer_positive_result,
    )

    peer_positive_record.update(
        {
            "case":
                "POST_ATTACK_PEER_INTEGRITY_POSITIVE",
            "same_runtime_authority_object_as_borrowed_attack":
                same_peer_runtime_object,
            "peer_authority_final":
                authority_snapshot(peer_authority),
        }
    )

    write_json(
        PEER_POSITIVE_PATH,
        peer_positive_record,
    )

    # ========================================================
    # POST-ATTACK LOW-BOUNDARY POSITIVE
    # EXACT SAME AUTHORITY OBJECT
    # ========================================================

    low_positive_result = gate.attempt(
        governance=governance,
        authority=low_positive_reference,
        presenter_identity="AGENT_X",
        action=F10_ACTION,
        target_tool=tools["LOW"],
    )

    low_positive_record = result_record(
        test_id="EASA-F10-LOW-POS-001",
        observation_time=observation_time,
        result=low_positive_result,
    )

    low_positive_record.update(
        {
            "case":
                "POST_ATTACK_LOW_BOUNDARY_POSITIVE",
            "same_runtime_authority_object_as_escalation_attack":
                same_low_runtime_object,
            "low_authority_final":
                authority_snapshot(low_authority),
        }
    )

    write_json(
        LOW_POSITIVE_PATH,
        low_positive_record,
    )

    # ========================================================
    # FINAL STATE + CHECKS
    # ========================================================

    final_governance = governance_snapshot(governance)

    final_authorities = {
        "peer": authority_snapshot(peer_authority),
        "stale": authority_snapshot(stale_authority),
        "low": authority_snapshot(low_authority),
    }

    final_tools = tool_snapshot(tools)

    unauthorized_delta = sum(
        (
            borrowed_result.consequence_delta,
            stale_result.consequence_delta,
            escalation_result.consequence_delta,
        )
    )

    peer_binding_unchanged_after_attacks = (
        post_attack_state["authorities"]["peer"]["subject_identity"]
        == pre_attack_state["authorities"]["peer"]["subject_identity"]
        and
        post_attack_state["authorities"]["peer"]["authority_epoch"]
        == pre_attack_state["authorities"]["peer"]["authority_epoch"]
        and
        post_attack_state["authorities"]["peer"]["bound_tool_identity"]
        == pre_attack_state["authorities"]["peer"]["bound_tool_identity"]
        and
        post_attack_state["authorities"]["peer"]["authorized_actions"]
        == pre_attack_state["authorities"]["peer"]["authorized_actions"]
        and
        post_attack_state["authorities"]["peer"]["valid"]
        == pre_attack_state["authorities"]["peer"]["valid"]
    )

    low_binding_unchanged_after_attack = (
        post_attack_state["authorities"]["low"]["subject_identity"]
        == pre_attack_state["authorities"]["low"]["subject_identity"]
        and
        post_attack_state["authorities"]["low"]["authority_epoch"]
        == pre_attack_state["authorities"]["low"]["authority_epoch"]
        and
        post_attack_state["authorities"]["low"]["bound_tool_identity"]
        == pre_attack_state["authorities"]["low"]["bound_tool_identity"]
        and
        post_attack_state["authorities"]["low"]["authorized_actions"]
        == pre_attack_state["authorities"]["low"]["authorized_actions"]
        and
        post_attack_state["authorities"]["low"]["valid"]
        == pre_attack_state["authorities"]["low"]["valid"]
    )

    governance_unchanged_after_attacks = (
        post_attack_state["governance"]
        == pre_attack_state["governance"]
    )

    checks = {

        "current_epoch_started_2":
            pre_attack_state["governance"]["current_epoch"] == 2,

        "epoch_1_started_revoked":
            pre_attack_state["governance"]["revoked_epochs"] == [1],

        "peer_authority_started_valid":
            pre_attack_state["authorities"]["peer"]["valid"] is True,

        "peer_authority_started_unconsumed":
            pre_attack_state["authorities"]["peer"]["consumed"] is False,

        "peer_authority_bound_agent_a":
            pre_attack_state["authorities"]["peer"]["subject_identity"]
            == "AGENT_A",

        "peer_authority_bound_peer_tool":
            pre_attack_state["authorities"]["peer"]["bound_tool_identity"]
            == TOOL_PEER,

        "stale_authority_started_valid":
            pre_attack_state["authorities"]["stale"]["valid"] is True,

        "stale_authority_started_unconsumed":
            pre_attack_state["authorities"]["stale"]["consumed"] is False,

        "stale_authority_epoch_1":
            pre_attack_state["authorities"]["stale"]["authority_epoch"]
            == 1,

        "stale_authority_correct_subject":
            pre_attack_state["authorities"]["stale"]["subject_identity"]
            == "AGENT_X",

        "stale_authority_correct_tool":
            pre_attack_state["authorities"]["stale"]["bound_tool_identity"]
            == TOOL_LOW,

        "low_authority_started_valid":
            pre_attack_state["authorities"]["low"]["valid"] is True,

        "low_authority_started_unconsumed":
            pre_attack_state["authorities"]["low"]["consumed"] is False,

        "low_authority_epoch_2":
            pre_attack_state["authorities"]["low"]["authority_epoch"]
            == 2,

        "low_authority_correct_subject":
            pre_attack_state["authorities"]["low"]["subject_identity"]
            == "AGENT_X",

        "low_authority_bound_low_tool":
            pre_attack_state["authorities"]["low"]["bound_tool_identity"]
            == TOOL_LOW,

        "borrowed_attack_refused":
            borrowed_result.verdict == "REFUSE",

        "borrowed_reason_identity_mismatch":
            borrowed_result.reason
            == "PRESENTER_IDENTITY_MISMATCH",

        "borrowed_delta_zero":
            borrowed_result.consequence_delta == 0,

        "peer_authority_unconsumed_after_borrowed":
            borrowed_result.authority_consumed_after is False,

        "peer_authority_unchanged_after_borrowed":
            borrowed_record["peer_authority_unchanged"] is True,

        "stale_attack_refused":
            stale_result.verdict == "REFUSE",

        "stale_reason_epoch_revoked":
            stale_result.reason
            == "AUTHORITY_EPOCH_REVOKED",

        "stale_delta_zero":
            stale_result.consequence_delta == 0,

        "stale_remained_unconsumed":
            stale_result.authority_consumed_after is False,

        "stale_authority_unchanged":
            stale_record["authority_unchanged"] is True,

        "escalation_refused":
            escalation_result.verdict == "REFUSE",

        "escalation_reason_tool_mismatch":
            escalation_result.reason
            == "TOOL_IDENTITY_MISMATCH",

        "escalation_delta_zero":
            escalation_result.consequence_delta == 0,

        "low_authority_unconsumed_after_escalation":
            escalation_result.authority_consumed_after is False,

        "low_authority_unchanged_after_escalation":
            escalation_record["authority_unchanged"] is True,

        "unauthorized_total_delta_zero":
            unauthorized_delta == 0,

        "governance_unchanged_after_attacks":
            governance_unchanged_after_attacks,

        "current_epoch_remains_2_after_attacks":
            post_attack_state["governance"]["current_epoch"] == 2,

        "revoked_epoch_set_remains_1":
            post_attack_state["governance"]["revoked_epochs"] == [1],

        "peer_binding_unchanged_after_attacks":
            peer_binding_unchanged_after_attacks,

        "low_binding_unchanged_after_attack":
            low_binding_unchanged_after_attack,

        "same_peer_authority_object_reused":
            same_peer_runtime_object,

        "peer_positive_permitted":
            peer_positive_result.verdict == "PERMIT",

        "peer_positive_reason_authorized":
            peer_positive_result.reason == "AUTHORIZED",

        "peer_positive_delta_one":
            peer_positive_result.consequence_delta == 1,

        "peer_authority_consumed_only_after_legitimate_use":
            (
                post_attack_state["authorities"]["peer"]["consumed"]
                is False
                and
                peer_positive_result.authority_consumed_after
                is True
            ),

        "same_low_authority_object_reused":
            same_low_runtime_object,

        "low_positive_permitted":
            low_positive_result.verdict == "PERMIT",

        "low_positive_reason_authorized":
            low_positive_result.reason == "AUTHORIZED",

        "low_positive_delta_one":
            low_positive_result.consequence_delta == 1,

        "low_authority_consumed_only_after_legitimate_use":
            (
                post_attack_state["authorities"]["low"]["consumed"]
                is False
                and
                low_positive_result.authority_consumed_after
                is True
            ),

        "high_tool_final_counter_zero":
            final_tools["HIGH"]["consequence_counter"] == 0,

        "peer_tool_final_counter_one":
            final_tools["PEER"]["consequence_counter"] == 1,

        "low_tool_final_counter_one":
            final_tools["LOW"]["consequence_counter"] == 1,

        "stale_authority_final_unconsumed":
            final_authorities["stale"]["consumed"] is False,

        "final_governance_epoch_2":
            final_governance["current_epoch"] == 2,

        "final_revoked_epochs_1":
            final_governance["revoked_epochs"] == [1],

        "malicious_failures_conferred_no_new_authority":
            (
                unauthorized_delta == 0
                and peer_binding_unchanged_after_attacks
                and low_binding_unchanged_after_attack
                and governance_unchanged_after_attacks
                and final_tools["HIGH"]["consequence_counter"] == 0
            ),
    }

    overall_pass = all(checks.values())

    summary = {
        "examination": "EASA-F10",
        "property": "COMPROMISED_AGENT_CONTAINMENT",
        "observation_time_utc": observation_time,
        "compromised_agent": "AGENT_X",
        "legitimate_peer": "AGENT_A",
        "attack_tests": [
            "EASA-F10-ATTACK-BORROWED-001",
            "EASA-F10-ATTACK-STALE-001",
            "EASA-F10-ATTACK-ESCALATION-001",
        ],
        "post_attack_positive_tests": [
            "EASA-F10-PEER-POS-001",
            "EASA-F10-LOW-POS-001",
        ],
        "borrowed_attack": {
            "verdict": borrowed_result.verdict,
            "reason": borrowed_result.reason,
            "consequence_delta":
                borrowed_result.consequence_delta,
        },
        "stale_attack": {
            "verdict": stale_result.verdict,
            "reason": stale_result.reason,
            "consequence_delta":
                stale_result.consequence_delta,
        },
        "escalation_attack": {
            "verdict": escalation_result.verdict,
            "reason": escalation_result.reason,
            "consequence_delta":
                escalation_result.consequence_delta,
        },
        "unauthorized_total_consequence_delta":
            unauthorized_delta,
        "governance_unchanged_after_attacks":
            governance_unchanged_after_attacks,
        "peer_binding_unchanged_after_attacks":
            peer_binding_unchanged_after_attacks,
        "low_binding_unchanged_after_attack":
            low_binding_unchanged_after_attack,
        "same_peer_runtime_authority_reused":
            same_peer_runtime_object,
        "same_low_runtime_authority_reused":
            same_low_runtime_object,
        "peer_positive": {
            "verdict": peer_positive_result.verdict,
            "reason": peer_positive_result.reason,
            "consequence_delta":
                peer_positive_result.consequence_delta,
        },
        "low_positive": {
            "verdict": low_positive_result.verdict,
            "reason": low_positive_result.reason,
            "consequence_delta":
                low_positive_result.consequence_delta,
        },
        "final_governance": final_governance,
        "final_authorities": final_authorities,
        "final_tools": final_tools,
        "checks": checks,
        "overall_result":
            "PASS" if overall_pass else "FAIL",
        "claim_state":
            "OBSERVATION_SUPPORTS_DEFINED_PROPERTY"
            if overall_pass
            else "DEFINED_PROPERTY_NOT_ESTABLISHED_BY_FIRST_OBSERVATION",
    }

    write_json(SUMMARY_PATH, summary)

    print("=== EASA-F10 FIRST OBSERVATION ===")
    print(json.dumps(summary, indent=2, sort_keys=True))

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())