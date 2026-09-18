from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Optional

from easa_f17_state import (
    GoverningState,
    PeerStateView,
    ResolverView,
)


F17_PRIMARY_TOOL = "TOOL_F17_PRIMARY"

F17_OTHER_TOOL = "TOOL_F17_OTHER"

F17_LOW_ACTION = "F17_LOW_IMPACT_WRITE"

F17_HIGH_ACTION = "F17_HIGH_IMPACT_WRITE"


@dataclass
class ExecutionAuthority:
    authority_id: str
    subject_identity: str
    authorized_action: str
    authorized_tool_identity: str
    authority_epoch: int
    valid: bool = True
    consumed: bool = False

    def __post_init__(self) -> None:
        self._lock = threading.RLock()

    def consumed_snapshot(self) -> bool:
        with self._lock:
            return self.consumed


class ConsequentialTool:

    def __init__(
        self,
        tool_identity: str,
    ) -> None:

        if tool_identity not in {
            F17_PRIMARY_TOOL,
            F17_OTHER_TOOL,
        }:
            raise ValueError(
                "F17_TOOL_IDENTITY_NOT_FROZEN"
            )

        self.tool_identity = (
            tool_identity
        )

        self._counter = 0

        self._lock = (
            threading.Lock()
        )

    @property
    def consequence_counter(
        self,
    ) -> int:

        with self._lock:
            return self._counter

    def execute(
        self,
        action: str,
    ) -> tuple[int, int]:

        if action not in {
            F17_LOW_ACTION,
            F17_HIGH_ACTION,
        }:
            raise RuntimeError(
                "F17_ACTION_NOT_SUPPORTED"
            )

        with self._lock:

            before = self._counter

            self._counter += 1

            after = self._counter

            return before, after


@dataclass(frozen=True)
class ExecutionDecision:

    case_id: str
    attempt_id: str
    decision_id: str

    presenter_identity: str

    authority_present: bool
    authority_id: Optional[str]
    authority_subject_identity: Optional[str]
    authority_valid: Optional[bool]
    authority_epoch: Optional[int]
    authority_consumed_before: Optional[bool]
    authority_consumed_after: Optional[bool]

    authorized_action: Optional[str]
    authorized_tool_identity: Optional[str]

    requested_action: str
    presented_tool_identity: str

    compromised_agent: bool

    delegation_lineage_valid: bool
    delegation_parent_scope: Optional[str]

    human_authority_required: bool
    human_authority_present: bool

    advisory_permit_votes: int
    advisory_refuse_votes: int
    advisory_result: str

    authoritative_epoch: int
    authoritative_state: str
    authoritative_admissible: bool

    peer_epoch: int
    peer_state: str
    peer_admissible: bool

    resolver_a_available: bool
    resolver_a_epoch: Optional[int]
    resolver_a_state: Optional[str]
    resolver_a_admissible: Optional[bool]

    resolver_b_available: bool
    resolver_b_epoch: Optional[int]
    resolver_b_state: Optional[str]
    resolver_b_admissible: Optional[bool]

    resolver_test_mode: bool
    execution_context_mode: str

    verdict: str
    reason: str

    consequence_before: int
    consequence_after: int
    consequence_delta: int

    worker_thread_identity: str


@dataclass(frozen=True)
class WitnessRecord:

    witness_id: str
    decision_id: str
    case_id: str
    attempt_id: str
    presenter_identity: str
    authority_id: Optional[str]
    verdict: str
    reason: str
    presented_tool_identity: str
    consequence_delta: int
    governing_epoch: int


@dataclass(frozen=True)
class AttemptOutcome:
    decision: ExecutionDecision
    witness: WitnessRecord


