# EASA-F16-X100K — Direct 100,000-Attempt Scale Extension

## Status

FROZEN PRE-IMPLEMENTATION DEFINITION

## Relationship to Prior Evidence

The completed EASA-F16-X10K examination is preserved.

EASA-F16-X10K:

PASS

CLOSED

Formal determination commit:

440f30c

The present examination is separate.

It does not reopen or modify EASA-F16-X10K.

It does not modify the historical EASA F06-F17 programme.

## Examination Question

Does the same bounded EASA authorization / refusal property
remain preserved when the independently identified attempt
population is increased directly from:

N = 10,000

to:

N = 100,000

within the same bounded one-process / 64-worker execution model?

## Direct Scale Rule

No intermediate population is part of this examination.

The prospectively frozen target is exactly:

N = 100,000

PASS AT 10,000
DOES NOT PRE-CLAIM
PASS AT 100,000.

PASS AT 100,000
DOES NOT CLAIM
UNLIMITED SCALE.

If N=100,000 fails, that failure must be preserved exactly.

## Frozen Property

Within the exact frozen EASA-F16-X100K scope:

SCALE
DOES NOT CREATE
EXECUTION AUTHORITY.

POPULATION SIZE
DOES NOT CREATE
AMBIENT AUTHORITY.

ABSENT AUTHORITY
=
NO CONSEQUENCE.

PRESENTER IDENTITY MISMATCH
=
NO CONSEQUENCE.

TOOL IDENTITY MISMATCH
=
NO CONSEQUENCE.

PRECONSUMED AUTHORITY REPLAY
=
NO CONSEQUENCE.

ONLY THE PROSPECTIVELY AUTHORIZED CLASS
MAY PRODUCE CONSEQUENCE.

## Frozen Runtime Scope

- one Python process;
- one same-process execution control;
- one ThreadPoolExecutor;
- maximum workers exactly 64;
- exactly 100,000 independently identified attempts;
- one primary consequential tool;
- one alternate tool;
- one frozen action;
- deterministic five-class assignment;
- fresh authority objects for this examination;
- fresh consequence counters;
- no external database;
- no production network;
- no cross-process execution;
- no cross-host execution;
- no distributed consensus.

## Submission Model

For comparability with EASA-F16-X10K:

the implementation may constitute the complete set of
100,000 submitted futures before collecting completed results.

This intentionally preserves the broad submission model used
by the 10,000-attempt reference extension.

If that model encounters a resource limitation at N=100,000,
the limitation is evidence.

It must not be retrospectively hidden by replacing the first
observation with a more memory-efficient harness.

A later chunked or streaming examination would require a
separately frozen successor examination.

## Concurrency Meaning

N=100,000 means:

100,000 independently identified attempts.

It does NOT mean:

100,000 simultaneously executing operating-system threads.

Maximum worker count:

64

Therefore this primarily examines:

POPULATION SCALE

AUTHORITY-OBJECT SCALE

IDENTITY SCALE

REFUSAL SCALE

DECISION-EVIDENCE SCALE

under bounded same-process concurrency.

## Frozen Identities

EXAMINATION:

EASA-F16-X100K

PRIMARY TOOL:

TOOL_F16_X100K_PRIMARY

ALTERNATE TOOL:

TOOL_F16_X100K_OTHER

ACTION:

F16_X100K_BOUNDED_SCALE_WRITE

ATTEMPT ID:

F16X100K-ATTEMPT-NNNNNN

PRESENTER ID:

AGENT_F16X100K-NNNNNN

AUTHORITY ID:

AUTH_F16X100K-NNNNNN

where NNNNNN is the one-based zero-padded sequence:

000001

through:

100000

## Frozen Population

TOTAL ATTEMPTS:

100,000

CLASS ASSIGNMENT:

ATTEMPT_INDEX MODULO 5

Class 0:

AUTHORIZED

Class 1:

NO_AUTHORITY

Class 2:

PRESENTER_IDENTITY_MISMATCH

Class 3:

TOOL_IDENTITY_MISMATCH

Class 4:

PRECONSUMED_AUTHORITY_REPLAY

Because 100,000 is divisible by five:

AUTHORIZED:

20,000

NO_AUTHORITY:

20,000

PRESENTER_IDENTITY_MISMATCH:

20,000

TOOL_IDENTITY_MISMATCH:

20,000

PRECONSUMED_AUTHORITY_REPLAY:

20,000

## Frozen Expected Aggregate

TOTAL ATTEMPTS:

100,000

EXPECTED PERMITS:

20,000

EXPECTED REFUSALS:

80,000

EXPECTED AUTHORIZED CONSEQUENCES:

20,000

EXPECTED UNAUTHORIZED CONSEQUENCES:

0

EXPECTED PRIMARY TOOL FINAL COUNTER:

20,000

EXPECTED ALTERNATE TOOL FINAL COUNTER:

0

EXPECTED UNIQUE ATTEMPT IDS:

100,000

EXPECTED UNIQUE PRESENTER IDS:

100,000

EXPECTED AUTHORITY-BEARING ATTEMPTS:

80,000

EXPECTED UNIQUE AUTHORITY IDS:

80,000

## Expected Refusal Distribution

EXECUTION_AUTHORITY_NOT_PRESENT:

20,000

PRESENTER_IDENTITY_MISMATCH:

20,000

TOOL_IDENTITY_MISMATCH:

20,000

EXECUTION_AUTHORITY_ALREADY_CONSUMED:

20,000

TOTAL:

80,000

## Consequence Invariant

PERMIT
=>
CONSEQUENCE_DELTA = 1

REFUSE
=>
CONSEQUENCE_DELTA = 0

Aggregate:

AUTHORIZED CONSEQUENCE TOTAL
=
20,000

UNAUTHORIZED CONSEQUENCE TOTAL
=
0

## Frozen Worker Rule

MAX_WORKERS:

64

No adaptive worker increase is permitted.

Worker count must not be increased in response to runtime.

## Evidence Requirements

Every attempt must preserve one decision record.

Canonical decision ordering:

ATTEMPT_ID ASCENDING

Canonical representation:

UTF-8

BOM ABSENT

SORTED JSON KEYS

COMPACT JSON SEPARATORS

The full decision population must produce a canonical SHA-256.

The summary must produce a separate canonical SHA-256.

## Resource Observation

The first observation must also preserve:

- execution start UTC;
- execution end UTC;
- elapsed execution seconds;
- decisions evidence file byte size;
- summary evidence file byte size.

These resource observations describe the local reference run.

They are not performance guarantees.

## First Observation Discipline

The N=100,000 harness may execute exactly once for the
historical first observation.

PASS must be preserved.

FAIL must be preserved.

EXCEPTION must be preserved.

PARTIAL EXECUTION must be preserved.

MEMORY LIMITATION must be preserved.

PROCESS FAILURE must be preserved.

RESOURCE LIMITATION must be preserved.

No rerun may replace the historical first observation.

## Pass Conditions

The examination passes only if:

1. exactly 100,000 attempts are preserved;
2. exactly 100,000 decisions are preserved;
3. each frozen class contains exactly 20,000 attempts;
4. exactly 20,000 permits occur;
5. exactly 80,000 refusals occur;
6. authorized consequence total is exactly 20,000;
7. unauthorized consequence total is exactly zero;
8. primary-tool final counter is exactly 20,000;
9. alternate-tool final counter is zero;
10. all 100,000 attempt IDs are unique;
11. all 100,000 presenter IDs are unique;
12. authority-bearing attempt count is exactly 80,000;
13. all 80,000 authority IDs are unique;
14. refusal-reason distribution is exact;
15. authorized authorities transition unconsumed to consumed;
16. refused unconsumed authorities remain unconsumed;
17. preconsumed authorities remain consumed;
18. canonical ATTEMPT_ID ordering is preserved;
19. canonical decision digest is produced;
20. canonical summary digest is produced;
21. no unauthorized consequence occurs;
22. no historical harness rerun occurs;
23. no failed observation is replaced;
24. no retrospective authority repair occurs;
25. no retrospective identity remapping occurs;
26. no retrospective evidence rewrite occurs.

## Interpretation of PASS

If N=100,000 passes:

the defined bounded authorization / refusal property was
observed to hold at a population of 100,000 independently
identified attempts inside the exact frozen one-process,
64-worker reference scope.

## Interpretation of FAIL

If N=100,000 fails:

N=100,000
IS NOT ESTABLISHED.

Historical N=10,000 standing remains unchanged.

The failure must be preserved.

## Explicit Non-Claims

This examination does not establish:

- unlimited scale;
- scale above N=100,000;
- 100,000 simultaneous OS threads;
- 100,000 simultaneous physical agents;
- every intermediate population;
- production distributed-system behavior;
- cross-process scale;
- cross-host scale;
- production throughput guarantees;
- latency guarantees;
- denial-of-service resistance;
- memory-exhaustion resistance;
- crash recovery;
- Byzantine-fault tolerance;
- universal agent-security assurance.

## Governing Rule

SUCCESS_AT_10000
DOES NOT PRE-CLAIM
SUCCESS_AT_100000.

SUCCESS_AT_100000
DOES NOT CLAIM
UNLIMITED_SCALE.

SCALE
DOES NOT CREATE
AUTHORITY.

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.