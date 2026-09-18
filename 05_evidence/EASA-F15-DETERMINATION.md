# EASA-F15 — Final Bounded Determination

## Examination

EASA-F15

Resolver / Partition Safe Degradation

## Final Determination

PASS

CLOSED

## Bounded Claim

ESTABLISHED WITHIN THE EXACT FROZEN EASA-F15
SINGLE-PROCESS, TWO-RESOLVER, SIMULATED-PARTITION
REFERENCE-SYSTEM SCOPE.

Within that scope, preserved evidence established that
a valid execution authority did not produce consequence when
required current resolution was unavailable, conflicting, or
current-but-inadmissible.

Historical cached admissibility did not substitute for current
resolution.

A permissive conflicting resolver view did not manufacture
execution standing.

Resolver agreement on an inadmissible current state did not
manufacture execution standing.

Execution recovered prospectively only after the authoritative
state transitioned to R3 READY / ADMISSIBLE TRUE and both frozen
resolver replicas corresponded to that current state.

## Frozen Provenance

Definition commit:

8d86468

Definition SHA-256:

A22DCBE1DF2DC870673C25168514D80EF920D4579854DE8783BBF4CD318BF666

Definition hash-record SHA-256:

8FB6BAD68B5235DC040E0AEE3F2F6686760C7E3E7C1596F3F735F894C941FE04

Implementation commit:

4f7c5ae

Resolver control SHA-256:

5E0F255B3452BE159ED7C0B15C5E0633D76F6CE111546E0FC50B26A9E3E500D2

Execution control SHA-256:

292A6F13957CC7485C3E52D4EE1B1A6B2DAC6ACD0CD176FE9E0EF7882D6CA9F3

Harness SHA-256:

4D6936AE1D05C290616252B078F908F46CD357AF0E003FDFFA98082A8E1FD13C

Implementation binding SHA-256:

BC0859905F0DF80592834D1579C5AC4B6F321A47123B1FA8D6C4440CC2E79666

First-observation preservation commit:

c04ab10

First-observation manifest SHA-256:

7E39867D7BC7EE21F88831AC2409091CC98433C19EA8A78B8D00F8FFD838F78A

Harness rerun:

NO

Retrospective repair:

NO

## Preserved First Observation

Process exit code:

0

Observed result:

PASS

Observed claim state:

OBSERVATION_SUPPORTS_DEFINED_PROPERTY

Execution attempts:

5

Permits:

2

Refusals:

3

Unauthorized consequence total:

0

Aggregate authorized consequence delta:

2

Final TOOL_F15 consequence counter:

2

Runtime evidence files required:

13

Runtime evidence files present:

13

Runtime evidence files missing:

0

## Positive Control

AUTH_F15-BASELINE:

PERMIT

Reason:

AUTHORIZED

Consequence delta:

1

Authority consumed after permit:

TRUE

## Partition / Unavailable Resolution

AUTH_F15-PARTITION:

REFUSE

Reason:

CURRENT_RESOLUTION_UNAVAILABLE

Historical cached state:

R1 READY / ADMISSIBLE TRUE

Consequence delta:

0

Authority consumed after refusal:

FALSE

Determination:

Historical admissibility did not substitute for unavailable
current resolution.

## Conflicting Resolver Views

RESOLVER_F15_A:

R1 READY / ADMISSIBLE TRUE

RESOLVER_F15_B:

R2 WITHDRAWN / ADMISSIBLE FALSE

AUTH_F15-CONFLICT:

REFUSE

Reason:

RESOLVER_STATE_CONFLICT

Consequence delta:

0

Authority consumed after refusal:

FALSE

Determination:

No conflicting resolver view created execution standing and the
permissive view was not selected merely because it permitted.

## Current Consistent But Inadmissible

Both resolvers:

R2 WITHDRAWN / ADMISSIBLE FALSE

AUTH_F15-CURRENT-BLOCKED:

REFUSE

Reason:

RESOLVED_STATE_NOT_ADMISSIBLE

Consequence delta:

0

Authority consumed after refusal:

FALSE

Determination:

CONSISTENCY != ADMISSIBILITY.

Resolver agreement alone did not create execution standing.

## Prospective Recovery

Authoritative transition:

R2 WITHDRAWN / FALSE
->
R3 READY / TRUE

Both resolvers:

R3 READY / ADMISSIBLE TRUE

AUTH_F15-RECOVERY:

PERMIT

Reason:

AUTHORIZED

Consequence delta:

1

Authority consumed after permit:

TRUE

Determination:

Recovery occurred prospectively only after current,
consistent and admissible resolver correspondence was restored.

## Safe-Degradation Determination

Within the exact frozen F15 scope:

CURRENT RESOLUTION UNAVAILABLE
=>
NO CONSEQUENCE

CONFLICTING REQUIRED RESOLVER VIEWS
=>
NO CONSEQUENCE

CURRENT CONSISTENT INADMISSIBLE STATE
=>
NO CONSEQUENCE

CURRENT CONSISTENT ADMISSIBLE STATE
+
VALID EXECUTION AUTHORITY
=>
PERMIT WITHIN FROZEN SCOPE

CACHE AVAILABILITY
!=
CURRENT EXECUTION STANDING

RESOLVER CONSISTENCY
!=
ADMISSIBILITY

RESOLVER AGREEMENT
!=
EXECUTION AUTHORITY

AVAILABILITY PRESSURE
!=
AUTHORIZATION

## Post-Execution Preservation Note

During post-execution PowerShell orchestration, the interactive
shell received an else statement after its corresponding if
statement had already completed.

The preceding condition was:

missingRuntimeFiles.Count -eq 0

and that condition was TRUE.

Therefore the executed branch had already assigned:

missingBlock = NONE

before the standalone else produced a PowerShell
CommandNotFoundException.

This occurred after the historical Python harness execution.

It did not rerun the harness.

It did not alter the preserved runtime JSON evidence.

It did not alter the observed PASS result.

It did not alter the 13-of-13 evidence completeness finding.

It did not alter any frozen definition or implementation object.

The anomaly is preserved here rather than repaired or erased.

## Non-Claims

This determination does not establish:

- production network-partition safety;
- distributed consensus correctness;
- Byzantine-fault tolerance;
- Raft correctness;
- Paxos correctness;
- production quorum safety;
- cross-process resolver integrity;
- cross-host resolver integrity;
- multi-region consistency;
- database serializability;
- durable resolver storage;
- crash recovery;
- packet-level network behavior;
- DNS security;
- service-mesh security;
- cloud-control-plane correctness;
- malicious resolver resistance;
- cryptographic resolver attestation;
- arbitrary resolver topologies;
- unlimited resolver count;
- unlimited partition duration;
- real-time liveness guarantees;
- universal availability guarantees;
- universal fail-safe behavior.

## Capability Evidence

F15 provides preserved supporting evidence for:

EASA-CAP-05
Replay, Freshness & Changed-State Security

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

and supporting evidence for:

EASA-CAP-02
Security Architecture & Trust-Boundary Design

EASA-CAP-03
Identity, Authorization & Least Privilege

EASA-CAP-08
Evidence, Audit & Forensic Reconstruction

EASA-CAP-09
Secure Change & Configuration Integrity

No broader capability classification is changed by this
determination alone.

## Closure

EASA-F15:

PASS

CLOSED

No successor is required from the preserved F15 observation.

The next prospective examination is EASA-F16:

Bounded Scale Preservation.

Lock it.
Log it.
Prove it.