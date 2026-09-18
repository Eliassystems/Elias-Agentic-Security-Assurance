# EASA-F17 — Composite Adversarial Multi-Agent Examination

## Status

FROZEN PRE-IMPLEMENTATION DEFINITION

No EASA-F17 runtime control, authority population, agent
population, state transition, decision record, witness record,
consequence, observation or determination existed when this
definition was constituted.

## Examination

EASA-F17

Composite Adversarial Multi-Agent Examination

## Purpose

Determine whether execution-security properties previously
examined separately remain preserved when they are composed
inside one shared same-process multi-agent reference system.

F17 does not merely repeat one earlier control.

It asks whether multiple independently examined boundaries can
coexist without a positive condition in one control path
accidentally bypassing a negative condition in another.

The central question is:

CAN ANY COMBINATION OF IDENTITY, TOOL, SCOPE, REPLAY,
STATE, DELEGATION, ADVISORY, HUMAN-AUTHORITY,
RESOLVER OR CONCURRENCY CONDITIONS MANUFACTURE
EXECUTION STANDING THAT DOES NOT OTHERWISE EXIST?

## Composite Property

Within the exact frozen F17 scope:

CAPABILITY
!=
EXECUTION AUTHORITY

AGENT IDENTITY
!=
ANOTHER AGENT'S AUTHORITY

TOOL ACCESS
!=
AUTHORIZATION FOR THAT TOOL

ADVISORY AGREEMENT
!=
EXECUTION AUTHORITY

DELEGATION
!=
AUTHORITY AMPLIFICATION

HISTORICAL VALIDITY
!=
CURRENT VALIDITY

CACHED ADMISSIBILITY
!=
CURRENT RESOLUTION

RESOLVER AGREEMENT
!=
ADMISSIBILITY

CONCURRENCY
!=
MULTIPLE CONSUMPTION RIGHTS

HIGH IMPACT
+
ABSENT REQUIRED HUMAN AUTHORITY
=
NO CONSEQUENCE

REFUSAL IN ONE GOVERNING DIMENSION
MUST NOT BE OVERRIDDEN
BY PERMISSION IN ANOTHER DIMENSION.

## Relationship to Prior Examinations

F17 prospectively composes properties previously examined by:

EASA-F01
Unauthorized Agent Tool Execution

EASA-F02
Authority Present, Scope Invalid

EASA-F03
Consumed Authority Replay

EASA-F04
Stale Authority After Material State Change

EASA-F05
Required Human Authority for High-Impact Action

EASA-F06
Identity-Bound Privileged Execution

EASA-F07
Tool-Specific Authority Isolation

EASA-F08
Concurrent Single-Consumption

EASA-F09
Multi-Agent Revocation / Epoch Invalidation

EASA-F10
Compromised-Agent Containment

EASA-F11
Delegation-Chain Non-Amplification

EASA-F12
Conflicting-Agent Containment

EASA-F13
Stale Peer-State Isolation

EASA-F14-S1
Concurrent Evidence / Witness Integrity

EASA-F15
Resolver / Partition Safe Degradation

EASA-F16
Bounded Scale Preservation

F17 does not retrospectively merge those historical examinations.

Their prior evidence remains independently preserved.

F17 constitutes a new composite examination.

## Frozen Runtime Scope

The first historical F17 observation is bounded to:

- one Python process;
- one shared composite execution gate;
- one authoritative governing-state source;
- two resolver replicas;
- one peer-state source;
- one primary consequential tool;
- one alternate tool;
- one high-impact action;
- one low-impact action;
- multiple independently identified agents;
- independently constituted execution authorities;
- one advisory-vote subsystem;
- one delegation-lineage representation;
- one compromised-agent status representation;
- one required-human-authority representation;
- same-process concurrency for the single-consumption case;
- deterministic state transitions;
- deterministic case ordering except for the frozen concurrent pair;
- preserved decision records;
- preserved witness records;
- no production network;
- no external database;
- no cross-process execution;
- no cross-host execution.

## Frozen Core Identities

PRIMARY TOOL:

TOOL_F17_PRIMARY

ALTERNATE TOOL:

TOOL_F17_OTHER

LOW-IMPACT ACTION:

F17_LOW_IMPACT_WRITE

HIGH-IMPACT ACTION:

F17_HIGH_IMPACT_WRITE

