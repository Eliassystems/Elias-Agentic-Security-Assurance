from __future__ import annotations

from dataclasses import dataclass, field
from typing import FrozenSet


F10_ACTION = "F10_PRIVILEGED_WRITE"

TOOL_PEER = "TOOL_F10_PEER"
TOOL_LOW = "TOOL_F10_LOW"
TOOL_HIGH = "TOOL_F10_HIGH"


@dataclass
class GovernanceState:
    current_epoch: int
    revoked_epochs: set[int] = field(default_factory=set)


@dataclass
class ExecutionAuthority:
    authority_id: str
    subject_identity: str
    authority_epoch: int
    bound_tool_identity: str
    authorized_actions: FrozenSet[str]
    valid: bool = True
    consumed: bool = False


@dataclass(frozen=True)
class GateResult:
    presenter_identity: str
    authority_id: str
    authority_subject_identity: str
    authority_epoch: int
    authority_tool_identity: str
    target_tool_identity: str
    action: str
    governing_current_epoch: int
    authority_epoch_revoked: bool
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

        if action != F10_ACTION:
            raise ValueError("UNSUPPORTED_TOOL_ACTION")

        self.consequence_counter += 1


class ContainmentExecutionGate:
    """
    Bounded EASA-F10 execution boundary.

    Refused attempts do not mutate authority state.

    Successful execution consumes the supplied authority only after all
    identity, scope, tool and epoch conditions have passed.
    """

    def attempt(
        self,
        *,
        governance: GovernanceState,
        authority: ExecutionAuthority,
        presenter_identity: str,
        action: str,
        target_tool: ConsequentialTool,
    ) -> GateResult:

        consumed_before = authority.consumed
        consequence_before = target_tool.consequence_counter

        def refuse(reason: str) -> GateResult:

            consequence_after = target_tool.consequence_counter

            return GateResult(
                presenter_identity=presenter_identity,
                authority_id=authority.authority_id,
                authority_subject_identity=authority.subject_identity,
                authority_epoch=authority.authority_epoch,
                authority_tool_identity=authority.bound_tool_identity,
                target_tool_identity=target_tool.tool_identity,
                action=action,
                governing_current_epoch=governance.current_epoch,
                authority_epoch_revoked=(
                    authority.authority_epoch
                    in governance.revoked_epochs
                ),
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

        if authority.authority_epoch in governance.revoked_epochs:
            return refuse("AUTHORITY_EPOCH_REVOKED")

        if authority.authority_epoch != governance.current_epoch:
            return refuse("AUTHORITY_EPOCH_NOT_CURRENT")

        if action != F10_ACTION:
            return refuse("ACTION_NOT_SUPPORTED")

        target_tool.execute(action)
        authority.consumed = True

        consequence_after = target_tool.consequence_counter

        return GateResult(
            presenter_identity=presenter_identity,
            authority_id=authority.authority_id,
            authority_subject_identity=authority.subject_identity,
            authority_epoch=authority.authority_epoch,
            authority_tool_identity=authority.bound_tool_identity,
            target_tool_identity=target_tool.tool_identity,
            action=action,
            governing_current_epoch=governance.current_epoch,
            authority_epoch_revoked=False,
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