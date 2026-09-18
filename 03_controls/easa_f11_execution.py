from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet

from easa_f11_delegation import DelegatedAuthority


@dataclass
class ConsequentialTool:
    tool_identity: str
    supported_actions: FrozenSet[str]
    consequence_counter: int = 0

    def execute(self, action: str) -> None:

        if action not in self.supported_actions:
            raise ValueError("TOOL_ACTION_NOT_SUPPORTED")

        self.consequence_counter += 1


@dataclass(frozen=True)
class ExecutionDecision:
    presenter_identity: str
    authority_id: str
    lineage_id: str
    action: str
    target_tool_identity: str
    verdict: str
    reason: str
    local_count_before: int
    local_count_after: int
    local_ceiling: int
    lineage_count_before: int
    lineage_count_after: int
    lineage_ceiling: int
    consequence_before: int
    consequence_after: int
    consequence_delta: int


class LineageExecutionGate:
    """
    EASA-F11 bounded lineage execution boundary.

    Execution consumes both:
    - the authority's local consequence budget; and
    - the shared lineage consequence budget.

    Descendant creation therefore cannot reset the shared lineage budget.
    """

    def attempt(
        self,
        *,
        authority: DelegatedAuthority,
        presenter_identity: str,
        action: str,
        target_tool: ConsequentialTool,
    ) -> ExecutionDecision:

        local_before = authority.local_consequence_count
        lineage_before = authority.lineage.consequence_count
        consequence_before = target_tool.consequence_counter

        def refuse(reason: str) -> ExecutionDecision:

            consequence_after = target_tool.consequence_counter

            return ExecutionDecision(
                presenter_identity=presenter_identity,
                authority_id=authority.authority_id,
                lineage_id=authority.lineage.lineage_id,
                action=action,
                target_tool_identity=target_tool.tool_identity,
                verdict="REFUSE",
                reason=reason,
                local_count_before=local_before,
                local_count_after=(
                    authority.local_consequence_count
                ),
                local_ceiling=(
                    authority.local_consequence_ceiling
                ),
                lineage_count_before=lineage_before,
                lineage_count_after=(
                    authority.lineage.consequence_count
                ),
                lineage_ceiling=(
                    authority.lineage.consequence_ceiling
                ),
                consequence_before=consequence_before,
                consequence_after=consequence_after,
                consequence_delta=(
                    consequence_after - consequence_before
                ),
            )

        if not authority.valid:
            return refuse("EXECUTION_AUTHORITY_INVALID")

        if presenter_identity != authority.subject_identity:
            return refuse("PRESENTER_IDENTITY_MISMATCH")

        if action not in authority.authorized_actions:
            return refuse("EXECUTION_SCOPE_NOT_AUTHORIZED")

        if (
            target_tool.tool_identity
            not in authority.authorized_tools
        ):
            return refuse("TOOL_IDENTITY_MISMATCH")

        if action not in target_tool.supported_actions:
            return refuse("ACTION_NOT_SUPPORTED_BY_TOOL")

        if (
            authority.local_consequence_count
            >= authority.local_consequence_ceiling
        ):
            return refuse(
                "LOCAL_CONSEQUENCE_CEILING_EXHAUSTED"
            )

        if (
            authority.lineage.consequence_count
            >= authority.lineage.consequence_ceiling
        ):
            return refuse(
                "LINEAGE_CONSEQUENCE_CEILING_EXHAUSTED"
            )

        target_tool.execute(action)

        authority.local_consequence_count += 1
        authority.lineage.consequence_count += 1

        consequence_after = target_tool.consequence_counter

        return ExecutionDecision(
            presenter_identity=presenter_identity,
            authority_id=authority.authority_id,
            lineage_id=authority.lineage.lineage_id,
            action=action,
            target_tool_identity=target_tool.tool_identity,
            verdict="PERMIT",
            reason="AUTHORIZED",
            local_count_before=local_before,
            local_count_after=(
                authority.local_consequence_count
            ),
            local_ceiling=(
                authority.local_consequence_ceiling
            ),
            lineage_count_before=lineage_before,
            lineage_count_after=(
                authority.lineage.consequence_count
            ),
            lineage_ceiling=(
                authority.lineage.consequence_ceiling
            ),
            consequence_before=consequence_before,
            consequence_after=consequence_after,
            consequence_delta=(
                consequence_after - consequence_before
            ),
        )