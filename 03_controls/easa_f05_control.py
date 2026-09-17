from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet


HIGH_IMPACT_ACTION = "HIGH_IMPACT_WRITE"
REQUIRED_SCOPE = "high_impact.write"


@dataclass(frozen=True)
class ExecutionAuthority:
    authority_id: str
    actor: str
    present: bool
    scopes: FrozenSet[str]


@dataclass(frozen=True)
class HumanAuthority:
    required: bool
    present: bool
    authority_id: str | None = None


@dataclass(frozen=True)
class SecurityDecision:
    verdict: str
    reason: str
    execution_authority_id: str | None
    human_authority_id: str | None
    action: str
    required_scope: str


class HumanAuthorityExecutionGate:
    """
    High-impact execution gate.

    Machine execution authority cannot substitute for required
    external human authority.
    """

    def evaluate(
        self,
        execution_authority: ExecutionAuthority | None,
        human_authority: HumanAuthority,
        action: str = HIGH_IMPACT_ACTION,
        required_scope: str = REQUIRED_SCOPE,
    ) -> SecurityDecision:

        if execution_authority is None or not execution_authority.present:
            return SecurityDecision(
                verdict="REFUSE",
                reason="EXECUTION_AUTHORITY_ABSENT",
                execution_authority_id=(
                    None if execution_authority is None
                    else execution_authority.authority_id
                ),
                human_authority_id=human_authority.authority_id,
                action=action,
                required_scope=required_scope,
            )

        if required_scope not in execution_authority.scopes:
            return SecurityDecision(
                verdict="REFUSE",
                reason="EXECUTION_SCOPE_NOT_AUTHORIZED",
                execution_authority_id=execution_authority.authority_id,
                human_authority_id=human_authority.authority_id,
                action=action,
                required_scope=required_scope,
            )

        if human_authority.required and not human_authority.present:
            return SecurityDecision(
                verdict="REFUSE",
                reason="REQUIRED_HUMAN_AUTHORITY_ABSENT",
                execution_authority_id=execution_authority.authority_id,
                human_authority_id=human_authority.authority_id,
                action=action,
                required_scope=required_scope,
            )

        return SecurityDecision(
            verdict="PERMIT",
            reason="REQUIRED_AUTHORITIES_PRESENT",
            execution_authority_id=execution_authority.authority_id,
            human_authority_id=human_authority.authority_id,
            action=action,
            required_scope=required_scope,
        )


class HighImpactTool:
    def __init__(self) -> None:
        self.consequence_count = 0

    def execute(self, action: str) -> dict:
        self.consequence_count += 1

        return {
            "tool": "bounded-high-impact-tool",
            "action": action,
            "executed": True,
            "consequence_count": self.consequence_count,
        }
