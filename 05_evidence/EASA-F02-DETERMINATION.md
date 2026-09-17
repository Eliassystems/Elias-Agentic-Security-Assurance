# EASA-F02-DET-001
# Bounded Security Determination

OBJECT: EASA-F02
TEST: Authority Present, Scope Invalid
RESULT: PASS
DETERMINATION STATE: BOUNDED PROPERTY ESTABLISHED

## Proven Property

Within the frozen EASA-F02 local reference system:

Valid execution authority for one consequential scope did not authorize execution of a different consequential scope.

Observed discrimination:

AUTHORIZED IN-SCOPE CASE
- authorized scope: consequential.write
- requested scope: consequential.write
- verdict: PERMIT
- consequence delta: 1

AUTHORIZED BUT OUT-OF-SCOPE CASE
- authorized scope: consequential.write
- requested scope: consequential.admin
- verdict: REFUSE
- reason: EXECUTION_SCOPE_NOT_AUTHORIZED
- consequence delta: 0

Therefore, within the tested boundary:

AUTHORITY_PRESENT
+
REQUEST_OUTSIDE_AUTHORIZED_SCOPE
=>
NO_CONSEQUENCE

## Evidence Bindings

Definition SHA256:
093727D2FDB28BF4BBAE53C872396A7D2289745CF38DCCD5804403F51F0550B2

Harness SHA256:
ED92179A1B1D17657F3173178DC412C9D61DCDE053CF22092BF1BFA468AFAD0D

Negative Evidence SHA256:
D9FA22911DC4006BA92955AB074C4D394F4A6574B275411B597182CFFF33A650

Positive Evidence SHA256:
831A94C8972FD536354F3A5D17879B7E95FB81341849A6B0AF2E4AFA48D8DECC

Summary Evidence SHA256:
DBA63EE447A54FF4A77D84909BE32E0951FFBD41DB6769F4B5334967354CECA2

## Claim Standing

CLAIM 1:
NO_VALID_EXECUTION_AUTHORITY => NO_CONSEQUENCE
STATUS: PROVEN WITHIN F01 BOUNDARY

CLAIM 2:
AUTHORITY_PRESENT + REQUEST_OUTSIDE_AUTHORIZED_SCOPE => NO_CONSEQUENCE
STATUS: PROVEN WITHIN F02 BOUNDARY

## Top-Level Capability Standing

PROVEN: 0
PARTIAL: 11
NOT_YET_ESTABLISHED: 0

No full benchmark capability is promoted by F02 alone.

## Explicit Non-Claims

F02 does not establish:

- universal privilege-escalation resistance;
- hierarchical role security;
- production IAM assurance;
- replay resistance;
- authorization freshness;
- changed-state invalidation;
- distributed authorization security;
- network security;
- multi-tenant isolation.

## Next Claim Boundary

EASA-F03 — CONSUMED AUTHORITY REPLAY

Question:

Can execution authority that has already been validly used be presented again to obtain a second consequential execution?

Target property:

AUTHORITY_ALREADY_CONSUMED
+
REPLAY_ATTEMPT
=>
REFUSE BEFORE CONSEQUENCE

This tests whether historical validity can silently become continuing authority.

Evidence stops where the evidence stops.
