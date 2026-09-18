from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from easa_f15_resolver import (
    AuthoritativeStateSource,
    ResolverReplica,
)


F15_PRESENTER = "AGENT_F15"
F15_ACTION = "F15_PARTITION_SENSITIVE_WRITE"
F15_TOOL = "TOOL_F15"

FROZEN_AUTHORITY_IDS = {
    "AUTH_F15-BASELINE",
    "AUTH_F15-PARTITION",
    "AUTH_F15-CONFLICT",
    "AUTH_F15-CURRENT-BLOCKED",
    "AUTH_F15-RECOVERY",
}


@dataclass
class ExecutionAuthority:
    authority_id: str
    subject_identity: str
    authorized_action: str
    bound_tool_identity: str
    valid: bool = True
    consumed: bool = False


class ConsequentialTool:

    tool_identity = F15_TOOL

    def __init__(self) -> None:
        self._counter = 0

    @property
    def consequence_counter(self) -> int:
        return self._counter

    def execute(
        self,
        action: str,
    ) -> tuple[int, int]:

        if action != F15_ACTION:
            raise RuntimeError(
                "F15_TOOL_ACTION_NOT_SUPPORTED"
            )

        before = self._counter
        self._counter += 1
        after = self._counter

        return before, after


@dataclass(frozen=True)
class ExecutionDecision:

    attempt_id: str

    presenter_identity: str

    authority_id: str
    authority_valid: bool
    authority_consumed_before: bool
    authority_consumed_after: bool

    action: str
    tool_identity: str

    authoritative_state_version: str
    authoritative_state: str
    authoritative_admissibility: bool

    resolver_a_availability: bool
    resolver_a_state_version: Optional[str]
    resolver_a_state: Optional[str]
    resolver_a_admissibility: Optional[bool]

    resolver_b_availability: bool
    resolver_b_state_version: Optional[str]
    resolver_b_state: Optional[str]
    resolver_b_admissibility: Optional[bool]

    cached_state_version: Optional[str]
    cached_state: Optional[str]
    cached_admissibility: Optional[bool]

    resolution_status: str

    verdict: str
    reason: str

    consequence_before: int
    consequence_after: int
    consequence_delta: int


def constitute_authority(
    authority_id: str,
) -> ExecutionAuthority:

    if authority_id not in FROZEN_AUTHORITY_IDS:

        raise RuntimeError(
            "F15_AUTHORITY_ID_NOT_IN_FROZEN_DEFINITION"
        )

    return ExecutionAuthority(
        authority_id=authority_id,
        subject_identity=F15_PRESENTER,
        authorized_action=F15_ACTION,
        bound_tool_identity=F15_TOOL,
        valid=True,
        consumed=False,
    )


