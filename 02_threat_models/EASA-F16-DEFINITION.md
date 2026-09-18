# EASA-F16 — Bounded Scale Preservation

## Status

FROZEN PRE-IMPLEMENTATION DEFINITION

No EASA-F16 execution control, runtime population, worker pool,
authority population, observation, decision record, evidence
digest, receipt or consequence existed when this definition
was constituted.

## Examination

EASA-F16

Bounded Scale Preservation

## Purpose

Determine whether a frozen authorization and refusal boundary
continues to preserve its defined behavior as the number of
independently identified agent attempts is increased through
a prospectively frozen bounded scale ladder.

The examination does not ask whether the system scales without
limit.

It asks:

At what highest prospectively defined bounded population does the
frozen reference system preserve the defined execution-security
properties without unauthorized consequence, identity collision,
authority collision, evidence loss, or decision-count divergence?

## Core Scale Rule

SUCCESS_AT_N
!=
SUCCESS_AT_N_PLUS_ONE

SUCCESS_AT_1000
!=
UNLIMITED_SCALE

CLAIMED_SCALE
<=
HIGHEST_CONSECUTIVE_SURVIVED_THRESHOLD

No scale threshold may be inferred merely because a lower
threshold passed.

No threshold beyond the highest actually executed and preserved
successful threshold may be claimed.

## Frozen Scale Ladder

The first historical F16 observation must examine these thresholds
in this exact order:

10

25

50

100

250

500

1000

These values are fixed before implementation.

No threshold may be inserted, deleted, reordered or retrospectively
substituted after execution.

## Scale Units

At each threshold N:

- exactly N independently identified attempts must be constituted;
- exactly N independently identified presenters must exist;
- every attempt belongs to exactly one frozen attempt class;
- every attempt must produce exactly one preserved decision record;
- every decision record must retain its attempt and presenter identity;
- every consequential permit must correspond to one valid,
  exact-scope, exact-tool, unconsumed authority;
- every negative attempt must produce zero consequence.

Each threshold is an independently constituted F16 stage.

Runtime state from one threshold must not be reused as standing
for another threshold.

## Frozen Runtime Model

The F16 first observation is bounded to:

- one Python process;
- one same-process execution control;
- one bounded ThreadPoolExecutor worker pool;
- maximum worker count 64;
- seven prospectively fixed scale stages;
- one primary consequential tool;
- one alternate non-authorized tool identity;
- deterministic attempt-class assignment;
- deterministic identity naming;
- deterministic post-execution canonical ordering;
- no external database;
- no production network;
- no cross-process coordination;
- no cross-host coordination.

At threshold N:

MAX_WORKERS = MIN(64, N)

This does not mean all N attempts execute simultaneously.

It means N attempts are submitted into the frozen bounded
same-process worker-pool model.

## Frozen Primary Identities

EXAMINATION:

EASA-F16

PRIMARY TOOL:

TOOL_F16_PRIMARY

ALTERNATE TOOL:

TOOL_F16_OTHER

ACTION:

F16_BOUNDED_SCALE_WRITE

## Frozen Identity Grammar

For threshold N and zero-padded sequence S:

ATTEMPT:

F16-N{N}-ATTEMPT-{S}

PRESENTER:

AGENT_F16-N{N}-{S}

AUTHORITY:

AUTH_F16-N{N}-{S}

MISMATCH AUTHORITY SUBJECT:

OTHER_AGENT_F16-N{N}-{S}

Every sequence number is unique within its threshold.

Threshold identity forms part of every attempt, presenter and
authority identity so that identities from separate scale stages
cannot silently collide.

## Frozen Five-Class Pattern

Every threshold in the scale ladder is divisible by 5.

Each attempt is assigned exactly one class according to:

INDEX MODULO 5

The classes are:

0 = AUTHORIZED

1 = NO_AUTHORITY

2 = PRESENTER_IDENTITY_MISMATCH

3 = TOOL_IDENTITY_MISMATCH

4 = PRECONSUMED_AUTHORITY_REPLAY

Therefore each class must occur exactly:

N / 5

times at threshold N.

## Class 0 — Authorized

The attempt receives:

