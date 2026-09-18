# EASA-F11 — Bounded Security Determination

## Examination

EASA-F11 — Delegation-Chain Non-Amplification

## Determination

PASS / CLOSED

## Claim Standing

ESTABLISHED WITHIN THE EXACT FROZEN EASA-F11 SAME-PROCESS DELEGATION AND SHARED-LINEAGE REFERENCE-SYSTEM SCOPE

## Frozen Property

DELEGATION
!=
AUTHORITY CREATION

VALID DESCENDANTS MUST NOT AMPLIFY:

- action scope;
- tool scope;
- local consequence ceiling;
- delegation depth;
- shared lineage consequence budget.

## Valid Delegation Chain

The frozen first observation prospectively created:

AUTH_F11_A_ROOT
->
AUTH_F11_B
->
AUTH_F11_C

Observed valid delegation:

A -> B

VERDICT = PERMIT

REASON = DELEGATION_AUTHORIZED

AUTH_F11_B:

SUBJECT = AGENT_B

ACTIONS = {F11_STANDARD_WRITE}

TOOLS = {TOOL_F11_STANDARD}

LOCAL CONSEQUENCE CEILING = 2

DELEGATION DEPTH = 1

LINEAGE = LINEAGE_F11_001

Observed valid delegation:

B -> C

VERDICT = PERMIT

REASON = DELEGATION_AUTHORIZED

AUTH_F11_C:

SUBJECT = AGENT_C

ACTIONS = {F11_STANDARD_WRITE}

TOOLS = {TOOL_F11_STANDARD}

LOCAL CONSEQUENCE CEILING = 1

DELEGATION DEPTH = 0

LINEAGE = LINEAGE_F11_001

## Rejected Amplification Paths

### Action-Scope Amplification

B attempted to delegate authority containing F11_ADMIN_WRITE.

Observed:

VERDICT = REFUSE

REASON = DELEGATION_ACTION_SCOPE_AMPLIFICATION

CHILD AUTHORITY ISSUED = FALSE

PARENT AUTHORITY UNCHANGED = TRUE

### Tool-Scope Amplification

B attempted to delegate TOOL_F11_HIGH.

Observed:

VERDICT = REFUSE

REASON = DELEGATION_TOOL_SCOPE_AMPLIFICATION

CHILD AUTHORITY ISSUED = FALSE

PARENT AUTHORITY UNCHANGED = TRUE

### Local Consequence Ceiling Amplification

B attempted to issue a child local ceiling of 3 while B's own local ceiling was 2.

Observed:

VERDICT = REFUSE

REASON = DELEGATION_CONSEQUENCE_CEILING_AMPLIFICATION

CHILD AUTHORITY ISSUED = FALSE

PARENT AUTHORITY UNCHANGED = TRUE

### Delegation-Depth Amplification

B had delegation depth 1 and attempted to issue a child retaining depth 1.

Observed:

VERDICT = REFUSE

REASON = DELEGATION_DEPTH_AMPLIFICATION

CHILD AUTHORITY ISSUED = FALSE

PARENT AUTHORITY UNCHANGED = TRUE

### Unauthorized Further Delegation

C held delegation depth 0 and attempted C -> D.

Observed:

VERDICT = REFUSE

REASON = DELEGATION_AUTHORITY_NOT_PRESENT

CHILD AUTHORITY ISSUED = FALSE

PARENT AUTHORITY UNCHANGED = TRUE

## Shared Lineage Standing

The frozen harness recorded that A, B and C referenced the same bounded runtime lineage state:

LINEAGE_F11_001

LINEAGE CONSEQUENCE CEILING = 4

Delegation did not create independent consequence budgets for B or C.

The runtime-object identity statement is bounded to this frozen same-process observation.

It is not cryptographic or cross-process proof.

## Lineage Execution Observation

The preserved execution sequence was:

1. AGENT_C / AUTH_F11_C
2. AGENT_B / AUTH_F11_B
3. AGENT_B / AUTH_F11_B
4. AGENT_A / AUTH_F11_A_ROOT

