# Final Reconciliation

Package ID: ELIAS_X1M_PERFORMANCE_EXAMINATION_V0.1_20260925

Frozen evidence timestamp: 2026-09-25T00:45:53.8932315+01:00

Status:

**FROZEN — BOUNDED EXPERIMENTAL PERFORMANCE EVIDENCE**

## Frozen baseline

Source:

03_controls/easa_f16_x1m_execution.py

SHA-256:

85ac55b617aacd714252a995558fed74d6b6e330dd4055d7d2b9f29ae59971de

The baseline source remained unchanged throughout the examination.

## Persisted Shadow V3

Source:

REPRODUCTION/shadow_v3_gate.py

SHA-256:

8c2f054fd4d2a9b9ec3684bdd73817d9e7a5c5e076d039aebb7928edae5f696f

## Persisted performance harness

Source:

REPRODUCTION/persisted_v3_performance_reexecution.py

SHA-256:

cea268cd8a4468cec2ab6b59493035f82ea23b324f5cd414fb0c929c1e569ce6

## Core re-examination

Observed:

- generated sequential comparisons: 100,000
- corresponding decision values compared: 21
- observed mismatches: 0
- total contention rounds: 600
- observed contention property failures: 0

## Canonical persisted performance result

Ten fresh-process ABBA batches:

CURRENT -> V3 -> V3 -> CURRENT

Authority construction was outside the timed region.

Aggregate CURRENT mean: 7.128 microseconds

Aggregate Shadow V3 mean: 1.719 microseconds

Ratio of aggregate means: 4.146x

Measured latency reduction: 75.9%

Shadow V3 was faster in all ten persisted ABBA processes.

## Seven-path persisted matrix

Shadow V3 was faster on all seven tested paths.

Observed measured reductions ranged from 71.8% to 80.6%.

## Historical measurement reconciliation

Earlier in-memory and pre-persistence results remain preserved.

The earlier approximately 0.917 microsecond same-run V3 observation did not survive fresh-process repeatability testing.

SUB_MICROSECOND_REPEATABLE_CLAIM = NOT ESTABLISHED

## PowerShell wrapper anomaly

The blank/null Process.ExitCode wrapper observation remains preserved.

It was not retrospectively rewritten.

Independent disk verification subsequently verified the persisted evidence artifacts.

## API boundary

The examination established bounded equality of 21 corresponding decision values in the tested population.

It did not establish Python object-type or drop-in API equivalence.

The frozen baseline returns an ExecutionDecision dataclass.

Shadow V3 returns a raw tuple.

See API_COMPATIBILITY_BOUNDARY.md.

## Final evidence standing

CORE_REEXECUTION: VERIFIED

PERSISTED_PERFORMANCE: VERIFIED

BASELINE_MODIFIED: NO

SHADOW_V3_STATUS: EXPERIMENTAL

EVIDENCE_PACKAGE_STATUS: FROZEN_BOUNDED_EXPERIMENTAL_EVIDENCE

BASELINE_REPLACEMENT_AUTHORITY: NO

PRODUCTION_READINESS: NOT_ESTABLISHED

DROP_IN_API_COMPATIBILITY: NOT_ESTABLISHED

EXTERNAL_CERTIFICATION: NOT_ESTABLISHED

Evidence stops where the evidence stops.

Lock it. Log it. Prove it.
