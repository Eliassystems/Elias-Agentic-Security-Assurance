# EASA-F13 — Bounded Security Determination

## Examination

EASA-F13 — Stale Peer-State Isolation / Freshness-Bound Peer Dependency

## Determination

PASS / CLOSED

## Claim Standing

ESTABLISHED WITHIN THE EXACT FROZEN EASA-F13 SAME-PROCESS SEMANTIC PEER-STATE FRESHNESS SCOPE

## Frozen Property

VALID CURRENT EXECUTION AUTHORITY
+
STALE LOCAL PEER SNAPSHOT
+
FRESHER AUTHORITATIVE PEER STATE
+
MATERIAL PEER-STANDING CHANGE
=>
REFUSE BEFORE CONSEQUENCE

while:

VALID CURRENT EXECUTION AUTHORITY
+
CURRENT PEER SNAPSHOT
+
CURRENT ADMISSIBLE PEER STANDING
=>
PERMIT

## Initial Governing State

Peer:

PEER_B

Initial authoritative state:

PEER_B_STATE_V1

VERSION = 1

STANDING = PEER_READY

ADMISSIBLE = TRUE

AGENT_A captured a distinct local version-1 snapshot before the material change.

The preserved local snapshot remained:

PEER_B_STATE_V1

VERSION = 1

STANDING = PEER_READY

ADMISSIBLE = TRUE

through the subsequent version-2 governing state.

## Pre-Change Positive Control

Authority:

AUTH_F13_PRE

Authority source:

AUTHORITY_SOURCE_F13

Local peer version:

1

Authoritative peer version:

1

Freshness correspondence:

TRUE

Authoritative standing:

PEER_READY

Observed:

VERDICT = PERMIT

REASON = AUTHORIZED

CONSEQUENCE DELTA = 1

AUTHORITY CONSUMED AFTER = TRUE

This establishes the pre-change admissible path.

## Material Peer-State Change

The authoritative source then performed:

F13-TRANSITION-PEER-B-V1-V2

PEER_B_STATE_V1
->
PEER_B_STATE_V2

VERSION:

1
->
2

STANDING:

PEER_READY
->
PEER_WITHDRAWN

ADMISSIBILITY:

TRUE
->
FALSE

The version-1 local snapshot remained preserved separately.

## Stale Peer-State Challenge

Only after version 2 became authoritative was a new execution authority prospectively constituted:

AUTH_F13_STALE_VIEW

That authority was:

VALID = TRUE

CONSUMED = FALSE

ISSUER = AUTHORITY_SOURCE_F13

SUBJECT = AGENT_A

ACTION = F13_PEER_DEPENDENT_WRITE

TOOL = TOOL_F13

The authority contained no:

- peer version;
- peer state identity;
- peer standing;
- peer admissibility;
- authority epoch.

Therefore the stale condition was not encoded in the authority.

It resided solely in AGENT_A's local peer snapshot.

Observed execution boundary:

LOCAL STATE = PEER_B_STATE_V1

LOCAL VERSION = 1

LOCAL STANDING = PEER_READY

AUTHORITATIVE STATE = PEER_B_STATE_V2

AUTHORITATIVE VERSION = 2

AUTHORITATIVE STANDING = PEER_WITHDRAWN

FRESHNESS CORRESPONDENCE = FALSE

Observed:

VERDICT = REFUSE

REASON = PEER_STATE_STALE

CONSEQUENCE DELTA = 0

AUTHORITY CONSUMED AFTER = FALSE

The authoritative peer state remained unchanged.

The stale version-1 snapshot remained unchanged.

## Current-State Inadmissibility Challenge

After the stale refusal, AGENT_A captured a current version-2 snapshot.

A separate valid authority was prospectively constituted:

AUTH_F13_CURRENT_BLOCKED

Observed execution boundary:

LOCAL VERSION = 2

AUTHORITATIVE VERSION = 2

FRESHNESS CORRESPONDENCE = TRUE

AUTHORITATIVE STANDING = PEER_WITHDRAWN

AUTHORITATIVE ADMISSIBILITY = FALSE

Observed:

VERDICT = REFUSE

REASON = PEER_STANDING_NOT_ADMISSIBLE

CONSEQUENCE DELTA = 0

AUTHORITY CONSUMED AFTER = FALSE

