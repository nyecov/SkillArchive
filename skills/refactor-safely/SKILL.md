---
id: d0c7179f-b348-4ffd-b429-a5f42f213e17
name: refactor-safely
version: 1.0.0
level: tactical
description: 'Use when planning or executing any refactor — from renaming a symbol
  to restructuring a layer boundary. Enforces impact analysis before edits and test
  validation after every small change. TRIGGER before any refactor that touches more
  than one file or changes a public symbol.'
category: engineering
tags:
- engineering
- refactoring
- safety
- methodology
references:
  - name: Code Review
    path: ../code-review/SKILL.md
  - name: Test-Driven Development (TDD)
    path: ../test-driven-development/SKILL.md
  - name: Gemba (Factual Discovery)
    path: ../gemba/SKILL.md
  - name: Nemawashi (Impact Analysis)
    path: ../nemawashi/SKILL.md
---
# Refactor Safely

Plan and execute refactoring with confidence using dependency analysis, incremental edits, and continuous test validation. A refactor that breaks behavior is not a refactor — it is a bug introduction.

## Core Mandates

### 1. Impact Analysis Before First Edit
- **Action:** Before touching any file, use grep to find all references to every symbol being changed. Map the full impact radius: callers, implementers, test files, documentation.
- **Constraint:** Do not make a single edit until the full impact radius is understood. Partial analysis leads to partial refactors — the worst kind.
- **Integration:** Implements **Nemawashi** — build consensus on the scope before making changes.

### 2. Small Steps, Continuous Green
- **Action:** Refactor in the smallest verifiable increments possible. Run the test suite after every logical change. If a step breaks the green state, revert it before continuing.
- **Constraint:** NEVER commit a refactor step that leaves the test suite red. Red commits are reserved for the [Red] phase of TDD — not for refactoring.
- **Integration:** Connects to **TDD Commit Protocol** — Refactor phase requires all tests to stay green.

### 3. Targeted Edits, Not Full Rewrites
- **Action:** Use the Edit tool with precise context strings for surgical replacements. Avoid rewriting entire files when only a few lines need to change.
- **Constraint:** Do not use Write to overwrite large files (over 500 lines). Use Edit with enough surrounding context to guarantee uniqueness.
- **Integration:** Prevents accidental removal of adjacent logic — a **Poka-yoke** against bulk-overwrite errors.

### 4. Quality Audit After Completion
- **Action:** After all refactor steps are complete and the test suite is green, run the full code quality audit (lint, naming, unused deps, standards) on the changed files.
- **Constraint:** Do not close a Refactor phase commit until all audit checks pass or all exceptions are explicitly noted.
- **Integration:** Applies **Kodawari Craftsmanship** — the refactor is not done until the code is cleaner than it started.

**Go audit after refactor:**
- `python audit_go_unused_deps.py`
- `python audit_go_lint.py`
- `python audit_go_naming.py`
- `python audit_go_standards.py`

**Python audit after refactor:**
- `python audit_python_unused_deps.py`
- `python audit_python_lint.py`
- `python audit_python_naming.py`
- `python audit_python_standards.py`

## Refactor Threshold

| Trigger | Approach |
|---|---|
| Single-file local cleanup, no signature change | Proceed directly |
| Cross-file rename within one layer | Impact analysis + `refactor-safely` |
| Layer-boundary change or interface change | `architectural-anchoring` review first |
| Performance work changing algorithmic complexity | Architecture review + benchmarking |

## Escalation & Halting

- **Jidoka:** If a refactor step breaks the test suite and cannot be reverted cleanly, halt. File an ISSUE before continuing.
- **Ho-Ren-So:** For layer-boundary refactors, consult the architect before making edits. Structural changes with unreviewed impact are a project risk.

## Implementation Workflow

1. **Trigger:** A refactor is needed — symbol rename, extract function, restructure module, etc.
2. **Execute:** Impact analysis → incremental edits → test after each step → quality audit.
3. **Verify:** Test suite green. All quality audit checks pass. No new issues introduced.
4. **Output:** A cleaner, behavior-preserving codebase with a `[Refactor]` commit and passing tests.
