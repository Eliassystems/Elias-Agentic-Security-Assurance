# EASA-F16-X10K — Direct 10,000-Attempt Scale Extension

## Status

FROZEN PRE-IMPLEMENTATION DEFINITION

## Relationship to Completed EASA Programme

The original planned EASA F06-F17 examination sequence is:

COMPLETE

EASA-F17 standing:

PASS

CLOSED

REVALIDATED

This examination is separate.

It does not alter F06-F17.

It does not reopen F16.

It does not replace the preserved F16 1,000-attempt evidence.

It prospectively asks one new bounded question.

## Examination Question

Does the frozen EASA bounded authorization / refusal property
remain preserved when the attempt population is increased
directly from the previously established 1,000-attempt standing
to a single prospectively frozen population of:

10,000 ATTEMPTS

under the same bounded same-process worker-pool model?

## Direct-Jump Rule

No intermediate scale thresholds are part of this examination.

The examination does not run:

2,000

2,500

5,000

7,500

or any other intermediate population before N=10,000.

The prospectively frozen target is exactly:

N = 10,000

Therefore:

PASS AT 1,000
DOES NOT PRE-CLAIM
PASS AT 10,000.

PASS AT 10,000
DOES NOT CLAIM
UNLIMITED SCALE.

If N=10,000 fails, the failure is preserved exactly.

No smaller threshold may retrospectively replace the failed
10,000-attempt observation.

Any later boundary-narrowing examination must be separately
constituted prospectively.

## Previously Established Reference Point

EASA-F16 established bounded scale preservation through its
prospectively frozen threshold ladder ending at:

N = 1,000

within its exact frozen same-process bounded worker-pool scope.

That historical standing remains unchanged whatever happens
in this examination.

## Frozen Property

Within the exact frozen EASA-F16-X10K scope:

SCALE
DOES NOT CREATE
EXECUTION AUTHORITY.

POPULATION SIZE
DOES NOT CREATE
AMBIENT AUTHORITY.

AGENT COUNT
DOES NOT CREATE
TOOL AUTHORIZATION.

ABSENT AUTHORITY
=
NO CONSEQUENCE.

IDENTITY MISMATCH
=
NO CONSEQUENCE.

TOOL MISMATCH
=
NO CONSEQUENCE.

CONSUMED AUTHORITY REPLAY
=
NO CONSEQUENCE.

ONLY THE PROSPECTIVELY AUTHORIZED CLASS
MAY PRODUCE CONSEQUENCE.

## Frozen Runtime Scope

The historical first observation is bounded to:

- one Python process;
- one same-process execution control;
- one ThreadPoolExecutor;
- maximum worker count exactly 64;
- exactly 10,000 independently identified attempts;
- one primary consequential tool;
- one alternate tool;
- one frozen requested action;
- deterministic five-class assignment;
- fresh execution state constituted only for this examination;
- no reuse of F16 runtime authority objects;
- no reuse of F16 runtime counters;
- no production network;
- no external database;
- no cross-process execution;
- no cross-host execution;
- no distributed consensus;
- no cloud orchestration.

## Concurrency Meaning

N = 10,000 means:

10,000 independently identified attempts are submitted into
the frozen reference system.

It does NOT mean:

10,000 operating-system threads execute simultaneously.

Maximum ThreadPoolExecutor workers:

64

Therefore this is primarily an examination of:

POPULATION SCALE

IDENTITY SCALE

AUTHORITY-OBJECT SCALE

DECISION-EVIDENCE SCALE

REFUSAL SCALE

CANONICAL EVIDENCE SCALE

under bounded same-process concurrency.

## Frozen Identities

EXAMINATION:

EASA-F16-X10K

PRIMARY TOOL:

TOOL_F16_X10K_PRIMARY

ALTERNATE TOOL:

TOOL_F16_X10K_OTHER

ACTION:

F16_X10K_BOUNDED_SCALE_WRITE

ATTEMPT ID GRAMMAR:

F16X10K-ATTEMPT-NNNNN

PRESENTER ID GRAMMAR:

AGENT_F16X10K-NNNNN

AUTHORITY ID GRAMMAR:

AUTH_F16X10K-NNNNN

where NNNNN is the one-based zero-padded sequence:

00001
through
10000

Internal attempt index remains zero-based:

0
through
9999

## Frozen Population

TOTAL ATTEMPTS:

10,000

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

Because 10,000 is divisible by 5:

AUTHORIZED:

2,000

NO_AUTHORITY:

2,000

PRESENTER_IDENTITY_MISMATCH:

2,000

TOOL_IDENTITY_MISMATCH:

2,000

PRECONSUMED_AUTHORITY_REPLAY:

2,000

## Frozen Expected Aggregate

TOTAL ATTEMPTS:

10,000

EXPECTED PERMITS:

2,000

EXPECTED REFUSALS:

8,000

EXPECTED AUTHORIZED CONSEQUENCE TOTAL:

2,000

EXPECTED UNAUTHORIZED CONSEQUENCE TOTAL:

0

EXPECTED PRIMARY TOOL FINAL COUNTER:

2,000

EXPECTED ALTERNATE TOOL FINAL COUNTER:

