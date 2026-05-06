---
id: 7e1f3a5c-9b2d-4e6f-8a0c-1d3f5b7e9a2d
name: agile-testing
version: 1.0.0
level: tactical
description: 'Use when authoring Test Plans (per Epic), Test Designs (per Story AC),
  or Test Executions with evidence. Handles UI, back-end, integration, and regression
  testing artifacts. TRIGGER when writing or updating test plans, designing test cases,
  logging executions, or tracing tests back to ACs. SKIP for unit-test-only TDD work.'
category: methodology
tags:
- agile
- testing
- methodology
- regression
- ui-testing
references:
  - name: Agile Backlog Authoring
    path: ../agile-backlog/SKILL.md
  - name: Test-Driven Development (TDD)
    path: ../test-driven-development/SKILL.md
  - name: Agile SDLC Orchestrator
    path: ../agile-sdlc/SKILL.md
---
# Agile Testing Workflow

Provides a standardized framework for all testing activities. Ensures testing is strategic, traceable, and comprehensive — separate from unit-level TDD work.

## Artifact Hierarchy (Hard Constraint)

No test artifact may exist without its immediate parent.

1. **Test Plan (TP)** — Overarching strategy for an Epic or Initiative.
2. **Test Set (TS)** — Logical grouping of tests. MUST have a parent Test Plan.
3. **Test Design (TD)** — Scenarios derived from Story ACs. MUST have a parent Test Set.
4. **Test Case (TC)** — Scoped to a single AC. MUST have a parent Test Design.
5. **Test Execution (TX)** — Record of running a Design/Case with evidence. MUST have a parent TD or TC.

A Story is many-to-many with both Test Designs and Test Plans. A Story may have multiple TDs (functional, UI, regression, performance) across multiple Test Sets.

## Core Mandates

### 1. Regression is Non-Negotiable
- **Action:** Every story deployment requires a regression execution. Every epic release requires the full regression suite. CI/CD pipeline MUST fail if regression fails.
- **Constraint:** No release without a passing TX artifact with attached evidence. No exceptions.
- **Integration:** Enforced as a hard gate in `agile-release-gate`.

### 2. UI Testing is Mandatory for UI-Representation Stories
- **Action:** Any story with UI labels, UI components, or UI citations MUST have at least one Test Design that exercises actual browser/UI behavior — not auto-generated boilerplate. Every TX for a UI story MUST include a `## Evidence` block with a screenshot or recording.
- **Constraint:** A unit-test-only TX is insufficient for a UI story. A passing unit suite while the user-visible feature is broken is a P0 incident.
- **Integration:** Failing UI test MUST be written before any production-code fix (per `test-driven-development` Red phase).

### 3. Bidirectional Traceability
- **Action:** Every Test Design must declare a `Covers AC` link targeting a specific AC in a specific Story. The Story must list the TD in its `## Linked Test Design(s)` section. Both directions are mandatory.
- **Constraint:** One-way links are invalid. `coverage.py validate-tests` fails closed on broken bidirectional links.
- **Integration:** Required for `agile-release-gate` pre-release audit.

### 4. Testers Are Active Issue Producers
- **Action:** File an ISSUE via `New-Issue.ps1` whenever: an AC cannot become a test design without unstated assumptions (→ Analyst); a test would need behavior not covered by any AC (→ PO); a cross-story regression is implied (→ Architect); a test environment dependency is missing (→ DevOps).
- **Constraint:** Run `Triage-Issues.ps1 -Open` at the start of every test review cycle to avoid filing duplicates.
- **Integration:** Connects to `agile-backlog` Issue routing matrix.

## Escalation & Halting

- **Jidoka:** If a UI-representation story has no REAL_UI Test Design, or a TX has no evidence block, halt release sign-off.
- **Ho-Ren-So:** Surface any test environment blockers or AC ambiguities as ISSUE artifacts before marking a story as `In Test`.

## Implementation Workflow

1. **Trigger:** Starting a new Epic (create Test Plan), beginning a Story (create Test Design per AC), or running tests (create Test Execution with evidence).
2. **Execute:** Grep existing tests first. Use templates. Author TDs that map directly to ACs. Run tests and record TX with evidence.
3. **Verify:** Bidirectional Story↔TD links valid. TX has evidence block. Regression suite passes for release-scoped items.
4. **Output:** A complete, evidence-backed test portfolio traceable from ACs to TX artifacts, ready for `agile-release-gate` sign-off.
sign-off.
