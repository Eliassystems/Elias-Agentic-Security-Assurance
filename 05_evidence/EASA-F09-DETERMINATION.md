# EASA-F09 — Bounded Security Determination

## Examination

EASA-F09 — Multi-Agent Revocation Propagation / Epoch Invalidation

## Determination

PASS / CLOSED

## Claim Standing

ESTABLISHED WITHIN THE EXACT FROZEN EASA-F09 SAME-PROCESS MULTI-NODE REFERENCE-SYSTEM SCOPE

## Frozen Property

MULTIPLE_NODES_AT_EPOCH_1
+
VALID_UNCONSUMED_EPOCH_1_AUTHORITIES
+
CENTRAL_EPOCH_ADVANCE_1_TO_2
+
REVOCATION_EVENT_FOR_EPOCH_1
+
ACKNOWLEDGED_PROPAGATION_TO_ALL_PARTICIPATING_NODES
=>
EPOCH_1_AUTHORITIES_REFUSED BEFORE CONSEQUENCE

while:

VALID_EPOCH_2_AUTHORITY
+
NODE_AT_EPOCH_2
=>
PERMIT

## Preserved Governing Change

The authoritative source began at:

CURRENT EPOCH = 1

A prospectively constituted event was applied:

REV_F09_E1_TO_E2

The authoritative state changed:

EPOCH 1 -> EPOCH 2

and:

EPOCH 1 -> REVOKED

## Propagation Standing

The same revocation-event identity was independently delivered to:

NODE_A

NODE_B

NODE_C

Each node emitted its required acknowledgement receipt:

F09-RECEIPT-NODE-A

F09-RECEIPT-NODE-B

F09-RECEIPT-NODE-C

Each receipt recorded:

PRIOR LOCAL EPOCH = 1

RESULTING LOCAL EPOCH = 2

REVOKED EPOCH = 1

APPLICATION STATUS = APPLIED

ACKNOWLEDGEMENT STATUS = ACKNOWLEDGED

All required receipts were complete before stale-authority execution attempts began.

## Stale Authority Observations

NODE_A:

AUTHORITY = AUTH_F09_A_E1

VERDICT = REFUSE

REASON = AUTHORITY_EPOCH_REVOKED

CONSEQUENCE DELTA = 0

NODE_B:

AUTHORITY = AUTH_F09_B_E1

VERDICT = REFUSE

REASON = AUTHORITY_EPOCH_REVOKED

CONSEQUENCE DELTA = 0

NODE_C:

AUTHORITY = AUTH_F09_C_E1

VERDICT = REFUSE

REASON = AUTHORITY_EPOCH_REVOKED

CONSEQUENCE DELTA = 0

All three stale authorities remained unconsumed.

Total stale consequence delta:

0

## Current-Epoch Positive Control

A fresh current authority was examined:

AUTH_F09_CURRENT_E2

AUTHORITY EPOCH = 2

Observed:

VERDICT = PERMIT

REASON = AUTHORIZED

CONSEQUENCE DELTA = 1

Accordingly, revocation did not disable the execution system globally.

It invalidated the superseded epoch while preserving valid current-epoch execution.

## Security Determination

Within the exact frozen EASA-F09 reference-system conditions, a prospectively constituted authority-epoch transition from 1 to 2 became effective across three independently represented local execution-node states through explicit propagation and acknowledgement.

After propagation was acknowledged, otherwise valid and unconsumed authorities carrying superseded epoch 1 were refused locally before consequence at NODE_A, NODE_B and NODE_C.

A fresh valid epoch-2 authority remained executable.

The preserved evidence therefore supports the defined bounded EASA-F09 property:

authority that has lost present standing did not regain execution power through stale local state after acknowledged propagation.

## Distinction From EASA-F04

EASA-F04 examined changed-state invalidation on a bounded stale-authority path.

EASA-F09 adds:

- three independently represented node states;
- one authoritative epoch transition;
- explicit revocation-event identity;
- explicit per-node propagation;
- per-node acknowledgement receipts;
- post-propagation stale-authority refusal at every node;
- a current epoch-2 positive control.

F09 therefore establishes a separate bounded propagation property rather than merely repeating F04.

## Isolation From Other Claims

