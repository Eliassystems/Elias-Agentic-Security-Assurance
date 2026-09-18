# EASA-F10
# Compromised-Agent Containment

STATUS: PRE-EXECUTION TEST DEFINITION
EXECUTION STATE: NOT YET RUN
CLAIM STATE: TEST DEFINITION ONLY

## Security Question

When one bounded agent is treated as compromised and attempts to misuse borrowed authority, superseded authority, and lower-privilege tool authority, does the execution boundary contain those attempts without:

1. producing unauthorized consequence;
2. conferring additional execution authority;
3. consuming or corrupting a legitimate peer's authority;
4. weakening peer standing;
5. disabling legitimate bounded execution?

## Security Principle

AGENT COMPROMISE
!=
AUTHORITY EXPANSION

ATTACKER POSSESSION OF AN AUTHORITY ARTIFACT
!=
EXECUTION AUTHORITY

FAILED MALICIOUS ATTEMPT
!=
PEER AUTHORITY LOSS

LOWER-PRIVILEGE AUTHORITY
!=
HIGHER-PRIVILEGE TOOL AUTHORITY

Containment requires both:

NO UNAUTHORIZED CONSEQUENCE

and

NO COLLATERAL AUTHORITY CORRUPTION

## Target Property

COMPROMISED_AGENT_X
+
BORROWED / STALE / TOOL-ESCALATION ATTEMPTS
=>
NO UNAUTHORIZED CONSEQUENCE
+
NO AUTHORITY AMPLIFICATION
+
NO PEER-STANDING CORRUPTION

while:

LEGITIMATE_PEER_AUTHORITY
=>
REMAINS EXECUTABLE

and:

LEGITIMATE_LOW-PRIVILEGE AUTHORITY FOR AGENT_X
=>
REMAINS USABLE ONLY WITHIN ITS ORIGINAL BOUNDARY

## Bounded System Under Test

The EASA-F10 reference system contains:

1. one compromised-agent identity;
2. one legitimate peer identity;
3. one current authority epoch;
4. one revoked prior epoch;
5. one peer consequential tool;
6. one low-privilege tool;
7. one higher-privilege tool;
8. one common bounded consequential action;
9. one fresh legitimate peer authority;
10. one stale authority belonging to the compromised agent;
11. one current low-privilege authority belonging to the compromised agent;
12. preserved attack-path decisions;
13. preserved post-attack peer-standing evidence;
14. preserved post-attack bounded-positive evidence.

## Identities

Compromised agent:

AGENT_X

Legitimate peer:

AGENT_A

The statement "compromised" is a frozen examination condition.

F10 does not claim to detect compromise.

It examines what happens when a known compromised actor interacts with already-defined authority boundaries.

## Epoch State

Current execution epoch:

2

Revoked epoch:

1

Epoch 1 is explicitly recorded as revoked before the stale-authority attack.

Epoch 2 is current and valid.

## Tools

Legitimate peer tool:

TOOL_F10_PEER

Compromised agent low-privilege tool:

TOOL_F10_LOW

Higher-privilege tool:

TOOL_F10_HIGH

## Bounded Action

The common bounded action is:

F10_PRIVILEGED_WRITE

Using the same action across low and high tools ensures the tool-escalation test cannot be explained merely by a different action label.

## Authority A — Legitimate Peer Authority

AUTH_F10_PEER_A

Properties:

SUBJECT = AGENT_A

AUTHORITY EPOCH = 2

VALID = TRUE

CONSUMED = FALSE

AUTHORIZED ACTION = F10_PRIVILEGED_WRITE

BOUND TOOL = TOOL_F10_PEER

This exact authority is intentionally exposed to the compromised-agent borrowed-authority attempt.

The hostile attempt must not consume, invalidate, mutate, replace, revoke, or otherwise damage AUTH_F10_PEER_A.

After the hostile attempt, AGENT_A must be able to use the exact same authority successfully.

## Authority B — Compromised Agent Stale Authority

AUTH_F10_X_STALE_E1

Properties:

SUBJECT = AGENT_X

AUTHORITY EPOCH = 1

VALID FLAG = TRUE

CONSUMED = FALSE

AUTHORIZED ACTION = F10_PRIVILEGED_WRITE

BOUND TOOL = TOOL_F10_LOW

Epoch 1 is revoked.

This authority is correctly bound to AGENT_X, the requested action, and TOOL_F10_LOW.

Therefore refusal of this attack must isolate superseded authority standing rather than identity or tool mismatch.

## Authority C — Compromised Agent Current Low-Privilege Authority

AUTH_F10_X_LOW_E2

Properties:

SUBJECT = AGENT_X

AUTHORITY EPOCH = 2

VALID = TRUE

CONSUMED = FALSE

AUTHORIZED ACTION = F10_PRIVILEGED_WRITE

BOUND TOOL = TOOL_F10_LOW

This authority gives AGENT_X bounded legitimate capability.

It must not confer authority over TOOL_F10_HIGH.

A failed high-tool escalation attempt must leave AUTH_F10_X_LOW_E2 unconsumed so that its legitimate low-tool use can still succeed afterward.

## Attack Path 1 — Borrowed Peer Authority / Presenter Substitution

AGENT_X obtains possession of:

AUTH_F10_PEER_A

AGENT_X presents the peer authority to:

TOOL_F10_PEER

for:

F10_PRIVILEGED_WRITE

All authority conditions except presenter identity remain valid.

Expected:

VERDICT = REFUSE

REASON = PRESENTER_IDENTITY_MISMATCH

CONSEQUENCE DELTA = 0

AUTH_F10_PEER_A remains:

VALID = TRUE

CONSUMED = FALSE

This attack combines possession of another agent's authority artifact with presenter substitution.

Possession alone must not transfer execution standing.

## Attack Path 2 — Superseded / Stale Authority

AGENT_X presents:

AUTH_F10_X_STALE_E1

to:

TOOL_F10_LOW

for:

F10_PRIVILEGED_WRITE

Conditions:

PRESENTER = CORRECT

TOOL = CORRECT

ACTION = CORRECT

VALID FLAG = TRUE

CONSUMED = FALSE

AUTHORITY EPOCH = 1

CURRENT EPOCH = 2

EPOCH 1 REVOKED = TRUE

Expected:

VERDICT = REFUSE

REASON = AUTHORITY_EPOCH_REVOKED

CONSEQUENCE DELTA = 0

AUTHORITY REMAINS UNCONSUMED

## Attack Path 3 — Tool Privilege Escalation

AGENT_X presents:

AUTH_F10_X_LOW_E2

to:

TOOL_F10_HIGH

for:

F10_PRIVILEGED_WRITE

Conditions:

PRESENTER = CORRECT

AUTHORITY EPOCH = CURRENT

AUTHORITY VALID = TRUE

AUTHORITY CONSUMED = FALSE

ACTION = AUTHORIZED

Authority is bound only to:

TOOL_F10_LOW

Expected:

VERDICT = REFUSE

REASON = TOOL_IDENTITY_MISMATCH

HIGH-TOOL CONSEQUENCE DELTA = 0

AUTH_F10_X_LOW_E2 remains:

CONSUMED = FALSE

The compromised agent's legitimate lower-privilege authority must not amplify itself into higher-tool authority.

## Post-Attack Peer Integrity Test

After the compromised-agent borrowed-authority attempt, the exact same:

AUTH_F10_PEER_A

must be presented by:

AGENT_A

to:

TOOL_F10_PEER

for:

F10_PRIVILEGED_WRITE

Expected:

VERDICT = PERMIT

REASON = AUTHORIZED

CONSEQUENCE DELTA = 1

AUTHORITY CONSUMED AFTER = TRUE

This test is required to demonstrate that the malicious attempt did not corrupt or consume the legitimate peer's standing.

## Post-Attack Low-Privilege Integrity Test

After the failed TOOL_F10_HIGH escalation attempt, the exact same:

AUTH_F10_X_LOW_E2

must be presented by:

AGENT_X

to its authorized:

TOOL_F10_LOW

for:

F10_PRIVILEGED_WRITE

Expected:

VERDICT = PERMIT

REASON = AUTHORIZED

LOW-TOOL CONSEQUENCE DELTA = 1

AUTHORITY CONSUMED AFTER = TRUE

This demonstrates selective containment:

the compromised agent is denied capability outside its authority boundary without the system manufacturing an unnecessary global disable of capability that remains explicitly authorized.

## Required Aggregate Consequences

Unauthorized attack-path consequence delta:

0

Peer legitimate consequence delta:

1

Compromised-agent legitimate low-boundary consequence delta:

1

High-tool consequence delta:

0

No attack path may produce consequential execution.

## Required Authority Integrity

After Attack Path 1:

AUTH_F10_PEER_A must remain valid and unconsumed.

After Attack Path 2:

AUTH_F10_X_STALE_E1 must remain unconsumed.

After Attack Path 3:

AUTH_F10_X_LOW_E2 must remain valid and unconsumed.

A refused malicious attempt must not mutate an otherwise reusable legitimate authority merely because an unauthorized actor attempted to present it.

## Peer-State Containment

