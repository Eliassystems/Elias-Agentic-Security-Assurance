from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import asdict, dataclass
from threading import Lock
from typing import Any


def canonical_json(
    value: dict[str, Any],
) -> str:

    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    )


def decision_digest(
    payload: dict[str, Any],
) -> str:

    return hashlib.sha256(
        canonical_json(payload).encode("utf-8")
    ).hexdigest().upper()


@dataclass(frozen=True)
class WitnessReceipt:
    witness_id: str
    attempt_id: str
    decision_id: str
    decision_digest: str


class ConcurrentWitnessStore:

    def __init__(self) -> None:

        self._lock = Lock()

        self._submitted_count = 0
        self._accepted_count = 0
        self._duplicate_rejection_count = 0

        self._records_by_attempt: dict[str, dict] = {}
        self._attempt_for_decision: dict[str, str] = {}
        self._attempt_for_witness: dict[str, str] = {}

        self._completion_order: list[str] = []

    def submit(
        self,
        chain: dict,
    ) -> bool:

        attempt_id = chain["attempt"]["attempt_id"]
        decision_id = chain["decision"]["decision_id"]
        witness_id = chain["witness"]["witness_id"]

        with self._lock:

            self._submitted_count += 1

            collision = (
                attempt_id in self._records_by_attempt
                or
                decision_id in self._attempt_for_decision
                or
                witness_id in self._attempt_for_witness
            )

            if collision:

                self._duplicate_rejection_count += 1

                return False

            self._records_by_attempt[
                attempt_id
            ] = deepcopy(chain)

            self._attempt_for_decision[
                decision_id
            ] = attempt_id

            self._attempt_for_witness[
                witness_id
            ] = attempt_id

            self._completion_order.append(
                attempt_id
            )

            self._accepted_count += 1

            return True

    def snapshot(self) -> dict:

        with self._lock:

            records = [
                deepcopy(
                    self._records_by_attempt[attempt_id]
                )
                for attempt_id
                in sorted(self._records_by_attempt.keys())
            ]

            return {
                "submitted_count":
                    self._submitted_count,

                "accepted_count":
                    self._accepted_count,

                "duplicate_rejection_count":
                    self._duplicate_rejection_count,

                "decision_record_count":
                    len(self._attempt_for_decision),

                "witness_receipt_count":
                    len(self._attempt_for_witness),

                "unique_attempt_count":
                    len(self._records_by_attempt),

                "unique_decision_count":
                    len(self._attempt_for_decision),

                "unique_witness_count":
                    len(self._attempt_for_witness),

                "completion_order":
                    list(self._completion_order),

                "records":
                    records,
            }


def make_witness(
    *,
    witness_id: str,
    attempt_id: str,
    decision_id: str,
    digest: str,
) -> WitnessReceipt:

    return WitnessReceipt(
        witness_id=witness_id,
        attempt_id=attempt_id,
        decision_id=decision_id,
        decision_digest=digest,
    )


def witness_dict(
    receipt: WitnessReceipt,
) -> dict:

    return asdict(receipt)