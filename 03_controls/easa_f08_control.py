from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import FrozenSet


CONCURRENT_ACTION = "CONCURRENT_PRIVILEGED_WRITE"
BOUND_TOOL = "TOOL_F08"


@dataclass
class SingleUseAuthority:
    authority_id: str
    authorized_presenters: FrozenSet[str]
    bound_tool_identity: str
    authorized_actions: FrozenSet[str]
    valid: bool = True
    consumed: bool = False
    governing_state_valid: bool = True
    single_use: bool = True
    _consumption_lock: threading.Lock = field(
        default_factory=threading.Lock,
        repr=False,
        compare=False,
    )


@dataclass(frozen=True)
class GateResult:
    presenter_identity: str
    authority_id: str
    verdict: str
    reason: str
    target_tool_identity: str
    action: str
    authority_consumed_before: bool
    authority_consumed_after: bool
    consequence_before: int
    consequence_after: int
    consequence_delta: int


class ConsequentialTool:
    """
    Bounded F08 consequential tool.

    The counter is mutated only after the execution gate has claimed the
    single-use authority while holding the authority's collision lock.
    """

    def __init__(self, tool_identity: str) -> None:
        self.tool_identity = tool_identity
        self.consequence_counter = 0

    def execute(self, action: str) -> None:
        if action != CONCURRENT_ACTION:
            raise ValueError("UNSUPPORTED_TOOL_ACTION")

        self.consequence_counter += 1


class ConcurrentSingleUseExecutionGate:
    """
    EASA-F08 gate.

    For the bounded thread-based reference system, current authority state,
    single-use claim, and consequential commit are serialized by one lock
    attached to the exact shared authority object.

    This is not a distributed-locking or cross-process claim.
    """

    def attempt(
        self,
        *,
        authority: SingleUseAuthority,
        presenter_identity: str,
        action: str,
        target_tool: ConsequentialTool,
    ) -> GateResult:

        with authority._consumption_lock:

            consequence_before = target_tool.consequence_counter
            consumed_before = authority.consumed

            def refuse(reason: str) -> GateResult:
                consequence_after = target_tool.consequence_counter

                return GateResult(
                    presenter_identity=presenter_identity,
                    authority_id=authority.authority_id,
                    verdict="REFUSE",
                    reason=reason,
                    target_tool_identity=target_tool.tool_identity,
                    action=action,
                    authority_consumed_before=consumed_before,
                    authority_consumed_after=authority.consumed,
                    consequence_before=consequence_before,
                    consequence_after=consequence_after,
                    consequence_delta=(
                        consequence_after - consequence_before
                    ),
                )

            if not authority.valid:
                return refuse("EXECUTION_AUTHORITY_INVALID")

            if authority.consumed:
                return refuse("EXECUTION_AUTHORITY_ALREADY_CONSUMED")

            if not authority.single_use:
                return refuse("AUTHORITY_NOT_SINGLE_USE")

            if not authority.governing_state_valid:
                return refuse("GOVERNING_STATE_INVALID")

            if presenter_identity not in authority.authorized_presenters:
                return refuse("PRESENTER_IDENTITY_NOT_AUTHORIZED")

            if action not in authority.authorized_actions:
                return refuse("EXECUTION_SCOPE_NOT_AUTHORIZED")

            if target_tool.tool_identity != authority.bound_tool_identity:
                return refuse("TOOL_IDENTITY_MISMATCH")

            if action != CONCURRENT_ACTION:
                return refuse("ACTION_NOT_SUPPORTED")

            # F08 collision boundary:
            #
            # Claim the one available use BEFORE consequential execution
            # while still holding the exact shared authority lock.
            authority.consumed = True

            target_tool.execute(action)

            consequence_after = target_tool.consequence_counter

            return GateResult(
                presenter_identity=presenter_identity,
                authority_id=authority.authority_id,
                verdict="PERMIT",
                reason="AUTHORIZED",
                target_tool_identity=target_tool.tool_identity,
                action=action,
                authority_consumed_before=consumed_before,
                authority_consumed_after=authority.consumed,
                consequence_before=consequence_before,
                consequence_after=consequence_after,
                consequence_delta=(
                    consequence_after - consequence_before
                ),
            )