The compromised agent must not be able to change:

- AGENT_A identity standing;
- AUTH_F10_PEER_A subject binding;
- AUTH_F10_PEER_A epoch;
- AUTH_F10_PEER_A authorized action;
- AUTH_F10_PEER_A tool binding;
- AUTH_F10_PEER_A validity;
- peer tool authorization policy;
- system current epoch;
- system revoked-epoch set.

F10 therefore examines not just refusal, but bounded containment of attacker effect.

## Boundary Integrity

Before and after every compromised-agent attack:

CURRENT EPOCH = 2

REVOKED EPOCHS = {1}

The attack sequence must not weaken these governing conditions.

No malicious refusal may:

- remove epoch 1 from the revoked set;
- change current epoch;
- rewrite an authority subject;
- rewrite an authority tool binding;
- add authorized actions;
- transfer authority ownership;
- grant TOOL_F10_HIGH authority.

## Attack-Path Ordering

The frozen examination order is:

1. establish initial governing state;
2. constitute three distinct authorities;
3. snapshot peer standing and policy state;
4. execute borrowed peer-authority attack;
5. verify zero consequence and peer authority unconsumed;
6. execute stale epoch-1 authority attack;
7. verify zero consequence;
8. execute high-tool escalation attack;
9. verify zero high-tool consequence and low authority unconsumed;
10. verify governing state unchanged;
11. execute legitimate peer positive control using the exact peer authority previously misused by AGENT_X;
12. execute legitimate low-tool positive control using the exact low authority previously used in escalation;
13. preserve all results;
14. compare pre-attack and post-attack boundary state.

## Relationship to EASA-F06

EASA-F06 established bounded presenter identity binding.

F10 reuses that primitive as one containment path but adds a new system-level question:

does a malicious misuse attempt damage or alter legitimate peer standing?

A F06 PASS alone does not establish F10.

## Relationship to EASA-F07

EASA-F07 established tool-specific authority isolation.

F10 reuses that primitive against a compromised low-privilege agent and then verifies that failed escalation does not destroy the agent's legitimate lower-bound capability.

A F07 PASS alone does not establish F10.

## Relationship to EASA-F09

EASA-F09 established bounded revocation propagation and epoch invalidation.

F10 reuses revoked epoch standing as one hostile path while combining it with other attack vectors and peer-integrity checks.

A F09 PASS alone does not establish F10.

## Material New Property

F10 is not established merely because its individual refusal primitives have previously passed.

Its new property is:

COMPOSITE MALICIOUS ACTIVITY
+
MULTIPLE FAILED AUTHORITY-ABUSE PATHS
=>
NO UNAUTHORIZED CONSEQUENCE
+
NO PEER AUTHORITY CORRUPTION
+
NO GOVERNANCE WEAKENING
+
LEGITIMATE BOUNDED CAPABILITY REMAINS AVAILABLE

## Failure Conditions

EASA-F10 fails if any of the following occurs:

- AGENT_X successfully executes using AUTH_F10_PEER_A;
- borrowed peer authority is consumed by AGENT_X's refused attempt;
- borrowed peer authority is mutated by the hostile attempt;
- stale epoch-1 authority executes;
- stale epoch-1 authority causes consequence;
- TOOL_F10_HIGH executes under AUTH_F10_X_LOW_E2;
- high-tool escalation consumes AUTH_F10_X_LOW_E2 despite refusal;
- any malicious attack produces consequence;
- current epoch changes from 2;
- revoked epoch 1 is removed;
- peer authority subject binding changes;
- peer authority tool binding changes;
- peer authority action scope changes;
- peer authority validity changes;
- AGENT_A cannot subsequently execute using the exact preserved peer authority;
- AGENT_X cannot subsequently execute its exact low authority through TOOL_F10_LOW despite otherwise valid standing;
- a malicious failure confers additional authority;
- evidence cannot reconstruct pre-attack and post-attack authority state.

## Pass Conditions

EASA-F10 passes only if:

1. current epoch begins at 2;
2. epoch 1 begins revoked;
3. AUTH_F10_PEER_A begins valid and unconsumed;
4. AUTH_F10_PEER_A is bound to AGENT_A;
5. AUTH_F10_PEER_A is bound to TOOL_F10_PEER;
6. AUTH_F10_X_STALE_E1 begins valid and unconsumed;
7. AUTH_F10_X_STALE_E1 carries epoch 1;
8. AUTH_F10_X_STALE_E1 is correctly bound to AGENT_X and TOOL_F10_LOW;
9. AUTH_F10_X_LOW_E2 begins valid and unconsumed;
10. AUTH_F10_X_LOW_E2 carries current epoch 2;
11. AUTH_F10_X_LOW_E2 is bound to AGENT_X and TOOL_F10_LOW;
12. borrowed-authority attack is refused;
13. borrowed-authority refusal reason is PRESENTER_IDENTITY_MISMATCH;
14. borrowed-authority consequence delta is 0;
15. AUTH_F10_PEER_A remains unconsumed after the borrowed attack;
16. stale-authority attack is refused;
17. stale-authority refusal reason is AUTHORITY_EPOCH_REVOKED;
18. stale-authority consequence delta is 0;
19. stale authority remains unconsumed;
20. high-tool escalation is refused;
21. escalation refusal reason is TOOL_IDENTITY_MISMATCH;
22. high-tool consequence delta is 0;
23. AUTH_F10_X_LOW_E2 remains unconsumed after failed escalation;
24. total unauthorized consequence delta is 0;
25. governing current epoch remains 2;
26. revoked epoch set remains {1};
27. peer authority subject binding is unchanged;
28. peer authority tool binding is unchanged;
29. peer authority action authorization is unchanged;
30. peer authority validity remains TRUE;
31. legitimate AGENT_A use of the exact peer authority is permitted after the attacks;
32. peer positive consequence delta is 1;
33. AUTH_F10_PEER_A becomes consumed only after AGENT_A's legitimate execution;
34. legitimate AGENT_X use of the exact low authority through TOOL_F10_LOW is permitted after escalation refusal;
35. low-tool positive consequence delta is 1;
36. AUTH_F10_X_LOW_E2 becomes consumed only after its legitimate low-tool execution;
37. TOOL_F10_HIGH final consequence counter remains 0;
38. evidence preserves every attack and positive control independently;
39. pre-attack and post-attack boundary state is reconstructable;
40. malicious failures confer no new authority.

## Relevant Capability Benchmark

Primary:

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

Supporting:

EASA-CAP-01
Threat & Attack-Path Analysis

EASA-CAP-03
Identity, Authorization & Least Privilege

EASA-CAP-04
Agent Tool & Action Security

EASA-CAP-05
Replay, Freshness & Changed-State Security

EASA-CAP-07
Adversarial Verification & Falsification

EASA-CAP-08
Evidence, Audit & Forensic Reconstruction

EASA-CAP-09
Secure Change & Configuration Integrity

## Explicit Non-Claims

EASA-F10 does not establish:

- compromise detection;
- endpoint detection and response;
- malware detection;
- malware sandboxing;
- process isolation;
- operating-system containment;
- credential theft prevention;
- cryptographic identity assurance;
- prevention of an attacker who is indistinguishable from a legitimate authenticated identity;
- memory-safety guarantees;
- arbitrary-code-execution prevention;
- network segmentation;
- lateral-movement prevention across real hosts;
- production zero-trust architecture;
- cross-process containment;
- cross-host containment;
- distributed containment;
- arbitrary privilege-escalation prevention;
- data-exfiltration prevention;
- prompt-injection resistance;
- model-weight protection;
- universal compromised-agent safety;
- swarm security.

## Identity Boundary

F10 does not claim that the system can distinguish an attacker who successfully impersonates AGENT_A at an external identity layer.

The borrowed-authority path uses the explicit presenter identity AGENT_X against authority bound to AGENT_A.

External identity authentication remains outside this examination.

## Containment Boundary

For F10, containment means only that within the frozen reference-system boundary:

- unauthorized consequential execution is withheld;
- failed hostile attempts do not confer execution authority;
- failed hostile attempts do not corrupt preserved peer authority;
- failed tool escalation does not expand tool standing;
- governing epoch/revocation state is not weakened;
- legitimate bounded capability remains selectively usable.

## Evidence Discipline

The definition must be frozen before implementation execution.

The exact control and harness identities must be frozen before first observation.

The exact peer authority used in the borrowed attack must later be reused in the peer positive control.

The exact low authority used in the high-tool escalation attack must later be reused in the low-tool positive control.

No replacement authority may be substituted to manufacture successful post-attack recovery evidence.

The first observation must be preserved whether PASS or FAIL.

A failed first observation must not be repaired, rerun, remapped, or waived.

Any correction requires a prospectively constituted successor.

## Governing Rule

COMPROMISE DOES NOT CONFER AUTHORITY.

FAILED HOSTILE USE DOES NOT CORRUPT LEGITIMATE STANDING.

CONTAINMENT MUST STOP THE UNAUTHORIZED CONSEQUENCE WITHOUT SILENTLY DESTROYING VALID AUTHORITY.

Lock it.
Log it.
Prove it.