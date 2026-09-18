# EASA-F15 — Resolver / Partition Safe Degradation

## Status

FROZEN PRE-IMPLEMENTATION DEFINITION

No EASA-F15 resolver runtime, authority object, execution gate,
worker, observation, receipt or consequence existed when this
definition was constituted.

## Examination

EASA-F15

Resolver / Partition Safe Degradation

## Purpose

Determine whether a consequential agent workflow remains safely
non-executing when a required current resolution dependency is:

- unavailable;
- partitioned;
- stale;
- internally conflicting;
- or current but substantively inadmissible.

The examination also determines whether execution can recover
prospectively after current, consistent and admissible resolution
is restored.

## Security Question

When execution requires current governing-state resolution,
can infrastructure failure or disagreement cause the system
to fall back to cached, stale, partial or permissive standing?

The required answer within the frozen F15 scope is:

NO.

## Core Security Properties

VALID_EXECUTION_AUTHORITY
+
REQUIRED_CURRENT_RESOLUTION_UNAVAILABLE
=>
REFUSE_BEFORE_CONSEQUENCE

VALID_EXECUTION_AUTHORITY
+
CONFLICTING_RESOLVER_VIEWS
=>
REFUSE_BEFORE_CONSEQUENCE

VALID_EXECUTION_AUTHORITY
+
CURRENT_CONSISTENT_RESOLUTION
+
CURRENT_STATE_NOT_ADMISSIBLE
=>
REFUSE_BEFORE_CONSEQUENCE

VALID_EXECUTION_AUTHORITY
+
CURRENT_CONSISTENT_RESOLUTION
+
CURRENT_STATE_ADMISSIBLE
=>
PERMIT_WITHIN_SCOPE

RESOLUTION_FAILURE
!=
AUTHORIZATION

AVAILABILITY_PRESSURE
!=
AUTHORIZATION

CACHED_ADMISSIBILITY
!=
CURRENT_RESOLUTION

PARTIAL_RESOLUTION
!=
CURRENT_STANDING

RESOLVER_CONSISTENCY
!=
EXECUTION_AUTHORITY

## Governing Distinction

The resolver does not create execution authority.

The resolver establishes whether a required governing-state
dependency is sufficiently current and internally consistent
for the separately constituted execution authority to be
evaluated.

Therefore:

VALID_EXECUTION_AUTHORITY
!=
SUFFICIENT_CURRENT_ADMISSIBILITY

and:

RESOLVER_AGREEMENT
!=
AUTHORITY_CREATION.

## Difference From EASA-F13

EASA-F13 examined stale peer-state isolation.

Its core seam was:

VALID CURRENT EXECUTION AUTHORITY
+
STALE LOCAL PEER SNAPSHOT
+
FRESHER AUTHORITATIVE PEER STATE
=>
REFUSE BEFORE CONSEQUENCE.

EASA-F15 examines a different property.

The F15 seam is the availability and consistency of the
resolution mechanism itself.

F15 asks whether:

- required resolver evidence can become unavailable;
- resolver views can diverge under a bounded simulated partition;
- cached admissibility can be substituted for current resolution;
- current consensus can resolve to a substantively inadmissible state;
- and execution can recover only after current admissible resolution
  is restored.

F15 does not inherit proof from F13.

## Frozen Runtime Scope

The first observation is bounded to:

- one Python process;
- one consequential tool;
- one presenter;
- one authoritative governing-state source;
- two resolver replicas;
- five independently constituted execution authorities;
- deterministic governing-state transitions;
- simulated resolver availability and partition conditions;
- one sequential examination harness;
- no production network;
- no external database;
- no cross-process communication.

## Frozen Identities

EXAMINATION:

EASA-F15

PRESENTER:

AGENT_F15

ACTION:

F15_PARTITION_SENSITIVE_WRITE

TOOL:

TOOL_F15

AUTHORITATIVE STATE SOURCE:

STATE_SOURCE_F15

RESOLVER A:

RESOLVER_F15_A

RESOLVER B:

RESOLVER_F15_B

## Governing-State Versions

Three authoritative governing-state versions are prospectively defined.

### R1

STATE_VERSION:

R1

STATE:

READY

ADMISSIBLE:

TRUE

### R2

STATE_VERSION:

R2

STATE:

WITHDRAWN

ADMISSIBLE:

FALSE

### R3

STATE_VERSION:

R3

STATE:

READY

ADMISSIBLE:

TRUE

## Material State Transitions

Two prospective authoritative transitions exist.

TRANSITION 1:

R1 READY
->
R2 WITHDRAWN

This is a material governing-state change.

TRANSITION 2:

R2 WITHDRAWN
->
R3 READY

This is a material prospective recovery change.

Neither transition modifies the validity of the separately issued
execution authorities.

## Frozen Authorities

