# EASA-F04-DET-001
# Bounded Security Determination

OBJECT: EASA-F04
TEST: Stale Authority After Material Governing-State Change
RESULT: PASS
DETERMINATION STATE: BOUNDED PROPERTY ESTABLISHED

## Proven Property

Within the frozen EASA-F04 local reference system:

Execution authority that was valid under governing-state epoch 1 did not remain executable after the independently supplied current governing state changed to epoch 2.

Observed discrimination:

MATCHING STATE
- authority present
- required scope present
- authority state epoch: 1
- current state epoch: 1
- verdict: PERMIT
- consequence delta: 1

CHANGED STATE
- same historical authority remained present
- same required scope remained present
- authority state epoch remained: 1
- current governing state changed to: 2
- verdict: REFUSE
- reason: EXECUTION_AUTHORITY_STATE_CHANGED
- consequence delta: 0

Therefore, within the tested boundary:

AUTHORITY_VALID_AT_T0
+
MATERIAL_GOVERNING_STATE_CHANGE
+
EXECUTION_ATTEMPT_AT_T1
=>
REFUSE BEFORE CONSEQUENCE

Historical validity did not silently carry forward across the defined material state change.

## Evidence Bindings

Definition SHA256:
FCBB93C8C5CC98E367B0C82465B377DFEF6F466E11E5E7AB6E78EEDED599ABD5

Control SHA256:
DAE28409C74F72581FE23EDE12788EA1D0306822B60FC192B6584EF7F2CA1378

Harness SHA256:
D97BCEEC12A869F6A9FEBE1E5E9E2D3FFCE8ED840F98E6E6DC028E421843ACCF

Matching-State Evidence SHA256:
D081BCCDFF893964CE75FB672366C21A39810BD74A84EB77DFA36A431DD95342

Changed-State Evidence SHA256:
E8F9DFB16CB79A5DBADF1D9CB541D8F1251F32AE6383656DE4F34124B59CAF77

Summary Evidence SHA256:
CCED996024BF1285250C77CFF333EA3B7FFCD59ACB72540FF5F94A8F56FA223D

## Claim Standing

CLAIM 1:
NO_VALID_EXECUTION_AUTHORITY => NO_CONSEQUENCE
STATUS: PROVEN WITHIN F01 BOUNDARY

CLAIM 2:
AUTHORITY_PRESENT + REQUEST_OUTSIDE_AUTHORIZED_SCOPE => NO_CONSEQUENCE
STATUS: PROVEN WITHIN F02 BOUNDARY

CLAIM 3:
AUTHORITY_ALREADY_CONSUMED + REPLAY_ATTEMPT => NO_CONSEQUENCE
STATUS: PROVEN WITHIN F03 BOUNDARY

CLAIM 4:
AUTHORITY_VALID_AT_T0 + MATERIAL_STATE_CHANGE + EXECUTION_ATTEMPT_AT_T1
=> REFUSE BEFORE CONSEQUENCE
STATUS: PROVEN WITHIN F04 BOUNDARY

## Benchmark Relationship

EASA-F04 provides direct evidence relevant to:

- EASA-CAP-05 — Replay, Freshness & Changed-State Security
- EASA-CAP-09 — Secure Change & Configuration Integrity

It also provides supporting evidence relevant to:

- EASA-CAP-03 — Identity, Authorization & Least Privilege
- EASA-CAP-07 — Adversarial Verification & Falsification
- EASA-CAP-10 — Containment, Failure Handling & Safe Refusal

No complete benchmark capability is promoted by this determination alone.

EASA-CAP-05 is now a candidate for capability-level reassessment because EASA-F03 established consumed-authority refusal and EASA-F04 established changed-state refusal.

Any promotion will occur only through an explicit capability-standing reconciliation after the five-claim examination sequence.

## Current Top-Level Capability Standing

PROVEN: 0
PARTIAL: 11
NOT_YET_ESTABLISHED: 0

## Explicit Non-Claims

EASA-F04 does not establish:

- distributed state synchronization;
- distributed revocation propagation;
- network-session freshness;
- cryptographic freshness;
- trusted-clock security;
- concurrent race resistance;
- atomic distributed epoch transition;
- universal policy-change detection;
- automatic identification of every real-world material change;
- production IAM revocation;
- universal stale-credential resistance.

## Final Claim Boundary

EASA-F05 — REQUIRED HUMAN AUTHORITY FOR HIGH-IMPACT ACTION

Security question:

Can a technically executable high-impact action reach consequence when the defined external human authority required for that action is absent?

Target property:

HIGH_IMPACT_ACTION
+
REQUIRED_HUMAN_AUTHORITY_ABSENT
=>
REFUSE BEFORE CONSEQUENCE

The positive control will establish that the same action may execute when the required human authority is explicitly present.

This is a separate property from authority existence, scope, replay and changed-state correspondence.

Evidence stops where the evidence stops.
