from __future__ import annotations

import hashlib
import json
import sys
import threading
from collections import Counter
from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)
from dataclasses import asdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CONTROL_DIR = ROOT / "03_controls"

if str(CONTROL_DIR) not in sys.path:

    sys.path.insert(
        0,
        str(CONTROL_DIR),
    )


from easa_f17_execution import (  # noqa: E402
    ConsequentialTool,
    ExecutionAuthority,
    F17CompositeExecutionGate,
    F17_HIGH_ACTION,
    F17_LOW_ACTION,
    F17_OTHER_TOOL,
    F17_PRIMARY_TOOL,
)

from easa_f17_state import (  # noqa: E402
    AuthoritativeStateSource,
    PeerStateView,
    ResolverReplica,
)


EVIDENCE_DIR = (
    ROOT
    / "05_evidence"
    / "EASA-F17"
)

TRANSITIONS_PATH = (
    EVIDENCE_DIR
    / "EASA-F17-STATE-TRANSITIONS.json"
)

COMPOSITE_PATH = (
    EVIDENCE_DIR
    / "EASA-F17-COMPOSITE-EVIDENCE.json"
)

SUMMARY_PATH = (
    EVIDENCE_DIR
    / "EASA-F17-SUMMARY.json"
)


EXPECTED_REASON_COUNTS = {
    "EXECUTION_AUTHORITY_NOT_PRESENT":
        2,

    "PRESENTER_IDENTITY_MISMATCH":
        1,

    "TOOL_IDENTITY_MISMATCH":
        1,

    "EXECUTION_SCOPE_NOT_AUTHORIZED":
        2,

    "EXECUTION_AUTHORITY_ALREADY_CONSUMED":
        2,

    "EXECUTION_AUTHORITY_EPOCH_CHANGED":
        1,

    "HUMAN_AUTHORITY_REQUIRED":
        1,

    "DELEGATION_SCOPE_AMPLIFICATION":
        1,

    "PEER_STATE_STALE":
        1,

    "CURRENT_RESOLUTION_UNAVAILABLE":
        1,

    "RESOLVER_STATE_CONFLICT":
        1,

    "RESOLVED_STATE_NOT_ADMISSIBLE":
        1,
}


EXPECTED_SINGLE_ATTEMPTS = {
    "F17-C01-ATTEMPT":
        ("PERMIT", "AUTHORIZED"),

    "F17-C02-ATTEMPT":
        ("PERMIT", "AUTHORIZED"),

    "F17-C03-ATTEMPT":
        (
            "REFUSE",
            "EXECUTION_AUTHORITY_NOT_PRESENT",
        ),

    "F17-C04-ATTEMPT":
        (
            "REFUSE",
            "PRESENTER_IDENTITY_MISMATCH",
        ),

    "F17-C05-ATTEMPT":
        (
            "REFUSE",
            "TOOL_IDENTITY_MISMATCH",
        ),

    "F17-C06-ATTEMPT":
        (
            "REFUSE",
            "EXECUTION_SCOPE_NOT_AUTHORIZED",
        ),

    "F17-C07-ATTEMPT":
        (
            "REFUSE",
            "EXECUTION_AUTHORITY_ALREADY_CONSUMED",
        ),

    "F17-C08-ATTEMPT":
        (
            "REFUSE",
            "EXECUTION_AUTHORITY_EPOCH_CHANGED",
        ),

    "F17-C09-ATTEMPT":
        (
            "REFUSE",
            "HUMAN_AUTHORITY_REQUIRED",
        ),

    "F17-C10-ATTEMPT":
        (
            "REFUSE",
            "EXECUTION_SCOPE_NOT_AUTHORIZED",
        ),

    "F17-C11-ATTEMPT":
        (
            "REFUSE",
            "DELEGATION_SCOPE_AMPLIFICATION",
        ),

    "F17-C12-ATTEMPT":
        (
            "REFUSE",
            "EXECUTION_AUTHORITY_NOT_PRESENT",
        ),

    "F17-C13-ATTEMPT":
        (
            "REFUSE",
            "PEER_STATE_STALE",
        ),

    "F17-C14-ATTEMPT":
        (
            "REFUSE",
            "CURRENT_RESOLUTION_UNAVAILABLE",
        ),

    "F17-C15A-ATTEMPT":
        (
            "REFUSE",
            "RESOLVER_STATE_CONFLICT",
        ),

    "F17-C15B-ATTEMPT":
        (
            "REFUSE",
            "RESOLVED_STATE_NOT_ADMISSIBLE",
        ),

    "F17-C17-ATTEMPT":
        ("PERMIT", "AUTHORIZED"),
}


