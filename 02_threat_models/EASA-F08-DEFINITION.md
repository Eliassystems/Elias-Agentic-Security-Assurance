# EASA-F08
# Concurrent Single-Consumption / Collision Control

STATUS: PRE-EXECUTION TEST DEFINITION
EXECUTION STATE: NOT YET RUN
CLAIM STATE: TEST DEFINITION ONLY

## Security Question

Can one valid single-use execution authority produce more than one consequential execution when two separately authorized agents present that same authority under a synchronized concurrent challenge?

## Security Principle

SINGLE-USE AUTHORITY
!=
ONE USE PER CONCURRENT PRESENTER

SINGLE-USE AUTHORITY
=>
AT MOST ONE CONSEQUENTIAL COMMIT

Concurrent possession or presentation must not multiply execution authority.

## Target Property

ONE_VALID_SINGLE_USE_AUTHORITY
+
TWO_EXPLICITLY_AUTHORIZED_PRESENTERS
+
SAME_AUTHORIZED_ACTION
+
SAME_AUTHORIZED_TOOL
+
SYNCHRONIZED_CONCURRENT_PRESENTATION
=>
MAXIMUM_CONSEQUENTIAL_EXECUTIONS = 1

## Bounded System Under Test

The EASA-F08 reference system contains:

1. one bounded consequential tool;
2. one bounded consequential action;
3. two distinct agent identities;
4. one positive-control authority instance;
5. one separate shared single-use authority instance for the concurrent challenge;
6. explicit authorization of both concurrent presenters for the shared authority;
7. one execution security gate;
8. one synchronization barrier used to release concurrent attempts;
9. one observable consequence counter;
10. preserved per-attempt and aggregate execution evidence.

## Agent Representation

The concurrent presenters are:

AGENT_A

and

AGENT_B

For the F08 concurrent challenge, both AGENT_A and AGENT_B are explicitly authorized presenters of the same authority object.

Therefore, refusal of either concurrent attempt must not depend on the identity-mismatch property examined by EASA-F06.

F08 does not claim that an authority bound only to AGENT_A may be used by AGENT_B.

The F08 shared authority is prospectively defined as authorizing both named presenters.

## Tool Representation

The bounded target tool is:

TOOL_F08

The bounded consequential action is:

CONCURRENT_PRIVILEGED_WRITE

The tool and action remain the same for both concurrent attempts.

Therefore, F08 does not depend on the tool-isolation property examined by EASA-F07 or the action-scope property examined by EASA-F02.

## Authority Representation

Two authority objects are used.

### Positive-Control Authority

AUTH_F08_POS

AUTH_F08_POS:

- is valid;
- begins unconsumed;
- authorizes AGENT_A;
- authorizes CONCURRENT_PRIVILEGED_WRITE;
- is bound to TOOL_F08;
- is valid under the governing state;
- permits one consequential execution.

### Concurrent-Challenge Authority

AUTH_F08_CONCURRENT

AUTH_F08_CONCURRENT:

- is one exact shared authority object;
- is valid immediately before concurrent release;
- is unconsumed immediately before concurrent release;
- is single-use;
- explicitly authorizes AGENT_A;
- explicitly authorizes AGENT_B;
- authorizes CONCURRENT_PRIVILEGED_WRITE;
- is bound to TOOL_F08;
- is valid under the governing state.

The exact same AUTH_F08_CONCURRENT authority object is supplied to both concurrent execution attempts.

The two concurrent attempts must not receive separate copies with independent consumption state.

## Positive Control

Conditions:

- authority is AUTH_F08_POS;
- presenter is AGENT_A;
- presenter is authorized;
- authority is valid;
- authority is unconsumed;
- target tool is TOOL_F08;
- action is CONCURRENT_PRIVILEGED_WRITE;
- action is authorized;
- governing state is valid.

Expected result:

VERDICT: PERMIT

Expected consequence delta:

1

Expected authority state after:

CONSUMED = TRUE