The stale refusals were not caused by:

- missing authority;
- invalid authority flag;
- prior authority consumption;
- replay;
- presenter mismatch;
- unauthorized action;
- tool mismatch;
- missing human authority.

Each stale authority remained otherwise valid and correctly bound.

The decisive property was:

AUTHORITY EPOCH 1

against:

LOCAL CURRENT EPOCH 2
+
EPOCH 1 REVOKED

## Evidence Chain

EASA-F09 DEFINITION FREEZE
eefe9eb

EASA-F09 IMPLEMENTATION FREEZE
817468b

EASA-F09 FIRST OBSERVATION PRESERVATION
f42acd0

EASA-F09 BOUNDED DETERMINATION
THIS COMMIT

## Frozen Implementation Identities

DEFINITION SHA256:
1FEA80D3CC569A6C48E7E4D8F31EC69DEFFC47C6CD52E96BBAEDC32382DACF65

CONTROL SHA256:
3A8E3C8B0AAB640CD462557FF8A370E5543A5752E5EB281DFDB699E91239347A

PROPAGATION SHA256:
5873D35EC3F37BBB99FF3AFC90DFDBC59C4CB44DC18FDA6A10E685AA6EACC06F

HARNESS SHA256:
6653A418641F5C51252A03625AD0B4B8564BC11C06E3039A01D0D084F899B6EE

IMPLEMENTATION BINDING SHA256:
0F05C76F83654CFD2C081831A1D9790D5319462FBEB30A2F3B557456AC1AADD4

## Frozen First-Observation Identities

AUTHORITATIVE CHANGE SHA256:
BD180FB106A590E733451EE7A67E45E511CF7520F2DD713E6CCA56A3C4E77B87

CURRENT EPOCH-2 POSITIVE SHA256:
0C4AC19E5AB8226949B0AB1412B47150F10FBDF02C0122EA9C4320EE25BE03B8

FIRST-OBSERVATION CONSOLE SHA256:
34A56A85B5743F7C225B3DBC1899AE1538CBDEA78AB894AF439B6D172ADFD8FE

NODE-A RECEIPT SHA256:
36324C691F07585E83D271913A3692AD4D51EF758497669E58F1F0FE11E94219

NODE-B RECEIPT SHA256:
6823AB579E5DFEBE0E5E9F4CA7A57460148115E841DAC29051FDC0812B39422D

NODE-C RECEIPT SHA256:
F9A92AE4EE7B675CA9E6072D59496806594CE89013CE5C2CEAD804CAB0998056

STALE NODE-A SHA256:
7EC73E7A63447E8B6B55164B8B61B3081787DA0CA58CDE3EFF03E4381E2017D5

STALE NODE-B SHA256:
7FA51F84F5C4DCA52E217ECCAAE649EE02F6B4639138BD529C597F117B35FCCF

STALE NODE-C SHA256:
0D1DE41EA4C56C3A578D26F01018A6239E0D2153CC350674AC422A11001A9D5D

SUMMARY SHA256:
9D8319751FDB15F5A63279D1A2DB33414BAEBE389074E90D66AF75B57DF97057

FIRST-OBSERVATION MANIFEST SHA256:
A542A2ACD477ED15F2A6D2DB97F13A19F43BF8522CEB2ADBC3CF6F4B4EACD01A

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

EASA-CAP-09
Secure Change & Configuration Integrity

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

## Explicit Non-Claims

EASA-F09 does not establish:

- production distributed consensus;
- production event-bus reliability;
- guaranteed network delivery;
- bounded real-world revocation latency;
- behavior during message loss;
- behavior during network partition;
- asynchronous safety during partial propagation;
- cross-host atomic broadcast;
- Byzantine resistance;
- malicious receipt forgery resistance;
- cryptographic receipt authenticity;
- persistent database durability;
- crash-recovery propagation;
- multi-region revocation;
- unlimited node counts;
- swarm-scale revocation safety.

This determination is bounded to the exact frozen same-process multi-node reference system.

## Closure Rule

The first F09 observation remains preserved exactly as observed.

It is not rerun, repaired, completed retrospectively, replaced, remapped, or waived.

F09 is closed only for the exact bounded property and frozen conditions documented by its evidence chain.

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.