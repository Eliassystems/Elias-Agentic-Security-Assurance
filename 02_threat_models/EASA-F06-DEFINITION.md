# EASA-F06
# Identity-Bound Privileged Execution

STATUS: PRE-EXECUTION TEST DEFINITION
EXECUTION STATE: NOT YET RUN
CLAIM STATE: TEST DEFINITION ONLY

## Security Question

Can privileged execution authority bound to one agent identity be exercised by a different presenting agent solely because that different agent possesses the authority object?

## Security Principle

POSSESSION != SUBJECT AUTHORITY

AUTHORITY FOR AGENT_A != AUTHORITY FOR AGENT_B

Possession of an execution-authority object must not silently transfer the authority represented by that object to a different agent identity.

## Target Property

VALID_UNCONSUMED_AUTHORITY_BOUND_TO_AGENT_A
+
PRESENTER_AGENT_B
=>
REFUSE BEFORE CONSEQUENCE

## Bounded System Under Test

The EASA-F06 reference system contains:

1. one bounded privileged consequential action;
2. two distinct agent identities;
3. two independently instantiated but policy-equivalent execution-authority objects;
4. explicit subject-identity binding on each authority object;
5. explicit presenter identity supplied at execution time;
6. one execution security gate;
7. one observable consequence counter;
8. preserved positive and negative execution evidence.

## Privileged Action Representation

For this bounded test, the consequential action is represented as:

PRIVILEGED_WRITE

The same action and authorized scope are used in the positive and negative cases.

## Agent Identity Representation

The bounded identities are represented as:

AGENT_A

and

AGENT_B

These identities are explicit reference-system identities supplied independently to the execution gate.

The agent request does not create or redefine the identity to which authority is bound.

This examination does not claim biometric, cryptographic, legal, or production IAM identity assurance.

It examines whether the bounded execution gate preserves an already-supplied identity-to-authority binding.

## Authority Representation

Two distinct execution-authority instances are used:

AUTH_F06_POS

AUTH_F06_NEG

Both authority instances:

- authorize PRIVILEGED_WRITE;
- contain the same required action scope;
- are valid under the same governing state;
- are unconsumed at the beginning of their respective test case;
- are bound to AGENT_A.

They are distinct authority instances so that the negative case cannot be explained by prior consumption or replay.

The positive and negative cases therefore differ in the presenting agent identity, not in authority validity, authority freshness, action scope, or governing state.

## Positive Control

Conditions:

- action is PRIVILEGED_WRITE;
- authority instance is AUTH_F06_POS;
- AUTH_F06_POS is valid;
- AUTH_F06_POS is unconsumed;
- AUTH_F06_POS is bound to AGENT_A;
- required action scope is present;
- presenter identity is AGENT_A;
- governing state remains valid.

Expected result:

VERDICT: PERMIT

Expected consequence delta:

1

This establishes that the bounded privileged action may execute when the presenting identity matches the authority subject identity and all other required conditions are satisfied.

## Negative / Presenter-Substitution Case

Conditions:

- action is PRIVILEGED_WRITE;
- authority instance is AUTH_F06_NEG;
- AUTH_F06_NEG is valid;
- AUTH_F06_NEG is unconsumed;
- AUTH_F06_NEG is bound to AGENT_A;
- required action scope is present;
- presenter identity is AGENT_B;
- governing state remains valid;
- AGENT_B possesses or presents AUTH_F06_NEG;
- AGENT_B requests execution.

Expected result:

VERDICT: REFUSE

Expected reason:

PRESENTER_IDENTITY_MISMATCH

Expected consequence delta:

0

## Isolation From Earlier Claims

The F06 negative case must not depend on:

- absent execution authority;
- invalid action scope;
- consumed authority;
- replay of a previously consumed authority;
- material governing-state change;
- absence of required human authority.

AUTH_F06_NEG must be valid and unconsumed when AGENT_B presents it.

This isolates the examined property:

AUTHORITY SUBJECT IDENTITY != PRESENTER IDENTITY

