# EASA-F16-X1M Formal Determination

## Identity

Examination:

EASA-F16-X1M

Definition commit:

7b84dc7

Implementation commit:

70e6429

First historical observation commit:

49f6c1d

Independent verification:

EVIDENCE ONLY

Historical harness rerun:

NO

## Independent Verification Result

PASS

The independent verifier streamed all 100 committed decision shards directly from the frozen observation commit.

Exactly 1,000,000 committed decision records were independently decompressed, parsed, canonicalized, sequenced, behaviour-checked, counted, and hashed.

The historical harness was not executed or imported during verification.

## Verified Population

Target population:

1,000,000

Verified decision records:

1,000,000

Execution chunks:

100

Records per chunk:

10,000

Frozen worker setting:

64

The 100 chunks are resource-management units inside the single historical examination. They are not separate scale examinations.

## Verified Outcomes

AUTHORIZED:

200,000

NO_AUTHORITY:

200,000

PRESENTER_IDENTITY_MISMATCH:

200,000

TOOL_IDENTITY_MISMATCH:

200,000

PRECONSUMED_AUTHORITY_REPLAY:

200,000

PERMIT:

200,000

REFUSE:

800,000

Authorized consequences:

200,000

Unauthorized consequences:

0

Authority-bearing attempts:

800,000

Unique attempt identities:

1,000,000

Unique presenter identities:

1,000,000

Unique authority identities:

800,000

## Independent Digest Reconciliation

Global canonical decision SHA-256:

AFDC32CA9A2D5452A8C0F14551CCF02321A126129EF7212698019E30059D6BE2

Shard-manifest canonical SHA-256:

243078EE0330743707FCEB4E83645B270456913B60A71D502894F74F66DD5F0D

Summary canonical SHA-256:

92FF8A6D5B379B542209A86ADF837C9A3EE7128C15B1C49205F867744E8231E8

All three independently recomputed identities matched the frozen historical evidence.

Independent verification record SHA-256:

D0C9FDC95965C7E3F58CB5FF40B4A24D605307C1B22542B660554D2983A50543

## Determination

PASS - SUPPORTED WITHIN FROZEN SCOPE

The first historical EASA-F16-X1M observation supports the defined bounded property at N = 1,000,000 within the exact frozen reference scope.

The evidence establishes:

1,000,000 bounded agentic execution attempts.

800,000 adversarial refusal cases.

0 unauthorized consequences.

## Scope Boundary

This determination is bounded to the frozen EASA-F16-X1M reference examination:

- one Python process;
- same-process execution control;
- ThreadPoolExecutor max_workers = 64;
- exactly 1,000,000 independently identified attempts;
- exactly 100 contiguous resource-management chunks of 10,000 records;
- the frozen five-class deterministic population;
- the frozen primary and alternate tool identities;
- the frozen action identity;
- the committed historical evidence population.

## Nonclaims

This determination does not establish:

- unlimited scale;
- populations above 1,000,000;
- one million simultaneous operating-system threads;
- one million physical agents;
- coordinated swarm behaviour;
- swarm consensus;
- distributed swarm attacks;
- cross-process execution;
- cross-host execution;
- cloud-distributed execution;
- production performance;
- denial-of-service resistance;
- crash tolerance;
- Byzantine tolerance;
- universal security;
- universal AI or agent safety.

The observed execution duration is historical evidence only and is not adjudicated as a performance benchmark.

## Historical Integrity

Historical harness rerun:

NO

Failed observation replacement:

NO

Retrospective runtime repair:

NO

Claim above N = 1,000,000:

NO

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.
