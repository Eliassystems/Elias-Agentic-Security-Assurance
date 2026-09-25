# Examination Protocol

## Baseline

Frozen implementation:

03_controls/easa_f16_x1m_execution.py

The baseline source was not modified during the observed examination.

## Experimental optimization direction

The experimental V3 work preserved the examined decision information
surface while reducing Python runtime representation overhead.

The principal observed optimization direction included:

- replacement of the expensive frozen dataclass decision construction
  in the experimental path with an immutable tuple-form receipt;
- retention of the 21 compared decision values in fixed field order;
- retention of authority presence validation;
- retention of authority validity validation;
- retention of prior-consumption validation;
- retention of presenter identity binding;
- retention of requested-action binding;
- retention of tool-identity binding;
- retention of the authority lock around single-use consequential
  execution;
- retention of consequential-tool execution locking behavior inherited
  from the existing tool object.

## Sequential equivalence population

100,000 generated cases cycling through seven path classes:

1. NO_AUTHORITY
2. INVALID_AUTHORITY
3. ALREADY_CONSUMED
4. IDENTITY_MISMATCH
5. ACTION_MISMATCH
6. TOOL_MISMATCH
7. AUTHORIZED

The current and V3 outputs were compared across 21 corresponding
decision values.

Observed mismatches: 0.

## Contention examination

One single-use authority was presented concurrently by:

2
4
8
16
32
64

workers.

100 rounds were executed for each worker count.

Required property:

- exactly one PERMIT;
- every other contender REFUSE;
- total consequence delta exactly 1;
- final consequence counter exactly 1.

Observed failures: 0.

## ABBA performance protocol

Ten fresh Python processes.

Within each process:

CURRENT_A
V3_A
V3_B
CURRENT_B

Each batch contained 100,000 decisions.

Authority objects were constructed before the timed region.

## Seven-path matrix

Seven decision paths were separately measured.

100,000 samples per path per repeat.
Five repeats.

Authority setup was outside the timed region.

## Evidence limitation

The experimental V3 code was executed in-memory from Python supplied
through PowerShell.

A persisted V3 source artifact is therefore required and must be
re-executed before this package can be marked frozen for release.