This separates freshness from admissibility.

A current snapshot did not make an inadmissible peer state permissible.

## Version-2 Aggregate

Stale-path consequence delta:

0

Current-but-inadmissible consequence delta:

0

TOTAL VERSION-2 NEGATIVE CONSEQUENCE DELTA:

0

## Prospective Recovery

Only after both version-2 negative cases completed did the authoritative peer source perform:

F13-TRANSITION-PEER-B-V2-V3

PEER_B_STATE_V2
->
PEER_B_STATE_V3

VERSION:

2
->
3

STANDING:

PEER_WITHDRAWN
->
PEER_READY

ADMISSIBILITY:

FALSE
->
TRUE

Version 2 remained preserved historically.

The transition to version 3 did not rewrite version 2.

## Recovery Positive Control

A fresh version-3 snapshot was obtained.

A new authority was prospectively constituted:

AUTH_F13_RECOVERY

Observed:

LOCAL VERSION = 3

AUTHORITATIVE VERSION = 3

FRESHNESS CORRESPONDENCE = TRUE

AUTHORITATIVE STANDING = PEER_READY

AUTHORITATIVE ADMISSIBILITY = TRUE

VERDICT = PERMIT

REASON = AUTHORIZED

CONSEQUENCE DELTA = 1

AUTHORITY CONSUMED AFTER = TRUE

FINAL TOOL_F13 CONSEQUENCE COUNTER = 2

## Exact Temporal Sequence

The preserved event sequence was:

1. initial V1 state / local V1 snapshot
2. AUTH_F13_PRE issue
3. pre-change execution
4. V1 -> V2 transition
5. AUTH_F13_STALE_VIEW issue
6. stale execution attempt
7. fresh V2 snapshot capture
8. AUTH_F13_CURRENT_BLOCKED issue
9. current-but-withdrawn execution attempt
10. V2 -> V3 transition
11. fresh V3 snapshot capture
12. AUTH_F13_RECOVERY issue
13. recovery execution

The stale-view authority was therefore prospectively issued after the material peer-state change.

The V2 -> V3 recovery occurred only after both version-2 negative cases.

## Security Determination

Within the exact frozen EASA-F13 conditions, valid execution authority was not sufficient to authorize execution against stale or currently inadmissible peer-state facts.

The stale-path refusal was not caused by:

- invalid authority;
- consumed authority;
- wrong presenter;
- wrong action;
- wrong tool;
- authority issuer mismatch;
- authority epoch revocation.

The authority survived the authority-plane checks.

The refusal arose specifically because:

LOCAL PEER VERSION 1
!=
AUTHORITATIVE PEER VERSION 2.

The independently current version-2 path then refused for a materially different reason:

PEER_STANDING_NOT_ADMISSIBLE.

Finally, fresh admissible version-3 state permitted execution again.

The preserved evidence therefore supports the bounded distinction:

FRESHNESS
!=
ADMISSIBILITY

and:

VALID AUTHORITY
!=
SUFFICIENT PRESENT-TENSE ADMISSIBILITY

for actions prospectively defined as dependent on mutable peer standing.

## Material Difference From Earlier Examinations

F04 examined stale execution authority after governing-state change.

F09 examined authority-epoch revocation and bounded propagation.

F13 does neither.

AUTH_F13_STALE_VIEW was prospectively constituted after the peer-state change.

No authority epoch was required.

The stale object was the peer snapshot itself.

F13 therefore establishes a separate bounded changed-state property:

an execution authority may remain valid while a separate mutable governing dependency makes execution inadmissible.

## Evidence Chain

EASA-F13 DEFINITION FREEZE:

a51e2db

EASA-F13 IMPLEMENTATION FREEZE:

2944e61

EASA-F13 FIRST OBSERVATION PRESERVATION:

0c9309f

EASA-F13 BOUNDED DETERMINATION:

THIS COMMIT

## Frozen Implementation Identities

DEFINITION SHA256:

ABEE38294082412CAA8AD54AB8F83958A5E602E9E35A908E957C01FEFB823488

DEFINITION HASH-RECORD SHA256:

925F882AED18088302CCFA6C10D16FDA701EA122C90511DAA33FF5AF829C43BD

PEER-STATE CONTROL SHA256:

