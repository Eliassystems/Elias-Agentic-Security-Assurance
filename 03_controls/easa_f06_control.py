from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet


PRIVILEGED_ACTION = "PRIVILEGED_WRITE"


@dataclass
class ExecutionAuthority:
    authority_id: str
    subject_identity: str
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
    action: str
    consequence_before: int
    consequence_after: int
    consequence_delta: int
    authority_consumed_before: bool
    authority_consumed_after: bool


class PrivilegedWriteTool:
    """
    Bounded consequential tool for EASA-F06.

    Successful execution increments one observable consequence counter.
    """

    def __init__(self) -> None:
        self.consequence_counter = 0

    def execute(self, action: str) -> None:
        if action != PRIVILEGED_ACTION:
            raise ValueError("UNSUPPORTED_TOOL_ACTION")

        self.consequence_counter += 1


class IdentityBoundExecutionGate:
    """
    EASA-F06 execution gate.

    The authority subject identity and the presenting identity must match
    before consequence is allowed.
    """

    def attempt(
        self,
        *,
        authority: ExecutionAuthority,
        presenter_identity: str,
        action: str,
        tool: PrivilegedWriteTool,
    ) -> GateResult:

        consequence_before = tool.consequence_counter
        consumed_before = authority.consumed

        def refuse(reason: str) -> GateResult:
            consequence_after = tool.consequence_counter

            return GateResult(
                verdict="REFUSE",
                reason=reason,
                authority_id=authority.authority_id,
                subject_identity=authority.subject_identity,
                presenter_identity=presenter_identity,
                action=action,
                consequence_before=consequence_before,
                consequence_after=consequence_after,
                consequence_delta=consequence_after - consequence_before,
                authority_consumed_before=consumed_before,
                authority_consumed_after=authority.consumed,
            )

        # Existing authority properties remain explicit so F06 cannot
        # accidentally convert another security failure into an identity PASS.

        if not authority.valid:
            return refuse("EXECUTION_AUTHORITY_INVALID")

        if authority.consumed:
            return refuse("EXECUTION_AUTHORITY_ALREADY_CONSUMED")

        if not authority.governing_state_valid:
            return refuse("GOVERNING_STATE_INVALID")

        if action not in authority.authorized_actions:
            return refuse("EXECUTION_SCOPE_NOT_AUTHORIZED")

        # F06 property under examination.
        if presenter_identity != authority.subject_identity:
            return refuse("PRESENTER_IDENTITY_MISMATCH")

        if action != PRIVILEGED_ACTION:
            return refuse("ACTION_NOT_SUPPORTED")

        tool.execute(action)
        authority.consumed = True

        consequence_after = tool.consequence_counter

        return GateResult(
            verdict="PERMIT",
            reason="AUTHORIZED",
            authority_id=authority.authority_id,
            subject_identity=authority.subject_identity,
            presenter_identity=presenter_identity,
            action=action,
            consequence_before=consequence_before,
            consequence_after=consequence_after,
            consequence_delta=consequence_after - consequence_before,
            authority_consumed_before=consumed_before,
            authority_consumed_after=authority.consumed,
        )