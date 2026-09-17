# EASA-MAP-001
# Initial Agentic Security Capability Standing Map

STATUS: INITIAL MAPPING
BENCHMARK: EASA-BM-001
CLAIM STATE: NO CAPABILITY CURRENTLY PROMOTED TO PROVEN

## Mapping Rule

This map distinguishes:

1. antecedent Elias capability,
2. candidate supporting evidence,
3. evidence constituted inside EASA,
4. final EASA standing.

Prior Elias work may justify PARTIAL standing.

Prior work alone does NOT justify PROVEN standing inside this programme.

PROVEN requires:
- identifiable evidence;
- evidence integrity;
- benchmark-condition correspondence;
- prospective or reproducible execution where required;
- explicit bounded determination.

---

## EASA-CAP-01 — Threat & Attack-Path Analysis

INITIAL STANDING: PARTIAL

ANTECEDENT CANDIDATES:
- replay-seam discovery;
- authority-bypass analysis;
- adversarial failure identification;
- preserved negative cases.

GAP TO PROVEN:
A formal EASA threat model must identify assets, actors, entry points, trust boundaries and at least one executable attack path.

---

## EASA-CAP-02 — Security Architecture & Trust-Boundary Design

INITIAL STANDING: PARTIAL

ANTECEDENT CANDIDATES:
- execution firewall;
- authority boundaries;
- identity → authority → policy → execution separation;
- fail-closed refusal behaviour.

GAP TO PROVEN:
The boundary must be instantiated and tested directly inside EASA.

---

## EASA-CAP-03 — Identity, Authorization & Least Privilege

INITIAL STANDING: PARTIAL

ANTECEDENT CANDIDATES:
- Capability != Authority;
- external authority checks;
- permit-bound execution;
- identity and authority separation.

GAP TO PROVEN:
EASA must execute paired authorized / unauthorized cases against the same capability surface.

---

## EASA-CAP-04 — Agent Tool & Action Security

INITIAL STANDING: PARTIAL

ANTECEDENT CANDIDATES:
- brokered tool execution;
- execution permission gates;
- refusal before consequence;
- bounded action handling.

GAP TO PROVEN:
EASA must expose at least one agent tool surface and prove unauthorized invocation cannot reach consequence.

---

## EASA-CAP-05 — Replay, Freshness & Changed-State Security

INITIAL STANDING: PARTIAL

ANTECEDENT CANDIDATES:
- consumed attestation handling;
- authority epoch change;
- changed-condition reassessment;
- stale authorization refusal.

GAP TO PROVEN:
EASA must execute replay and changed-state attacks prospectively under a frozen test definition.

---

## EASA-CAP-06 — High-Impact Action & Human Authority Control

INITIAL STANDING: PARTIAL

ANTECEDENT CANDIDATES:
- human-authority-presence checks;
- external veto;
- consequence-boundary withholding.

GAP TO PROVEN:
EASA must define a high-impact action and demonstrate refusal when required human authority is absent.

---

## EASA-CAP-07 — Adversarial Verification & Falsification

INITIAL STANDING: PARTIAL

ANTECEDENT CANDIDATES:
- preserved failures;
- successor implementations;
- negative controls;
- prospective reruns.

GAP TO PROVEN:
EASA must preserve a complete attack → observation → successor → retest chain.

---

## EASA-CAP-08 — Evidence, Audit & Forensic Reconstruction

INITIAL STANDING: PARTIAL

ANTECEDENT CANDIDATES:
- SHA-256 evidence identities;
- witness records;
- preserved decision evidence;
- frozen Git history.

GAP TO PROVEN:
EASA must reconstruct one consequential security decision entirely from locally preserved records.

---

## EASA-CAP-09 — Secure Change & Configuration Integrity

INITIAL STANDING: PARTIAL

ANTECEDENT CANDIDATES:
- authority epoch changes;
- changed-condition reassessment;
- predecessor/successor separation;
- no silent standing carry-forward.

GAP TO PROVEN:
EASA must mutate a security-relevant state or configuration and prove mandatory reassessment.

---

## EASA-CAP-10 — Containment, Failure Handling & Safe Refusal

INITIAL STANDING: PARTIAL

ANTECEDENT CANDIDATES:
- refusal before execution;
- containment semantics;
- preserved failed states;
- no retrospective repair.

GAP TO PROVEN:
EASA must prove a prohibited consequence remains unreachable after a security-control failure.

---

## EASA-CAP-11 — Security Communication & Bounded Reporting

INITIAL STANDING: PARTIAL

ANTECEDENT CANDIDATES:
- explicit non-claims;
- bounded determinations;
- preserved failures;
- next-falsification-boundary reporting.

GAP TO PROVEN:
EASA must issue a complete security determination derived from its own test evidence.

---

# Initial Standing Summary

EASA-CAP-01: PARTIAL
EASA-CAP-02: PARTIAL
EASA-CAP-03: PARTIAL
EASA-CAP-04: PARTIAL
EASA-CAP-05: PARTIAL
EASA-CAP-06: PARTIAL
EASA-CAP-07: PARTIAL
EASA-CAP-08: PARTIAL
EASA-CAP-09: PARTIAL
EASA-CAP-10: PARTIAL
EASA-CAP-11: PARTIAL

PROVEN: 0
PARTIAL: 11
NOT_YET_ESTABLISHED: 0

## Interpretation

The existing Elias estate supplies substantial antecedent candidate material.

This record does not promote that material automatically.

The purpose of EASA is now to convert candidate capability into locally constituted, executable cybersecurity evidence.

## Next Examination Boundary

EASA-F01:

UNAUTHORIZED AGENT TOOL EXECUTION

Question:

Can an AI/agent request and technically reach a consequential tool while remaining unable to execute that tool without independently valid execution authority?

This will become the first EASA security falsification target.

Evidence stops where the evidence stops.
