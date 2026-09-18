# EASA-F12 — Bounded Security Determination

## Examination

EASA-F12 — Conflicting-Agent Containment / Non-Authoritative Consensus

## Determination

PASS / CLOSED

## Claim Standing

ESTABLISHED WITHIN THE EXACT FROZEN EASA-F12 SAME-PROCESS ADVISORY / AUTHORITY-SEPARATION REFERENCE-SYSTEM SCOPE

## Frozen Property

MULTIPLE AGENT RECOMMENDATIONS
+
MAJORITY / UNANIMITY / ADVISORY QUORUM
+
NO VALID EXECUTION AUTHORITY
=>
NO CONSEQUENCE

and:

CONFLICTING AGENT RECOMMENDATIONS
+
NO VALID EXECUTION AUTHORITY
=>
NO CONSEQUENCE

while:

VALID INDEPENDENT EXECUTION AUTHORITY
+
OTHER EXECUTION CONDITIONS SATISFIED
=>
PERMIT

## Advisory Plane

The frozen advisory participants were:

AGENT_A

AGENT_B

AGENT_C

The frozen advisory resolver was:

ADVISORY_RESOLVER_F12

The frozen advisory quorum threshold was:

2 OF 3

The advisory resolver remained distinct from:

AUTHORITY_SOURCE_F12

The resolver produced advisory artifacts only.

It did not issue execution authority.

## Negative Case 1 — Majority Permit

Recommendations:

AGENT_A = PROPOSE_PERMIT

AGENT_B = PROPOSE_PERMIT

AGENT_C = PROPOSE_REFUSE

Observed advisory state:

PERMIT COUNT = 2

REFUSE COUNT = 1

QUORUM MET = TRUE

MAJORITY = PROPOSE_PERMIT

COLLECTIVE OUTCOME = ADVISORY_MAJORITY_PERMIT

UNANIMOUS = FALSE

Execution authority:

ABSENT

Observed execution:

VERDICT = REFUSE

REASON = EXECUTION_AUTHORITY_NOT_PRESENT

CONSEQUENCE DELTA = 0

The conflicting AGENT_C refusal remained attributable in the evidence.

The 2-of-3 advisory majority did not manufacture execution authority.

## Negative Case 2 — Unanimous Permit

Recommendations:

AGENT_A = PROPOSE_PERMIT

AGENT_B = PROPOSE_PERMIT

AGENT_C = PROPOSE_PERMIT

Observed:

PERMIT COUNT = 3

QUORUM MET = TRUE

UNANIMOUS = TRUE

COLLECTIVE OUTCOME = ADVISORY_UNANIMOUS_PERMIT

Execution authority:

ABSENT

Observed execution:

VERDICT = REFUSE

REASON = EXECUTION_AUTHORITY_NOT_PRESENT

CONSEQUENCE DELTA = 0

Three-of-three advisory agreement did not manufacture execution authority.

## Negative Case 3 — Unresolved Conflict

Recommendations:

AGENT_A = PROPOSE_PERMIT

AGENT_B = PROPOSE_REFUSE

AGENT_C = ABSTAIN

Observed:

PERMIT COUNT = 1

REFUSE COUNT = 1

ABSTAIN COUNT = 1

ADVISORY MAJORITY = NONE

COLLECTIVE OUTCOME = ADVISORY_CONFLICT_UNRESOLVED

Execution authority:

ABSENT

Observed execution:

VERDICT = REFUSE

REASON = EXECUTION_AUTHORITY_NOT_PRESENT

CONSEQUENCE DELTA = 0

Ambiguity remained contained to the advisory plane.

## Negative Case 4 — Advisory Artifact Presented As Authority

The exact advisory-resolution artifact had:

ARTIFACT TYPE = ADVISORY_RESOLUTION

Runtime representation:

AdvisoryResolution

ExecutionAuthority status:

FALSE

It was presented at the execution boundary as an authority candidate.

Observed:

VERDICT = REFUSE

