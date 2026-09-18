from __future__ import annotations

import json
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = ROOT / "03_controls"

if str(CONTROL_DIR) not in sys.path:
    sys.path.insert(
        0,
        str(CONTROL_DIR),
    )


from easa_f15_resolver import (  # noqa: E402
    AuthoritativeStateSource,
    ResolverReplica,
    RESOLVER_A_ID,
    RESOLVER_B_ID,
)
from easa_f15_execution import (  # noqa: E402
    F15_ACTION,
    F15_PRESENTER,
    F15_TOOL,
    ConsequentialTool,
    F15ExecutionGate,
    constitute_authority,
)


EVIDENCE_DIR = (
    ROOT
    / "05_evidence"
    / "EASA-F15"
)

INITIAL_STATE_PATH = (
    EVIDENCE_DIR
    / "EASA-F15-INITIAL-STATE.json"
)

BASELINE_PATH = (
    EVIDENCE_DIR
    / "EASA-F15-BASELINE-POSITIVE.json"
)

TRANSITION_R1_R2_PATH = (
    EVIDENCE_DIR
    / "EASA-F15-TRANSITION-R1-R2.json"
)

PARTITION_STATE_PATH = (
    EVIDENCE_DIR
    / "EASA-F15-PARTITION-STATE.json"
)

PARTITION_NEGATIVE_PATH = (
    EVIDENCE_DIR
    / "EASA-F15-PARTITION-NEGATIVE.json"
)

CONFLICT_STATE_PATH = (
    EVIDENCE_DIR
    / "EASA-F15-CONFLICT-STATE.json"
)

CONFLICT_NEGATIVE_PATH = (
    EVIDENCE_DIR
    / "EASA-F15-CONFLICT-NEGATIVE.json"
)

HEALED_R2_PATH = (
    EVIDENCE_DIR
    / "EASA-F15-HEALED-R2-STATE.json"
)

CURRENT_BLOCKED_PATH = (
    EVIDENCE_DIR
    / "EASA-F15-CURRENT-BLOCKED-NEGATIVE.json"
)

TRANSITION_R2_R3_PATH = (
    EVIDENCE_DIR
    / "EASA-F15-TRANSITION-R2-R3.json"
)

RECOVERED_R3_PATH = (
    EVIDENCE_DIR
    / "EASA-F15-RECOVERED-R3-STATE.json"
)

RECOVERY_PATH = (
    EVIDENCE_DIR
    / "EASA-F15-RECOVERY-POSITIVE.json"
)

SUMMARY_PATH = (
    EVIDENCE_DIR
    / "EASA-F15-SUMMARY.json"
)


ALL_RUNTIME_PATHS = (
    INITIAL_STATE_PATH,
    BASELINE_PATH,
    TRANSITION_R1_R2_PATH,
    PARTITION_STATE_PATH,
    PARTITION_NEGATIVE_PATH,
    CONFLICT_STATE_PATH,
    CONFLICT_NEGATIVE_PATH,
    HEALED_R2_PATH,
    CURRENT_BLOCKED_PATH,
    TRANSITION_R2_R3_PATH,
    RECOVERED_R3_PATH,
    RECOVERY_PATH,
    SUMMARY_PATH,
)


def utc_now() -> str:

    return datetime.now(
        timezone.utc
    ).isoformat()


