# EASA-F09
# Multi-Agent Revocation Propagation / Epoch Invalidation

STATUS: PRE-EXECUTION TEST DEFINITION
EXECUTION STATE: NOT YET RUN
CLAIM STATE: TEST DEFINITION ONLY

## Security Question

When multiple independent agent execution nodes initially recognize the same authority epoch as current, does a prospectively constituted authority-epoch change propagate to every participating node such that authorities from the superseded epoch are refused before consequence after revocation receipt?

## Security Principle

PRIOR VALIDITY
!=
PRESENT EXECUTION AUTHORITY

LOCAL PRIOR STANDING
+
CENTRAL AUTHORITY EPOCH CHANGE
+
REVOCATION PROPAGATION
=>
SUPERSEDED AUTHORITY MUST NOT EXECUTE

Revocation must become operational execution state rather than merely documentary state.

## Target Property

MULTIPLE_NODES_AT_EPOCH_1
+
VALID_UNCONSUMED_EPOCH_1_AUTHORITIES
+
CENTRAL_EPOCH_ADVANCE_1_TO_2
+
REVOCATION_EVENT_FOR_EPOCH_1
+
ACKNOWLEDGED_PROPAGATION_TO_ALL_PARTICIPATING_NODES
=>
EPOCH_1_AUTHORITIES_REFUSED_BEFORE_CONSEQUENCE

while:

VALID_EPOCH_2_AUTHORITY
+
NODE_AT_EPOCH_2
=>
PERMIT

## Bounded System Under Test

The EASA-F09 reference system contains:

1. one authoritative epoch source;
2. three independent local execution-node state objects;
3. three distinct agent identities;
4. one bounded consequential action;
5. one bounded consequential tool per node;
6. one revocation event;
7. one propagation mechanism;
8. one acknowledgement receipt per participating node;
9. distinct stale epoch-1 authority objects for each node;
10. one current epoch-2 positive authority;
11. preserved propagation, receipt, decision and consequence evidence.

## Participating Nodes

NODE_A

NODE_B

NODE_C

Each node maintains its own local authority-state object.

The node state objects are separate runtime objects.

Updating NODE_A must not implicitly mutate NODE_B or NODE_C merely through shared-object aliasing.

Each node must receive and apply the revocation event independently through the bounded propagation interface.

## Agent Identities

NODE_A presenter:

AGENT_A

NODE_B presenter:

AGENT_B

NODE_C presenter:

AGENT_C

Each stale authority is prospectively bound to the correct presenter for its node.

Therefore F09 refusal must not depend on the presenter-substitution condition examined in EASA-F06.

## Tool and Action

Each node exposes one bounded tool identity:

TOOL_F09_A

TOOL_F09_B

TOOL_F09_C

The common bounded action is:

EPOCH_BOUND_PRIVILEGED_WRITE

Each stale authority is correctly bound to its node's own tool and to the common action.

Therefore F09 refusal must not depend on action-scope mismatch or tool substitution.

## Initial Authoritative State

Before the material authority change:

AUTHORITATIVE EPOCH = 1

REVOKED EPOCHS = NONE

Each local node state records:

CURRENT EPOCH = 1

REVOKED EPOCHS = NONE

Each node therefore begins from an independently represented local view consistent with the authoritative source.

## Stale Test Authorities

Three distinct epoch-1 authorities are constituted:

AUTH_F09_A_E1

AUTH_F09_B_E1

AUTH_F09_C_E1

Each authority:

- is valid;
- is unconsumed;
- is bound to its correct presenter;
- is bound to its correct node tool;
- authorizes EPOCH_BOUND_PRIVILEGED_WRITE;
- records authority_epoch = 1;
- begins while epoch 1 is authoritative;
- is not executed before the epoch change.

The stale test authorities remain unconsumed so post-change refusal cannot be explained by prior consumption or replay.

## Material Authority Change

A prospective governing event is then constituted:

REVOCATION EVENT ID:

REV_F09_E1_TO_E2

The authoritative source changes:

CURRENT EPOCH:

1 -> 2

REVOKED EPOCHS:

{} -> {1}

The change means that authorities carrying epoch 1 no longer possess present execution standing.

## Revocation Propagation

The exact revocation event is delivered independently to:

NODE_A

NODE_B

NODE_C

Each node must apply the event to its own local state.

After application each node must record:

CURRENT EPOCH = 2

EPOCH 1 REVOKED = TRUE

LAST APPLIED REVOCATION EVENT = REV_F09_E1_TO_E2

## Propagation Receipts

Each node must emit one acknowledgement receipt.

Required receipts:

F09-RECEIPT-NODE-A

F09-RECEIPT-NODE-B

F09-RECEIPT-NODE-C

Each receipt must bind:

- node identity;
- revocation event identity;
- prior local epoch;
- resulting local epoch;
- revoked epoch;
- application status;
- acknowledgement status.

No post-revocation stale-authority execution attempt may occur until all three receipts have been constituted successfully.

This orders the examination as:

CHANGE
->
PROPAGATE
->
ACKNOWLEDGE
->
ATTEMPT EXECUTION

rather than attempting to infer propagation from refusal alone.

## Stale Post-Revocation Attempts

After all propagation acknowledgements exist:

NODE_A attempts:

AUTH_F09_A_E1
+
AGENT_A
+
TOOL_F09_A
+
EPOCH_BOUND_PRIVILEGED_WRITE

NODE_B attempts:

AUTH_F09_B_E1
+
AGENT_B
+
TOOL_F09_B
+
EPOCH_BOUND_PRIVILEGED_WRITE

NODE_C attempts:

AUTH_F09_C_E1
+
AGENT_C
+
TOOL_F09_C
+
EPOCH_BOUND_PRIVILEGED_WRITE

At each node:

AUTHORITY VALID FLAG = TRUE

AUTHORITY CONSUMED BEFORE = FALSE

PRESENTER IDENTITY = CORRECT

ACTION SCOPE = CORRECT

TOOL BINDING = CORRECT

The isolated changed condition is:

AUTHORITY EPOCH 1
vs
LOCAL CURRENT EPOCH 2 / REVOKED EPOCH 1

## Expected Stale Outcome

Each stale epoch-1 attempt must receive:

VERDICT: REFUSE

Expected reason:

AUTHORITY_EPOCH_REVOKED

Expected consequence delta at each node:

0

Each stale authority must remain:

CONSUMED = FALSE

Total stale-attempt consequence delta:

0

## Current-Epoch Positive Control

After propagation, a fresh authority is constituted:

AUTH_F09_CURRENT_E2

Conditions:

- authority_epoch = 2;
- authority valid = TRUE;
- authority consumed = FALSE;
- presenter = AGENT_C;
- presenter authorized = TRUE;
- target tool = TOOL_F09_C;
- action = EPOCH_BOUND_PRIVILEGED_WRITE;
- action authorized = TRUE;
- NODE_C local current epoch = 2;
- epoch 2 not revoked.

Expected result:

VERDICT: PERMIT

Expected reason:

AUTHORIZED

Expected consequence delta:

1

This positive case demonstrates that F09 does not merely disable execution globally after revocation.

## Attack Path

The bounded adversarial path is:

VALID EPOCH-1 AUTHORITY
->
AGENT RETAINS OLD AUTHORITY OBJECT
->
CENTRAL AUTHORITY ADVANCES TO EPOCH 2
->
AGENT OR NODE COULD OTHERWISE RELY ON STALE LOCAL STANDING
->
REVOCATION EVENT PROPAGATES
->
LOCAL NODE STATE UPDATES
->
OLD EPOCH-1 AUTHORITY PRESENTED
->
EXECUTION BOUNDARY COMPARES AUTHORITY EPOCH AGAINST LOCAL CURRENT/REVOKED STATE
->
REFUSE BEFORE CONSEQUENCE

The attack under examination is stale multi-agent execution after a governing authority epoch has been superseded.

## Isolation From Earlier Claims

The F09 stale refusals must not depend on:

- missing authority;
- invalid authority flag;
- consumed authority;
- sequential replay;
- presenter mismatch;
- action-scope mismatch;
- tool mismatch;
- absent human authority.

The stale authority objects remain otherwise valid and unconsumed.

The presenter, action and tool bindings remain correct.

The decisive changed property is authority epoch standing after propagated revocation.

## Relationship to EASA-F04

EASA-F04 examined a changed-state condition against one stale authority execution path.

F09 adds materially different properties:

- multiple independent local node-state objects;
- one authoritative epoch transition;
- explicit revocation-event identity;
- independent propagation to multiple nodes;
- one acknowledgement receipt per node;
- post-propagation stale-authority refusal at every node;
- proof that current epoch-2 authority still executes.

A PASS in F04 does not establish F09.

## Relationship to EASA-F08

EASA-F08 examined concurrent contention over one single-use authority object.

F09 does not test collision ownership.

The F09 authorities are distinct.

The contested property is whether a governing authority transition becomes effective across multiple independently represented execution-node states.

## Failure Conditions

EASA-F09 fails if any of the following occurs:

- the authoritative epoch does not advance from 1 to 2;
- epoch 1 is not recorded as revoked;
- fewer than three node propagation receipts are created;
- any receipt binds the wrong revocation event;
- any node remains at local epoch 1 after acknowledgement;
- any node fails to record epoch 1 as revoked;
- post-revocation execution occurs before all required acknowledgements;
- any epoch-1 stale authority is permitted after acknowledged propagation;
- any stale attempt causes consequence;
- any stale refusal depends on identity mismatch;
- any stale refusal depends on tool mismatch;
- any stale refusal depends on action-scope mismatch;
- any stale refusal depends on prior authority consumption;
- the current epoch-2 positive control is refused despite otherwise valid standing;
- evidence cannot reconstruct the authoritative change, propagation, receipt and execution chain independently for each node.

## Pass Conditions

EASA-F09 passes only if:

1. NODE_A, NODE_B and NODE_C begin as distinct local-state objects;
2. each node begins at local epoch 1;
3. the authoritative source begins at epoch 1;
4. AUTH_F09_A_E1 begins valid and unconsumed;
5. AUTH_F09_B_E1 begins valid and unconsumed;
6. AUTH_F09_C_E1 begins valid and unconsumed;
7. all three stale authorities carry epoch 1;
8. all three stale authorities have correct presenter identity;
9. all three stale authorities have correct tool binding;
10. all three stale authorities authorize EPOCH_BOUND_PRIVILEGED_WRITE;
11. REV_F09_E1_TO_E2 advances authoritative epoch from 1 to 2;
12. epoch 1 becomes authoritatively revoked;
13. the same revocation-event identity is propagated to all three nodes;
14. NODE_A applies the event independently;
15. NODE_B applies the event independently;
16. NODE_C applies the event independently;
17. NODE_A emits a valid acknowledgement receipt;
18. NODE_B emits a valid acknowledgement receipt;
19. NODE_C emits a valid acknowledgement receipt;
20. all required receipts exist before stale attempts begin;
21. each node records local current epoch 2;
22. each node records epoch 1 as revoked;
23. each node records REV_F09_E1_TO_E2 as its applied event;
24. AUTH_F09_A_E1 is refused with AUTHORITY_EPOCH_REVOKED;
25. AUTH_F09_B_E1 is refused with AUTHORITY_EPOCH_REVOKED;
26. AUTH_F09_C_E1 is refused with AUTHORITY_EPOCH_REVOKED;
27. stale consequence delta at NODE_A is 0;
28. stale consequence delta at NODE_B is 0;
29. stale consequence delta at NODE_C is 0;
30. all stale authorities remain unconsumed;
31. total stale consequence delta is 0;
32. AUTH_F09_CURRENT_E2 carries epoch 2;
33. AUTH_F09_CURRENT_E2 is otherwise valid and correctly bound;
34. AUTH_F09_CURRENT_E2 is permitted;
35. current-epoch positive consequence delta is exactly 1;
36. evidence preserves authoritative change, propagation receipts, stale decisions and current positive decision;
37. no node's stale refusal depends on a non-epoch failure condition.

## Relevant Capability Benchmark

Primary:

EASA-CAP-05
Replay, Freshness & Changed-State Security

Supporting:

EASA-CAP-03
Identity, Authorization & Least Privilege

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

EASA-F09 does not establish:

- production distributed consensus;
- production event-bus reliability;
- guaranteed network delivery;
- bounded real-world revocation latency;
- behavior during message loss;
- behavior during network partition;
- asynchronous race safety during partial propagation;
- cross-host atomic broadcast;
- Byzantine node resistance;
- malicious receipt forgery resistance;
- cryptographic receipt authenticity;
- persistent database durability;
- crash-recovery propagation;
- multi-region revocation;
- unlimited agent counts;
- swarm-scale revocation safety.

Those conditions require separate prospective examinations.

## Propagation Boundary

For F09, "multi-agent propagation" means:

one authoritative in-memory epoch source

plus

three separate local execution-node state objects

plus

explicit delivery of one frozen revocation event to each node

plus

one acknowledgement receipt per node

before stale post-revocation execution attempts.

This is a bounded multi-node reference-system examination.

It is not a claim of production network-distributed revocation.

## Evidence Discipline

The definition must be frozen before F09 implementation execution.

The exact control, propagation mechanism and harness identities must be frozen before first observation.

No stale epoch-1 authority may be executed before the frozen post-revocation examination.

The revocation event must be prospectively constituted.

The same event identity must be preserved across every propagation receipt.

Receipts must exist before stale execution attempts begin.

The first observed result must be preserved whether PASS or FAIL.

No missing receipt, failed propagation or stale execution may be retrospectively repaired.

Any correction requires a successor implementation and a fresh prospective examination.

## Governing Rule

AUTHORITY THAT HAS LOST PRESENT STANDING MUST NOT REGAIN EXECUTION POWER THROUGH STALE LOCAL STATE.

REVOCATION MUST PROPAGATE INTO THE EXECUTION BOUNDARY.

Lock it.
Log it.
Prove it.