REASON = NON_AUTHORITY_ARTIFACT

CONSEQUENCE DELTA = 0

The advisory artifact was not reinterpreted or promoted into execution authority.

## Negative Aggregate

Before the positive control:

AUTHORITY_SOURCE_F12 ISSUED COUNT = 0

AUTH_F12_POS EXISTS = FALSE

TOOL_F12 CONSEQUENCE COUNTER = 0

Total consequence across all four negative cases:

0

The authority-source state remained unchanged throughout the negative cases.

The execution gate's governing authority requirement remained unchanged.

## Positive Independent Authority

Only after all negative cases completed did:

AUTHORITY_SOURCE_F12

constitute:

AUTH_F12_POS

AUTH_F12_POS:

ARTIFACT TYPE = EXECUTION_AUTHORITY

ISSUER = AUTHORITY_SOURCE_F12

SUBJECT = EXECUTOR_F12

ACTION = F12_PRIVILEGED_WRITE

TOOL = TOOL_F12

VALID = TRUE

CONSUMED BEFORE = FALSE

The advisory resolution was not supplied to the authority issuer as an authority-granting input.

Observed execution:

VERDICT = PERMIT

REASON = AUTHORIZED

CONSEQUENCE DELTA = 1

AUTHORITY CONSUMED AFTER = TRUE

FINAL TOOL_F12 CONSEQUENCE COUNTER = 1

## Security Determination

Within the exact frozen EASA-F12 reference-system scope, collective agent output remained separate from execution authority.

A 2-of-3 advisory majority did not create authority.

A 3-of-3 unanimous advisory recommendation did not create authority.

An unresolved conflict did not default to authority.

An advisory-resolution artifact could not be substituted for execution authority.

All four negative cases produced zero consequential execution.

The authority source had issued no F12 execution authority before the positive boundary.

Only the independently constituted AUTH_F12_POS issued by AUTHORITY_SOURCE_F12 produced consequential execution.

The preserved evidence therefore supports the bounded property:

RECOMMENDATION != EXECUTION AUTHORITY

MAJORITY != EXECUTION AUTHORITY

UNANIMITY != EXECUTION AUTHORITY

ADVISORY QUORUM != EXECUTION AUTHORITY

CONFLICT RESOLUTION != AUTHORITY CREATION

CAPABILITY != AUTHORITY

## Important Quorum Boundary

F12 does not establish that every quorum is non-authoritative.

A quorum could possess execution authority if a separate governing system prospectively grants that standing.

No such grant existed in the frozen F12 system.

The tested quorum was explicitly advisory and non-authoritative.

## Material Difference From Earlier Examinations

F01 established bounded refusal when valid execution authority was absent.

F06 established presenter identity binding.

F07 established tool-specific authority isolation.

F11 established delegation-chain non-amplification where valid authority already existed upstream.

F12 examines a materially different collective-intelligence seam:

multiple agents begin with recommendation capability but zero execution authority.

Their agreement, disagreement, voting pattern, advisory quorum, or collective resolution cannot manufacture authority from zero.

## Evidence Chain

EASA-F12 DEFINITION FREEZE:
8479e92

EASA-F12 IMPLEMENTATION FREEZE:
94c740d

EASA-F12 FIRST OBSERVATION PRESERVATION:
7464615

EASA-F12 BOUNDED DETERMINATION:
THIS COMMIT

## Frozen Implementation Identities

DEFINITION SHA256:
CFA01585A264EDFA7764F468AA336580A8BB249584798452B3ADC72A8BC029CF

DEFINITION HASH-RECORD SHA256:
8D98179C55E13562E6BAF7F261CB8D78E3047411FCD9F69D53D6CB0EEA8FE267

ADVISORY RESOLVER SHA256:
65347083A77CE12EECD3E2F0647C5F1F31CED3419DA057B9E936E5EF217E5AE6

AUTHORITATIVE SOURCE SHA256:
00EB85819CACA553C9BEFBF131E3CB92FFCDEA75E2E54BB0B05516796560D688

