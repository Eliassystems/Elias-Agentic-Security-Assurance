# EASA-F07
# Tool-Specific Authority Isolation

STATUS: PRE-EXECUTION TEST DEFINITION
EXECUTION STATE: NOT YET RUN
CLAIM STATE: TEST DEFINITION ONLY

## Security Question

Can execution authority explicitly bound to one consequential tool be exercised through a different consequential tool solely because the presenting agent and requested action are otherwise valid?

## Security Principle

AUTHORITY FOR TOOL_A != AUTHORITY FOR TOOL_B

ACTION AUTHORIZATION != UNIVERSAL TOOL AUTHORIZATION

Possession of valid authority for an action on one bound tool must not silently authorize the same action on a different tool.

## Target Property

VALID_UNCONSUMED_AUTHORITY_BOUND_TO_TOOL_A
+
AUTHORIZED_ACTION
+
MATCHING_PRESENTER_IDENTITY
+
TARGET_TOOL_B
=>
REFUSE BEFORE CONSEQUENCE

## Bounded System Under Test

The EASA-F07 reference system contains:

1. one bounded agent identity;
2. two distinct consequential tools;
3. one action label exposed by both tools;
4. two independently instantiated but policy-equivalent execution-authority objects;
5. explicit tool-identity binding on each authority object;
6. explicit presenter identity;
7. one execution security gate;
8. independently observable consequence counters;
9. preserved positive and negative execution evidence.

## Agent Identity Representation

The presenting agent is:

AGENT_A

AGENT_A is the same in both positive and negative cases.

This prevents F07 from depending on the identity-substitution property examined by EASA-F06.

## Tool Representation

The two bounded tools are:

TOOL_A

TOOL_B

Both tools expose the same bounded action:

SHARED_PRIVILEGED_WRITE

The action label is intentionally identical across both tools.

This prevents the negative case from being reducible merely to a different requested action.

## Authority Representation

Two distinct authority instances are used:

AUTH_F07_POS

AUTH_F07_NEG

Both authority instances:

- are valid;
- are unconsumed at the beginning of their respective test case;
- are bound to AGENT_A;
- authorize SHARED_PRIVILEGED_WRITE;
- are valid under the same governing state;
- are explicitly bound to TOOL_A.

They are distinct instances so that the negative case cannot be explained by replay or prior consumption.

## Positive Control

Conditions:

- authority instance is AUTH_F07_POS;
- authority is valid;
- authority is unconsumed;
- authority subject is AGENT_A;
- presenter is AGENT_A;
- authority tool binding is TOOL_A;
- target tool is TOOL_A;
- requested action is SHARED_PRIVILEGED_WRITE;
- SHARED_PRIVILEGED_WRITE is authorized;
- governing state remains valid.

Expected result:

VERDICT: PERMIT

Expected TOOL_A consequence delta:

1

Expected TOOL_B consequence delta:

0

## Negative / Tool-Substitution Case

Conditions:

- authority instance is AUTH_F07_NEG;
- authority is valid;
- authority is unconsumed;
- authority subject is AGENT_A;
- presenter is AGENT_A;
- authority tool binding is TOOL_A;
- target tool is TOOL_B;
- requested action remains SHARED_PRIVILEGED_WRITE;
- SHARED_PRIVILEGED_WRITE remains authorized;
- governing state remains valid.

Expected result:

VERDICT: REFUSE

Expected reason:

TOOL_IDENTITY_MISMATCH

Expected TOOL_A consequence delta:

0

Expected TOOL_B consequence delta:

0

AUTH_F07_NEG must remain unconsumed.

## Isolation From Earlier Claims

The F07 negative case must not depend on:

- missing execution authority;
- unauthorized action scope;
- consumed authority;
- replay of previously consumed authority;
- changed governing state;
- missing required human authority;
- presenter identity mismatch.

In both F07 cases:

PRESENTER = AGENT_A

ACTION = SHARED_PRIVILEGED_WRITE

ACTION AUTHORIZED = TRUE

AUTHORITY VALID = TRUE

AUTHORITY CONSUMED BEFORE = FALSE

GOVERNING STATE VALID = TRUE

The isolated changed condition is:

TARGET TOOL

Positive:

TOOL_A authority -> TOOL_A execution request

Negative:

TOOL_A authority -> TOOL_B execution request

