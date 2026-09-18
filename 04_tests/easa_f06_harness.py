from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = ROOT / "03_controls"

if str(CONTROL_DIR) not in sys.path:
    sys.path.insert(0, str(CONTROL_DIR))

from easa_f06_control import (  # noqa: E402
    ExecutionAuthority,
    IdentityBoundExecutionGate,
    PrivilegedWriteTool,
    PRIVILEGED_ACTION,
)


EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F06"

POSITIVE_PATH = EVIDENCE_DIR / "EASA-F06-POS-001.json"
NEGATIVE_PATH = EVIDENCE_DIR / "EASA-F06-NEG-001.json"
SUMMARY_PATH = EVIDENCE_DIR / "EASA-F06-SUMMARY.json"


def write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:

    # First-observation protection:
    # never overwrite prior F06 evidence.

    evidence_targets = (
        POSITIVE_PATH,
        NEGATIVE_PATH,
        SUMMARY_PATH,
    )

    existing = [str(path) for path in evidence_targets if path.exists()]

    if existing:
        print("FIRST OBSERVATION EVIDENCE ALREADY EXISTS — STOP")
        for path in existing:
            print(path)
        return 2

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    observation_time = datetime.now(timezone.utc).isoformat()

    gate = IdentityBoundExecutionGate()
    tool = PrivilegedWriteTool()

    # --------------------------------------------------------
    # POSITIVE CONTROL
    # Fresh independent authority bound to AGENT_A.
    # Presenter is AGENT_A.
    # --------------------------------------------------------

    positive_authority = ExecutionAuthority(
        authority_id="AUTH_F06_POS",
        subject_identity="AGENT_A",
        authorized_actions=frozenset({PRIVILEGED_ACTION}),
        valid=True,
        consumed=False,
        governing_state_valid=True,
    )

    positive = gate.attempt(
        authority=positive_authority,
        presenter_identity="AGENT_A",
        action=PRIVILEGED_ACTION,
        tool=tool,
    )

    positive_record = {
        "test_id": "EASA-F06-POS-001",
        "observation_time_utc": observation_time,
        "case": "MATCHING_SUBJECT_AND_PRESENTER",
        "action": PRIVILEGED_ACTION,
        "authority_id": positive.authority_id,
        "authority_subject_identity": positive.subject_identity,
        "presenter_identity": positive.presenter_identity,
        "authority_valid_before": True,
        "authority_governing_state_valid_before": True,
        "authorized_actions": [PRIVILEGED_ACTION],
        "authority_consumed_before": positive.authority_consumed_before,
        "authority_consumed_after": positive.authority_consumed_after,
        "verdict": positive.verdict,
        "reason": positive.reason,
        "consequence_before": positive.consequence_before,
        "consequence_after": positive.consequence_after,
        "consequence_delta": positive.consequence_delta,
    }

    # --------------------------------------------------------
    # NEGATIVE SECURITY CASE
    # Separate fresh authority, also bound to AGENT_A.
    # Presenter is AGENT_B.
    #
    # This authority has never been consumed, so F03 cannot
    # explain the expected refusal.
    # --------------------------------------------------------

    negative_authority = ExecutionAuthority(
        authority_id="AUTH_F06_NEG",
        subject_identity="AGENT_A",
        authorized_actions=frozenset({PRIVILEGED_ACTION}),
        valid=True,
        consumed=False,
        governing_state_valid=True,
    )

    negative = gate.attempt(
        authority=negative_authority,
        presenter_identity="AGENT_B",
        action=PRIVILEGED_ACTION,
        tool=tool,
    )

    negative_record = {
        "test_id": "EASA-F06-NEG-001",
        "observation_time_utc": observation_time,
        "case": "PRESENTER_SUBSTITUTION",
        "action": PRIVILEGED_ACTION,
        "authority_id": negative.authority_id,
        "authority_subject_identity": negative.subject_identity,
        "presenter_identity": negative.presenter_identity,
        "authority_valid_before": True,
        "authority_governing_state_valid_before": True,
        "authorized_actions": [PRIVILEGED_ACTION],
        "authority_consumed_before": negative.authority_consumed_before,
        "authority_consumed_after": negative.authority_consumed_after,
        "verdict": negative.verdict,
        "reason": negative.reason,
        "consequence_before": negative.consequence_before,
        "consequence_after": negative.consequence_after,
        "consequence_delta": negative.consequence_delta,
    }

    checks = {
        "distinct_authority_instances":
            positive.authority_id != negative.authority_id,

        "same_bound_subject":
            positive.subject_identity == "AGENT_A"
            and negative.subject_identity == "AGENT_A",

        "positive_presenter_matches_subject":
            positive.presenter_identity == positive.subject_identity,

        "positive_verdict_permit":
            positive.verdict == "PERMIT",

        "positive_consequence_delta_exactly_one":
            positive.consequence_delta == 1,

        "positive_authority_started_unconsumed":
            positive.authority_consumed_before is False,

        "positive_authority_consumed_after_execution":
            positive.authority_consumed_after is True,

        "negative_presenter_differs_from_subject":
            negative.presenter_identity != negative.subject_identity,

        "negative_authority_started_unconsumed":
            negative.authority_consumed_before is False,

        "negative_verdict_refuse":
            negative.verdict == "REFUSE",

        "negative_reason_identity_mismatch":
            negative.reason == "PRESENTER_IDENTITY_MISMATCH",

        "negative_consequence_delta_zero":
            negative.consequence_delta == 0,

        "negative_authority_remains_unconsumed":
            negative.authority_consumed_after is False,

        "total_consequence_exactly_one":
            tool.consequence_counter == 1,
    }

    overall_pass = all(checks.values())

    summary_record = {
        "examination": "EASA-F06",
        "property": "IDENTITY_BOUND_PRIVILEGED_EXECUTION",
        "observation_time_utc": observation_time,
        "positive_test": "EASA-F06-POS-001",
        "negative_test": "EASA-F06-NEG-001",
        "checks": checks,
        "final_consequence_counter": tool.consequence_counter,
        "overall_result": "PASS" if overall_pass else "FAIL",
        "claim_state":
            "OBSERVATION_SUPPORTS_DEFINED_PROPERTY"
            if overall_pass
            else "DEFINED_PROPERTY_NOT_ESTABLISHED_BY_FIRST_OBSERVATION",
    }

    # Preserve both observations regardless of PASS or FAIL.

    write_json(POSITIVE_PATH, positive_record)
    write_json(NEGATIVE_PATH, negative_record)
    write_json(SUMMARY_PATH, summary_record)

    print("=== EASA-F06 FIRST OBSERVATION ===")
    print(json.dumps(summary_record, indent=2, sort_keys=True))

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())