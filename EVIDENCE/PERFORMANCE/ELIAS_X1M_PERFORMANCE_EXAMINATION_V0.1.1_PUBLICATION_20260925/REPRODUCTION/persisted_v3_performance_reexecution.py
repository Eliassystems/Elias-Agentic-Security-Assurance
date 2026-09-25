import csv
import hashlib
import importlib.util
import json
import statistics
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


ROOT = Path.cwd()

PACKAGE_ROOT = (
    ROOT
    / "EVIDENCE"
    / "PERFORMANCE"
    / "ELIAS_X1M_PERFORMANCE_EXAMINATION_V0.1_20260925"
)

V3_PATH = (
    PACKAGE_ROOT
    / "REPRODUCTION"
    / "shadow_v3_gate.py"
)

HARNESS_PATH = (
    PACKAGE_ROOT
    / "REPRODUCTION"
    / "persisted_v3_performance_reexecution.py"
)

RESULTS = PACKAGE_ROOT / "RESULTS"
RECEIPTS = PACKAGE_ROOT / "RECEIPTS"

BASELINE_PATH = (
    ROOT
    / "03_controls"
    / "easa_f16_x1m_execution.py"
)

EXPECTED_BASELINE_HASH = (
    "85ac55b617aacd714252a995558fed74d6b6e330dd4055d7d2b9f29ae59971de"
)

EXPECTED_V3_HASH = (
    "8c2f054fd4d2a9b9ec3684bdd73817d9e7a5c5e076d039aebb7928edae5f696f"
)