def write_json(
    path: Path,
    value: dict,
) -> None:

    path.write_text(
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def resolver_snapshot(
    resolver: ResolverReplica,
) -> dict:

    return asdict(
        resolver.observe()
    )


def decision_record(
    decision,
) -> dict:

    return asdict(
        decision
    )


def authority_state(
    authority,
) -> dict:

    return {
        "authority_id":
            authority.authority_id,

        "subject_identity":
            authority.subject_identity,

        "authorized_action":
            authority.authorized_action,

        "bound_tool_identity":
            authority.bound_tool_identity,

        "valid":
            authority.valid,

        "consumed":
            authority.consumed,
    }


def main() -> int:

    existing = [
        str(path)
        for path in ALL_RUNTIME_PATHS
        if path.exists()
    ]

    if existing:

        print(
            "F15 FIRST-OBSERVATION EVIDENCE ALREADY EXISTS — STOP"
        )

        for path in existing:
            print(path)

        return 2

    EVIDENCE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    observation_time = utc_now()

    # ========================================================
    # CONSTITUTE EXACT FROZEN RUNTIME
    # ========================================================

    source = AuthoritativeStateSource()

    resolver_a = ResolverReplica(
        RESOLVER_A_ID
    )

    resolver_b = ResolverReplica(
        RESOLVER_B_ID
    )

    resolver_a.synchronize(
        source
    )

    resolver_b.synchronize(
        source
    )

    tool = ConsequentialTool()

    gate = F15ExecutionGate()

    baseline_authority = (
        constitute_authority(
            "AUTH_F15-BASELINE"
        )
    )

    partition_authority = (
        constitute_authority(
            "AUTH_F15-PARTITION"
        )
    )

    conflict_authority = (
        constitute_authority(
            "AUTH_F15-CONFLICT"
        )
    )

    current_blocked_authority = (
        constitute_authority(
            "AUTH_F15-CURRENT-BLOCKED"
        )
    )

    recovery_authority = (
        constitute_authority(
            "AUTH_F15-RECOVERY"
        )
    )

    # ========================================================
    # F15-S0 — INITIAL STATE
    # ========================================================

    initial_state = {
        "examination":
            "EASA-F15",

        "stage":
            "F15-S0",

        "observation_time_utc":
            observation_time,

        "authoritative_source_identity":
            source.source_identity,

        "authoritative_state":
            source.snapshot(),

        "resolver_a":
            resolver_snapshot(
                resolver_a
            ),

        "resolver_b":
            resolver_snapshot(
                resolver_b
            ),

        "tool_identity":
            F15_TOOL,

        "tool_counter":
            tool.consequence_counter,

        "presenter_identity":
            F15_PRESENTER,

        "action":
            F15_ACTION,
    }

    write_json(
        INITIAL_STATE_PATH,
        initial_state,
    )

    historical_r1_cache = (
        source.snapshot()
    )

    # ========================================================
    # F15-S1 — BASELINE POSITIVE
    # ========================================================

    baseline = gate.attempt(
        attempt_id=(
            "F15-ATTEMPT-BASELINE"
        ),
        presenter_identity=(
            F15_PRESENTER
        ),
        authority=(
            baseline_authority
        ),
        action=F15_ACTION,
        tool=tool,
        state_source=source,
        resolver_a=resolver_a,
        resolver_b=resolver_b,
        cached_state=None,
    )

    baseline_record = {
        "examination":
            "EASA-F15",

        "stage":
            "F15-S1",

        "authority_after":
            authority_state(
                baseline_authority
            ),

        "decision":
            decision_record(
                baseline
            ),
    }

    write_json(
        BASELINE_PATH,
        baseline_record,
    )

    # ========================================================
    # F15-S2 — R1 -> R2
    # ========================================================

    transition_r1_r2 = (
        source.transition(
            expected_from_version="R1",
            to_version="R2",
            to_state="WITHDRAWN",
            to_admissible=False,
        )
    )

    transition_r1_r2_record = {
        "examination":
            "EASA-F15",

        "stage":
            "F15-S2",

        "transition":
            transition_r1_r2,

        "historical_cache":
            historical_r1_cache,
    }

    write_json(
        TRANSITION_R1_R2_PATH,
        transition_r1_r2_record,
    )

    # ========================================================
    # F15-S3 — PARTITION / CURRENT RESOLUTION UNAVAILABLE
    # ========================================================

    resolver_a.set_unavailable()
    resolver_b.set_unavailable()

    partition_state_record = {
        "examination":
            "EASA-F15",

        "stage":
            "F15-S3-STATE",

        "authoritative_state":
            source.snapshot(),

        "resolver_a":
            resolver_snapshot(
                resolver_a
            ),

        "resolver_b":
            resolver_snapshot(
                resolver_b
            ),

        "historical_cached_state":
            historical_r1_cache,

        "tool_counter_before_attempt":
            tool.consequence_counter,
    }

    write_json(
        PARTITION_STATE_PATH,
        partition_state_record,
    )

    partition = gate.attempt(
        attempt_id=(
            "F15-ATTEMPT-PARTITION"
        ),
        presenter_identity=(
            F15_PRESENTER
        ),
        authority=(
            partition_authority
        ),
        action=F15_ACTION,
        tool=tool,
        state_source=source,
        resolver_a=resolver_a,
        resolver_b=resolver_b,
        cached_state=(
            historical_r1_cache
        ),
    )

    partition_record = {
        "examination":
            "EASA-F15",

        "stage":
            "F15-S3-NEGATIVE",

        "authority_after":
            authority_state(
                partition_authority
            ),

        "decision":
            decision_record(
                partition
            ),
    }

    write_json(
        PARTITION_NEGATIVE_PATH,
        partition_record,
    )

    # ========================================================
    # F15-S4 — CONFLICT
    # ========================================================

    resolver_a.force_view(
        state_version="R1",
        state="READY",
        admissible=True,
    )

    resolver_b.force_view(
        state_version="R2",
        state="WITHDRAWN",
        admissible=False,
    )

    conflict_state_record = {
        "examination":
            "EASA-F15",

        "stage":
            "F15-S4-STATE",

        "authoritative_state":
            source.snapshot(),

        "resolver_a":
            resolver_snapshot(
                resolver_a
            ),

        "resolver_b":
            resolver_snapshot(
                resolver_b
            ),

        "tool_counter_before_attempt":
            tool.consequence_counter,
    }

    write_json(
        CONFLICT_STATE_PATH,
        conflict_state_record,
    )

    conflict = gate.attempt(
        attempt_id=(
            "F15-ATTEMPT-CONFLICT"
        ),
        presenter_identity=(
            F15_PRESENTER
        ),
        authority=(
            conflict_authority
        ),
        action=F15_ACTION,
        tool=tool,
        state_source=source,
        resolver_a=resolver_a,
        resolver_b=resolver_b,
        cached_state=(
            historical_r1_cache
        ),
    )

    conflict_record = {
        "examination":
            "EASA-F15",

        "stage":
            "F15-S4-NEGATIVE",

        "authority_after":
            authority_state(
                conflict_authority
            ),

        "decision":
            decision_record(
                conflict
            ),
    }

    write_json(
        CONFLICT_NEGATIVE_PATH,
        conflict_record,
    )

    # ========================================================
    # F15-S5 — HEALED BUT CURRENT STATE INADMISSIBLE
    # ========================================================

    resolver_a.synchronize(
        source
    )

    resolver_b.synchronize(
        source
    )

    healed_r2_record = {
        "examination":
            "EASA-F15",

        "stage":
            "F15-S5-STATE",

        "authoritative_state":
            source.snapshot(),

        "resolver_a":
            resolver_snapshot(
                resolver_a
            ),

        "resolver_b":
            resolver_snapshot(
                resolver_b
            ),

        "tool_counter_before_attempt":
            tool.consequence_counter,
    }

    write_json(
        HEALED_R2_PATH,
        healed_r2_record,
    )

    current_blocked = gate.attempt(
        attempt_id=(
            "F15-ATTEMPT-CURRENT-BLOCKED"
        ),
        presenter_identity=(
            F15_PRESENTER
        ),
        authority=(
            current_blocked_authority
        ),
        action=F15_ACTION,
        tool=tool,
        state_source=source,
        resolver_a=resolver_a,
        resolver_b=resolver_b,
        cached_state=None,
    )

    current_blocked_record = {
        "examination":
            "EASA-F15",

        "stage":
            "F15-S5-NEGATIVE",

        "authority_after":
            authority_state(
                current_blocked_authority
            ),

        "decision":
            decision_record(
                current_blocked
            ),
    }

    write_json(
        CURRENT_BLOCKED_PATH,
        current_blocked_record,
    )

    # ========================================================
    # F15-S6 — R2 -> R3 PROSPECTIVE RECOVERY
    # ========================================================

    transition_r2_r3 = (
        source.transition(
            expected_from_version="R2",
            to_version="R3",
            to_state="READY",
            to_admissible=True,
        )
    )

    transition_r2_r3_record = {
        "examination":
            "EASA-F15",

        "stage":
            "F15-S6-TRANSITION",

        "transition":
            transition_r2_r3,
    }

    write_json(
        TRANSITION_R2_R3_PATH,
        transition_r2_r3_record,
    )

    resolver_a.synchronize(
        source
    )

    resolver_b.synchronize(
        source
    )

    recovered_r3_record = {
        "examination":
            "EASA-F15",

        "stage":
            "F15-S6-STATE",

        "authoritative_state":
            source.snapshot(),

        "resolver_a":
            resolver_snapshot(
                resolver_a
            ),

        "resolver_b":
            resolver_snapshot(
                resolver_b
            ),

        "tool_counter_before_attempt":
            tool.consequence_counter,
    }

    write_json(
        RECOVERED_R3_PATH,
        recovered_r3_record,
    )

    recovery = gate.attempt(
        attempt_id=(
            "F15-ATTEMPT-RECOVERY"
        ),
        presenter_identity=(
            F15_PRESENTER
        ),
        authority=(
            recovery_authority
        ),
        action=F15_ACTION,
        tool=tool,
        state_source=source,
        resolver_a=resolver_a,
        resolver_b=resolver_b,
        cached_state=None,
    )

    recovery_record = {
        "examination":
            "EASA-F15",

        "stage":
            "F15-S6-POSITIVE",

        "authority_after":
            authority_state(
                recovery_authority
            ),

        "decision":
            decision_record(
                recovery
            ),
    }

    write_json(
        RECOVERY_PATH,
        recovery_record,
    )

    # ========================================================
    # DETERMINISTIC ADJUDICATION INPUT
    # ========================================================

    decisions = [
        baseline,
        partition,
        conflict,
        current_blocked,
        recovery,
    ]

    permit_decisions = [
        decision
        for decision in decisions
        if decision.verdict == "PERMIT"
    ]

    refuse_decisions = [
        decision
        for decision in decisions
        if decision.verdict == "REFUSE"
    ]

    refusal_reasons = [
        decision.reason
        for decision in refuse_decisions
    ]

    negative_decisions = [
        partition,
        conflict,
        current_blocked,
    ]

    unauthorized_consequence_total = sum(
        decision.consequence_delta
        for decision in negative_decisions
    )

    checks = {

        # Initial state
        "initial_authoritative_r1_ready_true":
            (
                initial_state[
                    "authoritative_state"
                ][
                    "state_version"
                ] == "R1"
                and
                initial_state[
                    "authoritative_state"
                ][
                    "state"
                ] == "READY"
                and
                initial_state[
                    "authoritative_state"
                ][
                    "admissible"
                ] is True
            ),

        "initial_resolver_a_r1_ready_true":
            (
                initial_state[
                    "resolver_a"
                ][
                    "available"
                ] is True
                and
                initial_state[
                    "resolver_a"
                ][
                    "state_version"
                ] == "R1"
                and
                initial_state[
                    "resolver_a"
                ][
                    "state"
                ] == "READY"
                and
                initial_state[
                    "resolver_a"
                ][
                    "admissible"
                ] is True
            ),

        "initial_resolver_b_r1_ready_true":
            (
                initial_state[
                    "resolver_b"
                ][
                    "available"
                ] is True
                and
                initial_state[
                    "resolver_b"
                ][
                    "state_version"
                ] == "R1"
                and
                initial_state[
                    "resolver_b"
                ][
                    "state"
                ] == "READY"
                and
                initial_state[
                    "resolver_b"
                ][
                    "admissible"
                ] is True
            ),

        # Baseline
        "baseline_permit":
            baseline.verdict
            == "PERMIT",

        "baseline_reason_authorized":
            baseline.reason
            == "AUTHORIZED",

        "baseline_delta_one":
            baseline.consequence_delta
            == 1,

        "baseline_authority_started_unconsumed":
            baseline.authority_consumed_before
            is False,

        "baseline_authority_consumed_after":
            baseline.authority_consumed_after
            is True,

        # Transition R1 -> R2
        "transition_r1_r2_exact":
            (
                transition_r1_r2[
                    "before"
                ][
                    "state_version"
                ] == "R1"
                and
                transition_r1_r2[
                    "after"
                ][
                    "state_version"
                ] == "R2"
                and
                transition_r1_r2[
                    "after"
                ][
                    "state"
                ] == "WITHDRAWN"
                and
                transition_r1_r2[
                    "after"
                ][
                    "admissible"
                ] is False
            ),

        "historical_cache_remains_r1":
            (
                historical_r1_cache[
                    "state_version"
                ] == "R1"
                and
                historical_r1_cache[
                    "state"
                ] == "READY"
                and
                historical_r1_cache[
                    "admissible"
                ] is True
            ),

        # Partition
        "partition_resolvers_unavailable":
            (
                partition.resolver_a_availability
                is False
                and
                partition.resolver_b_availability
                is False
            ),

        "partition_refuse":
            partition.verdict
            == "REFUSE",

        "partition_reason_exact":
            partition.reason
            == "CURRENT_RESOLUTION_UNAVAILABLE",

        "partition_resolution_status_unavailable":
            partition.resolution_status
            == "UNAVAILABLE",

        "partition_delta_zero":
            partition.consequence_delta
            == 0,

        "partition_authority_remains_unconsumed":
            (
                partition.authority_consumed_before
                is False
                and
                partition.authority_consumed_after
                is False
                and
                partition_authority.consumed
                is False
            ),

        "partition_preserves_cached_r1":
            (
                partition.cached_state_version
                == "R1"
                and
                partition.cached_state
                == "READY"
                and
                partition.cached_admissibility
                is True
            ),

        # Conflict
        "conflict_exact_split_view":
            (
                conflict.resolver_a_state_version
                == "R1"
                and
                conflict.resolver_a_state
                == "READY"
                and
                conflict.resolver_a_admissibility
                is True
                and
                conflict.resolver_b_state_version
                == "R2"
                and
                conflict.resolver_b_state
                == "WITHDRAWN"
                and
                conflict.resolver_b_admissibility
                is False
            ),

        "conflict_refuse":
            conflict.verdict
            == "REFUSE",

        "conflict_reason_exact":
            conflict.reason
            == "RESOLVER_STATE_CONFLICT",

        "conflict_status_exact":
            conflict.resolution_status
            == "CONFLICT",

        "conflict_delta_zero":
            conflict.consequence_delta
            == 0,

        "conflict_authority_remains_unconsumed":
            (
                conflict.authority_consumed_before
                is False
                and
                conflict.authority_consumed_after
                is False
                and
                conflict_authority.consumed
                is False
            ),

        # Healed R2 but inadmissible
        "healed_r2_resolvers_correspond":
            (
                current_blocked.resolver_a_state_version
                == "R2"
                and
                current_blocked.resolver_a_state
                == "WITHDRAWN"
                and
                current_blocked.resolver_a_admissibility
                is False
                and
                current_blocked.resolver_b_state_version
                == "R2"
                and
                current_blocked.resolver_b_state
                == "WITHDRAWN"
                and
                current_blocked.resolver_b_admissibility
                is False
            ),

        "current_blocked_refuse":
            current_blocked.verdict
            == "REFUSE",

        "current_blocked_reason_exact":
            current_blocked.reason
            == "RESOLVED_STATE_NOT_ADMISSIBLE",

        "current_blocked_status_exact":
            current_blocked.resolution_status
            == "CURRENT_CONSISTENT_INADMISSIBLE",

        "current_blocked_delta_zero":
            current_blocked.consequence_delta
            == 0,

        "current_blocked_authority_remains_unconsumed":
            (
                current_blocked.authority_consumed_before
                is False
                and
                current_blocked.authority_consumed_after
                is False
                and
                current_blocked_authority.consumed
                is False
            ),

        # R2 -> R3
        "transition_r2_r3_exact":
            (
                transition_r2_r3[
                    "before"
                ][
                    "state_version"
                ] == "R2"
                and
                transition_r2_r3[
                    "after"
                ][
                    "state_version"
                ] == "R3"
                and
                transition_r2_r3[
                    "after"
                ][
                    "state"
                ] == "READY"
                and
                transition_r2_r3[
                    "after"
                ][
                    "admissible"
                ] is True
            ),

        # Recovery
        "recovery_resolvers_r3_ready_true":
            (
                recovery.resolver_a_state_version
                == "R3"
                and
                recovery.resolver_a_state
                == "READY"
                and
                recovery.resolver_a_admissibility
                is True
                and
                recovery.resolver_b_state_version
                == "R3"
                and
                recovery.resolver_b_state
                == "READY"
                and
                recovery.resolver_b_admissibility
                is True
            ),

        "recovery_permit":
            recovery.verdict
            == "PERMIT",

        "recovery_reason_authorized":
            recovery.reason
            == "AUTHORIZED",

        "recovery_delta_one":
            recovery.consequence_delta
            == 1,

        "recovery_authority_started_unconsumed":
            recovery.authority_consumed_before
            is False,

        "recovery_authority_consumed_after":
            recovery.authority_consumed_after
            is True,

        # Aggregate
        "attempt_count_five":
            len(decisions)
            == 5,

        "permit_count_two":
            len(permit_decisions)
            == 2,

        "refuse_count_three":
            len(refuse_decisions)
            == 3,

        "expected_refusal_reasons_exact":
            sorted(
                refusal_reasons
            )
            == sorted(
                [
                    "CURRENT_RESOLUTION_UNAVAILABLE",
                    "RESOLVER_STATE_CONFLICT",
                    "RESOLVED_STATE_NOT_ADMISSIBLE",
                ]
            ),

        "unauthorized_consequence_total_zero":
            unauthorized_consequence_total
            == 0,

        "final_tool_counter_two":
            tool.consequence_counter
            == 2,

        "evidence_delta_equals_tool_counter":
            sum(
                decision.consequence_delta
                for decision in decisions
            )
            == tool.consequence_counter,

        "all_negative_authorities_valid":
            (
                partition.authority_valid
                is True
                and
                conflict.authority_valid
                is True
                and
                current_blocked.authority_valid
                is True
            ),

        "all_negative_authorities_unconsumed_after":
            (
                partition_authority.consumed
                is False
                and
                conflict_authority.consumed
                is False
                and
                current_blocked_authority.consumed
                is False
            ),
    }

    overall_pass = all(
        checks.values()
    )

    summary = {
        "examination":
            "EASA-F15",

        "property":
            "RESOLVER_PARTITION_SAFE_DEGRADATION",

        "observation_time_utc":
            observation_time,

        "attempt_count":
            len(decisions),

        "permit_count":
            len(permit_decisions),

        "refuse_count":
            len(refuse_decisions),

        "refusal_reasons":
            refusal_reasons,

        "unauthorized_consequence_total":
            unauthorized_consequence_total,

        "aggregate_evidence_consequence_delta":
            sum(
                decision.consequence_delta
                for decision in decisions
            ),

        "final_tool_consequence_counter":
            tool.consequence_counter,

        "baseline_authority_final_consumed":
            baseline_authority.consumed,

        "partition_authority_final_consumed":
            partition_authority.consumed,

        "conflict_authority_final_consumed":
            conflict_authority.consumed,

        "current_blocked_authority_final_consumed":
            current_blocked_authority.consumed,

        "recovery_authority_final_consumed":
            recovery_authority.consumed,

        "final_authoritative_state":
            source.snapshot(),

        "final_resolver_a":
            resolver_snapshot(
                resolver_a
            ),

        "final_resolver_b":
            resolver_snapshot(
                resolver_b
            ),

        "checks":
            checks,

        "overall_result":
            (
                "PASS"
                if overall_pass
                else "FAIL"
            ),

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

    print(
        "=== EASA-F15 FIRST OBSERVATION ==="
    )

    print(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
    )

    return (
        0
        if overall_pass
        else 1
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )