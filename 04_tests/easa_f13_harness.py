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

from easa_f13_authority import (  # noqa: E402
    AUTHORITY_SOURCE_ID,
    F13_ACTION,
    F13_AGENT,
    F13_TOOL,
    ExecutionAuthority,
    F13AuthoritySource,
)
from easa_f13_execution import (  # noqa: E402
    ConsequentialTool,
    F13ExecutionGate,
)
from easa_f13_peer_state import (  # noqa: E402
    PEER_ID,
    PEER_READY,
    PEER_STATE_SOURCE_ID,
    PEER_WITHDRAWN,
    STATE_V1,
    STATE_V2,
    STATE_V3,
    TRANSITION_V1_V2,
    TRANSITION_V2_V3,
    AuthoritativePeerStateSource,
    PeerSnapshot,
)


EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F13"

INITIAL_PATH = (
    EVIDENCE_DIR / "EASA-F13-INITIAL-STATE.json"
)

PRE_POS_PATH = (
    EVIDENCE_DIR / "EASA-F13-PRE-CHANGE-POSITIVE.json"
)

TRANSITION_12_PATH = (
    EVIDENCE_DIR / "EASA-F13-TRANSITION-V1-V2.json"
)

STALE_PATH = (
    EVIDENCE_DIR / "EASA-F13-STALE-ATTEMPT.json"
)

CURRENT_BLOCKED_PATH = (
    EVIDENCE_DIR / "EASA-F13-CURRENT-BLOCKED.json"
)

TRANSITION_23_PATH = (
    EVIDENCE_DIR / "EASA-F13-TRANSITION-V2-V3.json"
)

RECOVERY_PATH = (
    EVIDENCE_DIR / "EASA-F13-RECOVERY-POSITIVE.json"
)

