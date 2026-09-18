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

from easa_f09_control import (  # noqa: E402
    EPOCH_ACTION,
    REVOCATION_EVENT_ID,
    AuthoritativeEpochSource,
    ConsequentialTool,
    EpochBoundAuthority,
    EpochExecutionGate,
    LocalNodeState,
    RevocationEvent,
)
from easa_f09_propagation import (  # noqa: E402
    RECEIPT_IDS,
    RevocationPropagator,
)


EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F09"

CHANGE_PATH = (
    EVIDENCE_DIR / "EASA-F09-AUTHORITATIVE-CHANGE-001.json"
)

RECEIPT_PATHS = {
    "NODE_A": EVIDENCE_DIR / "EASA-F09-RECEIPT-NODE-A.json",
    "NODE_B": EVIDENCE_DIR / "EASA-F09-RECEIPT-NODE-B.json",
    "NODE_C": EVIDENCE_DIR / "EASA-F09-RECEIPT-NODE-C.json",
}

STALE_PATHS = {
    "NODE_A": EVIDENCE_DIR / "EASA-F09-STALE-A-001.json",
    "NODE_B": EVIDENCE_DIR / "EASA-F09-STALE-B-001.json",
    "NODE_C": EVIDENCE_DIR / "EASA-F09-STALE-C-001.json",
}

CURRENT_PATH = (
    EVIDENCE_DIR / "EASA-F09-CURRENT-E2-POS-001.json"
)

