---
name: kodawari-craftsmanship
version: 1.0.0
description: 'Kodawari (Devoted Craftsmanship) for high-quality, self-documenting
  code. Mandates the relentless pursuit of perfection in the details, ensuring architectural
  harmony (Wa) and readability.

  '
category: methodology
level: methodology
tags:
- design
- methodology
references:
- name: Lean Foundations
  path: ../lean-foundations/SKILL.md
- name: Poka-yoke
  path: ../poka-yoke/SKILL.md
---

# Kodawari: Devoted Craftsmanship

**Kodawari** is the relentless pursuit of perfection in one's craft. In software engineering, this translates to a devotion to the details that make code readable, maintainable, and architecturally harmonious.

## Core Mandates

### 1. Code-as-Documentation
The code MUST be so readable and intentional that it serves as its own primary documentation.
- **Action:** Use expressive naming, clear control flows, and concise abstractions. 
- **Constraint:** Avoid "clever" hacks or obscure logic that requires external explanation.

### 2. The Boy Scout Rule
Every modification must leave the code cleaner than it was found.
- **Action:** Perform minor refactors (Seiso - Shine) on the surrounding code as you implement changes.
- **Constraint:** NEVER introduce "hacks" or temporary fixes that violate architectural standards.

### 3. Architectural Harmony (Wa)
Ensure that new code blends seamlessly with the existing system's patterns and standards.
- **Action:** Audit every change for "Wa" (Harmony). Does it look like it belongs in this codebase?
- **Constraint:** Reject any implementation that introduces "Hybrid Rot" (mixing incompatible patterns).

## Escalation & Halting

- **Jidoka:** If a task requires violating "Wa" or introducing significant technical debt to function, trigger a Jidoka halt.
- **Hō-Ren-Sō:** Use the Renraku (Fact) protocol to report significant refactors or "Shine" operations to the user.

## Implementation Workflow

1. **Trigger:** Every code modification or creation task.
2. **Execute:** Implement with Kodawari discipline (Clean logic, Precise naming, Architectural alignment).
3. **Verify:** Perform a "Kodawari Audit" — Is the code self-documenting? Does it improve the surroundings?
4. **Output:** A high-integrity, harmonious addition to the codebase.
