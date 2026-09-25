# ELIAS X1M PERFORMANCE  -  v0.1.2 FORWARD-ONLY REPRODUCTION ARTIFACT
#
# Purpose:
#   Independently reproduce the bounded 100,000-case / 21-field
#   current-versus-persisted-Shadow-V3 semantic comparison.
#
# Provenance boundary:
#   This file is NEW reproduction code created after frozen commit
#   627c70e11fdc39f3ce7ca2ca144c510ed7aa46d0.
#
#   It is NOT represented as the original historical generating artifact.

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import sys
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

FIELDS = (
    "attempt_index",
    "display_sequence",
    "attempt_id",
    "attempt_class",
    "presenter_identity",
    "authority_present",
    "authority_id",
    "authority_subject_identity",
    "authority_valid",
    "authority_consumed_before",
    "authority_consumed_after",
    "authorized_action",
    "requested_action",
    "authorized_tool_identity",
    "presented_tool_identity",
    "verdict",
    "reason",
    "consequence_before",
    "consequence_after",
    "consequence_delta",
    "worker_thread_identity",
)

PATHS = (
    "NO_AUTHORITY",
    "INVALID_AUTHORITY",
    "ALREADY_CONSUMED",
    "IDENTITY_MISMATCH",
    "ACTION_MISMATCH",
    "TOOL_MISMATCH",
    "AUTHORIZED",
)


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