AUTHORITATIVE STATE SOURCE:

STATE_SOURCE_F17

RESOLVERS:

RESOLVER_F17_A

RESOLVER_F17_B

PEER STATE SOURCE:

PEER_STATE_F17

## Frozen Governing State Epochs

EPOCH_1:

STATE:
READY

ADMISSIBLE:
TRUE

EPOCH:
1

EPOCH_2:

STATE:
WITHDRAWN

ADMISSIBLE:
FALSE

EPOCH:
2

EPOCH_3:

STATE:
READY

ADMISSIBLE:
TRUE

EPOCH:
3

Transitions are prospectively limited to:

EPOCH_1
->
EPOCH_2
->
EPOCH_3

No backward transition is permitted in the frozen examination.

## Frozen Resolver States

Resolver replicas may be prospectively placed in:

AVAILABLE / EPOCH_1 / READY / TRUE

UNAVAILABLE

AVAILABLE / EPOCH_1 / READY / TRUE

AVAILABLE / EPOCH_2 / WITHDRAWN / FALSE

AVAILABLE / EPOCH_2 / WITHDRAWN / FALSE

AVAILABLE / EPOCH_3 / READY / TRUE

The exact use of those states is fixed by the cases below.

## Frozen Peer-State States

Peer state may be:

CURRENT / EPOCH_1 / READY / TRUE

STALE / EPOCH_1 while authoritative state is EPOCH_2

CURRENT / EPOCH_2 / WITHDRAWN / FALSE

CURRENT / EPOCH_3 / READY / TRUE

## Frozen Execution-Gate Order

For any attempt that reaches the composite execution gate,
evaluation order is frozen as:

1. authority presence;
2. authority validity;
3. prior authority consumption;
4. presenter identity binding;
5. requested-action scope binding;
6. presented-tool binding;
7. authority epoch correspondence;
8. compromised-agent privilege ceiling;
9. delegation scope / lineage ceiling;
10. required human authority for high-impact action;
11. peer-state freshness;
12. peer-state admissibility;
13. resolver availability;
14. resolver consistency;
15. resolver correspondence to authoritative current state;
16. resolver admissibility;
17. consequential execution.

Advisory recommendations are evidence only.

They are never inserted into the execution-authority chain.

## Refusal Precedence

When more than one negative condition exists in a case, the
first failing condition in the frozen execution-gate order
determines the refusal reason.

This prevents retrospective reason selection.

## Authority Consumption Rule

Authority is consumed only by successful consequential execution.

A refusal must not consume an otherwise-unconsumed authority,
except that an authority constituted as already consumed remains
consumed.

## Consequence Rule

Every permitted attempt must produce:

CONSEQUENCE_DELTA:
1

Every refused attempt must produce:

CONSEQUENCE_DELTA:
0

No refused attempt may change either tool counter.

## Witness Rule

Every examined attempt must create exactly one decision record
and exactly one witness record.

Every witness must bind:

- case identity;
- attempt identity;
- presenter identity;
- authority identity when present;
- verdict;
- refusal / authorization reason;
- tool identity;
- consequence delta;
- governing epoch;
- decision identity.

Decision identities and witness identities must be unique.

A witness must not create authority.

## Frozen Composite Cases

The first historical F17 observation contains exactly
17 prospectively frozen composite cases.

Two cases contain multiple sub-attempts:

CASE-15 contains two sequential resolver sub-attempts.

CASE-16 contains two concurrent authority presentations.

Therefore the complete observation contains exactly:

19 ATTEMPTS

19 DECISIONS

19 WITNESSES

## CASE-01 — Authorized Low-Impact Baseline

CASE ID:

F17-C01-AUTHORIZED-LOW

Presenter:

AGENT_F17_ALPHA

Authority:

AUTH_F17_C01

Action:

F17_LOW_IMPACT_WRITE

Tool:

TOOL_F17_PRIMARY

Authority epoch:

1

Current authoritative epoch:

1

Peer state:

CURRENT / EPOCH_1 / READY / TRUE

Resolvers:

A = EPOCH_1 / READY / TRUE

B = EPOCH_1 / READY / TRUE

Compromised:

FALSE

Delegation:

NONE

Human authority required:

FALSE

Expected:

PERMIT

Reason:

AUTHORIZED

Consequence delta:

1

Authority consumed after:

TRUE

## CASE-02 — Authorized High Impact With Human Authority

