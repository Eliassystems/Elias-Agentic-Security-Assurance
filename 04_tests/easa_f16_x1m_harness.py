from __future__ import annotations

import hashlib
import json
import struct
import sys
import time
import traceback
import zlib
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTROL_DIR = ROOT / "03_controls"
if str(CONTROL_DIR) not in sys.path:
    sys.path.insert(0, str(CONTROL_DIR))

from easa_f16_x1m_execution import (
    ACTION,
    ALTERNATE_TOOL,
    PRIMARY_TOOL,
    ConsequentialTool,
    ExecutionAuthority,
    X1MExecutionGate,
)

EXAMINATION = "EASA-F16-X1M"
TOTAL_ATTEMPTS = 1_000_000
CHUNK_SIZE = 10_000
CHUNK_COUNT = 100
MAX_WORKERS = 64
EXPECTED_PER_CLASS = 200_000
EXPECTED_PERMITS = 200_000
EXPECTED_REFUSALS = 800_000
EXPECTED_AUTHORIZED_CONSEQUENCE = 200_000
EXPECTED_UNAUTHORIZED_CONSEQUENCE = 0
EXPECTED_AUTHORITY_BEARING = 800_000
COMPRESSION_LEVEL = 6

CLASS_NAMES = (
    "AUTHORIZED",
    "NO_AUTHORITY",
    "PRESENTER_IDENTITY_MISMATCH",
    "TOOL_IDENTITY_MISMATCH",
    "PRECONSUMED_AUTHORITY_REPLAY",
)

EXPECTED_CLASS_COUNTS = {name: EXPECTED_PER_CLASS for name in CLASS_NAMES}
EXPECTED_CHUNK_CLASS_COUNTS = {name: 2_000 for name in CLASS_NAMES}
EXPECTED_REFUSAL_REASON_COUNTS = {
    "EXECUTION_AUTHORITY_NOT_PRESENT": 200_000,
    "PRESENTER_IDENTITY_MISMATCH": 200_000,
    "TOOL_IDENTITY_MISMATCH": 200_000,
    "EXECUTION_AUTHORITY_ALREADY_CONSUMED": 200_000,
}

EVIDENCE_DIR = ROOT / "05_evidence" / "EASA-F16-X1M"
SHARD_MANIFEST_PATH = EVIDENCE_DIR / "EASA-F16-X1M-SHARD-MANIFEST.json"
SUMMARY_PATH = EVIDENCE_DIR / "EASA-F16-X1M-SUMMARY.json"
FAILURE_PATH = EVIDENCE_DIR / "EASA-F16-X1M-FAILURE.json"

def canonical_bytes(value) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")

def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest().upper()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest().upper()

def write_json(path: Path, value) -> None:
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

class DeterministicGzipWriter:
    def __init__(self, path: Path, level: int = COMPRESSION_LEVEL) -> None:
        self.raw = path.open("wb")
        self.raw.write(
            b"\x1f\x8b\x08\x00"
            b"\x00\x00\x00\x00"
            b"\x00\xff"
        )
        self.compressor = zlib.compressobj(
            level,
            zlib.DEFLATED,
            -zlib.MAX_WBITS,
        )
        self.crc32 = 0
        self.size = 0
        self.closed = False

    def write(self, data: bytes) -> None:
        if self.closed:
            raise RuntimeError("DETERMINISTIC_GZIP_WRITER_CLOSED")
        self.crc32 = zlib.crc32(data, self.crc32)
        self.size = (self.size + len(data)) & 0xFFFFFFFF
        out = self.compressor.compress(data)
        if out:
            self.raw.write(out)

    def close(self) -> None:
        if self.closed:
            return
        tail = self.compressor.flush(zlib.Z_FINISH)
        if tail:
            self.raw.write(tail)
        self.raw.write(
            struct.pack(
                "<II",
                self.crc32 & 0xFFFFFFFF,
                self.size & 0xFFFFFFFF,
            )
        )
        self.raw.flush()
        self.raw.close()
        self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.close()
        return False

def frozen_identity(prefix: str, display_sequence: int) -> str:
    return f"{prefix}-{display_sequence:07d}"

def shard_path(chunk_number: int) -> Path:
    return EVIDENCE_DIR / (
        f"EASA-F16-X1M-DECISIONS-{chunk_number:03d}.jsonl.gz"
    )

