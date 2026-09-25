# Claims and Non-Claims

## Bounded supported observations

Within the exact examined scope:

- 100,000 generated sequential current-versus-V3 comparisons produced
  zero field-level mismatches across the 21 compared decision fields.

- The V3 single-use authority contention examination completed 600
  rounds across 2, 4, 8, 16, 32 and 64 contenders with zero observed
  property failures.

- Under the ten-process ABBA batch protocol, the ratio of aggregate
  CURRENT and V3 means was approximately 4.148x, corresponding to
  approximately 75.9% lower measured latency for V3.

- Under the seven-path batch matrix, V3 showed lower measured latency
  on every tested path, with measured reductions ranging from 72.3%
  to 80.3%.

- The existing frozen implementation remained unchanged during these
  observed examinations.

## Non-claims

This package does NOT establish:

- a universal or production latency guarantee;
- hardware-independent latency;
- network or distributed-system end-to-end latency;
- exhaustive semantic equivalence;
- correctness for every possible concurrent interleaving;
- performance under every operating system or Python implementation;
- performance under sustained production workload;
- superiority over any third-party governance, policy, security,
  trading, industrial, or real-time system;
- a general transactions-per-second capacity claim;
- a sub-microsecond repeatable latency claim;
- production readiness of Shadow V3;
- replacement authority for the frozen baseline;
- external certification or independent validation.

## Timing boundary

Authority object construction was outside the timed region in the ABBA
batch and seven-path batch protocols.

The measured region therefore represents the examined gate decision /
consequence path under those protocols, not full upstream authority
creation or end-to-end system latency.

## Status

Shadow V3 remains experimental.

The persisted V3 artifact has not yet been constituted and re-executed
from disk.

Evidence stops where the evidence stops.