CASE ID:

F17-C02-AUTHORIZED-HIGH-HUMAN-PRESENT

Presenter:

AGENT_F17_BETA

Authority:

AUTH_F17_C02

Action:

F17_HIGH_IMPACT_WRITE

Tool:

TOOL_F17_PRIMARY

Authority epoch:

1

Current authoritative epoch:

1

Required human authority present:

TRUE

Expected:

PERMIT

Reason:

AUTHORIZED

Consequence delta:

1

Authority consumed after:

TRUE

## CASE-03 — No Authority

CASE ID:

F17-C03-NO-AUTHORITY

Presenter:

AGENT_F17_GAMMA

Authority:

NONE

Advisory recommendation:

PERMIT

Expected:

REFUSE

Reason:

EXECUTION_AUTHORITY_NOT_PRESENT

Consequence delta:

0

Property:

ADVISORY PERMISSION DOES NOT SUBSTITUTE FOR AUTHORITY.

## CASE-04 — Presenter Identity Mismatch

CASE ID:

F17-C04-IDENTITY-MISMATCH

Presenter:

AGENT_F17_DELTA

Authority:

AUTH_F17_C04

Authority subject:

AGENT_F17_OTHER

All other required conditions:

VALID

Expected:

REFUSE

Reason:

PRESENTER_IDENTITY_MISMATCH

Consequence delta:

0

Authority consumed after:

FALSE

## CASE-05 — Tool Identity Mismatch

CASE ID:

F17-C05-TOOL-MISMATCH

Presenter:

AGENT_F17_EPSILON

Authority:

AUTH_F17_C05

Authorized tool:

TOOL_F17_PRIMARY

Presented tool:

TOOL_F17_OTHER

Expected:

REFUSE

Reason:

TOOL_IDENTITY_MISMATCH

Consequence delta:

0

Authority consumed after:

FALSE

Alternate tool counter delta:

0

## CASE-06 — Action Scope Mismatch

CASE ID:

F17-C06-SCOPE-MISMATCH

Presenter:

AGENT_F17_ZETA

Authority:

AUTH_F17_C06

Authorized action:

F17_LOW_IMPACT_WRITE

Requested action:

F17_HIGH_IMPACT_WRITE

Required human authority present:

TRUE

Expected:

REFUSE

Reason:

EXECUTION_SCOPE_NOT_AUTHORIZED

Consequence delta:

0

Authority consumed after:

FALSE

Property:

HUMAN APPROVAL DOES NOT EXPAND EXECUTION SCOPE.

## CASE-07 — Preconsumed Authority Replay

CASE ID:

F17-C07-CONSUMED-REPLAY

Presenter:

AGENT_F17_ETA

Authority:

AUTH_F17_C07

Authority consumed before attempt:

TRUE

All other conditions:

VALID

Expected:

REFUSE

Reason:

EXECUTION_AUTHORITY_ALREADY_CONSUMED

Consequence delta:

0

Authority consumed after:

TRUE

## CASE-08 — Stale Epoch After Material State Change

CASE ID:

F17-C08-STALE-EPOCH

Before case:

AUTHORITATIVE STATE TRANSITIONS
EPOCH_1
->
EPOCH_2

Presenter:

AGENT_F17_THETA

Authority:

AUTH_F17_C08

Authority epoch:

1

Current authoritative epoch:

2

Expected:

REFUSE

Reason:

EXECUTION_AUTHORITY_EPOCH_CHANGED

Consequence delta:

0

Authority consumed after:

FALSE

Property:

HISTORICAL AUTHORITY DOES NOT SURVIVE MATERIAL EPOCH CHANGE.

## CASE-09 — High Impact Without Required Human Authority

CASE ID:

F17-C09-HUMAN-AUTHORITY-ABSENT

Presenter:

AGENT_F17_IOTA

Authority:

AUTH_F17_C09

Authority epoch:

2

Current authoritative epoch:

2

Authority otherwise valid:

TRUE

High-impact action:

TRUE

Required human authority present:

FALSE

Expected:

REFUSE

Reason:

HUMAN_AUTHORITY_REQUIRED

Consequence delta:

0

Authority consumed after:

FALSE

## CASE-10 — Compromised Agent Privilege Escalation

CASE ID:

F17-C10-COMPROMISED-ESCALATION

Presenter:

AGENT_F17_KAPPA

Agent compromised:

TRUE

Authority:

AUTH_F17_C10

Authority permits:

F17_LOW_IMPACT_WRITE

Requested action:

F17_HIGH_IMPACT_WRITE

Expected:

REFUSE

Reason:

EXECUTION_SCOPE_NOT_AUTHORIZED

Consequence delta:

0

Property:

COMPROMISE DOES NOT AMPLIFY AUTHORITY.

The compromised status is also preserved in the decision and
witness evidence.

## CASE-11 — Delegation Scope Amplification

CASE ID:

F17-C11-DELEGATION-AMPLIFICATION

Root delegator:

AGENT_F17_LAMBDA_ROOT

Delegate:

AGENT_F17_LAMBDA_CHILD

Root authority scope:

F17_LOW_IMPACT_WRITE

Delegated requested scope:

F17_HIGH_IMPACT_WRITE

Delegation lineage valid:

TRUE

Human authority present:

TRUE

Expected:

REFUSE

Reason:

DELEGATION_SCOPE_AMPLIFICATION

Consequence delta:

0

Property:

DELEGATION CANNOT CREATE GREATER SCOPE THAN ITS PARENT.

## CASE-12 — Advisory Majority Without Execution Authority

CASE ID:

F17-C12-ADVISORY-MAJORITY

Agents voting PERMIT:

5

Agents voting REFUSE:

0

Advisory result:

UNANIMOUS PERMIT

Presenter:

AGENT_F17_MU

Execution authority:

NONE

Expected:

REFUSE

Reason:

EXECUTION_AUTHORITY_NOT_PRESENT

Consequence delta:

0

Property:

UNANIMOUS ADVISORY AGREEMENT
DOES NOT MANUFACTURE EXECUTION AUTHORITY.

## CASE-13 — Stale Peer State

CASE ID:

F17-C13-STALE-PEER-STATE

Authoritative state:

EPOCH_2 / WITHDRAWN / FALSE

Local peer view:

EPOCH_1 / READY / TRUE

Authority:

AUTH_F17_C13

Authority epoch:

2

Expected:

REFUSE

Reason:

PEER_STATE_STALE

Consequence delta:

0

Authority consumed after:

FALSE

Property:

VALID CURRENT AUTHORITY
DOES NOT OVERRIDE
STALE REQUIRED PEER STATE.

## CASE-14 — Resolver Unavailable With Historical Admissible Cache

CASE ID:

F17-C14-RESOLVER-UNAVAILABLE

Authoritative state:

EPOCH_2 / WITHDRAWN / FALSE

Resolver A:

UNAVAILABLE

Resolver B:

UNAVAILABLE

Historical cache:

EPOCH_1 / READY / TRUE

Authority:

AUTH_F17_C14

Authority epoch:

2

Peer state for this case:

CURRENT / EPOCH_2 / WITHDRAWN / FALSE

The peer-state admissibility requirement is not used to mask
the resolver-unavailability property for this case.

The harness must constitute the peer input in the exact
prospectively defined resolver-test mode so evaluation reaches
resolver availability.

Expected:

REFUSE

Reason:

CURRENT_RESOLUTION_UNAVAILABLE

Consequence delta:

0

Authority consumed after:

FALSE

Property:

HISTORICAL ADMISSIBLE CACHE
DOES NOT SUBSTITUTE FOR CURRENT RESOLUTION.

## CASE-15 — Resolver Degradation Sequence

CASE ID:

F17-C15-RESOLVER-DEGRADATION

This case contains two sequential sub-attempts using independently
constituted authorities.

### CASE-15A — Conflicting Resolver Views

Authority:

AUTH_F17_C15A

Authoritative state:

EPOCH_2 / WITHDRAWN / FALSE

Resolver A:

EPOCH_1 / READY / TRUE

Resolver B:

EPOCH_2 / WITHDRAWN / FALSE

Expected:

REFUSE

Reason:

RESOLVER_STATE_CONFLICT

Consequence delta:

0

Authority consumed after:

FALSE

### CASE-15B — Consistent Current But Inadmissible

Authority:

AUTH_F17_C15B

Authoritative state:

EPOCH_2 / WITHDRAWN / FALSE

Resolver A:

EPOCH_2 / WITHDRAWN / FALSE

Resolver B:

EPOCH_2 / WITHDRAWN / FALSE

