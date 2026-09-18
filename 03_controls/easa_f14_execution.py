from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Optional


AUTHORITY_SOURCE_ID = "AUTHORITY_SOURCE_F14"
F14_ACTION = "F14_WRITE"
F14_TOOL = "TOOL_F14"


@dataclass
class ExecutionAuthority:
    artifact_type: str
    authority_id: str
    issuer_identity: str
    subject_identity: str
    authorized_action: str
    bound_tool_identity: str
    valid: bool = True
    consumed: bool = False


class F14AuthoritySource:
    """
    Issues six independent authorities prospectively.

    No two permitted attempts share one authority.
    """

    source_identity = AUTHORITY_SOURCE_ID

    def __init__(self) -> None:
        self._issued: dict[str, ExecutionAuthority] = {}

    def issue(
        self,
        *,
        authority_id: str,
        subject_identity: str,
    ) -> ExecutionAuthority:

        if authority_id in self._issued:
            raise RuntimeError(
                f"AUTHORITY_ALREADY_ISSUED::{authority_id}"
            )

        authority = ExecutionAuthority(
            artifact_type="EXECUTION_AUTHORITY",
            authority_id=authority_id,
            issuer_identity=self.source_identity,
            subject_identity=subject_identity,
            authorized_action=F14_ACTION,
            bound_tool_identity=F14_TOOL,
            valid=True,
            consumed=False,
        )

        self._issued[authority_id] = authority

        return authority

    @property
    def issued_ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._issued.keys()))


class ConsequentialTool:
    """
    One bounded shared tool.

    Its counter mutation is protected so per-decision consequence
    attribution remains exact under concurrent permitted executions.
    """

    def __init__(self) -> None:
        self.tool_identity = F14_TOOL
        self._counter = 0
        self._lock = Lock()

    @property
    def consequence_counter(self) -> int:
        with self._lock:
            return self._counter

    def snapshot(self) -> int:
        with self._lock:
            return self._counter

    def execute(self, action: str) -> tuple[int, int]:

        if action != F14_ACTION:
            raise ValueError("ACTION_NOT_SUPPORTED_BY_TOOL")

        with self._lock:

            before = self._counter
            self._counter += 1
            after = self._counter

            return before, after


@dataclass(frozen=True)
class ExecutionDecision:
    attempt_id: str
    decision_id: str
    presenter_identity: str
    authority_id: Optional[str]
    authority_issuer_identity: Optional[str]
    action: str
    tool_identity: str

    verdict: str
    reason: str

    authority_consumed_before: Optional[bool]
    authority_consumed_after: Optional[bool]

    consequence_before: int
    consequence_after: int
    consequence_delta: int


class F14ExecutionGate:

    expected_authority_source_identity = AUTHORITY_SOURCE_ID

    def attempt(
        self,
        *,
        attempt_id: str,
        decision_id: str,
        presenter_identity: str,
        authority: Optional[ExecutionAuthority],
        action: str,
        tool: ConsequentialTool,
    ) -> ExecutionDecision:

        if authority is None:

            before = tool.snapshot()

            return ExecutionDecision(
                attempt_id=attempt_id,
                decision_id=decision_id,
                presenter_identity=presenter_identity,
                authority_id=None,
                authority_issuer_identity=None,
                action=action,
                tool_identity=tool.tool_identity,
                verdict="REFUSE",
                reason="EXECUTION_AUTHORITY_NOT_PRESENT",
                authority_consumed_before=None,
                authority_consumed_after=None,
                consequence_before=before,
                consequence_after=before,
                consequence_delta=0,
            )

        consumed_before = authority.consumed

        def refuse(reason: str) -> ExecutionDecision:

            before = tool.snapshot()

            return ExecutionDecision(
                attempt_id=attempt_id,
                decision_id=decision_id,
                presenter_identity=presenter_identity,
                authority_id=authority.authority_id,
                authority_issuer_identity=authority.issuer_identity,
                action=action,
                tool_identity=tool.tool_identity,
                verdict="REFUSE",
                reason=reason,
                authority_consumed_before=consumed_before,
                authority_consumed_after=authority.consumed,
                consequence_before=before,
                consequence_after=before,
                consequence_delta=0,
            )

        if (
            authority.issuer_identity
            != self.expected_authority_source_identity
        ):
            return refuse(
                "EXECUTION_AUTHORITY_ISSUER_NOT_AUTHORIZED"
            )

        if not authority.valid:
            return refuse(
                "EXECUTION_AUTHORITY_INVALID"
            )

        if authority.consumed:
            return refuse(
                "EXECUTION_AUTHORITY_ALREADY_CONSUMED"
            )

        if presenter_identity != authority.subject_identity:
            return refuse(
                "PRESENTER_IDENTITY_MISMATCH"
            )

        if action != authority.authorized_action:
            return refuse(
                "EXECUTION_SCOPE_NOT_AUTHORIZED"
            )

        if tool.tool_identity != authority.bound_tool_identity:
            return refuse(
                "TOOL_IDENTITY_MISMATCH"
            )

        before, after = tool.execute(action)

        authority.consumed = True

        return ExecutionDecision(
            attempt_id=attempt_id,
            decision_id=decision_id,
            presenter_identity=presenter_identity,
            authority_id=authority.authority_id,
            authority_issuer_identity=authority.issuer_identity,
            action=action,
            tool_identity=tool.tool_identity,
            verdict="PERMIT",
            reason="AUTHORIZED",
            authority_consumed_before=consumed_before,
            authority_consumed_after=authority.consumed,
            consequence_before=before,
            consequence_after=after,
            consequence_delta=after - before,
        )