A8D568B74D6277E5845A7305E367C51726076A6F3B3A7C34F3D4FF1630E7504C

AUTHORITY SOURCE SHA256:

248730145A7695872199E3A0954EE972B75EB55302DB5E1FE2D7EAC321A7A201

EXECUTION GATE SHA256:

3FA86BD35E41A16855A5ACAB855D7868F7DE83A509186521F48764E678D5EAD2

HARNESS SHA256:

18E203BBC23DBCD3208E148AE3F60BB2B35EA899D8E818F7C6B174F863CE0E59

IMPLEMENTATION BINDING SHA256:

6309D3416B99CD36F826857B7A88E26F989B095839E90E65431E61B03EB16995

## Frozen First-Observation Identities

INITIAL STATE SHA256:

449347E5E602400A07D489EE5BBA18F970647167A81E4D726FA9D7398BA9D716

PRE-CHANGE POSITIVE SHA256:

34D68A32727D91F7C73743A5D26A35E0EEB8856DDE20FC6B97A0BC0C0CB8F936

V1 -> V2 TRANSITION SHA256:

22A4C3E136AA3B1E3DF04FA010C8C8C868E0495351BD13B4C2D5400D966F4A0C

STALE ATTEMPT SHA256:

1BE65F49BB84F535C9B6A30C507DB0B27BD78D256FF671FF60400EB147E9189C

CURRENT-BLOCKED SHA256:

588B03C524CBD84BF754BD8E2842535EB2F4B7C5C6891520AC9D656DD3D481E2

V2 -> V3 TRANSITION SHA256:

AE4C7BCF3191A3BAB9C3C644914F4B1A716962B590FD0588A338B62191479DA4

RECOVERY POSITIVE SHA256:

52CBF78A7F881F385DC30F6D06B1AD2BEADA12A3F9B8E07C8AE5752A7CB24009

SUMMARY SHA256:

3C425E9205AF1BBF5BC2A425F5F63DFB7FC9884D053A4893935937A4AEC072E9

FIRST-OBSERVATION CONSOLE SHA256:

0C7FE1A90607A786D01BEB944A56D3F571C0520B942F0D7A8DC407FCB78C0971

FIRST-OBSERVATION MANIFEST SHA256:

B2E4D14AE4AE4907EBED5865BAAB281A4881340FE6AC358B26B940CC58021FB1

## Capability Relationship

Primary:

EASA-CAP-05
Replay, Freshness & Changed-State Security

EASA-CAP-03
Identity, Authorization & Least Privilege

Supporting:

EASA-CAP-01
Threat & Attack-Path Analysis

EASA-CAP-04
Agent Tool & Action Security

EASA-CAP-07
Adversarial Verification & Falsification

EASA-CAP-08
Evidence, Audit & Forensic Reconstruction

EASA-CAP-09
Secure Change & Configuration Integrity

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

## Explicit Non-Claims

EASA-F13 does not establish:

- production cache coherence;
- distributed database consistency;
- linearizable distributed reads;
- cross-host state synchronization;
- network delivery guarantees;
- state propagation latency bounds;
- partition tolerance;
- Byzantine peer-state sources;
- malicious authoritative peer-state sources;
- cryptographic peer-state authenticity;
- signed state snapshots;
- clock synchronization;
- TTL correctness;
- wall-clock freshness;
- eventual consistency guarantees;
- distributed consensus;
- multi-region peer-state integrity;
- arbitrary peer graphs;
- unlimited agents;
- race-free concurrent state transition;
- TOCTOU elimination across arbitrary infrastructure;
- universal stale-state safety;
- swarm security.

## Same-Process Boundary

The authoritative peer-state source and AGENT_A's local snapshots were separate logical state objects in one bounded reference process.

F13 establishes semantic freshness correspondence across those objects only.

It does not establish distributed-memory or network coherence.

## Closure Rule

The historical first F13 observation remains preserved exactly as committed at:

0c9309f

It is not rerun, repaired, replaced, remapped, or waived.

The version-1 local snapshot remains historical evidence.

The version-2 PEER_WITHDRAWN state remains historical evidence.

The version-3 recovery is a prospective successor state and does not replace the prior version-2 condition.

F13 is closed only for the exact frozen property and bounded conditions documented by this evidence chain.

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.