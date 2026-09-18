# EASA-F10 — Bounded Security Determination

## Examination

EASA-F10 — Compromised-Agent Containment

## Determination

PASS / CLOSED

## Claim Standing

ESTABLISHED WITHIN THE EXACT FROZEN EASA-F10 APPLICATION-LEVEL REFERENCE-SYSTEM SCOPE

## Frozen Property

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

LEGITIMATE PEER AUTHORITY
=>
REMAINS EXECUTABLE

and:

LEGITIMATE LOW-PRIVILEGE AUTHORITY
=>
REMAINS EXECUTABLE ONLY WITHIN ITS ORIGINAL AUTHORIZED BOUNDARY

## Preserved Hostile Observations

### Borrowed Peer Authority

Compromised presenter:

AGENT_X

Authority:

AUTH_F10_PEER_A

Authority owner:

AGENT_A

Observed:

VERDICT = REFUSE

REASON = PRESENTER_IDENTITY_MISMATCH

CONSEQUENCE DELTA = 0

The peer authority remained unchanged and unconsumed.

### Superseded Authority

Authority:

AUTH_F10_X_STALE_E1

Presenter:

AGENT_X

AUTHORITY EPOCH = 1

CURRENT EPOCH = 2

EPOCH 1 REVOKED = TRUE

Observed:

VERDICT = REFUSE

REASON = AUTHORITY_EPOCH_REVOKED

CONSEQUENCE DELTA = 0

The stale authority remained unchanged and unconsumed.

### High-Tool Escalation

Authority:

AUTH_F10_X_LOW_E2

Authority-bound tool:

TOOL_F10_LOW

Attempted target:

TOOL_F10_HIGH

Observed:

VERDICT = REFUSE

REASON = TOOL_IDENTITY_MISMATCH

CONSEQUENCE DELTA = 0

The low-boundary authority remained unchanged and unconsumed.

## Aggregate Hostile Consequence

Total unauthorized consequence delta:

0

TOOL_F10_HIGH final consequence counter:

0

No hostile path conferred additional execution standing.

## Governance Integrity

Before the attacks:

CURRENT EPOCH = 2

REVOKED EPOCHS = {1}

After all hostile attacks:

CURRENT EPOCH = 2

REVOKED EPOCHS = {1}

The preserved observation records that governance state remained unchanged.

## Peer Authority Integrity

The peer authority's:

- subject identity;
- authority epoch;
- tool binding;
- action scope;
- validity;
- unconsumed standing

survived the hostile borrowed-authority attempt.

The frozen harness then reused the same runtime peer authority object for the legitimate peer execution.

Observed:

AUTHORITY = AUTH_F10_PEER_A

PRESENTER = AGENT_A

VERDICT = PERMIT

REASON = AUTHORIZED

CONSEQUENCE DELTA = 1

AUTHORITY CONSUMED AFTER = TRUE

The runtime-object reuse is a property recorded by the frozen first-observation harness.

## Low-Boundary Integrity

The low authority survived the attempted escalation to TOOL_F10_HIGH without being consumed or expanded.

The frozen harness then reused the same runtime low-authority object through its originally authorized tool.

Observed:

AUTHORITY = AUTH_F10_X_LOW_E2

PRESENTER = AGENT_X

TARGET = TOOL_F10_LOW

VERDICT = PERMIT

REASON = AUTHORIZED

CONSEQUENCE DELTA = 1

AUTHORITY CONSUMED AFTER = TRUE

Accordingly, the containment behavior was selective rather than globally disabling the compromised agent's explicitly authorized bounded capability.

## Final Tool State

TOOL_F10_PEER consequence counter:

1

TOOL_F10_LOW consequence counter:

1

TOOL_F10_HIGH consequence counter:

0

The two authorized consequences occurred only through the legitimate post-attack positive controls.

No hostile attack produced consequence.

## Security Determination

Within the exact frozen EASA-F10 reference-system conditions, a compromised-agent condition did not confer additional execution authority.

Three hostile authority-abuse paths were independently refused before consequence:

1. borrowed peer authority;
2. superseded epoch authority;
3. higher-tool escalation.

Those failures did not corrupt the legitimate peer authority, did not expand the compromised agent's low-tool authority, and did not weaken the governing epoch/revocation state.

The preserved first observation further demonstrated that legitimate bounded execution remained available after the hostile attempts.

The evidence therefore supports the defined bounded EASA-F10 containment property:

COMPROMISE DID NOT CONFER AUTHORITY.

FAILED HOSTILE USE DID NOT CORRUPT LEGITIMATE STANDING.

UNAUTHORIZED CONSEQUENCE WAS WITHHELD WITHOUT SILENTLY DESTROYING VALID BOUNDED AUTHORITY.

## Material Difference From F06 / F07 / F09

F06 established presenter identity binding.

F07 established bounded tool-specific authority isolation.

F09 established bounded epoch revocation propagation.

F10 combines those primitives under a compromised-agent condition and adds a materially different containment requirement:

failed hostile attempts must not corrupt peer standing, weaken governance state, or destroy legitimate bounded authority.

F10 is therefore not merely three repeated refusal tests.

Its established property is the bounded containment of attacker effect across those abuse paths.

## Evidence Chain

EASA-F10 DEFINITION FREEZE
94c42ef

EASA-F10 IMPLEMENTATION FREEZE
8718f49

EASA-F10 FIRST OBSERVATION PRESERVATION
2e572ff

EASA-F10 BOUNDED DETERMINATION
THIS COMMIT

## Frozen Implementation Identities

DEFINITION SHA256:
D066A7AC91DBD906B05E24683A342DB4E16BC644225633C04AA7BEB2A067EEF5

CONTROL SHA256:
8EF80E0F51770B21A1737B4051B3130FCFE6053817AD50FD7D6D04E00D8DE84F

HARNESS SHA256:
D3F06FAC6887AABA547CB4BA35D1F6B38558AE44B2FDE27C4D1E6223E63450E2

IMPLEMENTATION BINDING SHA256:
AD1A1AF61C527D725A80E6543C18E107B4FCEB9C05FBAD24223E77137BFE9E4F

## Frozen First-Observation Identities

BORROWED ATTACK SHA256:
CBE109332572639CE2EA23446CE6681523788A9CD0E6DD7F5A0A8DCDCCC6A2EF

ESCALATION ATTACK SHA256:
8C1E48825AEFF0219A5E3580672A54AA13B49BC638AA0A5B7CCBAEE496DF84DF

STALE ATTACK SHA256:
671D9E3B85FB528B47BFB53743D74C38C6B75C0E34CFD39183014D976C69AD53

FIRST-OBSERVATION CONSOLE SHA256:
0A81FB5F6E4DA72124E1831E8F246A510E151FA47B8FFE656DC58534B35E07C3

LOW POSITIVE SHA256:
4FF848BEE0D46E9DE7C03F303374F209BE4830F839783BE7CE96FE2D5B62ED7D

PEER POSITIVE SHA256:
AF16053DC9474F58529F4851FBAFBF90FE1BA4FD753BC6634CBA3AD372A7F898

POST-ATTACK STATE SHA256:
05EA5F31068AE680275D416758875C8E06D8E877CE8173046791143B68973DA2

PRE-ATTACK STATE SHA256:
F91237C5E8EB7ABA1CB4FBCDA5B6CF5E5D56C4CD04105505C729C44BA545B286

SUMMARY SHA256:
9E9FEB3FCB5396E33CEF6E8405C33A96C5F6C8B815ED766CB3F5897063A29565

FIRST-OBSERVATION MANIFEST SHA256:
A6A5F59ACDF62B5DAA921CEB035DBBF53CB1879DF94E4C02B7B4D231BD078835

## Capability Relationship

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
- credential-theft prevention;
- cryptographic identity assurance;
- prevention of an attacker indistinguishable from a legitimate authenticated identity;
- memory-safety guarantees;
- arbitrary-code-execution prevention;
- network segmentation;
- real-host lateral-movement prevention;
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

The borrowed-authority test used explicit presenter AGENT_X against authority bound to AGENT_A.

F10 does not establish the ability to detect an attacker that an external identity system presents indistinguishably as AGENT_A.

## Runtime-Identity Boundary

The preserved harness recorded that the exact runtime authority objects used in the hostile borrowed-authority and tool-escalation attempts were reused in their corresponding positive controls.

This is bounded runtime observation evidence.

It is not cryptographic proof of object identity outside the frozen execution process.

## Closure Rule

The historical first F10 observation remains preserved exactly as observed.

It is not rerun, repaired, replaced, remapped, or waived.

F10 is closed only for the exact bounded property and frozen conditions documented by its evidence chain.

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.