def run_attempt(
    *,
    attempt_index: int,
    gate: X1MExecutionGate,
    primary_tool: ConsequentialTool,
    alternate_tool: ConsequentialTool,
):
    display_sequence = attempt_index + 1
    attempt_id = frozen_identity("F16X1M-ATTEMPT", display_sequence)
    presenter_identity = frozen_identity("AGENT_F16X1M", display_sequence)
    authority_id = frozen_identity("AUTH_F16X1M", display_sequence)
    attempt_class = CLASS_NAMES[attempt_index % 5]
    authority = None
    presented_tool = primary_tool

    if attempt_class == "AUTHORIZED":
        authority = ExecutionAuthority(
            authority_id=authority_id,
            subject_identity=presenter_identity,
            authorized_action=ACTION,
            authorized_tool_identity=PRIMARY_TOOL,
            valid=True,
            consumed=False,
        )
    elif attempt_class == "NO_AUTHORITY":
        authority = None
    elif attempt_class == "PRESENTER_IDENTITY_MISMATCH":
        authority = ExecutionAuthority(
            authority_id=authority_id,
            subject_identity=frozen_identity(
                "BOUND_AGENT_F16X1M",
                display_sequence,
            ),
            authorized_action=ACTION,
            authorized_tool_identity=PRIMARY_TOOL,
            valid=True,
            consumed=False,
        )
    elif attempt_class == "TOOL_IDENTITY_MISMATCH":
        authority = ExecutionAuthority(
            authority_id=authority_id,
            subject_identity=presenter_identity,
            authorized_action=ACTION,
            authorized_tool_identity=PRIMARY_TOOL,
            valid=True,
            consumed=False,
        )
        presented_tool = alternate_tool
    elif attempt_class == "PRECONSUMED_AUTHORITY_REPLAY":
        authority = ExecutionAuthority(
            authority_id=authority_id,
            subject_identity=presenter_identity,
            authorized_action=ACTION,
            authorized_tool_identity=PRIMARY_TOOL,
            valid=True,
            consumed=True,
        )
    else:
        raise RuntimeError("X1M_CLASS_NOT_FROZEN")

    return gate.attempt(
        attempt_index=attempt_index,
        display_sequence=display_sequence,
        attempt_id=attempt_id,
        attempt_class=attempt_class,
        presenter_identity=presenter_identity,
        authority=authority,
        requested_action=ACTION,
        presented_tool=presented_tool,
    )

def validate_record(record: dict, expected_index: int) -> bool:
    sequence = expected_index + 1
    cls = CLASS_NAMES[expected_index % 5]
    presenter = frozen_identity("AGENT_F16X1M", sequence)

    if record["attempt_index"] != expected_index:
        return False
    if record["display_sequence"] != sequence:
        return False
    if record["attempt_class"] != cls:
        return False
    if record["attempt_id"] != frozen_identity("F16X1M-ATTEMPT", sequence):
        return False
    if record["presenter_identity"] != presenter:
        return False
    if record["requested_action"] != ACTION:
        return False

    if cls == "NO_AUTHORITY":
        return (
            record["authority_present"] is False
            and record["authority_id"] is None
            and record["verdict"] == "REFUSE"
            and record["reason"] == "EXECUTION_AUTHORITY_NOT_PRESENT"
            and record["consequence_delta"] == 0
        )

    if record["authority_id"] != frozen_identity("AUTH_F16X1M", sequence):
        return False
    if record["authority_present"] is not True:
        return False
    if record["authority_valid"] is not True:
        return False
    if record["authorized_action"] != ACTION:
        return False

    if cls == "AUTHORIZED":
        return (
            record["authority_subject_identity"] == presenter
            and record["authorized_tool_identity"] == PRIMARY_TOOL
            and record["presented_tool_identity"] == PRIMARY_TOOL
            and record["verdict"] == "PERMIT"
            and record["reason"] == "AUTHORIZED"
            and record["consequence_delta"] == 1
            and record["authority_consumed_before"] is False
            and record["authority_consumed_after"] is True
        )

    if cls == "PRESENTER_IDENTITY_MISMATCH":
        return (
            record["authority_subject_identity"]
            == frozen_identity("BOUND_AGENT_F16X1M", sequence)
            and record["authorized_tool_identity"] == PRIMARY_TOOL
            and record["presented_tool_identity"] == PRIMARY_TOOL
            and record["verdict"] == "REFUSE"
            and record["reason"] == "PRESENTER_IDENTITY_MISMATCH"
            and record["consequence_delta"] == 0
            and record["authority_consumed_before"] is False
            and record["authority_consumed_after"] is False
        )

    if cls == "TOOL_IDENTITY_MISMATCH":
        return (
            record["authority_subject_identity"] == presenter
            and record["authorized_tool_identity"] == PRIMARY_TOOL
            and record["presented_tool_identity"] == ALTERNATE_TOOL
            and record["verdict"] == "REFUSE"
            and record["reason"] == "TOOL_IDENTITY_MISMATCH"
            and record["consequence_delta"] == 0
            and record["authority_consumed_before"] is False
            and record["authority_consumed_after"] is False
        )

    if cls == "PRECONSUMED_AUTHORITY_REPLAY":
        return (
            record["authority_subject_identity"] == presenter
            and record["authorized_tool_identity"] == PRIMARY_TOOL
            and record["presented_tool_identity"] == PRIMARY_TOOL
            and record["verdict"] == "REFUSE"
            and record["reason"] == "EXECUTION_AUTHORITY_ALREADY_CONSUMED"
            and record["consequence_delta"] == 0
            and record["authority_consumed_before"] is True
            and record["authority_consumed_after"] is True
        )

    return False