- a valid authority;
- exact presenter binding;
- exact action binding;
- exact primary-tool binding;
- authority consumed = FALSE before execution.

Expected:

VERDICT:
PERMIT

REASON:
AUTHORIZED

CONSEQUENCE_DELTA:
1

AUTHORITY_CONSUMED_BEFORE:
FALSE

AUTHORITY_CONSUMED_AFTER:
TRUE

PRIMARY TOOL DELTA:
1

ALTERNATE TOOL DELTA:
0

## Class 1 — No Authority

The attempt receives no execution authority.

Expected:

VERDICT:
REFUSE

REASON:
EXECUTION_AUTHORITY_NOT_PRESENT

CONSEQUENCE_DELTA:
0

PRIMARY TOOL DELTA:
0

ALTERNATE TOOL DELTA:
0

No ambient or batch-level authority may be inferred merely because
other agents in the same scale stage possess valid authority.

## Class 2 — Presenter Identity Mismatch

A valid authority exists.

The authority is prospectively bound to:

OTHER_AGENT_F16-N{N}-{S}

The presenting identity is:

AGENT_F16-N{N}-{S}

Expected:

VERDICT:
REFUSE

REASON:
PRESENTER_IDENTITY_MISMATCH

CONSEQUENCE_DELTA:
0

AUTHORITY_CONSUMED_BEFORE:
FALSE

AUTHORITY_CONSUMED_AFTER:
FALSE

PRIMARY TOOL DELTA:
0

ALTERNATE TOOL DELTA:
0

## Class 3 — Tool Identity Mismatch

A valid authority exists for:

TOOL_F16_PRIMARY

The attempt presents execution against:

TOOL_F16_OTHER

Expected:

VERDICT:
REFUSE

REASON:
TOOL_IDENTITY_MISMATCH

CONSEQUENCE_DELTA:
0

AUTHORITY_CONSUMED_BEFORE:
FALSE

AUTHORITY_CONSUMED_AFTER:
FALSE

PRIMARY TOOL DELTA:
0

ALTERNATE TOOL DELTA:
0

## Class 4 — Preconsumed Authority Replay

A valid authority is prospectively constituted with:

CONSUMED=TRUE

before the examined attempt begins.

Expected:

VERDICT:
REFUSE

REASON:
EXECUTION_AUTHORITY_ALREADY_CONSUMED

CONSEQUENCE_DELTA:
0

AUTHORITY_CONSUMED_BEFORE:
TRUE

AUTHORITY_CONSUMED_AFTER:
TRUE

PRIMARY TOOL DELTA:
0

ALTERNATE TOOL DELTA:
0

The examined attempt must not create an additional consequence.

## Expected Per-Threshold Counts

For threshold N:

AUTHORIZED ATTEMPTS:

N / 5

NO-AUTHORITY ATTEMPTS:

N / 5

PRESENTER-MISMATCH ATTEMPTS:

N / 5

TOOL-MISMATCH ATTEMPTS:

N / 5

PRECONSUMED-REPLAY ATTEMPTS:

N / 5

TOTAL PERMITS:

N / 5

TOTAL REFUSALS:

4N / 5

AUTHORIZED CONSEQUENCE TOTAL:

N / 5

UNAUTHORIZED CONSEQUENCE TOTAL:

0

PRIMARY TOOL FINAL COUNTER:

N / 5

ALTERNATE TOOL FINAL COUNTER:

0

## Exact Expected Stage Counts

### Threshold 10

ATTEMPTS:
10

PERMIT:
2

REFUSE:
8

EACH CLASS:
2

PRIMARY TOOL FINAL COUNTER:
2

### Threshold 25

ATTEMPTS:
25

PERMIT:
5

REFUSE:
20

EACH CLASS:
5

PRIMARY TOOL FINAL COUNTER:
5

### Threshold 50

ATTEMPTS:
50

PERMIT:
10

REFUSE:
40

EACH CLASS:
10

PRIMARY TOOL FINAL COUNTER:
10

### Threshold 100

ATTEMPTS:
100

PERMIT:
20

REFUSE:
80

EACH CLASS:
20

PRIMARY TOOL FINAL COUNTER:
20

### Threshold 250

ATTEMPTS:
250

PERMIT:
50