def sha256(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for block in iter(
            lambda: f.read(1024 * 1024),
            b"",
        ):
            h.update(block)

    return h.hexdigest()


if sha256(BASELINE_PATH) != EXPECTED_BASELINE_HASH:
    raise RuntimeError(
        "BASELINE HASH MISMATCH"
    )

if sha256(V3_PATH) != EXPECTED_V3_HASH:
    raise RuntimeError(
        "V3 HASH MISMATCH"
    )


sys.path.insert(
    0,
    str(ROOT / "03_controls"),
)

from easa_f16_x1m_execution import (
    X1MExecutionGate,
    ExecutionAuthority,
    ExecutionDecision,
    ConsequentialTool,
    PRIMARY_TOOL,
    ALTERNATE_TOOL,
    ACTION,
)


# ============================================================
# LOAD EXACT PERSISTED V3
# ============================================================

spec = importlib.util.spec_from_file_location(
    "elias_persisted_shadow_v3",
    V3_PATH,
)

v3_module = importlib.util.module_from_spec(
    spec
)

spec.loader.exec_module(
    v3_module
)

ShadowV3Gate = v3_module.ShadowV3Gate
FIELDS = v3_module.FIELDS


if FIELDS != tuple(
    ExecutionDecision.__dataclass_fields__.keys()
):
    raise RuntimeError(
        "V3 FIELD SCHEMA MISMATCH"
    )


# ============================================================
# COMMON ABBA FUNCTIONS
# ============================================================

ABBA_SAMPLES = 100_000
ABBA_WARMUP = 20_000


def warm_authorized(
    gate,
    tuple_result,
):

    tool = ConsequentialTool(
        PRIMARY_TOOL
    )

    for i in range(
        ABBA_WARMUP
    ):

        authority = ExecutionAuthority(
            "WARM",
            "SUBJECT_A",
            ACTION,
            PRIMARY_TOOL,
        )

        decision = gate.attempt(
            attempt_index=i,
            display_sequence=i,
            attempt_id="WARM",
            attempt_class="AUTHORIZED",
            presenter_identity="SUBJECT_A",
            authority=authority,
            requested_action=ACTION,
            presented_tool=tool,
        )

        verdict = (
            decision[15]
            if tuple_result
            else decision.verdict
        )

        if verdict != "PERMIT":
            raise RuntimeError(
                "WARMUP FAILURE"
            )


def authorized_batch(
    gate_class,
    tuple_result,
):

    gate = gate_class()

    warm_authorized(
        gate,
        tuple_result,
    )

    # Authority construction intentionally outside timer.
    authorities = [
        ExecutionAuthority(
            "BENCH",
            "SUBJECT_A",
            ACTION,
            PRIMARY_TOOL,
        )
        for _ in range(
            ABBA_SAMPLES
        )
    ]

    tool = ConsequentialTool(
        PRIMARY_TOOL
    )

    last = None

    start = time.perf_counter_ns()

    for i, authority in enumerate(
        authorities
    ):

        last = gate.attempt(
            attempt_index=i,
            display_sequence=i,
            attempt_id="BENCH",
            attempt_class="AUTHORIZED",
            presenter_identity="SUBJECT_A",
            authority=authority,
            requested_action=ACTION,
            presented_tool=tool,
        )

    elapsed = (
        time.perf_counter_ns()
        - start
    )

    # Validation intentionally outside timed region.
    if tuple_result:
        verdict = last[15]
        delta = last[19]
    else:
        verdict = last.verdict
        delta = last.consequence_delta

    if verdict != "PERMIT":
        raise RuntimeError(
            "AUTHORIZED VERDICT FAILURE"
        )

    if delta != 1:
        raise RuntimeError(
            "AUTHORIZED DELTA FAILURE"
        )

    if (
        tool.consequence_counter
        != ABBA_SAMPLES
    ):
        raise RuntimeError(
            "AUTHORIZED COUNTER FAILURE"
        )

    if not all(
        a.consumed
        for a in authorities
    ):
        raise RuntimeError(
            "AUTHORITY CONSUMPTION FAILURE"
        )

    return (
        elapsed
        / ABBA_SAMPLES
        / 1000
    )


# ============================================================
# CHILD MODE — ONE FRESH ABBA PROCESS
# ============================================================

if "--abba-child" in sys.argv:

    current_a = authorized_batch(
        X1MExecutionGate,
        False,
    )

    v3_a = authorized_batch(
        ShadowV3Gate,
        True,
    )

    v3_b = authorized_batch(
        ShadowV3Gate,
        True,
    )

    current_b = authorized_batch(
        X1MExecutionGate,
        False,
    )

    current_mean = statistics.mean(
        [current_a, current_b]
    )

    v3_mean = statistics.mean(
        [v3_a, v3_b]
    )

    ratio = (
        current_mean
        / v3_mean
    )

    reduction = (
        1
        - (
            v3_mean
            / current_mean
        )
    ) * 100

    print(
        json.dumps(
            {
                "current_a_us": current_a,
                "v3_a_us": v3_a,
                "v3_b_us": v3_b,
                "current_b_us": current_b,
                "current_mean_us": current_mean,
                "v3_mean_us": v3_mean,
                "ratio_x": ratio,
                "reduction_percent": reduction,
            }
        )
    )

    raise SystemExit(0)


# ============================================================
# SEVEN-PATH PERFORMANCE FUNCTIONS
# ============================================================

PATHS = (
    "NO_AUTHORITY",
    "INVALID_AUTHORITY",
    "ALREADY_CONSUMED",
    "IDENTITY_MISMATCH",
    "ACTION_MISMATCH",
    "TOOL_MISMATCH",
    "AUTHORIZED",
)

MATRIX_SAMPLES = 100_000
MATRIX_WARMUP = 5_000
MATRIX_REPEATS = 5


def build_case(
    path,
    i,
):

    presenter = "SUBJECT_A"
    requested_action = ACTION
    tool_identity = PRIMARY_TOOL
    authority = None

    if path == "NO_AUTHORITY":
        pass

    elif path == "INVALID_AUTHORITY":

        authority = ExecutionAuthority(
            f"A-{i}",
            "SUBJECT_A",
            ACTION,
            PRIMARY_TOOL,
            valid=False,
        )

    elif path == "ALREADY_CONSUMED":

        authority = ExecutionAuthority(
            f"A-{i}",
            "SUBJECT_A",
            ACTION,
            PRIMARY_TOOL,
        )

        authority.consumed = True

    elif path == "IDENTITY_MISMATCH":

        authority = ExecutionAuthority(
            f"A-{i}",
            "SUBJECT_A",
            ACTION,
            PRIMARY_TOOL,
        )

        presenter = "SUBJECT_B"

    elif path == "ACTION_MISMATCH":

        authority = ExecutionAuthority(
            f"A-{i}",
            "SUBJECT_A",
            ACTION,
            PRIMARY_TOOL,
        )

        requested_action = (
            "NOT_AUTHORIZED_ACTION"
        )

    elif path == "TOOL_MISMATCH":

        authority = ExecutionAuthority(
            f"A-{i}",
            "SUBJECT_A",
            ACTION,
            PRIMARY_TOOL,
        )

        tool_identity = (
            ALTERNATE_TOOL
        )

    elif path == "AUTHORIZED":

        authority = ExecutionAuthority(
            f"A-{i}",
            "SUBJECT_A",
            ACTION,
            PRIMARY_TOOL,
        )

    else:

        raise ValueError(
            path
        )

    return (
        presenter,
        requested_action,
        tool_identity,
        authority,
    )


def path_batch(
    gate_class,
    tuple_result,
    path,
):

    gate = gate_class()

    # Warmup.
    for i in range(
        MATRIX_WARMUP
    ):

        (
            presenter,
            action,
            tool_id,
            authority,
        ) = build_case(
            path,
            i,
        )

        tool = ConsequentialTool(
            tool_id
        )

        gate.attempt(
            attempt_index=i,
            display_sequence=i,
            attempt_id="WARM",
            attempt_class=path,
            presenter_identity=presenter,
            authority=authority,
            requested_action=action,
            presented_tool=tool,
        )

    prepared = []

    shared_tool = ConsequentialTool(
        ALTERNATE_TOOL
        if path == "TOOL_MISMATCH"
        else PRIMARY_TOOL
    )

    # State construction intentionally outside timer.
    for i in range(
        MATRIX_SAMPLES
    ):

        (
            presenter,
            action,
            _,
            authority,
        ) = build_case(
            path,
            i,
        )

        prepared.append(
            (
                presenter,
                action,
                authority,
            )
        )

    last = None

    start = time.perf_counter_ns()

    for i, (
        presenter,
        action,
        authority,
    ) in enumerate(
        prepared
    ):

        last = gate.attempt(
            attempt_index=i,
            display_sequence=i,
            attempt_id="BENCH",
            attempt_class=path,
            presenter_identity=presenter,
            authority=authority,
            requested_action=action,
            presented_tool=shared_tool,
        )

    elapsed = (
        time.perf_counter_ns()
        - start
    )

    if tuple_result:
        verdict = last[15]
        delta = last[19]
    else:
        verdict = last.verdict
        delta = last.consequence_delta

    expected = (
        "PERMIT"
        if path == "AUTHORIZED"
        else "REFUSE"
    )

    if verdict != expected:
        raise RuntimeError(
            f"{path}: VERDICT FAILURE"
        )

    if path == "AUTHORIZED":

        if delta != 1:
            raise RuntimeError(
                "AUTHORIZED DELTA FAILURE"
            )

        if (
            shared_tool.consequence_counter
            != MATRIX_SAMPLES
        ):
            raise RuntimeError(
                "AUTHORIZED COUNTER FAILURE"
            )

    else:

        if delta != 0:
            raise RuntimeError(
                f"{path}: DELTA FAILURE"
            )

        if (
            shared_tool.consequence_counter
            != 0
        ):
            raise RuntimeError(
                f"{path}: UNEXPECTED CONSEQUENCE"
            )

    return (
        elapsed
        / MATRIX_SAMPLES
        / 1000
    )


# ============================================================
# TEN FRESH-PROCESS ABBA RUNS
# ============================================================

abba_rows = []

for process_no in range(
    1,
    11,
):

    completed = subprocess.run(
        [
            sys.executable,
            str(HARNESS_PATH),
            "--abba-child",
        ],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        check=True,
    )

    lines = [
        line.strip()
        for line
        in completed.stdout.splitlines()
        if line.strip()
    ]

    if not lines:
        raise RuntimeError(
            "EMPTY ABBA CHILD OUTPUT"
        )

    row = json.loads(
        lines[-1]
    )

    row["process"] = process_no

    abba_rows.append(
        row
    )


abba_csv_path = (
    RESULTS
    / "PERSISTED_V3_ABBA_10_PROCESS_RESULTS.csv"
)

with open(
    abba_csv_path,
    "w",
    newline="",
    encoding="utf-8",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "process",
            "current_a_us",
            "v3_a_us",
            "v3_b_us",
            "current_b_us",
            "current_mean_us",
            "v3_mean_us",
            "ratio_x",
            "reduction_percent",
        ],
    )

    writer.writeheader()

    for row in abba_rows:

        writer.writerow(
            row
        )