This establishes that the bounded one-use execution path functions when there is no concurrent collision.

## Concurrent Collision Challenge

A fresh authority object is used:

AUTH_F08_CONCURRENT

Immediately before synchronized release:

AUTHORITY VALID = TRUE

AUTHORITY CONSUMED = FALSE

REMAINING AUTHORIZED CONSEQUENTIAL USES = 1

AGENT_A AUTHORIZED = TRUE

AGENT_B AUTHORIZED = TRUE

ACTION AUTHORIZED = TRUE

TOOL AUTHORIZED = TRUE

GOVERNING STATE VALID = TRUE

Two worker contexts are prepared.

Worker A presents:

AGENT_A
+
AUTH_F08_CONCURRENT
+
TOOL_F08
+
CONCURRENT_PRIVILEGED_WRITE

Worker B presents:

AGENT_B
+
AUTH_F08_CONCURRENT
+
TOOL_F08
+
CONCURRENT_PRIVILEGED_WRITE

Both workers must reach a common synchronization barrier before either is released to attempt execution.

After common release, both attempts contend for the same single-use authority state.

## Expected Concurrent Outcome

Exactly one concurrent attempt may receive:

VERDICT: PERMIT

Exactly one concurrent attempt must receive:

VERDICT: REFUSE

Expected refusal reason:

EXECUTION_AUTHORITY_ALREADY_CONSUMED

The identity of the winning presenter is not predetermined.

AGENT_A may win or AGENT_B may win.

The required invariant is independent of scheduling order:

PERMIT COUNT = 1

REFUSE COUNT = 1

TOTAL CONSEQUENCE DELTA = 1

FINAL AUTHORITY CONSUMED = TRUE

No execution schedule may produce:

PERMIT COUNT > 1

or:

TOTAL CONSEQUENCE DELTA > 1

## Atomic Consumption Requirement

For this bounded examination, the transition from available single-use authority to consumed authority must be protected as one indivisible execution-gate decision boundary with respect to the concurrent worker attempts.

The implementation must not perform an unsafe sequence equivalent to:

1. worker A observes unconsumed;
2. worker B observes unconsumed;
3. worker A executes;
4. worker B executes;
5. consumption is recorded afterwards.

The bounded security requirement is:

CHECK CURRENT AUTHORITY STATE
+
CLAIM SINGLE USE
=>
ONE COLLISION-SAFE DECISION BOUNDARY

before more than one consequential execution can be authorized.

## Isolation From Earlier Claims

The F08 concurrent refusal must not depend on:

- absent execution authority;
- unauthorized action scope;
- changed governing state;
- absent required human authority;
- presenter identity mismatch;
- tool identity mismatch.

Both concurrent presenters are explicitly authorized.

Both request the same authorized action.

Both target the same authorized tool.

The shared authority is valid and unconsumed immediately before common release.

The contested property is concurrent single consumption.

## Relationship to EASA-F03

EASA-F03 established a sequential condition:

AUTHORITY ALREADY CONSUMED
+
LATER REPLAY ATTEMPT
=>
NO CONSEQUENCE

F08 examines a materially different condition:

ONE AUTHORITY AVAILABLE BEFORE COMMON RELEASE
+
MULTIPLE AUTHORIZED PRESENTERS CONTEND CONCURRENTLY
=>
AT MOST ONE CONSEQUENCE

A PASS in EASA-F03 does not establish EASA-F08.

## Relationship to EASA-F06

EASA-F06 established that an authority bound to AGENT_A could not be exercised by AGENT_B.

F08 does not reuse that negative condition.

AUTH_F08_CONCURRENT explicitly authorizes both AGENT_A and AGENT_B.

Therefore, losing the collision must not be attributable to presenter-identity mismatch.

## Relationship to EASA-F07

EASA-F07 established tool-specific authority isolation.

F08 uses the same authorized tool for both concurrent attempts.

Therefore, losing the collision must not be attributable to tool-identity mismatch.

