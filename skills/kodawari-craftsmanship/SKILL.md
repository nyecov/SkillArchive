---
name: kodawari-craftsmanship
version: 1.1.0
level: methodology
category: methodology
description: 'Use during any code modification or creation task as an always-active operating principle. Mandates the relentless pursuit of perfection, enforcing the Boy Scout Rule and Architectural Harmony (Wa) without introducing scope creep.'
tags:
- design
- methodology
- lean
- TPS
references:
- name: Lean Foundations
  path: ../lean-foundations/SKILL.md
- name: Poka-yoke
  path: ../poka-yoke/SKILL.md
- name: Shisa Kanko
  path: ../shisa-kanko/SKILL.md
---

# Kodawari Craftsmanship

**Kodawari** is the relentless pursuit of perfection in one's craft. In the context of agentic software engineering, it acts as the primary immune system against entropy, technical debt, and "Hybrid Rot." It ensures that every modification leaves the code self-documenting, cleaner, and architecturally harmonious, strictly bounded to prevent scope creep.

## Core Mandates

### 1. Code-as-Documentation
The code MUST be so readable and intentional that it serves as its own primary documentation.
- **Action:** Use expressive naming, clear control flows, and concise abstractions.
- **Constraint:** Avoid "clever" hacks or obscure logic that requires external explanation.
- **Integration:** Binds to **Poka-yoke** to ensure readability is treated as a structural requirement, not an aesthetic preference.

### 2. The Boy Scout Rule (Strictly Bounded)
Every modification must leave the code cleaner than it was found, but ONLY within safe, verifiable boundaries.
- **Action:** Perform minor refactors (Seiso - Shine) on the surrounding code as you implement the primary task.
- **Constraint (Zero-Scope Interlock):** NEVER introduce new functional methods, external tool calls, or scope-creeping features during a Kodawari refactor. The code must do exactly what it did before.
- **Constraint (Test Coverage Prerequisite):** You are ONLY authorized to perform autonomous Boy Scout refactoring if the target code has existing verifiable test coverage to prove behavioral equivalence.
- **Integration:** Relies on **Shisa Kanko** for strict execution and verification of the primary task before attempting Shine operations.

### 3. Architectural Harmony (Wa)
Ensure that new code blends seamlessly with the existing system's patterns and standards.
- **Action:** Audit every change for "Wa" (Harmony). Does it look like it belongs in this codebase? Utilize deterministic formatters and linters automatically to enforce this before relying on subjective reasoning.
- **Constraint:** Reject any implementation that introduces "Hybrid Rot" (mixing incompatible patterns).

## Escalation & Halting

- **Jidoka (Andon Cord):** If a task requires violating "Wa", or if the Boy Scout rule is attempted on a file with zero test coverage, autonomous "Shine" operations MUST be halted. Execute ONLY the primary user request.
- **Hō-Ren-Sō (Legacy Batching):** When facing massive legacy code that wildly violates Wa (and lacks tests), invoke the Sōdan (Consult) protocol. Break the work into smaller chunks and interview the user case-by-case rather than attempting an autonomous massive rewrite.

## Implementation Workflow

1. **Trigger:** Activated autonomously during any code modification or creation task.
2. **Execute:** 
   - Verify the presence of test coverage before augmenting the scope with "Shine" refactoring.
   - Implement the primary change with clean logic and precise naming.
   - Run deterministic linters/formatters.
3. **Verify:** Perform a Shisa Kanko audit — Is the new logic verifiable? Does the surrounding code remain unchanged in functional capability?
4. **Output:** A high-integrity, harmonious addition to the codebase without scope creep.
