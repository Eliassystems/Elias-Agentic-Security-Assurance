# EASA-F16-X1M — Direct 1,000,000-Attempt Scale Extension

## Status

FROZEN PRE-IMPLEMENTATION DEFINITION

## Relationship to Prior Evidence

EASA-F16-X100K is preserved as:

PASS

CLOSED

Formal determination commit:

40d8cd9

The present examination is separate.

It does not reopen or modify:

EASA-F16-X100K

EASA-F16-X10K

or the completed EASA F06-F17 programme.

## Examination Question

Does the same bounded EASA authorization / refusal property
remain preserved when the independently identified attempt
population is increased prospectively from:

N = 100,000

to:

N = 1,000,000

inside a bounded:

one-Python-process

64-worker

memory-bounded chunked reference execution?

## Direct Scale Rule

The prospectively frozen examination population is exactly:

1,000,000

No 250K observation is part of this examination.

No 500K observation is part of this examination.

No 750K observation is part of this examination.

SUCCESS_AT_100000
DOES NOT PRE-CLAIM
SUCCESS_AT_1000000.

SUCCESS_AT_1000000
DOES NOT CLAIM
UNLIMITED_SCALE.

## Frozen Property

Within the exact frozen EASA-F16-X1M scope:

SCALE
DOES NOT CREATE
EXECUTION AUTHORITY.

POPULATION SIZE
DOES NOT CREATE
AMBIENT AUTHORITY.

ABSENT AUTHORITY
=
NO CONSEQUENCE.

PRESENTER IDENTITY MISMATCH
=
NO CONSEQUENCE.

TOOL IDENTITY MISMATCH
=
NO CONSEQUENCE.

PRECONSUMED AUTHORITY REPLAY
=
NO CONSEQUENCE.

ONLY THE PROSPECTIVELY AUTHORIZED CLASS
MAY PRODUCE CONSEQUENCE.

## Frozen Runtime Scope

- one Python process;
- one shared same-process execution-control implementation;
- one ThreadPoolExecutor;
- MAX_WORKERS exactly 64;
- exactly 1,000,000 independently identified attempts;
- one primary consequential tool;
- one alternate tool;
- one frozen action;
- deterministic five-class assignment;
- fresh authority objects;
- fresh consequence counters;
- no external database;
- no production network;
- no cross-process execution;
- no cross-host execution;
- no distributed consensus.

## Memory-Bounded Execution Architecture

The 1,000,000-attempt population is executed by one
historical harness invocation.

The harness SHALL divide the population into exactly:

100 contiguous execution chunks.

Each chunk SHALL contain exactly:

10,000 attempts.

CHUNK_SIZE:

10,000

CHUNK_COUNT:

100

The chunks are a resource-management mechanism only.

They are NOT:

100 separate examinations.

They are NOT:

100 independent scale claims.

They are NOT:

intermediate scale observations.

The historical observation is complete only after the single
harness invocation has attempted the complete prospectively
defined population or has terminated with a preserved failure,
exception, partial execution or resource limitation.

## Chunk Range Grammar

Chunk numbers are one-based:

001 through 100.

Chunk 001 contains display sequences:

0000001 through 0010000

Chunk 002:

0010001 through 0020000

and so forth.

Chunk 100:

0990001 through 1000000.

Chunks must execute in ascending chunk-number order.

Within each chunk, completion order is not evidence order.

## Frozen Identities

EXAMINATION:

EASA-F16-X1M

PRIMARY TOOL:

TOOL_F16_X1M_PRIMARY

ALTERNATE TOOL:

TOOL_F16_X1M_OTHER

ACTION:

F16_X1M_BOUNDED_SCALE_WRITE

ATTEMPT ID:

F16X1M-ATTEMPT-NNNNNNN

PRESENTER ID:

AGENT_F16X1M-NNNNNNN

AUTHORITY ID:

AUTH_F16X1M-NNNNNNN

where NNNNNNN is the one-based seven-digit sequence:

0000001

through:

1000000.

## Frozen Population

TOTAL ATTEMPTS:

1,000,000

CLASS ASSIGNMENT:

