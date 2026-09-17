# ELIAS Agentic Security Assurance

## EASA v1.0 Baseline

**ELIAS Agentic Security Assurance (EASA)** examines the security boundary between an AI/agent deciding to act and a system actually allowing that action to produce consequence.

Core principle:

> **CAPABILITY != AUTHORITY**

Technical capability, model intent, historical validity or confidence do not independently establish present execution authority.

## Security Boundary

```text
AI / AGENT REQUESTS ACTION
        |
        v
AUTHORITY IS EVALUATED
        |
        v
SECURITY CONDITIONS ARE APPLIED
        |
        v
PERMIT OR REFUSE
        |
        v
CONSEQUENCE
        |
        v
EVIDENCE / DETERMINATION
```

## Five Bounded Security Examinations

### EASA-F01 — Unauthorized Agent Tool Execution

```text
NO_VALID_EXECUTION_AUTHORITY
=>
NO_CONSEQUENCE
```

**Result: PASS / CLOSED**

### EASA-F02 — Authority Present, Scope Invalid

```text
AUTHORITY_PRESENT
+
REQUEST_OUTSIDE_AUTHORIZED_SCOPE
=>
NO_CONSEQUENCE
```

**Result: PASS / CLOSED**

### EASA-F03 — Consumed Authority Replay

```text
AUTHORITY_ALREADY_CONSUMED
+
REPLAY_ATTEMPT
=>
NO_CONSEQUENCE
```

**Result: PASS / CLOSED**

### EASA-F04 — Stale Authority After Material State Change

```text
AUTHORITY_VALID_AT_T0
+
MATERIAL_GOVERNING_STATE_CHANGE
+
EXECUTION_ATTEMPT_AT_T1
=>
REFUSE_BEFORE_CONSEQUENCE
```

**Result: PASS / CLOSED**

### EASA-F05 — Required Human Authority for High-Impact Action

```text
HIGH_IMPACT_ACTION
+
REQUIRED_HUMAN_AUTHORITY_ABSENT
=>
REFUSE_BEFORE_CONSEQUENCE
```

**Result: PASS / CLOSED**

## Evidence Method

Each examination follows the same evidence discipline:

```text
DEFINE
-> HASH
-> FREEZE
-> BUILD
-> HASH
-> FREEZE IMPLEMENTATION
-> FIRST EXECUTION
-> PRESERVE FIRST OBSERVATION
-> DETERMINE
-> FREEZE
```

A result is not rewritten after execution.

If an implementation fails, the failed historical object is preserved and any correction must become a successor with a new prospective examination.

## Capability Benchmark Standing

EASA-BM-001 contains eleven frozen capability targets.

Following completion of EASA-F01 through EASA-F05, EASA-MAP-002 records:

```text
PROVEN:              5
PARTIAL:             6
NOT_YET_ESTABLISHED: 0
```

### PROVEN within the bounded EASA reference-system scope

- EASA-CAP-02 — Security Architecture & Trust-Boundary Design
- EASA-CAP-05 — Replay, Freshness & Changed-State Security
- EASA-CAP-06 — High-Impact Action & Human Authority Control
- EASA-CAP-09 — Secure Change & Configuration Integrity
- EASA-CAP-11 — Security Communication & Bounded Reporting

### PARTIAL

- EASA-CAP-01 — Threat & Attack-Path Analysis
- EASA-CAP-03 — Identity, Authorization & Least Privilege
- EASA-CAP-04 — Agent Tool & Action Security
- EASA-CAP-07 — Adversarial Verification & Falsification
- EASA-CAP-08 — Evidence, Audit & Forensic Reconstruction
- EASA-CAP-10 — Containment, Failure Handling & Safe Refusal

`PARTIAL` does not mean failed. It means supporting evidence exists, but the complete frozen examination boundary has not yet been satisfied.

## Repository Structure

```text
00_scope          Security boundary
01_benchmark      Capability benchmark and standing maps
02_threat_models  Frozen examination definitions
03_controls       Reference security controls
04_tests          Prospective test harnesses
05_evidence       Preserved observations and determinations
06_failures       Reserved preserved failure records
07_successors     Reserved successor implementations
08_witness        Witness / attestation material
09_releases       Frozen release records
tools             Supporting tooling
```

## Explicit Non-Claims

This baseline does **not** establish:

- universal AI or agent security;
- universal cybersecurity assurance;
- production IAM assurance;
- network penetration-testing capability;
- malware reverse engineering;
- endpoint detection and response;
- SOC operations;
- distributed replay resistance;
- cryptographic freshness;
- concurrent race resistance;
- universal human-in-the-loop safety;
- biometric human identity;
- legal consent validity;
- universal irreversible-action safety;
- automatic detection of every material real-world state change.

The evidence applies to the exact bounded systems and conditions documented in this repository.

## Governing Rules

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
Baseline: EASA v1.0
