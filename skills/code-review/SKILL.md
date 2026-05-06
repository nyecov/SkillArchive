---
id: 4d6f8b0d-2e4a-4d6f-8b0d-2e4a6d8f0b2e
name: code-review
version: 1.0.0
level: tactical
description: 'Use when performing a structured code review on a PR, diff, or changeset.
  Handles change detection, impact analysis, contract verification, code quality audits,
  and regression confirmation. TRIGGER when reviewing a PR, validating a fix, or auditing
  changed files before merge.'
category: engineering
tags:
- engineering
- code-review
- quality
- testing
references:
  - name: Refactor Safely
    path: ../refactor-safely/SKILL.md
  - name: Test-Driven Development (TDD)
    path: ../test-driven-development/SKILL.md
  - name: Architecture & Anchoring
    path: ../architectural-anchoring/SKILL.md
---
# Code Review

Perform a thorough, risk-aware code review using focused discovery and impact analysis. Output findings grouped by risk level with a merge recommendation.

## Core Mandates

### 1. Change Analysis First
- **Action:** Start every review with `git diff` to identify the exact lines and logic changed. Do not form opinions before reading the actual diff.
- **Constraint:** Never review code based on the PR description alone. The diff is the ground truth.
- **Integration:** Implements **Genchi Genbutsu** — go and see the actual change.

### 2. Impact Analysis Before Judgment
- **Action:** For every modified function or data structure, grep for all call sites and consumers. Verify that all callers are consistent with the new signature or behavior.
- **Constraint:** A change with unexamined call sites is not reviewed — it is partially reviewed. Do not mark a review complete until impact is bounded.
- **Integration:** Connects to **Refactor Safely** — impact radius must be understood before approval.

### 3. Code Quality Audit
- **Action:** Run the appropriate maintenance audit scripts on changed files as part of every review. Use `--path` to limit scope to changed files only.
- **Constraint:** Do not approve a change that introduces new linting violations, unused imports, or naming convention violations without explicitly noting them as accepted tradeoffs.
- **Integration:** Applies **Kodawari Craftsmanship** — relentless pursuit of quality as a standard gate.

**Go changes:**
- `python audit_go_unused_deps.py --path <changed-files>`
- `python audit_go_lint.py --path <changed-files>`
- `python audit_go_naming.py --path <changed-files>`
- `python audit_go_standards.py --path <changed-files>`

**Python changes:**
- `python audit_python_unused_deps.py --path <changed-files>`
- `python audit_python_lint.py --path <changed-files>`
- `python audit_python_naming.py --path <changed-files>`
- `python audit_python_standards.py --path <changed-files>`

### 4. Test Coverage Confirmation
- **Action:** Verify that the change has corresponding test coverage. Run the project test suite or the relevant story's test execution to confirm no regressions.
- **Constraint:** A change without test coverage confirmation is not approved — it is deferred pending evidence.
- **Integration:** Enforces `test-driven-development` discipline at review time.

## Output Format

Group findings by risk level:

- **High** — correctness issues, broken contracts, missing error handling, security concerns
- **Medium** — untested paths, naming violations, complexity spikes, coupling increases
- **Low** — style, documentation, minor optimization opportunities

End with: overall merge recommendation (Approve / Request Changes / Block) and a one-line rationale.

## Token Efficiency Rules

- **Focused Discovery:** grep with narrow patterns and file filters. Do not grep broadly.
- **Surgical Reads:** Use start/end line bounds for files over 100 lines.
- **Target:** Complete any review in 5 or fewer tool calls, 800 or fewer output tokens.

## Escalation & Halting

- **Jidoka:** If a change breaks a layer boundary (per `architectural-anchoring` checklist) or introduces a security issue, halt and block merge unconditionally.
- **Ho-Ren-So:** Report High findings to the author before the review is finalized.

## Implementation Workflow

1. **Trigger:** A PR is opened or a code change needs formal review.
2. **Execute:** Analyze diff → impact analysis → quality audit → test coverage check.
3. **Verify:** All call sites examined. Quality audit passed (or exceptions noted). Test evidence present.
4. **Output:** Findings grouped by risk, with a merge recommendation and rationale.
ationale.
nale.
