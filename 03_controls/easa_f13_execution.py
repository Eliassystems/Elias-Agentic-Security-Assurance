from __future__ import annotations

from dataclasses import dataclass

from easa_f13_authority import (
    AUTHORITY_SOURCE_ID,
    ExecutionAuthority,
    F13_ACTION,
    F13_TOOL,
)
from easa_f13_peer_state import PeerSnapshot


@dataclass
class ConsequentialTool:
    tool_identity: str = F13_TOOL
    consequence_counter: int = 0

    def execute(self, action: str) -> None:

        if action != F13_ACTION:
            raise ValueError("ACTION_NOT_SUPPORTED_BY_TOOL")

        self.consequence_counter += 1


@dataclass(frozen=True)
class ExecutionDecision:
    presenter_identity: str
    authority_id: str
    authority_issuer_identity: str
    authority_valid: bool
    authority_consumed_before: bool
    authority_consumed_after: bool
    action: str
    target_tool_identity: str

    local_peer_id: str
    local_peer_state_identity: str
    local_peer_version: int
    local_peer_standing: str
    local_peer_admissible: bool

    authoritative_peer_id: str
    authoritative_peer_state_identity: str
    authoritative_peer_version: int
    authoritative_peer_standing: str
    authoritative_peer_admissible: bool

    freshness_correspondence: bool

    verdict: str
    reason: str

    consequence_before: int
    consequence_after: int
    consequence_delta: int


class F13ExecutionGate:
    """
    F13 requires both:
      1. valid execution authority; and
      2. current admissible peer standing.

    Authority validation precedes peer-state evaluation.

    Once authority standing is valid, a stale peer snapshot is refused
    specifically as PEER_STATE_STALE.
    """

    expected_authority_source_identity = AUTHORITY_SOURCE_ID
    requires_current_peer_state = True
    requires_admissible_peer_standing = True

    def policy_snapshot(self) -> dict:
        return {
            "expected_authority_source_identity":
                self.expected_authority_source_identity,
            "requires_current_peer_state":
                self.requires_current_peer_state,
            "requires_admissible_peer_standing":
                self.requires_admissible_peer_standing,
        }

    def attempt(
        self,
        *,
        authority: ExecutionAuthority,
        presenter_identity: str,
        local_peer_snapshot: PeerSnapshot,
        authoritative_peer_state: PeerSnapshot,
        action: str,
        target_tool: ConsequentialTool,
    ) -> ExecutionDecision:

        consumed_before = authority.consumed
        consequence_before = target_tool.consequence_counter

        freshness_correspondence = (
            local_peer_snapshot.peer_id
            == authoritative_peer_state.peer_id
            and
            local_peer_snapshot.version
            == authoritative_peer_state.version
        )

        def decision(
            *,
            verdict: str,
            reason: str,
        ) -> ExecutionDecision:

            consequence_after = target_tool.consequence_counter

            return ExecutionDecision(
                presenter_identity=presenter_identity,
                authority_id=authority.authority_id,
                authority_issuer_identity=authority.issuer_identity,
                authority_valid=authority.valid,
                authority_consumed_before=consumed_before,
                authority_consumed_after=authority.consumed,
                action=action,
                target_tool_identity=target_tool.tool_identity,

                local_peer_id=local_peer_snapshot.peer_id,
                local_peer_state_identity=(
                    local_peer_snapshot.state_identity
                ),
                local_peer_version=local_peer_snapshot.version,
                local_peer_standing=local_peer_snapshot.standing,
                local_peer_admissible=local_peer_snapshot.admissible,

                authoritative_peer_id=(
                    authoritative_peer_state.peer_id
                ),
                authoritative_peer_state_identity=(
                    authoritative_peer_state.state_identity
                ),
                authoritative_peer_version=(
                    authoritative_peer_state.version
                ),
                authoritative_peer_standing=(
                    authoritative_peer_state.standing
                ),
                authoritative_peer_admissible=(
                    authoritative_peer_state.admissible
                ),

                freshness_correspondence=freshness_correspondence,

                verdict=verdict,
                reason=reason,

                consequence_before=consequence_before,
                consequence_after=consequence_after,
                consequence_delta=(
                    consequence_after - consequence_before
                ),
            )

        # ----------------------------------------------------
        # EXECUTION-AUTHORITY PLANE
        # ----------------------------------------------------

        if (
            authority.issuer_identity
            != self.expected_authority_source_identity
        ):
            return decision(
                verdict="REFUSE",
                reason="EXECUTION_AUTHORITY_ISSUER_NOT_AUTHORIZED",
            )

        if not authority.valid:
            return decision(
                verdict="REFUSE",
                reason="EXECUTION_AUTHORITY_INVALID",
            )

        if authority.consumed:
            return decision(
                verdict="REFUSE",
                reason="EXECUTION_AUTHORITY_ALREADY_CONSUMED",
            )

        if presenter_identity != authority.subject_identity:
            return decision(
                verdict="REFUSE",
                reason="PRESENTER_IDENTITY_MISMATCH",
            )

        if action != authority.authorized_action:
            return decision(
                verdict="REFUSE",
                reason="EXECUTION_SCOPE_NOT_AUTHORIZED",
            )

        if target_tool.tool_identity != authority.bound_tool_identity:
            return decision(
                verdict="REFUSE",
                reason="TOOL_IDENTITY_MISMATCH",
            )

        # ----------------------------------------------------
        # PEER-DEPENDENT GOVERNING PLANE
        # ----------------------------------------------------

        if (
            local_peer_snapshot.peer_id
            != authoritative_peer_state.peer_id
        ):
            return decision(
                verdict="REFUSE",
                reason="PEER_IDENTITY_MISMATCH",
            )

        if (
            local_peer_snapshot.version
            != authoritative_peer_state.version
        ):
            return decision(
                verdict="REFUSE",
                reason="PEER_STATE_STALE",
            )

        if authoritative_peer_state.admissible is not True:
            return decision(
                verdict="REFUSE",
                reason="PEER_STANDING_NOT_ADMISSIBLE",
            )

        # The local snapshot is current, but authoritative standing
        # remains the governing admissibility source.
        if action != F13_ACTION:
            return decision(
                verdict="REFUSE",
                reason="ACTION_NOT_SUPPORTED",
            )

        target_tool.execute(action)
        authority.consumed = True

        return decision(
            verdict="PERMIT",
            reason="AUTHORIZED",
        )