## Failure Conditions

EASA-F06 fails if any of the following occurs:

- AGENT_B produces consequence using authority bound to AGENT_A;
- possession of AUTH_F06_NEG is treated as transfer of authority;
- presenter identity is not evaluated before consequence;
- authority subject identity is not evaluated before consequence;
- the implementation silently rebinds authority from AGENT_A to AGENT_B;
- the negative case is permitted;
- the negative case produces any consequence delta;
- the negative refusal depends on prior consumption rather than identity mismatch;
- the implementation cannot distinguish AGENT_A from AGENT_B;
- the implementation cannot distinguish authority subject identity from presenter identity.

## Pass Conditions

EASA-F06 passes only if:

1. the same defined privileged action is used in positive and negative cases;
2. equivalent authorized scope is present in both cases;
3. governing state remains valid in both cases;
4. both authority instances are valid at presentation;
5. both authority instances are unconsumed at the beginning of their respective case;
6. both authority instances are bound to AGENT_A;
7. the positive presenter is AGENT_A;
8. the positive case permits execution;
9. positive consequence delta is exactly 1;
10. the negative presenter is AGENT_B;
11. AGENT_B presents a valid unconsumed authority object bound to AGENT_A;
12. the negative case is refused before execution;
13. refusal reason is PRESENTER_IDENTITY_MISMATCH;
14. negative consequence delta is exactly 0;
15. positive and negative observations are preserved separately;
16. the negative result cannot be attributed to replay, prior consumption, scope failure, changed governing state, or absent human authority.

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

EASA-F04 examined:

AUTHORITY HISTORICALLY VALID
+
GOVERNING STATE MATERIALLY CHANGED
=>
NO CONSEQUENCE WITHOUT CURRENT CORRESPONDENCE

EASA-F05 examined:

HIGH_IMPACT_ACTION
+
REQUIRED HUMAN AUTHORITY ABSENT
=>
NO CONSEQUENCE

EASA-F06 examines:

VALID UNCONSUMED AUTHORITY BOUND TO AGENT_A
+
PRESENTER AGENT_B
=>
NO CONSEQUENCE

These are separate security properties.

Success in one does not establish the others.

## Relevant Capability Benchmark

Primary:

EASA-CAP-03
Identity, Authorization & Least Privilege

Supporting:

EASA-CAP-04
Agent Tool & Action Security

EASA-CAP-05
Replay, Freshness & Changed-State Security

EASA-CAP-07
Adversarial Verification & Falsification

EASA-CAP-08
Evidence, Audit & Forensic Reconstruction

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

## Explicit Non-Claims

EASA-F06 does not establish:

- production IAM assurance;
- cryptographic identity verification;
- biometric identity verification;
- human identity verification;
- identity federation security;
- distributed identity consensus;
- Sybil resistance;
- credential lifecycle security;
- credential issuance security;
- credential revocation infrastructure;
- resistance where an attacker is indistinguishable from the legitimate principal at the supplied identity boundary;
- network authentication security;
- hardware-backed identity;
- multi-agent swarm security;
- concurrent race resistance;
- distributed replay resistance;
- universal least-privilege enforcement;
- universal prevention of identity theft or credential compromise.

The evidence applies only to the exact bounded identity and authority conditions documented in this examination.

## Evidence Discipline

The definition must be frozen before implementation execution.

The exact control and harness identities must be frozen before first observation.

The positive and negative authority instances must remain distinct.

The negative authority instance must be valid and unconsumed before the presenter-substitution attempt.

The first execution result must be preserved whether PASS or FAIL.

No retrospective repair of failed historical evidence is permitted.

If the implementation fails, the failed implementation and evidence remain preserved and any correction becomes a successor with a new prospective execution.

## Governing Rule

AUTHORITY MAY BE EXERCISED ONLY BY ITS BOUND SUBJECT IDENTITY.

POSSESSION OF AN AUTHORITY OBJECT DOES NOT TRANSFER AUTHORITY.

Lock it.
Log it.
Prove it.