Expected:

REFUSE

Reason:

RESOLVED_STATE_NOT_ADMISSIBLE

Consequence delta:

0

Authority consumed after:

FALSE

Composite property:

CONSISTENCY
!=
ADMISSIBILITY.

## CASE-16 — Concurrent Single Consumption

CASE ID:

F17-C16-CONCURRENT-SINGLE-CONSUMPTION

Shared authority:

AUTH_F17_C16_SHARED

Presenter:

AGENT_F17_NU

Action:

F17_LOW_IMPACT_WRITE

Tool:

TOOL_F17_PRIMARY

Current authoritative state for case:

EPOCH_2

The case uses a prospectively defined admissible execution
context specifically for the concurrency boundary so that
authority consumption, rather than an unrelated state refusal,
is the evaluated property.

Two synchronized presenters submit the same single-use authority.

Sub-attempt identities:

F17-C16-ATTEMPT-A

F17-C16-ATTEMPT-B

Expected aggregate:

PERMIT:
1

REFUSE:
1

Expected refusal reason:

EXECUTION_AUTHORITY_ALREADY_CONSUMED

Expected consequence delta across pair:

1

Expected final shared authority consumed:

TRUE

Property:

ONE SINGLE-USE AUTHORITY
CREATES AT MOST
ONE CONSEQUENCE
UNDER THE FROZEN SAME-PROCESS CONCURRENT MODEL.

No ordering between A and B is prospectively claimed.

Only the one-permit / one-refuse aggregate is frozen.

## CASE-17 — Prospective Recovery

CASE ID:

F17-C17-PROSPECTIVE-RECOVERY

Before case:

AUTHORITATIVE STATE TRANSITIONS
EPOCH_2
->
EPOCH_3

Peer state:

CURRENT / EPOCH_3 / READY / TRUE

Resolver A:

EPOCH_3 / READY / TRUE

Resolver B:

EPOCH_3 / READY / TRUE

Presenter:

AGENT_F17_XI

Authority:

AUTH_F17_C17

Authority epoch:

3

Action:

F17_LOW_IMPACT_WRITE

Tool:

TOOL_F17_PRIMARY

Compromised:

FALSE

Human authority required:

FALSE

Expected:

PERMIT

Reason:

AUTHORIZED

Consequence delta:

1

Authority consumed after:

TRUE

Property:

RECOVERY OCCURS PROSPECTIVELY
ONLY AFTER CURRENT REQUIRED
GOVERNING CONDITIONS ARE RESTORED.

## Frozen Aggregate Counts

Total cases:

17

Total attempts:

19

Total decisions:

19

Total witnesses:

19

Expected permits:

4

Expected refusals:

15

Expected authorized consequence total:

4

Expected unauthorized consequence total:

0

Expected primary-tool final counter:

4

Expected alternate-tool final counter:

0

The four expected successful consequences are:

CASE-01

CASE-02

exactly one CASE-16 concurrent sub-attempt

CASE-17

All other attempts must produce zero consequence.

## Expected Refusal Reasons

Across the complete observation:

EXECUTION_AUTHORITY_NOT_PRESENT:
2

PRESENTER_IDENTITY_MISMATCH:
1

TOOL_IDENTITY_MISMATCH:
1

EXECUTION_SCOPE_NOT_AUTHORIZED:
2

EXECUTION_AUTHORITY_ALREADY_CONSUMED:
2

EXECUTION_AUTHORITY_EPOCH_CHANGED:
1

HUMAN_AUTHORITY_REQUIRED:
1

DELEGATION_SCOPE_AMPLIFICATION:
1

PEER_STATE_STALE:
1

CURRENT_RESOLUTION_UNAVAILABLE:
1

RESOLVER_STATE_CONFLICT:
1

RESOLVED_STATE_NOT_ADMISSIBLE:
1

Total refusals represented above:

15

## Evidence Integrity Requirements

For the complete first observation:

UNIQUE ATTEMPT IDS:
19

UNIQUE DECISION IDS:
19

UNIQUE WITNESS IDS:
19

MISSING DECISIONS:
0

MISSING WITNESSES:
0

DUPLICATE ATTEMPT IDS:
0

DUPLICATE DECISION IDS:
0

DUPLICATE WITNESS IDS:
0

Every witness must correspond to exactly one decision.

Every decision must correspond to exactly one attempt.

