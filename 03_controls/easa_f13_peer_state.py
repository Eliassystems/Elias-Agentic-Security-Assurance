from __future__ import annotations

from dataclasses import dataclass, asdict


PEER_STATE_SOURCE_ID = "PEER_STATE_SOURCE_F13"
PEER_ID = "PEER_B"

PEER_READY = "PEER_READY"
PEER_WITHDRAWN = "PEER_WITHDRAWN"

STATE_V1 = "PEER_B_STATE_V1"
STATE_V2 = "PEER_B_STATE_V2"
STATE_V3 = "PEER_B_STATE_V3"

TRANSITION_V1_V2 = "F13-TRANSITION-PEER-B-V1-V2"
TRANSITION_V2_V3 = "F13-TRANSITION-PEER-B-V2-V3"


@dataclass(frozen=True)
class PeerSnapshot:
    peer_id: str
    state_identity: str
    version: int
    standing: str
    admissible: bool


@dataclass(frozen=True)
class PeerTransition:
    transition_identity: str
    source_identity: str
    peer_id: str
    prior_state_identity: str
    resulting_state_identity: str
    prior_version: int
    resulting_version: int
    prior_standing: str
    resulting_standing: str
    prior_admissible: bool
    resulting_admissible: bool


class AuthoritativePeerStateSource:
    """
    EASA-F13 bounded authoritative peer-state source.

    Local snapshots are immutable copies. Advancing authoritative state
    never mutates an already-issued snapshot.
    """

    source_identity = PEER_STATE_SOURCE_ID

    def __init__(self) -> None:
        self._current_state = PeerSnapshot(
            peer_id=PEER_ID,
            state_identity=STATE_V1,
            version=1,
            standing=PEER_READY,
            admissible=True,
        )

    @property
    def current_state(self) -> PeerSnapshot:
        state = self._current_state

        return PeerSnapshot(
            peer_id=state.peer_id,
            state_identity=state.state_identity,
            version=state.version,
            standing=state.standing,
            admissible=state.admissible,
        )

    def capture_snapshot(self) -> PeerSnapshot:
        return self.current_state

    def snapshot_dict(self) -> dict:
        return asdict(self.current_state)

    def transition_v1_to_v2(self) -> PeerTransition:

        prior = self._current_state

        if (
            prior.peer_id != PEER_ID
            or prior.state_identity != STATE_V1
            or prior.version != 1
            or prior.standing != PEER_READY
            or prior.admissible is not True
        ):
            raise RuntimeError(
                "F13_V1_TO_V2_PRECONDITION_NOT_MET"
            )

        resulting = PeerSnapshot(
            peer_id=PEER_ID,
            state_identity=STATE_V2,
            version=2,
            standing=PEER_WITHDRAWN,
            admissible=False,
        )

        self._current_state = resulting

        return PeerTransition(
            transition_identity=TRANSITION_V1_V2,
            source_identity=self.source_identity,
            peer_id=PEER_ID,
            prior_state_identity=prior.state_identity,
            resulting_state_identity=resulting.state_identity,
            prior_version=prior.version,
            resulting_version=resulting.version,
            prior_standing=prior.standing,
            resulting_standing=resulting.standing,
            prior_admissible=prior.admissible,
            resulting_admissible=resulting.admissible,
        )

    def transition_v2_to_v3(self) -> PeerTransition:

        prior = self._current_state

        if (
            prior.peer_id != PEER_ID
            or prior.state_identity != STATE_V2
            or prior.version != 2
            or prior.standing != PEER_WITHDRAWN
            or prior.admissible is not False
        ):
            raise RuntimeError(
                "F13_V2_TO_V3_PRECONDITION_NOT_MET"
            )

        resulting = PeerSnapshot(
            peer_id=PEER_ID,
            state_identity=STATE_V3,
            version=3,
            standing=PEER_READY,
            admissible=True,
        )

        self._current_state = resulting

        return PeerTransition(
            transition_identity=TRANSITION_V2_V3,
            source_identity=self.source_identity,
            peer_id=PEER_ID,
            prior_state_identity=prior.state_identity,
            resulting_state_identity=resulting.state_identity,
            prior_version=prior.version,
            resulting_version=resulting.version,
            prior_standing=prior.standing,
            resulting_standing=resulting.standing,
            prior_admissible=prior.admissible,
            resulting_admissible=resulting.admissible,
        )