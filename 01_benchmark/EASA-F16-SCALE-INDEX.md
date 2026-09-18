# EASA F16 Scale Examination Index

Release: **EASA-v2.0-F17-X1M**

EASA scale evidence is constituted as separate bounded examinations.

| Examination | Population | Standing | Definition | Determination |
| --- | ---: | --- | --- | --- |
| F16 | through N=1,000 | PASS / CLOSED / REVALIDATED | [definition](../02_threat_models/EASA-F16-DEFINITION.md) | [determination](../05_evidence/EASA-F16-DETERMINATION-REVALIDATION.md) |
| F16-X10K | 10,000 | PASS / CLOSED | [definition](../02_threat_models/EASA-F16-X10K-DEFINITION.md) | [determination](../05_evidence/EASA-F16-X10K-DETERMINATION.md) |
| F16-X100K | 100,000 | PASS / CLOSED | [definition](../02_threat_models/EASA-F16-X100K-DEFINITION.md) | [determination](../05_evidence/EASA-F16-X100K-DETERMINATION.md) |
| F16-X1M | 1,000,000 | PASS / CLOSED / INDEPENDENT EVIDENCE-ONLY VERIFICATION | [definition](../02_threat_models/EASA-F16-X1M-DEFINITION.md) | [determination](../05_evidence/EASA-F16-X1M-DETERMINATION.md) |

## X1M bounded result

> **1,000,000 bounded agentic execution attempts. 800,000 adversarial refusal cases. 0 unauthorized consequences.**

```text
ATTEMPTS=1000000
DECISIONS=1000000
PERMITS=200000
REFUSALS=800000
AUTHORIZED_CONSEQUENCES=200000
UNAUTHORIZED_CONSEQUENCES=0
DECISION_SHARDS=100
```

Chain:

`7b84dc7 -> 70e6429 -> 49f6c1d -> 1be60c7`

Independent verification SHA-256:

`D0C9FDC95965C7E3F58CB5FF40B4A24D605307C1B22542B660554D2983A50543`

Formal determination SHA-256:

`3E06E708A19EE9C3AC9D7DA09B690C01B7B35DCC549EDEB454A7AE76D5970375`

Global canonical decision digest:

`AFDC32CA9A2D5452A8C0F14551CCF02321A126129EF7212698019E30059D6BE2`

Canonical shard-manifest digest:

`243078EE0330743707FCEB4E83645B270456913B60A71D502894F74F66DD5F0D`

Canonical summary digest:

`92FF8A6D5B379B542209A86ADF837C9A3EE7128C15B1C49205F867744E8231E8`

Historical harness rerun: **NO**

The 100 chunks are resource-management units inside one historical examination. They are not separate scale examinations.

This does not establish one million simultaneous threads, one million physical agents, coordinated swarm attacks, distributed execution, production performance or unlimited scale.
