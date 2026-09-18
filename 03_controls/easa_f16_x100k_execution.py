from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Optional


PRIMARY_TOOL = "TOOL_F16_X100K_PRIMARY"
ALTERNATE_TOOL = "TOOL_F16_X100K_OTHER"
ACTION = "F16_X100K_BOUNDED_SCALE_WRITE"


@dataclass
class ExecutionAuthority:
    authority_id: str
    subject_identity: str
    authorized_action: str
    authorized_tool_identity: str
    valid: bool = True
    consumed: bool = False

    def __post_init__(self) -> None:
        self._lock = threading.RLock()

    def consumed_snapshot(self) -> bool:
        with self._lock:
            return self.consumed


class ConsequentialTool:

    def __init__(
        self,
        tool_identity: str,
    ) -> None:

        if tool_identity not in {
            PRIMARY_TOOL,
            ALTERNATE_TOOL,
        }:
            raise ValueError(
                "F16_X100K_TOOL_IDENTITY_NOT_FROZEN"
            )

        self.tool_identity = tool_identity
        self._counter = 0
        self._lock = threading.Lock()

    @property
    def consequence_counter(self) -> int:

        with self._lock:
            return self._counter

    def execute(
        self,
        action: str,
    ) -> tuple[int, int]:

        if action != ACTION:
            raise RuntimeError(
                "F16_X100K_ACTION_NOT_FROZEN"
            )

        with self._lock:

            before = self._counter
            self._counter += 1
            after = self._counter

            return before, after


@dataclass(frozen=True)
class ExecutionDecision:
    attempt_index: int
    display_sequence: int
    attempt_id: str
    attempt_class: str
    presenter_identity: str

    authority_present: bool
    authority_id: Optional[str]
    authority_subject_identity: Optional[str]
    authority_valid: Optional[bool]
    authority_consumed_before: Optional[bool]
    authority_consumed_after: Optional[bool]

    authorized_action: Optional[str]
    requested_action: str

    authorized_tool_identity: Optional[str]
    presented_tool_identity: str

    verdict: str
    reason: str

    consequence_before: int
    consequence_after: int
    consequence_delta: int

    worker_thread_identity: str


class X100KExecutionGate:

    def attempt(
        self,
        *,
        attempt_index: int,
        display_sequence: int,
        attempt_id: str,
        attempt_class: str,
        presenter_identity: str,
        authority: Optional[ExecutionAuthority],
        requested_action: str,
        presented_tool: ConsequentialTool,
    ) -> ExecutionDecision:

        worker_identity = (
            f"{threading.current_thread().name}:"
            f"{threading.get_ident()}"
        )

        def authority_fields():

            if authority is None:

                return {
                    "authority_present": False,
                    "authority_id": None,
                    "authority_subject_identity": None,
                    "authority_valid": None,
                    "authority_consumed_before": None,
                    "authority_consumed_after": None,
                    "authorized_action": None,
                    "authorized_tool_identity": None,
                }

            return {
                "authority_present": True,
                "authority_id":
                    authority.authority_id,
                "authority_subject_identity":
                    authority.subject_identity,
                "authority_valid":
                    authority.valid,
                "authority_consumed_before":
                    authority.consumed_snapshot(),
                "authority_consumed_after":
                    authority.consumed_snapshot(),
                "authorized_action":
                    authority.authorized_action,
                "authorized_tool_identity":
                    authority.authorized_tool_identity,
            }

        def refuse(
            reason: str,
            *,
            consumed_before_override=None,
        ) -> ExecutionDecision:

            # One counter snapshot is used for both before/after.
            # Another worker may execute concurrently, but that
            # must not appear as consequence caused by this refusal.
            counter_snapshot = (
                presented_tool.consequence_counter
            )

            fields = authority_fields()

            if (
                consumed_before_override
                is not None
            ):
                fields[
                    "authority_consumed_before"
                ] = consumed_before_override

            return ExecutionDecision(
                attempt_index=attempt_index,
                display_sequence=display_sequence,
                attempt_id=attempt_id,
                attempt_class=attempt_class,
                presenter_identity=presenter_identity,
                requested_action=requested_action,
                presented_tool_identity=(
                    presented_tool.tool_identity
                ),
                verdict="REFUSE",
                reason=reason,
                consequence_before=counter_snapshot,
                consequence_after=counter_snapshot,
                consequence_delta=0,
                worker_thread_identity=worker_identity,
                **fields,
            )

        # 1. Authority presence
        if authority is None:

            return refuse(
                "EXECUTION_AUTHORITY_NOT_PRESENT"
            )

        # 2. Authority validity
        if authority.valid is not True:

            return refuse(
                "EXECUTION_AUTHORITY_INVALID"
            )

        # 3. Prior consumption
        if authority.consumed_snapshot():

            return refuse(
                "EXECUTION_AUTHORITY_ALREADY_CONSUMED",
                consumed_before_override=True,
            )

        # 4. Presenter identity binding
        if (
            presenter_identity
            != authority.subject_identity
        ):

            return refuse(
                "PRESENTER_IDENTITY_MISMATCH"
            )

        # 5. Action binding
        if (
            requested_action
            != authority.authorized_action
        ):

            return refuse(
                "EXECUTION_SCOPE_NOT_AUTHORIZED"
            )

        # 6. Tool binding
        if (
            presented_tool.tool_identity
            != authority.authorized_tool_identity
        ):

            return refuse(
                "TOOL_IDENTITY_MISMATCH"
            )

        # 7. Single-use consequential execution
        with authority._lock:

            consumed_before = authority.consumed

            if consumed_before:

                return refuse(
                    "EXECUTION_AUTHORITY_ALREADY_CONSUMED",
                    consumed_before_override=True,
                )

            before, after = (
                presented_tool.execute(
                    requested_action
                )
            )

            authority.consumed = True

            consumed_after = (
                authority.consumed
            )

        return ExecutionDecision(
            attempt_index=attempt_index,
            display_sequence=display_sequence,
            attempt_id=attempt_id,
            attempt_class=attempt_class,
            presenter_identity=presenter_identity,
            authority_present=True,
            authority_id=authority.authority_id,
            authority_subject_identity=(
                authority.subject_identity
            ),
            authority_valid=authority.valid,
            authority_consumed_before=(
                consumed_before
            ),
            authority_consumed_after=(
                consumed_after
            ),
            authorized_action=(
                authority.authorized_action
            ),
            requested_action=requested_action,
            authorized_tool_identity=(
                authority.authorized_tool_identity
            ),
            presented_tool_identity=(
                presented_tool.tool_identity
            ),
            verdict="PERMIT",
            reason="AUTHORIZED",
            consequence_before=before,
            consequence_after=after,
            consequence_delta=(
                after - before
            ),
            worker_thread_identity=worker_identity,
        )