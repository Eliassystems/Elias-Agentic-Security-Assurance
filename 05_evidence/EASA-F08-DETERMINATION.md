# EASA-F08 — Bounded Security Determination

## Examination

EASA-F08 — Concurrent Single-Consumption / Collision Control

## Determination

PASS / CLOSED

## Claim Standing

ESTABLISHED WITHIN THE EXACT FROZEN EASA-F08 THREAD-BASED REFERENCE-SYSTEM SCOPE

## Frozen Property

ONE_VALID_SINGLE_USE_AUTHORITY
+
TWO_EXPLICITLY_AUTHORIZED_PRESENTERS
+
SAME_AUTHORIZED_ACTION
+
SAME_AUTHORIZED_TOOL
+
SYNCHRONIZED_CONCURRENT_PRESENTATION
=>
MAXIMUM_CONSEQUENTIAL_EXECUTIONS = 1

## Preserved Observation

The F08 positive control produced:

VERDICT = PERMIT
CONSEQUENCE DELTA = 1

The fresh concurrent authority was:

AUTH_F08_CONCURRENT

Immediately before the common barrier release it was recorded as:

VALID = TRUE
CONSUMED = FALSE
SINGLE_USE = TRUE

Authorized presenters:

AGENT_A
AGENT_B

Authorized action:

CONCURRENT_PRIVILEGED_WRITE

Authorized tool:

TOOL_F08

Both workers were observed waiting at the synchronization barrier before release.

Two concurrent attempts were then made against the same shared runtime authority object.

Observed:

ATTEMPT COUNT = 2
PERMIT COUNT = 1
REFUSE COUNT = 1
CONCURRENT CONSEQUENCE DELTA = 1
FINAL SHARED AUTHORITY CONSUMED = TRUE

Historical scheduling outcome:

WINNER = AGENT_B
LOSER = AGENT_A

The winning identity is not a pass criterion.

The losing concurrent attempt was refused with:

EXECUTION_AUTHORITY_ALREADY_CONSUMED

The refused attempt produced:

CONSEQUENCE DELTA = 0

## Security Determination

Within the exact frozen EASA-F08 same-process, shared-memory, thread-based reference system, concurrent presentation by two explicitly authorized agents did not multiply one single-use execution authority into multiple consequential executions.

The one available use was claimed inside the frozen collision boundary before consequential execution.

Exactly one concurrent contender was permitted.

The other contender subsequently observed the shared authority as consumed and was refused before additional consequence.

The concurrent challenge produced exactly one consequential commit.

Accordingly, the defined EASA-F08 concurrent single-consumption property is supported by the preserved first observation.

## Distinction From EASA-F03

EASA-F03 examined sequential replay after authority had already been consumed.

EASA-F08 examined a materially different condition:

the shared authority was valid and unconsumed before synchronized release, and two authorized presenters then contended for that same available use.

Therefore F08 establishes a bounded concurrent collision property rather than merely repeating sequential replay refusal.

## Isolation From Earlier Claims

The losing F08 attempt was not refused because of:

- missing authority;
- presenter identity mismatch;
- unauthorized action scope;
- tool identity mismatch;
- changed governing state;
- missing human authority.

Both presenters were explicitly authorized.

Both requested the same authorized action.

Both targeted the same authorized tool.

The isolated reason for the losing attempt was:

EXECUTION_AUTHORITY_ALREADY_CONSUMED

## Final Tool Counter

The final tool consequence counter was 2.

This consists of:

1 consequence from the positive control

plus

1 consequence from the concurrent collision examination.

The concurrent examination itself produced consequence delta = 1.

The final counter therefore does not represent two concurrent commits.

## Evidence Chain

EASA-F08 DEFINITION FREEZE
fea89ee

EASA-F08 CONTROL + HARNESS FREEZE
08e372e

EASA-F08 FIRST CONCURRENT OBSERVATION
a3347c5

EASA-F08 BOUNDED DETERMINATION
THIS COMMIT

## Frozen Identities

DEFINITION SHA256:
A796265AF1F1CF85401AFD4AC09976A9738508DE92A3634362FB21BEE6A3DB30

CONTROL SHA256:
88763E28BCE9AAFD99D9FEA4CA010D45C6DE5CD7DF86D53FDAD12E7BFD43D642

HARNESS SHA256:
7D6E8DE29399342706101E684025D150C20B53C405C0E935CE74BF6BF766930E

IMPLEMENTATION BINDING SHA256:
8714063AC3E576F371892E330B0CBB84E09C12816C5A6BAD770DC941453155E6

POSITIVE OBSERVATION SHA256:
F048FD221A8CBDE15F4A3432322667DAB5B3D359537C6D6549966ED34F598FE6

WORKER A OBSERVATION SHA256:
098CA75CB0ECAEB9039126013F99877EE8AC8CBDB5A4C910C4FC21E85CC66EA3

WORKER B OBSERVATION SHA256:
25C0153E3497EE01DF3F0A090F586BD9C6509D94E73A3E40CD5391CA8B114B12

SUMMARY SHA256:
C7513CF968BBE24F3F417735D18564267EBF682E2DD77CCEB930D7B97C947FD8

FIRST-OBSERVATION MANIFEST SHA256:
9FB7E1C44E77EDE7E5A54E5F61753BF4D0C2C6C8244908C90A71314BE9CADED7

## Capability Relationship

Primary:

EASA-CAP-05
Replay, Freshness & Changed-State Security

Supporting:

EASA-CAP-03
Identity, Authorization & Least Privilege

EASA-CAP-04
Agent Tool & Action Security

EASA-CAP-07
Adversarial Verification & Falsification

EASA-CAP-08
Evidence, Audit & Forensic Reconstruction

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

## Explicit Non-Claims

EASA-F08 does not establish:

- distributed consensus;
- distributed locking;
- database transaction serializability;
- cross-process atomicity;
- cross-host atomicity;
- network partition safety;
- arbitrary scheduler independence;
- production message-broker exactly-once delivery;
- production payment exactly-once semantics;
- universal linearizability;
- cluster-wide single-consumption;
- multi-region single-consumption;
- crash-recovery correctness;
- unlimited concurrency;
- swarm-scale security.

The determination is bounded to the exact frozen thread-based reference-system conditions.

## Closure Rule

The historical first concurrent observation remains preserved exactly as observed.

It is not rerun, repaired, replaced, rescheduled, winner-selected, remapped, or waived.

F08 is closed only for the exact bounded property and frozen conditions documented by its evidence chain.

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.