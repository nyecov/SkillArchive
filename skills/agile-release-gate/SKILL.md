---
id: 6c2dad9d-4b06-4892-b4fa-dc0960db629b
name: agile-release-gate
version: 1.0.0
level: tactical
description: 'Use when a feature or epic is "code complete" and approaching release.
  Governs the pre-release audit checklist, traceability verification, regression gate,
  and release memo compilation. Complements the Ship skill with SDLC-specific artifact
  traceability requirements. TRIGGER when preparing final sign-off on a story, epic,
  or initiative.'
category: engineering
tags:
- agile
- release
- engineering
- safety
- methodology
references:
  - name: Agile SDLC Orchestrator
    path: ../agile-sdlc/SKILL.md
  - name: Agile Testing
    path: ../agile-testing/SKILL.md
  - name: Test-Driven Development (TDD)
    path: ../test-driven-development/SKILL.md
  - name: Ship (Production Deployment)
    path: ../release-management/SKILL.md
---
# Agile Release Gate

Governs the transition from "Feature Complete" to "Production Ready" within an Agile SDLC. Compiles test executions into a Release Memo and enforces a complete pre-release audit before sign-off.

## Core Mandates

### 1. Pre-Release Audit Is Non-Negotiable
- **Action:** Every release must pass the complete pre-release audit checklist before sign-off. All tools must exit 0. No exceptions.
- **Constraint:** A single failing validator blocks the release. No partial sign-offs.
- **Integration:** Implements **Jidoka** — the line stops when any anomaly is detected.

### 2. Evidence-Backed Sign-Off
- **Action:** Every Test Execution (TX) must have an attached `## Evidence` block (screenshot, recording, or log reference). For UI-representation stories, the evidence must show the user-visible behavior working.
- **Constraint:** A TX without evidence is incomplete. A unit-test-only TX for a UI story is insufficient.
- **Integration:** Connects to **Shisa Kanko** — point-and-call verification that the actual user-facing behavior was confirmed.

### 3. Full Traceability Chain
- **Action:** Verify the complete chain: Initiative → Epic → Story → Subtask → Code → Test Design → Test Execution. Every link must resolve. Every story must have at least one TX.
- **Constraint:** Broken traceability chains block release sign-off.
- **Integration:** Enables `Validate-AgileHierarchy.ps1` to function as the automated traceability gate.

### 4. TDD Convention Integrity
- **Action:** Run `verify_red_phase.py --range origin/main..HEAD` to confirm the `[Red]/[Green]/[Refactor]` commit-prefix convention is intact across the release range.
- **Constraint:** A `[Green]` commit without a preceding `[Red]` for the same story is a convention violation and blocks sign-off.
- **Integration:** Enforces `test-driven-development` discipline as an auditable release gate.

## Pre-Release Audit Checklist

Run every validator. All must exit 0 before sign-off:

| # | Check | Pass Criterion |
|---|---|---|
| 1 | `triage_validator.py --strict` | All bugs/issues passed 4-review triage |
| 2 | `coverage.py all` | Full coverage suite green (rollup, subtasks, carving, validate-tests) |
| 3 | `Validate-AgileHierarchy.ps1` | Zero broken parent/child links |
| 4 | `Sync-EpicAcceptance.ps1` | Zero stale Epic ACs, zero dangling Story refs |
| 5 | `Triage-Issues.ps1 -Open` | Zero active BLOCKERs |
| 6 | `verify_red_phase.py` | TDD commit conventions intact across release range |
| 7 | Full test suite (E2E + unit) | All suites green against release candidate |
| 8 | Spec-gap rollup | No release-blocking open findings |

After the audit, compile a Release Memo summarizing: features shipped, bugs resolved, safety verification status, and any open non-blocking issues deferred to the next release.

## Escalation & Halting

- **Jidoka:** Any failing validator halts release sign-off unconditionally. File an ISSUE for each failure before the next attempt.
- **Ho-Ren-So:** Report the audit summary (pass/fail per check, count of deferred items) to stakeholders before the release memo is finalized.

## Implementation Workflow

1. **Trigger:** A story, epic, or initiative is marked "feature complete" and is being prepared for release.
2. **Execute:** Run the pre-release audit checklist. Fix all failures. Compile the Release Memo.
3. **Verify:** All checklist items exit 0. Release Memo is complete.
4. **Output:** A signed-off release with a durable Release Memo and a clean audit trail. Hand off to `Ship` for production deployment.