class F15ExecutionGate:

    def attempt(
        self,
        *,
        attempt_id: str,
        presenter_identity: str,
        authority: ExecutionAuthority,
        action: str,
        tool: ConsequentialTool,
        state_source: AuthoritativeStateSource,
        resolver_a: ResolverReplica,
        resolver_b: ResolverReplica,
        cached_state: Optional[dict] = None,
    ) -> ExecutionDecision:

        authoritative = (
            state_source.current
        )

        a = resolver_a.observe()
        b = resolver_b.observe()

        consumed_before = (
            authority.consumed
        )

        cached_state_version = None
        cached_state_name = None
        cached_admissibility = None

        if cached_state is not None:

            cached_state_version = (
                cached_state[
                    "state_version"
                ]
            )

            cached_state_name = (
                cached_state["state"]
            )

            cached_admissibility = (
                cached_state[
                    "admissible"
                ]
            )

        def build_refusal(
            *,
            reason: str,
            resolution_status: str,
        ) -> ExecutionDecision:

            before = (
                tool.consequence_counter
            )

            return ExecutionDecision(
                attempt_id=attempt_id,

                presenter_identity=(
                    presenter_identity
                ),

                authority_id=(
                    authority.authority_id
                ),

                authority_valid=(
                    authority.valid
                ),

                authority_consumed_before=(
                    consumed_before
                ),

                authority_consumed_after=(
                    authority.consumed
                ),

                action=action,

                tool_identity=(
                    tool.tool_identity
                ),

                authoritative_state_version=(
                    authoritative.state_version
                ),

                authoritative_state=(
                    authoritative.state
                ),

                authoritative_admissibility=(
                    authoritative.admissible
                ),

                resolver_a_availability=(
                    a.available
                ),

                resolver_a_state_version=(
                    a.state_version
                ),

                resolver_a_state=(
                    a.state
                ),

                resolver_a_admissibility=(
                    a.admissible
                ),

                resolver_b_availability=(
                    b.available
                ),

                resolver_b_state_version=(
                    b.state_version
                ),

                resolver_b_state=(
                    b.state
                ),

                resolver_b_admissibility=(
                    b.admissible
                ),

                cached_state_version=(
                    cached_state_version
                ),

                cached_state=(
                    cached_state_name
                ),

                cached_admissibility=(
                    cached_admissibility
                ),

                resolution_status=(
                    resolution_status
                ),

                verdict="REFUSE",
                reason=reason,

                consequence_before=before,
                consequence_after=before,
                consequence_delta=0,
            )

        # ----------------------------------------------------
        # AUTHORITY BOUNDARY
        # ----------------------------------------------------

        if authority.valid is not True:

            return build_refusal(
                reason=(
                    "EXECUTION_AUTHORITY_INVALID"
                ),
                resolution_status=(
                    "NOT_EVALUATED"
                ),
            )

        if authority.consumed:

            return build_refusal(
                reason=(
                    "EXECUTION_AUTHORITY_ALREADY_CONSUMED"
                ),
                resolution_status=(
                    "NOT_EVALUATED"
                ),
            )

        if (
            presenter_identity
            != authority.subject_identity
        ):

            return build_refusal(
                reason=(
                    "PRESENTER_IDENTITY_MISMATCH"
                ),
                resolution_status=(
                    "NOT_EVALUATED"
                ),
            )

        if (
            action
            != authority.authorized_action
        ):

            return build_refusal(
                reason=(
                    "EXECUTION_SCOPE_NOT_AUTHORIZED"
                ),
                resolution_status=(
                    "NOT_EVALUATED"
                ),
            )

        if (
            tool.tool_identity
            != authority.bound_tool_identity
        ):

            return build_refusal(
                reason=(
                    "TOOL_IDENTITY_MISMATCH"
                ),
                resolution_status=(
                    "NOT_EVALUATED"
                ),
            )

        # ----------------------------------------------------
        # RESOLUTION AVAILABILITY
        # ----------------------------------------------------

        if (
            a.available is not True
            or
            b.available is not True
        ):

            return build_refusal(
                reason=(
                    "CURRENT_RESOLUTION_UNAVAILABLE"
                ),
                resolution_status=(
                    "UNAVAILABLE"
                ),
            )

        # ----------------------------------------------------
        # RESOLUTION COMPLETENESS
        # ----------------------------------------------------

        if (
            a.state_version is None
            or
            a.state is None
            or
            a.admissible is None
            or
            b.state_version is None
            or
            b.state is None
            or
            b.admissible is None
        ):

            return build_refusal(
                reason=(
                    "CURRENT_RESOLUTION_UNAVAILABLE"
                ),
                resolution_status=(
                    "INCOMPLETE"
                ),
            )

        # ----------------------------------------------------
        # RESOLVER CONSISTENCY
        # ----------------------------------------------------

        resolver_views_match = (
            a.state_version
            == b.state_version
            and
            a.state
            == b.state
            and
            a.admissible
            == b.admissible
        )

        if not resolver_views_match:

            return build_refusal(
                reason=(
                    "RESOLVER_STATE_CONFLICT"
                ),
                resolution_status=(
                    "CONFLICT"
                ),
            )

        # ----------------------------------------------------
        # AUTHORITATIVE CORRESPONDENCE
        # ----------------------------------------------------

        corresponds_to_authoritative = (
            a.state_version
            == authoritative.state_version
            and
            a.state
            == authoritative.state
            and
            a.admissible
            == authoritative.admissible
        )

        if not corresponds_to_authoritative:

            return build_refusal(
                reason=(
                    "RESOLVER_STATE_NOT_CURRENT"
                ),
                resolution_status=(
                    "STALE"
                ),
            )

        # ----------------------------------------------------
        # CURRENT ADMISSIBILITY
        # ----------------------------------------------------

        if authoritative.admissible is not True:

            return build_refusal(
                reason=(
                    "RESOLVED_STATE_NOT_ADMISSIBLE"
                ),
                resolution_status=(
                    "CURRENT_CONSISTENT_INADMISSIBLE"
                ),
            )

        # ----------------------------------------------------
        # PERMIT
        # ----------------------------------------------------

        before, after = tool.execute(
            action
        )

        authority.consumed = True

        return ExecutionDecision(
            attempt_id=attempt_id,

            presenter_identity=(
                presenter_identity
            ),

            authority_id=(
                authority.authority_id
            ),

            authority_valid=(
                authority.valid
            ),

            authority_consumed_before=(
                consumed_before
            ),

            authority_consumed_after=(
                authority.consumed
            ),

            action=action,

            tool_identity=(
                tool.tool_identity
            ),

            authoritative_state_version=(
                authoritative.state_version
            ),

            authoritative_state=(
                authoritative.state
            ),

            authoritative_admissibility=(
                authoritative.admissible
            ),

            resolver_a_availability=(
                a.available
            ),

            resolver_a_state_version=(
                a.state_version
            ),

            resolver_a_state=(
                a.state
            ),

            resolver_a_admissibility=(
                a.admissible
            ),

            resolver_b_availability=(
                b.available
            ),

            resolver_b_state_version=(
                b.state_version
            ),

            resolver_b_state=(
                b.state
            ),

            resolver_b_admissibility=(
                b.admissible
            ),

            cached_state_version=(
                cached_state_version
            ),

            cached_state=(
                cached_state_name
            ),

            cached_admissibility=(
                cached_admissibility
            ),

            resolution_status=(
                "CURRENT_CONSISTENT_ADMISSIBLE"
            ),

            verdict="PERMIT",
            reason="AUTHORIZED",

            consequence_before=before,
            consequence_after=after,
            consequence_delta=(
                after - before
            ),
        )