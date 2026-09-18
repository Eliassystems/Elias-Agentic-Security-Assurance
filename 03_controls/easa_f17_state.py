from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GoverningState:
    epoch: int
    state: str
    admissible: bool


@dataclass(frozen=True)
class PeerStateView:
    epoch: int
    state: str
    admissible: bool


@dataclass(frozen=True)
class ResolverView:
    resolver_id: str
    available: bool
    epoch: int | None
    state: str | None
    admissible: bool | None


class AuthoritativeStateSource:

    _FROZEN_STATES = {
        1: GoverningState(
            epoch=1,
            state="READY",
            admissible=True,
        ),
        2: GoverningState(
            epoch=2,
            state="WITHDRAWN",
            admissible=False,
        ),
        3: GoverningState(
            epoch=3,
            state="READY",
            admissible=True,
        ),
    }

    def __init__(self) -> None:
        self._current = self._FROZEN_STATES[1]

    def snapshot(self) -> GoverningState:
        return self._current

    def transition_to(
        self,
        epoch: int,
    ) -> tuple[GoverningState, GoverningState]:

        before = self._current

        allowed = {
            1: 2,
            2: 3,
        }

        expected = allowed.get(
            before.epoch
        )

        if epoch != expected:
            raise RuntimeError(
                "F17_INVALID_AUTHORITATIVE_TRANSITION"
            )

        after = self._FROZEN_STATES[
            epoch
        ]

        self._current = after

        return before, after


class ResolverReplica:

    _FROZEN_IDS = {
        "RESOLVER_F17_A",
        "RESOLVER_F17_B",
    }

    def __init__(
        self,
        resolver_id: str,
    ) -> None:

        if resolver_id not in self._FROZEN_IDS:
            raise ValueError(
                "F17_RESOLVER_ID_NOT_FROZEN"
            )

        self.resolver_id = resolver_id

        self._view = ResolverView(
            resolver_id=resolver_id,
            available=False,
            epoch=None,
            state=None,
            admissible=None,
        )

    def observe(self) -> ResolverView:
        return self._view

    def synchronize(
        self,
        governing_state: GoverningState,
    ) -> ResolverView:

        self._view = ResolverView(
            resolver_id=self.resolver_id,
            available=True,
            epoch=governing_state.epoch,
            state=governing_state.state,
            admissible=governing_state.admissible,
        )

        return self._view

    def unavailable(self) -> ResolverView:

        self._view = ResolverView(
            resolver_id=self.resolver_id,
            available=False,
            epoch=None,
            state=None,
            admissible=None,
        )

        return self._view

    def force_view(
        self,
        *,
        epoch: int,
        state: str,
        admissible: bool,
    ) -> ResolverView:

        if epoch not in {1, 2, 3}:
            raise ValueError(
                "F17_RESOLVER_EPOCH_NOT_FROZEN"
            )

        if state not in {
            "READY",
            "WITHDRAWN",
        }:
            raise ValueError(
                "F17_RESOLVER_STATE_NOT_FROZEN"
            )

        self._view = ResolverView(
            resolver_id=self.resolver_id,
            available=True,
            epoch=epoch,
            state=state,
            admissible=admissible,
        )

        return self._view