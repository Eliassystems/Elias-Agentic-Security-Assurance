# Claims and Non-Claims

## Supported within the frozen examination scope

The exact persisted Shadow V3 artifact produced zero observed field-value mismatches across 100,000 generated sequential comparisons against the frozen baseline across 21 corresponding decision values.

The persisted Shadow V3 artifact completed 600 bounded single-use authority contention rounds with zero observed property failures.

Under the persisted ten-fresh-process ABBA batch protocol:

- frozen CURRENT aggregate mean: 7.128 microseconds
- Shadow V3 aggregate mean: 1.719 microseconds
- ratio of aggregate means: 4.146x
- measured latency reduction: 75.9%

Under the persisted seven-path matrix, Shadow V3 showed lower measured latency on all seven tested paths.

Observed seven-path reductions ranged from 71.8% to 80.6%.

Authority and benchmark-state construction was outside the timed region where specified by the protocol.

The frozen baseline remained unchanged.

## Non-claims

This package does not establish:

- a universal latency guarantee;
- production latency;
- end-to-end distributed-system latency;
- hardware-independent performance;
- exhaustive semantic equivalence;
- exhaustive concurrency correctness;
- correctness under every scheduler or interleaving;
- a sub-microsecond repeatable latency claim;
- general transactions-per-second capacity;
- superiority over third-party systems;
- production readiness;
- baseline replacement authority;
- external certification;
- Python object-type equivalence;
- named-attribute API compatibility;
- drop-in replacement compatibility.

## Representation boundary

The frozen baseline returns an ExecutionDecision frozen dataclass.

Shadow V3 returns a raw tuple.

The examination supports bounded equality of the tested 21 corresponding values and field order.

It does not support a claim that the two return objects expose the same Python API.

## Standing

SHADOW_V3: EXPERIMENTAL

PACKAGE: FROZEN BOUNDED EXPERIMENTAL PERFORMANCE EVIDENCE

Evidence stops where the evidence stops.
