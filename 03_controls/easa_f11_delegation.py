from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet, Optional


F11_STANDARD_WRITE = "F11_STANDARD_WRITE"
F11_ADMIN_WRITE = "F11_ADMIN_WRITE"

TOOL_F11_STANDARD = "TOOL_F11_STANDARD"
TOOL_F11_HIGH = "TOOL_F11_HIGH"


@dataclass
class LineageState:
    lineage_id: str
    consequence_ceiling: int
    consequence_count: int = 0


@dataclass
class DelegatedAuthority:
    authority_id: str
    subject_identity: str
    parent_authority_id: Optional[str]
    lineage: LineageState
    authorized_actions: FrozenSet[str]
    authorized_tools: FrozenSet[str]
    local_consequence_ceiling: int
    local_consequence_count: int
    delegation_depth_remaining: int
    authority_epoch: int
    valid: bool = True


@dataclass(frozen=True)
class DelegationDecision:
    parent_authority_id: str
    requested_child_authority_id: str
    requested_child_subject: str
    requested_actions: tuple[str, ...]
    requested_tools: tuple[str, ...]
    requested_local_consequence_ceiling: int
    requested_delegation_depth: int
    verdict: str
    reason: str
    child_authority_issued: bool


@dataclass
class DelegationResult:
    decision: DelegationDecision
    child_authority: Optional[DelegatedAuthority]


class DelegationGate:
    """
    EASA-F11 bounded delegation boundary.

    Valid delegation may attenuate authority.
    It may not amplify actions, tools, local consequence ceiling,
    delegation depth, epoch, or lineage budget.

    All valid descendants retain the exact supplied lineage-state object.
    """

    def delegate(
        self,
        *,
        parent: DelegatedAuthority,
        child_authority_id: str,
        child_subject_identity: str,
        child_actions: FrozenSet[str],
        child_tools: FrozenSet[str],
        child_local_consequence_ceiling: int,
        child_delegation_depth_remaining: int,
    ) -> DelegationResult:

        def refuse(reason: str) -> DelegationResult:

            return DelegationResult(
                decision=DelegationDecision(
                    parent_authority_id=parent.authority_id,
                    requested_child_authority_id=child_authority_id,
                    requested_child_subject=child_subject_identity,
                    requested_actions=tuple(
                        sorted(child_actions)
                    ),
                    requested_tools=tuple(
                        sorted(child_tools)
                    ),
                    requested_local_consequence_ceiling=(
                        child_local_consequence_ceiling
                    ),
                    requested_delegation_depth=(
                        child_delegation_depth_remaining
                    ),
                    verdict="REFUSE",
                    reason=reason,
                    child_authority_issued=False,
                ),
                child_authority=None,
            )

        if not parent.valid:
            return refuse("PARENT_AUTHORITY_INVALID")

        if parent.delegation_depth_remaining <= 0:
            return refuse("DELEGATION_AUTHORITY_NOT_PRESENT")

        if not child_actions.issubset(parent.authorized_actions):
            return refuse(
                "DELEGATION_ACTION_SCOPE_AMPLIFICATION"
            )

        if not child_tools.issubset(parent.authorized_tools):
            return refuse(
                "DELEGATION_TOOL_SCOPE_AMPLIFICATION"
            )

        if child_local_consequence_ceiling <= 0:
            return refuse(
                "DELEGATION_CONSEQUENCE_CEILING_INVALID"
            )

        if (
            child_local_consequence_ceiling
            > parent.local_consequence_ceiling
        ):
            return refuse(
                "DELEGATION_CONSEQUENCE_CEILING_AMPLIFICATION"
            )

        if child_delegation_depth_remaining < 0:
            return refuse(
                "DELEGATION_DEPTH_INVALID"
            )

        if (
            child_delegation_depth_remaining
            >= parent.delegation_depth_remaining
        ):
            return refuse(
                "DELEGATION_DEPTH_AMPLIFICATION"
            )

        child = DelegatedAuthority(
            authority_id=child_authority_id,
            subject_identity=child_subject_identity,
            parent_authority_id=parent.authority_id,
            lineage=parent.lineage,
            authorized_actions=frozenset(child_actions),
            authorized_tools=frozenset(child_tools),
            local_consequence_ceiling=(
                child_local_consequence_ceiling
            ),
            local_consequence_count=0,
            delegation_depth_remaining=(
                child_delegation_depth_remaining
            ),
            authority_epoch=parent.authority_epoch,
            valid=True,
        )

        return DelegationResult(
            decision=DelegationDecision(
                parent_authority_id=parent.authority_id,
                requested_child_authority_id=child_authority_id,
                requested_child_subject=child_subject_identity,
                requested_actions=tuple(
                    sorted(child_actions)
                ),
                requested_tools=tuple(
                    sorted(child_tools)
                ),
                requested_local_consequence_ceiling=(
                    child_local_consequence_ceiling
                ),
                requested_delegation_depth=(
                    child_delegation_depth_remaining
                ),
                verdict="PERMIT",
                reason="DELEGATION_AUTHORIZED",
                child_authority_issued=True,
            ),
            child_authority=child,
        )