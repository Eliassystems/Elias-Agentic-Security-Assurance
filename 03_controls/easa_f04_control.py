from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet


REQUIRED_SCOPE = "consequential.write"


@dataclass(frozen=True)
class StateBoundAuthority:
    authority_id: str
    actor: str
    present: bool
    scopes: FrozenSet[str]
    state_epoch: int


@dataclass(frozen=True)
class SecurityDecision:
    verdict: str
    reason: str
    authority_id: str | None
    required_scope: str
    authority_state_epoch: int | None
    current_state_epoch: int


class ChangedStateExecutionGate:
    """
    Execution gate requiring authority to correspond to the
    current governing-state epoch.
    """

    def evaluate(
        self,
        authority: StateBoundAuthority | None,
        current_state_epoch: int,
        required_scope: str = REQUIRED_SCOPE,
    ) -> SecurityDecision:

        if authority is None or not authority.present:
            return SecurityDecision(
                verdict="REFUSE",
                reason="EXECUTION_AUTHORITY_ABSENT",
                authority_id=None if authority is None else authority.authority_id,
                required_scope=required_scope,
                authority_state_epoch=None if authority is None else authority.state_epoch,
                current_state_epoch=current_state_epoch,
            )

        if required_scope not in authority.scopes:
            return SecurityDecision(
                verdict="REFUSE",
                reason="EXECUTION_SCOPE_NOT_AUTHORIZED",
                authority_id=authority.authority_id,
                required_scope=required_scope,
                authority_state_epoch=authority.state_epoch,
                current_state_epoch=current_state_epoch,
            )

        if authority.state_epoch != current_state_epoch:
            return SecurityDecision(
                verdict="REFUSE",
                reason="EXECUTION_AUTHORITY_STATE_CHANGED",
                authority_id=authority.authority_id,
                required_scope=required_scope,
                authority_state_epoch=authority.state_epoch,
                current_state_epoch=current_state_epoch,
            )

        return SecurityDecision(
            verdict="PERMIT",
            reason="EXECUTION_AUTHORITY_CURRENT",
            authority_id=authority.authority_id,
            required_scope=required_scope,
            authority_state_epoch=authority.state_epoch,
            current_state_epoch=current_state_epoch,
        )


class ConsequentialTool:
    def __init__(self) -> None:
        self.consequence_count = 0

    def execute(self, requested_action: str) -> dict:
        self.consequence_count += 1

        return {
            "tool": REQUIRED_SCOPE,
            "action": requested_action,
            "executed": True,
            "consequence_count": self.consequence_count,
        }