def normalize(decision):
    if isinstance(decision, tuple):
        values = tuple(decision)
    else:
        values = tuple(getattr(decision, field) for field in FIELDS)

    if len(values) != len(FIELDS):
        raise RuntimeError(
            f"Decision field count is {len(values)}; expected {len(FIELDS)}."
        )
    return values


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--samples",
        type=int,
        default=100_000,
        help="Number of deterministic sequential comparison cases.",
    )
    args = parser.parse_args()

    if args.samples <= 0:
        raise SystemExit("--samples must be greater than zero")

    root = find_repo_root()
    baseline_path = root / "03_controls" / "easa_f16_x1m_execution.py"
    v3_path = root / V3_RELATIVE_PATH

    baseline_hash = sha256_file(baseline_path)
    v3_hash = sha256_file(v3_path)

    print("ELIAS X1M v0.1.2  -  V3 SEMANTIC EQUIVALENCE REPRODUCTION")
    print("=" * 78)
    print(f"FROZEN_COMMIT           : {FROZEN_COMMIT}")
    print(f"BASELINE_SHA256         : {baseline_hash}")
    print(f"PERSISTED_V3_SHA256     : {v3_hash}")
    print()

    if baseline_hash != EXPECTED_BASELINE_SHA256:
        raise SystemExit("BASELINE HASH MISMATCH  -  REFUSING REPRODUCTION")
    if v3_hash != EXPECTED_V3_SHA256:
        raise SystemExit("V3 HASH MISMATCH  -  REFUSING REPRODUCTION")

    print("BASELINE_HASH_MATCH      : TRUE")
    print("V3_HASH_MATCH            : TRUE")
    print()

    sys.path.insert(0, str(root / "03_controls"))

    baseline = load_module(
        "easa_f16_x1m_execution_reproduction",
        baseline_path,
    )
    v3 = load_module(
        "elias_persisted_shadow_v3_reproduction",
        v3_path,
    )

    X1MExecutionGate = baseline.X1MExecutionGate
    ExecutionAuthority = baseline.ExecutionAuthority
    ConsequentialTool = baseline.ConsequentialTool
    PRIMARY_TOOL = baseline.PRIMARY_TOOL
    ALTERNATE_TOOL = baseline.ALTERNATE_TOOL
    ACTION = baseline.ACTION
    ShadowV3Gate = v3.ShadowV3Gate

    current_gate = X1MExecutionGate()
    shadow_gate = ShadowV3Gate()

    mismatches = 0
    permit_count = 0
    refuse_count = 0

    for i in range(args.samples):
        path = PATHS[i % len(PATHS)]

        presenter = "SUBJECT_A"
        requested_action = ACTION
        tool_id = PRIMARY_TOOL
        current_authority = None

        if path == "NO_AUTHORITY":
            pass
        elif path == "INVALID_AUTHORITY":
            current_authority = ExecutionAuthority(
                f"REPRO-A-{i}", "SUBJECT_A", ACTION, PRIMARY_TOOL, valid=False
            )
        elif path == "ALREADY_CONSUMED":
            current_authority = ExecutionAuthority(
                f"REPRO-A-{i}", "SUBJECT_A", ACTION, PRIMARY_TOOL
            )
            current_authority.consumed = True
        elif path == "IDENTITY_MISMATCH":
            current_authority = ExecutionAuthority(
                f"REPRO-A-{i}", "SUBJECT_A", ACTION, PRIMARY_TOOL
            )
            presenter = "SUBJECT_B"
        elif path == "ACTION_MISMATCH":
            current_authority = ExecutionAuthority(
                f"REPRO-A-{i}", "SUBJECT_A", ACTION, PRIMARY_TOOL
            )
            requested_action = "NOT_AUTHORIZED_ACTION"
        elif path == "TOOL_MISMATCH":
            current_authority = ExecutionAuthority(
                f"REPRO-A-{i}", "SUBJECT_A", ACTION, PRIMARY_TOOL
            )
            tool_id = ALTERNATE_TOOL
        elif path == "AUTHORIZED":
            current_authority = ExecutionAuthority(
                f"REPRO-A-{i}", "SUBJECT_A", ACTION, PRIMARY_TOOL
            )
        else:
            raise RuntimeError(f"Unknown reproduction path: {path}")

        if current_authority is None:
            shadow_authority = None
        else:
            shadow_authority = ExecutionAuthority(
                current_authority.authority_id,
                current_authority.subject_identity,
                current_authority.authorized_action,
                current_authority.authorized_tool_identity,
                valid=current_authority.valid,
            )
            shadow_authority.consumed = current_authority.consumed

        current_tool = ConsequentialTool(tool_id)
        shadow_tool = ConsequentialTool(tool_id)

        current_decision = current_gate.attempt(
            attempt_index=i,
            display_sequence=i + 1,
            attempt_id=f"REPRO-{i}",
            attempt_class=path,
            presenter_identity=presenter,
            authority=current_authority,
            requested_action=requested_action,
            presented_tool=current_tool,
        )

        shadow_decision = shadow_gate.attempt(
            attempt_index=i,
            display_sequence=i + 1,
            attempt_id=f"REPRO-{i}",
            attempt_class=path,
            presenter_identity=presenter,
            authority=shadow_authority,
            requested_action=requested_action,
            presented_tool=shadow_tool,
        )

        current_normalized = normalize(current_decision)
        shadow_normalized = normalize(shadow_decision)

        if current_normalized != shadow_normalized:
            mismatches += 1
            print("MISMATCH")
            print(f"ATTEMPT                : {i}")
            print(f"PATH                   : {path}")
            print(f"CURRENT                : {current_normalized}")
            print(f"SHADOW_V3              : {shadow_normalized}")
            break

        verdict = current_normalized[15]
        if verdict == "PERMIT":
            permit_count += 1
        elif verdict == "REFUSE":
            refuse_count += 1
        else:
            raise RuntimeError(f"Unexpected verdict at attempt {i}: {verdict}")

    print()
    print("=" * 78)
    print(f"ATTEMPTS_REQUESTED      : {args.samples:,}")
    print(f"FIELDS_COMPARED         : {len(FIELDS)}")
    print(f"PATH_CLASSES            : {len(PATHS)}")
    print(f"PERMIT                  : {permit_count:,}")
    print(f"REFUSE                  : {refuse_count:,}")
    print(f"MISMATCHES              : {mismatches:,}")
    print(f"EQUIVALENT              : {mismatches == 0}")
    print("SOURCE_MODIFIED         : NO")
    print("ARTIFACT_STATUS         : FORWARD_ONLY_REPRODUCTION")
    print("=" * 78)

    if mismatches != 0:
        return 1

    print("V0.1.2_SEMANTIC_REPRODUCTION=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
