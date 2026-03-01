---
name: test-driven-development
version: 1.1.0
level: tactical
description: 'Use when implementing any feature or bugfix, before writing implementation code. Enforces the strict Red-Green-Refactor loop.'
category: engineering
tags: [engineering, testing, methodology]
references:
  - name: Isolate (Systematic Debugging)
    path: ../isolate-debugging/SKILL.md
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko/SKILL.md
---

# Test-Driven Development

Write the test first. Watch it fail. Write minimal code to pass. If you didn't watch the test fail, you don't know if it tests the right thing. Violating the letter of the rules is violating the spirit of the rules.

## Core Mandates

### 1. The Iron Law of TDD
- **Action:** You must write a failing test BEFORE writing any production code. No exceptions.
- **Constraint:** NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST. Do not write code and keep it as "reference" while writing tests. Delete it and start over.
- **Integration:** Aligns with **Isolate** debugging; a failing test is the ultimate reproducible minimal case.

### 2. Verify RED (Watch It Fail)
- **Action:** After writing the minimal test, you MUST run the test suite and confirm the test fails (not errors due to typos) because the feature is missing.
- **Constraint:** NEVER skip watching the test fail. If the test passes immediately, you are testing existing behavior. Fix the test.
- **AI Execution Constraint (Poka-yoke):** You MUST NOT write the test and the implementation in the same tool call or turn. You MUST output the `run_shell_command` test execution, observe the explicit failure log, and then write the implementation in a subsequent turn.
- **Integration:** A critical **Shisa Kanko** step: observe the specific failure message before attempting a fix.

### 3. GREEN and REFACTOR
- **Action:** Write the simplest, most minimal code to pass the test. Run the test to verify it passes. Then, refactor the code for cleanliness while keeping the test green.
- **Constraint:** Do not add extra features or guess future requirements while in the Green phase. YAGNI (You Aren't Gonna Need It).
- **Integration:** Refactoring connects to **Kodawari** (Craftsmanship).

### 4. 5S Test Organization (Seiton / Set in Order)
- **Action:** Tests must be permanently stored as regression assets, but they MUST NOT pollute the project root.
- **Constraint:** After the initial Red/Green loop, relocate the test file into the target component's folder (e.g., `skills/<skill_name>/scripts/` or `skills/<skill_name>/tests/`).
- **Integration:** Directly applies the Lean **5S** concept of sorting and setting in order, preventing digital workspace bloat.

## Escalation & Halting

- **Jidoka:** If a test errors out instead of failing cleanly, halt and fix the test setup before writing implementation code.
- **Hō-Ren-Sō:** Communicate test failures clearly to the user during the Red phase to ensure alignment on expected behavior.

## Implementation Workflow

1. **Trigger:** Starting a new feature, bug fix, or behavior change.
2. **Execute:** Write a failing test. Run it. Observe the failure. Write minimal code to pass. Run it. Observe the pass. Refactor.
3. **Verify:** The test suite must be fully green after the Refactor phase.
4. **Output:** A completed, tested, and cleanly refactored unit of code, documented using the Poka-yoke Output Template.

## Poka-yoke Output Template

When a TDD cycle is complete, the agent MUST output the final verification using exactly the schema defined in the Poka-yoke Output Template.

👉 **[TDD Cycle Verification Template](templates/poka-yoke-output.md)**

