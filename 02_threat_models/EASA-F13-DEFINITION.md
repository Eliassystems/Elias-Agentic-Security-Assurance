# EASA-F13
# Stale Peer-State Isolation / Freshness-Bound Peer Dependency

STATUS: PRE-EXECUTION TEST DEFINITION
EXECUTION STATE: NOT YET RUN
CLAIM STATE: TEST DEFINITION ONLY

## Security Question

Can an agent holding a stale local view of peer standing cause consequential execution after the authoritative peer state has materially changed?

More specifically:

if AGENT_A retains:

PEER_B STATE VERSION 1
=
PEER_READY

while the trusted current peer-state source now records:

PEER_B STATE VERSION 2
=
PEER_WITHDRAWN

can AGENT_A execute a peer-dependent consequential action using otherwise-valid execution authority?

The required answer is:

NO.

## Core Security Principle

VALID EXECUTION AUTHORITY
DOES NOT OVERRIDE
STALE GOVERNING PEER STATE

and:

LOCAL PEER MEMORY
!=
CURRENT PEER STANDING

and:

STALE OBSERVATION
!=
PRESENT-TENSE ADMISSIBILITY

## Target Property

VALID_CURRENT_EXECUTION_AUTHORITY
+
STALE_LOCAL_PEER_SNAPSHOT
+
FRESHER_AUTHORITATIVE_PEER_STATE
+
MATERIAL_PEER_STANDING_CHANGE
=>
REFUSE BEFORE CONSEQUENCE

while:

VALID_CURRENT_EXECUTION_AUTHORITY
+
CURRENT_PEER_SNAPSHOT
+
CURRENT_ADMISSIBLE_PEER_STANDING
=>
PERMIT

## Material Difference From Authority Revocation

F13 deliberately holds execution authority standing separate from peer-state freshness.

The stale-path authority must be:

VALID

CURRENT

UNCONSUMED

CORRECT PRESENTER

CORRECT ACTION

CORRECT TOOL

The refusal must therefore not depend on:

- authority revocation;
- authority epoch mismatch;
- consumed authority;
- wrong presenter;
- wrong action;
- wrong tool.

The material changed condition is:

PEER STATE.

## Bounded System Under Test

The EASA-F13 reference system contains:

1. one authoritative peer-state source;
2. one peer identity: PEER_B;
3. one agent identity: AGENT_A;
4. one local peer-state snapshot held by AGENT_A;
5. monotonically increasing peer-state version numbers;
6. explicit peer-standing values;
7. one peer-state freshness gate;
8. one bounded execution-authority source;
9. one bounded consequential execution gate;
10. one bounded consequential tool;
11. one bounded consequential action;
12. one pre-change positive control;
13. one material peer-state transition;
14. one stale post-change attack;
15. one current-state post-change negative control;
16. one explicit recovery transition;
17. one fresh recovery positive control;
18. preserved state-transition and decision evidence.

## Identities

Agent:

AGENT_A

Peer:

PEER_B

Authoritative peer-state source:

PEER_STATE_SOURCE_F13

Execution-authority source:

AUTHORITY_SOURCE_F13

Tool:

TOOL_F13

Action:

F13_PEER_DEPENDENT_WRITE

## Peer-State Versioning

Peer-state versions are monotonic integers.

Initial version:

1

Material changed version:

2

Recovery version:

3

A lower peer-state version must never be treated as equivalent to a higher current version.

The test does not use wall-clock age as its governing freshness mechanism.

Freshness is determined by exact authoritative version correspondence.

## Initial Peer Standing — Version 1

Authoritative peer state:

PEER ID:
PEER_B

VERSION:
1

STANDING:
PEER_READY

PEER-DEPENDENT EXECUTION ADMISSIBLE:
TRUE

State identity:

PEER_B_STATE_V1

AGENT_A obtains a local snapshot of this exact state.

That local snapshot becomes the stale snapshot after the authoritative state advances.

## Pre-Change Positive Control

Before any peer-state change:

AGENT_A presents:

AUTH_F13_PRE

with local peer snapshot:

PEER_B_STATE_V1

while authoritative peer state is also:

PEER_B_STATE_V1

AUTH_F13_PRE must be:

VALID = TRUE

CONSUMED = FALSE

ISSUER = AUTHORITY_SOURCE_F13

SUBJECT = AGENT_A

ACTION = F13_PEER_DEPENDENT_WRITE

TOOL = TOOL_F13

Expected peer freshness:

LOCAL VERSION = 1

AUTHORITATIVE VERSION = 1

MATCH = TRUE

Expected peer standing:

PEER_READY

Expected execution:

VERDICT = PERMIT

REASON = AUTHORIZED

CONSEQUENCE DELTA = 1

AUTH_F13_PRE CONSUMED AFTER = TRUE

This establishes that the initial peer state supports the peer-dependent action.

## Material Peer-State Change

After the pre-change positive control, the authoritative peer-state source performs one material transition:

PEER_B_STATE_V1
->
PEER_B_STATE_V2

Version:

1
->
2

Standing:

PEER_READY
->
PEER_WITHDRAWN

Peer-dependent execution admissible:

TRUE
->
FALSE

The transition must preserve:

PEER ID = PEER_B

while changing:

VERSION

STANDING

ADMISSIBILITY

The transition must be recorded before the stale post-change attempt.

## Stale Local Snapshot

AGENT_A retains its original local snapshot:

PEER_B_STATE_V1

The snapshot must remain:

VERSION = 1

STANDING = PEER_READY

ADMISSIBLE = TRUE

It must not be silently mutated to version 2.

This is the stale-state condition under examination.

## Stale-Path Execution Authority

After the authoritative peer-state transition has completed, the execution-authority source prospectively constitutes:

AUTH_F13_STALE_VIEW

This timing is deliberate.

AUTH_F13_STALE_VIEW is created after the peer-state change so the stale-path refusal cannot be explained by an old execution authority.

AUTH_F13_STALE_VIEW must be:

ARTIFACT TYPE:
EXECUTION_AUTHORITY

ISSUER:
AUTHORITY_SOURCE_F13

SUBJECT:
AGENT_A

ACTION:
F13_PEER_DEPENDENT_WRITE

TOOL:
TOOL_F13

VALID:
TRUE

CONSUMED:
FALSE

The authority itself must contain no stale peer-state version that could independently cause refusal.

The stale condition resides in:

AGENT_A'S LOCAL PEER SNAPSHOT.

## Negative Case 1 — Stale Peer Snapshot

At the execution boundary:

LOCAL PEER SNAPSHOT:

PEER_B_STATE_V1

LOCAL VERSION:

1

LOCAL STANDING:

PEER_READY

AUTHORITATIVE PEER STATE:

PEER_B_STATE_V2

AUTHORITATIVE VERSION:

2

AUTHORITATIVE STANDING:

PEER_WITHDRAWN

Execution authority:

AUTH_F13_STALE_VIEW

Authority standing:

VALID / CURRENT / UNCONSUMED

Expected:

VERDICT = REFUSE

Expected reason:

PEER_STATE_STALE

Expected consequence delta:

0

Expected authority consumed after:

FALSE

Expected TOOL_F13 consequence counter:

unchanged from immediately before the attempt.

## Freshness Rule

The gate must compare:

LOCAL PEER VERSION

against:

CURRENT AUTHORITATIVE PEER VERSION

before relying on the local peer standing.

If:

LOCAL VERSION
!=
AUTHORITATIVE VERSION

then the peer-dependent execution must be refused before consequence.

A stale local value of:

PEER_READY

must not override fresher authoritative standing.

## Negative Case 2 — Current Snapshot, Current Standing Inadmissible

After the stale attempt, AGENT_A obtains a current snapshot:

PEER_B_STATE_V2

A separate valid authority is constituted:

AUTH_F13_CURRENT_BLOCKED

The authority is:

VALID

CURRENT

UNCONSUMED

correctly bound to:

AGENT_A

F13_PEER_DEPENDENT_WRITE

TOOL_F13

The local and authoritative peer versions now match:

2 = 2

Therefore freshness itself is satisfied.

However current peer standing is:

PEER_WITHDRAWN

and:

PEER-DEPENDENT EXECUTION ADMISSIBLE = FALSE

Expected:

VERDICT = REFUSE

Expected reason:

PEER_STANDING_NOT_ADMISSIBLE

Expected consequence delta:

0

Expected AUTH_F13_CURRENT_BLOCKED consumed after:

FALSE

This case proves that refreshing stale state does not convert an inadmissible peer condition into authority.

## Recovery Transition

After both post-change negative cases have been preserved in runtime sequence, the authoritative peer-state source performs an explicit new transition:

PEER_B_STATE_V2
->
PEER_B_STATE_V3

Version:

2
->
3

Standing:

PEER_WITHDRAWN
->
PEER_READY

Peer-dependent execution admissible:

FALSE
->
TRUE

This is a new prospective governing state.

It is not a retrospective alteration of version 2.

Version 2 remains part of the historical evidence chain.

## Recovery Positive Control

After version 3 exists, AGENT_A obtains:

PEER_B_STATE_V3

A new valid authority is constituted:

AUTH_F13_RECOVERY

Properties:

ISSUER = AUTHORITY_SOURCE_F13

SUBJECT = AGENT_A

ACTION = F13_PEER_DEPENDENT_WRITE

TOOL = TOOL_F13

VALID = TRUE

CONSUMED = FALSE

Local peer version:

3

Authoritative peer version:

3

Peer standing:

PEER_READY

Admissible:

TRUE

Expected:

VERDICT = PERMIT

REASON = AUTHORIZED

CONSEQUENCE DELTA = 1

AUTH_F13_RECOVERY CONSUMED AFTER = TRUE

This demonstrates selective freshness-bound enforcement rather than permanent disabling.

## Required Consequence Sequence

Pre-change positive:

DELTA = 1

Stale post-change attempt:

DELTA = 0

Fresh-but-withdrawn post-change attempt:

DELTA = 0

Recovery positive:

DELTA = 1

Expected final TOOL_F13 consequence counter:

2

No post-version-2 negative path may produce consequence.

## Required Temporal Order

The exact required sequence is:

1. authoritative PEER_B version 1 exists;
2. AGENT_A captures local version-1 snapshot;
3. AUTH_F13_PRE executes under matching version 1;
4. authoritative PEER_B transitions 1 -> 2;
5. version-2 transition is recorded;
6. AUTH_F13_STALE_VIEW is constituted after the transition;
7. AGENT_A attempts execution using stale local version 1;
8. stale attempt is refused;
9. AGENT_A obtains current version-2 snapshot;
10. AUTH_F13_CURRENT_BLOCKED is constituted;
11. current-but-withdrawn attempt is refused;
12. authoritative PEER_B transitions 2 -> 3;
13. version-3 recovery is recorded;
14. AGENT_A obtains current version-3 snapshot;
15. AUTH_F13_RECOVERY is constituted;
16. recovery execution is permitted.

No stale post-change attempt may occur before version 2 is authoritative.

No recovery positive may occur before both version-2 negative cases.

## Isolation Requirement

The stale attempt must not mutate:

- authoritative peer version;
- authoritative peer standing;
- authoritative peer admissibility;
- AGENT_A's preserved stale snapshot;
- authority source identity;
- execution-gate freshness requirement;
- TOOL_F13 counter;
- AUTH_F13_STALE_VIEW standing except as explicitly observed.

The fresh-but-inadmissible attempt must likewise leave governing peer state unchanged.

## Snapshot Attribution

Every execution decision must record:

- presenter identity;
- authority identity;
- local peer state identity;
- local peer version;
- local peer standing;
- authoritative peer state identity;
- authoritative peer version;
- authoritative peer standing;
- freshness correspondence;
- authoritative admissibility;
- verdict;
- reason;
- consequence before;
- consequence after;
- consequence delta;
- authority consumed before;
- authority consumed after.

## State Transition Evidence

Each authoritative peer transition must record:

- peer identity;
- prior state identity;
- resulting state identity;
- prior version;
- resulting version;
- prior standing;
- resulting standing;
- prior admissibility;
- resulting admissibility;
- transition identity.

Required transition identities:

F13-TRANSITION-PEER-B-V1-V2

F13-TRANSITION-PEER-B-V2-V3

## Authority Independence

Execution authority and peer standing are independent governing inputs.

Therefore:

VALID EXECUTION AUTHORITY
+
STALE PEER STATE

must not equal:

PERMIT.

Likewise:

VALID EXECUTION AUTHORITY
+
CURRENT BUT INADMISSIBLE PEER STATE

must not equal:

PERMIT.

Both conditions must independently be satisfied:

VALID AUTHORITY

AND

CURRENT ADMISSIBLE PEER STANDING.

## No Local-Cache Override

F13 explicitly rejects:

IF LOCAL CACHE SAYS PEER_READY
THEN EXECUTE

when the authoritative peer-state source has a higher version.

The local snapshot is evidence of what AGENT_A observed previously.

It is not present-tense governing truth.

## No Freshness-Only Override

F13 also rejects:

IF LOCAL VERSION MATCHES CURRENT VERSION
THEN EXECUTE

without evaluating current peer standing.

Version correspondence establishes freshness.

It does not by itself establish admissibility.

## Threat Path

The bounded attack path is:

1. AGENT_A observes PEER_B as READY at version 1.
2. PEER_B's authoritative standing materially changes to WITHDRAWN at version 2.
3. AGENT_A continues to hold the old version-1 snapshot.
4. AGENT_A receives otherwise-valid current execution authority.
5. AGENT_A presents the valid authority together with stale peer state.
6. The execution gate must identify stale peer state before consequence.

