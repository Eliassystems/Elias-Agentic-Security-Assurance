# EASA-F05-DET-001
# Bounded Security Determination

OBJECT: EASA-F05
TEST: Required Human Authority for High-Impact Action
RESULT: PASS
DETERMINATION STATE: BOUNDED PROPERTY ESTABLISHED

## Proven Property

Within the frozen EASA-F05 local reference system:

The same defined high-impact action was evaluated under the same machine execution-authority and scope conditions.

When required human authority was present:

- verdict: PERMIT
- consequence delta: 1

When required human authority was absent:

- machine execution authority remained present
- required execution scope remained present
- human authority remained explicitly required
- verdict: REFUSE
- reason: REQUIRED_HUMAN_AUTHORITY_ABSENT
- consequence delta: 0

Therefore, within the tested boundary:

HIGH_IMPACT_ACTION
+
REQUIRED_HUMAN_AUTHORITY_ABSENT
=>
REFUSE BEFORE CONSEQUENCE

Machine execution authority did not substitute for required external human authority.

## Evidence Bindings

Definition SHA256:
4DFE296B00E82EEE60287BFCE92C879B2FE58561F18454891448157D814A8B3A

Control SHA256:
7895A642BED2C725A127BF210F8E1757786C2E992D800E9C4AD66608F2C15BCA

Harness SHA256:
8226A075DBF444D31E6F1C5D295DBA84E151FEEC328B087D6CE845939542AA47

Human-Present Evidence SHA256:
5F73257AC42144576D1A40959F16B5AD36C104B5BC38D887C6ADE56FCD80F942

Human-Absent Evidence SHA256:
F547DF2B2AAADA6E39B54C180DA374CAC1B0828DBE059B2194F0063B872A6FD6

Summary Evidence SHA256:
B9DADE6EED577B7299651F7542857A45AF605EE56B15998CE191879BD4F8F2B1

## Five-Claim Standing

CLAIM 1:
NO_VALID_EXECUTION_AUTHORITY => NO_CONSEQUENCE
STATUS: PROVEN WITHIN F01 BOUNDARY

CLAIM 2:
AUTHORITY_PRESENT + REQUEST_OUTSIDE_AUTHORIZED_SCOPE => NO_CONSEQUENCE
STATUS: PROVEN WITHIN F02 BOUNDARY

CLAIM 3:
AUTHORITY_ALREADY_CONSUMED + REPLAY_ATTEMPT => NO_CONSEQUENCE
STATUS: PROVEN WITHIN F03 BOUNDARY

CLAIM 4:
AUTHORITY_VALID_AT_T0 + MATERIAL_STATE_CHANGE + EXECUTION_ATTEMPT_AT_T1
=> REFUSE BEFORE CONSEQUENCE
STATUS: PROVEN WITHIN F04 BOUNDARY

CLAIM 5:
HIGH_IMPACT_ACTION + REQUIRED_HUMAN_AUTHORITY_ABSENT
=> REFUSE BEFORE CONSEQUENCE
STATUS: PROVEN WITHIN F05 BOUNDARY

## Benchmark Relationship

Primary:

EASA-CAP-06
High-Impact Action & Human Authority Control

Supporting:

EASA-CAP-03
Identity, Authorization & Least Privilege

EASA-CAP-04
Agent Tool & Action Security

EASA-CAP-07
Adversarial Verification & Falsification

EASA-CAP-10
Containment, Failure Handling & Safe Refusal

No benchmark capability is automatically promoted by this determination alone.

Capability standing will be reconciled separately against the complete frozen EASA-BM-001 benchmark.

## Explicit Non-Claims

EASA-F05 does not establish:

- universal human-in-the-loop safety;
- biometric human identity verification;
- production approval-workflow security;
- multi-party approval;
- quorum authorization;
- legal consent validity;
- non-repudiation;
- cryptographic human signatures;
- universal irreversible-action safety;
- social-engineering resistance;
- coercion resistance;
- universal classification of all high-impact actions.

## Final Five-Claim Examination State

F01: PASS / CLOSED
F02: PASS / CLOSED
F03: PASS / CLOSED
F04: PASS / CLOSED
F05: PASS / CLOSED

The five bounded security properties are now ready for capability-level reconciliation.

Evidence stops where the evidence stops.
