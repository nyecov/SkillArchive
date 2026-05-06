---
id: 3f7a1c2d-8e4b-4a9f-b6c5-2d0e9f3a7b1c
name: agile-sdlc
version: 1.0.0
level: methodology
description: 'Use when orchestrating the full Software Development Lifecycle (SDLC) across
  Agile, TDD, and testing stages. Handles Planning → Development → CI → Feature Verification
  → Regression → Release. TRIGGER at the start of any multi-stage development turn or
  when a stage transition needs to be governed.'
category: methodology
tags:
- agile
- sdlc
- methodology
- tdd
- testing
references:
  - name: Agile Backlog Authoring
    path: ../agile-backlog/SKILL.md
  - name: Test-Driven Development (TDD)
    path: ../test-driven-development/SKILL.md
  - name: Agile Testing
    path: ../agile-testing/SKILL.md
  - name: Agile Release Gate
    path: ../agile-release-gate/SKILL.md
  - name: Spec Mapping
    path: ../spec-mapping/SKILL.md
---
# Integrated Agile SDLC

Governs the complete software development lifecycle by integrating Agile backlog management, Test-Driven Development, and rigorous testing into a single unified workflow.

## Core Mandates

### 1. Minimize Bloat
- **Action:** Before creating any artifact or task, grep the backlog for overlapping items. Prefer extending existing artifacts over creating new ones. Merge items that share 80%+ scope.
- **Constraint:** Never create a new epic, story, or test artifact without checking for an existing one that covers the same work.
- **Integration:** Connects to **Lean Foundations** — eliminate documentation waste before it accumulates.

### 2. Stage-Gate Sequencing
- **Action:** Enforce the strict stage order: Planning → Development (TDD) → CI/Merge → Feature Verification → Regression → Release. No stage may begin until its predecessor's gates are verified.
- **Constraint:** NEVER skip the Regression stage before a release. NEVER ship without a passing test execution artifact with evidence.
- **Integration:** Each stage delegates to the owning skill: `agile-backlog`, `test-driven-development`, `agile-testing`, `agile-release-gate`.

### 3. Diagrams Are Derivatives
- **Action:** If an error is found in a diagram or flowchart, fix the spec source first, then the code, then redraw the diagram.
- **Constraint:** NEVER update a diagram before updating the source of truth.
- **Integration:** Prevents documentation drift that undermines **Gemba** (go-and-see accuracy).

### 4. Universal Resumption
- **Action:** Before starting any turn, read the backlog's spec-gap ledger and any active ISSUE artifacts to resume rather than duplicate in-flight work.
- **Constraint:** Never start a new task without first checking what is already open or blocked.
- **Integration:** Supports **Kaizen** by building on prior observations instead of repeating them.

## SDLC Stages

| Stage | Owning Skill | Gate to Next Stage |
|---|---|---|
| 1. Planning & Kickoff | `agile-backlog`, `spec-mapping` | Backlog health check green |
| 2. Development (TDD) | `test-driven-development` | All ACs have passing [Green] commits |
| 3. CI / Merge | `agile-testing` | Unit + integration suite green |
| 4. Feature Verification | `agile-testing` | Passing TX artifact with evidence |
| 5. System Regression | `agile-testing` | Full regression suite green |
| 6. Acceptance & Release | `agile-release-gate` | All release gates pass |

## Escalation & Halting

- **Jidoka:** If any stage gate fails (non-zero exit, missing evidence, or broken link), halt the pipeline and raise an ISSUE artifact before proceeding.
- **Ho-Ren-So:** Use Sodan (Consult) when a stage gate failure requires a strategic decision (e.g., defer story vs. hotfix vs. release block).

## Implementation Workflow

1. **Trigger:** A development turn begins, a stage transition is needed, or a release is being prepared.
2. **Execute:** Identify the current stage. Invoke the owning skill for that stage. Verify all gate criteria are met before advancing.
3. **Verify:** Check that every artifact produced in this stage (commit, test execution, release memo) is present and valid.
4. **Output:** A verified stage completion with gate evidence, followed by activation of the next stage's owning skill.
ng skill.
ng skill.
