from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet


SHARED_ACTION = "SHARED_PRIVILEGED_WRITE"


@dataclass
class ExecutionAuthority:
    authority_id: str
    subject_identity: str
    bound_tool_identity: str
    authorized_actions: FrozenSet[str]
    valid: bool = True
    consumed: bool = False
    governing_state_valid: bool = True


@dataclass(frozen=True)
class GateResult:
    verdict: str
    reason: str
    authority_id: str
    subject_identity: str
    presenter_identity: str
    authority_tool_identity: str
    target_tool_identity: str
    action: str
    authority_consumed_before: bool
    authority_consumed_after: bool
    target_consequence_before: int
    target_consequence_after: int
    target_consequence_delta: int


class ConsequentialTool:

    def __init__(self, tool_identity: str) -> None:
        self.tool_identity = tool_identity
        self.consequence_counter = 0

    def execute(self, action: str) -> None:

        if action != SHARED_ACTION:
            raise ValueError("UNSUPPORTED_TOOL_ACTION")

        self.consequence_counter += 1


class ToolBoundExecutionGate:
    """
    EASA-F07 execution gate.

    Valid authority for one tool does not transfer to another tool merely
    because the presenter and action are otherwise valid.
    """

    def attempt(
        self,
        *,
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
                verdict="REFUSE",
                reason=reason,
                authority_id=authority.authority_id,
                subject_identity=authority.subject_identity,
                presenter_identity=presenter_identity,
                authority_tool_identity=authority.bound_tool_identity,
                target_tool_identity=target_tool.tool_identity,
                action=action,
                authority_consumed_before=consumed_before,
                authority_consumed_after=authority.consumed,
                target_consequence_before=consequence_before,
                target_consequence_after=consequence_after,
                target_consequence_delta=(
                    consequence_after - consequence_before
                ),
            )

        if not authority.valid:
            return refuse("EXECUTION_AUTHORITY_INVALID")

        if authority.consumed:
            return refuse("EXECUTION_AUTHORITY_ALREADY_CONSUMED")

        if not authority.governing_state_valid:
            return refuse("GOVERNING_STATE_INVALID")

        if action not in authority.authorized_actions:
            return refuse("EXECUTION_SCOPE_NOT_AUTHORIZED")

        if presenter_identity != authority.subject_identity:
            return refuse("PRESENTER_IDENTITY_MISMATCH")

        # F07 property under examination.
        if target_tool.tool_identity != authority.bound_tool_identity:
            return refuse("TOOL_IDENTITY_MISMATCH")

        if action != SHARED_ACTION:
            return refuse("ACTION_NOT_SUPPORTED")

        target_tool.execute(action)
        authority.consumed = True

        consequence_after = target_tool.consequence_counter

        return GateResult(
            verdict="PERMIT",
            reason="AUTHORIZED",
            authority_id=authority.authority_id,
            subject_identity=authority.subject_identity,
            presenter_identity=presenter_identity,
            authority_tool_identity=authority.bound_tool_identity,
            target_tool_identity=target_tool.tool_identity,
            action=action,
            authority_consumed_before=consumed_before,
            authority_consumed_after=authority.consumed,
            target_consequence_before=consequence_before,
            target_consequence_after=consequence_after,
            target_consequence_delta=(
                consequence_after - consequence_before
            ),
        )