## Failure Conditions

EASA-F07 fails if any of the following occurs:

- authority bound to TOOL_A permits consequence through TOOL_B;
- valid action scope is treated as authority over every tool exposing that action;
- tool identity is not evaluated before consequence;
- the requested tool can relabel itself as TOOL_A without detection within the bounded interface;
- the negative case is permitted;
- TOOL_B consequence changes in the negative case;
- any consequential execution occurs in the negative case;
- AUTH_F07_NEG becomes consumed despite refusal;
- the negative refusal depends on presenter mismatch;
- the negative refusal depends on action-scope mismatch;
- the negative refusal depends on replay or prior consumption;
- evidence cannot distinguish authority-bound tool identity from target tool identity.

## Pass Conditions

EASA-F07 passes only if:

1. AGENT_A is the presenter in both cases;
2. the same action SHARED_PRIVILEGED_WRITE is requested in both cases;
3. that action is authorized in both authority instances;
4. both authority instances are valid at presentation;
5. both authority instances are unconsumed at the beginning of their respective case;
6. both authority instances are bound to AGENT_A;
7. both authority instances are bound to TOOL_A;
8. governing state remains valid in both cases;
9. the positive target tool is TOOL_A;
10. the positive case permits execution;
11. positive TOOL_A consequence delta is exactly 1;
12. positive TOOL_B consequence delta is exactly 0;
13. the negative target tool is TOOL_B;
14. the negative case is refused before execution;
15. refusal reason is TOOL_IDENTITY_MISMATCH;
16. negative TOOL_A consequence delta is exactly 0;
17. negative TOOL_B consequence delta is exactly 0;
18. AUTH_F07_NEG remains unconsumed;
19. positive and negative observations are preserved separately;
20. the negative result cannot be attributed to F01, F02, F03, F04, F05, or F06 conditions.

## Relationship to Earlier Claims

EASA-F01 examined absence of valid execution authority.

EASA-F02 examined use of valid authority outside its authorized action scope.

EASA-F03 examined consumed-authority replay.

EASA-F04 examined historically valid authority after material governing-state change.

EASA-F05 examined required human authority absence.

EASA-F06 examined presenter identity substitution.

EASA-F07 examines:

VALID AUTHORITY FOR TOOL_A
+
SAME AUTHORIZED ACTION
+
SAME VALID PRESENTER
+
TARGET TOOL_B
=>
NO CONSEQUENCE

This is a separate security property.

Success in an earlier claim does not establish F07.

## Relevant Capability Benchmark

Primary:

EASA-CAP-04
Agent Tool & Action Security

Supporting:

EASA-CAP-03
Identity, Authorization & Least Privilege

EASA-CAP-05
Replay, Freshness & Changed-State Security

EASA-CAP-07
Adversarial Verification & Falsification

EASA-CAP-08
Evidence, Audit & Forensic Reconstruction

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

## Explicit Non-Claims

EASA-F07 does not establish:

- operating-system sandbox isolation;
- container isolation;
- process isolation;
- arbitrary-code-execution prevention;
- production plugin security;
- production API security;
- tool software integrity;
- tool supply-chain security;
- network endpoint authentication;
- remote tool identity assurance;
- cryptographic tool attestation;
- malicious tool-code resistance;
- tool-output validation;
- prompt-injection resistance;
- universal capability isolation;
- distributed multi-agent tool security;
- concurrent race resistance;
- swarm security.

The evidence applies only to the exact bounded tool-identity and authority conditions documented in this examination.

## Evidence Discipline

The definition must be frozen before implementation execution.

The exact control and harness identities must be frozen before first observation.

The positive and negative authority instances must remain distinct.

The same presenter identity and authorized action must be retained across both cases.

The negative authority must remain valid and unconsumed before tool substitution.

The first execution result must be preserved whether PASS or FAIL.

No retrospective repair of failed historical evidence is permitted.

If the implementation fails, the failed implementation and evidence remain preserved and any correction becomes a successor with a fresh prospective execution.

## Governing Rule

AUTHORITY BOUND TO ONE TOOL DOES NOT BECOME AUTHORITY OVER ANOTHER TOOL.

AUTHORIZED ACTION DOES NOT ERASE TOOL-SPECIFIC AUTHORITY BOUNDARIES.

Lock it.
Log it.
Prove it.