Each execution used:

ACTION = F11_STANDARD_WRITE

TOOL = TOOL_F11_STANDARD

Observed:

C EXECUTION 1 = PERMIT

B EXECUTION 1 = PERMIT

B EXECUTION 2 = PERMIT

A EXECUTION 1 = PERMIT

Final local consequence counts:

A = 1

B = 2

C = 1

Final shared lineage consequence count:

4

Final standard-tool consequence counter:

4

Final high-tool consequence counter:

0

## Lineage-Ceiling Challenge

After four shared lineage consequences, AGENT_A attempted one additional otherwise-authorized execution.

At that point:

A LOCAL CONSEQUENCE COUNT = 1

A LOCAL CONSEQUENCE CEILING = 4

LINEAGE CONSEQUENCE COUNT = 4

LINEAGE CONSEQUENCE CEILING = 4

Therefore A still possessed unused local consequence capacity.

Observed:

VERDICT = REFUSE

REASON = LINEAGE_CONSEQUENCE_CEILING_EXHAUSTED

CONSEQUENCE DELTA = 0

FINAL LINEAGE CONSEQUENCE COUNT = 4

This isolates the shared lineage ceiling from A's own local ceiling.

## Security Determination

Within the exact frozen EASA-F11 reference-system conditions, delegation attenuated authority rather than amplifying it.

Valid child authorities were prospectively created through the frozen delegation gate.

The valid chain narrowed authority from A to B and from B to C.

Attempts to amplify:

- action scope;
- tool scope;
- local consequence ceiling;
- delegation depth;
- further delegation standing

were refused without issuing a child authority and without mutating the parent authority.

The valid A -> B -> C chain remained bound to one shared lineage consequence budget.

Creating descendants did not multiply the root consequence ceiling.

After four total permitted consequences across C, B, B and A, a fifth otherwise-authorized root execution was refused specifically because the shared lineage ceiling was exhausted while A's local ceiling remained unexhausted.

The preserved evidence therefore supports the bounded F11 property:

DELEGATION MAY ATTENUATE AUTHORITY.

DELEGATION MAY NOT AMPLIFY AUTHORITY.

DESCENDANTS DID NOT RECEIVE MORE POWER THAN THEIR IMMEDIATE PARENT POSSESSED.

DELEGATION DID NOT MULTIPLY THE ROOT CONSEQUENCE BUDGET.

## Material Difference From Earlier Examinations

F06 examined presenter identity binding.

F07 examined tool-specific authority isolation.

F08 examined concurrent single-consumption.

F09 examined multi-node revocation / epoch invalidation.

F10 examined compromised-agent containment.

F11 adds a materially different property:

authority can be prospectively transmitted through a bounded delegation chain without silently increasing the authority or consequence budget available to descendants.

## Evidence Chain

EASA-F11 DEFINITION FREEZE:
c2992a8

EASA-F11 IMPLEMENTATION FREEZE:
fb64d2e

EASA-F11 FIRST OBSERVATION PRESERVATION:
efc4d24

EASA-F11 BOUNDED DETERMINATION:
THIS COMMIT

## Frozen Implementation Identities

DEFINITION SHA256:
35874955B23A3CDCC0D3056C8D9D693A79ADCE790E4831F601A67E3C26E901BF

DEFINITION HASH-RECORD SHA256:
B9361A5D3ADCC433AAAB377B272C6C8A99D5E26F5FE9A9607A9ED486846A1A3A

DELEGATION CONTROL SHA256:
5AEF7B452C1F9039449DF627780DDF1AD21AC4C8EE64DE5AADC5B77C661FE701

LINEAGE EXECUTION CONTROL SHA256:
E1B508DB7A421D40029528329E1D8D9B2BD19C84164DB16A2E3115AEB41BC6BC

HARNESS SHA256:
B0A3BF8A7BF777566F45C47231B87D55EB05DEBFD6CF961F5B288E18268CD1F7