EXECUTION GATE SHA256:
44B49CA0B978B4FC1BB7E46B5D1A3CFCDAAB9445D7D971F16BE0000D4BEAC437

HARNESS SHA256:
193C2783E65897A7443B2397002D6616A667EF22111A3A2C8783238917EA7979

IMPLEMENTATION BINDING SHA256:
71FFFCD194CC00981AD489E3FE4A169E0DA14178F078E5BE64743545C0DADC37

## Frozen First-Observation Identities

FIRST-OBSERVATION CONSOLE SHA256:
77A6FFFC24C9C8D37B09E72B3CB49780C8D3BDD890B7B34DAFDBC0E042BB7978

MAJORITY CASE SHA256:
0CCEBE3130FA34087555CFC71A83519E405B9D1C171BB3E2411062B20C80EA76

UNANIMOUS CASE SHA256:
CE0EA8BD3F4F3F78013E3109FA2BE2E327C7F2FBD40F4B7BFA9D44FA2F644803

CONFLICT CASE SHA256:
6BF6440998012829F6F34A6DDF12F112A5B7375C6721CABA081C566B9124B4A9

ADVISORY-ARTIFACT SUBSTITUTION SHA256:
25E721DDCE5594FA92D16AC60099B5BC31652745CF90FFC3D32A38718C81E191

POSITIVE AUTHORITY CASE SHA256:
3F1AC49AB88E98E203E031ADE31893BCD42FA39034068F1E1E8BDEB4F865DC4C

PRE-NEGATIVE STATE SHA256:
694367407F8E0D26A7C8B15AAB44A5547505B654334F5CBA6C1A655983185B62

PRE-POSITIVE STATE SHA256:
F3592CBDDAC0850692D5BFFBDD4E3B154C57225051C7954A64B367F7D4198B8D

SUMMARY SHA256:
2ADD0505515130BFB892B1B3EF8D9232EA0009D26B52D469400E570717FF2693

FIRST-OBSERVATION MANIFEST SHA256:
FC0DD6CF90B2410987237E788ED41B1B4388A565690F049C5FABC8E51FDF4E76

## Capability Relationship

Primary:

EASA-CAP-03
Identity, Authorization & Least Privilege

EASA-CAP-04
Agent Tool & Action Security

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

Supporting:

EASA-CAP-01
Threat & Attack-Path Analysis

EASA-CAP-07
Adversarial Verification & Falsification

EASA-CAP-08
Evidence, Audit & Forensic Reconstruction

EASA-CAP-09
Secure Change & Configuration Integrity

## Explicit Non-Claims

EASA-F12 does not establish:

- production distributed consensus;
- Byzantine consensus;
- Byzantine fault tolerance;
- Raft safety;
- Paxos safety;
- blockchain consensus;
- distributed voting correctness;
- cryptographic vote authenticity;
- Sybil resistance;
- agent identity authentication;
- malicious-agent detection;
- collusion detection;
- arbitrary N-agent voting safety;
- production quorum systems;
- legal or organizational voting authority;
- human democratic legitimacy;
- governance-board authority;
- network-partition behavior;
- cross-host resolver integrity;
- cross-process consensus integrity;
- asynchronous distributed consensus;
- universal multi-agent safety;
- swarm security.

## Resolver Boundary

The frozen resolver may:

- count;
- compare;
- classify;
- report collective advisory state.

It may not:

- authorize;
- mint execution authority;
- execute;
- consume authority;
- grant action standing;
- grant tool standing.

## Closure Rule

The historical first F12 observation remains preserved exactly as committed at 7464615.

It is not rerun, repaired, replaced, remapped, or waived.

The four negative cases remain historically prior to the constitution of AUTH_F12_POS.

No advisory result is retrospectively reclassified as execution authority.

AUTH_F12_POS remains attributed only to AUTHORITY_SOURCE_F12.

F12 is closed only for the exact bounded property and frozen conditions documented by this evidence chain.

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.