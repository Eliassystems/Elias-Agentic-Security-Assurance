from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet


EPOCH_ACTION = "EPOCH_BOUND_PRIVILEGED_WRITE"
REVOCATION_EVENT_ID = "REV_F09_E1_TO_E2"


@dataclass(frozen=True)
class RevocationEvent:
    event_id: str
    prior_epoch: int
    new_epoch: int
    revoked_epoch: int


@dataclass(frozen=True)
class AuthorityChangeResult:
    event_id: str
    prior_authoritative_epoch: int
    resulting_authoritative_epoch: int
    revoked_epoch: int
    revoked_epochs_after: tuple[int, ...]


class AuthoritativeEpochSource:

    def __init__(self, *, current_epoch: int) -> None:
        self.current_epoch = current_epoch
        self.revoked_epochs: set[int] = set()

    def apply_event(
        self,
        event: RevocationEvent,
    ) -> AuthorityChangeResult:

        prior = self.current_epoch

        if event.prior_epoch != prior:
            raise ValueError("AUTHORITATIVE_PRIOR_EPOCH_MISMATCH")

        if event.new_epoch <= event.prior_epoch:
            raise ValueError("AUTHORITATIVE_EPOCH_NOT_ADVANCED")

        if event.revoked_epoch != event.prior_epoch:
            raise ValueError("REVOKED_EPOCH_DOES_NOT_MATCH_PRIOR_EPOCH")

        self.current_epoch = event.new_epoch
        self.revoked_epochs.add(event.revoked_epoch)

        return AuthorityChangeResult(
            event_id=event.event_id,
            prior_authoritative_epoch=prior,
            resulting_authoritative_epoch=self.current_epoch,
            revoked_epoch=event.revoked_epoch,
            revoked_epochs_after=tuple(
                sorted(self.revoked_epochs)
            ),
        )


@dataclass
class LocalNodeState:
    node_id: str
    current_epoch: int
    revoked_epochs: set[int] = field(default_factory=set)
    last_applied_revocation_event: str | None = None


@dataclass
class EpochBoundAuthority:
    authority_id: str
    subject_identity: str
    bound_tool_identity: str
    authorized_actions: FrozenSet[str]
    authority_epoch: int
    valid: bool = True
    consumed: bool = False


@dataclass(frozen=True)
class GateResult:
    node_id: str
    presenter_identity: str
    authority_id: str
    authority_epoch: int
    local_current_epoch: int
    local_epoch_revoked: bool
    target_tool_identity: str
    action: str
    verdict: str
    reason: str
    authority_consumed_before: bool
    authority_consumed_after: bool
    consequence_before: int
    consequence_after: int
    consequence_delta: int


class ConsequentialTool:

    def __init__(self, tool_identity: str) -> None:
        self.tool_identity = tool_identity
        self.consequence_counter = 0

    def execute(self, action: str) -> None:

        if action != EPOCH_ACTION:
            raise ValueError("UNSUPPORTED_TOOL_ACTION")

        self.consequence_counter += 1


class EpochExecutionGate:
    """
    EASA-F09 local execution boundary.

    The gate consumes local propagated epoch/revocation state.
    It does not query the authoritative source during execution.
    """

    def attempt(
        self,
        *,
        node_state: LocalNodeState,
        authority: EpochBoundAuthority,
        presenter_identity: str,
        action: str,
        target_tool: ConsequentialTool,
    ) -> GateResult:

        consumed_before = authority.consumed
        consequence_before = target_tool.consequence_counter

        def refuse(reason: str) -> GateResult:

            consequence_after = target_tool.consequence_counter

            return GateResult(
                node_id=node_state.node_id,
                presenter_identity=presenter_identity,
                authority_id=authority.authority_id,
                authority_epoch=authority.authority_epoch,
                local_current_epoch=node_state.current_epoch,
                local_epoch_revoked=(
                    authority.authority_epoch
                    in node_state.revoked_epochs
                ),
                target_tool_identity=target_tool.tool_identity,
                action=action,
                verdict="REFUSE",
                reason=reason,
                authority_consumed_before=consumed_before,
                authority_consumed_after=authority.consumed,
                consequence_before=consequence_before,
                consequence_after=consequence_after,
                consequence_delta=(
                    consequence_after - consequence_before
                ),
            )

        if not authority.valid:
            return refuse("EXECUTION_AUTHORITY_INVALID")

        if authority.consumed:
            return refuse("EXECUTION_AUTHORITY_ALREADY_CONSUMED")

        if presenter_identity != authority.subject_identity:
            return refuse("PRESENTER_IDENTITY_MISMATCH")

        if action not in authority.authorized_actions:
            return refuse("EXECUTION_SCOPE_NOT_AUTHORIZED")

        if target_tool.tool_identity != authority.bound_tool_identity:
            return refuse("TOOL_IDENTITY_MISMATCH")

        # F09 governing property:
        # explicit revocation takes precedence.
        if authority.authority_epoch in node_state.revoked_epochs:
            return refuse("AUTHORITY_EPOCH_REVOKED")

        if authority.authority_epoch != node_state.current_epoch:
            return refuse("AUTHORITY_EPOCH_NOT_CURRENT")

        if action != EPOCH_ACTION:
            return refuse("ACTION_NOT_SUPPORTED")

        target_tool.execute(action)
        authority.consumed = True

        consequence_after = target_tool.consequence_counter

        return GateResult(
            node_id=node_state.node_id,
            presenter_identity=presenter_identity,
            authority_id=authority.authority_id,
            authority_epoch=authority.authority_epoch,
            local_current_epoch=node_state.current_epoch,
            local_epoch_revoked=False,
            target_tool_identity=target_tool.tool_identity,
            action=action,
            verdict="PERMIT",
            reason="AUTHORIZED",
            authority_consumed_before=consumed_before,
            authority_consumed_after=authority.consumed,
            consequence_before=consequence_before,
            consequence_after=consequence_after,
            consequence_delta=(
                consequence_after - consequence_before
            ),
        )