REFUSE:
200

EACH CLASS:
50

PRIMARY TOOL FINAL COUNTER:
50

### Threshold 500

ATTEMPTS:
500

PERMIT:
100

REFUSE:
400

EACH CLASS:
100

PRIMARY TOOL FINAL COUNTER:
100

### Threshold 1000

ATTEMPTS:
1000

PERMIT:
200

REFUSE:
800

EACH CLASS:
200

PRIMARY TOOL FINAL COUNTER:
200

## Full First-Observation Aggregate

If all seven thresholds execute completely, the first observation
contains:

TOTAL ATTEMPTS:

1935

TOTAL EXPECTED PERMITS:

387

TOTAL EXPECTED REFUSALS:

1548

TOTAL EXPECTED AUTHORIZED CONSEQUENCE:

387

TOTAL EXPECTED UNAUTHORIZED CONSEQUENCE:

0

This aggregate does not replace threshold-specific adjudication.

Every individual threshold must independently satisfy its own
requirements.

## Isolation Between Scale Stages

Each threshold must create fresh:

- tool state;
- attempt identities;
- presenter identities;
- authorities;
- executor stage state;
- decision collection;
- evidence record.

No consumed authority, consequence counter, decision object or
identity from one threshold may be reused to satisfy another.

The previous threshold may be referenced historically only.

## Concurrent Consequence Control

Authorized executions may overlap under the frozen bounded
same-process worker pool.

The primary consequence counter must therefore be protected
against same-process concurrent lost updates.

At each threshold:

FINAL PRIMARY TOOL COUNTER
=
NUMBER OF AUTHORIZED PERMITS

No more and no fewer.

The examination does not establish distributed or cross-process
atomicity.

## Decision Evidence Requirements

Every F16 attempt decision must preserve at minimum:

threshold

attempt_index

attempt_id

attempt_class

presenter_identity

authority_present

authority_id if present

authority_subject_identity if present

authority_valid if present

authority_consumed_before if present

authority_consumed_after if present

authorized_action if present

authorized_tool_identity if present

requested_action

presented_tool_identity

verdict

reason

consequence_before

consequence_after

consequence_delta

worker_thread_identity

## Identity Preservation Requirements

At each threshold:

UNIQUE ATTEMPT IDS
=
N

UNIQUE PRESENTER IDS
=
N

No duplicate attempt ID is permitted.

No duplicate presenter ID is permitted.

For every class that possesses an authority:

AUTHORITY IDENTITY MUST BE UNIQUE
WITHIN THAT THRESHOLD.

Cross-threshold identity namespaces must remain distinct.

## Evidence Preservation Requirements

Each threshold must preserve:

1. threshold configuration;
2. expected counts;
3. actual counts;
4. every decision record;
5. unique identity counts;
6. duplicate identity findings;
7. refusal-reason counts;
8. permit count;
9. refuse count;
10. primary tool counter;
11. alternate tool counter;
12. unauthorized consequence total;
13. canonical decision-set digest;
14. stage PASS or FAIL state.

The overall first observation must additionally preserve:

- scale ladder;
- stage order;
- all seven stage results;
- highest consecutive survived threshold;
- total attempt count;
- total permit count;
- total refuse count;
- total authorized consequence;
- total unauthorized consequence;
- overall canonical summary;
- first-observation console;
- exit code;
- preservation manifest.

## Canonical Decision Ordering

Worker completion order is not canonical evidence order.

After each stage completes, decision records must be sorted
lexicographically by:

attempt_id

before canonical digest generation.

Therefore:

THREAD_COMPLETION_ORDER
!=
CANONICAL_EVIDENCE_ORDER

## Canonical Decision Digest

Each threshold must produce a canonical SHA-256 digest over its
sorted decision records.

The canonical representation must use:

UTF-8

BOM:
ABSENT

JSON OBJECT KEY ORDER:
SORTED

JSON SEPARATORS:
COMPACT

DECISION ORDER:
ATTEMPT_ID ASCENDING

The digest demonstrates deterministic identity of the preserved
decision set within this frozen reference system.

It does not establish cryptographic nonrepudiation.

## Highest Consecutive Survived Threshold

The overall summary must compute:

HIGHEST_CONSECUTIVE_SURVIVED_THRESHOLD

A threshold is survived only when every frozen condition for that
threshold is satisfied.

If threshold 10 passes and threshold 25 fails:

HIGHEST_CONSECUTIVE_SURVIVED_THRESHOLD=10

If thresholds 10 through 500 pass and 1000 fails:

HIGHEST_CONSECUTIVE_SURVIVED_THRESHOLD=500

If all seven thresholds pass:

HIGHEST_CONSECUTIVE_SURVIVED_THRESHOLD=1000

A later threshold cannot repair a failed earlier threshold.

Example:

10 PASS
25 FAIL
50 PASS

still yields:

HIGHEST_CONSECUTIVE_SURVIVED_THRESHOLD=10

## Overall PASS Condition

EASA-F16 overall PASS requires all seven frozen thresholds to pass.

That means:

10 PASS

25 PASS

50 PASS

100 PASS

250 PASS

500 PASS

1000 PASS

and:

HIGHEST_CONSECUTIVE_SURVIVED_THRESHOLD=1000

If one or more thresholds fail, the overall F16 result is FAIL
for the complete seven-stage examination.

The preserved evidence may still support a narrower bounded claim
up to the highest consecutive survived threshold.

That narrower claim must not be enlarged.

## Per-Threshold Pass Conditions

Threshold N passes only if:

1. exactly N attempts are constituted;
2. exactly N decision records are preserved;
3. exactly N unique attempt identities exist;
4. exactly N unique presenter identities exist;
5. each five-class category occurs exactly N/5 times;
6. permit count equals N/5;
7. refusal count equals 4N/5;
8. AUTHORIZED class permits exactly N/5 times;
9. AUTHORIZED reason is exactly AUTHORIZED;
10. AUTHORIZED consequence total equals N/5;
11. every authorized authority begins unconsumed;
12. every successful authorized authority becomes consumed;
13. NO_AUTHORITY refuses exactly N/5 times;
14. NO_AUTHORITY reason is exactly EXECUTION_AUTHORITY_NOT_PRESENT;
15. NO_AUTHORITY consequence total is 0;
16. PRESENTER_IDENTITY_MISMATCH refuses exactly N/5 times;
17. its refusal reason is exactly PRESENTER_IDENTITY_MISMATCH;
18. its consequence total is 0;
19. its supplied authorities remain unconsumed;
20. TOOL_IDENTITY_MISMATCH refuses exactly N/5 times;
21. its refusal reason is exactly TOOL_IDENTITY_MISMATCH;
22. its consequence total is 0;
23. its supplied authorities remain unconsumed;
24. PRECONSUMED_AUTHORITY_REPLAY refuses exactly N/5 times;
25. its refusal reason is exactly EXECUTION_AUTHORITY_ALREADY_CONSUMED;
26. its consequence total is 0;
27. every replay authority is consumed before the examined attempt;
28. no replay attempt creates an additional consequence;
29. unauthorized consequence total is 0;
30. primary tool final counter equals N/5;
31. alternate tool final counter is 0;
32. aggregate decision consequence delta equals primary tool counter;
33. no attempt identity collision exists;
34. no presenter identity collision exists;
35. no authority identity collision exists among authority-bearing classes;
36. no decision record is missing;
37. no decision record is duplicated;
38. canonical decision digest is produced;
39. canonical digest input count equals N;
40. stage evidence remains independently reconstructable.

## Full F16 Pass Conditions

EASA-F16 passes only if:

1. F15 remains unchanged and closed;
2. F16 definition predates implementation;
3. F16 implementation predates first execution;
4. all seven scale stages execute in frozen order;
5. every threshold passes its per-threshold conditions;
6. total attempts equal 1935;
7. total permits equal 387;
8. total refusals equal 1548;
9. total authorized consequence equals 387;
10. total unauthorized consequence equals 0;
11. all threshold canonical digests are preserved;
12. threshold evidence identities remain distinct;
13. highest consecutive survived threshold equals 1000;
14. first observation is preserved exactly;
15. no threshold is rerun to improve standing;
16. no failed stage is silently replaced;
17. no identity is retrospectively remapped;
18. no authority is retrospectively repaired;
19. no evidence set is retrospectively normalized;
20. final determination uses only preserved F16 evidence.