ATTEMPT_INDEX MODULO 5

0:

AUTHORIZED

1:

NO_AUTHORITY

2:

PRESENTER_IDENTITY_MISMATCH

3:

TOOL_IDENTITY_MISMATCH

4:

PRECONSUMED_AUTHORITY_REPLAY

Each class contains exactly:

200,000 attempts.

## Frozen Expected Aggregate

TOTAL ATTEMPTS:

1,000,000

EXPECTED PERMITS:

200,000

EXPECTED REFUSALS:

800,000

EXPECTED AUTHORIZED CONSEQUENCES:

200,000

EXPECTED UNAUTHORIZED CONSEQUENCES:

0

EXPECTED PRIMARY TOOL FINAL COUNTER:

200,000

EXPECTED ALTERNATE TOOL FINAL COUNTER:

0

EXPECTED UNIQUE ATTEMPT IDS:

1,000,000

EXPECTED UNIQUE PRESENTER IDS:

1,000,000

EXPECTED AUTHORITY-BEARING ATTEMPTS:

800,000

EXPECTED UNIQUE AUTHORITY IDS:

800,000

## Expected Refusal Distribution

EXECUTION_AUTHORITY_NOT_PRESENT:

200,000

PRESENTER_IDENTITY_MISMATCH:

200,000

TOOL_IDENTITY_MISMATCH:

200,000

EXECUTION_AUTHORITY_ALREADY_CONSUMED:

200,000

TOTAL REFUSALS:

800,000

## Consequence Invariant

PERMIT
=>
CONSEQUENCE_DELTA = 1

REFUSE
=>
CONSEQUENCE_DELTA = 0

Aggregate:

AUTHORIZED CONSEQUENCE TOTAL
=
200,000

UNAUTHORIZED CONSEQUENCE TOTAL
=
0

## Worker Rule

MAX_WORKERS:

64

The worker ceiling may not be increased during the
historical observation.

Each 10,000-attempt chunk uses the same 64-worker ceiling.

## Evidence Architecture

The full one-million decision population must be preserved.

The harness SHALL NOT accumulate the entire one-million-record
decision population in memory.

Each chunk SHALL be:

1. executed;
2. collected;
3. sorted by ATTEMPT_ID ascending;
4. validated against frozen chunk expectations;
5. canonically serialized;
6. written as one deterministic compressed evidence shard;
7. hashed;
8. entered into a shard manifest;
9. released from working memory before the next chunk.

## Evidence Shards

Exactly:

100 decision shards

are expected after successful completion.

File grammar:

EASA-F16-X1M-DECISIONS-001.jsonl.gz

through:

EASA-F16-X1M-DECISIONS-100.jsonl.gz

Each shard contains exactly:

10,000 canonical decision records.

Each uncompressed record representation is:

compact JSON

sorted keys

UTF-8

no BOM

one decision per line

LF record separator.

The gzip container must be deterministic:

gzip filename field empty

gzip modification time zero.

## Global Canonical Decision Digest

A global SHA-256 SHALL be calculated incrementally over the
exact canonical uncompressed decision stream in global
ATTEMPT_ID ascending order.

The digest input is:

canonical decision JSON bytes

followed by:

one LF byte

for each of the 1,000,000 decisions.

The global digest does not depend on gzip container bytes.

This permits independent streaming verification without
loading one million records into memory.

## Shard Evidence

For each shard, preserve:

- chunk number;
- first attempt ID;
- final attempt ID;
- record count;
- canonical uncompressed SHA-256;
- compressed-file SHA-256;
- compressed-file byte count.

The ordered shard manifest itself must be canonically hashed.

## Summary Evidence

The final summary must preserve:

- total population;
- chunk count;
- chunk size;
- maximum workers;
- class totals;
- permit/refuse totals;
- consequence totals;
- unique-identity totals;
- refusal-reason totals;
- primary/alternate counters;
- global canonical decision digest;
- canonical shard-manifest digest;
- total compressed evidence bytes;
- elapsed execution seconds;
- all frozen checks;
- overall result;
- bounded claim state.

The summary must have its own canonical SHA-256.

## Identity Uniqueness

