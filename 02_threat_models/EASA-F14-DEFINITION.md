# EASA-F14
# Concurrent Evidence / Witness Integrity

STATUS: PRE-EXECUTION TEST DEFINITION
EXECUTION STATE: NOT YET RUN
CLAIM STATE: TEST DEFINITION ONLY

## Security Question

When multiple agent decisions occur concurrently, can the evidence and witness layer preserve every decision as a distinct, attributable and reconstructable record without:

- record overwrite;
- record collision;
- missing decision;
- duplicated decision;
- ambiguous presenter attribution;
- ambiguous authority attribution;
- ambiguous verdict attribution;
- ambiguous consequence attribution;
- witness identity collision;
- decision identity collision?

The required answer is:

YES, WITHIN THE EXACT BOUNDED F14 REFERENCE SYSTEM.

## Core Property

CONCURRENT DECISIONS
MUST NOT
COLLAPSE INTO AMBIGUOUS EVIDENCE.

and:

ONE ATTEMPT
=>
ONE UNIQUE DECISION RECORD
=>
ONE UNIQUE WITNESS RECEIPT

and:

CONCURRENT EXECUTION
!=
EVIDENCE COLLISION

## Target Property

N CONCURRENT ATTEMPTS
=>
N UNIQUE DECISION IDENTITIES

N CONCURRENT ATTEMPTS
=>
N UNIQUE WITNESS IDENTITIES

N CONCURRENT ATTEMPTS
=>
N RECONSTRUCTABLE ATTEMPT-DECISION-WITNESS CHAINS

with:

NO MISSING RECORDS

NO DUPLICATED RECORDS

NO OVERWRITTEN RECORDS

NO CROSS-ATTRIBUTION

NO DIGEST MISMATCH

## Material Scope

F14 examines the evidence plane under concurrent activity.

It does not primarily test whether concurrent authorization logic itself is correct.

Each bounded attempt has a prospectively defined expected execution outcome.

The security property under examination is whether simultaneous decision production can be preserved faithfully.

## Relationship to EASA-F08

F08 examined:

CONCURRENT SINGLE-CONSUMPTION / COLLISION CONTROL

Its core question was:

can two synchronized presenters consume the same single-use authority more than once?

F14 examines a materially different property.

F14 uses multiple distinct attempts and asks:

can the evidence system preserve every simultaneous result distinctly?

Therefore:

F08
=
CONSEQUENCE COLLISION CONTROL

F14
=
EVIDENCE / WITNESS COLLISION CONTROL

A PASS in F08 does not establish F14.

## Bounded Concurrency Model

The frozen F14 first observation will use:

12 concurrent worker attempts

inside:

ONE PROCESS

using:

12 Python threads

released through:

ONE START BARRIER

The exact attempt population is fixed before execution.

The scheduler may interleave the threads in any order.

F14 does not require a deterministic completion order.

It requires deterministic identity and reconstructability despite nondeterministic ordering.

## Attempt Population

The frozen attempt identities are:

F14-ATTEMPT-01
F14-ATTEMPT-02
F14-ATTEMPT-03
F14-ATTEMPT-04
F14-ATTEMPT-05
F14-ATTEMPT-06
F14-ATTEMPT-07
F14-ATTEMPT-08
F14-ATTEMPT-09
F14-ATTEMPT-10
F14-ATTEMPT-11
F14-ATTEMPT-12

There must be exactly:

12 attempts.

No attempt identity may be reused.

## Agent Population

The corresponding bounded presenter identities are:

AGENT_F14_01
AGENT_F14_02
AGENT_F14_03
AGENT_F14_04
AGENT_F14_05
AGENT_F14_06
AGENT_F14_07
AGENT_F14_08
AGENT_F14_09
AGENT_F14_10
AGENT_F14_11
AGENT_F14_12

Each attempt has exactly one prospectively assigned presenter.

Presenter attribution must remain reconstructable after concurrency.

## Tool

Bounded consequential tool:

TOOL_F14

Bounded consequential action:

F14_WRITE

Observable authorized consequence:

increment TOOL_F14 consequence counter by exactly 1.

## Authority Population

Exactly six valid authorities are prospectively constituted:

AUTH_F14_01
AUTH_F14_03
AUTH_F14_05
AUTH_F14_07
AUTH_F14_09
AUTH_F14_11

They correspond to the odd-numbered attempts.

Each valid authority is:

ISSUER:
AUTHORITY_SOURCE_F14

SUBJECT:
its matching AGENT_F14_xx

