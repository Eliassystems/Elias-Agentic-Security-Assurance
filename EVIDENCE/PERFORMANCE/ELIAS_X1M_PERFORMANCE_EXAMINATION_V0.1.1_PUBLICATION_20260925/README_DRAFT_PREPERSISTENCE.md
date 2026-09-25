# Elias X1M Performance Examination

Package ID: ELIAS_X1M_PERFORMANCE_EXAMINATION_V0.1_20260925

Status: DRAFT — PERSISTED RE-EXECUTION REQUIRED

Repository:
<LOCAL_REPOSITORY>

Frozen baseline branch:
easa-f06-f17-multi-agent-security

Frozen baseline commit:
a313cd17a9c1d4a2c66185bfb38d243b6dd8a67c

Frozen baseline source:
03_controls/easa_f16_x1m_execution.py

Frozen baseline source SHA-256:
85ac55b617aacd714252a995558fed74d6b6e330dd4055d7d2b9f29ae59971de

Package creation:
2026-09-25T00:24:17.1074064+01:00

## Purpose

This package preserves the observed results of a bounded performance
examination of the existing Elias X1M execution-governance gate and an
experimental Shadow V3 implementation.

The examination investigated whether execution-governance latency could
be materially reduced without intentionally removing the tested
authority checks, single-use execution constraint, or 21-field decision
information surface.

## Core observed results

1. 100,000 generated sequential current-versus-V3 comparisons:
   - mismatches: 0
   - compared decision fields: 21

2. Shadow V3 single-use authority contention:
   - worker counts: 2, 4, 8, 16, 32, 64
   - rounds per worker count: 100
   - total rounds: 600
   - failures: 0
   - required property per round:
     exactly one PERMIT,
     all other contenders REFUSE,
     total consequence delta = 1,
     final consequential-tool counter = 1

3. Ten-process ABBA batch comparison:
   - aggregate CURRENT mean: 7.1762 microseconds
   - aggregate V3 mean: 1.7300 microseconds
   - ratio of aggregate means: 4.148x
   - aggregate latency reduction: 75.9%
   - observed per-process ratios: 3.587x to 4.714x

4. Seven-path performance matrix:
   - V3 was faster on every tested path
   - measured reductions ranged from 72.3% to 80.3%
   - authority setup was outside the timed region

## Evidence boundary

These are bounded experimental measurements.

They are not a production latency guarantee.
They are not hardware-independent results.
They are not a claim of exhaustive semantic equivalence.
They are not a third-party-system comparison.
They are not a claim of sub-microsecond repeatable performance.

The frozen baseline implementation was not modified during the
examination.

## Persistence caveat

Shadow V3 was executed from Python supplied through PowerShell into
fresh/in-memory Python processes.

The tested V3 logic had not yet been persisted as a canonical source
file at the time these observations were produced.

Accordingly this package remains DRAFT until a persisted V3 source is
created, hashed, and the core examinations are rerun from that exact
artifact.

Evidence stops where the evidence stops.

Lock it. Log it. Prove it.
