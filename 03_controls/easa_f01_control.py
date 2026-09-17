from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Optional


REQUIRED_SCOPE = "consequential.write"


@dataclass(frozen=True)
class ExecutionAuthority:
    authority_id: str
    actor: str
    present: bool
    scopes: FrozenSet[str]


@dataclass(frozen=True)
class SecurityDecision:
    verdict: str
    reason: str
    authority_id: Optional[str]
    required_scope: str


class ExecutionGate:
    """
    Independent consequence-boundary security gate.

    Agent request != execution authority.
    Tool availability != permission.
    """

    def evaluate(
        self,
        authority: Optional[ExecutionAuthority],
        required_scope: str = REQUIRED_SCOPE,
    ) -> SecurityDecision:

        if authority is None or not authority.present:
            return SecurityDecision(
                verdict="REFUSE",
                reason="EXECUTION_AUTHORITY_ABSENT",
                authority_id=None if authority is None else authority.authority_id,
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


class ConsequentialTool:
    """
    Local bounded consequential tool.

    Execution changes observable state by incrementing consequence_count.
    """

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
