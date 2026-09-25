# Elias X1M Performance Examination — v0.1

**Status:** FROZEN — BOUNDED EXPERIMENTAL PERFORMANCE EVIDENCE

This release preserves a performance examination of an experimental Shadow V3 execution-governance path against the existing frozen Elias X1M baseline.

## Result

Persisted-source re-examination recorded:

- 100,000 generated sequential comparisons;
- 21 corresponding decision values;
- 0 observed field-value mismatches;
- 600 bounded contention rounds;
- 0 observed contention-property failures;
- 10 fresh-process ABBA performance runs;
- V3 faster in all 10 ABBA runs;
- V3 faster on all 7 tested governance paths.

Canonical persisted ABBA result:

- Frozen baseline aggregate mean: 7.128 microseconds
- Shadow V3 aggregate mean: 1.719 microseconds
- Ratio of aggregate means: 4.146x
- Measured latency reduction: 75.9%

Seven-path measured reductions ranged from 71.8% to 80.6%.

## What changed experimentally

The principal performance change replaced the expensive frozen dataclass decision construction on the experimental path with a raw tuple-form decision record while retaining the examined governance checks and single-use authority locking behavior.

## Important API boundary

The frozen baseline returns an ExecutionDecision dataclass.

Shadow V3 returns a raw tuple.

The examination supports equality of the tested 21 corresponding values within the bounded generated comparison population.

It does not establish drop-in Python API compatibility.

## Non-claims

This release does not claim production readiness, universal latency, hardware independence, exhaustive equivalence, exhaustive concurrency correctness, sub-microsecond repeatable latency, or replacement authority for the frozen baseline.

## Reproducibility

The package contains:

- exact persisted Shadow V3 source;
- persisted performance harness;
- environment receipt;
- semantic comparison receipt;
- contention receipt;
- raw CSV performance results;
- canonical performance summary;
- measurement correction history;
- wrapper anomaly record;
- SHA-256 manifest.

**Evidence stops where the evidence stops.**

**Lock it. Log it. Prove it.**
