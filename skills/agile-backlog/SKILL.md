---
id: 5c9d2e4f-1a7b-4c8e-9d3f-6b0a5e2c8d4f
name: agile-backlog
version: 1.0.0
level: tactical
description: 'Use when creating, editing, refining, or reviewing Agile artifacts: Initiatives,
  Epics, User Stories, Subtasks, Issues, or Bugs. Enforces strict hierarchy, canonical
  ID grammar, and BDD acceptance criteria. SKIP for ad-hoc TODOs, PR descriptions,
  or commit messages.'
category: methodology
tags:
- agile
- backlog
- methodology
- stories
- artifacts
references:
  - name: Agile SDLC Orchestrator
    path: ../agile-sdlc/SKILL.md
  - name: Agile Testing
    path: ../agile-testing/SKILL.md
  - name: Spec Mapping
    path: ../spec-mapping/SKILL.md
---
# Agile Backlog Authoring

Enforces a standardized anatomy for all Agile hierarchy levels. Ensures strategic goals are properly decomposed into actionable, user-centric deliverables with strict parentage and traceability.

## Artifact Hierarchy (Hard Constraint)

No artifact may exist without its immediate parent.

1. **Initiative** — High-level strategic objective. Top of chain.
2. **Epic** — Body of work achieving a specific goal. MUST have a parent Initiative.
3. **User Story** — Delivers concrete user value. MUST have a parent Epic.
4. **Subtask** — Granular technical step. MUST have a parent Story.
5. **Issue** — Cross-cutting blocker or spec ambiguity. Flat-namespaced; lists affected artifacts.
6. **Bug** — Defect where implementation diverges from a documented AC. Distinct from Issue.

## Core Mandates

### 1. Grep Before Drafting
- **Action:** Search the backlog for overlapping epics, stories, or subtasks before creating anything new. Prefer extending an existing artifact (adding ACs or subtasks) over creating a duplicate.
- **Constraint:** Do not create a new story if an existing one covers 80%+ of the same scope. Merge overlap instead.
- **Integration:** Implements the **Lean Foundations** "eliminate Muda" principle at the artifact level.

### 2. Anatomy Compliance
- **Action:** Every artifact must have all required fields from its template: parent link, title, status, description, and acceptance criteria. Stories use "As a... I want... so that..." format with BDD (Given/When/Then) ACs.
- **Constraint:** No artifact is valid without its required fields. Anatomy is enforced by `Validate-AgileHierarchy.ps1` before every commit.
- **Integration:** Connects to **Poka-yoke** — structural validation as a mistake-proofing gate.

### 3. Status Vocabulary Discipline
- **Action:** Use only canonical status values. Story lifecycle: `Backlog → Needs Refinement → In Design → Ready for Development → In Progress → Testable → In Test → Done`. Lateral: `Blocked (by <TICKET-ID>)` (ticket ID required), `To Be Reviewed:<Code|Story|Design|Test|Spec>`, `Cancelled`, `Deprecated`.
- **Constraint:** Never use bare `Blocked` without a ticket ID. Never invent parallel status values.
- **Integration:** Single source of truth prevents **Mura** (unevenness) in workflow state.

### 4. Bidirectional Traceability
- **Action:** Every story must link to its parent epic. Every subtask must link to its parent story. Every Issue/Bug must list the affected artifacts in an `## Affects` section. Backlinks are mandatory — no one-way links.
- **Constraint:** Broken links fail `Validate-AgileHierarchy.ps1`. Fix before commit.
- **Integration:** Enables end-to-end traceability required by `agile-release-gate`.

## Verification Tooling

After authoring or editing artifacts, run before closing the turn:

- `Validate-AgileHierarchy.ps1` — parent/child link integrity and ID grammar.
- `Export-BacklogSummary.ps1` — generate a full backlog markdown report.
- `Search-AllArtifacts.ps1` — search across all markdown artifacts for keywords or duplicates.
- `Triage-Issues.ps1 -Open` — surface active blockers before starting a development turn.
- `New-Issue.ps1` — create a properly routed ISSUE artifact when a blocker is discovered.
- `New-AgileArtifact.ps1` — scaffold a new artifact from the correct template with auto-increment IDs.

## Escalation & Halting

- **Jidoka:** If hierarchy validation fails, halt the commit and fix broken links before proceeding.
- **Ho-Ren-So:** File an ISSUE artifact and route to the appropriate owner (Analyst, Architect, PO, etc.) when a blocker cannot be resolved within the current turn.

## Implementation Workflow

1. **Trigger:** A user requests creation, refinement, or review of any backlog artifact.
2. **Execute:** Search for existing artifacts first. Use the appropriate template. Apply all required fields. Run anatomy verification.
3. **Verify:** `Validate-AgileHierarchy.ps1` exits 0. All parent and child links resolve.
4. **Output:** A valid, traceable backlog artifact committed via `Complete-AgileTurn.ps1`.
