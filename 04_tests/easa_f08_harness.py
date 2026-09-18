from __future__ import annotations

import json
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = ROOT / "03_controls"

if str(CONTROL_DIR) not in sys.path:
    sys.path.insert(0, str(CONTROL_DIR))

from easa_f08_control import (  # noqa: E402
    BOUND_TOOL,
    CONCURRENT_ACTION,
    ConcurrentSingleUseExecutionGate,
    ConsequentialTool,
    SingleUseAuthority,
)


EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F08"

POSITIVE_PATH = EVIDENCE_DIR / "EASA-F08-POS-001.json"
ATTEMPT_A_PATH = EVIDENCE_DIR / "EASA-F08-CONCURRENT-A-001.json"
ATTEMPT_B_PATH = EVIDENCE_DIR / "EASA-F08-CONCURRENT-B-001.json"
SUMMARY_PATH = EVIDENCE_DIR / "EASA-F08-SUMMARY.json"


def write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def gate_result_to_record(
    *,
    test_id: str,
    observation_time: str,
    result,
) -> dict:

    return {
        "test_id": test_id,
        "observation_time_utc": observation_time,
        "authority_id": result.authority_id,
        "presenter_identity": result.presenter_identity,
        "target_tool_identity": result.target_tool_identity,
        "action": result.action,
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

    evidence_targets = (
        POSITIVE_PATH,
        ATTEMPT_A_PATH,
        ATTEMPT_B_PATH,
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

    gate = ConcurrentSingleUseExecutionGate()
    tool = ConsequentialTool(BOUND_TOOL)

    # ========================================================
    # POSITIVE CONTROL
    # ========================================================

    positive_authority = SingleUseAuthority(
        authority_id="AUTH_F08_POS",
        authorized_presenters=frozenset({"AGENT_A"}),
        bound_tool_identity=BOUND_TOOL,
        authorized_actions=frozenset({CONCURRENT_ACTION}),
        valid=True,
        consumed=False,
        governing_state_valid=True,
        single_use=True,
    )

    positive_tool_before = tool.consequence_counter

    positive = gate.attempt(
        authority=positive_authority,
        presenter_identity="AGENT_A",
        action=CONCURRENT_ACTION,
        target_tool=tool,
    )

    positive_tool_after = tool.consequence_counter

    positive_record = gate_result_to_record(
        test_id="EASA-F08-POS-001",
        observation_time=observation_time,
        result=positive,
    )

    positive_record.update(
        {
            "case": "NON_CONCURRENT_POSITIVE_CONTROL",
            "authority_valid_before": True,
            "authority_single_use": True,
            "authorized_presenters": ["AGENT_A"],
            "authorized_action": CONCURRENT_ACTION,
            "bound_tool_identity": BOUND_TOOL,
            "governing_state_valid_before": True,
            "tool_counter_before_case": positive_tool_before,
            "tool_counter_after_case": positive_tool_after,
            "case_consequence_delta":
                positive_tool_after - positive_tool_before,
        }
    )

    # ========================================================
    # FRESH SHARED AUTHORITY FOR CONCURRENT COLLISION
    # ========================================================

    shared_authority = SingleUseAuthority(
        authority_id="AUTH_F08_CONCURRENT",
        authorized_presenters=frozenset(
            {
                "AGENT_A",
                "AGENT_B",
            }
        ),
        bound_tool_identity=BOUND_TOOL,
        authorized_actions=frozenset({CONCURRENT_ACTION}),
        valid=True,
        consumed=False,
        governing_state_valid=True,
        single_use=True,
    )

    # Two explicit references to the exact same runtime object.
    authority_ref_a = shared_authority
    authority_ref_b = shared_authority

    same_shared_object_reference = (
        authority_ref_a is authority_ref_b
        and authority_ref_a is shared_authority
    )

    concurrent_before = tool.consequence_counter

    shared_state_before = {
        "authority_id": shared_authority.authority_id,
        "authority_valid": shared_authority.valid,
        "authority_consumed": shared_authority.consumed,
        "authority_single_use": shared_authority.single_use,
        "authorized_presenters": sorted(
            shared_authority.authorized_presenters
        ),
        "authorized_actions": sorted(
            shared_authority.authorized_actions
        ),
        "bound_tool_identity":
            shared_authority.bound_tool_identity,
        "governing_state_valid":
            shared_authority.governing_state_valid,
        "same_shared_runtime_object_reference":
            same_shared_object_reference,
    }

    # ========================================================
    # SYNCHRONIZED CONCURRENT RELEASE
    #
    # Barrier parties:
    # - worker A
    # - worker B
    # - main harness thread
    #
    # Main does not enter the barrier until both workers are
    # observed waiting at it.
    # ========================================================

    start_barrier = threading.Barrier(3)

    results = {}
    result_lock = threading.Lock()

    worker_a_ready = threading.Event()
    worker_b_ready = threading.Event()

    worker_errors = []

    def worker(
        *,
        worker_name: str,
        presenter_identity: str,
        authority,
        ready_event: threading.Event,
    ) -> None:

        try:
            ready_event.set()

            start_barrier.wait(timeout=10)

            result = gate.attempt(
                authority=authority,
                presenter_identity=presenter_identity,
                action=CONCURRENT_ACTION,
                target_tool=tool,
            )

            with result_lock:
                results[worker_name] = result

        except BaseException as exc:
            with result_lock:
                worker_errors.append(
                    {
                        "worker_name": worker_name,
                        "exception_type": type(exc).__name__,
                        "exception_text": str(exc),
                    }
                )

    thread_a = threading.Thread(
        target=worker,
        kwargs={
            "worker_name": "WORKER_A",
            "presenter_identity": "AGENT_A",
            "authority": authority_ref_a,
            "ready_event": worker_a_ready,
        },
        name="EASA-F08-WORKER-A",
    )

    thread_b = threading.Thread(
        target=worker,
        kwargs={
            "worker_name": "WORKER_B",
            "presenter_identity": "AGENT_B",
            "authority": authority_ref_b,
            "ready_event": worker_b_ready,
        },
        name="EASA-F08-WORKER-B",
    )

    thread_a.start()
    thread_b.start()

    if not worker_a_ready.wait(timeout=10):
        raise RuntimeError("WORKER_A_DID_NOT_REACH_READY_STATE")

    if not worker_b_ready.wait(timeout=10):
        raise RuntimeError("WORKER_B_DID_NOT_REACH_READY_STATE")

    deadline = time.monotonic() + 10.0

    while (
        start_barrier.n_waiting != 2
        and time.monotonic() < deadline
    ):
        time.sleep(0.001)

    workers_waiting_before_release = (
        start_barrier.n_waiting == 2
    )

    if not workers_waiting_before_release:
        raise RuntimeError(
            "BOTH_WORKERS_NOT_OBSERVED_AT_BARRIER_BEFORE_RELEASE"
        )

    release_time = datetime.now(timezone.utc).isoformat()

    # Third barrier participant.
    # This releases both waiting workers from the same barrier cycle.
    start_barrier.wait(timeout=10)

    thread_a.join(timeout=10)
    thread_b.join(timeout=10)

    if thread_a.is_alive() or thread_b.is_alive():
        raise RuntimeError("CONCURRENT_WORKER_DID_NOT_TERMINATE")

    if worker_errors:
        raise RuntimeError(
            "WORKER_ERROR: "
            + json.dumps(worker_errors, sort_keys=True)
        )

    if set(results) != {"WORKER_A", "WORKER_B"}:
        raise RuntimeError(
            "EXPECTED_EXACTLY_TWO_WORKER_RESULTS"
        )

    result_a = results["WORKER_A"]
    result_b = results["WORKER_B"]

    concurrent_after = tool.consequence_counter
    concurrent_delta = concurrent_after - concurrent_before

    record_a = gate_result_to_record(
        test_id="EASA-F08-CONCURRENT-A-001",
        observation_time=observation_time,
        result=result_a,
    )

    record_a.update(
        {
            "case": "CONCURRENT_COLLISION",
            "worker_name": "WORKER_A",
            "barrier_release_time_utc": release_time,
            "same_shared_authority_object":
                same_shared_object_reference,
            "authority_valid_before_common_release": True,
            "authority_unconsumed_before_common_release": True,
            "presenter_explicitly_authorized": True,
            "action_explicitly_authorized": True,
            "tool_binding_valid": True,
            "governing_state_valid_before_common_release": True,
        }
    )

    record_b = gate_result_to_record(
        test_id="EASA-F08-CONCURRENT-B-001",
        observation_time=observation_time,
        result=result_b,
    )

    record_b.update(
        {
            "case": "CONCURRENT_COLLISION",
            "worker_name": "WORKER_B",
            "barrier_release_time_utc": release_time,
            "same_shared_authority_object":
                same_shared_object_reference,
            "authority_valid_before_common_release": True,
            "authority_unconsumed_before_common_release": True,
            "presenter_explicitly_authorized": True,
            "action_explicitly_authorized": True,
            "tool_binding_valid": True,
            "governing_state_valid_before_common_release": True,
        }
    )

    concurrent_records = [record_a, record_b]

    permit_records = [
        record
        for record in concurrent_records
        if record["verdict"] == "PERMIT"
    ]

    refuse_records = [
        record
        for record in concurrent_records
        if record["verdict"] == "REFUSE"
    ]

    permit_count = len(permit_records)
    refuse_count = len(refuse_records)

    refusal_reasons = sorted(
        record["reason"]
        for record in refuse_records
    )

    winner_presenter = (
        permit_records[0]["presenter_identity"]
        if permit_count == 1
        else None
    )

    loser_presenter = (
        refuse_records[0]["presenter_identity"]
        if refuse_count == 1
        else None
    )

    checks = {

        "positive_authority_distinct_from_concurrent":
            positive.authority_id
            != shared_authority.authority_id,

        "positive_started_unconsumed":
            positive.authority_consumed_before is False,

        "positive_verdict_permit":
            positive.verdict == "PERMIT",

        "positive_case_consequence_delta_one":
            positive_record["case_consequence_delta"] == 1,

        "positive_consumed_after":
            positive.authority_consumed_after is True,

        "shared_authority_same_runtime_object":
            same_shared_object_reference,

        "shared_authority_valid_before_release":
            shared_state_before["authority_valid"] is True,

        "shared_authority_unconsumed_before_release":
            shared_state_before["authority_consumed"] is False,

        "shared_authority_single_use":
            shared_state_before["authority_single_use"] is True,

        "agent_a_explicitly_authorized":
            "AGENT_A"
            in shared_state_before["authorized_presenters"],

        "agent_b_explicitly_authorized":
            "AGENT_B"
            in shared_state_before["authorized_presenters"],

        "concurrent_action_authorized":
            CONCURRENT_ACTION
            in shared_state_before["authorized_actions"],

        "concurrent_tool_binding_valid":
            shared_state_before["bound_tool_identity"]
            == BOUND_TOOL,

        "concurrent_governing_state_valid":
            shared_state_before["governing_state_valid"] is True,

        "both_workers_observed_waiting_at_barrier":
            workers_waiting_before_release,

        "exactly_two_worker_results":
            len(concurrent_records) == 2,

        "exactly_one_permit":
            permit_count == 1,

        "exactly_one_refuse":
            refuse_count == 1,

        "refusal_reason_already_consumed":
            refusal_reasons
            == ["EXECUTION_AUTHORITY_ALREADY_CONSUMED"],

        "concurrent_consequence_delta_exactly_one":
            concurrent_delta == 1,

        "shared_authority_consumed_after":
            shared_authority.consumed is True,

        "winner_is_authorized_presenter":
            winner_presenter in {"AGENT_A", "AGENT_B"},

        "loser_is_other_authorized_presenter":
            loser_presenter in {"AGENT_A", "AGENT_B"}
            and loser_presenter != winner_presenter,

        "permit_attempt_delta_exactly_one":
            permit_count == 1
            and permit_records[0]["consequence_delta"] == 1,

        "refused_attempt_delta_zero":
            refuse_count == 1
            and refuse_records[0]["consequence_delta"] == 0,

        "no_identity_mismatch_refusal":
            "PRESENTER_IDENTITY_NOT_AUTHORIZED"
            not in refusal_reasons,

        "no_tool_mismatch_refusal":
            "TOOL_IDENTITY_MISMATCH"
            not in refusal_reasons,

        "no_scope_mismatch_refusal":
            "EXECUTION_SCOPE_NOT_AUTHORIZED"
            not in refusal_reasons,
    }

    overall_pass = all(checks.values())

    summary_record = {
        "examination": "EASA-F08",
        "property":
            "CONCURRENT_SINGLE_CONSUMPTION_COLLISION_CONTROL",
        "observation_time_utc": observation_time,
        "barrier_release_time_utc": release_time,
        "positive_test": "EASA-F08-POS-001",
        "concurrent_tests": [
            "EASA-F08-CONCURRENT-A-001",
            "EASA-F08-CONCURRENT-B-001",
        ],
        "shared_authority_state_before_release":
            shared_state_before,
        "workers_waiting_at_barrier_before_release":
            workers_waiting_before_release,
        "concurrent_attempt_count":
            len(concurrent_records),
        "permit_count":
            permit_count,
        "refuse_count":
            refuse_count,
        "refusal_reasons":
            refusal_reasons,
        "winner_presenter":
            winner_presenter,
        "loser_presenter":
            loser_presenter,
        "concurrent_consequence_before":
            concurrent_before,
        "concurrent_consequence_after":
            concurrent_after,
        "concurrent_consequence_delta":
            concurrent_delta,
        "final_shared_authority_consumed":
            shared_authority.consumed,
        "final_tool_consequence_counter":
            tool.consequence_counter,
        "checks":
            checks,
        "overall_result":
            "PASS" if overall_pass else "FAIL",
        "claim_state":
            "OBSERVATION_SUPPORTS_DEFINED_PROPERTY"
            if overall_pass
            else "DEFINED_PROPERTY_NOT_ESTABLISHED_BY_FIRST_OBSERVATION",
    }

    # Preserve every observation regardless of PASS or FAIL.

    write_json(POSITIVE_PATH, positive_record)
    write_json(ATTEMPT_A_PATH, record_a)
    write_json(ATTEMPT_B_PATH, record_b)
    write_json(SUMMARY_PATH, summary_record)

    print("=== EASA-F08 FIRST OBSERVATION ===")
    print(json.dumps(summary_record, indent=2, sort_keys=True))

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())