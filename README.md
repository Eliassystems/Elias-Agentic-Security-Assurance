# ELIAS Agentic Security Assurance (EASA)

## EASA v2.0 - F01-F17 + X1M Evidence Release

EASA examines the boundary between an AI/agent proposing an action and a system allowing that action to produce consequence.

> **CAPABILITY != AUTHORITY**

## Headline bounded result

> **1,000,000 bounded agentic execution attempts. 800,000 adversarial refusal cases. 0 unauthorized consequences.**

Independent evidence-only verification: **PASS**

Formal determination: **PASS WITHIN FROZEN SCOPE**

Historical harness rerun: **NO**

- [F01-F17 gate index](01_benchmark/EASA-F01-F17-GATE-INDEX.md)
- [F16 scale examination index](01_benchmark/EASA-F16-SCALE-INDEX.md)
- [Claims and nonclaims](00_scope/EASA-v2.0-CLAIMS-AND-NONCLAIMS.md)
- [X1M independent verification](05_evidence/EASA-F16-X1M-INDEPENDENT-VERIFICATION.json)
- [X1M formal determination](05_evidence/EASA-F16-X1M-DETERMINATION.md)
- [Release record](09_releases/EASA-v2.0-F17-X1M-RELEASE.md)

## Examination standing

| Gate | Standing | Definition | Determination |
| --- | --- | --- | --- |
| F01 | **PASS / CLOSED** | [definition](02_threat_models/EASA-F01-DEFINITION.md) | [determination](05_evidence/EASA-F01-DETERMINATION.md) |
| F02 | **PASS / CLOSED** | [definition](02_threat_models/EASA-F02-DEFINITION.md) | [determination](05_evidence/EASA-F02-DETERMINATION.md) |
| F03 | **PASS / CLOSED** | [definition](02_threat_models/EASA-F03-DEFINITION.md) | [determination](05_evidence/EASA-F03-DETERMINATION.md) |
| F04 | **PASS / CLOSED** | [definition](02_threat_models/EASA-F04-DEFINITION.md) | [determination](05_evidence/EASA-F04-DETERMINATION.md) |
| F05 | **PASS / CLOSED** | [definition](02_threat_models/EASA-F05-DEFINITION.md) | [determination](05_evidence/EASA-F05-DETERMINATION.md) |
| F06 | **PASS / CLOSED** | [definition](02_threat_models/EASA-F06-DEFINITION.md) | [determination](05_evidence/EASA-F06-DETERMINATION.md) |
| F07 | **PASS / CLOSED** | [definition](02_threat_models/EASA-F07-DEFINITION.md) | [determination](05_evidence/EASA-F07-DETERMINATION.md) |
| F08 | **PASS / CLOSED** | [definition](02_threat_models/EASA-F08-DEFINITION.md) | [determination](05_evidence/EASA-F08-DETERMINATION.md) |
| F09 | **PASS / CLOSED** | [definition](02_threat_models/EASA-F09-DEFINITION.md) | [determination](05_evidence/EASA-F09-DETERMINATION.md) |
| F10 | **PASS / CLOSED** | [definition](02_threat_models/EASA-F10-DEFINITION.md) | [determination](05_evidence/EASA-F10-DETERMINATION.md) |
| F11 | **PASS / CLOSED** | [definition](02_threat_models/EASA-F11-DEFINITION.md) | [determination](05_evidence/EASA-F11-DETERMINATION.md) |
| F12 | **PASS / CLOSED / REVALIDATED** | [definition](02_threat_models/EASA-F12-DEFINITION.md) | [determination](05_evidence/EASA-F12-DETERMINATION-REVALIDATION.md) |
| F13 | **PASS / CLOSED** | [definition](02_threat_models/EASA-F13-DEFINITION.md) | [determination](05_evidence/EASA-F13-DETERMINATION.md) |
| F14 | **NOT ESTABLISHED - PRESERVED** | [definition](02_threat_models/EASA-F14-DEFINITION.md) | [determination](05_evidence/EASA-F14-DETERMINATION.md) |
| F14-S1 | **PASS / CLOSED - PROSPECTIVE SUCCESSOR** | [definition](02_threat_models/EASA-F14-S1-DEFINITION.md) | [determination](05_evidence/EASA-F14-S1-DETERMINATION.md) |
| F15 | **PASS / CLOSED** | [definition](02_threat_models/EASA-F15-DEFINITION.md) | [determination](05_evidence/EASA-F15-DETERMINATION.md) |
| F16 | **PASS / CLOSED / REVALIDATED** | [definition](02_threat_models/EASA-F16-DEFINITION.md) | [determination](05_evidence/EASA-F16-DETERMINATION-REVALIDATION.md) |
| F17 | **PASS / CLOSED / REVALIDATED** | [definition](02_threat_models/EASA-F17-DEFINITION.md) | [determination](05_evidence/EASA-F17-DETERMINATION-REVALIDATION.md) |

F14 remains **NOT ESTABLISHED** as a preserved historical finding.

F14-S1 is a separately constituted prospective successor. No retrospective repair converts F14 into a pass.

## Scale ladder

| Examination | Population | Standing |
| --- | ---: | --- |
| F16 | through N=1,000 | PASS / CLOSED / REVALIDATED |
| F16-X10K | 10,000 | PASS / CLOSED |
| F16-X100K | 100,000 | PASS / CLOSED |
| F16-X1M | 1,000,000 | PASS / CLOSED / INDEPENDENT EVIDENCE-ONLY VERIFICATION |

### X1M frozen chain

```text
Definition:      7b84dc7
Implementation:  70e6429
Observation:     49f6c1d
Closure:         1be60c7
```

Independent verification SHA-256:

`D0C9FDC95965C7E3F58CB5FF40B4A24D605307C1B22542B660554D2983A50543`

Formal determination SHA-256:

`3E06E708A19EE9C3AC9D7DA09B690C01B7B35DCC549EDEB454A7AE76D5970375`

Global canonical decision digest:

`AFDC32CA9A2D5452A8C0F14551CCF02321A126129EF7212698019E30059D6BE2`

## Evidence discipline

```text
DEFINE -> HASH -> FREEZE -> BUILD -> HASH / FREEZE IMPLEMENTATION
-> FIRST EXECUTION -> PRESERVE FIRST OBSERVATION -> DETERMINE -> FREEZE
```

Failures remain failures. Successors remain successors. Historical evidence is not retrospectively repaired.

## Capability benchmark boundary

The original v1.0 capability map remains a historical baseline:

```text
PROVEN:              5
PARTIAL:             6
NOT_YET_ESTABLISHED: 0
```

This v2.0 evidence release does not silently re-adjudicate that capability matrix.

## Explicit nonclaims

This release does **not** establish unlimited scale, populations above 1,000,000, one million simultaneous operating-system threads, one million physical agents, coordinated swarm behaviour, swarm consensus, distributed swarm attacks, cross-process/cross-host/cloud-distributed assurance, production performance, denial-of-service resistance, crash tolerance, Byzantine tolerance, universal cybersecurity, universal AI security, or universal agent safety.

The evidence applies to the exact bounded systems and conditions documented in this repository.

## Governing rules

```text
CAPABILITY != AUTHORITY
DOCUMENTATION != EVIDENCE
PRIOR SUCCESS != CURRENT STANDING
CLAIM != PROOF
```

**Evidence stops where the evidence stops.**

---

ELIAS Systems Ltd  
Agentic Security Assurance  
Current publication package: `EASA-v2.0-F17-X1M`