Every F15 attempt receives a distinct authority so that refusal
standing is not confused with replay or single-consumption logic.

### Baseline Authority

AUTH_F15-BASELINE

Presenter:

AGENT_F15

Action:

F15_PARTITION_SENSITIVE_WRITE

Tool:

TOOL_F15

Initial state:

VALID
UNCONSUMED

### Partition Authority

AUTH_F15-PARTITION

Presenter:

AGENT_F15

Action:

F15_PARTITION_SENSITIVE_WRITE

Tool:

TOOL_F15

Initial state:

VALID
UNCONSUMED

### Conflict Authority

AUTH_F15-CONFLICT

Presenter:

AGENT_F15

Action:

F15_PARTITION_SENSITIVE_WRITE

Tool:

TOOL_F15

Initial state:

VALID
UNCONSUMED

### Current-Blocked Authority

AUTH_F15-CURRENT-BLOCKED

Presenter:

AGENT_F15

Action:

F15_PARTITION_SENSITIVE_WRITE

Tool:

TOOL_F15

Initial state:

VALID
UNCONSUMED

### Recovery Authority

AUTH_F15-RECOVERY

Presenter:

AGENT_F15

Action:

F15_PARTITION_SENSITIVE_WRITE

Tool:

TOOL_F15

Initial state:

VALID
UNCONSUMED

## Required Resolver Rule

For an F15 execution attempt to reach consequential execution,
both required resolver replicas must provide:

- a response;
- the same authoritative state version;
- the same state identity;
- the same admissibility value;
- and correspondence to the authoritative governing-state source.

If required current resolution cannot be established,
execution must not occur.

This two-resolver rule is a frozen F15 reference-system condition.

It is not claimed as a universal production quorum rule.

## Stage F15-S0 — Initial Resolution State

Authoritative state:

R1 READY / ADMISSIBLE TRUE

RESOLVER_F15_A:

R1 READY / ADMISSIBLE TRUE

RESOLVER_F15_B:

R1 READY / ADMISSIBLE TRUE

Required resolution:

CURRENT
CONSISTENT
ADMISSIBLE

Tool consequence counter:

0

## Stage F15-S1 — Baseline Positive

Authority:

AUTH_F15-BASELINE

Resolver state:

A = R1 READY
B = R1 READY

Expected:

VERDICT:
PERMIT

REASON:
AUTHORIZED

AUTHORITY_CONSUMED_BEFORE:
FALSE

AUTHORITY_CONSUMED_AFTER:
TRUE

CONSEQUENCE_DELTA:
1

TOOL COUNTER AFTER:
1

This establishes only the pre-partition positive control.

## Stage F15-S2 — Material Transition to R2

The authoritative source prospectively transitions:

R1 READY
->
R2 WITHDRAWN

Authoritative current state becomes:

R2 WITHDRAWN / ADMISSIBLE FALSE

A cached historical R1 READY state may still exist locally.

That cached state is historical only.

## Stage F15-S3 — Resolver Unavailable / Partition Negative

The resolver dependency becomes unavailable under the bounded
simulated partition.

RESOLVER_F15_A:

UNAVAILABLE

RESOLVER_F15_B:

UNAVAILABLE

Historical local cache:

R1 READY / ADMISSIBLE TRUE

Authority:

AUTH_F15-PARTITION

Authority remains:

VALID
UNCONSUMED

Expected:

VERDICT:
REFUSE

REASON:
CURRENT_RESOLUTION_UNAVAILABLE

AUTHORITY_CONSUMED_BEFORE:
FALSE

AUTHORITY_CONSUMED_AFTER:
FALSE

CONSEQUENCE_DELTA:
0

TOOL COUNTER REMAINS:
1

The historical cached READY state must not substitute for required
current resolution.

Therefore:

CACHE_AVAILABLE
+
CURRENT_RESOLUTION_UNAVAILABLE
!=
EXECUTION_PERMISSION.

## Stage F15-S4 — Conflicting Resolver Views

A bounded split-view condition is then constituted.

RESOLVER_F15_A reports:

R1 READY / ADMISSIBLE TRUE

RESOLVER_F15_B reports:

R2 WITHDRAWN / ADMISSIBLE FALSE

The authoritative source remains:

R2 WITHDRAWN / ADMISSIBLE FALSE

Authority:

AUTH_F15-CONFLICT

Authority remains:

VALID
UNCONSUMED

Expected:

VERDICT:
REFUSE

REASON:
RESOLVER_STATE_CONFLICT

AUTHORITY_CONSUMED_BEFORE:
FALSE

AUTHORITY_CONSUMED_AFTER:
FALSE

CONSEQUENCE_DELTA:
0

TOOL COUNTER REMAINS:
1

No resolver view may win merely because it is permissive.

No tie-breaking rule may manufacture standing.

