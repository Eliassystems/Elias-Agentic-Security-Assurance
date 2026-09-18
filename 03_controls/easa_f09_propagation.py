from __future__ import annotations

from dataclasses import dataclass

from easa_f09_control import LocalNodeState, RevocationEvent


RECEIPT_IDS = {
    "NODE_A": "F09-RECEIPT-NODE-A",
    "NODE_B": "F09-RECEIPT-NODE-B",
    "NODE_C": "F09-RECEIPT-NODE-C",
}


@dataclass(frozen=True)
class PropagationReceipt:
    receipt_id: str
    node_id: str
    revocation_event_id: str
    prior_local_epoch: int
    resulting_local_epoch: int
    revoked_epoch: int
    revoked_epoch_recorded: bool
    event_recorded: bool
    application_status: str
    acknowledgement_status: str


class RevocationPropagator:
    """
    Bounded F09 propagation mechanism.

    Each call updates exactly one supplied LocalNodeState object and emits
    one acknowledgement receipt for that node.
    """

    def deliver(
        self,
        *,
        event: RevocationEvent,
        node_state: LocalNodeState,
    ) -> PropagationReceipt:

        if node_state.node_id not in RECEIPT_IDS:
            raise ValueError("UNKNOWN_NODE_ID")

        prior = node_state.current_epoch

        if prior != event.prior_epoch:
            raise ValueError("LOCAL_PRIOR_EPOCH_MISMATCH")

        if event.new_epoch <= event.prior_epoch:
            raise ValueError("LOCAL_EPOCH_NOT_ADVANCED")

        node_state.current_epoch = event.new_epoch
        node_state.revoked_epochs.add(event.revoked_epoch)
        node_state.last_applied_revocation_event = event.event_id

        return PropagationReceipt(
            receipt_id=RECEIPT_IDS[node_state.node_id],
            node_id=node_state.node_id,
            revocation_event_id=event.event_id,
            prior_local_epoch=prior,
            resulting_local_epoch=node_state.current_epoch,
            revoked_epoch=event.revoked_epoch,
            revoked_epoch_recorded=(
                event.revoked_epoch
                in node_state.revoked_epochs
            ),
            event_recorded=(
                node_state.last_applied_revocation_event
                == event.event_id
            ),
            application_status="APPLIED",
            acknowledgement_status="ACKNOWLEDGED",
        )