SUMMARY_PATH = EVIDENCE_DIR / "EASA-F09-SUMMARY.json"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, value: dict) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def result_record(
    *,
    test_id: str,
    observation_time: str,
    result,
) -> dict:

    return {
        "test_id": test_id,
        "observation_time_utc": observation_time,
        "node_id": result.node_id,
        "presenter_identity": result.presenter_identity,
        "authority_id": result.authority_id,
        "authority_epoch": result.authority_epoch,
        "local_current_epoch": result.local_current_epoch,
        "local_epoch_revoked": result.local_epoch_revoked,
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

    evidence_targets = [
        CHANGE_PATH,
        *RECEIPT_PATHS.values(),
        *STALE_PATHS.values(),
        CURRENT_PATH,
        SUMMARY_PATH,
    ]

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

    observation_time = now_utc()

    # ========================================================
    # INDEPENDENT INITIAL NODE STATES
    # ========================================================

    source = AuthoritativeEpochSource(current_epoch=1)

    nodes = {
        "NODE_A": LocalNodeState(
            node_id="NODE_A",
            current_epoch=1,
        ),
        "NODE_B": LocalNodeState(
            node_id="NODE_B",
            current_epoch=1,
        ),
        "NODE_C": LocalNodeState(
            node_id="NODE_C",
            current_epoch=1,
        ),
    }

    node_objects_distinct = (
        nodes["NODE_A"] is not nodes["NODE_B"]
        and nodes["NODE_A"] is not nodes["NODE_C"]
        and nodes["NODE_B"] is not nodes["NODE_C"]
    )

    revoked_sets_distinct = (
        nodes["NODE_A"].revoked_epochs
        is not nodes["NODE_B"].revoked_epochs
        and nodes["NODE_A"].revoked_epochs
        is not nodes["NODE_C"].revoked_epochs
        and nodes["NODE_B"].revoked_epochs
        is not nodes["NODE_C"].revoked_epochs
    )

    initial_node_state = {
        node_id: {
            "current_epoch": node.current_epoch,
            "revoked_epochs": sorted(node.revoked_epochs),
            "last_applied_revocation_event":
                node.last_applied_revocation_event,
        }
        for node_id, node in nodes.items()
    }

    tools = {
        "NODE_A": ConsequentialTool("TOOL_F09_A"),
        "NODE_B": ConsequentialTool("TOOL_F09_B"),
        "NODE_C": ConsequentialTool("TOOL_F09_C"),
    }

    stale_authorities = {
        "NODE_A": EpochBoundAuthority(
            authority_id="AUTH_F09_A_E1",
            subject_identity="AGENT_A",
            bound_tool_identity="TOOL_F09_A",
            authorized_actions=frozenset({EPOCH_ACTION}),
            authority_epoch=1,
            valid=True,
            consumed=False,
        ),
        "NODE_B": EpochBoundAuthority(
            authority_id="AUTH_F09_B_E1",
            subject_identity="AGENT_B",
            bound_tool_identity="TOOL_F09_B",
            authorized_actions=frozenset({EPOCH_ACTION}),
            authority_epoch=1,
            valid=True,
            consumed=False,
        ),
        "NODE_C": EpochBoundAuthority(
            authority_id="AUTH_F09_C_E1",
            subject_identity="AGENT_C",
            bound_tool_identity="TOOL_F09_C",
            authorized_actions=frozenset({EPOCH_ACTION}),
            authority_epoch=1,
            valid=True,
            consumed=False,
        ),
    }

    presenters = {
        "NODE_A": "AGENT_A",
        "NODE_B": "AGENT_B",
        "NODE_C": "AGENT_C",
    }

    stale_initial_state = {
        node_id: {
            "authority_id": authority.authority_id,
            "authority_epoch": authority.authority_epoch,
            "subject_identity": authority.subject_identity,
            "bound_tool_identity":
                authority.bound_tool_identity,
            "authorized_actions":
                sorted(authority.authorized_actions),
            "valid": authority.valid,
            "consumed": authority.consumed,
        }
        for node_id, authority
        in stale_authorities.items()
    }

    # ========================================================
    # PROSPECTIVE AUTHORITY CHANGE
    # ========================================================

    event = RevocationEvent(
        event_id=REVOCATION_EVENT_ID,
        prior_epoch=1,
        new_epoch=2,
        revoked_epoch=1,
    )

    source_before = {
        "current_epoch": source.current_epoch,
        "revoked_epochs": sorted(source.revoked_epochs),
    }

    change_result = source.apply_event(event)

    change_time = now_utc()

    change_record = {
        "examination": "EASA-F09",
        "record_type": "AUTHORITATIVE_EPOCH_CHANGE",
        "observation_time_utc": observation_time,
        "change_time_utc": change_time,
        "event": asdict(event),
        "source_before": source_before,
        "source_after": {
            "current_epoch": source.current_epoch,
            "revoked_epochs":
                sorted(source.revoked_epochs),
        },
        "change_result": asdict(change_result),
    }

    write_json(CHANGE_PATH, change_record)

    # ========================================================
    # INDEPENDENT REVOCATION PROPAGATION
    # ========================================================

    propagator = RevocationPropagator()

    receipt_records = {}

    for node_id in ("NODE_A", "NODE_B", "NODE_C"):

        node = nodes[node_id]

        try:

            receipt = propagator.deliver(
                event=event,
                node_state=node,
            )

            record = asdict(receipt)

            record["receipt_time_utc"] = now_utc()
            record["error"] = None

        except BaseException as exc:

            record = {
                "receipt_id": RECEIPT_IDS[node_id],
                "node_id": node_id,
                "revocation_event_id": event.event_id,
                "prior_local_epoch": node.current_epoch,
                "resulting_local_epoch": node.current_epoch,
                "revoked_epoch": event.revoked_epoch,
                "revoked_epoch_recorded": (
                    event.revoked_epoch
                    in node.revoked_epochs
                ),
                "event_recorded": (
                    node.last_applied_revocation_event
                    == event.event_id
                ),
                "application_status": "FAILED",
                "acknowledgement_status": "NOT_ACKNOWLEDGED",
                "receipt_time_utc": now_utc(),
                "error": {
                    "type": type(exc).__name__,
                    "text": str(exc),
                },
            }

        receipt_records[node_id] = record
        write_json(RECEIPT_PATHS[node_id], record)

    expected_receipt_ids = {
        "NODE_A": "F09-RECEIPT-NODE-A",
        "NODE_B": "F09-RECEIPT-NODE-B",
        "NODE_C": "F09-RECEIPT-NODE-C",
    }

    receipts_complete = all(
        receipt_records[node_id]["receipt_id"]
            == expected_receipt_ids[node_id]
        and receipt_records[node_id]["node_id"]
            == node_id
        and receipt_records[node_id]["revocation_event_id"]
            == REVOCATION_EVENT_ID
        and receipt_records[node_id]["prior_local_epoch"]
            == 1
        and receipt_records[node_id]["resulting_local_epoch"]
            == 2
        and receipt_records[node_id]["revoked_epoch"]
            == 1
        and receipt_records[node_id]["revoked_epoch_recorded"]
            is True
        and receipt_records[node_id]["event_recorded"]
            is True
        and receipt_records[node_id]["application_status"]
            == "APPLIED"
        and receipt_records[node_id]["acknowledgement_status"]
            == "ACKNOWLEDGED"
        and receipt_records[node_id]["error"]
            is None
        for node_id
        in ("NODE_A", "NODE_B", "NODE_C")
    )

    receipts_completed_time = now_utc()

    # F09 definition prohibits stale attempts until all required
    # propagation acknowledgements have been successfully constituted.

    if not receipts_complete:

        failure_summary = {
            "examination": "EASA-F09",
            "property":
                "MULTI_AGENT_REVOCATION_PROPAGATION_EPOCH_INVALIDATION",
            "observation_time_utc": observation_time,
            "authoritative_change_completed": True,
            "all_propagation_receipts_complete": False,
            "receipts": receipt_records,
            "stale_attempts_performed": False,
            "current_epoch_positive_performed": False,
            "overall_result": "FAIL",
            "claim_state":
                "DEFINED_PROPERTY_NOT_ESTABLISHED_BY_FIRST_OBSERVATION",
            "failure_reason":
                "PROPAGATION_ACKNOWLEDGEMENT_INCOMPLETE",
        }

        write_json(SUMMARY_PATH, failure_summary)

        print("=== EASA-F09 FIRST OBSERVATION ===")
        print(
            json.dumps(
                failure_summary,
                indent=2,
                sort_keys=True,
            )
        )

        return 1

    # ========================================================
    # VERIFY PROPAGATED LOCAL STATE BEFORE STALE ATTEMPTS
    # ========================================================

    node_state_after_propagation = {
        node_id: {
            "current_epoch": node.current_epoch,
            "revoked_epochs": sorted(node.revoked_epochs),
            "last_applied_revocation_event":
                node.last_applied_revocation_event,
        }
        for node_id, node in nodes.items()
    }

    stale_attempts_start_time = now_utc()

    gate = EpochExecutionGate()

    # ========================================================
    # STALE EPOCH-1 ATTEMPTS
    # ========================================================

    stale_records = {}

    stale_test_ids = {
        "NODE_A": "EASA-F09-STALE-A-001",
        "NODE_B": "EASA-F09-STALE-B-001",
        "NODE_C": "EASA-F09-STALE-C-001",
    }

    for node_id in ("NODE_A", "NODE_B", "NODE_C"):

        result = gate.attempt(
            node_state=nodes[node_id],
            authority=stale_authorities[node_id],
            presenter_identity=presenters[node_id],
            action=EPOCH_ACTION,
            target_tool=tools[node_id],
        )

        record = result_record(
            test_id=stale_test_ids[node_id],
            observation_time=observation_time,
            result=result,
        )

        record.update(
            {
                "case": "POST_PROPAGATION_STALE_EPOCH",
                "all_receipts_complete_before_attempt":
                    receipts_complete,
                "revocation_event_id":
                    REVOCATION_EVENT_ID,
                "authority_valid_before": True,
                "authority_unconsumed_before": True,
                "presenter_binding_correct": True,
                "action_scope_correct": True,
                "tool_binding_correct": True,
            }
        )

        stale_records[node_id] = record
        write_json(STALE_PATHS[node_id], record)

    # ========================================================
    # FRESH CURRENT-EPOCH POSITIVE CONTROL
    # ========================================================

    current_authority = EpochBoundAuthority(
        authority_id="AUTH_F09_CURRENT_E2",
        subject_identity="AGENT_C",
        bound_tool_identity="TOOL_F09_C",
        authorized_actions=frozenset({EPOCH_ACTION}),
        authority_epoch=2,
        valid=True,
        consumed=False,
    )

    current_result = gate.attempt(
        node_state=nodes["NODE_C"],
        authority=current_authority,
        presenter_identity="AGENT_C",
        action=EPOCH_ACTION,
        target_tool=tools["NODE_C"],
    )

    current_record = result_record(
        test_id="EASA-F09-CURRENT-E2-POS-001",
        observation_time=observation_time,
        result=current_result,
    )

    current_record.update(
        {
            "case": "CURRENT_EPOCH_POSITIVE_CONTROL",
            "authority_valid_before": True,
            "presenter_binding_correct": True,
            "action_scope_correct": True,
            "tool_binding_correct": True,
            "epoch_2_revoked_before": (
                2 in nodes["NODE_C"].revoked_epochs
            ),
        }
    )

    write_json(CURRENT_PATH, current_record)

    # ========================================================
    # AGGREGATE CHECKS
    # ========================================================

    stale_list = [
        stale_records["NODE_A"],
        stale_records["NODE_B"],
        stale_records["NODE_C"],
    ]

    total_stale_delta = sum(
        int(record["consequence_delta"])
        for record in stale_list
    )

    stale_reasons = [
        record["reason"]
        for record in stale_list
    ]

    checks = {

        "node_state_objects_distinct":
            node_objects_distinct,

        "node_revoked_sets_distinct":
            revoked_sets_distinct,

        "authoritative_source_started_epoch_1":
            source_before["current_epoch"] == 1,

        "nodes_started_epoch_1":
            all(
                initial_node_state[node_id]["current_epoch"] == 1
                for node_id
                in ("NODE_A", "NODE_B", "NODE_C")
            ),

        "nodes_started_without_revocations":
            all(
                initial_node_state[node_id]["revoked_epochs"] == []
                for node_id
                in ("NODE_A", "NODE_B", "NODE_C")
            ),

        "all_stale_authorities_valid_before":
            all(
                stale_initial_state[node_id]["valid"] is True
                for node_id
                in ("NODE_A", "NODE_B", "NODE_C")
            ),

        "all_stale_authorities_unconsumed_before":
            all(
                stale_initial_state[node_id]["consumed"] is False
                for node_id
                in ("NODE_A", "NODE_B", "NODE_C")
            ),

        "all_stale_authorities_epoch_1":
            all(
                stale_initial_state[node_id]["authority_epoch"] == 1
                for node_id
                in ("NODE_A", "NODE_B", "NODE_C")
            ),

        "authoritative_epoch_advanced_1_to_2":
            change_result.prior_authoritative_epoch == 1
            and change_result.resulting_authoritative_epoch == 2,

        "authoritative_epoch_1_revoked":
            1 in source.revoked_epochs,

        "revocation_event_identity_correct":
            event.event_id == REVOCATION_EVENT_ID,

        "all_receipts_complete":
            receipts_complete,

        "all_receipts_same_event":
            all(
                receipt_records[node_id]["revocation_event_id"]
                == REVOCATION_EVENT_ID
                for node_id
                in ("NODE_A", "NODE_B", "NODE_C")
            ),

        "all_receipts_acknowledged":
            all(
                receipt_records[node_id]["acknowledgement_status"]
                == "ACKNOWLEDGED"
                for node_id
                in ("NODE_A", "NODE_B", "NODE_C")
            ),

        "all_receipts_before_stale_attempts":
            receipts_complete
            and receipts_completed_time
                <= stale_attempts_start_time,

        "all_nodes_epoch_2_after_propagation":
            all(
                node_state_after_propagation[node_id]["current_epoch"]
                == 2
                for node_id
                in ("NODE_A", "NODE_B", "NODE_C")
            ),

        "all_nodes_record_epoch_1_revoked":
            all(
                1
                in node_state_after_propagation[node_id][
                    "revoked_epochs"
                ]
                for node_id
                in ("NODE_A", "NODE_B", "NODE_C")
            ),

        "all_nodes_record_event_identity":
            all(
                node_state_after_propagation[node_id][
                    "last_applied_revocation_event"
                ]
                == REVOCATION_EVENT_ID
                for node_id
                in ("NODE_A", "NODE_B", "NODE_C")
            ),

        "all_stale_attempts_refused":
            all(
                record["verdict"] == "REFUSE"
                for record in stale_list
            ),

        "all_stale_reasons_epoch_revoked":
            stale_reasons
            == [
                "AUTHORITY_EPOCH_REVOKED",
                "AUTHORITY_EPOCH_REVOKED",
                "AUTHORITY_EPOCH_REVOKED",
            ],

        "all_stale_deltas_zero":
            all(
                int(record["consequence_delta"]) == 0
                for record in stale_list
            ),

        "total_stale_delta_zero":
            total_stale_delta == 0,

        "all_stale_authorities_remain_unconsumed":
            all(
                stale_authorities[node_id].consumed is False
                for node_id
                in ("NODE_A", "NODE_B", "NODE_C")
            ),

        "no_identity_mismatch_refusal":
            "PRESENTER_IDENTITY_MISMATCH"
            not in stale_reasons,

        "no_scope_mismatch_refusal":
            "EXECUTION_SCOPE_NOT_AUTHORIZED"
            not in stale_reasons,

        "no_tool_mismatch_refusal":
            "TOOL_IDENTITY_MISMATCH"
            not in stale_reasons,

        "no_consumed_authority_refusal":
            "EXECUTION_AUTHORITY_ALREADY_CONSUMED"
            not in stale_reasons,

        "current_authority_epoch_2":
            current_authority.authority_epoch == 2,

        "current_epoch_not_revoked":
            2 not in nodes["NODE_C"].revoked_epochs,

        "current_positive_permitted":
            current_result.verdict == "PERMIT",

        "current_positive_reason_authorized":
            current_result.reason == "AUTHORIZED",

        "current_positive_delta_one":
            current_result.consequence_delta == 1,

        "current_authority_consumed_after":
            current_authority.consumed is True,

        "node_a_final_counter_zero":
            tools["NODE_A"].consequence_counter == 0,

        "node_b_final_counter_zero":
            tools["NODE_B"].consequence_counter == 0,

        "node_c_final_counter_one":
            tools["NODE_C"].consequence_counter == 1,
    }

    overall_pass = all(checks.values())

    summary_record = {
        "examination": "EASA-F09",
        "property":
            "MULTI_AGENT_REVOCATION_PROPAGATION_EPOCH_INVALIDATION",
        "observation_time_utc": observation_time,
        "authoritative_change_time_utc": change_time,
        "receipts_completed_time_utc":
            receipts_completed_time,
        "stale_attempts_start_time_utc":
            stale_attempts_start_time,
        "initial_node_state":
            initial_node_state,
        "node_state_after_propagation":
            node_state_after_propagation,
        "node_state_objects_distinct":
            node_objects_distinct,
        "revoked_set_objects_distinct":
            revoked_sets_distinct,
        "revocation_event":
            asdict(event),
        "receipts":
            receipt_records,
        "all_propagation_receipts_complete":
            receipts_complete,
        "stale_attempts_performed":
            True,
        "stale_attempt_count":
            len(stale_list),
        "stale_refuse_count":
            sum(
                1
                for record in stale_list
                if record["verdict"] == "REFUSE"
            ),
        "stale_total_consequence_delta":
            total_stale_delta,
        "current_epoch_positive_performed":
            True,
        "current_epoch_positive_verdict":
            current_result.verdict,
        "current_epoch_positive_delta":
            current_result.consequence_delta,
        "final_tool_counters": {
            node_id: tool.consequence_counter
            for node_id, tool in tools.items()
        },
        "checks":
            checks,
        "overall_result":
            "PASS" if overall_pass else "FAIL",
        "claim_state":
            "OBSERVATION_SUPPORTS_DEFINED_PROPERTY"
            if overall_pass
            else "DEFINED_PROPERTY_NOT_ESTABLISHED_BY_FIRST_OBSERVATION",
    }

    write_json(SUMMARY_PATH, summary_record)

    print("=== EASA-F09 FIRST OBSERVATION ===")
    print(
        json.dumps(
            summary_record,
            indent=2,
            sort_keys=True,
        )
    )

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())