current_aggregate = statistics.mean(
    row["current_mean_us"]
    for row in abba_rows
)

v3_aggregate = statistics.mean(
    row["v3_mean_us"]
    for row in abba_rows
)

aggregate_ratio = (
    current_aggregate
    / v3_aggregate
)

aggregate_reduction = (
    1
    - (
        v3_aggregate
        / current_aggregate
    )
) * 100

ratios = [
    row["ratio_x"]
    for row in abba_rows
]

reductions = [
    row["reduction_percent"]
    for row in abba_rows
]


# ============================================================
# SEVEN-PATH MATRIX FROM PERSISTED V3
# ============================================================

matrix_rows = []

for path in PATHS:

    current_runs = []
    v3_runs = []

    for repeat in range(
        MATRIX_REPEATS
    ):

        if repeat % 2 == 0:

            current_runs.append(
                path_batch(
                    X1MExecutionGate,
                    False,
                    path,
                )
            )

            v3_runs.append(
                path_batch(
                    ShadowV3Gate,
                    True,
                    path,
                )
            )

        else:

            v3_runs.append(
                path_batch(
                    ShadowV3Gate,
                    True,
                    path,
                )
            )

            current_runs.append(
                path_batch(
                    X1MExecutionGate,
                    False,
                    path,
                )
            )

    current_mean = statistics.mean(
        current_runs
    )

    v3_mean = statistics.mean(
        v3_runs
    )

    ratio = (
        current_mean
        / v3_mean
    )

    reduction = (
        1
        - (
            v3_mean
            / current_mean
        )
    ) * 100

    matrix_rows.append(
        {
            "path": path,
            "current_us": current_mean,
            "v3_us": v3_mean,
            "ratio_x": ratio,
            "reduction_percent": reduction,
        }
    )


