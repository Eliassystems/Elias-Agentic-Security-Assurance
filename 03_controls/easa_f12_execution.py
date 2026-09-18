from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from easa_f12_authority import (
    AUTHORITY_SOURCE_ID,
    ExecutionAuthority,
    F12_ACTION,
    F12_TOOL,
)


@dataclass
class ConsequentialTool:
    tool_identity: str = F12_TOOL
    consequence_counter: int = 0

    def execute(self, action: str) -> None:

        if action != F12_ACTION:
            raise ValueError("ACTION_NOT_SUPPORTED_BY_TOOL")

        self.consequence_counter += 1


@dataclass(frozen=True)
class ExecutionDecision:
    presenter_identity: str
    candidate_artifact_type: str
    execution_authority_present: bool
    authority_id: Optional[str]
    authority_issuer_identity: Optional[str]
    target_tool_identity: str
    action: str
    verdict: str
    reason: str
    authority_consumed_before: Optional[bool]
    authority_consumed_after: Optional[bool]
    consequence_before: int
    consequence_after: int
    consequence_delta: int


class F12ExecutionGate:
    """
    Bounded F12 authority gate.

    Advisory recommendations and AdvisoryResolution artifacts
    are not execution authority.

    Only an actual ExecutionAuthority issued by the frozen
    authoritative source can proceed to normal authorization checks.
    """

    expected_authority_source_identity = AUTHORITY_SOURCE_ID
    requires_execution_authority = True

    def policy_snapshot(self) -> dict:
        return {
            "expected_authority_source_identity":
                self.expected_authority_source_identity,
            "requires_execution_authority":
                self.requires_execution_authority,
        }

    def attempt(
        self,
        *,
        authority_candidate: Any,
        presenter_identity: str,
        action: str,
        target_tool: ConsequentialTool,
    ) -> ExecutionDecision:

        consequence_before = target_tool.consequence_counter

        if authority_candidate is None:

            return ExecutionDecision(
                presenter_identity=presenter_identity,
                candidate_artifact_type="NONE",
                execution_authority_present=False,
                authority_id=None,
                authority_issuer_identity=None,
                target_tool_identity=target_tool.tool_identity,
                action=action,
                verdict="REFUSE",
                reason="EXECUTION_AUTHORITY_NOT_PRESENT",
                authority_consumed_before=None,
                authority_consumed_after=None,
                consequence_before=consequence_before,
                consequence_after=target_tool.consequence_counter,
                consequence_delta=0,
            )

        if not isinstance(
            authority_candidate,
            ExecutionAuthority,
        ):

            candidate_type = getattr(
                authority_candidate,
                "artifact_type",
                type(authority_candidate).__name__,
            )

            return ExecutionDecision(
                presenter_identity=presenter_identity,
                candidate_artifact_type=str(candidate_type),
                execution_authority_present=False,
                authority_id=None,
                authority_issuer_identity=None,
                target_tool_identity=target_tool.tool_identity,
                action=action,
                verdict="REFUSE",
                reason="NON_AUTHORITY_ARTIFACT",
                authority_consumed_before=None,
                authority_consumed_after=None,
                consequence_before=consequence_before,
                consequence_after=target_tool.consequence_counter,
                consequence_delta=0,
            )

        authority = authority_candidate

        consumed_before = authority.consumed

        def refuse(reason: str) -> ExecutionDecision:

            consequence_after = target_tool.consequence_counter

            return ExecutionDecision(
                presenter_identity=presenter_identity,
                candidate_artifact_type=authority.artifact_type,
                execution_authority_present=True,
                authority_id=authority.authority_id,
                authority_issuer_identity=authority.issuer_identity,
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

        if (
            authority.issuer_identity
            != self.expected_authority_source_identity
        ):
            return refuse(
                "EXECUTION_AUTHORITY_ISSUER_NOT_AUTHORIZED"
            )

        if not authority.valid:
            return refuse("EXECUTION_AUTHORITY_INVALID")

        if authority.consumed:
            return refuse("EXECUTION_AUTHORITY_ALREADY_CONSUMED")

        if presenter_identity != authority.subject_identity:
            return refuse("PRESENTER_IDENTITY_MISMATCH")

        if action != authority.authorized_action:
            return refuse("EXECUTION_SCOPE_NOT_AUTHORIZED")

        if target_tool.tool_identity != authority.bound_tool_identity:
            return refuse("TOOL_IDENTITY_MISMATCH")

        if action != F12_ACTION:
            return refuse("ACTION_NOT_SUPPORTED")

        target_tool.execute(action)
        authority.consumed = True

        consequence_after = target_tool.consequence_counter

        return ExecutionDecision(
            presenter_identity=presenter_identity,
            candidate_artifact_type=authority.artifact_type,
            execution_authority_present=True,
            authority_id=authority.authority_id,
            authority_issuer_identity=authority.issuer_identity,
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