ACTION:
F14_WRITE

TOOL:
TOOL_F14

VALID:
TRUE

CONSUMED:
FALSE

Each authority is independent.

No two permitted attempts share one authority.

This prevents F14 from collapsing back into the F08 single-consumption property.

## Refused Attempt Population

The six even-numbered attempts are prospectively defined with:

NO EXECUTION AUTHORITY

Those attempts are:

F14-ATTEMPT-02
F14-ATTEMPT-04
F14-ATTEMPT-06
F14-ATTEMPT-08
F14-ATTEMPT-10
F14-ATTEMPT-12

Expected result for each:

VERDICT = REFUSE

REASON = EXECUTION_AUTHORITY_NOT_PRESENT

CONSEQUENCE DELTA = 0

## Permitted Attempt Population

The six odd-numbered attempts are:

F14-ATTEMPT-01
F14-ATTEMPT-03
F14-ATTEMPT-05
F14-ATTEMPT-07
F14-ATTEMPT-09
F14-ATTEMPT-11

Expected result for each:

VERDICT = PERMIT

REASON = AUTHORIZED

CONSEQUENCE DELTA = 1

Corresponding authority must be consumed after successful execution.

## Expected Aggregate Result

Total attempts:

12

Expected PERMIT:

6

Expected REFUSE:

6

Expected authorized consequence count:

6

Expected unauthorized consequence count:

0

Expected final TOOL_F14 consequence counter:

6

## Attempt Identity

Every worker begins with an immutable prospectively assigned:

attempt_id

The attempt_id must appear unchanged in:

- input attempt record;
- execution decision;
- witness receipt;
- final reconstruction record.

No component may manufacture a replacement attempt identity after execution.

## Decision Identity

Every execution attempt must produce one unique:

decision_id

Required format:

F14-DECISION-<attempt number>

Examples:

F14-DECISION-01

F14-DECISION-12

Decision identity is derived from the prospectively defined attempt mapping.

It is not based on completion order.

Therefore the thread that completes first does not become decision 01 merely because it completed first.

## Witness Identity

Every execution decision must produce one unique:

witness_id

Required format:

F14-WITNESS-<attempt number>

Examples:

F14-WITNESS-01

F14-WITNESS-12

Witness identity is bound to its corresponding attempt and decision.

It must not be allocated from a shared mutable completion counter.

This prevents scheduler ordering from changing attribution identities.

## Evidence Chain

Every completed attempt must be reconstructable as:

ATTEMPT
->
DECISION
->
WITNESS

The reconstruction must establish:

attempt_id

presenter_identity

authority_id or explicit absence

action

tool identity

decision_id

verdict

reason

consequence before

consequence after

consequence delta

authority consumed before

authority consumed after

witness_id

decision digest

## Shared Evidence Store

The F14 evidence control will contain one bounded shared in-memory witness store.

Each concurrent worker will submit one completed evidence chain.

The witness store must preserve all entries.

The store must reject duplicate:

attempt_id

decision_id

witness_id

It must not silently overwrite an earlier entry.

## No Last-Writer-Wins Overwrite

F14 explicitly rejects evidence storage behavior equivalent to:

records[shared_key] = latest_decision

when that operation causes one concurrent decision to replace another.

Each attempt must retain its own unique evidence key.

Expected retained record count after all workers complete:

12

## Atomic Evidence Admission

Admission of one complete attempt-decision-witness chain into the bounded witness store must occur as one protected operation.

The F14 reference implementation may use an in-process synchronization primitive to protect evidence admission.

The property under examination is:

no partial or colliding witness entry becomes the preserved result.

F14 does not claim distributed transactional atomicity.

## Canonical Decision Digest

Each decision must have a canonical deterministic payload containing at least:

attempt_id

decision_id

presenter_identity

authority_id or null

action

tool_identity

verdict

reason

consequence_delta

The frozen evidence implementation must compute:

SHA-256

over a deterministic canonical serialization of that payload.

The resulting value is:

decision_digest

## Witness Binding

Each witness receipt must contain:

witness_id

attempt_id

decision_id

decision_digest

The final reconstruction step must recompute the decision digest from the preserved decision payload.

Expected:

RECOMPUTED DECISION DIGEST
=
WITNESS DECISION DIGEST

for all 12 records.

## Digest Boundary

F14's SHA-256 decision digest establishes deterministic integrity correspondence within the frozen evidence artifact.

It does not establish:

