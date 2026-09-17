# EASA v1.0 Baseline — Release Record

RELEASE: EASA-v1.0-baseline
PROJECT: ELIAS Agentic Security Assurance
STATUS: FROZEN BASELINE
EXAMINATION RANGE: EASA-F01 through EASA-F05

## Release Purpose

This release freezes the first EASA agentic-security assurance baseline.

It contains:

- the EASA security boundary;
- the eleven-capability benchmark;
- initial and post-examination capability standing maps;
- five frozen security examination definitions;
- reference security controls;
- prospective execution harnesses;
- preserved first-observation evidence;
- bounded security determinations;
- SHA-256 evidence identities;
- explicit non-claims and remaining examination gaps.

## Five-Claim Result

EASA-F01: PASS / CLOSED
EASA-F02: PASS / CLOSED
EASA-F03: PASS / CLOSED
EASA-F04: PASS / CLOSED
EASA-F05: PASS / CLOSED

## Bounded Properties

F01:
NO_VALID_EXECUTION_AUTHORITY => NO_CONSEQUENCE

F02:
AUTHORITY_PRESENT + REQUEST_OUTSIDE_AUTHORIZED_SCOPE => NO_CONSEQUENCE

F03:
AUTHORITY_ALREADY_CONSUMED + REPLAY_ATTEMPT => NO_CONSEQUENCE

F04:
AUTHORITY_VALID_AT_T0 + MATERIAL_GOVERNING_STATE_CHANGE + EXECUTION_ATTEMPT_AT_T1
=> REFUSE BEFORE CONSEQUENCE

F05:
HIGH_IMPACT_ACTION + REQUIRED_HUMAN_AUTHORITY_ABSENT
=> REFUSE BEFORE CONSEQUENCE

## Post-Examination Capability Standing

PROVEN: 5
PARTIAL: 6
NOT_YET_ESTABLISHED: 0

PROVEN:
- EASA-CAP-02
- EASA-CAP-05
- EASA-CAP-06
- EASA-CAP-09
- EASA-CAP-11

PARTIAL:
- EASA-CAP-01
- EASA-CAP-03
- EASA-CAP-04
- EASA-CAP-07
- EASA-CAP-08
- EASA-CAP-10

## Evidence Discipline

The release preserves the sequence:

DEFINE
-> HASH
-> FREEZE
-> IMPLEMENT
-> HASH
-> FREEZE
-> EXECUTE
-> PRESERVE
-> DETERMINE

Historical observations are not retrospectively repaired.

A failed future examination must remain preserved and any correction must be constituted as a successor.

## Scope Boundary

This is a bounded reference-system security assurance release.

It is not:

- universal cybersecurity assurance;
- certification;
- regulatory approval;
- production deployment certification;
- penetration-testing accreditation;
- third-party assurance.

## Release Principle

CAPABILITY != AUTHORITY

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.
