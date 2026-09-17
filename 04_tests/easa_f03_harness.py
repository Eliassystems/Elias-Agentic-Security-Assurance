from __future__ import annotations

import hashlib
import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = ROOT / "03_controls"
EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F03"

sys.path.insert(0, str(CONTROL_DIR))

from easa_f03_control import (  # noqa: E402
    ConsequentialTool,
    ConsumableAuthority,
    ReplayProtectedExecutionGate,
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
    tool: ConsequentialTool,
    gate: ReplayProtectedExecutionGate,
    authority: ConsumableAuthority,
    expected_verdict: str,
    expected_delta: int,
    consume_on_permit: bool,
) -> dict:

    requested_action = "WRITE_BOUNDED_LOCAL_STATE"

    before = tool.consequence_count
    consumed_before = authority.consumed

    decision = gate.evaluate(
        authority=authority,
        required_scope=REQUIRED_SCOPE,
    )

    tool_result = None

    if decision.verdict == "PERMIT":
        tool_result = tool.execute(requested_action)

        if consume_on_permit:
            gate.consume(authority)

    after = tool.consequence_count
    consumed_after = authority.consumed
    delta = after - before

    passed = (
        decision.verdict == expected_verdict
        and delta == expected_delta
    )

    return {
        "object": "EASA-F03",
        "case_id": case_id,
        "recorded_at_utc": datetime.now(timezone.utc).isoformat(),
        "authority": {
            "authority_id": authority.authority_id,
            "actor": authority.actor,
            "present": authority.present,
            "scopes": sorted(authority.scopes),
            "consumed_before": consumed_before,
            "consumed_after": consumed_after,
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
            "consequence_delta": expected_delta,
        },
        "case_pass": passed,
    }


def main() -> int:

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    definition_path = ROOT / "02_threat_models" / "EASA-F03-DEFINITION.md"
    control_path = ROOT / "03_controls" / "easa_f03_control.py"
    harness_path = Path(__file__).resolve()

    definition_hash = sha256_file(definition_path)
    control_hash = sha256_file(control_path)
    harness_hash = sha256_file(harness_path)

    gate = ReplayProtectedExecutionGate()
    tool = ConsequentialTool()

    authority = ConsumableAuthority(
        authority_id="EASA-F03-AUTH-001",
        actor="bounded-test-operator",
        present=True,
        scopes=frozenset({REQUIRED_SCOPE}),
    )

    first_use = run_case(
        case_id="EASA-F03-FIRST-USE-001",
        tool=tool,
        gate=gate,
        authority=authority,
        expected_verdict="PERMIT",
        expected_delta=1,
        consume_on_permit=True,
    )

    replay = run_case(
        case_id="EASA-F03-REPLAY-001",
        tool=tool,
        gate=gate,
        authority=authority,
        expected_verdict="REFUSE",
        expected_delta=0,
        consume_on_permit=False,
    )

    for record in (first_use, replay):
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
        first_use["case_pass"]
        and replay["case_pass"]
        and first_use["security_decision"]["verdict"] == "PERMIT"
        and first_use["tool_executed"] is True
        and first_use["authority"]["consumed_after"] is True
        and replay["security_decision"]["verdict"] == "REFUSE"
        and replay["security_decision"]["reason"]
            == "EXECUTION_AUTHORITY_ALREADY_CONSUMED"
        and replay["tool_executed"] is False
        and replay["consequence"]["delta"] == 0
    )

    summary = {
        "object": "EASA-F03",
        "security_property": (
            "AUTHORITY_ALREADY_CONSUMED + REPLAY_ATTEMPT "
            "=> NO_CONSEQUENCE"
        ),
        "definition_sha256": definition_hash,
        "control_sha256": control_hash,
        "harness_sha256": harness_hash,
        "first_use_case": first_use["case_id"],
        "first_use_pass": first_use["case_pass"],
        "replay_case": replay["case_id"],
        "replay_pass": replay["case_pass"],
        "final_consequence_count": tool.consequence_count,
        "overall_pass": overall_pass,
        "claim_boundary": (
            "Single-use authority for one bounded local consequential action."
        ),
    }

    write_json(
        EVIDENCE_DIR / "EASA-F03-SUMMARY.json",
        summary,
    )

    print("=== EASA-F03 ===")
    print(
        "FIRST USE:",
        first_use["security_decision"]["verdict"],
        "DELTA:",
        first_use["consequence"]["delta"],
        "CONSUMED:",
        first_use["authority"]["consumed_after"],
        "PASS:",
        first_use["case_pass"],
    )
    print(
        "REPLAY:",
        replay["security_decision"]["verdict"],
        "REASON:",
        replay["security_decision"]["reason"],
        "DELTA:",
        replay["consequence"]["delta"],
        "PASS:",
        replay["case_pass"],
    )
    print("OVERALL PASS:", overall_pass)

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