matrix_csv_path = (
    RESULTS
    / "PERSISTED_V3_SEVEN_PATH_PERFORMANCE.csv"
)

with open(
    matrix_csv_path,
    "w",
    newline="",
    encoding="utf-8",
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=[
            "path",
            "current_us",
            "v3_us",
            "ratio_x",
            "reduction_percent",
        ],
    )

    writer.writeheader()

    for row in matrix_rows:

        writer.writerow(
            row
        )


all_faster = all(
    row["v3_us"]
    < row["current_us"]
    for row in matrix_rows
)


if not all_faster:
    raise RuntimeError(
        "PERSISTED V3 NOT FASTER ON EVERY TESTED PATH"
    )


# ============================================================
# SUMMARY FILE
# ============================================================

timestamp = (
    datetime.now()
    .astimezone()
    .isoformat()
)

summary_path = (
    RESULTS
    / "PERSISTED_V3_PERFORMANCE_REEXECUTION.txt"
)

summary_lines = [
    "ELIAS X1M — PERSISTED V3 PERFORMANCE RE-EXECUTION",
    "=" * 76,
    "",
    f"TIMESTAMP={timestamp}",
    f"BASELINE_SHA256={sha256(BASELINE_PATH)}",
    f"V3_SHA256={sha256(V3_PATH)}",
    f"HARNESS_SHA256={sha256(HARNESS_PATH)}",
    "",
    "ABBA_FRESH_PROCESSES=10",
    f"ABBA_SAMPLES_PER_BATCH={ABBA_SAMPLES}",
    "ABBA_AUTHORITY_CONSTRUCTION=OUTSIDE_TIMED_REGION",
    f"ABBA_CURRENT_AGGREGATE_MEAN_US={current_aggregate:.6f}",
    f"ABBA_V3_AGGREGATE_MEAN_US={v3_aggregate:.6f}",
    f"ABBA_RATIO_OF_AGGREGATE_MEANS={aggregate_ratio:.6f}x",
    f"ABBA_AGGREGATE_REDUCTION={aggregate_reduction:.3f}%",
    f"ABBA_PROCESS_RATIO_MIN={min(ratios):.6f}x",
    f"ABBA_PROCESS_RATIO_MAX={max(ratios):.6f}x",
    f"ABBA_PROCESS_REDUCTION_MIN={min(reductions):.3f}%",
    f"ABBA_PROCESS_REDUCTION_MAX={max(reductions):.3f}%",
    "",
    "SEVEN_PATH_MATRIX:",
]

for row in matrix_rows:

    summary_lines.append(
        (
            f"{row['path']}: "
            f"CURRENT={row['current_us']:.6f}us "
            f"V3={row['v3_us']:.6f}us "
            f"RATIO={row['ratio_x']:.6f}x "
            f"REDUCTION={row['reduction_percent']:.3f}%"
        )
    )