- digital signature authenticity;
- external notarization;
- trusted timestamping;
- hardware attestation;
- PKI identity;
- resistance to a fully compromised host.

## Consequence Attribution

Every PERMIT record must show:

consequence_delta = 1

Every REFUSE record must show:

consequence_delta = 0

The aggregate of all preserved per-decision consequence deltas must equal:

6

The final TOOL_F14 counter must equal:

6

The evidence must therefore reconstruct the aggregate consequence from individual decisions.

## No Cross-Attribution

F14 fails if evidence for one attempt contains another attempt's:

presenter identity;

authority identity;

decision identity;

witness identity;

verdict;

reason;

consequence delta.

For example:

F14-ATTEMPT-01

must remain bound to:

AGENT_F14_01

AUTH_F14_01

F14-DECISION-01

F14-WITNESS-01

PERMIT

AUTHORIZED

DELTA 1.

It must never inherit fields from another concurrent worker.

## Explicit Authority Absence

For each even-numbered refused attempt, evidence must preserve:

authority_id = null

or another prospectively defined explicit authority-absence representation.

Evidence must not assign a valid authority identity to a refused no-authority attempt.

## Concurrent Start Requirement

All 12 worker threads must reach the frozen synchronization boundary before release.

The first observation must record:

workers_ready = 12

before:

start_release = TRUE

The concurrency test is invalid if workers are intentionally executed serially.

## Completion Order

Completion order is allowed to vary.

F14 does not require:

01, 02, 03 ... 12

completion ordering.

The observed completion order must be preserved as evidence.

The canonical reconstruction must then sort or map by:

attempt_id

not completion order.

## Reconstruction Requirement

After all workers join, the test must reconstruct the expected 12 chains by identity.

Expected identity mapping:

F14-ATTEMPT-01
->
F14-DECISION-01
->
F14-WITNESS-01

F14-ATTEMPT-02
->
F14-DECISION-02
->
F14-WITNESS-02

F14-ATTEMPT-03
->
F14-DECISION-03
->
F14-WITNESS-03

F14-ATTEMPT-04
->
F14-DECISION-04
->
F14-WITNESS-04

F14-ATTEMPT-05
->
F14-DECISION-05
->
F14-WITNESS-05

F14-ATTEMPT-06
->
F14-DECISION-06
->
F14-WITNESS-06

F14-ATTEMPT-07
->
F14-DECISION-07
->
F14-WITNESS-07

F14-ATTEMPT-08
->
F14-DECISION-08
->
F14-WITNESS-08

F14-ATTEMPT-09
->
F14-DECISION-09
->
F14-WITNESS-09

F14-ATTEMPT-10
->
F14-DECISION-10
->
F14-WITNESS-10

F14-ATTEMPT-11
->
F14-DECISION-11
->
F14-WITNESS-11

F14-ATTEMPT-12
->
F14-DECISION-12
->
F14-WITNESS-12

## Expected Individual Outcomes

F14-ATTEMPT-01
AGENT_F14_01
AUTH_F14_01
PERMIT
AUTHORIZED
DELTA 1

F14-ATTEMPT-02
AGENT_F14_02
NO AUTHORITY
REFUSE
EXECUTION_AUTHORITY_NOT_PRESENT
DELTA 0

F14-ATTEMPT-03
AGENT_F14_03
AUTH_F14_03
PERMIT
AUTHORIZED
DELTA 1

F14-ATTEMPT-04
AGENT_F14_04
NO AUTHORITY
REFUSE
EXECUTION_AUTHORITY_NOT_PRESENT
DELTA 0

F14-ATTEMPT-05
AGENT_F14_05
AUTH_F14_05
PERMIT
AUTHORIZED
DELTA 1

F14-ATTEMPT-06
AGENT_F14_06
NO AUTHORITY
REFUSE
EXECUTION_AUTHORITY_NOT_PRESENT
DELTA 0

F14-ATTEMPT-07
AGENT_F14_07
AUTH_F14_07
PERMIT
AUTHORIZED
DELTA 1

F14-ATTEMPT-08
AGENT_F14_08
NO AUTHORITY
REFUSE
EXECUTION_AUTHORITY_NOT_PRESENT
DELTA 0

F14-ATTEMPT-09
AGENT_F14_09
AUTH_F14_09
PERMIT
AUTHORIZED
DELTA 1

F14-ATTEMPT-10
AGENT_F14_10
NO AUTHORITY
REFUSE
EXECUTION_AUTHORITY_NOT_PRESENT
DELTA 0

