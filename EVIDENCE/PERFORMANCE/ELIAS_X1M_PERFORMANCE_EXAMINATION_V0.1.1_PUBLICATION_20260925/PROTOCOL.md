# Examination Protocol

## Baseline identity

03_controls/easa_f16_x1m_execution.py

SHA-256:

85ac55b617aacd714252a995558fed74d6b6e330dd4055d7d2b9f29ae59971de

## Experimental artifact identity

REPRODUCTION/shadow_v3_gate.py

SHA-256:

8c2f054fd4d2a9b9ec3684bdd73817d9e7a5c5e076d039aebb7928edae5f696f

## Performance harness identity

REPRODUCTION/persisted_v3_performance_reexecution.py

SHA-256:

cea268cd8a4468cec2ab6b59493035f82ea23b324f5cd414fb0c929c1e569ce6

## Core comparison

100,000 deterministically generated cases spanning:

- NO_AUTHORITY
- INVALID_AUTHORITY
- ALREADY_CONSUMED
- IDENTITY_MISMATCH
- ACTION_MISMATCH
- TOOL_MISMATCH
- AUTHORIZED

Twenty-one corresponding decision values were compared.

Observed mismatches: 0

## Contention examination

Worker counts:

2, 4, 8, 16, 32, 64

Rounds per worker count: 100

Total rounds: 600

Required per round:

- exactly one PERMIT;
- all other contenders REFUSE;
- total consequence delta = 1;
- final consequence counter = 1.

Observed failures: 0

## Performance comparison

Ten fresh Python processes.

ABBA order:

CURRENT -> V3 -> V3 -> CURRENT

100,000 decisions per batch.

Authority construction was outside the timed region.

Canonical persisted result:

CURRENT = 7.128 us
V3      = 1.719 us
RATIO   = 4.146x
REDUCTION = 75.9%

## Seven-path matrix

100,000 samples per path per repeat.

Five repeats.

All seven persisted paths showed lower measured latency under V3.

## API compatibility

Performance and field-value examination does not constitute API compatibility examination.

See API_COMPATIBILITY_BOUNDARY.md.

## Historical execution anomalies

Historical failed and interrupted wrapper attempts and the blank/null PowerShell Process.ExitCode observation remain preserved in the evidence package.

No retrospective repair has been applied.
