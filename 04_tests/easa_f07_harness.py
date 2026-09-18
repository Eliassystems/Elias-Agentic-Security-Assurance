from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = ROOT / "03_controls"

if str(CONTROL_DIR) not in sys.path:
    sys.path.insert(0, str(CONTROL_DIR))

from easa_f07_control import (  # noqa: E402
    ConsequentialTool,
    ExecutionAuthority,
    SHARED_ACTION,
    ToolBoundExecutionGate,
)


EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F07"

POSITIVE_PATH = EVIDENCE_DIR / "EASA-F07-POS-001.json"
NEGATIVE_PATH = EVIDENCE_DIR / "EASA-F07-NEG-001.json"
SUMMARY_PATH = EVIDENCE_DIR / "EASA-F07-SUMMARY.json"


def write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:

    evidence_targets = (
        POSITIVE_PATH,
        NEGATIVE_PATH,
        SUMMARY_PATH,
    )

    existing = [
        str(path)
        for path in evidence_targets
        if path.exists()
    ]

    if existing:
        print("FIRST OBSERVATION EVIDENCE ALREADY EXISTS — STOP")

        for path in existing:
            print(path)

        return 2

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    observation_time = datetime.now(timezone.utc).isoformat()

    gate = ToolBoundExecutionGate()

    tool_a = ConsequentialTool("TOOL_A")
    tool_b = ConsequentialTool("TOOL_B")

    # --------------------------------------------------------
    # POSITIVE CONTROL
    #
    # Authority bound to TOOL_A.
    # AGENT_A presents it to TOOL_A.
    # --------------------------------------------------------

    positive_authority = ExecutionAuthority(
        authority_id="AUTH_F07_POS",
        subject_identity="AGENT_A",
        bound_tool_identity="TOOL_A",
        authorized_actions=frozenset({SHARED_ACTION}),
        valid=True,
        consumed=False,
        governing_state_valid=True,
    )

    pos_tool_a_before = tool_a.consequence_counter
    pos_tool_b_before = tool_b.consequence_counter

    positive = gate.attempt(
        authority=positive_authority,
        presenter_identity="AGENT_A",
        action=SHARED_ACTION,
        target_tool=tool_a,
    )

    pos_tool_a_after = tool_a.consequence_counter
    pos_tool_b_after = tool_b.consequence_counter

    positive_record = {
        "test_id": "EASA-F07-POS-001",
        "observation_time_utc": observation_time,
        "case": "MATCHING_BOUND_AND_TARGET_TOOL",
        "authority_id": positive.authority_id,
        "authority_subject_identity": positive.subject_identity,
        "presenter_identity": positive.presenter_identity,
        "authority_tool_identity": positive.authority_tool_identity,
        "target_tool_identity": positive.target_tool_identity,
        "action": positive.action,
        "action_authorized_before": True,
        "authority_valid_before": True,
        "authority_governing_state_valid_before": True,
        "authority_consumed_before": positive.authority_consumed_before,
        "authority_consumed_after": positive.authority_consumed_after,
        "verdict": positive.verdict,
        "reason": positive.reason,
        "tool_a_consequence_before": pos_tool_a_before,
        "tool_a_consequence_after": pos_tool_a_after,
        "tool_a_consequence_delta": (
            pos_tool_a_after - pos_tool_a_before
        ),
        "tool_b_consequence_before": pos_tool_b_before,
        "tool_b_consequence_after": pos_tool_b_after,
        "tool_b_consequence_delta": (
            pos_tool_b_after - pos_tool_b_before
        ),
    }

    # --------------------------------------------------------
    # NEGATIVE TOOL-SUBSTITUTION CASE
    #
    # Separate fresh authority also bound to TOOL_A.
    # Same presenter.
    # Same authorized action.
    # Target changed only to TOOL_B.
    # --------------------------------------------------------

    negative_authority = ExecutionAuthority(
        authority_id="AUTH_F07_NEG",
        subject_identity="AGENT_A",
        bound_tool_identity="TOOL_A",
        authorized_actions=frozenset({SHARED_ACTION}),
        valid=True,
        consumed=False,
        governing_state_valid=True,
    )

    neg_tool_a_before = tool_a.consequence_counter
    neg_tool_b_before = tool_b.consequence_counter

    negative = gate.attempt(
        authority=negative_authority,
        presenter_identity="AGENT_A",
        action=SHARED_ACTION,
        target_tool=tool_b,
    )

    neg_tool_a_after = tool_a.consequence_counter
    neg_tool_b_after = tool_b.consequence_counter

    negative_record = {
        "test_id": "EASA-F07-NEG-001",
        "observation_time_utc": observation_time,
        "case": "TOOL_SUBSTITUTION",
        "authority_id": negative.authority_id,
        "authority_subject_identity": negative.subject_identity,
        "presenter_identity": negative.presenter_identity,
        "authority_tool_identity": negative.authority_tool_identity,
        "target_tool_identity": negative.target_tool_identity,
        "action": negative.action,
        "action_authorized_before": True,
        "authority_valid_before": True,
        "authority_governing_state_valid_before": True,
        "authority_consumed_before": negative.authority_consumed_before,
        "authority_consumed_after": negative.authority_consumed_after,
        "verdict": negative.verdict,
        "reason": negative.reason,
        "tool_a_consequence_before": neg_tool_a_before,
        "tool_a_consequence_after": neg_tool_a_after,
        "tool_a_consequence_delta": (
            neg_tool_a_after - neg_tool_a_before
        ),
        "tool_b_consequence_before": neg_tool_b_before,
        "tool_b_consequence_after": neg_tool_b_after,
        "tool_b_consequence_delta": (
            neg_tool_b_after - neg_tool_b_before
        ),
    }

    checks = {

        "distinct_authority_instances":
            positive.authority_id != negative.authority_id,

        "same_presenter_identity":
            positive.presenter_identity == "AGENT_A"
            and negative.presenter_identity == "AGENT_A",

        "same_authority_subject_identity":
            positive.subject_identity == "AGENT_A"
            and negative.subject_identity == "AGENT_A",

        "same_authorized_action":
            positive.action == SHARED_ACTION
            and negative.action == SHARED_ACTION,

        "same_authority_tool_binding":
            positive.authority_tool_identity == "TOOL_A"
            and negative.authority_tool_identity == "TOOL_A",

        "positive_target_tool_a":
            positive.target_tool_identity == "TOOL_A",

        "positive_started_unconsumed":
            positive.authority_consumed_before is False,

        "positive_verdict_permit":
            positive.verdict == "PERMIT",

        "positive_tool_a_delta_one":
            positive_record["tool_a_consequence_delta"] == 1,

        "positive_tool_b_delta_zero":
            positive_record["tool_b_consequence_delta"] == 0,

        "positive_authority_consumed_after":
            positive.authority_consumed_after is True,

        "negative_target_tool_b":
            negative.target_tool_identity == "TOOL_B",

        "negative_started_unconsumed":
            negative.authority_consumed_before is False,

        "negative_verdict_refuse":
            negative.verdict == "REFUSE",

        "negative_reason_tool_identity_mismatch":
            negative.reason == "TOOL_IDENTITY_MISMATCH",

        "negative_tool_a_delta_zero":
            negative_record["tool_a_consequence_delta"] == 0,

        "negative_tool_b_delta_zero":
            negative_record["tool_b_consequence_delta"] == 0,

        "negative_authority_remains_unconsumed":
            negative.authority_consumed_after is False,

        "final_tool_a_counter_exactly_one":
            tool_a.consequence_counter == 1,

        "final_tool_b_counter_exactly_zero":
            tool_b.consequence_counter == 0,
    }

    overall_pass = all(checks.values())

    summary_record = {
        "examination": "EASA-F07",
        "property": "TOOL_SPECIFIC_AUTHORITY_ISOLATION",
        "observation_time_utc": observation_time,
        "positive_test": "EASA-F07-POS-001",
        "negative_test": "EASA-F07-NEG-001",
        "checks": checks,
        "final_tool_a_consequence_counter":
            tool_a.consequence_counter,
        "final_tool_b_consequence_counter":
            tool_b.consequence_counter,
        "overall_result":
            "PASS" if overall_pass else "FAIL",
        "claim_state":
            "OBSERVATION_SUPPORTS_DEFINED_PROPERTY"
            if overall_pass
            else "DEFINED_PROPERTY_NOT_ESTABLISHED_BY_FIRST_OBSERVATION",
    }

    write_json(POSITIVE_PATH, positive_record)
    write_json(NEGATIVE_PATH, negative_record)
    write_json(SUMMARY_PATH, summary_record)

    print("=== EASA-F07 FIRST OBSERVATION ===")
    print(json.dumps(summary_record, indent=2, sort_keys=True))

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())