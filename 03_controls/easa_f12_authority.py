from __future__ import annotations

from dataclasses import dataclass


AUTHORITY_SOURCE_ID = "AUTHORITY_SOURCE_F12"

F12_EXECUTOR = "EXECUTOR_F12"
F12_ACTION = "F12_PRIVILEGED_WRITE"
F12_TOOL = "TOOL_F12"


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


class AuthoritativeExecutionSource:
    """
    EASA-F12 authoritative execution source.

    This object is separate from the advisory resolver.

    It is the only bounded F12 component permitted to issue
    ExecutionAuthority.
    """

    source_identity = AUTHORITY_SOURCE_ID

    def __init__(self) -> None:
        self._issued_authority_ids: list[str] = []

    @property
    def issued_authority_ids(self) -> tuple[str, ...]:
        return tuple(self._issued_authority_ids)

    @property
    def issued_count(self) -> int:
        return len(self._issued_authority_ids)

    def issue_positive_authority(self) -> ExecutionAuthority:

        authority_id = "AUTH_F12_POS"

        if authority_id in self._issued_authority_ids:
            raise RuntimeError(
                "AUTH_F12_POS_ALREADY_ISSUED"
            )

        authority = ExecutionAuthority(
            artifact_type="EXECUTION_AUTHORITY",
            authority_id=authority_id,
            issuer_identity=self.source_identity,
            subject_identity=F12_EXECUTOR,
            authorized_action=F12_ACTION,
            bound_tool_identity=F12_TOOL,
            valid=True,
            consumed=False,
        )

        self._issued_authority_ids.append(
            authority.authority_id
        )

        return authority