class F17CompositeExecutionGate:

    def _witness(
        self,
        decision: ExecutionDecision,
    ) -> WitnessRecord:

        return WitnessRecord(
            witness_id=(
                f"WITNESS::{decision.attempt_id}"
            ),
            decision_id=(
                decision.decision_id
            ),
            case_id=(
                decision.case_id
            ),
            attempt_id=(
                decision.attempt_id
            ),
            presenter_identity=(
                decision.presenter_identity
            ),
            authority_id=(
                decision.authority_id
            ),
            verdict=(
                decision.verdict
            ),
            reason=(
                decision.reason
            ),
            presented_tool_identity=(
                decision.presented_tool_identity
            ),
            consequence_delta=(
                decision.consequence_delta
            ),
            governing_epoch=(
                decision.authoritative_epoch
            ),
        )

    def attempt(
        self,
        *,
        case_id: str,
        attempt_id: str,
        presenter_identity: str,
        authority: Optional[ExecutionAuthority],
        requested_action: str,
        presented_tool: ConsequentialTool,
        authoritative_state: GoverningState,
        peer_state: PeerStateView,
        resolver_a: ResolverView,
        resolver_b: ResolverView,
        compromised_agent: bool = False,
        delegation_lineage_valid: bool = True,
        delegation_parent_scope: Optional[str] = None,
        human_authority_required: bool = False,
        human_authority_present: bool = False,
        advisory_permit_votes: int = 0,
        advisory_refuse_votes: int = 0,
        advisory_result: str = "NONE",
        resolver_test_mode: bool = False,
        execution_context_mode: str = "STANDARD",
        pre_consumption_barrier: Optional[
            threading.Barrier
        ] = None,
    ) -> AttemptOutcome:

        worker_identity = (
            f"{threading.current_thread().name}:"
            f"{threading.get_ident()}"
        )

        decision_id = (
            f"DECISION::{attempt_id}"
        )

        def build_decision(
            *,
            verdict: str,
            reason: str,
            consequence_before: int,
            consequence_after: int,
            consumed_before_override: Optional[
                bool
            ] = None,
        ) -> ExecutionDecision:

            if authority is None:

                consumed_before = None
                consumed_after = None

                authority_id = None
                subject_identity = None
                authority_valid = None
                authority_epoch = None
                authorized_action = None
                authorized_tool_identity = None

            else:

                authority_id = (
                    authority.authority_id
                )

                subject_identity = (
                    authority.subject_identity
                )

                authority_valid = (
                    authority.valid
                )

                authority_epoch = (
                    authority.authority_epoch
                )

                authorized_action = (
                    authority.authorized_action
                )

                authorized_tool_identity = (
                    authority
                    .authorized_tool_identity
                )

                if (
                    consumed_before_override
                    is not None
                ):

                    consumed_before = (
                        consumed_before_override
                    )

                else:

                    consumed_before = (
                        authority
                        .consumed_snapshot()
                    )

                consumed_after = (
                    authority
                    .consumed_snapshot()
                )

            return ExecutionDecision(
                case_id=case_id,
                attempt_id=attempt_id,
                decision_id=decision_id,
                presenter_identity=(
                    presenter_identity
                ),
                authority_present=(
                    authority is not None
                ),
                authority_id=(
                    authority_id
                ),
                authority_subject_identity=(
                    subject_identity
                ),
                authority_valid=(
                    authority_valid
                ),
                authority_epoch=(
                    authority_epoch
                ),
                authority_consumed_before=(
                    consumed_before
                ),
                authority_consumed_after=(
                    consumed_after
                ),
                authorized_action=(
                    authorized_action
                ),
                authorized_tool_identity=(
                    authorized_tool_identity
                ),
                requested_action=(
                    requested_action
                ),
                presented_tool_identity=(
                    presented_tool.tool_identity
                ),
                compromised_agent=(
                    compromised_agent
                ),
                delegation_lineage_valid=(
                    delegation_lineage_valid
                ),
                delegation_parent_scope=(
                    delegation_parent_scope
                ),
                human_authority_required=(
                    human_authority_required
                ),
                human_authority_present=(
                    human_authority_present
                ),
                advisory_permit_votes=(
                    advisory_permit_votes
                ),
                advisory_refuse_votes=(
                    advisory_refuse_votes
                ),
                advisory_result=(
                    advisory_result
                ),
                authoritative_epoch=(
                    authoritative_state.epoch
                ),
                authoritative_state=(
                    authoritative_state.state
                ),
                authoritative_admissible=(
                    authoritative_state.admissible
                ),
                peer_epoch=(
                    peer_state.epoch
                ),
                peer_state=(
                    peer_state.state
                ),
                peer_admissible=(
                    peer_state.admissible
                ),
                resolver_a_available=(
                    resolver_a.available
                ),
                resolver_a_epoch=(
                    resolver_a.epoch
                ),
                resolver_a_state=(
                    resolver_a.state
                ),
                resolver_a_admissible=(
                    resolver_a.admissible
                ),
                resolver_b_available=(
                    resolver_b.available
                ),
                resolver_b_epoch=(
                    resolver_b.epoch
                ),
                resolver_b_state=(
                    resolver_b.state
                ),
                resolver_b_admissible=(
                    resolver_b.admissible
                ),
                resolver_test_mode=(
                    resolver_test_mode
                ),
                execution_context_mode=(
                    execution_context_mode
                ),
                verdict=verdict,
                reason=reason,
                consequence_before=(
                    consequence_before
                ),
                consequence_after=(
                    consequence_after
                ),
                consequence_delta=(
                    consequence_after
                    - consequence_before
                ),
                worker_thread_identity=(
                    worker_identity
                ),
            )

        def refuse(
            reason: str,
            *,
            consumed_before_override: Optional[
                bool
            ] = None,
        ) -> AttemptOutcome:

            before = (
                presented_tool
                .consequence_counter
            )

            decision = build_decision(
                verdict="REFUSE",
                reason=reason,
                consequence_before=before,
                consequence_after=before,
                consumed_before_override=(
                    consumed_before_override
                ),
            )

            return AttemptOutcome(
                decision=decision,
                witness=self._witness(
                    decision
                ),
            )

        # 1. Authority presence
        if authority is None:

            return refuse(
                "EXECUTION_AUTHORITY_NOT_PRESENT"
            )

        # 2. Authority validity
        if authority.valid is not True:

            return refuse(
                "EXECUTION_AUTHORITY_INVALID"
            )

        # Frozen synchronization point for CASE-16.
        # This is not an authority-producing operation.
        if pre_consumption_barrier is not None:

            pre_consumption_barrier.wait()

        # 3. Prior authority consumption
        if authority.consumed_snapshot():

            return refuse(
                "EXECUTION_AUTHORITY_ALREADY_CONSUMED",
                consumed_before_override=True,
            )

        # 4. Presenter identity binding
        if (
            presenter_identity
            != authority.subject_identity
        ):

            return refuse(
                "PRESENTER_IDENTITY_MISMATCH"
            )

        # 5. Requested-action scope binding
        if (
            requested_action
            != authority.authorized_action
        ):

            return refuse(
                "EXECUTION_SCOPE_NOT_AUTHORIZED"
            )

        # 6. Presented-tool binding
        if (
            presented_tool.tool_identity
            != authority.authorized_tool_identity
        ):

            return refuse(
                "TOOL_IDENTITY_MISMATCH"
            )

        # 7. Authority epoch correspondence
        if (
            authority.authority_epoch
            != authoritative_state.epoch
        ):

            return refuse(
                "EXECUTION_AUTHORITY_EPOCH_CHANGED"
            )

        # 8. Compromised-agent privilege ceiling.
        # CASE-10 is prospectively expected to fail earlier
        # at scope binding. This branch exists for composite
        # integrity if a compromised agent otherwise reaches
        # the privilege ceiling.
        if (
            compromised_agent
            and requested_action
            == F17_HIGH_ACTION
            and authority.authorized_action
            == F17_HIGH_ACTION
            and delegation_parent_scope
            is None
        ):

            return refuse(
                "COMPROMISED_AGENT_PRIVILEGE_ESCALATION"
            )

        # 9. Delegation scope / lineage ceiling
        if delegation_parent_scope is not None:

            if delegation_lineage_valid is not True:

                return refuse(
                    "DELEGATION_LINEAGE_INVALID"
                )

            if (
                requested_action
                != delegation_parent_scope
            ):

                return refuse(
                    "DELEGATION_SCOPE_AMPLIFICATION"
                )

        # 10. Required human authority
        if (
            human_authority_required
            and human_authority_present
            is not True
        ):

            return refuse(
                "HUMAN_AUTHORITY_REQUIRED"
            )

        # 11. Peer-state freshness
        if (
            peer_state.epoch
            != authoritative_state.epoch
        ):

            return refuse(
                "PEER_STATE_STALE"
            )

        # 12. Peer-state admissibility
        #
        # Resolver-test mode is prospectively frozen for the
        # resolver-focused C14/C15 cases so an inadmissible
        # peer view does not mask the resolver property.
        if (
            not resolver_test_mode
            and peer_state.admissible
            is not True
        ):

            return refuse(
                "PEER_STATE_NOT_ADMISSIBLE"
            )

        # 13. Resolver availability
        if (
            resolver_a.available
            is not True
            or resolver_b.available
            is not True
        ):

            return refuse(
                "CURRENT_RESOLUTION_UNAVAILABLE"
            )

        # 14. Resolver consistency
        resolver_a_tuple = (
            resolver_a.epoch,
            resolver_a.state,
            resolver_a.admissible,
        )

        resolver_b_tuple = (
            resolver_b.epoch,
            resolver_b.state,
            resolver_b.admissible,
        )

        if (
            resolver_a_tuple
            != resolver_b_tuple
        ):

            return refuse(
                "RESOLVER_STATE_CONFLICT"
            )

        # 15. Resolver correspondence to current authority epoch.
        #
        # In F17, currentness is operationalized as epoch
        # correspondence. State/admissibility is separately
        # governed by the consistency and admissibility checks.
        if (
            resolver_a.epoch
            != authoritative_state.epoch
            or resolver_b.epoch
            != authoritative_state.epoch
        ):

            return refuse(
                "RESOLVER_STATE_NOT_CURRENT"
            )

        # 16. Resolver admissibility
        if (
            resolver_a.admissible
            is not True
            or resolver_b.admissible
            is not True
        ):

            return refuse(
                "RESOLVED_STATE_NOT_ADMISSIBLE"
            )

        # 17. Consequential execution.
        #
        # Consumption + consequence are serialized under the
        # authority lock so one single-use authority cannot
        # commit twice inside the frozen same-process model.
        with authority._lock:

            if authority.consumed:

                return refuse(
                    "EXECUTION_AUTHORITY_ALREADY_CONSUMED",
                    consumed_before_override=True,
                )

            before, after = (
                presented_tool.execute(
                    requested_action
                )
            )

            authority.consumed = True

            decision = build_decision(
                verdict="PERMIT",
                reason="AUTHORIZED",
                consequence_before=before,
                consequence_after=after,
                consumed_before_override=False,
            )

        return AttemptOutcome(
            decision=decision,
            witness=self._witness(
                decision
            ),
        )