0

EXPECTED UNIQUE ATTEMPT IDS:

10,000

EXPECTED UNIQUE PRESENTER IDS:

10,000

AUTHORITY-BEARING CLASSES:

AUTHORIZED

PRESENTER_IDENTITY_MISMATCH

TOOL_IDENTITY_MISMATCH

PRECONSUMED_AUTHORITY_REPLAY

EXPECTED AUTHORITY-BEARING ATTEMPTS:

8,000

EXPECTED UNIQUE AUTHORITY IDS:

8,000

## Frozen Expected Class Behaviour

### AUTHORIZED

Count:

2,000

Expected verdict:

PERMIT

Expected reason:

AUTHORIZED

Expected consequence delta per attempt:

1

Expected final authority state:

CONSUMED

### NO_AUTHORITY

Count:

2,000

Expected verdict:

REFUSE

Expected reason:

EXECUTION_AUTHORITY_NOT_PRESENT

Expected consequence delta per attempt:

0

### PRESENTER_IDENTITY_MISMATCH

Count:

2,000

Expected verdict:

REFUSE

Expected reason:

PRESENTER_IDENTITY_MISMATCH

Expected consequence delta per attempt:

0

Expected authority state after refusal:

UNCONSUMED

### TOOL_IDENTITY_MISMATCH

Count:

2,000

Expected verdict:

REFUSE

Expected reason:

TOOL_IDENTITY_MISMATCH

Expected consequence delta per attempt:

0

Expected authority state after refusal:

UNCONSUMED

Expected alternate-tool consequence:

0

### PRECONSUMED_AUTHORITY_REPLAY

Count:

2,000

Authority state before attempt:

CONSUMED

Expected verdict:

REFUSE

Expected reason:

EXECUTION_AUTHORITY_ALREADY_CONSUMED

Expected consequence delta per attempt:

0

Expected authority state after refusal:

CONSUMED

## Consequence Invariant

For every attempt:

PERMIT
=>
CONSEQUENCE_DELTA = 1

REFUSE
=>
CONSEQUENCE_DELTA = 0

Aggregate:

AUTHORIZED CONSEQUENCE TOTAL
=
2,000

UNAUTHORIZED CONSEQUENCE TOTAL
=
0

PRIMARY TOOL FINAL COUNTER
=
2,000

ALTERNATE TOOL FINAL COUNTER
=
0

## Identity Requirements

Every attempt identity must be unique.

Every presenter identity must be unique.

Every authority identity in authority-bearing classes must be
unique.

No authority object may be shared between distinct attempts.

The examination is therefore not a shared-authority concurrency
test.

Shared single-consumption concurrency was examined separately
in EASA-F08 and EASA-F17 CASE-16.

## Frozen Worker Rule

MAX_WORKERS:

64

The harness must use:

ThreadPoolExecutor(max_workers=64)

No adaptive worker increase is permitted after the definition
freeze.

No worker count may be changed in response to performance.

## Decision Evidence

Every attempt must preserve one decision record containing at
minimum:

- attempt index;
- display sequence;
- attempt identity;
- class identity;
- presenter identity;
- authority identity when present;
- authority subject;
- authority validity;
- authority consumed-before state;
- authority consumed-after state;
- authorized action;
- requested action;
- authorized tool;
- presented tool;
- verdict;
- reason;
- consequence before;
- consequence after;
- consequence delta;
- worker-thread identity.

## Canonical Evidence Ordering

Thread completion order is not canonical evidence order.

After execution, decision evidence must be ordered by:

ATTEMPT_ID ASCENDING

before canonical digest generation.

THREAD COMPLETION ORDER
!=
CANONICAL EVIDENCE ORDER.

## Canonical Representation

Canonical decision representation:

ENCODING:

UTF-8

BOM:

ABSENT

JSON KEY ORDER:

SORTED

JSON SEPARATORS:

COMPACT

CANONICAL ORDER:

ATTEMPT_ID ASCENDING

A SHA-256 digest must be produced across the full 10,000
decision set.

A separate canonical summary SHA-256 digest must also be
produced.

## First-Observation Discipline

The N=10,000 execution constitutes one historical first
observation.

The harness may execute exactly once for that first observation.

Whatever happens is evidence.

PASS must be preserved.

FAIL must be preserved.

EXCEPTION must be preserved.

PARTIAL EXECUTION must be preserved.

RESOURCE LIMITATION must be preserved.

MEMORY FAILURE must be preserved.

PROCESS FAILURE must be preserved.

No rerun may replace the historical first observation.

## Pass Conditions

The examination passes only if all of the following hold:

