from __future__ import annotations

import threading
from dataclasses import dataclass
from typing import Optional


F16_ACTION = "F16_BOUNDED_SCALE_WRITE"

F16_PRIMARY_TOOL = "TOOL_F16_PRIMARY"

F16_OTHER_TOOL = "TOOL_F16_OTHER"


@dataclass
class ExecutionAuthority:

    authority_id: str

    subject_identity: str

    authorized_action: str

    authorized_tool_identity: str

    valid: bool = True

    consumed: bool = False


class ConsequentialTool:

    def __init__(
        self,
        tool_identity: str,
    ) -> None:

        if tool_identity not in {
            F16_PRIMARY_TOOL,
            F16_OTHER_TOOL,
        }:
            raise ValueError(
                "F16_TOOL_IDENTITY_NOT_FROZEN"
            )

        self.tool_identity = (
            tool_identity
        )

        self._counter = 0

        self._lock = (
            threading.Lock()
        )

    @property
    def consequence_counter(
        self,
    ) -> int:

        with self._lock:

            return self._counter

    def execute(
        self,
        action: str,
    ) -> tuple[int, int]:

        if action != F16_ACTION:

            raise RuntimeError(
                "F16_ACTION_NOT_SUPPORTED"
            )

        with self._lock:

            before = self._counter

            self._counter += 1

            after = self._counter

            return before, after


@dataclass(frozen=True)
class ExecutionDecision:

    threshold: int

    attempt_index: int

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

    authorized_tool_identity: Optional[str]

    requested_action: str

    presented_tool_identity: str

    verdict: str

    reason: str

    consequence_before: int

    consequence_after: int

    consequence_delta: int

    worker_thread_identity: str


class F16ExecutionGate:

    def attempt(
        self,
        *,
        threshold: int,
        attempt_index: int,
        attempt_id: str,
        attempt_class: str,
        presenter_identity: str,
        authority: Optional[
            ExecutionAuthority
        ],
        requested_action: str,
        presented_tool: ConsequentialTool,
    ) -> ExecutionDecision:

        worker_identity = (
            f"{threading.current_thread().name}:"
            f"{threading.get_ident()}"
        )

        if authority is None:

            before = (
                presented_tool
                .consequence_counter
            )

            return ExecutionDecision(
                threshold=threshold,
                attempt_index=attempt_index,
                attempt_id=attempt_id,
                attempt_class=attempt_class,
                presenter_identity=(
                    presenter_identity
                ),
                authority_present=False,
                authority_id=None,
                authority_subject_identity=None,
                authority_valid=None,
                authority_consumed_before=None,
                authority_consumed_after=None,
                authorized_action=None,
                authorized_tool_identity=None,
                requested_action=(
                    requested_action
                ),
                presented_tool_identity=(
                    presented_tool
                    .tool_identity
                ),
                verdict="REFUSE",
                reason=(
                    "EXECUTION_AUTHORITY_NOT_PRESENT"
                ),
                consequence_before=before,
                consequence_after=before,
                consequence_delta=0,
                worker_thread_identity=(
                    worker_identity
                ),
            )

        consumed_before = (
            authority.consumed
        )

        def refuse(
            reason: str,
        ) -> ExecutionDecision:

            before = (
                presented_tool
                .consequence_counter
            )

            return ExecutionDecision(
                threshold=threshold,
                attempt_index=attempt_index,
                attempt_id=attempt_id,
                attempt_class=attempt_class,
                presenter_identity=(
                    presenter_identity
                ),
                authority_present=True,
                authority_id=(
                    authority.authority_id
                ),
                authority_subject_identity=(
                    authority.subject_identity
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
                authorized_action=(
                    authority.authorized_action
                ),
                authorized_tool_identity=(
                    authority
                    .authorized_tool_identity
                ),
                requested_action=(
                    requested_action
                ),
                presented_tool_identity=(
                    presented_tool
                    .tool_identity
                ),
                verdict="REFUSE",
                reason=reason,
                consequence_before=before,
                consequence_after=before,
                consequence_delta=0,
                worker_thread_identity=(
                    worker_identity
                ),
            )

        if authority.valid is not True:

            return refuse(
                "EXECUTION_AUTHORITY_INVALID"
            )

        if (
            presenter_identity
            != authority.subject_identity
        ):

            return refuse(
                "PRESENTER_IDENTITY_MISMATCH"
            )

        if (
            requested_action
            != authority.authorized_action
        ):

            return refuse(
                "EXECUTION_SCOPE_NOT_AUTHORIZED"
            )

        if (
            presented_tool.tool_identity
            != authority.authorized_tool_identity
        ):

            return refuse(
                "TOOL_IDENTITY_MISMATCH"
            )

        if authority.consumed:

            return refuse(
                "EXECUTION_AUTHORITY_ALREADY_CONSUMED"
            )

        before, after = (
            presented_tool.execute(
                requested_action
            )
        )

        authority.consumed = True

        return ExecutionDecision(
            threshold=threshold,
            attempt_index=attempt_index,
            attempt_id=attempt_id,
            attempt_class=attempt_class,
            presenter_identity=(
                presenter_identity
            ),
            authority_present=True,
            authority_id=(
                authority.authority_id
            ),
            authority_subject_identity=(
                authority.subject_identity
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
            authorized_action=(
                authority.authorized_action
            ),
            authorized_tool_identity=(
                authority
                .authorized_tool_identity
            ),
            requested_action=(
                requested_action
            ),
            presented_tool_identity=(
                presented_tool
                .tool_identity
            ),
            verdict="PERMIT",
            reason="AUTHORIZED",
            consequence_before=before,
            consequence_after=after,
            consequence_delta=(
                after - before
            ),
            worker_thread_identity=(
                worker_identity
            ),
        )