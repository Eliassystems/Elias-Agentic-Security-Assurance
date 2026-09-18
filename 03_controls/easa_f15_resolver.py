from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Optional


STATE_SOURCE_ID = "STATE_SOURCE_F15"

RESOLVER_A_ID = "RESOLVER_F15_A"
RESOLVER_B_ID = "RESOLVER_F15_B"


@dataclass(frozen=True)
class GoverningState:
    state_version: str
    state: str
    admissible: bool


@dataclass(frozen=True)
class ResolverView:
    resolver_identity: str
    available: bool
    state_version: Optional[str]
    state: Optional[str]
    admissible: Optional[bool]


class AuthoritativeStateSource:

    source_identity = STATE_SOURCE_ID

    def __init__(self) -> None:

        self._current = GoverningState(
            state_version="R1",
            state="READY",
            admissible=True,
        )

    @property
    def current(self) -> GoverningState:
        return self._current

    def snapshot(self) -> dict:
        return asdict(self._current)

    def transition(
        self,
        *,
        expected_from_version: str,
        to_version: str,
        to_state: str,
        to_admissible: bool,
    ) -> dict:

        before = self._current

        if (
            before.state_version
            != expected_from_version
        ):
            raise RuntimeError(
                "F15_UNEXPECTED_AUTHORITATIVE_TRANSITION_SOURCE"
            )

        allowed = {
            (
                "R1",
                "R2",
                "WITHDRAWN",
                False,
            ),
            (
                "R2",
                "R3",
                "READY",
                True,
            ),
        }

        transition_tuple = (
            expected_from_version,
            to_version,
            to_state,
            to_admissible,
        )

        if transition_tuple not in allowed:
            raise RuntimeError(
                "F15_TRANSITION_NOT_IN_FROZEN_DEFINITION"
            )

        self._current = GoverningState(
            state_version=to_version,
            state=to_state,
            admissible=to_admissible,
        )

        return {
            "source_identity":
                self.source_identity,

            "before":
                asdict(before),

            "after":
                asdict(self._current),
        }


class ResolverReplica:

    def __init__(
        self,
        resolver_identity: str,
    ) -> None:

        if resolver_identity not in {
            RESOLVER_A_ID,
            RESOLVER_B_ID,
        }:
            raise ValueError(
                "F15_RESOLVER_IDENTITY_NOT_FROZEN"
            )

        self.resolver_identity = (
            resolver_identity
        )

        self._available = True
        self._view: Optional[
            GoverningState
        ] = None

    def synchronize(
        self,
        source: AuthoritativeStateSource,
    ) -> None:

        current = source.current

        self._available = True

        self._view = GoverningState(
            state_version=(
                current.state_version
            ),
            state=current.state,
            admissible=current.admissible,
        )

    def set_unavailable(self) -> None:

        self._available = False

    def force_view(
        self,
        *,
        state_version: str,
        state: str,
        admissible: bool,
    ) -> None:

        allowed_views = {
            ("R1", "READY", True),
            ("R2", "WITHDRAWN", False),
            ("R3", "READY", True),
        }

        candidate = (
            state_version,
            state,
            admissible,
        )

        if candidate not in allowed_views:
            raise RuntimeError(
                "F15_RESOLVER_VIEW_NOT_IN_FROZEN_DEFINITION"
            )

        self._available = True

        self._view = GoverningState(
            state_version=state_version,
            state=state,
            admissible=admissible,
        )

    def observe(self) -> ResolverView:

        if not self._available:

            return ResolverView(
                resolver_identity=(
                    self.resolver_identity
                ),
                available=False,
                state_version=None,
                state=None,
                admissible=None,
            )

        if self._view is None:

            return ResolverView(
                resolver_identity=(
                    self.resolver_identity
                ),
                available=True,
                state_version=None,
                state=None,
                admissible=None,
            )

        return ResolverView(
            resolver_identity=(
                self.resolver_identity
            ),
            available=True,
            state_version=(
                self._view.state_version
            ),
            state=self._view.state,
            admissible=(
                self._view.admissible
            ),
        )