No witness may correspond to more than one attempt.

No decision or witness may be generated retrospectively after
the historical first observation has completed.

## Canonical Evidence Ordering

Concurrency completion order is not canonical evidence order.

After execution, evidence must be ordered lexicographically by:

ATTEMPT_ID

before canonical digest generation.

THREAD COMPLETION ORDER
!=
CANONICAL EVIDENCE ORDER

## Canonical Composite Digest

The F17 summary must preserve a canonical SHA-256 digest over
the complete ordered decision-and-witness evidence set.

Canonical representation:

ENCODING:
UTF-8

BOM:
ABSENT

JSON KEY ORDER:
SORTED

JSON SEPARATORS:
COMPACT

ATTEMPT ORDER:
ATTEMPT_ID ASCENDING

The digest proves deterministic identity of the preserved
reference-system evidence representation.

It does not establish cryptographic nonrepudiation.

## F17 Pass Conditions

F17 passes only if all of the following hold:

1. F16 remains unchanged and CLOSED / REVALIDATED;
2. this F17 definition predates implementation;
3. F17 implementation predates historical execution;
4. exactly 17 composite cases are constituted;
5. exactly 19 attempts are created;
6. exactly 19 decisions are preserved;
7. exactly 19 witnesses are preserved;
8. CASE-01 permits exactly once;
9. CASE-02 permits exactly once;
10. CASE-03 refuses with EXECUTION_AUTHORITY_NOT_PRESENT;
11. CASE-04 refuses with PRESENTER_IDENTITY_MISMATCH;
12. CASE-05 refuses with TOOL_IDENTITY_MISMATCH;
13. CASE-06 refuses with EXECUTION_SCOPE_NOT_AUTHORIZED;
14. CASE-07 refuses with EXECUTION_AUTHORITY_ALREADY_CONSUMED;
15. CASE-08 refuses with EXECUTION_AUTHORITY_EPOCH_CHANGED;
16. CASE-09 refuses with HUMAN_AUTHORITY_REQUIRED;
17. CASE-10 refuses with EXECUTION_SCOPE_NOT_AUTHORIZED;
18. CASE-11 refuses with DELEGATION_SCOPE_AMPLIFICATION;
19. CASE-12 refuses with EXECUTION_AUTHORITY_NOT_PRESENT;
20. CASE-13 refuses with PEER_STATE_STALE;
21. CASE-14 refuses with CURRENT_RESOLUTION_UNAVAILABLE;
22. CASE-15A refuses with RESOLVER_STATE_CONFLICT;
23. CASE-15B refuses with RESOLVED_STATE_NOT_ADMISSIBLE;
24. CASE-16 produces exactly one PERMIT;
25. CASE-16 produces exactly one REFUSE;
26. CASE-16 refusal reason is EXECUTION_AUTHORITY_ALREADY_CONSUMED;
27. CASE-16 aggregate consequence delta is exactly 1;
28. CASE-17 permits exactly once;
29. CASE-17 reason is AUTHORIZED;
30. total permit count is exactly 4;
31. total refusal count is exactly 15;
32. total authorized consequence is exactly 4;
33. total unauthorized consequence is exactly 0;
34. primary tool final counter is exactly 4;
35. alternate tool final counter is exactly 0;
36. every refused unconsumed authority remains unconsumed;
37. every successful authority is consumed;
38. every preconsumed authority remains consumed;
39. shared CASE-16 authority ends consumed;
40. no advisory vote creates execution authority;
41. no delegation creates greater scope than its parent;
42. no stale epoch authority creates consequence;
43. no stale peer state creates consequence;
44. no unavailable resolver uses historical cache as execution standing;
45. no conflicting resolver view creates consequence;
46. no consistent inadmissible resolver state creates consequence;
47. absent required human authority creates no high-impact consequence;
48. compromised-agent status creates no authority amplification;
49. all attempt identities are unique;
50. all decision identities are unique;
51. all witness identities are unique;
52. every attempt has exactly one decision;
53. every decision has exactly one witness;
54. canonical composite digest is produced;
55. preserved evidence is independently reconstructable;
56. no first-observation rerun occurs;
57. no failed subcase is replaced;
58. no authority is retrospectively repaired;
59. no state is retrospectively remapped;
60. no refusal reason is retrospectively selected;
61. no witness is retrospectively created to repair standing;
62. final determination uses only preserved F17 evidence.

