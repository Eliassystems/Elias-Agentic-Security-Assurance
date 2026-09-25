# Elias X1M Performance Examination

Package ID:

ELIAS_X1M_PERFORMANCE_EXAMINATION_V0.1_20260925

Status:

**FROZEN — BOUNDED EXPERIMENTAL PERFORMANCE EVIDENCE**

## Canonical finding

Under the exact persisted-source examination and recorded environment, the experimental Shadow V3 governance path showed:

- frozen baseline aggregate mean: 7.128 microseconds
- Shadow V3 aggregate mean: 1.719 microseconds
- ratio of aggregate means: 4.146x
- measured latency reduction: 75.9%

The comparison used ten fresh-process ABBA runs with authority construction outside the timed region.

Shadow V3 was also faster on all seven tested governance paths.

## Core evidence

- 100,000 generated sequential comparisons
- 21 corresponding decision values
- 0 observed mismatches
- 600 bounded contention rounds
- 0 observed property failures

## Exact identities

Frozen baseline SHA-256:

85ac55b617aacd714252a995558fed74d6b6e330dd4055d7d2b9f29ae59971de

Persisted Shadow V3 SHA-256:

8c2f054fd4d2a9b9ec3684bdd73817d9e7a5c5e076d039aebb7928edae5f696f

Persisted performance harness SHA-256:

cea268cd8a4468cec2ab6b59493035f82ea23b324f5cd414fb0c929c1e569ce6

## Read first

- FINAL_RECONCILIATION.md
- CLAIMS_AND_NONCLAIMS.md
- API_COMPATIBILITY_BOUNDARY.md
- PROTOCOL.md
- RELEASE_NOTES.md
- MEASUREMENT_HISTORY.md

## Important boundary

Shadow V3 remains experimental.

This package freezes evidence of the examination.

It does not authorize replacement of the existing frozen baseline.

The V3 raw tuple and baseline ExecutionDecision dataclass are not claimed to be drop-in API equivalents.

## Historical preservation

Pre-persistence documents and execution anomalies remain in the package.

They have not been retrospectively deleted or repaired.

Evidence stops where the evidence stops.

Lock it. Log it. Prove it.