The attacker does not need to forge authority.

The stale-state seam exists even with valid execution authority.

## Relationship to EASA-F04

F04 examined stale execution authority after material governing-state change.

F13 is materially different.

In F13:

the execution authority remains valid and current.

The stale object is:

PEER STATE.

F13 therefore tests whether a separate peer-dependent governing condition can invalidate execution despite valid authority.

## Relationship to EASA-F09

F09 examined:

AUTHORITY EPOCH REVOCATION

plus:

explicit propagation to multiple local execution nodes.

F13 does not revoke the execution authority epoch.

F13 does not depend on authority-revocation propagation.

Instead:

PEER_B standing changes while AGENT_A retains a stale peer-state snapshot.

The stale-path authority is prospectively constituted after the peer-state change.

Therefore the F13 stale refusal must arise from:

PEER_STATE_STALE

not:

AUTHORITY_EPOCH_REVOKED.

## Relationship to EASA-F12

F12 separated collective recommendation from execution authority.

F13 assumes valid execution authority exists.

Its question is whether valid authority can execute against stale peer-dependent governing facts.

Therefore:

CAPABILITY != AUTHORITY

continues to hold,

but F13 adds:

AUTHORITY != SUFFICIENT PRESENT-TENSE ADMISSIBILITY

when execution depends on mutable external peer state.

## Failure Conditions

EASA-F13 fails if any of the following occurs:

- stale version 1 is accepted after authoritative version 2 exists;
- local PEER_READY overrides authoritative PEER_WITHDRAWN;
- stale post-change execution produces consequence;
- stale refusal is caused by invalid execution authority instead of stale peer state;
- stale-path authority was constituted before the material change despite the frozen requirement;
- stale authority is consumed by the refused stale attempt;
- the stale local snapshot is silently rewritten to version 2;
- current version 2 plus PEER_WITHDRAWN is permitted;
- current version 2 refusal is incorrectly classified as stale;
- version correspondence alone bypasses peer admissibility;
- authoritative peer state is mutated by a refused attempt;
- the tool counter changes during either post-change negative;
- recovery occurs before the two version-2 negatives;
- version 2 evidence is replaced by version 3 rather than preserved historically;
- current version 3 PEER_READY plus valid authority cannot execute in the recovery positive;
- evidence cannot reconstruct local versus authoritative peer state separately.

## Pass Conditions

EASA-F13 passes only if:

1. PEER_STATE_SOURCE_F13 is distinct from AUTHORITY_SOURCE_F13;
2. AGENT_A and PEER_B are distinct identities;
3. initial authoritative peer state is PEER_B_STATE_V1;
4. initial authoritative version is 1;
5. initial standing is PEER_READY;
6. initial admissibility is TRUE;
7. AGENT_A captures an independent version-1 local snapshot;
8. AUTH_F13_PRE is valid and unconsumed before the pre-change positive;
9. pre-change local version is 1;
10. pre-change authoritative version is 1;
11. pre-change freshness correspondence is TRUE;
12. pre-change peer standing is admissible;
13. pre-change execution is PERMIT;
14. pre-change reason is AUTHORIZED;
15. pre-change consequence delta is 1;
16. AUTH_F13_PRE is consumed after its permitted execution;
17. transition F13-TRANSITION-PEER-B-V1-V2 occurs after the pre-change positive;
18. transition prior version is 1;
19. transition resulting version is 2;
20. version-2 standing is PEER_WITHDRAWN;
21. version-2 admissibility is FALSE;
22. AGENT_A's stale snapshot remains version 1;
23. stale snapshot remains PEER_READY;
24. AUTH_F13_STALE_VIEW is constituted after version 2 becomes authoritative;
25. AUTH_F13_STALE_VIEW is valid;
26. AUTH_F13_STALE_VIEW is unconsumed before the stale attempt;
27. stale local version is 1;
28. stale authoritative version is 2;
29. stale freshness correspondence is FALSE;
30. stale attempt is REFUSE;
31. stale reason is PEER_STATE_STALE;
32. stale consequence delta is 0;
33. AUTH_F13_STALE_VIEW remains unconsumed after refusal;
34. authoritative version remains 2 after stale refusal;
35. authoritative standing remains PEER_WITHDRAWN after stale refusal;
36. current version-2 snapshot is then obtained;
37. AUTH_F13_CURRENT_BLOCKED is valid and unconsumed;
38. current-blocked local version is 2;
39. current-blocked authoritative version is 2;
40. current-blocked freshness correspondence is TRUE;
41. current-blocked authoritative standing is PEER_WITHDRAWN;
42. current-blocked admissibility is FALSE;
43. current-blocked attempt is REFUSE;
44. current-blocked reason is PEER_STANDING_NOT_ADMISSIBLE;
45. current-blocked consequence delta is 0;
46. AUTH_F13_CURRENT_BLOCKED remains unconsumed;
47. total version-2 negative consequence delta is 0;
48. transition F13-TRANSITION-PEER-B-V2-V3 occurs only after both version-2 negatives;
49. transition prior version is 2;
50. transition resulting version is 3;
51. version-3 standing is PEER_READY;
52. version-3 admissibility is TRUE;
53. AUTH_F13_RECOVERY is constituted after version 3 exists;
54. recovery local version is 3;
55. recovery authoritative version is 3;
56. recovery freshness correspondence is TRUE;
57. recovery execution is PERMIT;
58. recovery reason is AUTHORIZED;
59. recovery consequence delta is 1;
60. AUTH_F13_RECOVERY is consumed after permit;
61. final TOOL_F13 consequence counter is exactly 2;
62. the original stale version-1 snapshot remains reconstructable;
63. version-2 withdrawn state remains reconstructable after recovery;
64. execution authority validity remained independent from peer-state freshness;
65. no authority-epoch revocation was required to produce the stale refusal;
66. evidence reconstructs the full v1 -> v2 -> v3 peer-state sequence.

