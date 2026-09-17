from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet


REQUIRED_SCOPE = "consequential.write"


@dataclass
class ConsumableAuthority:
    authority_id: str
    actor: str
    present: bool
    scopes: FrozenSet[str]
    consumed: bool = False


@dataclass(frozen=True)
class SecurityDecision:
    verdict: str
    reason: str
    authority_id: str | None
    required_scope: str


class ReplayProtectedExecutionGate:
    """
    Single-use execution-authority gate.

    Historical validity does not imply current authority.
    Consumed authority must fail before consequence.
    """

    def evaluate(
        self,
        authority: ConsumableAuthority | None,
        required_scope: str = REQUIRED_SCOPE,
    ) -> SecurityDecision:

        if authority is None or not authority.present:
            return SecurityDecision(
                verdict="REFUSE",
                reason="EXECUTION_AUTHORITY_ABSENT",
                authority_id=None if authority is None else authority.authority_id,
                required_scope=required_scope,
            )

        if authority.consumed:
            return SecurityDecision(
                verdict="REFUSE",
                reason="EXECUTION_AUTHORITY_ALREADY_CONSUMED",
                authority_id=authority.authority_id,
                required_scope=required_scope,
            )

        if required_scope not in authority.scopes:
            return SecurityDecision(
                verdict="REFUSE",
                reason="EXECUTION_SCOPE_NOT_AUTHORIZED",
                authority_id=authority.authority_id,
                required_scope=required_scope,
            )

        return SecurityDecision(
            verdict="PERMIT",
            reason="EXECUTION_AUTHORITY_VALID",
            authority_id=authority.authority_id,
            required_scope=required_scope,
        )

    def consume(self, authority: ConsumableAuthority) -> None:
        authority.consumed = True


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
