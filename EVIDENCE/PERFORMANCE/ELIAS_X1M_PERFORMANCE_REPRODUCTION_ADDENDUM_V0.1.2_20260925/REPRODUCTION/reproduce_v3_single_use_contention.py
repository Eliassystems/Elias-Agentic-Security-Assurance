# ELIAS X1M PERFORMANCE - v0.1.2 FORWARD-ONLY CONTENTION REPRODUCTION
#
# Purpose:
#   Independently reproduce the bounded single-use contention property
#   against the persisted Shadow V3 gate.
#
# Historical boundary:
#   This is NEW reproduction code created after frozen commit
#   627c70e11fdc39f3ce7ca2ca144c510ed7aa46d0.
#   It is not represented as the original historical generating artifact.

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

FROZEN_COMMIT = "627c70e11fdc39f3ce7ca2ca144c510ed7aa46d0"
EXPECTED_BASELINE_SHA256 = "85ac55b617aacd714252a995558fed74d6b6e330dd4055d7d2b9f29ae59971de"
EXPECTED_V3_SHA256 = "8c2f054fd4d2a9b9ec3684bdd73817d9e7a5c5e076d039aebb7928edae5f696f"

V3_RELATIVE_PATH = (
    Path("EVIDENCE")
    / "PERFORMANCE"
    / "ELIAS_X1M_PERFORMANCE_EXAMINATION_V0.1.1_PUBLICATION_20260925"
    / "REPRODUCTION"
    / "shadow_v3_gate.py"
)

DEFAULT_THREAD_COUNTS = (2, 4, 8, 16, 32, 64)
DEFAULT_ROUNDS_PER_COUNT = 100
FIELDS_PRESERVED = 21


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def find_repo_root() -> Path:
    here = Path(__file__).resolve()
    for candidate in (here.parent, *here.parents):
        baseline = candidate / "03_controls" / "easa_f16_x1m_execution.py"
        if baseline.is_file():
            return candidate
    raise RuntimeError("Repository root not found from reproduction artifact location.")


