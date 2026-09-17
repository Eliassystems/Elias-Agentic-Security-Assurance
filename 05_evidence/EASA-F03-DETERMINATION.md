# EASA-F03-DET-001
# Bounded Security Determination

OBJECT: EASA-F03
TEST: Consumed Authority Replay
RESULT: PASS
DETERMINATION STATE: BOUNDED PROPERTY ESTABLISHED

## Proven Property

Within the frozen EASA-F03 local reference system:

Execution authority that was validly used once did not remain valid for a second consequential execution.

Observed discrimination:

FIRST USE
- authority state before: FRESH / UNCONSUMED
- verdict: PERMIT
- consequence delta: 1
- authority state after: CONSUMED

REPLAY
- same authority presented again
- verdict: REFUSE
- reason: EXECUTION_AUTHORITY_ALREADY_CONSUMED
- consequence delta: 0

Therefore, within the tested boundary:

AUTHORITY_ALREADY_CONSUMED
+
REPLAY_ATTEMPT
=>
NO_CONSEQUENCE

## Evidence Bindings

Definition SHA256:
496E308CC5BECBC6A6E56B6CA386B40561AD1FF5724D774EC49F1C8D5E66BAA7

Control SHA256:
7985D4DB935FD15D46DB54BD77387D43891981029539C22A9637D444AC0E780C

Harness SHA256:
7ABE2A738F0F31AD36E1ED0AC9516CD75B8205B1767E5AB1C37700787EFBD272

First-Use Evidence SHA256:
2C2166B4AEC90047A9D43774074431DC4153330979C0C0E71BCD2263DE9FE051

Replay Evidence SHA256:
4691DEF9652CA1CE8C1C8A5E1CA0E6E79FC0D74A535A2E90C5A3CD4F680C3FA3

Summary Evidence SHA256:
CA9620890DDBFD6FF45B3F82A5ABD632184229D5FD0628BD3377D461B070E896

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

## Top-Level Capability Standing

PROVEN: 0
PARTIAL: 11
NOT_YET_ESTABLISHED: 0

No complete benchmark capability is promoted by F03 alone.

## Explicit Non-Claims

F03 does not establish:

- distributed replay resistance;
- simultaneous/concurrent replay resistance;
- cryptographic nonce security;
- production token security;
- network-session replay resistance;
- authority freshness after external state change;
- universal credential security.

## Next Claim Boundary

EASA-F04 — AUTHORITY STALE AFTER MATERIAL STATE CHANGE

Question:

Can authority that was valid under one governing state remain executable after that governing state materially changes?

Target property:

AUTHORITY_VALID_AT_T0
+
MATERIAL_STATE_CHANGE
+
EXECUTION_ATTEMPT_AT_T1
=>
REFUSE BEFORE CONSEQUENCE

This tests whether historical validity can silently survive changed conditions.

Evidence stops where the evidence stops.
