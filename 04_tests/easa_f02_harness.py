from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = ROOT / "03_controls"
EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F02"

sys.path.insert(0, str(CONTROL_DIR))

from easa_f01_control import (  # noqa: E402
    ConsequentialTool,
    ExecutionAuthority,
    ExecutionGate,
)


SCOPE_A = "consequential.write"
SCOPE_B = "consequential.admin"


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
    gate: ExecutionGate,
    authority: ExecutionAuthority,
    requested_scope: str,
    expected_verdict: str,
    expected_delta: int,
) -> dict:

    requested_action = f"EXECUTE::{requested_scope}"

    before = tool.consequence_count

    decision = gate.evaluate(
        authority=authority,
        required_scope=requested_scope,
    )

    tool_result = None

    if decision.verdict == "PERMIT":
        tool_result = tool.execute(requested_action)

    after = tool.consequence_count
    delta = after - before

    passed = (
        decision.verdict == expected_verdict
        and delta == expected_delta
    )

    return {
        "object": "EASA-F02",
        "case_id": case_id,
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "authority": {
            "authority_id": authority.authority_id,
            "actor": authority.actor,
            "present": authority.present,
            "authorized_scopes": sorted(authority.scopes),
        },
        "request": {
            "requested_scope": requested_scope,
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
            "consequence_delta": expected_delta,
        },
        "case_pass": passed,
    }


def main() -> int:

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    definition_path = ROOT / "02_threat_models" / "EASA-F02-DEFINITION.md"
    control_path = ROOT / "03_controls" / "easa_f01_control.py"
    harness_path = Path(__file__).resolve()

    definition_hash = sha256_file(definition_path)
    control_hash = sha256_file(control_path)
    harness_hash = sha256_file(harness_path)

    gate = ExecutionGate()
    tool = ConsequentialTool()

    authority = ExecutionAuthority(
        authority_id="EASA-F02-AUTH-001",
        actor="bounded-test-operator",
        present=True,
        scopes=frozenset({SCOPE_A}),
    )

    positive = run_case(
        case_id="EASA-F02-POS-001",
        tool=tool,
        gate=gate,
        authority=authority,
        requested_scope=SCOPE_A,
        expected_verdict="PERMIT",
        expected_delta=1,
    )

    negative = run_case(
        case_id="EASA-F02-NEG-001",
        tool=tool,
        gate=gate,
        authority=authority,
        requested_scope=SCOPE_B,
        expected_verdict="REFUSE",
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
        and negative["security_decision"]["verdict"] == "REFUSE"
        and negative["security_decision"]["reason"] == "EXECUTION_SCOPE_NOT_AUTHORIZED"
        and negative["tool_executed"] is False
        and negative["consequence"]["delta"] == 0
    )

    summary = {
        "object": "EASA-F02",
        "security_property": (
            "AUTHORITY_PRESENT + REQUEST_OUTSIDE_AUTHORIZED_SCOPE "
            "=> NO_CONSEQUENCE"
        ),
        "authorized_scope": SCOPE_A,
        "unauthorized_requested_scope": SCOPE_B,
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
            "One authority object, two bounded local consequential scopes."
        ),
    }

    write_json(
        EVIDENCE_DIR / "EASA-F02-SUMMARY.json",
        summary,
    )

    print("=== EASA-F02 ===")
    print(
        "POSITIVE:",
        positive["security_decision"]["verdict"],
        "SCOPE:",
        SCOPE_A,
        "DELTA:",
        positive["consequence"]["delta"],
        "PASS:",
        positive["case_pass"],
    )
    print(
        "NEGATIVE:",
        negative["security_decision"]["verdict"],
        "REASON:",
        negative["security_decision"]["reason"],
        "SCOPE:",
        SCOPE_B,
        "DELTA:",
        negative["consequence"]["delta"],
        "PASS:",
        negative["case_pass"],
    )
    print("OVERALL PASS:", overall_pass)

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
