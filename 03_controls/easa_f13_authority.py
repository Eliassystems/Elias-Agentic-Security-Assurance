from __future__ import annotations

from dataclasses import dataclass


AUTHORITY_SOURCE_ID = "AUTHORITY_SOURCE_F13"

F13_AGENT = "AGENT_A"
F13_ACTION = "F13_PEER_DEPENDENT_WRITE"
F13_TOOL = "TOOL_F13"


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


class F13AuthoritySource:
    """
    Bounded EASA-F13 authority source.

    Execution authorities intentionally contain no peer-state version,
    peer standing, peer state identity, or freshness field.

    Peer-state freshness is therefore a separate governing input.
    """

    source_identity = AUTHORITY_SOURCE_ID

    ALLOWED_IDS = frozenset(
        {
            "AUTH_F13_PRE",
            "AUTH_F13_STALE_VIEW",
            "AUTH_F13_CURRENT_BLOCKED",
            "AUTH_F13_RECOVERY",
        }
    )

    def __init__(self) -> None:
        self._issued_ids: list[str] = []

    @property
    def issued_ids(self) -> tuple[str, ...]:
        return tuple(self._issued_ids)

    @property
    def issued_count(self) -> int:
        return len(self._issued_ids)

    def issue(self, authority_id: str) -> ExecutionAuthority:

        if authority_id not in self.ALLOWED_IDS:
            raise ValueError("UNSUPPORTED_F13_AUTHORITY_ID")

        if authority_id in self._issued_ids:
            raise RuntimeError(
                f"F13_AUTHORITY_ALREADY_ISSUED::{authority_id}"
            )

        authority = ExecutionAuthority(
            artifact_type="EXECUTION_AUTHORITY",
            authority_id=authority_id,
            issuer_identity=self.source_identity,
            subject_identity=F13_AGENT,
            authorized_action=F13_ACTION,
            bound_tool_identity=F13_TOOL,
            valid=True,
            consumed=False,
        )

        self._issued_ids.append(authority_id)

        return authority