# EASA-F14 — Bounded Determination

## Examination

EASA-F14 — Concurrent Evidence / Witness Integrity

## Historical First Observation

PRESERVED

Observation commit:

330b997

Observed harness result:

PASS

Observed claim state:

OBSERVATION_SUPPORTS_DEFINED_PROPERTY

## Final Determination

NOT ESTABLISHED AS EXACTLY DEFINED

SUCCESSOR EXAMINATION REQUIRED

## Reason

The historical first observation is internally coherent and technically successful within the frozen implementation that actually executed.

However, the implementation does not preserve two exact prospectively frozen identity formats from the EASA-F14 definition.

The frozen definition specified presenter identities in the form:

AGENT_F14_01
AGENT_F14_02
...
AGENT_F14_12

The frozen implementation and first observation used:

AGENT_F14-01
AGENT_F14-02
...
AGENT_F14-12

The frozen definition specified the six authority identities in the form:

AUTH_F14_01
AUTH_F14_03
AUTH_F14_05
AUTH_F14_07
AUTH_F14_09
AUTH_F14_11

The frozen implementation and first observation used:

AUTH_F14-01
AUTH_F14-03
AUTH_F14-05
AUTH_F14-07
AUTH_F14-09
AUTH_F14-11

This yields:

12 presenter identity-format differences

plus:

6 authority identity-format differences

for:

18 exact frozen identity-contract differences.

## Important Distinction

This determination does not classify the concurrent evidence mechanism itself as failed.

The historical observation established, inside the implementation that actually ran:

12 workers ready

one common barrier release

0 worker exceptions

12 submitted evidence chains

12 accepted evidence chains

0 duplicate rejections

12 decision records

12 witness receipts

12 unique attempt identities

12 unique decision identities

12 unique witness identities

6 PERMIT

6 REFUSE

aggregate evidence consequence delta 6

final TOOL_F14 consequence counter 6

0 digest mismatches

0 attribution mismatches

0 missing attempts

12 reconstructed attempt-decision-witness chains.

The observed completion order was non-canonical while the canonical reconstruction remained intact.

Therefore the execution produced strong evidence for the underlying concurrent witness-integrity mechanism.

## Why Exact Closure Is Withheld

EASA examination discipline requires the implementation to answer the exact frozen prospective definition.

A frozen identity contract is part of that definition.

The later implementation cannot silently substitute:

underscore

with:

hyphen

and then retrospectively treat the two identities as identical.

Semantic similarity does not erase byte-level or identifier-level difference.

Accordingly:

IMPLEMENTATION-LOCAL PROPERTY SUPPORT
does not equal
EXACT FROZEN-DEFINITION ESTABLISHMENT.

## No Retrospective Repair

The following are prohibited:

- editing the frozen definition to use hyphens;
- editing the historical implementation to use underscores;
- editing first-observation evidence;
- renaming historical presenters;
- renaming historical authorities;
- remapping witness records;
- rerunning the F14 harness and replacing the first observation;
- treating the mismatch as though it never occurred.

The historical first observation remains preserved exactly at:

330b997

## Successor Requirement

A prospectively constituted F14 successor must:

1. choose one identity grammar before implementation;
2. use that grammar identically in definition, implementation, binding, harness and evidence;
3. freeze the successor definition;
4. freeze the successor implementation;
5. execute a new first observation exactly once;
6. preserve that successor observation independently.

The historical EASA-F14 observation remains valid evidence about the system that actually ran.

It is not promoted into a claim about an identity contract it did not exactly implement.

## Frozen Historical Identities

Definition SHA256:

344E0411C5F4991D0BC987A6799E2B9434C948E28F24F4470253EABC2BDEDB06

Definition hash-record SHA256:

96166AE6E83CDC16048F6486C465FC149155952482F5F0E21509B53A3D70DCBF

Execution control SHA256:

26A70FECD61683A78C2B6CBEC65F477B7387068551AFC6C008CE3647D72655EF

Witness control SHA256:

521B9DEE4C2FA17640FC2720795C6FA174A07D63BB726F5052DE84D47B3C121D

Harness SHA256:

445A0EB564FD38A558208E2B9272A8B58B851308398B1E66552195FAE61216C5

Implementation binding SHA256:

B6F33C5ED76F6D73CCE31A87A92853625E642D9D3F85C0C93C1A94FD399E12D0

Population SHA256:

E6641E0B08DA7F7CACE8F46FA63A8866635DC6AE4FA7A6E33D080D4EAD193807

Witness-store SHA256:

C8DA2AB4B59321D1D7191E8F0A7B4456896D54D150C04A7D5BA4399E0719A57E

Reconstruction SHA256:

E08B167ED6AE7A5ABBED6BC558D2653040157C389F7DB253010E05ECC86FBF60

Summary SHA256:

BCEF7C1B37C504D83C2F4362794B053974B87CE81BE4681432E439CBF836096E

Console SHA256:

81D3EF41B2FDC7C03E3DE2873C714F6B4AA162EA3D4F1EC6E5A15B01A63C14E0

First-observation manifest SHA256:

276E0E36E5BBB8B7E5BAB0E42BD0DC3926DBC04CF16E5605FD09A8EDE47703CB

## Evidence Chain

Definition freeze:

51cfbcb

Implementation freeze:

1ee0273

First observation preservation:

330b997

Bounded determination:

THIS COMMIT

## Standing

F14 ORIGINAL:

FIRST OBSERVATION = PRESERVED

OBSERVATION INTERNAL RESULT = PASS

EXACT FROZEN DEFINITION = NOT ESTABLISHED

CAUSE = DEFINITION / IMPLEMENTATION IDENTITY-CONTRACT MISMATCH

RETROSPECTIVE REPAIR = PROHIBITED

SUCCESSOR = REQUIRED

Evidence stops where the evidence stops.

Lock it.
Log it.
Prove it.