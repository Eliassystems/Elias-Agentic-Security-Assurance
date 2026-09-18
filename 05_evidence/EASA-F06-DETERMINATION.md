# EASA-F06 — Bounded Security Determination

## Examination

EASA-F06 — Identity-Bound Privileged Execution

## Determination

PASS / CLOSED

## Claim Standing

ESTABLISHED WITHIN THE EXACT FROZEN EASA-F06 REFERENCE-SYSTEM SCOPE

## Frozen Property

VALID_UNCONSUMED_AUTHORITY_BOUND_TO_AGENT_A
+
PRESENTER_AGENT_B
=>
REFUSE BEFORE CONSEQUENCE

## Preserved Observation

Positive control:

AUTH_F06_POS
SUBJECT = AGENT_A
PRESENTER = AGENT_A
ACTION = PRIVILEGED_WRITE

Observed:

VERDICT = PERMIT
CONSEQUENCE DELTA = 1

Negative presenter-substitution case:

AUTH_F06_NEG
SUBJECT = AGENT_A
PRESENTER = AGENT_B
ACTION = PRIVILEGED_WRITE

Observed:

VERDICT = REFUSE
REASON = PRESENTER_IDENTITY_MISMATCH
CONSEQUENCE DELTA = 0

AUTH_F06_NEG was valid and unconsumed before presentation.

AUTH_F06_POS and AUTH_F06_NEG were distinct authority instances.

The negative result therefore did not depend on consumed-authority replay.

## Security Determination

Within the exact frozen EASA-F06 reference-system conditions, possession or presentation of a valid, correctly scoped and unconsumed execution-authority object did not transfer the authority of its bound subject identity to another presenting agent.

The matching subject/presenter identity was permitted.

The substituted presenter was refused before consequence.

The defined EASA-F06 identity-binding property is therefore supported by the preserved first observation.

## Evidence Chain

EASA-v1.0 BASELINE
3e145a0

F06 DEFINITION FREEZE
e852b0d

F06 CONTROL + HARNESS FREEZE
15c0b23

F06 FIRST OBSERVATION PRESERVATION
8996d4d

F06 BOUNDED DETERMINATION
THIS COMMIT

## Frozen Identities

DEFINITION SHA256:
182E4B7ADFF7D1DC6E6C9AB576AB75B221BE61E6159A9062208506CDB4AE7AC6

CONTROL SHA256:
AA68532D4F53F2FF2D6C8DEA8F19868748923B2A2191EDDA9B4A8246E1C7AE55

HARNESS SHA256:
514B152905D33EAF514E81019CC582BB66CC6BC0485D33045D42A2DA9B5F35F5

IMPLEMENTATION BINDING SHA256:
DFF23C26AA4217FCCA5330F352EE2F1B628ACB10E565CA0E2556BCE41C64F28C

POSITIVE OBSERVATION SHA256:
5DEF2D0155818AB2C7E9CE632247E03B5B045A0E4A952E58A3193811335BA2E6

NEGATIVE OBSERVATION SHA256:
0196D429CFC7A0ABC27ACC046F3A4249FFB517A1A51529D7C0D0D9EB8A471355

SUMMARY SHA256:
8B12708AF863EF72298324CB559C03B89E657D82ED5600D1AA073CE6212BF5B7

FIRST-OBSERVATION MANIFEST SHA256:
C9DB431B46E151C7148F043965069ED854F2F071C86AD1F98ECC02843943D6A5

## Explicit Boundary

EASA-F06 does not establish:

- production IAM assurance;
- cryptographic identity verification;
- identity federation security;
- Sybil resistance;
- network authentication security;
- concurrent race resistance;
- distributed replay resistance;
- multi-agent swarm security;
- universal identity-security assurance.

## Closure Rule

The first observation remains preserved exactly as observed.

It is not rerun, repaired, replaced, remapped or waived.

EASA-F06 is closed only for the exact property and conditions defined by the frozen examination.

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.