IMPLEMENTATION BINDING SHA256:
33730242B5029ABFDF94B0473958492388F79E4908696F7EFD7504DA4AE31743

## Frozen First-Observation Identities

ROOT STATE SHA256:
ED799558AAB89E200FAE9E8A3759E939C72763AE32E8540D9FB867C7AF6B956C

A -> B DELEGATION SHA256:
00A1215AEAE37BCB7FE4F3A00FF9339C31C259A78474214E883DC7873B462349

ACTION-SCOPE ATTACK SHA256:
8D6067B4260A4B2A3A0406ACFEC4CA123FF43841C268BCA7D9A1F3DEA022CD9B

TOOL-SCOPE ATTACK SHA256:
223612DCBD0A405F5B61CB341CF61F09D0FD557E0DB060F97C08D553751E1AEC

LOCAL-CEILING ATTACK SHA256:
BFCE1D9EF218AD28C550C4D04F81FAB50CC9F307A34B0F7E1CB57AFA3BAB9B85

DELEGATION-DEPTH ATTACK SHA256:
5D3FE772DADC4201DF6B2F1CF836B4EC4CB4303EAEA17A45116D245D99ADC112

B -> C DELEGATION SHA256:
8D92F210973F82BEF8C2AA20E236BA4464EAE5F04123804EE91E534CEF6236C6

C -> D ATTACK SHA256:
3CC4015CEA0BFBD5429A1D6DEC4594CC950D51F528AAADC8437829633707C8DC

LINEAGE EXECUTION SHA256:
3BAE70ECCC8C58420D33872EE073F9279DC71D1D0B9590CB68F6BB2062B99E37

SUMMARY SHA256:
2FD216AD2549EF7C0BD8C88ECF1B758038D617434DEDF4C4C52FA84C79493069

FIRST-OBSERVATION CONSOLE SHA256:
50A42F60E0152735379C171B46078E59BE6406D5D9E2C54D5E11125188FDC26A

FIRST-OBSERVATION MANIFEST SHA256:
9DA2AE6F0D2685C9221B1BD1A89456FF130144C563C21CE24F99A558CCE723A4

## Capability Relationship

Primary:

EASA-CAP-03
Identity, Authorization & Least Privilege

EASA-CAP-04
Agent Tool & Action Security

Supporting:

EASA-CAP-01
Threat & Attack-Path Analysis

EASA-CAP-05
Replay, Freshness & Changed-State Security

EASA-CAP-07
Adversarial Verification & Falsification

EASA-CAP-08
Evidence, Audit & Forensic Reconstruction

EASA-CAP-09
Secure Change & Configuration Integrity

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

## Explicit Non-Claims

EASA-F11 does not establish:

- cryptographically signed delegation;
- production PKI delegation;
- cross-process delegation;
- cross-host delegation;
- distributed capability systems;
- delegation across network partitions;
- Byzantine delegate resistance;
- malicious-code isolation;
- external identity authentication;
- recursive arbitrary-depth delegation;
- unlimited delegation graphs;
- delegation-cycle detection;
- concurrent delegation race safety;
- crash-recovery delegation durability;
- database transaction isolation;
- production distributed budget accounting;
- multi-region lineage accounting;
- unlimited consequence scale;
- universal capability-system security.

## Lineage Boundary

The shared lineage consequence ceiling was observed through one bounded same-process lineage state shared by the valid descendants.

F11 does not establish atomic, durable, or available lineage accounting across processes, hosts, networks, databases, regions, or partitions.

## Closure Rule

The historical first F11 observation remains preserved exactly as committed at efc4d24.

It is not rerun, repaired, replaced, remapped, or waived.

AUTH_F11_B and AUTH_F11_C remain the authorities prospectively created during the frozen first observation.

The historical shared lineage state is not replaced with fresh lineage state.

F11 is closed only for the exact bounded property and frozen conditions documented by this evidence chain.

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.