SUMMARY_PATH = (
    EVIDENCE_DIR / "EASA-F13-SUMMARY.json"
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


def snapshot_dict(snapshot: PeerSnapshot) -> dict:
    return asdict(snapshot)


def authority_dict(authority: ExecutionAuthority) -> dict:
    return asdict(authority)


def source_dict(source: F13AuthoritySource) -> dict:
    return {
        "source_identity": source.source_identity,
        "issued_count": source.issued_count,
        "issued_ids": list(source.issued_ids),
    }


def authority_has_no_peer_state_fields(
    authority: ExecutionAuthority,
) -> bool:

    fields = set(vars(authority).keys())

    forbidden = {
        "peer_id",
        "peer_version",
        "peer_state_identity",
        "peer_standing",
        "peer_admissible",
        "local_peer_version",
        "authoritative_peer_version",
    }

    return fields.isdisjoint(forbidden)


def main() -> int:

    targets = (
        INITIAL_PATH,
        PRE_POS_PATH,
        TRANSITION_12_PATH,
        STALE_PATH,
        CURRENT_BLOCKED_PATH,
        TRANSITION_23_PATH,
        RECOVERY_PATH,
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

    # Explicit ordering evidence independent of wall-clock time.
    event_index = 0

    def next_event() -> int:
        nonlocal event_index
        event_index += 1
        return event_index

    peer_source = AuthoritativePeerStateSource()
    authority_source = F13AuthoritySource()
    gate = F13ExecutionGate()
    tool = ConsequentialTool()

    # ========================================================
    # 1. INITIAL V1 + IMMUTABLE LOCAL SNAPSHOT
    # ========================================================

    initial_event = next_event()

    authoritative_v1 = peer_source.current_state
    stale_snapshot_v1 = peer_source.capture_snapshot()

    initial_record = {
        "examination": "EASA-F13",
        "record_type": "INITIAL_STATE",
        "observation_time_utc": observation_time,
        "event_index": initial_event,
        "peer_state_source_identity":
            peer_source.source_identity,
        "authority_source_identity":
            authority_source.source_identity,
        "agent_identity":
            F13_AGENT,
        "peer_identity":
            PEER_ID,
        "authoritative_peer_state":
            snapshot_dict(authoritative_v1),
        "agent_local_snapshot_v1":
            snapshot_dict(stale_snapshot_v1),
        "snapshot_is_distinct_runtime_object":
            stale_snapshot_v1 is not authoritative_v1,
        "execution_gate_policy":
            gate.policy_snapshot(),
        "authority_source":
            source_dict(authority_source),
        "tool_counter":
            tool.consequence_counter,
    }

    write_json(
        INITIAL_PATH,
        initial_record,
    )

    # ========================================================
    # 2/3. PRE-CHANGE AUTHORITY + POSITIVE
    # ========================================================

    pre_authority_issue_event = next_event()

    auth_pre = authority_source.issue(
        "AUTH_F13_PRE"
    )

    pre_execution_event = next_event()

    pre_authoritative_state = peer_source.current_state

    pre_result = gate.attempt(
        authority=auth_pre,
        presenter_identity=F13_AGENT,
        local_peer_snapshot=stale_snapshot_v1,
        authoritative_peer_state=pre_authoritative_state,
        action=F13_ACTION,
        target_tool=tool,
    )

    pre_record = {
        "test_id":
            "EASA-F13-PRE-CHANGE-POSITIVE",
        "observation_time_utc":
            observation_time,
        "authority_issue_event_index":
            pre_authority_issue_event,
        "execution_event_index":
            pre_execution_event,
        "authority_before_execution": {
            **authority_dict(auth_pre),
            "consumed": False,
        },
        "authority_contains_peer_state_fields":
            not authority_has_no_peer_state_fields(
                auth_pre
            ),
        "local_snapshot":
            snapshot_dict(stale_snapshot_v1),
        "authoritative_peer_state":
            snapshot_dict(pre_authoritative_state),
        "execution":
            asdict(pre_result),
        "authority_after_execution":
            authority_dict(auth_pre),
        "tool_counter_after":
            tool.consequence_counter,
    }

    write_json(
        PRE_POS_PATH,
        pre_record,
    )

    # ========================================================
    # 4/5. MATERIAL V1 -> V2 TRANSITION
    # ========================================================

    transition_12_event = next_event()

    transition_12 = peer_source.transition_v1_to_v2()

    authoritative_v2_after_transition = (
        peer_source.current_state
    )

    transition_12_record = {
        "test_id":
            TRANSITION_V1_V2,
        "observation_time_utc":
            observation_time,
        "transition_event_index":
            transition_12_event,
        "transition":
            asdict(transition_12),
        "authoritative_state_after_transition":
            snapshot_dict(
                authoritative_v2_after_transition
            ),
        "preserved_stale_snapshot_after_transition":
            snapshot_dict(stale_snapshot_v1),
        "stale_snapshot_still_version_1":
            stale_snapshot_v1.version == 1,
        "stale_snapshot_still_ready":
            stale_snapshot_v1.standing
            == PEER_READY,
        "stale_snapshot_still_admissible":
            stale_snapshot_v1.admissible
            is True,
    }

    write_json(
        TRANSITION_12_PATH,
        transition_12_record,
    )

    # ========================================================
    # 6/7/8. STALE VIEW AUTHORITY + ATTEMPT
    # AUTHORITY IS ISSUED AFTER V2 TRANSITION
    # ========================================================

    stale_authority_issue_event = next_event()

    auth_stale = authority_source.issue(
        "AUTH_F13_STALE_VIEW"
    )

    stale_authority_before = authority_dict(
        auth_stale
    )

    stale_execution_event = next_event()

    authoritative_v2_for_stale = (
        peer_source.current_state
    )

    stale_result = gate.attempt(
        authority=auth_stale,
        presenter_identity=F13_AGENT,
        local_peer_snapshot=stale_snapshot_v1,
        authoritative_peer_state=(
            authoritative_v2_for_stale
        ),
        action=F13_ACTION,
        target_tool=tool,
    )

    stale_record = {
        "test_id":
            "EASA-F13-STALE-ATTEMPT",
        "observation_time_utc":
            observation_time,
        "transition_v1_v2_event_index":
            transition_12_event,
        "authority_issue_event_index":
            stale_authority_issue_event,
        "execution_event_index":
            stale_execution_event,
        "authority_issued_after_v2_transition":
            (
                stale_authority_issue_event
                > transition_12_event
            ),
        "authority_before_execution":
            stale_authority_before,
        "authority_contains_peer_state_fields":
            not authority_has_no_peer_state_fields(
                auth_stale
            ),
        "local_snapshot":
            snapshot_dict(stale_snapshot_v1),
        "authoritative_peer_state_before":
            snapshot_dict(
                authoritative_v2_for_stale
            ),
        "execution":
            asdict(stale_result),
        "authority_after_execution":
            authority_dict(auth_stale),
        "authoritative_peer_state_after":
            snapshot_dict(
                peer_source.current_state
            ),
        "preserved_stale_snapshot_after":
            snapshot_dict(stale_snapshot_v1),
        "tool_counter_after":
            tool.consequence_counter,
    }

    write_json(
        STALE_PATH,
        stale_record,
    )

    # ========================================================
    # 9/10/11. FRESH V2 SNAPSHOT + CURRENT BLOCKED
    # Capture occurs strictly after stale execution.
    # ========================================================

    v2_snapshot_capture_event = next_event()

    current_snapshot_v2 = peer_source.capture_snapshot()

    current_blocked_authority_event = next_event()

    auth_current_blocked = authority_source.issue(
        "AUTH_F13_CURRENT_BLOCKED"
    )

    current_blocked_before = authority_dict(
        auth_current_blocked
    )

    current_blocked_execution_event = next_event()

    authoritative_v2_for_current = (
        peer_source.current_state
    )

    current_blocked_result = gate.attempt(
        authority=auth_current_blocked,
        presenter_identity=F13_AGENT,
        local_peer_snapshot=current_snapshot_v2,
        authoritative_peer_state=(
            authoritative_v2_for_current
        ),
        action=F13_ACTION,
        target_tool=tool,
    )

    current_blocked_record = {
        "test_id":
            "EASA-F13-CURRENT-BLOCKED",
        "observation_time_utc":
            observation_time,
        "stale_execution_event_index":
            stale_execution_event,
        "v2_snapshot_capture_event_index":
            v2_snapshot_capture_event,
        "authority_issue_event_index":
            current_blocked_authority_event,
        "execution_event_index":
            current_blocked_execution_event,
        "fresh_v2_snapshot_captured_after_stale_attempt":
            (
                v2_snapshot_capture_event
                > stale_execution_event
            ),
        "authority_before_execution":
            current_blocked_before,
        "authority_contains_peer_state_fields":
            not authority_has_no_peer_state_fields(
                auth_current_blocked
            ),
        "local_snapshot":
            snapshot_dict(current_snapshot_v2),
        "authoritative_peer_state_before":
            snapshot_dict(
                authoritative_v2_for_current
            ),
        "execution":
            asdict(current_blocked_result),
        "authority_after_execution":
            authority_dict(
                auth_current_blocked
            ),
        "authoritative_peer_state_after":
            snapshot_dict(
                peer_source.current_state
            ),
        "tool_counter_after":
            tool.consequence_counter,
    }

    write_json(
        CURRENT_BLOCKED_PATH,
        current_blocked_record,
    )

    # ========================================================
    # 12/13. V2 -> V3 RECOVERY
    # Only after BOTH V2 negatives.
    # ========================================================

    transition_23_event = next_event()

    transition_23 = peer_source.transition_v2_to_v3()

    authoritative_v3_after_transition = (
        peer_source.current_state
    )

    transition_23_record = {
        "test_id":
            TRANSITION_V2_V3,
        "observation_time_utc":
            observation_time,
        "stale_execution_event_index":
            stale_execution_event,
        "current_blocked_execution_event_index":
            current_blocked_execution_event,
        "transition_event_index":
            transition_23_event,
        "transition_occurs_after_both_v2_negatives":
            (
                transition_23_event
                > stale_execution_event
                and
                transition_23_event
                > current_blocked_execution_event
            ),
        "transition":
            asdict(transition_23),
        "authoritative_state_after_transition":
            snapshot_dict(
                authoritative_v3_after_transition
            ),
        "historical_v2_state_preserved":
            snapshot_dict(
                authoritative_v2_for_current
            ),
        "historical_v1_snapshot_preserved":
            snapshot_dict(stale_snapshot_v1),
    }

    write_json(
        TRANSITION_23_PATH,
        transition_23_record,
    )

    # ========================================================
    # 14/15/16. FRESH V3 + RECOVERY POSITIVE
    # ========================================================

    v3_snapshot_capture_event = next_event()

    recovery_snapshot_v3 = peer_source.capture_snapshot()

    recovery_authority_event = next_event()

    auth_recovery = authority_source.issue(
        "AUTH_F13_RECOVERY"
    )

    recovery_before = authority_dict(
        auth_recovery
    )

    recovery_execution_event = next_event()

    authoritative_v3_for_recovery = (
        peer_source.current_state
    )

    recovery_result = gate.attempt(
        authority=auth_recovery,
        presenter_identity=F13_AGENT,
        local_peer_snapshot=recovery_snapshot_v3,
        authoritative_peer_state=(
            authoritative_v3_for_recovery
        ),
        action=F13_ACTION,
        target_tool=tool,
    )

    recovery_record = {
        "test_id":
            "EASA-F13-RECOVERY-POSITIVE",
        "observation_time_utc":
            observation_time,
        "transition_v2_v3_event_index":
            transition_23_event,
        "snapshot_capture_event_index":
            v3_snapshot_capture_event,
        "authority_issue_event_index":
            recovery_authority_event,
        "execution_event_index":
            recovery_execution_event,
        "authority_before_execution":
            recovery_before,
        "authority_contains_peer_state_fields":
            not authority_has_no_peer_state_fields(
                auth_recovery
            ),
        "local_snapshot":
            snapshot_dict(recovery_snapshot_v3),
        "authoritative_peer_state":
            snapshot_dict(
                authoritative_v3_for_recovery
            ),
        "execution":
            asdict(recovery_result),
        "authority_after_execution":
            authority_dict(auth_recovery),
        "tool_counter_after":
            tool.consequence_counter,
    }

    write_json(
        RECOVERY_PATH,
        recovery_record,
    )

    # ========================================================
    # AGGREGATE CHECKS
    # ========================================================

    v2_negative_total_delta = (
        stale_result.consequence_delta
        + current_blocked_result.consequence_delta
    )

    checks = {

        "peer_source_distinct_from_authority_source":
            (
                PEER_STATE_SOURCE_ID
                != AUTHORITY_SOURCE_ID
            ),

        "agent_distinct_from_peer":
            F13_AGENT != PEER_ID,

        "initial_state_v1":
            (
                authoritative_v1.state_identity
                == STATE_V1
                and authoritative_v1.version == 1
                and authoritative_v1.standing
                == PEER_READY
                and authoritative_v1.admissible
                is True
            ),

        "v1_snapshot_distinct_runtime_object":
            stale_snapshot_v1
            is not authoritative_v1,

        "v1_snapshot_exact":
            stale_snapshot_v1
            == authoritative_v1,

        # PRE-CHANGE POSITIVE

        "pre_authority_valid":
            auth_pre.valid is True,

        "pre_authority_no_peer_state_fields":
            authority_has_no_peer_state_fields(
                auth_pre
            ),

        "pre_versions_match":
            (
                pre_result.local_peer_version == 1
                and
                pre_result.authoritative_peer_version
                == 1
                and
                pre_result.freshness_correspondence
                is True
            ),

        "pre_peer_admissible":
            pre_result.authoritative_peer_admissible
            is True,

        "pre_permitted":
            pre_result.verdict == "PERMIT",

        "pre_reason_authorized":
            pre_result.reason == "AUTHORIZED",

        "pre_delta_one":
            pre_result.consequence_delta == 1,

        "pre_authority_consumed":
            auth_pre.consumed is True,

        # V1 -> V2

        "transition_12_after_pre_execution":
            transition_12_event
            > pre_execution_event,

        "transition_12_identity":
            transition_12.transition_identity
            == TRANSITION_V1_V2,

        "transition_12_versions":
            (
                transition_12.prior_version == 1
                and
                transition_12.resulting_version == 2
            ),

        "transition_12_standing":
            (
                transition_12.prior_standing
                == PEER_READY
                and
                transition_12.resulting_standing
                == PEER_WITHDRAWN
            ),

        "transition_12_admissibility":
            (
                transition_12.prior_admissible
                is True
                and
                transition_12.resulting_admissible
                is False
            ),

        "stale_snapshot_preserved_v1":
            (
                stale_snapshot_v1.state_identity
                == STATE_V1
                and
                stale_snapshot_v1.version == 1
                and
                stale_snapshot_v1.standing
                == PEER_READY
                and
                stale_snapshot_v1.admissible
                is True
            ),

        # STALE CASE

        "stale_authority_issued_after_v2":
            stale_authority_issue_event
            > transition_12_event,

        "stale_authority_valid":
            auth_stale.valid is True,

        "stale_authority_started_unconsumed":
            stale_authority_before[
                "consumed"
            ]
            is False,

        "stale_authority_no_peer_state_fields":
            authority_has_no_peer_state_fields(
                auth_stale
            ),

        "stale_local_version_1":
            stale_result.local_peer_version == 1,

        "stale_authoritative_version_2":
            stale_result.authoritative_peer_version
            == 2,

        "stale_freshness_false":
            stale_result.freshness_correspondence
            is False,

        "stale_authoritative_withdrawn":
            stale_result.authoritative_peer_standing
            == PEER_WITHDRAWN,

        "stale_refused":
            stale_result.verdict == "REFUSE",

        "stale_reason_peer_state_stale":
            stale_result.reason
            == "PEER_STATE_STALE",

        "stale_delta_zero":
            stale_result.consequence_delta == 0,

        "stale_authority_remains_unconsumed":
            auth_stale.consumed is False,

        "authoritative_v2_unchanged_after_stale":
            (
                peer_source.current_state.version == 3
                if False
                else
                stale_record[
                    "authoritative_peer_state_before"
                ]
                ==
                stale_record[
                    "authoritative_peer_state_after"
                ]
            ),

        "stale_snapshot_unchanged_after_attempt":
            (
                stale_record[
                    "local_snapshot"
                ]
                ==
                stale_record[
                    "preserved_stale_snapshot_after"
                ]
            ),

        # CURRENT V2 BLOCKED CASE

        "fresh_v2_captured_after_stale":
            v2_snapshot_capture_event
            > stale_execution_event,

        "current_v2_snapshot_correct":
            (
                current_snapshot_v2.state_identity
                == STATE_V2
                and
                current_snapshot_v2.version == 2
                and
                current_snapshot_v2.standing
                == PEER_WITHDRAWN
                and
                current_snapshot_v2.admissible
                is False
            ),

        "current_blocked_authority_valid":
            auth_current_blocked.valid is True,

        "current_blocked_authority_started_unconsumed":
            current_blocked_before[
                "consumed"
            ]
            is False,

        "current_blocked_authority_no_peer_state_fields":
            authority_has_no_peer_state_fields(
                auth_current_blocked
            ),

        "current_blocked_versions_match":
            (
                current_blocked_result.local_peer_version
                == 2
                and
                current_blocked_result.authoritative_peer_version
                == 2
                and
                current_blocked_result.freshness_correspondence
                is True
            ),

        "current_blocked_inadmissible":
            (
                current_blocked_result.authoritative_peer_standing
                == PEER_WITHDRAWN
                and
                current_blocked_result.authoritative_peer_admissible
                is False
            ),

        "current_blocked_refused":
            current_blocked_result.verdict
            == "REFUSE",

        "current_blocked_reason":
            current_blocked_result.reason
            == "PEER_STANDING_NOT_ADMISSIBLE",

        "current_blocked_delta_zero":
            current_blocked_result.consequence_delta
            == 0,

        "current_blocked_authority_remains_unconsumed":
            auth_current_blocked.consumed
            is False,

        "v2_negative_total_delta_zero":
            v2_negative_total_delta == 0,

        # V2 -> V3

        "transition_23_after_both_v2_negatives":
            (
                transition_23_event
                > stale_execution_event
                and
                transition_23_event
                > current_blocked_execution_event
            ),

        "transition_23_identity":
            transition_23.transition_identity
            == TRANSITION_V2_V3,

        "transition_23_versions":
            (
                transition_23.prior_version == 2
                and
                transition_23.resulting_version == 3
            ),

        "transition_23_standing":
            (
                transition_23.prior_standing
                == PEER_WITHDRAWN
                and
                transition_23.resulting_standing
                == PEER_READY
            ),

        "transition_23_admissibility":
            (
                transition_23.prior_admissible
                is False
                and
                transition_23.resulting_admissible
                is True
            ),

        "historical_v2_preserved":
            (
                authoritative_v2_for_current.state_identity
                == STATE_V2
                and
                authoritative_v2_for_current.version
                == 2
                and
                authoritative_v2_for_current.standing
                == PEER_WITHDRAWN
                and
                authoritative_v2_for_current.admissible
                is False
            ),

        "historical_v1_preserved":
            (
                stale_snapshot_v1.state_identity
                == STATE_V1
                and
                stale_snapshot_v1.version == 1
                and
                stale_snapshot_v1.standing
                == PEER_READY
            ),

        # RECOVERY

        "recovery_snapshot_v3":
            (
                recovery_snapshot_v3.state_identity
                == STATE_V3
                and
                recovery_snapshot_v3.version == 3
                and
                recovery_snapshot_v3.standing
                == PEER_READY
                and
                recovery_snapshot_v3.admissible
                is True
            ),

        "recovery_authority_after_v3":
            recovery_authority_event
            > transition_23_event,

        "recovery_authority_valid":
            auth_recovery.valid is True,

        "recovery_authority_started_unconsumed":
            recovery_before["consumed"]
            is False,

        "recovery_authority_no_peer_state_fields":
            authority_has_no_peer_state_fields(
                auth_recovery
            ),

        "recovery_versions_match":
            (
                recovery_result.local_peer_version
                == 3
                and
                recovery_result.authoritative_peer_version
                == 3
                and
                recovery_result.freshness_correspondence
                is True
            ),

        "recovery_peer_admissible":
            recovery_result.authoritative_peer_admissible
            is True,

        "recovery_permitted":
            recovery_result.verdict == "PERMIT",

        "recovery_reason_authorized":
            recovery_result.reason == "AUTHORIZED",

        "recovery_delta_one":
            recovery_result.consequence_delta
            == 1,

        "recovery_authority_consumed":
            auth_recovery.consumed is True,

        # FINAL

        "final_tool_counter_two":
            tool.consequence_counter == 2,

        "authority_source_issued_exact_four":
            (
                authority_source.issued_ids
                ==
                (
                    "AUTH_F13_PRE",
                    "AUTH_F13_STALE_VIEW",
                    "AUTH_F13_CURRENT_BLOCKED",
                    "AUTH_F13_RECOVERY",
                )
            ),

        "stale_refusal_not_authority_failure":
            stale_result.reason
            not in {
                "EXECUTION_AUTHORITY_ISSUER_NOT_AUTHORIZED",
                "EXECUTION_AUTHORITY_INVALID",
                "EXECUTION_AUTHORITY_ALREADY_CONSUMED",
                "PRESENTER_IDENTITY_MISMATCH",
                "EXECUTION_SCOPE_NOT_AUTHORIZED",
                "TOOL_IDENTITY_MISMATCH",
            },

        "no_authority_epoch_required":
            (
                "authority_epoch"
                not in vars(auth_stale)
            ),
    }

    overall_pass = all(checks.values())

    summary = {
        "examination":
            "EASA-F13",

        "property":
            "STALE_PEER_STATE_ISOLATION",

        "observation_time_utc":
            observation_time,

        "peer_state_source_identity":
            peer_source.source_identity,

        "authority_source_identity":
            authority_source.source_identity,

        "stale_snapshot": {
            "state_identity":
                stale_snapshot_v1.state_identity,
            "version":
                stale_snapshot_v1.version,
            "standing":
                stale_snapshot_v1.standing,
            "admissible":
                stale_snapshot_v1.admissible,
        },

        "pre_change_positive": {
            "authority_id":
                auth_pre.authority_id,
            "local_version":
                pre_result.local_peer_version,
            "authoritative_version":
                pre_result.authoritative_peer_version,
            "freshness":
                pre_result.freshness_correspondence,
            "verdict":
                pre_result.verdict,
            "reason":
                pre_result.reason,
            "consequence_delta":
                pre_result.consequence_delta,
        },

        "transition_v1_v2": {
            **asdict(transition_12),
            "event_index":
                transition_12_event,
        },

        "stale_attempt": {
            "authority_id":
                auth_stale.authority_id,
            "authority_issue_event_index":
                stale_authority_issue_event,
            "execution_event_index":
                stale_execution_event,
            "authority_issued_after_v2_transition":
                stale_authority_issue_event
                > transition_12_event,
            "authority_contains_peer_state_fields":
                not authority_has_no_peer_state_fields(
                    auth_stale
                ),
            "local_version":
                stale_result.local_peer_version,
            "authoritative_version":
                stale_result.authoritative_peer_version,
            "freshness":
                stale_result.freshness_correspondence,
            "verdict":
                stale_result.verdict,
            "reason":
                stale_result.reason,
            "consequence_delta":
                stale_result.consequence_delta,
            "consumed_after":
                auth_stale.consumed,
        },

        "current_blocked_attempt": {
            "authority_id":
                auth_current_blocked.authority_id,
            "local_version":
                current_blocked_result.local_peer_version,
            "authoritative_version":
                current_blocked_result.authoritative_peer_version,
            "freshness":
                current_blocked_result.freshness_correspondence,
            "authoritative_standing":
                current_blocked_result.authoritative_peer_standing,
            "authoritative_admissible":
                current_blocked_result.authoritative_peer_admissible,
            "verdict":
                current_blocked_result.verdict,
            "reason":
                current_blocked_result.reason,
            "consequence_delta":
                current_blocked_result.consequence_delta,
            "consumed_after":
                auth_current_blocked.consumed,
        },

        "version_2_negative_total_delta":
            v2_negative_total_delta,

        "transition_v2_v3": {
            **asdict(transition_23),
            "event_index":
                transition_23_event,
        },

        "recovery_positive": {
            "authority_id":
                auth_recovery.authority_id,
            "local_version":
                recovery_result.local_peer_version,
            "authoritative_version":
                recovery_result.authoritative_peer_version,
            "freshness":
                recovery_result.freshness_correspondence,
            "verdict":
                recovery_result.verdict,
            "reason":
                recovery_result.reason,
            "consequence_delta":
                recovery_result.consequence_delta,
            "consumed_after":
                auth_recovery.consumed,
        },

        "final_tool_consequence_counter":
            tool.consequence_counter,

        "final_authoritative_peer_state":
            snapshot_dict(peer_source.current_state),

        "authority_source":
            source_dict(authority_source),

        "event_order": {
            "initial":
                initial_event,
            "pre_authority_issue":
                pre_authority_issue_event,
            "pre_execution":
                pre_execution_event,
            "transition_v1_v2":
                transition_12_event,
            "stale_authority_issue":
                stale_authority_issue_event,
            "stale_execution":
                stale_execution_event,
            "v2_snapshot_capture":
                v2_snapshot_capture_event,
            "current_blocked_authority_issue":
                current_blocked_authority_event,
            "current_blocked_execution":
                current_blocked_execution_event,
            "transition_v2_v3":
                transition_23_event,
            "v3_snapshot_capture":
                v3_snapshot_capture_event,
            "recovery_authority_issue":
                recovery_authority_event,
            "recovery_execution":
                recovery_execution_event,
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

    print("=== EASA-F13 FIRST OBSERVATION ===")

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