## Failure Conditions

EASA-F08 fails if any of the following occurs:

- both concurrent attempts are permitted;
- the consequence counter increases by more than one during the concurrent challenge;
- the single-use authority produces two consequential commits;
- both workers independently observe and consume the same available use;
- authority consumption is recorded only after multiple consequences become possible;
- the losing worker is refused for presenter identity mismatch;
- the losing worker is refused for tool mismatch;
- the losing worker is refused for action-scope mismatch;
- the shared authority was already consumed before synchronized release;
- the two concurrent workers did not contend on the same authority state;
- evidence cannot reconstruct each worker's presenter identity, verdict, reason, and consequence outcome;
- evidence cannot establish the aggregate consequence count.

## Pass Conditions

EASA-F08 passes only if:

1. the positive-control authority is distinct from AUTH_F08_CONCURRENT;
2. the positive control begins valid and unconsumed;
3. the positive control permits exactly one consequential execution;
4. AUTH_F08_CONCURRENT is one shared authority object;
5. AUTH_F08_CONCURRENT is valid immediately before concurrent release;
6. AUTH_F08_CONCURRENT is unconsumed immediately before concurrent release;
7. AUTH_F08_CONCURRENT is explicitly single-use;
8. AGENT_A is an authorized presenter;
9. AGENT_B is an authorized presenter;
10. both concurrent workers request CONCURRENT_PRIVILEGED_WRITE;
11. both concurrent workers target TOOL_F08;
12. action scope is authorized for the shared authority;
13. tool binding is valid for both attempts;
14. governing state remains valid;
15. both workers reach the synchronization barrier before common release;
16. exactly two execution attempts are made against the shared authority;
17. exactly one concurrent attempt receives PERMIT;
18. exactly one concurrent attempt receives REFUSE;
19. the refused concurrent attempt reports EXECUTION_AUTHORITY_ALREADY_CONSUMED;
20. total concurrent consequence delta is exactly 1;
21. final shared-authority state is CONSUMED;
22. no duplicate consequential commit occurs;
23. both per-attempt observations are preserved;
24. aggregate collision evidence is preserved;
25. the outcome does not depend on which authorized presenter wins.

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

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

## Explicit Non-Claims

EASA-F08 does not establish:

- distributed consensus;
- distributed locking;
- database transaction serializability;
- cross-host atomicity;
- cross-process atomicity;
- network partition safety;
- arbitrary scheduler independence;
- operating-system process isolation;
- production message-broker exactly-once delivery;
- production payment exactly-once semantics;
- universal linearizability;
- cluster-wide single-consumption;
- multi-region single-consumption;
- crash-recovery correctness;
- rollback correctness after tool failure;
- unlimited concurrency;
- swarm-scale security.

The F08 evidence applies only to the exact bounded thread-based concurrent reference-system conditions documented in this examination.

## Concurrency Boundary

For F08, concurrent presentation means:

two independent worker threads are prepared against one shared authority object and are held at a common synchronization barrier before release.

This establishes contention under the frozen reference harness.

It does not establish arbitrary distributed simultaneity across machines, processes, networks, regions, or external services.

## Evidence Discipline

The definition must be frozen before implementation execution.

The exact control and harness identities must be frozen before first observation.

AUTH_F08_CONCURRENT must not be executed before the frozen concurrent examination.

The first observed concurrent result must be preserved whether PASS or FAIL.

Worker scheduling order must not be retrospectively selected or manipulated to manufacture a PASS.

The winning agent identity is not part of the pass requirement.

No failed first observation may be repaired retrospectively.

Any correction following failure requires a successor implementation and a fresh prospective examination.

## Governing Rule

ONE SINGLE-USE AUTHORITY MAY AUTHORIZE AT MOST ONE CONSEQUENTIAL COMMIT, EVEN UNDER CONCURRENT CONTENTION.

CONCURRENCY DOES NOT MULTIPLY AUTHORITY.

Lock it.
Log it.
Prove it.