## Stage F15-S5 — Current Consistent But Inadmissible

The simulated partition heals.

Both resolvers now correspond exactly to the authoritative source:

RESOLVER_F15_A:

R2 WITHDRAWN / ADMISSIBLE FALSE

RESOLVER_F15_B:

R2 WITHDRAWN / ADMISSIBLE FALSE

Authority:

AUTH_F15-CURRENT-BLOCKED

Authority remains:

VALID
UNCONSUMED

Expected:

VERDICT:
REFUSE

REASON:
RESOLVED_STATE_NOT_ADMISSIBLE

AUTHORITY_CONSUMED_BEFORE:
FALSE

AUTHORITY_CONSUMED_AFTER:
FALSE

CONSEQUENCE_DELTA:
0

TOOL COUNTER REMAINS:
1

This condition proves that:

CONSISTENT
!=
ADMISSIBLE.

Resolver agreement alone is not sufficient for execution.

## Stage F15-S6 — Prospective Recovery

The authoritative source prospectively transitions:

R2 WITHDRAWN
->
R3 READY

Both required resolver replicas synchronize to:

R3 READY / ADMISSIBLE TRUE

Authority:

AUTH_F15-RECOVERY

Expected:

VERDICT:
PERMIT

REASON:
AUTHORIZED

AUTHORITY_CONSUMED_BEFORE:
FALSE

AUTHORITY_CONSUMED_AFTER:
TRUE

CONSEQUENCE_DELTA:
1

FINAL TOOL COUNTER:
2

## Expected Aggregate Outcome

EXECUTION ATTEMPTS:

5

PERMIT:

2

REFUSE:

3

AUTHORIZED CONSEQUENCE TOTAL:

2

UNAUTHORIZED CONSEQUENCE TOTAL:

0

FINAL TOOL_F15 COUNTER:

2

REFUSAL REASONS:

CURRENT_RESOLUTION_UNAVAILABLE

RESOLVER_STATE_CONFLICT

RESOLVED_STATE_NOT_ADMISSIBLE

Each expected exactly once.

## Safe-Degradation Property

The bounded F15 safe-degradation property is:

When required current resolution cannot be established,
the system loses permission to proceed consequentially.

It does not substitute:

- historical cache;
- partial resolver evidence;
- the most permissive resolver;
- execution pressure;
- availability preference;
- or previously admissible state.

The system may recover only prospectively when required current,
consistent and admissible resolution is restored.

## Authority Preservation on Refusal

For each negative attempt:

AUTH_F15-PARTITION

AUTH_F15-CONFLICT

AUTH_F15-CURRENT-BLOCKED

the authority must remain unconsumed after refusal.

Expected:

AUTHORITY_CONSUMED_BEFORE=FALSE

AUTHORITY_CONSUMED_AFTER=FALSE

This demonstrates that refusal is caused by current resolution
standing rather than authority replay.

## Evidence Requirements

The first observation must preserve at minimum:

1. initial authoritative R1 state;
2. initial resolver A state;
3. initial resolver B state;
4. baseline positive attempt;
5. R1 -> R2 authoritative transition;
6. partition/unavailable resolver state;
7. historical cached R1 state;
8. partition negative attempt;
9. conflicting resolver A/B state;
10. conflict negative attempt;
11. healed R2 resolver state;
12. current-but-inadmissible negative attempt;
13. R2 -> R3 authoritative recovery transition;
14. recovered R3 resolver state;
15. recovery positive attempt;
16. final summary;
17. first-observation console;
18. preservation manifest.

Every observed artifact must be preserved whether the examination
returns the expected result or not.

## Required Decision Evidence

Each execution attempt must preserve:

attempt_id

presenter_identity

authority_id

authority_valid

authority_consumed_before

authority_consumed_after

action

tool_identity

authoritative_state_version

authoritative_state

authoritative_admissibility

resolver_a_availability

resolver_a_state_version

resolver_a_state

resolver_a_admissibility

resolver_b_availability

resolver_b_state_version

resolver_b_state

resolver_b_admissibility

cached_state_version if present

cached_state if present

cached_admissibility if present

resolution_status

verdict

reason

consequence_before

consequence_after

consequence_delta

## Pass Conditions

EASA-F15 passes only if:

1. F14-S1 remains unchanged;
2. F15 definition predates implementation;
3. no F15 runtime existed at definition freeze;
4. initial authoritative state is exactly R1 READY / TRUE;
5. both initial resolvers exactly report R1 READY / TRUE;
6. baseline authority begins valid and unconsumed;
7. baseline attempt permits;
8. baseline consequence delta is exactly 1;
9. baseline authority becomes consumed;
10. R1 -> R2 transition is preserved;
11. authoritative current state becomes R2 WITHDRAWN / FALSE;
12. historical R1 cache remains explicitly historical;
13. partition condition makes required current resolution unavailable;
14. partition authority remains valid;
15. partition attempt refuses;
16. partition reason is CURRENT_RESOLUTION_UNAVAILABLE;
17. partition consequence delta is 0;
18. partition authority remains unconsumed;
19. conflict state preserves A=R1 READY and B=R2 WITHDRAWN;
20. conflict authority remains valid;
21. conflict attempt refuses;
22. conflict reason is RESOLVER_STATE_CONFLICT;
23. conflict consequence delta is 0;
24. conflict authority remains unconsumed;
25. healed resolvers both correspond to R2 WITHDRAWN / FALSE;
26. current-blocked authority remains valid;
27. current-blocked attempt refuses;
28. current-blocked reason is RESOLVED_STATE_NOT_ADMISSIBLE;
29. current-blocked consequence delta is 0;
30. current-blocked authority remains unconsumed;
31. R2 -> R3 transition is preserved;
32. authoritative current state becomes R3 READY / TRUE;
33. both resolvers correspond to R3 READY / TRUE;
34. recovery authority begins valid and unconsumed;
35. recovery attempt permits;
36. recovery consequence delta is exactly 1;
37. recovery authority becomes consumed;
38. permit count is exactly 2;
39. refuse count is exactly 3;
40. unauthorized consequence total is 0;
41. final tool counter is exactly 2;
42. every expected refusal reason occurs exactly once;
43. no unavailable resolver state creates execution standing;
44. no cached R1 state substitutes for current resolution;
45. no conflicting resolver view creates execution standing;
46. resolver agreement on an inadmissible state does not create execution standing;
47. safe prospective recovery occurs only after R3 READY becomes current;
48. first observation is preserved regardless of outcome;
49. no retrospective repair is used;
50. closure occurs only from preserved F15 evidence.

## Failure Conditions

EASA-F15 fails if:

- execution occurs while required current resolution is unavailable;
- cached R1 READY standing substitutes for unavailable current resolution;
- either conflicting resolver view is silently selected to permit execution;
- the permissive resolver is preferred merely because it permits;
- resolver disagreement is ignored;
- current R2 WITHDRAWN state permits execution;
- a negative authority is consumed despite refusal;
- any negative attempt changes the tool counter;
- R3 recovery permits before both required resolvers correspond to R3;
- aggregate consequence exceeds 2;
- unauthorized consequence total exceeds 0;
- historical state is rewritten;
- first-observation evidence is replaced;
- or the harness is rerun to improve standing.

## Explicit Non-Claims

EASA-F15 does not establish:

- production network-partition safety;
- distributed consensus correctness;
- Byzantine-fault tolerance;
- Raft correctness;
- Paxos correctness;
- production quorum safety;
- cross-process resolver integrity;
- cross-host resolver integrity;
- multi-region consistency;
- database serializability;
- durable resolver storage;
- crash recovery;
- packet-level network behavior;
- DNS security;
- service-mesh security;
- cloud-control-plane correctness;
- malicious resolver resistance;
- cryptographic resolver attestation;
- arbitrary resolver topologies;
- unlimited resolver count;
- unlimited partition duration;
- real-time liveness guarantees;
- universal availability guarantees;
- universal fail-safe behavior.

## Capability Relationship

Primary:

EASA-CAP-05
Replay, Freshness & Changed-State Security

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

Supporting:

EASA-CAP-02
Security Architecture & Trust-Boundary Design

EASA-CAP-03
Identity, Authorization & Least Privilege

EASA-CAP-08
Evidence, Audit & Forensic Reconstruction

EASA-CAP-09
Secure Change & Configuration Integrity

No capability classification is changed merely by freezing this
definition.

Any capability standing change requires preserved F15 evidence
and subsequent determination.

## First-Observation Discipline

The F15 harness may execute exactly once for its historical
first observation.

PASS, FAIL, exception, partial output or incomplete execution
must be preserved.

NO HARNESS RERUN TO IMPROVE STANDING.

NO EVIDENCE REPLACEMENT.

NO RETROSPECTIVE STATE REMAPPING.

NO RETROSPECTIVE AUTHORITY REPAIR.

NO RETROSPECTIVE RESOLVER NORMALIZATION.

If a material defect is found after execution, a prospectively
constituted successor is required.

## Governing Rules

CURRENT RESOLUTION PRECEDES
DEPENDENT CONSEQUENCE.

UNAVAILABLE
DOES NOT MEAN
PERMITTED.

CONFLICT
DOES NOT MEAN
CHOOSE THE PERMISSIVE VIEW.

CONSISTENCY
DOES NOT MEAN
ADMISSIBILITY.

VALID AUTHORITY
DOES NOT ERASE
CURRENT STATE REQUIREMENTS.

RECOVERY MUST BE
PROSPECTIVE.

Lock it.
Log it.
Prove it.