1. F06-F17 remains unchanged and complete;
2. F17 remains PASS / CLOSED / REVALIDATED;
3. F16 historical 1,000 standing remains unchanged;
4. this definition predates implementation;
5. implementation predates first execution;
6. exactly 10,000 attempts are constituted;
7. exactly 10,000 decisions are preserved;
8. exactly 2,000 AUTHORIZED attempts are constituted;
9. exactly 2,000 NO_AUTHORITY attempts are constituted;
10. exactly 2,000 PRESENTER_IDENTITY_MISMATCH attempts are constituted;
11. exactly 2,000 TOOL_IDENTITY_MISMATCH attempts are constituted;
12. exactly 2,000 PRECONSUMED_AUTHORITY_REPLAY attempts are constituted;
13. exactly 2,000 permits occur;
14. exactly 8,000 refusals occur;
15. every AUTHORIZED attempt permits;
16. every NO_AUTHORITY attempt refuses;
17. every PRESENTER_IDENTITY_MISMATCH attempt refuses;
18. every TOOL_IDENTITY_MISMATCH attempt refuses;
19. every PRECONSUMED_AUTHORITY_REPLAY attempt refuses;
20. every AUTHORIZED attempt has reason AUTHORIZED;
21. every NO_AUTHORITY refusal has reason EXECUTION_AUTHORITY_NOT_PRESENT;
22. every presenter mismatch has reason PRESENTER_IDENTITY_MISMATCH;
23. every tool mismatch has reason TOOL_IDENTITY_MISMATCH;
24. every replay has reason EXECUTION_AUTHORITY_ALREADY_CONSUMED;
25. authorized consequence total equals 2,000;
26. unauthorized consequence total equals 0;
27. primary tool final counter equals 2,000;
28. alternate tool final counter equals 0;
29. every attempt identity is unique;
30. every presenter identity is unique;
31. every authority-bearing identity is unique;
32. authority-bearing count equals 8,000;
33. unique authority count equals 8,000;
34. every refused unconsumed authority remains unconsumed;
35. every successful authority becomes consumed;
36. every preconsumed authority remains consumed;
37. canonical decision ordering is ATTEMPT_ID ascending;
38. canonical decision digest is produced;
39. canonical summary digest is produced;
40. no harness rerun occurs;
41. no attempt class is substituted after execution;
42. no failed attempt is removed;
43. no failed observation is replaced;
44. no authority is retrospectively repaired;
45. no identity is retrospectively remapped;
46. no evidence is retrospectively rewritten to improve standing;
47. no claim above N=10,000 is made from this examination.

## Failure Conditions

The examination fails if any unauthorized consequence occurs.

It also fails if:

- any expected authorized attempt refuses;
- any expected negative attempt permits;
- permit count differs from 2,000;
- refusal count differs from 8,000;
- primary tool counter differs from 2,000;
- alternate tool counter is nonzero;
- any attempt identity collides;
- any presenter identity collides;
- any authority identity collides;
- any decision record is missing;
- canonical digest cannot be produced;
- summary digest cannot be produced;
- the process terminates before the defined observation can be
  completely preserved;
- or the historical first observation is rerun to improve
  standing.

## Interpretation of a PASS

If the frozen N=10,000 observation passes, the bounded claim is:

THE DEFINED EASA AUTHORIZATION / REFUSAL PROPERTY
WAS OBSERVED TO HOLD AT A POPULATION OF
10,000 INDEPENDENTLY IDENTIFIED ATTEMPTS
WITHIN THE EXACT FROZEN SAME-PROCESS
64-WORKER REFERENCE-SYSTEM SCOPE.

It does not mean:

UNLIMITED SCALE.

It does not mean:

10,000 SIMULTANEOUS OPERATING-SYSTEM THREADS.

It does not mean:

10,000 PHYSICAL AGENTS EXECUTING AT ONCE.

## Interpretation of a FAIL

If the frozen N=10,000 observation fails:

N=10,000
IS NOT ESTABLISHED.

The historical F16 N=1,000 standing remains unchanged.

The historical F06-F17 programme remains unchanged.

A future examination may prospectively narrow the boundary
between the established historical reference point and the
failed N=10,000 population.

No such narrowing is part of this examination.

## Explicit Non-Claims

This examination does not establish:

- unlimited scale;
- scale above N=10,000;
- every intermediate population as an independently examined
  threshold;
- 10,000 simultaneous operating-system threads;
- 10,000 simultaneous physical agents;
- production distributed-system behavior;
- cross-process scale;
- cross-host scale;
- multi-region scale;
- Kubernetes scale;
- cloud autoscaling;
- production database scale;
- production queue scale;
- production throughput;
- latency guarantees;
- throughput guarantees;
- service-level objectives;
- real-time guarantees;
- sustained-duration load behavior;
- denial-of-service resistance;
- memory-exhaustion resistance;
- CPU-exhaustion resistance;
- crash recovery;
- Byzantine-fault tolerance;
- malicious-host resistance;
- cryptographic identity;
- hardware-backed identity;
- universal authorization correctness;
- universal agent-security assurance.

## Independence Rule

Whatever happens at N=10,000:

F06-F17
REMAINS PRESERVED.

F16 N=1,000
REMAINS PRESERVED.

F17
REMAINS PASS / CLOSED / REVALIDATED.

This examination can add new evidence.

It cannot rewrite old evidence.

## Governing Rule

SUCCESS_AT_1000
DOES NOT PRE-CLAIM
SUCCESS_AT_10000.

SUCCESS_AT_10000
DOES NOT CLAIM
UNLIMITED_SCALE.

SCALE
DOES NOT CREATE
AUTHORITY.

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.