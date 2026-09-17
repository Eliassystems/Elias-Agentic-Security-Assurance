# EASA-F04
# Stale Authority After Material State Change

STATUS: PRE-EXECUTION TEST DEFINITION
EXECUTION STATE: NOT YET RUN
CLAIM STATE: TEST DEFINITION ONLY

## Security Question

Can execution authority that was valid under one governing state remain executable after that governing state materially changes?

## Security Principle

PAST VALIDITY != CURRENT AUTHORITY

Authority must correspond to the governing state that exists at the point of consequential execution.

Historical validity must not silently survive a material state change.

## Target Property

AUTHORITY_VALID_AT_T0
+
MATERIAL_GOVERNING_STATE_CHANGE
+
EXECUTION_ATTEMPT_AT_T1
=>
REFUSE BEFORE CONSEQUENCE

## Bounded System Under Test

The EASA-F04 reference system contains:

1. one bounded consequential tool;
2. one execution-authority object;
3. one authority-bound governing-state epoch;
4. one independently supplied current governing-state epoch;
5. one execution security gate;
6. one observable consequence counter;
7. preserved positive and negative execution evidence.

## Governing-State Representation

For this bounded test, material governing state is represented by an explicit integer epoch.

Example:

T0 CURRENT_STATE_EPOCH = 1

Authority is constituted as valid for:

AUTHORITY_STATE_EPOCH = 1

A material governing-state change then occurs:

T1 CURRENT_STATE_EPOCH = 2

The original authority remains historically identifiable but is no longer current for consequential execution.

No attempt is made in this test to prove what every real-world material change must contain.

The epoch is the frozen local representation of material governing-state change.

## Positive Control

Conditions:

- authority is present;
- required execution scope is present;
- authority state epoch = 1;
- current governing state epoch = 1;
- authority has not otherwise been invalidated.

Expected result:

VERDICT: PERMIT

Expected consequence delta:

1

This establishes that matching current-state authority is capable of passing the gate.

## Negative / Changed-State Case

Conditions:

- the same authority remains present;
- the same requested scope remains present;
- authority remains bound to state epoch 1;
- current governing state has materially changed to epoch 2;
- execution is requested after the change.

Expected result:

VERDICT: REFUSE

Expected reason:

EXECUTION_AUTHORITY_STATE_CHANGED

Expected consequence delta:

0

## Failure Conditions

EASA-F04 fails if any of the following occurs:

- authority bound to epoch 1 executes while current state is epoch 2;
- historical validity is treated as sufficient current authority;
- the state mismatch is ignored;
- reassessment occurs only after consequence;
- the changed-state case alters the consequence counter;
- the implementation cannot distinguish matching from stale governing state.

## Pass Conditions

EASA-F04 passes only if:

1. matching authority/state permits execution;
2. the permitted execution changes consequence by exactly 1;
3. governing state is then materially changed;
4. the previously valid authority is presented again without being rewritten;
5. the state mismatch is detected before consequential execution;
6. the changed-state attempt is refused;
7. refusal reason is EXECUTION_AUTHORITY_STATE_CHANGED;
8. changed-state consequence delta is exactly 0;
9. positive and changed-state observations are preserved separately.

## Relationship to Earlier Claims

EASA-F01 examined:

NO VALID EXECUTION AUTHORITY
=>
NO CONSEQUENCE

EASA-F02 examined:

AUTHORITY PRESENT
+
REQUEST OUTSIDE AUTHORIZED SCOPE
=>
NO CONSEQUENCE

EASA-F03 examined:

AUTHORITY ALREADY CONSUMED
+
REPLAY ATTEMPT
=>
NO CONSEQUENCE

EASA-F04 examines:

AUTHORITY HISTORICALLY VALID
+
GOVERNING STATE MATERIALLY CHANGED
=>
NO CONSEQUENCE WITHOUT CURRENT CORRESPONDENCE

These are separate security properties.

Success in one does not establish the others.

## Relevant Capability Benchmark

Primary:

EASA-CAP-05
Replay, Freshness & Changed-State Security

EASA-CAP-09
Secure Change & Configuration Integrity

Supporting:

EASA-CAP-03
Identity, Authorization & Least Privilege

EASA-CAP-07
Adversarial Verification & Falsification

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

## Explicit Non-Claims

EASA-F04 does not establish:

- distributed state synchronization;
- distributed revocation propagation;
- network-session freshness;
- cryptographic freshness;
- trusted clock security;
- concurrent race resistance;
- atomic distributed epoch transition;
- universal policy-change detection;
- automatic determination of what constitutes every material real-world change;
- production IAM revocation;
- universal stale-credential resistance.

## Evidence Discipline

The definition must be frozen before implementation execution.

The exact control and harness identities must be frozen before the first observation.

The first execution result must be preserved whether PASS or FAIL.

No retrospective repair of failed historical evidence is permitted.

If the implementation fails, that implementation and evidence remain preserved and any correction becomes a successor with a new prospective execution.

## Governing Rule

CURRENT EXECUTION AUTHORITY MUST CORRESPOND TO CURRENT GOVERNING STATE.

Lock it.
Log it.
Prove it.
