from __future__ import annotations

import json
import sys
import threading
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = ROOT / "03_controls"

if str(CONTROL_DIR) not in sys.path:
    sys.path.insert(0, str(CONTROL_DIR))


from easa_f14_execution import (  # noqa: E402
    F14_ACTION,
    F14_TOOL,
    ConsequentialTool,
    F14AuthoritySource,
    F14ExecutionGate,
)
from easa_f14_witness import (  # noqa: E402
    ConcurrentWitnessStore,
    decision_digest,
    make_witness,
    witness_dict,
)


EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F14"

POPULATION_PATH = (
    EVIDENCE_DIR / "EASA-F14-POPULATION.json"
)

STORE_PATH = (
    EVIDENCE_DIR / "EASA-F14-WITNESS-STORE.json"
)

RECONSTRUCTION_PATH = (
    EVIDENCE_DIR / "EASA-F14-RECONSTRUCTION.json"
)

SUMMARY_PATH = (
    EVIDENCE_DIR / "EASA-F14-SUMMARY.json"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(
    path: Path,
    value: dict,
) -> None:

    path.write_text(
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )


def identifier(
    prefix: str,
    number: int,
) -> str:

    return f"{prefix}-{number:02d}"


def build_attempt_population() -> list[dict]:

    attempts: list[dict] = []

    for number in range(1, 13):

        is_permitted = (
            number % 2 == 1
        )

        attempt_id = identifier(
            "F14-ATTEMPT",
            number,
        )

        decision_id = identifier(
            "F14-DECISION",
            number,
        )

        witness_id = identifier(
            "F14-WITNESS",
            number,
        )

        presenter_identity = identifier(
            "AGENT_F14",
            number,
        )

        authority_id = (
            identifier(
                "AUTH_F14",
                number,
            )
            if is_permitted
            else None
        )

        attempts.append(
            {
                "attempt_number":
                    number,

                "attempt_id":
                    attempt_id,

                "decision_id":
                    decision_id,

                "witness_id":
                    witness_id,

                "presenter_identity":
                    presenter_identity,

                "authority_id":
                    authority_id,

                "action":
                    F14_ACTION,

                "tool_identity":
                    F14_TOOL,

                "expected_verdict":
                    (
                        "PERMIT"
                        if is_permitted
                        else "REFUSE"
                    ),

                "expected_reason":
                    (
                        "AUTHORIZED"
                        if is_permitted
                        else
                        "EXECUTION_AUTHORITY_NOT_PRESENT"
                    ),

                "expected_consequence_delta":
                    1 if is_permitted else 0,
            }
        )

    return attempts


def canonical_decision_payload(
    decision: dict,
) -> dict:

    return {
        "attempt_id":
            decision["attempt_id"],

        "decision_id":
            decision["decision_id"],

        "presenter_identity":
            decision["presenter_identity"],

        "authority_id":
            decision["authority_id"],

        "action":
            decision["action"],

        "tool_identity":
            decision["tool_identity"],

        "verdict":
            decision["verdict"],

        "reason":
            decision["reason"],

        "consequence_delta":
            decision["consequence_delta"],
    }


def main() -> int:

    evidence_targets = (
        POPULATION_PATH,
        STORE_PATH,
        RECONSTRUCTION_PATH,
        SUMMARY_PATH,
    )

    existing = [
        str(path)
        for path in evidence_targets
        if path.exists()
    ]

    if existing:

        print(
            "FIRST OBSERVATION EVIDENCE ALREADY EXISTS — STOP"
        )

        for path in existing:
            print(path)

        return 2

    EVIDENCE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    observation_time = now_utc()

    attempts = build_attempt_population()

    authority_source = F14AuthoritySource()

    authorities = {}

    for attempt in attempts:

        authority_id = attempt["authority_id"]

        if authority_id is None:
            continue

        authorities[authority_id] = (
            authority_source.issue(
                authority_id=authority_id,
                subject_identity=(
                    attempt["presenter_identity"]
                ),
            )
        )

    population_record = {
        "examination":
            "EASA-F14",

        "record_type":
            "PROSPECTIVE_POPULATION",

        "observation_time_utc":
            observation_time,

        "attempt_count":
            len(attempts),

        "attempts":
            attempts,

        "issued_authority_ids":
            list(authority_source.issued_ids),

        "expected_permit_count":
            6,

        "expected_refuse_count":
            6,

        "expected_final_tool_counter":
            6,

        "execution_started":
            False,
    }

    write_json(
        POPULATION_PATH,
        population_record,
    )

    gate = F14ExecutionGate()
    tool = ConsequentialTool()
    witness_store = ConcurrentWitnessStore()

    # ========================================================
    # FROZEN START SYNCHRONIZATION
    # 12 workers + main thread = 13 barrier parties.
    #
    # The barrier action executes only when every party has
    # arrived and immediately before release.
    # ========================================================

    ready_condition = threading.Condition()
    worker_error_lock = threading.Lock()

    workers_ready = 0
    start_release = False
    barrier_action_count = 0

    worker_errors: list[dict] = []

    def barrier_action() -> None:

        nonlocal start_release
        nonlocal barrier_action_count

        with ready_condition:

            barrier_action_count += 1

            if workers_ready != 12:
                raise RuntimeError(
                    "F14_BARRIER_RELEASE_BEFORE_12_WORKERS_READY"
                )

            start_release = True

    start_barrier = threading.Barrier(
        parties=13,
        action=barrier_action,
    )

    def worker(
        attempt: dict,
    ) -> None:

        nonlocal workers_ready

        try:

            authority_id = attempt["authority_id"]

            authority = (
                authorities[authority_id]
                if authority_id is not None
                else None
            )

            with ready_condition:

                workers_ready += 1

                ready_condition.notify_all()

            start_barrier.wait(
                timeout=30,
            )

            decision = gate.attempt(
                attempt_id=attempt["attempt_id"],
                decision_id=attempt["decision_id"],
                presenter_identity=(
                    attempt["presenter_identity"]
                ),
                authority=authority,
                action=attempt["action"],
                tool=tool,
            )

            decision_dict = asdict(
                decision
            )

            digest_payload = (
                canonical_decision_payload(
                    decision_dict
                )
            )

            digest = decision_digest(
                digest_payload
            )

            witness = make_witness(
                witness_id=attempt["witness_id"],
                attempt_id=attempt["attempt_id"],
                decision_id=attempt["decision_id"],
                digest=digest,
            )

            chain = {
                "attempt":
                    dict(attempt),

                "decision":
                    decision_dict,

                "canonical_decision_payload":
                    digest_payload,

                "decision_digest":
                    digest,

                "witness":
                    witness_dict(witness),
            }

            accepted = witness_store.submit(
                chain
            )

            if not accepted:
                raise RuntimeError(
                    "F14_UNEXPECTED_EVIDENCE_COLLISION"
                )

        except BaseException as exc:

            with worker_error_lock:

                worker_errors.append(
                    {
                        "attempt_id":
                            attempt["attempt_id"],

                        "exception_type":
                            type(exc).__name__,

                        "exception_message":
                            str(exc),
                    }
                )

    threads = [
        threading.Thread(
            target=worker,
            args=(attempt,),
            name=attempt["attempt_id"],
        )
        for attempt in attempts
    ]

    for thread in threads:
        thread.start()

    # Wait until every worker reports itself at the common
    # synchronization boundary before main enters the barrier.

    with ready_condition:

        all_ready = ready_condition.wait_for(
            lambda: workers_ready == 12,
            timeout=30,
        )

    if not all_ready:

        try:
            start_barrier.abort()
        except BaseException:
            pass

        for thread in threads:
            thread.join(timeout=5)

        worker_errors.append(
            {
                "attempt_id":
                    "HARNESS",
                "exception_type":
                    "StartBarrierTimeout",
                "exception_message":
                    (
                        f"workers_ready={workers_ready}"
                    ),
            }
        )

    else:

        try:

            start_barrier.wait(
                timeout=30,
            )

        except BaseException as exc:

            with worker_error_lock:

                worker_errors.append(
                    {
                        "attempt_id":
                            "HARNESS",
                        "exception_type":
                            type(exc).__name__,
                        "exception_message":
                            str(exc),
                    }
                )

    for thread in threads:
        thread.join(timeout=30)

    still_alive = [
        thread.name
        for thread in threads
        if thread.is_alive()
    ]

    for thread_name in still_alive:

        worker_errors.append(
            {
                "attempt_id":
                    thread_name,
                "exception_type":
                    "WorkerJoinTimeout",
                "exception_message":
                    "THREAD_STILL_ALIVE_AFTER_JOIN_TIMEOUT",
            }
        )

    store_snapshot = witness_store.snapshot()

    store_record = {
        "examination":
            "EASA-F14",

        "record_type":
            "CONCURRENT_WITNESS_STORE_SNAPSHOT",

        "observation_time_utc":
            observation_time,

        "workers_expected":
            12,

        "workers_ready_before_release":
            workers_ready,

        "barrier_parties":
            13,

        "barrier_action_count":
            barrier_action_count,

        "start_release":
            start_release,

        "worker_exception_count":
            len(worker_errors),

        "worker_exceptions":
            worker_errors,

        "tool_final_counter":
            tool.consequence_counter,

        **store_snapshot,
    }

    write_json(
        STORE_PATH,
        store_record,
    )

    # ========================================================
    # RECONSTRUCTION
    # ========================================================

    records_by_attempt = {
        record["attempt"]["attempt_id"]:
            record
        for record in store_snapshot["records"]
    }

    digest_mismatches = []
    attribution_mismatches = []
    missing_attempts = []
    reconstructed_chains = []

    permit_count = 0
    refuse_count = 0
    reconstructed_delta = 0

    for expected in attempts:

        attempt_id = expected["attempt_id"]

        record = records_by_attempt.get(
            attempt_id
        )

        if record is None:

            missing_attempts.append(
                attempt_id
            )

            continue

        decision = record["decision"]
        witness = record["witness"]

        recomputed_payload = (
            canonical_decision_payload(
                decision
            )
        )

        recomputed_digest = (
            decision_digest(
                recomputed_payload
            )
        )

        digest_matches = (
            record["decision_digest"]
            == recomputed_digest
            == witness["decision_digest"]
        )

        if not digest_matches:

            digest_mismatches.append(
                attempt_id
            )

        expected_mapping_matches = (
            decision["attempt_id"]
            == expected["attempt_id"]
            and
            decision["decision_id"]
            == expected["decision_id"]
            and
            decision["presenter_identity"]
            == expected["presenter_identity"]
            and
            decision["authority_id"]
            == expected["authority_id"]
            and
            decision["action"]
            == expected["action"]
            and
            decision["tool_identity"]
            == expected["tool_identity"]
            and
            decision["verdict"]
            == expected["expected_verdict"]
            and
            decision["reason"]
            == expected["expected_reason"]
            and
            decision["consequence_delta"]
            == expected[
                "expected_consequence_delta"
            ]
            and
            witness["witness_id"]
            == expected["witness_id"]
            and
            witness["attempt_id"]
            == expected["attempt_id"]
            and
            witness["decision_id"]
            == expected["decision_id"]
        )

        if not expected_mapping_matches:

            attribution_mismatches.append(
                attempt_id
            )

        if decision["verdict"] == "PERMIT":
            permit_count += 1

        if decision["verdict"] == "REFUSE":
            refuse_count += 1

        reconstructed_delta += int(
            decision["consequence_delta"]
        )

        reconstructed_chains.append(
            {
                "attempt_id":
                    attempt_id,

                "decision_id":
                    decision["decision_id"],

                "witness_id":
                    witness["witness_id"],

                "presenter_identity":
                    decision["presenter_identity"],

                "authority_id":
                    decision["authority_id"],

                "verdict":
                    decision["verdict"],

                "reason":
                    decision["reason"],

                "consequence_delta":
                    decision["consequence_delta"],

                "decision_digest":
                    record["decision_digest"],

                "recomputed_decision_digest":
                    recomputed_digest,

                "digest_matches":
                    digest_matches,

                "expected_mapping_matches":
                    expected_mapping_matches,
            }
        )

    reconstruction_record = {
        "examination":
            "EASA-F14",

        "record_type":
            "CANONICAL_RECONSTRUCTION",

        "observation_time_utc":
            observation_time,

        "canonical_order":
            [
                attempt["attempt_id"]
                for attempt in attempts
            ],

        "observed_completion_order":
            store_snapshot[
                "completion_order"
            ],

        "missing_attempts":
            missing_attempts,

        "digest_mismatches":
            digest_mismatches,

        "attribution_mismatches":
            attribution_mismatches,

        "reconstructed_chain_count":
            len(reconstructed_chains),

        "permit_count":
            permit_count,

        "refuse_count":
            refuse_count,

        "aggregate_reconstructed_delta":
            reconstructed_delta,

        "tool_final_counter":
            tool.consequence_counter,

        "chains":
            reconstructed_chains,
    }

    write_json(
        RECONSTRUCTION_PATH,
        reconstruction_record,
    )

    # ========================================================
    # CHECKS
    # ========================================================

    attempt_ids = [
        attempt["attempt_id"]
        for attempt in attempts
    ]

    decision_ids = [
        attempt["decision_id"]
        for attempt in attempts
    ]

    witness_ids = [
        attempt["witness_id"]
        for attempt in attempts
    ]

    presenter_ids = [
        attempt["presenter_identity"]
        for attempt in attempts
    ]

    valid_authority_ids = [
        attempt["authority_id"]
        for attempt in attempts
        if attempt["authority_id"] is not None
    ]

    odd_records = [
        records_by_attempt.get(
            identifier("F14-ATTEMPT", number)
        )
        for number in range(1, 13, 2)
    ]

    even_records = [
        records_by_attempt.get(
            identifier("F14-ATTEMPT", number)
        )
        for number in range(2, 13, 2)
    ]

    checks = {

        "exactly_12_attempts":
            len(attempts) == 12,

        "exactly_12_unique_attempt_ids":
            len(set(attempt_ids)) == 12,

        "exactly_12_unique_decision_ids":
            len(set(decision_ids)) == 12,

        "exactly_12_unique_witness_ids":
            len(set(witness_ids)) == 12,

        "exactly_12_unique_presenters":
            len(set(presenter_ids)) == 12,

        "exactly_6_valid_authorities":
            len(valid_authority_ids) == 6,

        "valid_authorities_only_on_odd_attempts":
            all(
                (
                    attempt["authority_id"]
                    is not None
                )
                ==
                (
                    attempt["attempt_number"]
                    % 2 == 1
                )
                for attempt in attempts
            ),

        "issued_authority_set_correct":
            list(
                authority_source.issued_ids
            )
            ==
            [
                "AUTH_F14-01",
                "AUTH_F14-03",
                "AUTH_F14-05",
                "AUTH_F14-07",
                "AUTH_F14-09",
                "AUTH_F14-11",
            ],

        "workers_ready_12":
            workers_ready == 12,

        "single_barrier_release":
            (
                start_release is True
                and
                barrier_action_count == 1
            ),

        "worker_exception_count_zero":
            len(worker_errors) == 0,

        "submitted_count_12":
            store_snapshot[
                "submitted_count"
            ]
            == 12,

        "accepted_count_12":
            store_snapshot[
                "accepted_count"
            ]
            == 12,

        "duplicate_rejection_count_zero":
            store_snapshot[
                "duplicate_rejection_count"
            ]
            == 0,

        "decision_record_count_12":
            store_snapshot[
                "decision_record_count"
            ]
            == 12,

        "witness_receipt_count_12":
            store_snapshot[
                "witness_receipt_count"
            ]
            == 12,

        "unique_attempt_count_12":
            store_snapshot[
                "unique_attempt_count"
            ]
            == 12,

        "unique_decision_count_12":
            store_snapshot[
                "unique_decision_count"
            ]
            == 12,

        "unique_witness_count_12":
            store_snapshot[
                "unique_witness_count"
            ]
            == 12,

        "completion_order_has_12":
            len(
                store_snapshot[
                    "completion_order"
                ]
            )
            == 12,

        "completion_order_identity_set_complete":
            set(
                store_snapshot[
                    "completion_order"
                ]
            )
            == set(attempt_ids),

        "no_missing_attempts":
            missing_attempts == [],

        "reconstructed_chain_count_12":
            len(reconstructed_chains)
            == 12,

        "digest_mismatch_count_zero":
            digest_mismatches == [],

        "attribution_mismatch_count_zero":
            attribution_mismatches == [],

        "permit_count_6":
            permit_count == 6,

        "refuse_count_6":
            refuse_count == 6,

        "aggregate_delta_6":
            reconstructed_delta == 6,

        "final_tool_counter_6":
            tool.consequence_counter == 6,

        "all_odd_records_present":
            all(
                record is not None
                for record in odd_records
            ),

        "all_even_records_present":
            all(
                record is not None
                for record in even_records
            ),

        "odd_records_permit_authorized_delta_1":
            all(
                record is not None
                and
                record["decision"]["verdict"]
                == "PERMIT"
                and
                record["decision"]["reason"]
                == "AUTHORIZED"
                and
                record["decision"][
                    "consequence_delta"
                ]
                == 1
                and
                record["decision"][
                    "authority_id"
                ]
                is not None
                and
                record["decision"][
                    "authority_consumed_before"
                ]
                is False
                and
                record["decision"][
                    "authority_consumed_after"
                ]
                is True
                for record in odd_records
            ),

        "even_records_refuse_no_authority_delta_0":
            all(
                record is not None
                and
                record["decision"]["verdict"]
                == "REFUSE"
                and
                record["decision"]["reason"]
                ==
                "EXECUTION_AUTHORITY_NOT_PRESENT"
                and
                record["decision"][
                    "consequence_delta"
                ]
                == 0
                and
                record["decision"][
                    "authority_id"
                ]
                is None
                for record in even_records
            ),

        "all_witnesses_digest_bound":
            all(
                chain["digest_matches"]
                is True
                for chain in reconstructed_chains
            ),

        "all_attribution_exact":
            all(
                chain[
                    "expected_mapping_matches"
                ]
                is True
                for chain in reconstructed_chains
            ),

        "canonical_reconstruction_independent_of_completion_order":
            [
                chain["attempt_id"]
                for chain in reconstructed_chains
            ]
            ==
            attempt_ids,

        "all_six_authorities_consumed":
            all(
                authority.consumed is True
                for authority in authorities.values()
            ),
    }

    overall_pass = all(
        checks.values()
    )

    summary = {
        "examination":
            "EASA-F14",

        "property":
            "CONCURRENT_EVIDENCE_WITNESS_INTEGRITY",

        "observation_time_utc":
            observation_time,

        "attempt_count":
            len(attempts),

        "worker_count":
            len(threads),

        "workers_ready":
            workers_ready,

        "start_release":
            start_release,

        "barrier_action_count":
            barrier_action_count,

        "worker_exception_count":
            len(worker_errors),

        "submitted_count":
            store_snapshot[
                "submitted_count"
            ],

        "accepted_count":
            store_snapshot[
                "accepted_count"
            ],

        "duplicate_rejection_count":
            store_snapshot[
                "duplicate_rejection_count"
            ],

        "decision_record_count":
            store_snapshot[
                "decision_record_count"
            ],

        "witness_receipt_count":
            store_snapshot[
                "witness_receipt_count"
            ],

        "unique_attempt_count":
            store_snapshot[
                "unique_attempt_count"
            ],

        "unique_decision_count":
            store_snapshot[
                "unique_decision_count"
            ],

        "unique_witness_count":
            store_snapshot[
                "unique_witness_count"
            ],

        "observed_completion_order":
            store_snapshot[
                "completion_order"
            ],

        "canonical_attempt_order":
            attempt_ids,

        "permit_count":
            permit_count,

        "refuse_count":
            refuse_count,

        "aggregate_evidence_consequence_delta":
            reconstructed_delta,

        "final_tool_consequence_counter":
            tool.consequence_counter,

        "digest_mismatch_count":
            len(digest_mismatches),

        "attribution_mismatch_count":
            len(attribution_mismatches),

        "missing_attempt_count":
            len(missing_attempts),

        "reconstructed_chain_count":
            len(reconstructed_chains),

        "checks":
            checks,

        "overall_result":
            "PASS"
            if overall_pass
            else "FAIL",

        "claim_state":
            (
                "OBSERVATION_SUPPORTS_DEFINED_PROPERTY"
                if overall_pass
                else
                "DEFINED_PROPERTY_NOT_ESTABLISHED_BY_FIRST_OBSERVATION"
            ),
    }

    write_json(
        SUMMARY_PATH,
        summary,
    )

    print(
        "=== EASA-F14 FIRST OBSERVATION ==="
    )

    print(
        json.dumps(
            summary,
            indent=2,
            sort_keys=True,
        )
    )

    return 0 if overall_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())