def load_module(module_name: str, path: Path):
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--thread-counts",
        nargs="+",
        type=int,
        default=list(DEFAULT_THREAD_COUNTS),
        help="Thread counts to examine.",
    )
    parser.add_argument(
        "--rounds-per-count",
        type=int,
        default=DEFAULT_ROUNDS_PER_COUNT,
        help="Contention rounds for each thread count.",
    )
    args = parser.parse_args()

    if not args.thread_counts or any(n < 2 for n in args.thread_counts):
        raise SystemExit("Every thread count must be at least 2.")
    if args.rounds_per_count <= 0:
        raise SystemExit("--rounds-per-count must be greater than zero.")

    root = find_repo_root()
    baseline_path = root / "03_controls" / "easa_f16_x1m_execution.py"
    v3_path = root / V3_RELATIVE_PATH

    baseline_hash = sha256_file(baseline_path)
    v3_hash = sha256_file(v3_path)

    print("ELIAS X1M v0.1.2 - V3 SINGLE-USE CONTENTION REPRODUCTION")
    print("=" * 86)
    print(f"FROZEN_COMMIT           : {FROZEN_COMMIT}")
    print(f"BASELINE_SHA256         : {baseline_hash}")
    print(f"PERSISTED_V3_SHA256     : {v3_hash}")
    print()

    if baseline_hash != EXPECTED_BASELINE_SHA256:
        raise SystemExit("BASELINE HASH MISMATCH - REFUSING REPRODUCTION")
    if v3_hash != EXPECTED_V3_SHA256:
        raise SystemExit("V3 HASH MISMATCH - REFUSING REPRODUCTION")

    print("BASELINE_HASH_MATCH      : TRUE")
    print("V3_HASH_MATCH            : TRUE")
    print()

    baseline = load_module(
        "easa_f16_x1m_execution_contention_reproduction",
        baseline_path,
    )
    v3 = load_module(
        "elias_persisted_shadow_v3_contention_reproduction",
        v3_path,
    )

    ExecutionAuthority = baseline.ExecutionAuthority
    ConsequentialTool = baseline.ConsequentialTool
    PRIMARY_TOOL = baseline.PRIMARY_TOOL
    ACTION = baseline.ACTION
    ShadowV3Gate = v3.ShadowV3Gate

    gate = ShadowV3Gate()

    total_rounds = 0
    total_failures = 0
    total_expected_permits = 0
    total_observed_permits = 0

    print("GATE       THREADS  ROUNDS  FAILURES  EXPECTED_PERMITS  OBSERVED_PERMITS")
    print("-" * 86)

    for thread_count in args.thread_counts:
        failures = 0
        observed_permits = 0

        for round_index in range(args.rounds_per_count):
            total_rounds += 1

            authority = ExecutionAuthority(
                authority_id=f"V012-CONTENTION-{thread_count}-{round_index}",
                subject_identity="SUBJECT_A",
                authorized_action=ACTION,
                authorized_tool_identity=PRIMARY_TOOL,
            )
            tool = ConsequentialTool(PRIMARY_TOOL)
            barrier = threading.Barrier(thread_count)

            def worker(worker_index: int):
                barrier.wait(timeout=30)
                return gate.attempt(
                    attempt_index=worker_index,
                    display_sequence=worker_index + 1,
                    attempt_id=(
                        f"V012-CONTENTION-{thread_count}-"
                        f"{round_index}-{worker_index}"
                    ),
                    attempt_class="SINGLE_USE_CONTENTION",
                    presenter_identity="SUBJECT_A",
                    authority=authority,
                    requested_action=ACTION,
                    presented_tool=tool,
                )

            try:
                with ThreadPoolExecutor(max_workers=thread_count) as executor:
                    decisions = list(executor.map(worker, range(thread_count)))
            except Exception as exc:
                failures += 1
                total_failures += 1
                print(
                    f"FAIL DETAIL threads={thread_count} "
                    f"round={round_index} exception={type(exc).__name__}:{exc}"
                )
                continue

            permits = sum(1 for d in decisions if d[15] == "PERMIT")
            refuses = sum(1 for d in decisions if d[15] == "REFUSE")
            consequence_delta = sum(d[19] for d in decisions)
            final_counter = tool.consequence_counter

            observed_permits += permits

            valid = (
                len(decisions) == thread_count
                and permits == 1
                and refuses == thread_count - 1
                and consequence_delta == 1
                and final_counter == 1
                and authority.consumed_snapshot() is True
            )

            if not valid:
                failures += 1
                total_failures += 1
                print(
                    "FAIL DETAIL "
                    f"threads={thread_count} "
                    f"round={round_index} "
                    f"decisions={len(decisions)} "
                    f"permits={permits} "
                    f"refuses={refuses} "
                    f"consequence_delta={consequence_delta} "
                    f"final_counter={final_counter} "
                    f"authority_consumed={authority.consumed_snapshot()}"
                )

        expected_permits = args.rounds_per_count
        total_expected_permits += expected_permits
        total_observed_permits += observed_permits

        print(
            f"SHADOW_V3  {thread_count:7d}  "
            f"{args.rounds_per_count:6d}  "
            f"{failures:8d}  "
            f"{expected_permits:16d}  "
            f"{observed_permits:16d}"
        )

    property_pass = total_failures == 0

    print()
    print("=" * 86)
    print(f"THREAD_COUNTS           : {','.join(str(n) for n in args.thread_counts)}")
    print(f"ROUNDS_PER_COUNT        : {args.rounds_per_count}")
    print(f"TOTAL_ROUNDS            : {total_rounds}")
    print(f"TOTAL_FAILURES          : {total_failures}")
    print(f"EXPECTED_PERMITS        : {total_expected_permits}")
    print(f"OBSERVED_PERMITS        : {total_observed_permits}")
    print(f"PROPERTY                : {'PASS' if property_pass else 'FAIL'}")
    print("REQUIRED_PER_ROUND      : EXACTLY_ONE_PERMIT")
    print("OTHER_CONTENDERS        : REFUSE")
    print("TOTAL_CONSEQUENCE_DELTA : 1")
    print("FINAL_TOOL_COUNTER      : 1")
    print(f"FIELDS_PRESERVED        : {FIELDS_PRESERVED}")
    print("SOURCE_MODIFIED         : NO")
    print("ARTIFACT_STATUS         : FORWARD_ONLY_REPRODUCTION")
    print("=" * 86)

    if not property_pass:
        return 1

    print("V0.1.2_CONTENTION_REPRODUCTION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