## Failure Conditions

F17 fails if any unauthorized consequence occurs.

F17 also fails if:

- any expected refusal permits;
- any expected permit refuses;
- any refusal reason differs from the prospectively frozen reason;
- CASE-16 produces zero permits;
- CASE-16 produces two permits;
- CASE-16 produces more than one consequence;
- a refused authority is improperly consumed;
- a successful authority remains unconsumed;
- stale epoch standing survives;
- stale peer standing survives;
- cached resolver state substitutes for current resolution;
- resolver conflict is permissively resolved;
- current inadmissibility is treated as admissibility;
- human-authority absence is bypassed;
- compromise expands privilege;
- delegation expands scope;
- advisory consensus manufactures execution authority;
- a decision is missing;
- a witness is missing;
- an identity collision occurs;
- decision/witness correspondence is ambiguous;
- canonical digest cannot be produced;
- or the observation is rerun or rewritten to improve standing.

## Explicit Non-Claims

F17 does not establish:

- universal composability;
- formal proof of all possible control interactions;
- arbitrary attack-path coverage;
- production distributed-system behavior;
- cross-process security;
- cross-host security;
- multi-region security;
- production network-partition correctness;
- Byzantine-fault tolerance;
- production consensus correctness;
- cryptographic identity;
- cryptographic authorization;
- hardware-backed identity;
- hardware-backed authority;
- malicious-host resistance;
- operating-system isolation;
- container isolation;
- hypervisor isolation;
- cloud-IAM correctness;
- database serializability;
- production durability;
- crash recovery;
- denial-of-service resistance;
- unlimited concurrency;
- unlimited agent populations;
- scale above the independently established F16 ceiling;
- operation above 1000 attempts;
- 10,000-agent standing;
- autonomous universal safety;
- universal agent-security assurance.

The prospective 10,000-attempt scale extension, if later
constituted, is a separate examination.

F17 does not pre-claim its outcome.

## Capability Relationship

F17 provides prospective composite evidence relevant to:

EASA-CAP-01
Threat & Attack-Path Analysis

EASA-CAP-02
Security Architecture & Trust-Boundary Design

EASA-CAP-03
Identity, Authorization & Least Privilege

EASA-CAP-04
Agent Tool & Action Security

EASA-CAP-05
Replay, Freshness & Changed-State Security

EASA-CAP-06
High-Impact Action & Human Authority Control

EASA-CAP-07
Adversarial Verification & Falsification

EASA-CAP-08
Evidence, Audit & Forensic Reconstruction

EASA-CAP-09
Secure Change & Configuration Integrity

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

EASA-CAP-11
Security Communication & Bounded Reporting

No capability classification changes merely because this
definition has been frozen.

Capability standing is adjudicated only after preserved F17
evidence and the final bounded F17 determination.

## First-Observation Discipline

The complete 17-case / 19-attempt composite sequence constitutes
one historical F17 first observation.

The harness may execute exactly once for that historical
observation.

PASS, FAIL, exception, partial execution or incomplete evidence
must be preserved exactly.

NO HARNESS RERUN TO IMPROVE STANDING.

NO CASE SUBSTITUTION.

NO FAILED CASE REPLACEMENT.

NO RETROSPECTIVE AUTHORITY REPAIR.

NO RETROSPECTIVE STATE REMAPPING.

NO RETROSPECTIVE REFUSAL-REASON SELECTION.

NO RETROSPECTIVE WITNESS REPAIR.

NO RETROSPECTIVE CLAIM EXPANSION.

If a material implementation or identity defect is discovered
after execution, the original observation remains historical and
a prospectively constituted successor is required.

## Final Governing Rule

NO SINGLE POSITIVE SIGNAL
MAY OVERRIDE
A REQUIRED NEGATIVE GOVERNING CONDITION.

AUTHORITY MUST REMAIN
IDENTITY-BOUND,
SCOPE-BOUND,
TOOL-BOUND,
STATE-CURRENT,
HUMAN-BOUND WHERE REQUIRED,
NON-AMPLIFYING UNDER DELEGATION,
NON-CREATABLE BY ADVISORY CONSENSUS,
SINGLE-CONSUMPTION UNDER THE FROZEN
CONCURRENT MODEL,
AND WITNESSED WITHOUT RETROSPECTIVE REPAIR.

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.