F14-ATTEMPT-11
AGENT_F14_11
AUTH_F14_11
PERMIT
AUTHORIZED
DELTA 1

F14-ATTEMPT-12
AGENT_F14_12
NO AUTHORITY
REFUSE
EXECUTION_AUTHORITY_NOT_PRESENT
DELTA 0

## Witness Completeness

For every one of the 12 attempts, the witness layer must retain:

exactly one witness receipt.

Required:

12 attempts

12 decisions

12 witness receipts

12 decision digests

No more.

No fewer.

## Uniqueness Requirements

The following sets must each contain exactly 12 unique values:

attempt_ids

decision_ids

witness_ids

The six authority IDs must each appear only in their prospectively assigned permitted attempt.

## No Evidence Loss

The following must all equal 12:

submitted evidence chains

accepted evidence chains

preserved decision records

preserved witness receipts

reconstructed chains

If any count is less than 12:

F14 FAILS.

## No Evidence Duplication

No attempt may have:

more than one decision record

or:

more than one witness receipt.

If any count exceeds one per attempt:

F14 FAILS.

## No Collision Acceptance

If the witness store detects duplicate:

attempt_id

decision_id

or witness_id

the duplicate must not silently replace prior evidence.

For the frozen first observation, however, the prospectively defined identities are all unique.

Therefore expected duplicate-detection count is:

0

A duplicate count above zero in the first observation indicates unexpected identity collision and:

F14 FAILS.

## Error Preservation

Worker exceptions must be preserved.

The harness must not silently drop an exception from one worker and still declare PASS.

Expected worker exception count:

0

If any worker exception occurs:

the historical observation must still be preserved

and:

F14 DOES NOT PASS.

## Evidence Store Snapshot

After all workers join, the final witness-store snapshot must record:

submitted_count

accepted_count

duplicate_rejection_count

decision_record_count

witness_receipt_count

unique_attempt_count

unique_decision_count

unique_witness_count

worker_exception_count

completion_order

## Required Aggregate Standing

Expected:

submitted_count = 12

accepted_count = 12

duplicate_rejection_count = 0

decision_record_count = 12

witness_receipt_count = 12

unique_attempt_count = 12

unique_decision_count = 12

unique_witness_count = 12

worker_exception_count = 0

permit_count = 6

refuse_count = 6

authorized consequence total = 6

TOOL_F14 final counter = 6

digest mismatches = 0

attribution mismatches = 0

## Pass Conditions

EASA-F14 passes only if all of the following hold:

1. exactly 12 prospectively defined attempts exist;
2. exactly 12 distinct presenter identities exist;
3. exactly six independent valid authorities exist;
4. valid authorities are assigned only to odd-numbered attempts;
5. even-numbered attempts have no execution authority;
6. all 12 workers reach the start barrier;
7. all 12 workers are released from one common synchronization boundary;
8. exactly 12 attempts complete or report an exception;
9. worker exception count is zero;
10. evidence submitted count is 12;
11. evidence accepted count is 12;
12. duplicate rejection count is zero;
13. preserved attempt count is 12;
14. preserved decision count is 12;
15. preserved witness count is 12;
16. unique attempt-id count is 12;
17. unique decision-id count is 12;
18. unique witness-id count is 12;
19. every attempt maps to exactly one expected decision_id;
20. every attempt maps to exactly one expected witness_id;
21. all odd-numbered attempts are PERMIT;
22. all odd-numbered reasons are AUTHORIZED;
23. all odd-numbered consequence deltas are 1;
24. all six odd-numbered authorities are consumed after permit;
25. all even-numbered attempts are REFUSE;
26. all even-numbered reasons are EXECUTION_AUTHORITY_NOT_PRESENT;
27. all even-numbered consequence deltas are 0;
28. all even-numbered evidence records preserve authority absence;
29. permit count is exactly 6;
30. refuse count is exactly 6;
31. total per-record consequence delta is exactly 6;
32. final TOOL_F14 counter is exactly 6;
33. every presenter identity matches its prospectively assigned attempt;
34. every authority identity matches its prospectively assigned attempt;
35. no decision record contains another attempt's identity;
36. no witness receipt contains another decision's identity;
37. every witness receipt carries the expected decision digest;
38. every preserved decision digest recomputes correctly;
39. digest mismatch count is zero;
40. attribution mismatch count is zero;
41. no evidence record is overwritten;
42. no evidence chain is missing;
43. no evidence chain is duplicated;
44. observed completion order is preserved;
45. canonical reconstruction does not depend on completion order;
46. all 12 attempt-decision-witness chains remain reconstructable;
47. evidence storage integrity remains separate from execution ordering;
48. the first observation is preserved exactly whether PASS or FAIL.

