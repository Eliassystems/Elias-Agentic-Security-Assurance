from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = ROOT / "03_controls"
EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F05"

sys.path.insert(0, str(CONTROL_DIR))

from easa_f05_control import (  # noqa: E402
    ExecutionAuthority,
    HIGH_IMPACT_ACTION,
    HighImpactTool,
    HumanAuthority,
    HumanAuthorityExecutionGate,
    REQUIRED_SCOPE,
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
    tool: HighImpactTool,
    gate: HumanAuthorityExecutionGate,
    execution_authority: ExecutionAuthority,
    human_authority: HumanAuthority,
    expected_verdict: str,
    expected_reason: str,
    expected_delta: int,
) -> dict:

    before = tool.consequence_count

    decision = gate.evaluate(
        execution_authority=execution_authority,
        human_authority=human_authority,
        action=HIGH_IMPACT_ACTION,
        required_scope=REQUIRED_SCOPE,
    )

    tool_result = None

    if decision.verdict == "PERMIT":
        tool_result = tool.execute(HIGH_IMPACT_ACTION)

    after = tool.consequence_count
    delta = after - before

    passed = (
        decision.verdict == expected_verdict
        and decision.reason == expected_reason
        and delta == expected_delta
    )

    return {
        "object": "EASA-F05",
        "case_id": case_id,
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "execution_authority": {
            "authority_id": execution_authority.authority_id,
            "actor": execution_authority.actor,
            "present": execution_authority.present,
            "scopes": sorted(execution_authority.scopes),
        },
        "human_authority": {
            "required": human_authority.required,
            "present": human_authority.present,
            "authority_id": human_authority.authority_id,
        },
        "request": {
            "action": HIGH_IMPACT_ACTION,
            "required_scope": REQUIRED_SCOPE,
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

    definition_path = ROOT / "02_threat_models" / "EASA-F05-DEFINITION.md"
    control_path = ROOT / "03_controls" / "easa_f05_control.py"
    harness_path = Path(__file__).resolve()

    definition_hash = sha256_file(definition_path)
    control_hash = sha256_file(control_path)
    harness_hash = sha256_file(harness_path)

    gate = HumanAuthorityExecutionGate()
    tool = HighImpactTool()

    execution_authority = ExecutionAuthority(
        authority_id="EASA-F05-MACHINE-AUTH-001",
        actor="bounded-test-agent",
        present=True,
        scopes=frozenset({REQUIRED_SCOPE}),
    )

    positive_human_authority = HumanAuthority(
        required=True,
        present=True,
        authority_id="EASA-F05-HUMAN-AUTH-001",
    )

    absent_human_authority = HumanAuthority(
        required=True,
        present=False,
        authority_id=None,
    )

    positive = run_case(
        case_id="EASA-F05-HUMAN-PRESENT-001",
        tool=tool,
        gate=gate,
        execution_authority=execution_authority,
        human_authority=positive_human_authority,
        expected_verdict="PERMIT",
        expected_reason="REQUIRED_AUTHORITIES_PRESENT",
        expected_delta=1,
    )

    negative = run_case(
        case_id="EASA-F05-HUMAN-ABSENT-001",
        tool=tool,
        gate=gate,
        execution_authority=execution_authority,
        human_authority=absent_human_authority,
        expected_verdict="REFUSE",
        expected_reason="REQUIRED_HUMAN_AUTHORITY_ABSENT",
        expected_delta=0,
    )

    for record in (positive, negative):
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
        positive["case_pass"]
        and negative["case_pass"]
        and positive["security_decision"]["verdict"] == "PERMIT"
        and positive["tool_executed"] is True
        and positive["consequence"]["delta"] == 1
        and positive["human_authority"]["required"] is True
        and positive["human_authority"]["present"] is True
        and negative["security_decision"]["verdict"] == "REFUSE"
        and negative["security_decision"]["reason"]
            == "REQUIRED_HUMAN_AUTHORITY_ABSENT"
        and negative["tool_executed"] is False
        and negative["consequence"]["delta"] == 0
        and negative["execution_authority"]["present"] is True
        and REQUIRED_SCOPE
            in negative["execution_authority"]["scopes"]
        and negative["human_authority"]["required"] is True
        and negative["human_authority"]["present"] is False
    )

    summary = {
        "object": "EASA-F05",
        "security_property": (
            "HIGH_IMPACT_ACTION + REQUIRED_HUMAN_AUTHORITY_ABSENT "
            "=> REFUSE_BEFORE_CONSEQUENCE"
        ),
        "definition_sha256": definition_hash,
        "control_sha256": control_hash,
        "harness_sha256": harness_hash,
        "positive_case": positive["case_id"],
        "positive_pass": positive["case_pass"],
        "negative_case": negative["case_id"],
        "negative_pass": negative["case_pass"],
        "final_consequence_count": tool.consequence_count,
        "overall_pass": overall_pass,
        "claim_boundary": (
            "One bounded local high-impact action with an explicit "
            "required-human-authority condition."
        ),
    }

    write_json(
        EVIDENCE_DIR / "EASA-F05-SUMMARY.json",
        summary,
    )

    print("=== EASA-F05 ===")

    print(
        "HUMAN PRESENT:",
        positive["security_decision"]["verdict"],
        "HUMAN:",
        positive["human_authority"]["present"],
        "DELTA:",
        positive["consequence"]["delta"],
        "PASS:",
        positive["case_pass"],
    )

    print(
        "HUMAN ABSENT:",
        negative["security_decision"]["verdict"],
        "REASON:",
        negative["security_decision"]["reason"],
        "HUMAN:",
        negative["human_authority"]["present"],
        "DELTA:",
        negative["consequence"]["delta"],
        "PASS:",
        negative["case_pass"],
    )

    print("OVERALL PASS:", overall_pass)

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