def progress_manifest(shards: list[dict]) -> dict:
    return {
        "examination": EXAMINATION,
        "status": "IN_PROGRESS",
        "chunk_size": CHUNK_SIZE,
        "expected_chunk_count": CHUNK_COUNT,
        "completed_chunk_count": len(shards),
        "shards": shards,
    }

def main() -> int:
    if EVIDENCE_DIR.exists():
        existing = [p for p in EVIDENCE_DIR.iterdir() if p.is_file()]
        if existing:
            print("EASA-F16-X1M HISTORICAL EVIDENCE ALREADY EXISTS")
            print("DO NOT RERUN")
            return 2

    EVIDENCE_DIR.mkdir(parents=True, exist_ok=True)

    primary_tool = ConsequentialTool(PRIMARY_TOOL)
    alternate_tool = ConsequentialTool(ALTERNATE_TOOL)
    gate = X1MExecutionGate()

    global_digest = hashlib.sha256()
    class_counts = Counter()
    verdict_counts = Counter()
    reason_counts = Counter()

    authorized_consequence = 0
    unauthorized_consequence = 0
    processed = 0
    authority_bearing = 0
    identity_exact = True
    behavior_exact = True
    shards: list[dict] = []
    total_compressed_bytes = 0

    current_chunk = 0
    partial_results = 0
    started = time.perf_counter()

    try:
        with ThreadPoolExecutor(
            max_workers=MAX_WORKERS,
            thread_name_prefix="F16X1M",
        ) as executor:
            for chunk_number in range(1, CHUNK_COUNT + 1):
                current_chunk = chunk_number
                partial_results = 0
                start_index = (chunk_number - 1) * CHUNK_SIZE
                end_index = start_index + CHUNK_SIZE

                futures = [
                    executor.submit(
                        run_attempt,
                        attempt_index=i,
                        gate=gate,
                        primary_tool=primary_tool,
                        alternate_tool=alternate_tool,
                    )
                    for i in range(start_index, end_index)
                ]

                completed = []
                for future in as_completed(futures):
                    completed.append(future.result())
                    partial_results += 1

                ordered = sorted(completed, key=lambda d: d.attempt_id)
                if len(ordered) != CHUNK_SIZE:
                    raise RuntimeError("X1M_CHUNK_DECISION_COUNT_MISMATCH")

                chunk_counts = Counter()
                shard_digest = hashlib.sha256()
                out_path = shard_path(chunk_number)
                if out_path.exists():
                    raise RuntimeError("X1M_SHARD_ALREADY_EXISTS")

                first_id = None
                final_id = None

                with DeterministicGzipWriter(out_path) as gz:
                    for offset, decision in enumerate(ordered):
                        expected_index = start_index + offset
                        record = asdict(decision)

                        if not validate_record(record, expected_index):
                            identity_exact = False
                            behavior_exact = False
                            raise RuntimeError(
                                f"X1M_RECORD_VALIDATION_FAILED:{expected_index}"
                            )

                        first_id = first_id or record["attempt_id"]
                        final_id = record["attempt_id"]
                        cls = record["attempt_class"]

                        chunk_counts[cls] += 1
                        class_counts[cls] += 1
                        verdict_counts[record["verdict"]] += 1

                        if record["verdict"] == "REFUSE":
                            reason_counts[record["reason"]] += 1
                        if record["authority_id"] is not None:
                            authority_bearing += 1

                        if cls == "AUTHORIZED":
                            authorized_consequence += record["consequence_delta"]
                        else:
                            unauthorized_consequence += record["consequence_delta"]

                        line = canonical_bytes(record) + b"\n"
                        shard_digest.update(line)
                        global_digest.update(line)
                        gz.write(line)
                        processed += 1

                if dict(chunk_counts) != EXPECTED_CHUNK_CLASS_COUNTS:
                    raise RuntimeError(
                        f"X1M_CHUNK_CLASS_COUNTS_MISMATCH:{chunk_number}"
                    )

                expected_first = frozen_identity(
                    "F16X1M-ATTEMPT",
                    start_index + 1,
                )
                expected_final = frozen_identity(
                    "F16X1M-ATTEMPT",
                    end_index,
                )
                if first_id != expected_first:
                    raise RuntimeError(
                        f"X1M_CHUNK_FIRST_ID_MISMATCH:{chunk_number}"
                    )
                if final_id != expected_final:
                    raise RuntimeError(
                        f"X1M_CHUNK_FINAL_ID_MISMATCH:{chunk_number}"
                    )

                compressed_bytes = out_path.stat().st_size
                total_compressed_bytes += compressed_bytes

                shards.append(
                    {
                        "chunk_number": chunk_number,
                        "first_attempt_id": first_id,
                        "final_attempt_id": final_id,
                        "record_count": CHUNK_SIZE,
                        "canonical_uncompressed_sha256":
                            shard_digest.hexdigest().upper(),
                        "compressed_file": out_path.name,
                        "compressed_file_sha256": sha256_file(out_path),
                        "compressed_file_bytes": compressed_bytes,
                    }
                )

                write_json(
                    SHARD_MANIFEST_PATH,
                    progress_manifest(shards),
                )

                print(
                    f"CHUNK={chunk_number:03d} STATUS=PASS "
                    f"RECORDS={CHUNK_SIZE} "
                    f"COMPRESSED_BYTES={compressed_bytes}",
                    flush=True,
                )

                del futures
                del completed
                del ordered

        elapsed = round(time.perf_counter() - started, 6)
        global_decision_digest = global_digest.hexdigest().upper()

        manifest_core = {
            "examination": EXAMINATION,
            "status": "COMPLETE",
            "chunk_size": CHUNK_SIZE,
            "chunk_count": CHUNK_COUNT,
            "canonical_order": "ATTEMPT_ID_ASCENDING",
            "canonical_record_representation":
                "COMPACT_SORTED_JSON_UTF8_PLUS_LF",
            "deterministic_gzip": {
                "filename_field": "ABSENT",
                "mtime": 0,
                "os": 255,
                "compression_level": COMPRESSION_LEVEL,
            },
            "shards": shards,
        }

        manifest_digest = sha256_hex(canonical_bytes(manifest_core))
        final_manifest = dict(manifest_core)
        final_manifest[
            "canonical_shard_manifest_digest_sha256"
        ] = manifest_digest
        write_json(SHARD_MANIFEST_PATH, final_manifest)

        checks = {
            "single_historical_harness_invocation": True,
            "chunk_count_100": len(shards) == 100,
            "chunk_size_10000": CHUNK_SIZE == 10_000,
            "population_1000000": TOTAL_ATTEMPTS == 1_000_000,
            "processed_attempts_1000000": processed == 1_000_000,
            "decision_count_1000000": processed == 1_000_000,
            "class_counts_exact":
                dict(class_counts) == EXPECTED_CLASS_COUNTS,
            "permit_count_200000":
                verdict_counts["PERMIT"] == 200_000,
            "refuse_count_800000":
                verdict_counts["REFUSE"] == 800_000,
            "refusal_reason_counts_exact":
                dict(reason_counts) == EXPECTED_REFUSAL_REASON_COUNTS,
            "authorized_consequence_200000":
                authorized_consequence == 200_000,
            "unauthorized_consequence_zero":
                unauthorized_consequence == 0,
            "primary_tool_counter_200000":
                primary_tool.consequence_counter == 200_000,
            "alternate_tool_counter_zero":
                alternate_tool.consequence_counter == 0,
            "identity_sequence_exact": identity_exact,
            "unique_attempt_ids_1000000":
                identity_exact and processed == 1_000_000,
            "unique_presenter_ids_1000000":
                identity_exact and processed == 1_000_000,
            "authority_bearing_count_800000":
                authority_bearing == 800_000,
            "unique_authority_ids_800000":
                identity_exact and authority_bearing == 800_000,
            "all_record_behavior_exact": behavior_exact,
            "shard_count_100":
                len(
                    list(
                        EVIDENCE_DIR.glob(
                            "EASA-F16-X1M-DECISIONS-*.jsonl.gz"
                        )
                    )
                ) == 100,
            "every_shard_record_count_10000":
                all(x["record_count"] == 10_000 for x in shards),
            "shard_ranges_contiguous":
                all(
                    x["chunk_number"] == pos
                    for pos, x in enumerate(shards, start=1)
                ),
            "global_decision_digest_present":
                len(global_decision_digest) == 64,
            "shard_manifest_digest_present":
                len(manifest_digest) == 64,
            "max_workers_64": MAX_WORKERS == 64,
            "no_intermediate_population_claim": True,
        }

        overall = all(checks.values())

        summary_core = {
            "examination": EXAMINATION,
            "property":
                "BOUNDED_AUTHORIZATION_REFUSAL_PRESERVATION_AT_N_1000000",
            "target_population": TOTAL_ATTEMPTS,
            "chunk_size": CHUNK_SIZE,
            "chunk_count": CHUNK_COUNT,
            "max_workers": MAX_WORKERS,
            "compression_level": COMPRESSION_LEVEL,
            "class_counts": dict(sorted(class_counts.items())),
            "attempt_count": processed,
            "decision_count": processed,
            "permit_count": verdict_counts["PERMIT"],
            "refuse_count": verdict_counts["REFUSE"],
            "authorized_consequence_total": authorized_consequence,
            "unauthorized_consequence_total": unauthorized_consequence,
            "primary_tool_final_counter":
                primary_tool.consequence_counter,
            "alternate_tool_final_counter":
                alternate_tool.consequence_counter,
            "unique_attempt_id_count": processed,
            "unique_presenter_id_count": processed,
            "authority_bearing_attempt_count": authority_bearing,
            "unique_authority_id_count": authority_bearing,
            "refusal_reason_counts":
                dict(sorted(reason_counts.items())),
            "canonical_order": "ATTEMPT_ID_ASCENDING",
            "canonical_decision_stream":
                "COMPACT_SORTED_JSON_UTF8_PLUS_LF",
            "canonical_decision_digest_sha256":
                global_decision_digest,
            "canonical_shard_manifest_digest_sha256":
                manifest_digest,
            "total_compressed_evidence_bytes":
                total_compressed_bytes,
            "elapsed_execution_seconds": elapsed,
            "checks": checks,
            "overall_result": "PASS" if overall else "FAIL",
            "claim_state":
                "OBSERVATION_SUPPORTS_DEFINED_PROPERTY_AT_N_1000000"
                if overall
                else
                "DEFINED_PROPERTY_AT_N_1000000_NOT_ESTABLISHED_BY_FIRST_OBSERVATION",
        }

        summary_digest = sha256_hex(canonical_bytes(summary_core))
        summary = dict(summary_core)
        summary["canonical_summary_digest_sha256"] = summary_digest
        write_json(SUMMARY_PATH, summary)

        print("=== EASA-F16-X1M FIRST OBSERVATION ===")
        print(f"TARGET_POPULATION={TOTAL_ATTEMPTS}")
        print(f"MAX_WORKERS={MAX_WORKERS}")
        print(f"CHUNK_SIZE={CHUNK_SIZE}")
        print(f"CHUNK_COUNT={CHUNK_COUNT}")
        print(f"ATTEMPT_COUNT={processed}")
        print(f"DECISION_COUNT={processed}")
        print(f"AUTHORIZED_COUNT={class_counts['AUTHORIZED']}")
        print(f"NO_AUTHORITY_COUNT={class_counts['NO_AUTHORITY']}")
        print(
            "PRESENTER_IDENTITY_MISMATCH_COUNT="
            f"{class_counts['PRESENTER_IDENTITY_MISMATCH']}"
        )
        print(
            "TOOL_IDENTITY_MISMATCH_COUNT="
            f"{class_counts['TOOL_IDENTITY_MISMATCH']}"
        )
        print(
            "PRECONSUMED_REPLAY_COUNT="
            f"{class_counts['PRECONSUMED_AUTHORITY_REPLAY']}"
        )
        print(f"PERMIT_COUNT={verdict_counts['PERMIT']}")
        print(f"REFUSE_COUNT={verdict_counts['REFUSE']}")
        print(
            f"AUTHORIZED_CONSEQUENCE_TOTAL={authorized_consequence}"
        )
        print(
            f"UNAUTHORIZED_CONSEQUENCE_TOTAL={unauthorized_consequence}"
        )
        print(
            "PRIMARY_TOOL_FINAL_COUNTER="
            f"{primary_tool.consequence_counter}"
        )
        print(
            "ALTERNATE_TOOL_FINAL_COUNTER="
            f"{alternate_tool.consequence_counter}"
        )
        print(f"UNIQUE_ATTEMPT_IDS={processed}")
        print(f"UNIQUE_PRESENTER_IDS={processed}")
        print(f"AUTHORITY_BEARING_ATTEMPTS={authority_bearing}")
        print(f"UNIQUE_AUTHORITY_IDS={authority_bearing}")
        print(f"DECISION_SHARDS={len(shards)}")
        print(
            "GLOBAL_DECISION_DIGEST_SHA256="
            f"{global_decision_digest}"
        )
        print(
            "SHARD_MANIFEST_DIGEST_SHA256="
            f"{manifest_digest}"
        )
        print(f"SUMMARY_DIGEST_SHA256={summary_digest}")
        print(
            "TOTAL_COMPRESSED_EVIDENCE_BYTES="
            f"{total_compressed_bytes}"
        )
        print(f"ELAPSED_EXECUTION_SECONDS={elapsed}")
        print(f"ALL_CHECKS_TRUE={all(checks.values())}")
        print(f"OVERALL_RESULT={summary['overall_result']}")
        print(f"CLAIM_STATE={summary['claim_state']}")

        return 0 if overall else 1

    except BaseException as exc:
        elapsed = round(time.perf_counter() - started, 6)
        failure = {
            "examination": EXAMINATION,
            "result": "FAIL",
            "claim_state":
                "DEFINED_PROPERTY_AT_N_1000000_NOT_ESTABLISHED_BY_FIRST_OBSERVATION",
            "current_chunk_number": current_chunk,
            "completed_chunk_count": len(shards),
            "processed_attempt_count": processed,
            "partial_results_collected_in_failed_chunk":
                partial_results,
            "primary_tool_counter":
                primary_tool.consequence_counter,
            "alternate_tool_counter":
                alternate_tool.consequence_counter,
            "error_type": type(exc).__name__,
            "error_message": str(exc),
            "traceback": traceback.format_exc(),
            "elapsed_execution_seconds": elapsed,
            "historical_harness_rerun": False,
            "retrospective_repair": False,
        }
        try:
            write_json(FAILURE_PATH, failure)
        except Exception as preserve_error:
            print(
                "FAILURE_RECORD_WRITE_ERROR="
                f"{type(preserve_error).__name__}:{preserve_error}"
            )
        print("=== EASA-F16-X1M FIRST OBSERVATION FAILURE ===")
        print("OVERALL_RESULT=FAIL")
        print(
            "CLAIM_STATE="
            "DEFINED_PROPERTY_AT_N_1000000_NOT_ESTABLISHED_BY_FIRST_OBSERVATION"
        )
        print(f"CURRENT_CHUNK={current_chunk}")
        print(f"COMPLETED_CHUNKS={len(shards)}")
        print(f"PROCESSED_ATTEMPTS={processed}")
        print(f"ERROR_TYPE={type(exc).__name__}")
        print(f"ERROR_MESSAGE={exc}")
        print(f"ELAPSED_EXECUTION_SECONDS={elapsed}")
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