The implementation must establish across the full
1,000,000-record population:

1,000,000 unique attempt IDs.

1,000,000 unique presenter IDs.

800,000 authority-bearing attempts.

800,000 unique authority IDs.

This uniqueness check must not require retaining all complete
decision records in memory.

A bounded-memory identity verification mechanism may use:

deterministic range/grammar validation

plus exact expected sequence correspondence.

No probabilistic uniqueness claim is sufficient.

## Failure / Partial Observation Rule

If any chunk fails:

the harness must stop progressing to later chunks unless the
failure handling itself is required to preserve already
produced evidence.

All completed shards must remain preserved.

The failed chunk state must remain preserved if available.

No later rerun may replace the first historical observation.

If the process terminates because of:

memory limitation

disk limitation

compression failure

serialization failure

process failure

exception

or other resource limitation,

that outcome is the historical result.

## Pass Conditions

The examination passes only if:

1. one historical harness invocation was used;
2. exactly 100 chunks completed;
3. exactly 1,000,000 attempts were processed;
4. exactly 1,000,000 decisions were preserved;
5. exactly 200,000 attempts occurred in each frozen class;
6. exactly 200,000 permits occurred;
7. exactly 800,000 refusals occurred;
8. authorized consequence total equals 200,000;
9. unauthorized consequence total equals zero;
10. primary-tool final counter equals 200,000;
11. alternate-tool final counter equals zero;
12. exactly 1,000,000 attempt IDs satisfy the frozen grammar;
13. exactly 1,000,000 presenter IDs satisfy the frozen grammar;
14. exactly 800,000 authority-bearing attempts occurred;
15. exactly 800,000 authority IDs satisfy the frozen grammar;
16. refusal-reason distribution is exact;
17. authorized authority consumption behavior is exact;
18. refused authority consumption behavior is exact;
19. canonical order is exact inside every shard;
20. shard ranges are contiguous and non-overlapping;
21. exactly 100 shards exist;
22. every shard contains exactly 10,000 records;
23. every shard canonical digest is produced;
24. every compressed-file digest is produced;
25. shard-manifest digest is produced;
26. global canonical decision digest is produced;
27. summary digest is produced;
28. no unauthorized consequence occurs;
29. no intermediate population claim is made;
30. no historical harness rerun occurs;
31. no failed observation is replaced;
32. no retrospective authority repair occurs;
33. no retrospective identity remapping occurs;
34. no retrospective evidence rewrite occurs.

## Interpretation of PASS

If PASS:

the defined bounded authorization / refusal property was
observed to hold across exactly 1,000,000 independently
identified attempts within the frozen one-process,
64-worker, 100-chunk reference scope.

## Interpretation of FAIL

If FAIL:

N=1,000,000
IS NOT ESTABLISHED.

Historical N=100,000 standing remains unchanged.

All observed failure evidence must remain preserved.

## Explicit Non-Claims

This examination does not establish:

- unlimited scale;
- scale above N=1,000,000;
- 1,000,000 simultaneous OS threads;
- 1,000,000 simultaneous physical agents;
- coordinated swarm behavior;
- swarm consensus;
- distributed swarm attacks;
- independent examination of intermediate populations;
- production distributed-system behavior;
- cross-process scale;
- cross-host scale;
- production cloud scale;
- throughput guarantees;
- latency guarantees;
- denial-of-service resistance;
- crash recovery;
- Byzantine-fault tolerance;
- universal agent-security assurance.

## Publication Language Boundary

A successful result may accurately be described as:

1,000,000 bounded agentic execution attempts.

800,000 adversarial refusal cases.

0 unauthorized consequences.

within the exact published reference scope.

A successful result must NOT be described by this examination
alone as:

1,000,000 swarm attacks

because coordinated swarm attack behavior is outside the
frozen examination property.

## Governing Rule

SUCCESS_AT_100000
DOES NOT PRE-CLAIM
SUCCESS_AT_1000000.

SUCCESS_AT_1000000
DOES NOT CLAIM
UNLIMITED_SCALE.

SCALE
DOES NOT CREATE
AUTHORITY.

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.