def canonical_bytes(
    value,
) -> bytes:

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode(
        "utf-8"
    )


def sha256_hex(
    data: bytes,
) -> str:

    return hashlib.sha256(
        data
    ).hexdigest().upper()


def write_json(
    path: Path,
    value,
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


def authority(
    *,
    authority_id: str,
    subject: str,
    action: str,
    tool: str,
    epoch: int,
    consumed: bool = False,
) -> ExecutionAuthority:

    return ExecutionAuthority(
        authority_id=authority_id,
        subject_identity=subject,
        authorized_action=action,
        authorized_tool_identity=tool,
        authority_epoch=epoch,
        valid=True,
        consumed=consumed,
    )


def main() -> int:

    expected_paths = [
        TRANSITIONS_PATH,
        COMPOSITE_PATH,
        SUMMARY_PATH,
    ]

    existing = [
        str(path)
        for path in expected_paths
        if path.exists()
    ]

    if existing:

        print(
            "F17 FIRST-OBSERVATION EVIDENCE "
            "ALREADY EXISTS — STOP"
        )

        for path in existing:
            print(path)

        return 2

    EVIDENCE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    source = (
        AuthoritativeStateSource()
    )

    resolver_a = ResolverReplica(
        "RESOLVER_F17_A"
    )

    resolver_b = ResolverReplica(
        "RESOLVER_F17_B"
    )

    primary_tool = ConsequentialTool(
        F17_PRIMARY_TOOL
    )

    alternate_tool = ConsequentialTool(
        F17_OTHER_TOOL
    )

    gate = (
        F17CompositeExecutionGate()
    )

    outcomes = []

    transitions = []

    authorities = {}

    # --------------------------------------------------------
    # EPOCH 1 INITIALIZATION
    # --------------------------------------------------------

    current = source.snapshot()

    resolver_a.synchronize(
        current
    )

    resolver_b.synchronize(
        current
    )

    peer_e1 = PeerStateView(
        epoch=1,
        state="READY",
        admissible=True,
    )

    # --------------------------------------------------------
    # CASE 01 — AUTHORIZED LOW
    # --------------------------------------------------------

    authorities["C01"] = authority(
        authority_id="AUTH_F17_C01",
        subject="AGENT_F17_ALPHA",
        action=F17_LOW_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=1,
    )

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C01-AUTHORIZED-LOW"
            ),
            attempt_id=(
                "F17-C01-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_ALPHA"
            ),
            authority=(
                authorities["C01"]
            ),
            requested_action=(
                F17_LOW_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e1
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
        )
    )

    # --------------------------------------------------------
    # CASE 02 — AUTHORIZED HIGH WITH HUMAN
    # --------------------------------------------------------

    authorities["C02"] = authority(
        authority_id="AUTH_F17_C02",
        subject="AGENT_F17_BETA",
        action=F17_HIGH_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=1,
    )

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C02-AUTHORIZED-HIGH-HUMAN-PRESENT"
            ),
            attempt_id=(
                "F17-C02-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_BETA"
            ),
            authority=(
                authorities["C02"]
            ),
            requested_action=(
                F17_HIGH_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e1
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
            human_authority_required=True,
            human_authority_present=True,
        )
    )

    # --------------------------------------------------------
    # CASE 03 — NO AUTHORITY + ADVISORY PERMIT
    # --------------------------------------------------------

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C03-NO-AUTHORITY"
            ),
            attempt_id=(
                "F17-C03-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_GAMMA"
            ),
            authority=None,
            requested_action=(
                F17_LOW_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e1
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
            advisory_permit_votes=1,
            advisory_refuse_votes=0,
            advisory_result="PERMIT",
        )
    )

    # --------------------------------------------------------
    # CASE 04 — IDENTITY MISMATCH
    # --------------------------------------------------------

    authorities["C04"] = authority(
        authority_id="AUTH_F17_C04",
        subject="AGENT_F17_OTHER",
        action=F17_LOW_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=1,
    )

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C04-IDENTITY-MISMATCH"
            ),
            attempt_id=(
                "F17-C04-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_DELTA"
            ),
            authority=(
                authorities["C04"]
            ),
            requested_action=(
                F17_LOW_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e1
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
        )
    )

    # --------------------------------------------------------
    # CASE 05 — TOOL MISMATCH
    # --------------------------------------------------------

    authorities["C05"] = authority(
        authority_id="AUTH_F17_C05",
        subject="AGENT_F17_EPSILON",
        action=F17_LOW_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=1,
    )

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C05-TOOL-MISMATCH"
            ),
            attempt_id=(
                "F17-C05-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_EPSILON"
            ),
            authority=(
                authorities["C05"]
            ),
            requested_action=(
                F17_LOW_ACTION
            ),
            presented_tool=(
                alternate_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e1
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
        )
    )

    # --------------------------------------------------------
    # CASE 06 — ACTION SCOPE MISMATCH
    # --------------------------------------------------------

    authorities["C06"] = authority(
        authority_id="AUTH_F17_C06",
        subject="AGENT_F17_ZETA",
        action=F17_LOW_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=1,
    )

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C06-SCOPE-MISMATCH"
            ),
            attempt_id=(
                "F17-C06-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_ZETA"
            ),
            authority=(
                authorities["C06"]
            ),
            requested_action=(
                F17_HIGH_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e1
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
            human_authority_required=True,
            human_authority_present=True,
        )
    )

    # --------------------------------------------------------
    # CASE 07 — PRECONSUMED REPLAY
    # --------------------------------------------------------

    authorities["C07"] = authority(
        authority_id="AUTH_F17_C07",
        subject="AGENT_F17_ETA",
        action=F17_LOW_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=1,
        consumed=True,
    )

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C07-CONSUMED-REPLAY"
            ),
            attempt_id=(
                "F17-C07-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_ETA"
            ),
            authority=(
                authorities["C07"]
            ),
            requested_action=(
                F17_LOW_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e1
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
        )
    )

    # --------------------------------------------------------
    # TRANSITION EPOCH 1 -> EPOCH 2
    # --------------------------------------------------------

    before, after = (
        source.transition_to(2)
    )

    transitions.append(
        {
            "transition":
                "EPOCH_1_TO_EPOCH_2",

            "before":
                asdict(before),

            "after":
                asdict(after),
        }
    )

    current = after

    resolver_a.synchronize(
        current
    )

    resolver_b.synchronize(
        current
    )

    peer_e2_withdrawn = (
        PeerStateView(
            epoch=2,
            state="WITHDRAWN",
            admissible=False,
        )
    )

    # --------------------------------------------------------
    # CASE 08 — STALE EPOCH
    # --------------------------------------------------------

    authorities["C08"] = authority(
        authority_id="AUTH_F17_C08",
        subject="AGENT_F17_THETA",
        action=F17_LOW_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=1,
    )

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C08-STALE-EPOCH"
            ),
            attempt_id=(
                "F17-C08-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_THETA"
            ),
            authority=(
                authorities["C08"]
            ),
            requested_action=(
                F17_LOW_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e2_withdrawn
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
        )
    )

    # --------------------------------------------------------
    # CASE 09 — HUMAN AUTHORITY ABSENT
    # --------------------------------------------------------

    authorities["C09"] = authority(
        authority_id="AUTH_F17_C09",
        subject="AGENT_F17_IOTA",
        action=F17_HIGH_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=2,
    )

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C09-HUMAN-AUTHORITY-ABSENT"
            ),
            attempt_id=(
                "F17-C09-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_IOTA"
            ),
            authority=(
                authorities["C09"]
            ),
            requested_action=(
                F17_HIGH_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e2_withdrawn
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
            human_authority_required=True,
            human_authority_present=False,
        )
    )

    # --------------------------------------------------------
    # CASE 10 — COMPROMISED AGENT SCOPE ESCALATION
    # --------------------------------------------------------

    authorities["C10"] = authority(
        authority_id="AUTH_F17_C10",
        subject="AGENT_F17_KAPPA",
        action=F17_LOW_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=2,
    )

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C10-COMPROMISED-ESCALATION"
            ),
            attempt_id=(
                "F17-C10-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_KAPPA"
            ),
            authority=(
                authorities["C10"]
            ),
            requested_action=(
                F17_HIGH_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e2_withdrawn
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
            compromised_agent=True,
        )
    )

    # --------------------------------------------------------
    # CASE 11 — DELEGATION AMPLIFICATION
    # --------------------------------------------------------

    authorities["C11"] = authority(
        authority_id="AUTH_F17_C11",
        subject="AGENT_F17_LAMBDA_CHILD",
        action=F17_HIGH_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=2,
    )

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C11-DELEGATION-AMPLIFICATION"
            ),
            attempt_id=(
                "F17-C11-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_LAMBDA_CHILD"
            ),
            authority=(
                authorities["C11"]
            ),
            requested_action=(
                F17_HIGH_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e2_withdrawn
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
            delegation_lineage_valid=True,
            delegation_parent_scope=(
                F17_LOW_ACTION
            ),
            human_authority_required=True,
            human_authority_present=True,
        )
    )

    # --------------------------------------------------------
    # CASE 12 — UNANIMOUS ADVISORY, NO AUTHORITY
    # --------------------------------------------------------

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C12-ADVISORY-MAJORITY"
            ),
            attempt_id=(
                "F17-C12-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_MU"
            ),
            authority=None,
            requested_action=(
                F17_LOW_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e2_withdrawn
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
            advisory_permit_votes=5,
            advisory_refuse_votes=0,
            advisory_result=(
                "UNANIMOUS_PERMIT"
            ),
        )
    )

    # --------------------------------------------------------
    # CASE 13 — STALE PEER STATE
    # --------------------------------------------------------

    authorities["C13"] = authority(
        authority_id="AUTH_F17_C13",
        subject="AGENT_F17_PEER",
        action=F17_LOW_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=2,
    )

    stale_peer = PeerStateView(
        epoch=1,
        state="READY",
        admissible=True,
    )

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C13-STALE-PEER-STATE"
            ),
            attempt_id=(
                "F17-C13-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_PEER"
            ),
            authority=(
                authorities["C13"]
            ),
            requested_action=(
                F17_LOW_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                stale_peer
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
        )
    )

    # --------------------------------------------------------
    # CASE 14 — RESOLVERS UNAVAILABLE, HISTORICAL CACHE EXISTS
    # --------------------------------------------------------

    authorities["C14"] = authority(
        authority_id="AUTH_F17_C14",
        subject="AGENT_F17_RESOLVER_UNAVAILABLE",
        action=F17_LOW_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=2,
    )

    resolver_a.unavailable()
    resolver_b.unavailable()

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C14-RESOLVER-UNAVAILABLE"
            ),
            attempt_id=(
                "F17-C14-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_RESOLVER_UNAVAILABLE"
            ),
            authority=(
                authorities["C14"]
            ),
            requested_action=(
                F17_LOW_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e2_withdrawn
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
            resolver_test_mode=True,
            execution_context_mode=(
                "RESOLVER_BOUNDARY"
            ),
        )
    )

    # --------------------------------------------------------
    # CASE 15A — RESOLVER CONFLICT
    # --------------------------------------------------------

    authorities["C15A"] = authority(
        authority_id="AUTH_F17_C15A",
        subject="AGENT_F17_RESOLVER_CONFLICT",
        action=F17_LOW_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=2,
    )

    resolver_a.force_view(
        epoch=1,
        state="READY",
        admissible=True,
    )

    resolver_b.force_view(
        epoch=2,
        state="WITHDRAWN",
        admissible=False,
    )

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C15-RESOLVER-DEGRADATION"
            ),
            attempt_id=(
                "F17-C15A-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_RESOLVER_CONFLICT"
            ),
            authority=(
                authorities["C15A"]
            ),
            requested_action=(
                F17_LOW_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e2_withdrawn
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
            resolver_test_mode=True,
            execution_context_mode=(
                "RESOLVER_BOUNDARY"
            ),
        )
    )

    # --------------------------------------------------------
    # CASE 15B — CURRENT CONSISTENT INADMISSIBLE
    # --------------------------------------------------------

    authorities["C15B"] = authority(
        authority_id="AUTH_F17_C15B",
        subject="AGENT_F17_RESOLVER_INADMISSIBLE",
        action=F17_LOW_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=2,
    )

    resolver_a.force_view(
        epoch=2,
        state="WITHDRAWN",
        admissible=False,
    )

    resolver_b.force_view(
        epoch=2,
        state="WITHDRAWN",
        admissible=False,
    )

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C15-RESOLVER-DEGRADATION"
            ),
            attempt_id=(
                "F17-C15B-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_RESOLVER_INADMISSIBLE"
            ),
            authority=(
                authorities["C15B"]
            ),
            requested_action=(
                F17_LOW_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e2_withdrawn
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
            resolver_test_mode=True,
            execution_context_mode=(
                "RESOLVER_BOUNDARY"
            ),
        )
    )

    # --------------------------------------------------------
    # CASE 16 — CONCURRENT SINGLE CONSUMPTION
    # --------------------------------------------------------

    authorities["C16"] = authority(
        authority_id="AUTH_F17_C16_SHARED",
        subject="AGENT_F17_NU",
        action=F17_LOW_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=2,
    )

    concurrency_peer = (
        PeerStateView(
            epoch=2,
            state="READY",
            admissible=True,
        )
    )

    resolver_a.force_view(
        epoch=2,
        state="READY",
        admissible=True,
    )

    resolver_b.force_view(
        epoch=2,
        state="READY",
        admissible=True,
    )

    barrier = threading.Barrier(2)

    def run_c16(
        attempt_id: str,
    ):

        return gate.attempt(
            case_id=(
                "F17-C16-CONCURRENT-SINGLE-CONSUMPTION"
            ),
            attempt_id=(
                attempt_id
            ),
            presenter_identity=(
                "AGENT_F17_NU"
            ),
            authority=(
                authorities["C16"]
            ),
            requested_action=(
                F17_LOW_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                concurrency_peer
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
            execution_context_mode=(
                "CONCURRENCY_ADMISSIBLE_CONTEXT"
            ),
            pre_consumption_barrier=(
                barrier
            ),
        )

    c16_completion = []

    with ThreadPoolExecutor(
        max_workers=2,
        thread_name_prefix="F17C16",
    ) as executor:

        futures = [
            executor.submit(
                run_c16,
                "F17-C16-ATTEMPT-A",
            ),
            executor.submit(
                run_c16,
                "F17-C16-ATTEMPT-B",
            ),
        ]

        for future in as_completed(
            futures
        ):

            c16_completion.append(
                future.result()
            )

    outcomes.extend(
        c16_completion
    )

    # --------------------------------------------------------
    # TRANSITION EPOCH 2 -> EPOCH 3
    # --------------------------------------------------------

    before, after = (
        source.transition_to(3)
    )

    transitions.append(
        {
            "transition":
                "EPOCH_2_TO_EPOCH_3",

            "before":
                asdict(before),

            "after":
                asdict(after),
        }
    )

    current = after

    resolver_a.synchronize(
        current
    )

    resolver_b.synchronize(
        current
    )

    peer_e3 = PeerStateView(
        epoch=3,
        state="READY",
        admissible=True,
    )

    # --------------------------------------------------------
    # CASE 17 — PROSPECTIVE RECOVERY
    # --------------------------------------------------------

    authorities["C17"] = authority(
        authority_id="AUTH_F17_C17",
        subject="AGENT_F17_XI",
        action=F17_LOW_ACTION,
        tool=F17_PRIMARY_TOOL,
        epoch=3,
    )

    outcomes.append(
        gate.attempt(
            case_id=(
                "F17-C17-PROSPECTIVE-RECOVERY"
            ),
            attempt_id=(
                "F17-C17-ATTEMPT"
            ),
            presenter_identity=(
                "AGENT_F17_XI"
            ),
            authority=(
                authorities["C17"]
            ),
            requested_action=(
                F17_LOW_ACTION
            ),
            presented_tool=(
                primary_tool
            ),
            authoritative_state=(
                current
            ),
            peer_state=(
                peer_e3
            ),
            resolver_a=(
                resolver_a.observe()
            ),
            resolver_b=(
                resolver_b.observe()
            ),
        )
    )

    # --------------------------------------------------------
    # CANONICAL EVIDENCE ORDER
    # --------------------------------------------------------

    ordered = sorted(
        outcomes,
        key=lambda item:
            item.decision.attempt_id,
    )

    decisions = [
        asdict(
            item.decision
        )
        for item in ordered
    ]

    witnesses = [
        asdict(
            item.witness
        )
        for item in ordered
    ]

    composite_pairs = [
        {
            "decision":
                asdict(
                    item.decision
                ),

            "witness":
                asdict(
                    item.witness
                ),
        }
        for item in ordered
    ]

    composite_digest = (
        sha256_hex(
            canonical_bytes(
                composite_pairs
            )
        )
    )

    # --------------------------------------------------------
    # AGGREGATE COUNTS
    # --------------------------------------------------------

    verdict_counts = Counter(
        item.decision.verdict
        for item in ordered
    )

    reason_counts = Counter(
        item.decision.reason
        for item in ordered
        if item.decision.verdict
        == "REFUSE"
    )

    permits = [
        item.decision
        for item in ordered
        if item.decision.verdict
        == "PERMIT"
    ]

    refusals = [
        item.decision
        for item in ordered
        if item.decision.verdict
        == "REFUSE"
    ]

    attempt_ids = [
        item.decision.attempt_id
        for item in ordered
    ]

    decision_ids = [
        item.decision.decision_id
        for item in ordered
    ]

    witness_ids = [
        item.witness.witness_id
        for item in ordered
    ]

    case_ids = {
        item.decision.case_id
        for item in ordered
    }

    decision_by_attempt = {
        item.decision.attempt_id:
            item.decision
        for item in ordered
    }

    witness_by_attempt = {
        item.witness.attempt_id:
            item.witness
        for item in ordered
    }

    # --------------------------------------------------------
    # EXACT SINGLE-ATTEMPT CASE CHECKS
    # --------------------------------------------------------

    exact_case_checks = {}

    for (
        attempt_id,
        expected,
    ) in EXPECTED_SINGLE_ATTEMPTS.items():

        decision = (
            decision_by_attempt.get(
                attempt_id
            )
        )

        exact_case_checks[
            f"{attempt_id}_present"
        ] = (
            decision is not None
        )

        if decision is not None:

            exact_case_checks[
                f"{attempt_id}_verdict"
            ] = (
                decision.verdict
                == expected[0]
            )

            exact_case_checks[
                f"{attempt_id}_reason"
            ] = (
                decision.reason
                == expected[1]
            )

            expected_delta = (
                1
                if expected[0]
                == "PERMIT"
                else 0
            )

            exact_case_checks[
                f"{attempt_id}_delta"
            ] = (
                decision.consequence_delta
                == expected_delta
            )

    # --------------------------------------------------------
    # CASE 16 AGGREGATE
    # --------------------------------------------------------

    c16_decisions = [
        item.decision
        for item in ordered
        if item.decision.case_id
        == "F17-C16-CONCURRENT-SINGLE-CONSUMPTION"
    ]

    c16_verdict_counts = Counter(
        item.verdict
        for item in c16_decisions
    )

    c16_refusal_reasons = Counter(
        item.reason
        for item in c16_decisions
        if item.verdict
        == "REFUSE"
    )

    c16_delta = sum(
        item.consequence_delta
        for item in c16_decisions
    )

    # --------------------------------------------------------
    # AUTHORITY STATE CHECKS
    # --------------------------------------------------------

    expected_consumed_true = {
        "C01",
        "C02",
        "C07",
        "C16",
        "C17",
    }

    expected_consumed_false = {
        "C04",
        "C05",
        "C06",
        "C08",
        "C09",
        "C10",
        "C11",
        "C13",
        "C14",
        "C15A",
        "C15B",
    }

    authority_state_checks = {}

    for key in expected_consumed_true:

        authority_state_checks[
            f"{key}_final_consumed_true"
        ] = (
            authorities[
                key
            ].consumed_snapshot()
            is True
        )

    for key in expected_consumed_false:

        authority_state_checks[
            f"{key}_final_consumed_false"
        ] = (
            authorities[
                key
            ].consumed_snapshot()
            is False
        )

    # --------------------------------------------------------
    # WITNESS CORRESPONDENCE
    # --------------------------------------------------------

    witness_correspondence = all(
        (
            witness_by_attempt[
                attempt_id
            ].decision_id
            ==
            decision_by_attempt[
                attempt_id
            ].decision_id
        )
        and
        (
            witness_by_attempt[
                attempt_id
            ].verdict
            ==
            decision_by_attempt[
                attempt_id
            ].verdict
        )
        and
        (
            witness_by_attempt[
                attempt_id
            ].reason
            ==
            decision_by_attempt[
                attempt_id
            ].reason
        )
        and
        (
            witness_by_attempt[
                attempt_id
            ].consequence_delta
            ==
            decision_by_attempt[
                attempt_id
            ].consequence_delta
        )
        for attempt_id
        in attempt_ids
    )

    # --------------------------------------------------------
    # SPECIAL COMPOSITE PROPERTY CHECKS
    # --------------------------------------------------------

    c03 = decision_by_attempt[
        "F17-C03-ATTEMPT"
    ]

    c06 = decision_by_attempt[
        "F17-C06-ATTEMPT"
    ]

    c10 = decision_by_attempt[
        "F17-C10-ATTEMPT"
    ]

    c11 = decision_by_attempt[
        "F17-C11-ATTEMPT"
    ]

    c12 = decision_by_attempt[
        "F17-C12-ATTEMPT"
    ]

    c14 = decision_by_attempt[
        "F17-C14-ATTEMPT"
    ]

    c15a = decision_by_attempt[
        "F17-C15A-ATTEMPT"
    ]

    c15b = decision_by_attempt[
        "F17-C15B-ATTEMPT"
    ]

    checks = {

        "case_count_17":
            len(
                case_ids
            ) == 17,

        "attempt_count_19":
            len(
                ordered
            ) == 19,

        "decision_count_19":
            len(
                decisions
            ) == 19,

        "witness_count_19":
            len(
                witnesses
            ) == 19,

        "permit_count_4":
            verdict_counts[
                "PERMIT"
            ] == 4,

        "refuse_count_15":
            verdict_counts[
                "REFUSE"
            ] == 15,

        "authorized_consequence_4":
            sum(
                item.consequence_delta
                for item in permits
            ) == 4,

        "unauthorized_consequence_zero":
            sum(
                item.consequence_delta
                for item in refusals
            ) == 0,

        "primary_tool_counter_4":
            primary_tool
            .consequence_counter
            == 4,

        "alternate_tool_counter_zero":
            alternate_tool
            .consequence_counter
            == 0,

        "unique_attempt_ids_19":
            len(
                set(
                    attempt_ids
                )
            ) == 19,

        "unique_decision_ids_19":
            len(
                set(
                    decision_ids
                )
            ) == 19,

        "unique_witness_ids_19":
            len(
                set(
                    witness_ids
                )
            ) == 19,

        "witness_correspondence_exact":
            witness_correspondence,

        "reason_counts_exact":
            dict(
                sorted(
                    reason_counts.items()
                )
            )
            ==
            dict(
                sorted(
                    EXPECTED_REASON_COUNTS.items()
                )
            ),

        "case16_two_attempts":
            len(
                c16_decisions
            ) == 2,

        "case16_one_permit":
            c16_verdict_counts[
                "PERMIT"
            ] == 1,

        "case16_one_refuse":
            c16_verdict_counts[
                "REFUSE"
            ] == 1,

        "case16_refusal_reason_exact":
            c16_refusal_reasons[
                "EXECUTION_AUTHORITY_ALREADY_CONSUMED"
            ] == 1,

        "case16_delta_exact":
            c16_delta == 1,

        "case16_shared_authority_consumed":
            authorities[
                "C16"
            ].consumed_snapshot()
            is True,

        "advisory_case03_did_not_create_authority":
            (
                c03.authority_present
                is False
                and c03.verdict
                == "REFUSE"
            ),

        "advisory_case12_did_not_create_authority":
            (
                c12.authority_present
                is False
                and c12.advisory_permit_votes
                == 5
                and c12.advisory_refuse_votes
                == 0
                and c12.verdict
                == "REFUSE"
            ),

        "human_approval_did_not_expand_scope":
            (
                c06.human_authority_present
                is True
                and c06.reason
                == "EXECUTION_SCOPE_NOT_AUTHORIZED"
            ),

        "compromise_did_not_expand_scope":
            (
                c10.compromised_agent
                is True
                and c10.reason
                == "EXECUTION_SCOPE_NOT_AUTHORIZED"
            ),

        "delegation_did_not_expand_scope":
            (
                c11.delegation_parent_scope
                == F17_LOW_ACTION
                and c11.requested_action
                == F17_HIGH_ACTION
                and c11.reason
                == "DELEGATION_SCOPE_AMPLIFICATION"
            ),

        "resolver_unavailable_mode_preserved":
            (
                c14.resolver_test_mode
                is True
                and c14.reason
                == "CURRENT_RESOLUTION_UNAVAILABLE"
            ),

        "resolver_conflict_mode_preserved":
            (
                c15a.resolver_test_mode
                is True
                and c15a.reason
                == "RESOLVER_STATE_CONFLICT"
            ),

        "resolver_inadmissible_mode_preserved":
            (
                c15b.resolver_test_mode
                is True
                and c15b.reason
                == "RESOLVED_STATE_NOT_ADMISSIBLE"
            ),

        "canonical_digest_present":
            len(
                composite_digest
            ) == 64,

        "transition_count_2":
            len(
                transitions
            ) == 2,

        "transition_1_to_2_exact":
            (
                transitions[0][
                    "before"
                ][
                    "epoch"
                ] == 1
                and
                transitions[0][
                    "after"
                ][
                    "epoch"
                ] == 2
            ),

        "transition_2_to_3_exact":
            (
                transitions[1][
                    "before"
                ][
                    "epoch"
                ] == 2
                and
                transitions[1][
                    "after"
                ][
                    "epoch"
                ] == 3
            ),
    }

    checks.update(
        exact_case_checks
    )

    checks.update(
        authority_state_checks
    )

    overall_pass = all(
        checks.values()
    )

    # --------------------------------------------------------
    # PRESERVE EVIDENCE
    # --------------------------------------------------------

    transitions_evidence = {
        "examination":
            "EASA-F17",

        "property":
            "COMPOSITE_ADVERSARIAL_MULTI_AGENT_BOUNDARY_PRESERVATION",

        "transitions":
            transitions,
    }

    composite_evidence = {
        "examination":
            "EASA-F17",

        "canonical_order":
            "ATTEMPT_ID_ASCENDING",

        "canonical_encoding":
            "UTF-8",

        "canonical_bom":
            "ABSENT",

        "canonical_json_key_order":
            "SORTED",

        "canonical_json_separators":
            "COMPACT",

        "canonical_composite_digest_sha256":
            composite_digest,

        "decisions":
            decisions,

        "witnesses":
            witnesses,
    }

    summary_without_digest = {
        "examination":
            "EASA-F17",

        "property":
            "COMPOSITE_ADVERSARIAL_MULTI_AGENT_BOUNDARY_PRESERVATION",

        "case_count":
            len(
                case_ids
            ),

        "attempt_count":
            len(
                ordered
            ),

        "decision_count":
            len(
                decisions
            ),

        "witness_count":
            len(
                witnesses
            ),

        "permit_count":
            verdict_counts[
                "PERMIT"
            ],

        "refuse_count":
            verdict_counts[
                "REFUSE"
            ],

        "authorized_consequence_total":
            sum(
                item.consequence_delta
                for item in permits
            ),

        "unauthorized_consequence_total":
            sum(
                item.consequence_delta
                for item in refusals
            ),

        "primary_tool_final_counter":
            primary_tool
            .consequence_counter,

        "alternate_tool_final_counter":
            alternate_tool
            .consequence_counter,

        "refusal_reason_counts":
            dict(
                sorted(
                    reason_counts.items()
                )
            ),

        "case16_permit_count":
            c16_verdict_counts[
                "PERMIT"
            ],

        "case16_refuse_count":
            c16_verdict_counts[
                "REFUSE"
            ],

        "case16_consequence_delta":
            c16_delta,

        "case16_shared_authority_consumed":
            authorities[
                "C16"
            ].consumed_snapshot(),

        "unique_attempt_id_count":
            len(
                set(
                    attempt_ids
                )
            ),

        "unique_decision_id_count":
            len(
                set(
                    decision_ids
                )
            ),

        "unique_witness_id_count":
            len(
                set(
                    witness_ids
                )
            ),

        "canonical_composite_digest_sha256":
            composite_digest,

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
                "OBSERVATION_SUPPORTS_DEFINED_COMPOSITE_PROPERTY"
                if overall_pass
                else
                "DEFINED_COMPOSITE_PROPERTY_NOT_ESTABLISHED_BY_FIRST_OBSERVATION"
            ),
    }

    summary_digest = (
        sha256_hex(
            canonical_bytes(
                summary_without_digest
            )
        )
    )

    summary = dict(
        summary_without_digest
    )

    summary[
        "canonical_summary_digest_sha256"
    ] = summary_digest

    write_json(
        TRANSITIONS_PATH,
        transitions_evidence,
    )

    write_json(
        COMPOSITE_PATH,
        composite_evidence,
    )

    write_json(
        SUMMARY_PATH,
        summary,
    )

    # --------------------------------------------------------
    # CONSOLE
    # --------------------------------------------------------

    print(
        "=== EASA-F17 FIRST OBSERVATION ==="
    )

    for item in ordered:

        print(
            "{attempt} | {verdict} | {reason} | DELTA={delta}".format(
                attempt=(
                    item.decision.attempt_id
                ),
                verdict=(
                    item.decision.verdict
                ),
                reason=(
                    item.decision.reason
                ),
                delta=(
                    item.decision.consequence_delta
                ),
            )
        )

    print(
        f"CASE_COUNT={summary['case_count']}"
    )

    print(
        f"ATTEMPT_COUNT={summary['attempt_count']}"
    )

    print(
        f"DECISION_COUNT={summary['decision_count']}"
    )

    print(
        f"WITNESS_COUNT={summary['witness_count']}"
    )

    print(
        f"PERMIT_COUNT={summary['permit_count']}"
    )

    print(
        f"REFUSE_COUNT={summary['refuse_count']}"
    )

    print(
        "UNAUTHORIZED_CONSEQUENCE_TOTAL="
        f"{summary['unauthorized_consequence_total']}"
    )

    print(
        "PRIMARY_TOOL_FINAL_COUNTER="
        f"{summary['primary_tool_final_counter']}"
    )

    print(
        "ALTERNATE_TOOL_FINAL_COUNTER="
        f"{summary['alternate_tool_final_counter']}"
    )

    print(
        "CASE16_PERMIT_REFUSE="
        f"{summary['case16_permit_count']}"
        "/"
        f"{summary['case16_refuse_count']}"
    )

    print(
        "COMPOSITE_DIGEST_SHA256="
        f"{summary['canonical_composite_digest_sha256']}"
    )

    print(
        "SUMMARY_DIGEST_SHA256="
        f"{summary['canonical_summary_digest_sha256']}"
    )

    print(
        f"OVERALL_RESULT="
        f"{summary['overall_result']}"
    )

    print(
        f"CLAIM_STATE="
        f"{summary['claim_state']}"
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