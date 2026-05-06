---
id: d7891a5d-453a-4584-aaf7-83746f441203
name: test-driven-development
version: 1.2.0
level: tactical
description: 'Use when implementing any feature or bugfix, before writing implementation code. Enforces the strict Red-Green-Refactor loop and auditable git commit conventions.'
category: engineering
tags: [engineering, testing, methodology, git]
references:
  - name: Isolate (Systematic Debugging)
    path: ../root-cause-isolation/SKILL.md
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko/SKILL.md
  - name: Agile Backlog Authoring
    path: ../agile-backlog/SKILL.md
  - name: Agile Testing
    path: ../agile-testing/SKILL.md
---
# Test-Driven Development (TDD)

Write the test first. Watch it fail. Write minimal code to pass. If you didn't watch the test fail, you don't know if it tests the right thing. This skill enforces the strict Red-Green-Refactor loop combined with auditable commit conventions and story checkpoint discipline.

## Core Mandates

### 1. The Iron Law of TDD
- **Action:** You must write a failing test BEFORE writing any production code. No exceptions.
- **Constraint:** NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST. Do not write code and keep it as "reference" while writing tests. Delete it and start over.
- **Integration:** Aligns with **Isolate** debugging; a failing test is the ultimate reproducible minimal case.

### 2. Verifiable Commit Conventions
Every TDD phase produces a separate commit with a structured prefix:

| Phase | Prefix | Allowed Changes |
|---|---|---|
| Red | `[Red] STORY-ID: <test description>` | Test files only. NO net-new production code. |
| Green | `[Green] STORY-ID: <implementation summary>` | Production code to make the Red test pass. Minimum required. |
| Refactor | `[Refactor] STORY-ID: <cleanup summary>` | Behavior-preserving cleanup. No new tests, no new behavior. |

**Other allowed prefixes:** `[Fix] BUG-ID: <summary>`, `[Meta]: <tooling/process change>`, `[Carving]: <spec mapping>`.

### 3. AI Execution Constraint (Poka-yoke)
- **Action:** You MUST NOT write the test and the implementation in the same tool call or turn. You MUST output the `run_shell_command` test execution, observe the explicit failure log (`[Red]`), and then write the implementation in a subsequent turn (`[Green]`).
- **Constraint:** NEVER skip watching the test fail. If the test passes immediately, you are testing existing behavior. Fix the test.
- **Integration:** A critical **Shisa Kanko** step: observe the specific failure message before attempting a fix.

### 4. Checkpoint Updates After Every Phase
- **Action:** After every Red, Green, or Refactor phase, update both the `Status` metadata field and the `## Checkpoint` block at the bottom of the Story file.
- **Constraint:** Checkpoint fields: `Phase` (Red|Green|Refactor|Done), `AC Coverage` (X/Y), `Last Updated`, `Notes` (one-sentence turn summary).
- **Integration:** Enables async handover — the next agent or session can resume exactly where this one left off.

### 5. 5S Test Organization (Seiton / Set in Order)
- **Action:** Tests must be permanently stored as regression assets, but they MUST NOT pollute the project root.
- **Constraint:** After the initial Red/Green loop, relocate the test file into the target component's folder (e.g., `skills/<skill_name>/tests/`).
- **Integration:** Directly applies the Lean **5S** concept, preventing digital workspace bloat.

### 6. Anti-Stall Protocol
- **Action:** If a TDD turn produces no new observable artifact (passing test, committed code, updated checkpoint) within a bounded number of attempts, halt and state the exact failure fingerprint.
- **Constraint:** Never loop indefinitely on the same failure. Identical failure fingerprints on two consecutive attempts trigger mandatory escalation.

## Escalation & Halting

- **Jidoka:** If a test errors out instead of failing cleanly, halt and fix the test setup before writing implementation code.
- **Hō-Ren-Sō:** Communicate test failures clearly to the user during the Red phase to ensure alignment on expected behavior.

## Implementation Workflow (End-of-Turn Protocol)

1. **Red Phase:** Write failing test. Run it. Observe failure. Commit as `[Red]`.
2. **Green Phase:** Write minimal code to pass. Run it. Observe pass. Commit as `[Green]`.
3. **Refactor Phase:** Clean up code while keeping tests green. Commit as `[Refactor]`.
4. **End-of-Turn:** Update Story Checkpoint, commit via `Complete-AgileTurn.ps1`, and report summary to user.

## Poka-yoke Output Template

When a TDD cycle is complete, the agent MUST output the final verification using exactly the schema defined in the Poka-yoke Output Template.

👉 **[TDD Cycle Verification Template](templates/poka-yoke-output.md)**