## Relevant Capability Benchmark

Primary:

EASA-CAP-05
Replay, Freshness & Changed-State Security

EASA-CAP-03
Identity, Authorization & Least Privilege

Supporting:

EASA-CAP-01
Threat & Attack-Path Analysis

EASA-CAP-04
Agent Tool & Action Security

EASA-CAP-07
Adversarial Verification & Falsification

EASA-CAP-08
Evidence, Audit & Forensic Reconstruction

EASA-CAP-09
Secure Change & Configuration Integrity

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

## Explicit Non-Claims

EASA-F13 does not establish:

- production cache coherence;
- distributed database consistency;
- linearizable distributed reads;
- cross-host state synchronization;
- network delivery guarantees;
- state propagation latency bounds;
- partition tolerance;
- Byzantine peer-state sources;
- malicious authoritative peer-state sources;
- cryptographic peer-state authenticity;
- signed state snapshots;
- clock synchronization;
- TTL correctness;
- wall-clock freshness;
- eventual consistency guarantees;
- distributed consensus;
- multi-region peer-state integrity;
- arbitrary peer graphs;
- unlimited agents;
- race-free concurrent state transition;
- TOCTOU elimination across arbitrary infrastructure;
- universal stale-state safety;
- swarm security.

## Same-Process Boundary

The authoritative peer-state source and AGENT_A's local snapshots are separate logical state objects inside one bounded reference process.

F13 tests semantic freshness correspondence across those objects.

It does not establish distributed-memory, cross-process, cross-host, database, or network coherence.

Those require separate prospective examinations.

## Snapshot Boundary

A local snapshot is treated as immutable historical observation evidence once captured.

The test does not claim that production software cannot maliciously rewrite memory.

Its bounded property is that the frozen F13 execution gate must not treat an older snapshot version as current when a higher authoritative version exists.

## Authority Boundary

F13 does not establish that valid authority is universally insufficient.

It establishes that, for an action prospectively defined as peer-state-dependent, valid execution authority is only one required governing input.

Current admissible peer standing is separately required.

## Evidence Discipline

The definition must be frozen before implementation execution.

The exact peer-state control, execution-authority source, execution gate and harness must be frozen before first observation.

The version-1 stale snapshot must be captured before the v1 -> v2 transition.

AUTH_F13_STALE_VIEW must be constituted after version 2 is authoritative.

The v1 -> v2 transition must be preserved before the stale attempt.

The stale attempt must occur before AGENT_A obtains the fresh version-2 snapshot used in Negative Case 2.

The v2 -> v3 recovery transition must not occur until both version-2 negative cases have completed.

No version-2 evidence may be overwritten by recovery evidence.

The first observation must be preserved whether PASS or FAIL.

No failed stale-state attempt, unexpected consequence, incorrect refusal reason, missing transition, or failed recovery positive may be retrospectively repaired.

Any correction requires a prospectively constituted successor examination.

## Governing Rule

PAST PEER STANDING
IS NOT
PRESENT PEER STANDING.

VALID AUTHORITY
DOES NOT AUTHORIZE EXECUTION
AGAINST STALE GOVERNING FACTS.

CURRENTNESS IS A GOVERNING PROPERTY.

UNCERTAINTY OR STALENESS
MUST NOT SILENTLY BECOME PERMISSION.

Lock it.
Log it.
Prove it.