summary_lines.extend(
    [
        "",
        f"SEVEN_PATH_ALL_V3_FASTER={all_faster}",
        "",
        "BASELINE_MODIFIED=NO",
        "PERSISTED_V3_IMPORTED_FROM_DISK=YES",
        "PERFORMANCE_REEXECUTION=PASS",
        "RELEASE_GATE=HOLD",
        "NEXT=FINAL_PACKAGE_RECONCILIATION_AND_FREEZE",
        "",
        "=" * 76,
    ]
)

summary_text = "\n".join(
    summary_lines
)

summary_path.write_text(
    summary_text,
    encoding="utf-8",
)


# ============================================================
# RECEIPT
# ============================================================

receipt_path = (
    RECEIPTS
    / "PERSISTED_V3_PERFORMANCE_RECEIPT.txt"
)

receipt_path.write_text(
    (
        "ELIAS PERSISTED V3 PERFORMANCE RECEIPT\n"
        "======================================\n\n"
        f"TIMESTAMP={timestamp}\n"
        f"BASELINE_SHA256={sha256(BASELINE_PATH)}\n"
        f"V3_SHA256={sha256(V3_PATH)}\n"
        f"HARNESS_SHA256={sha256(HARNESS_PATH)}\n\n"
        "TEN_FRESH_PROCESS_ABBA=PASS\n"
        "SEVEN_PATH_MATRIX=PASS\n"
        f"ALL_SEVEN_PATHS_V3_FASTER={all_faster}\n"
        "BASELINE_MODIFIED=NO\n"
        "PERFORMANCE_REEXECUTION=PASS\n"
        "RELEASE_GATE=HOLD\n\n"
        "======================================\n"
    ),
    encoding="utf-8",
)


# ============================================================
# TERMINAL OUTPUT
# ============================================================

print()
print(
    "ELIAS PERSISTED V3 — PERFORMANCE RE-EXECUTION"
)
print("=" * 92)

print()
print(
    f"BASELINE SHA-256 : "
    f"{sha256(BASELINE_PATH)}"
)

print(
    f"V3 SHA-256       : "
    f"{sha256(V3_PATH)}"
)

print(
    f"HARNESS SHA-256  : "
    f"{sha256(HARNESS_PATH)}"
)

print()
print(
    "TEN FRESH-PROCESS ABBA RESULTS"
)
print("-" * 92)

for row in abba_rows:

    print(
        f"PROCESS {row['process']:>2}  "
        f"CURRENT={row['current_mean_us']:.3f} us  "
        f"V3={row['v3_mean_us']:.3f} us  "
        f"RATIO={row['ratio_x']:.3f}x  "
        f"REDUCTION={row['reduction_percent']:.1f}%"
    )

print("-" * 92)

print(
    f"AGGREGATE CURRENT MEAN : "
    f"{current_aggregate:.3f} us"
)

print(
    f"AGGREGATE V3 MEAN      : "
    f"{v3_aggregate:.3f} us"
)

print(
    f"AGGREGATE RATIO        : "
    f"{aggregate_ratio:.3f}x"
)

print(
    f"AGGREGATE REDUCTION    : "
    f"{aggregate_reduction:.1f}%"
)

print()
print(
    "SEVEN-PATH PERSISTED V3 MATRIX"
)
print("-" * 92)

print(
    f"{'PATH':<22}"
    f"{'CURRENT_US':>13}"
    f"{'V3_US':>13}"
    f"{'RATIO':>12}"
    f"{'REDUCTION':>14}"
)

for row in matrix_rows:

    print(
        f"{row['path']:<22}"
        f"{row['current_us']:>13.3f}"
        f"{row['v3_us']:>13.3f}"
        f"{row['ratio_x']:>11.3f}x"
        f"{row['reduction_percent']:>13.1f}%"
    )

print("-" * 92)

print(
    f"ALL SEVEN PATHS V3 FASTER : "
    f"{all_faster}"
)

print()
print(
    "PERFORMANCE_REEXECUTION=PASS"
)

print(
    "BASELINE_MODIFIED=NO"
)

print(
    "RELEASE_GATE=HOLD"
)

print(
    "NEXT=FINAL_PACKAGE_RECONCILIATION_AND_FREEZE"
)

print("=" * 92)
