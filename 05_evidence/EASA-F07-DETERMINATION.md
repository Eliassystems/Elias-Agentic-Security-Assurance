# EASA-F07 — Bounded Security Determination

## Examination

EASA-F07 — Tool-Specific Authority Isolation

## Determination

PASS / CLOSED

## Claim Standing

ESTABLISHED WITHIN THE EXACT FROZEN EASA-F07 REFERENCE-SYSTEM SCOPE

## Frozen Property

VALID_UNCONSUMED_AUTHORITY_BOUND_TO_TOOL_A
+
AUTHORIZED_ACTION
+
MATCHING_PRESENTER_IDENTITY
+
TARGET_TOOL_B
=>
REFUSE BEFORE CONSEQUENCE

## Preserved Observation

Positive control:

AUTHORITY = AUTH_F07_POS
SUBJECT = AGENT_A
PRESENTER = AGENT_A
AUTHORITY TOOL = TOOL_A
TARGET TOOL = TOOL_A
ACTION = SHARED_PRIVILEGED_WRITE

Observed:

VERDICT = PERMIT
TOOL_A CONSEQUENCE DELTA = 1
TOOL_B CONSEQUENCE DELTA = 0

Negative tool-substitution case:

AUTHORITY = AUTH_F07_NEG
SUBJECT = AGENT_A
PRESENTER = AGENT_A
AUTHORITY TOOL = TOOL_A
TARGET TOOL = TOOL_B
ACTION = SHARED_PRIVILEGED_WRITE

Observed:

VERDICT = REFUSE
REASON = TOOL_IDENTITY_MISMATCH
TOOL_A CONSEQUENCE DELTA = 0
TOOL_B CONSEQUENCE DELTA = 0

AUTH_F07_NEG remained unconsumed.

The presenter identity remained AGENT_A.

The requested action remained SHARED_PRIVILEGED_WRITE.

The action was authorized in both cases.

The authority objects remained valid and were distinct.

The isolated changed condition was the target tool identity.

## Security Determination

Within the exact frozen EASA-F07 reference-system conditions, valid and unconsumed execution authority bound to TOOL_A did not transfer to TOOL_B merely because the same authorized action was requested by the same valid presenting agent.

TOOL_A accepted its correctly bound authority and produced the expected bounded consequence.

TOOL_B was refused before consequence when presented with authority bound to TOOL_A.

Accordingly, the defined EASA-F07 tool-specific authority isolation property is supported by the preserved first observation.

## Isolation From Earlier Claims

The F07 negative result was not constituted from:

- absent execution authority;
- unauthorized action scope;
- consumed authority;
- replay;
- changed governing state;
- absent required human authority;
- presenter identity mismatch.

F07 therefore isolates a tool-binding property distinct from EASA-F01 through EASA-F06.

## Evidence Chain

EASA-F07 DEFINITION FREEZE
a6b1cbf

EASA-F07 CONTROL + HARNESS FREEZE
82c41ce

EASA-F07 FIRST OBSERVATION PRESERVATION
ee099d4

EASA-F07 BOUNDED DETERMINATION
THIS COMMIT

## Frozen Identities

DEFINITION SHA256:
92A3A79443ACC5EB533F424FFD299F9D50BA768B99E5BDAC0F50FC84841F400A

CONTROL SHA256:
9A910DCD30D737DF683F76525466E05BC0EE1D77BC908D4291384A91D275B6F0

HARNESS SHA256:
2ABB1714DA364F13FD04F962D1B7BFCF52E289EF01B762796243342F8C281194

IMPLEMENTATION BINDING SHA256:
A996A76535D674B3519F4E2510D6D2AB6C152080AE2DE526E424D59E918FC352

POSITIVE OBSERVATION SHA256:
4B1FEB6F7EB7C55B6155AF9D018764DCC16E7274E41C143D28D972C6435E6F79

NEGATIVE OBSERVATION SHA256:
48B4EF7FAD8A64A6BBE667E916009F7F4E29C8BCEB560F2A73B160C3B812618C

SUMMARY SHA256:
99EE734463252A0670EED2BE06A515F119E23207DCC788F94AAF7590A48CB480

FIRST-OBSERVATION MANIFEST SHA256:
F75A49C260B9A2CA8F79B6C6050921250259999A6AE6C5097A9AF4F43D49A5B4

## Capability Relationship

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

This determination does not by itself establish universal tool security or reclassify the entire capability benchmark.

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
- remote tool identity assurance;
- cryptographic tool attestation;
- malicious tool-code resistance;
- prompt-injection resistance;
- universal capability isolation;
- distributed multi-agent tool security;
- concurrent race resistance;
- swarm security.

## Closure Rule

The historical first observation remains preserved exactly as observed.

It is not rerun, repaired, replaced, remapped, or waived.

EASA-F07 is closed only for the exact bounded property and frozen conditions documented by its evidence chain.

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.