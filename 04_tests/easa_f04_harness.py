from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = ROOT / "03_controls"
EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F04"

sys.path.insert(0, str(CONTROL_DIR))

from easa_f04_control import (  # noqa: E402
    ChangedStateExecutionGate,
    ConsequentialTool,
    REQUIRED_SCOPE,
    StateBoundAuthority,
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def write_json(path: Path, payload: dict) -> None:
    path.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def run_case(
    *,
    case_id: str,
    tool: ConsequentialTool,
    gate: ChangedStateExecutionGate,
    authority: StateBoundAuthority,
    current_state_epoch: int,
    expected_verdict: str,
    expected_reason: str,
    expected_delta: int,
) -> dict:

    requested_action = "WRITE_BOUNDED_LOCAL_STATE"

    before = tool.consequence_count

    decision = gate.evaluate(
        authority=authority,
        current_state_epoch=current_state_epoch,
        required_scope=REQUIRED_SCOPE,
    )

    tool_result = None

    if decision.verdict == "PERMIT":
        tool_result = tool.execute(requested_action)

    after = tool.consequence_count
    delta = after - before

    passed = (
        decision.verdict == expected_verdict
        and decision.reason == expected_reason
        and delta == expected_delta
    )

    return {
        "object": "EASA-F04",
        "case_id": case_id,
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "authority": {
            "authority_id": authority.authority_id,
            "actor": authority.actor,
            "present": authority.present,
            "scopes": sorted(authority.scopes),
            "state_epoch": authority.state_epoch,
        },
        "governing_state": {
            "current_state_epoch": current_state_epoch,
        },
        "request": {
            "required_scope": REQUIRED_SCOPE,
            "action": requested_action,
        },
        "security_decision": asdict(decision),
        "consequence": {
            "before": before,
            "after": after,
            "delta": delta,
        },
        "tool_executed": tool_result is not None,
        "tool_result": tool_result,
        "expected": {
            "verdict": expected_verdict,
            "reason": expected_reason,
            "consequence_delta": expected_delta,
        },
        "case_pass": passed,
    }


def main() -> int:

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    definition_path = ROOT / "02_threat_models" / "EASA-F04-DEFINITION.md"
    control_path = ROOT / "03_controls" / "easa_f04_control.py"
    harness_path = Path(__file__).resolve()

    definition_hash = sha256_file(definition_path)
    control_hash = sha256_file(control_path)
    harness_hash = sha256_file(harness_path)

    gate = ChangedStateExecutionGate()
    tool = ConsequentialTool()

    authority = StateBoundAuthority(
        authority_id="EASA-F04-AUTH-001",
        actor="bounded-test-operator",
        present=True,
        scopes=frozenset({REQUIRED_SCOPE}),
        state_epoch=1,
    )

    matching_state = run_case(
        case_id="EASA-F04-MATCHING-STATE-001",
        tool=tool,
        gate=gate,
        authority=authority,
        current_state_epoch=1,
        expected_verdict="PERMIT",
        expected_reason="EXECUTION_AUTHORITY_CURRENT",
        expected_delta=1,
    )

    changed_state = run_case(
        case_id="EASA-F04-CHANGED-STATE-001",
        tool=tool,
        gate=gate,
        authority=authority,
        current_state_epoch=2,
        expected_verdict="REFUSE",
        expected_reason="EXECUTION_AUTHORITY_STATE_CHANGED",
        expected_delta=0,
    )

    for record in (matching_state, changed_state):
        record["bindings"] = {
            "definition_sha256": definition_hash,
            "control_sha256": control_hash,
            "harness_sha256": harness_hash,
        }

        write_json(
            EVIDENCE_DIR / f"{record['case_id']}.json",
            record,
        )

    overall_pass = (
        matching_state["case_pass"]
        and changed_state["case_pass"]
        and matching_state["security_decision"]["verdict"] == "PERMIT"
        and matching_state["tool_executed"] is True
        and matching_state["consequence"]["delta"] == 1
        and changed_state["security_decision"]["verdict"] == "REFUSE"
        and changed_state["security_decision"]["reason"]
            == "EXECUTION_AUTHORITY_STATE_CHANGED"
        and changed_state["tool_executed"] is False
        and changed_state["consequence"]["delta"] == 0
        and authority.state_epoch == 1
        and changed_state["governing_state"]["current_state_epoch"] == 2
    )

    summary = {
        "object": "EASA-F04",
        "security_property": (
            "AUTHORITY_VALID_AT_T0 + MATERIAL_GOVERNING_STATE_CHANGE + "
            "EXECUTION_ATTEMPT_AT_T1 => REFUSE_BEFORE_CONSEQUENCE"
        ),
        "definition_sha256": definition_hash,
        "control_sha256": control_hash,
        "harness_sha256": harness_hash,
        "matching_state_case": matching_state["case_id"],
        "matching_state_pass": matching_state["case_pass"],
        "changed_state_case": changed_state["case_id"],
        "changed_state_pass": changed_state["case_pass"],
        "authority_state_epoch": authority.state_epoch,
        "changed_current_state_epoch": 2,
        "final_consequence_count": tool.consequence_count,
        "overall_pass": overall_pass,
        "claim_boundary": (
            "One bounded local authority bound to an explicit governing-state epoch."
        ),
    }

    write_json(
        EVIDENCE_DIR / "EASA-F04-SUMMARY.json",
        summary,
    )

    print("=== EASA-F04 ===")
    print(
        "MATCHING STATE:",
        matching_state["security_decision"]["verdict"],
        "AUTHORITY EPOCH:",
        matching_state["authority"]["state_epoch"],
        "CURRENT EPOCH:",
        matching_state["governing_state"]["current_state_epoch"],
        "DELTA:",
        matching_state["consequence"]["delta"],
        "PASS:",
        matching_state["case_pass"],
    )

    print(
        "CHANGED STATE:",
        changed_state["security_decision"]["verdict"],
        "REASON:",
        changed_state["security_decision"]["reason"],
        "AUTHORITY EPOCH:",
        changed_state["authority"]["state_epoch"],
        "CURRENT EPOCH:",
        changed_state["governing_state"]["current_state_epoch"],
        "DELTA:",
        changed_state["consequence"]["delta"],
        "PASS:",
        changed_state["case_pass"],
    )

    print("OVERALL PASS:", overall_pass)

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