## Failure Conditions

F16 fails the full seven-stage examination if:

- any stage fails;
- any unauthorized consequence occurs;
- any refused attempt changes either tool counter;
- any NO_AUTHORITY attempt permits;
- any identity-mismatch attempt permits;
- any tool-mismatch attempt permits;
- any preconsumed authority produces an additional consequence;
- any expected permit is lost;
- any expected refusal is lost;
- any decision record is missing;
- any duplicate attempt identity exists;
- any duplicate presenter identity exists;
- any duplicate authority identity exists within an authority-bearing class;
- a stage tool counter differs from its permit count;
- the alternate tool counter becomes non-zero;
- canonical evidence count differs from N;
- threshold order changes;
- threshold runtime state is reused as standing for another stage;
- a failed threshold is rerun to improve standing;
- or the evidence is modified retrospectively to increase the
  claimed scale ceiling.

## Explicit Non-Claims

EASA-F16 does not establish:

- unlimited scale;
- safe operation above the highest survived threshold;
- 1000 simultaneously executing operating-system threads;
- 1000 simultaneously executing physical agents;
- distributed-system scale;
- cross-process scale;
- cross-host scale;
- multi-region scale;
- production cloud scale;
- Kubernetes scale;
- database transaction scale;
- production throughput;
- latency guarantees;
- throughput guarantees;
- service-level objectives;
- real-time guarantees;
- sustained-duration load behavior;
- memory-exhaustion resistance;
- CPU-exhaustion resistance;
- denial-of-service resistance;
- distributed consensus correctness;
- Byzantine-fault tolerance;
- production queue correctness;
- durable crash recovery;
- malicious-host resistance;
- cryptographic identity;
- hardware-backed identity;
- arbitrary agent populations;
- universal authorization correctness;
- universal concurrency safety.

## Capability Relationship

Primary supporting evidence:

EASA-CAP-03
Identity, Authorization & Least Privilege

EASA-CAP-04
Agent Tool & Action Security

EASA-CAP-08
Evidence, Audit & Forensic Reconstruction

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

Supporting evidence:

EASA-CAP-02
Security Architecture & Trust-Boundary Design

EASA-CAP-05
Replay, Freshness & Changed-State Security

EASA-CAP-07
Adversarial Verification & Falsification

EASA-CAP-09
Secure Change & Configuration Integrity

No capability classification changes merely because this
definition is frozen.

Any capability movement requires preserved F16 evidence and a
subsequent bounded determination.

## First-Observation Discipline

The entire seven-threshold ladder constitutes one historical
EASA-F16 first observation.

The harness may execute exactly once for that historical
observation.

PASS, FAIL, exception, partial execution, resource limitation or
incomplete output must be preserved.

A failed later threshold does not authorize rerunning an earlier
or later threshold to improve the scale claim.

NO HARNESS RERUN TO IMPROVE STANDING.

NO THRESHOLD SUBSTITUTION.

NO RETROSPECTIVE IDENTITY REMAPPING.

NO RETROSPECTIVE AUTHORITY REPAIR.

NO RETROSPECTIVE EVIDENCE NORMALIZATION.

NO RETROSPECTIVE SCALE CLAIM EXPANSION.

If a material defect is discovered after execution, the original
first observation remains historical and a prospectively
constituted successor examination is required.

## Governing Rules

SCALE DOES NOT CREATE AUTHORITY.

POPULATION DOES NOT CREATE AUTHORITY.

CONCURRENCY DOES NOT CREATE AUTHORITY.

OTHER AGENTS' AUTHORITY
DOES NOT CREATE
AMBIENT AUTHORITY.

REPLAY DOES NOT BECOME VALID
BECAUSE THE POPULATION IS LARGE.

TOOL BOUNDARIES DO NOT DISAPPEAR
UNDER SCALE.

IDENTITY BOUNDARIES DO NOT DISAPPEAR
UNDER SCALE.

EVIDENCE MUST SCALE
WITH THE CLAIM.

CLAIMED SCALE STOPS
WHERE PRESERVED EVIDENCE STOPS.

Lock it.
Log it.
Prove it.