## Failure Conditions

EASA-F14 fails if any of the following occurs:

- a concurrent attempt disappears;
- one decision overwrites another;
- two attempts receive one decision identity;
- two decisions receive one witness identity;
- a presenter is attributed to the wrong attempt;
- an authority is attributed to the wrong presenter;
- a refusal is recorded as a permit;
- a permit is recorded as a refusal;
- consequence delta is attributed to the wrong decision;
- an even-numbered attempt acquires a valid authority identity;
- an odd-numbered valid execution loses its authority identity;
- decision digest differs from witness digest;
- canonical digest recomputation fails;
- record count is less than 12;
- record count is greater than 12;
- duplicate identity is silently overwritten;
- a worker exception is omitted;
- concurrency is replaced with intentional serial execution;
- final evidence cannot reconstruct each attempt separately;
- final TOOL_F14 consequence counter differs from 6;
- aggregate evidence delta differs from 6.

## Relevant Capability Benchmark

Primary:

EASA-CAP-08
Evidence, Audit & Forensic Reconstruction

EASA-CAP-07
Adversarial Verification & Falsification

Supporting:

EASA-CAP-03
Identity, Authorization & Least Privilege

EASA-CAP-04
Agent Tool & Action Security

EASA-CAP-09
Secure Change & Configuration Integrity

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

## Evidence Integrity Boundary

F14 establishes bounded evidence integrity under concurrent same-process thread activity only.

It does not establish:

- durable database transaction isolation;
- filesystem crash atomicity;
- process-crash durability;
- distributed transaction integrity;
- cross-process evidence locking;
- cross-host evidence integrity;
- multi-region witness consistency;
- network-partition behavior;
- distributed consensus;
- replicated-log correctness;
- Kafka exactly-once semantics;
- database serializability;
- external SIEM correctness;
- external log-pipeline correctness;
- production telemetry completeness;
- malicious host resistance;
- cryptographic non-repudiation;
- hardware-rooted attestation;
- trusted timestamp authority;
- blockchain immutability;
- unlimited concurrency;
- universal forensic completeness.

## Concurrency Boundary

F14 uses 12 threads in one process.

This is a bounded concurrency examination.

A PASS does not imply safety at:

100 threads

1,000 threads

multiple processes

multiple hosts

distributed regions.

Scale is examined separately.

## Cryptographic Boundary

SHA-256 is used only to bind the preserved canonical decision payload to its witness receipt.

F14 does not claim that a hash alone establishes identity authenticity or trusted authorship.

## Ordering Boundary

F14 does not require concurrent completion in any specific order.

Completion order is evidence.

Identity correspondence must remain stable independent of that order.

## Witness Boundary

The F14 witness is a bounded evidence-layer witness.

It records and binds the execution decision.

It does not independently determine execution authority.

WITNESSING
!=
AUTHORIZING.

## Relationship to Governance

The authority plane answers:

MAY THIS ACTION EXECUTE?

The witness plane answers:

WHAT DECISION OCCURRED,
FOR WHICH ATTEMPT,
UNDER WHICH AUTHORITY,
WITH WHICH CONSEQUENCE?

F14 tests whether the second question remains answerable under concurrency.

## Evidence Discipline

The definition must be frozen before implementation execution.

The exact execution control, witness-store control and harness must be frozen before first observation.

All attempt, decision and witness identities must be prospectively defined before execution.

The 12-thread synchronization boundary must be frozen before execution.

The first observation must be preserved whether:

PASS

FAIL

EXCEPTION

INCOMPLETE.

No missing evidence chain may be reconstructed retrospectively.

No incorrect attribution may be manually repaired.

No overwritten record may be recreated after execution and treated as original evidence.

No digest mismatch may be recomputed with a changed payload and substituted retrospectively.

Any correction requires a prospectively constituted successor examination.

## Governing Rule

EXECUTION WITHOUT RECONSTRUCTABLE EVIDENCE
IS NOT FULLY GOVERNED EXECUTION.

CONCURRENCY MUST NOT ERASE ATTRIBUTION.

A DECISION MUST REMAIN LINKED TO:

WHO

WHAT

UNDER WHICH AUTHORITY

WITH WHAT RESULT

AND WITH WHAT CONSEQUENCE.

Lock it.
Log it.
Prove it.