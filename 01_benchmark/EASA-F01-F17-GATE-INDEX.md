# EASA F01-F17 Gate Index

Release: **EASA-v2.0-F17-X1M**

This index is the navigation layer for the frozen EASA examination sequence. It does not replace the underlying definitions, observations, determinations, revalidations, failure records or successor records.

## Examination standing

| Gate | Standing | Definition | Determination |
| --- | --- | --- | --- |
| F01 | **PASS / CLOSED** | [definition](../02_threat_models/EASA-F01-DEFINITION.md) | [determination](../05_evidence/EASA-F01-DETERMINATION.md) |
| F02 | **PASS / CLOSED** | [definition](../02_threat_models/EASA-F02-DEFINITION.md) | [determination](../05_evidence/EASA-F02-DETERMINATION.md) |
| F03 | **PASS / CLOSED** | [definition](../02_threat_models/EASA-F03-DEFINITION.md) | [determination](../05_evidence/EASA-F03-DETERMINATION.md) |
| F04 | **PASS / CLOSED** | [definition](../02_threat_models/EASA-F04-DEFINITION.md) | [determination](../05_evidence/EASA-F04-DETERMINATION.md) |
| F05 | **PASS / CLOSED** | [definition](../02_threat_models/EASA-F05-DEFINITION.md) | [determination](../05_evidence/EASA-F05-DETERMINATION.md) |
| F06 | **PASS / CLOSED** | [definition](../02_threat_models/EASA-F06-DEFINITION.md) | [determination](../05_evidence/EASA-F06-DETERMINATION.md) |
| F07 | **PASS / CLOSED** | [definition](../02_threat_models/EASA-F07-DEFINITION.md) | [determination](../05_evidence/EASA-F07-DETERMINATION.md) |
| F08 | **PASS / CLOSED** | [definition](../02_threat_models/EASA-F08-DEFINITION.md) | [determination](../05_evidence/EASA-F08-DETERMINATION.md) |
| F09 | **PASS / CLOSED** | [definition](../02_threat_models/EASA-F09-DEFINITION.md) | [determination](../05_evidence/EASA-F09-DETERMINATION.md) |
| F10 | **PASS / CLOSED** | [definition](../02_threat_models/EASA-F10-DEFINITION.md) | [determination](../05_evidence/EASA-F10-DETERMINATION.md) |
| F11 | **PASS / CLOSED** | [definition](../02_threat_models/EASA-F11-DEFINITION.md) | [determination](../05_evidence/EASA-F11-DETERMINATION.md) |
| F12 | **PASS / CLOSED / REVALIDATED** | [definition](../02_threat_models/EASA-F12-DEFINITION.md) | [determination](../05_evidence/EASA-F12-DETERMINATION-REVALIDATION.md) |
| F13 | **PASS / CLOSED** | [definition](../02_threat_models/EASA-F13-DEFINITION.md) | [determination](../05_evidence/EASA-F13-DETERMINATION.md) |
| F14 | **NOT ESTABLISHED - PRESERVED** | [definition](../02_threat_models/EASA-F14-DEFINITION.md) | [determination](../05_evidence/EASA-F14-DETERMINATION.md) |
| F14-S1 | **PASS / CLOSED - PROSPECTIVE SUCCESSOR** | [definition](../02_threat_models/EASA-F14-S1-DEFINITION.md) | [determination](../05_evidence/EASA-F14-S1-DETERMINATION.md) |
| F15 | **PASS / CLOSED** | [definition](../02_threat_models/EASA-F15-DEFINITION.md) | [determination](../05_evidence/EASA-F15-DETERMINATION.md) |
| F16 | **PASS / CLOSED / REVALIDATED** | [definition](../02_threat_models/EASA-F16-DEFINITION.md) | [determination](../05_evidence/EASA-F16-DETERMINATION-REVALIDATION.md) |
| F17 | **PASS / CLOSED / REVALIDATED** | [definition](../02_threat_models/EASA-F17-DEFINITION.md) | [determination](../05_evidence/EASA-F17-DETERMINATION-REVALIDATION.md) |

## Continuity rules

EASA-F14 remains preserved as **NOT ESTABLISHED**.

It was not retrospectively repaired, rewritten, remapped or waived.

EASA-F14-S1 is a separately constituted prospective successor and carries its own PASS / CLOSED standing.

Where a historical determination required prospective revalidation, this index points to the authoritative revalidation object while preserving the original determination in the repository.

This applies to F12, F16 and F17.

## Evidence discipline

```text
DEFINE
-> HASH
-> FREEZE
-> BUILD
-> HASH / FREEZE IMPLEMENTATION
-> FIRST EXECUTION
-> PRESERVE FIRST OBSERVATION
-> DETERMINE
-> FREEZE
```

Failures remain failures. Successors remain successors.

**Evidence stops where the evidence stops.**
