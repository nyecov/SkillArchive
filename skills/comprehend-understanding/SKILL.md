---
name: comprehend-understanding
version: 1.0.0
description: 'Use before debugging, extending, or shipping code the user cannot explain.
  Handles 4-level comprehension gates, rubber duck escalation, and hard/soft enforcement
  modes.\'
category: cognition
tags:
- cognition
references:
- name: Crowd Control (Source Repo)
  url: https://github.com/newsbubbles/crowd_control
- name: CC — Deglaze (Anti-Sycophancy)
  path: ../deglaze-tactics/SKILL.md
- name: CC — Anchor (Architectural Coherence)
  path: ../anchor-coherence/SKILL.md
- name: CC — Circuit (Iteration Breaker)
  path: ../jidoka/SKILL.md
- name: CC — Isolate (Systematic Debugging)
  path: ../isolate-debugging/SKILL.md
- name: CC — Secure (Security)
  path: ../secure-security/SKILL.md
- name: CC — Ship (Production Readiness)
  path: ../ship-production/SKILL.md
- name: Hansei (Self-reflection)
  path: ../hansei/SKILL.md
level: methodology
---

# Comprehend: The Understanding Gate (Policy)

*You can't fix what you can't explain. You can't extend what you don't understand.*

Every piece of code the user doesn't understand is **comprehension debt**. Unlike technical debt, you can't refactor your way out of it — you have to actually learn. This skill serves as the **Policy Gate** for the system, mandating forward progress only on demonstrated understanding.

## Core Mandates

### 1. Comprehension Gating (The 4-Level Protocol)
Gate all forward progress on the user's demonstrated understanding of the current state.
- **Action:** Before execution, verify understanding across four levels: What (Trace), Why (Rationale), Edge (Hazards), and Flow (Coupling).
- **Constraint:** NEVER implement a feature on top of code the user cannot explain.
- **Integration:** This is a cognitive **Poka-yoke** — it prevents the "Magic Code" anti-pattern. Use the tactical pressure techniques in **CC — Deglaze** to perform the actual verification.

### 2. Debt Identification
Identify and "call out" comprehension debt early.
- **Action:** Flag phrases like "The AI wrote this" or "I don't know why it works" as critical risks.
- **Constraint:** Do not ignore comprehension gaps to maintain "velocity."
- **Integration:** Feeds into **Hansei** to reflect on why understanding was lost.

### 3. Rubber Duck Escalation
When understanding fails, pivot from "Execution Mode" to "Teaching/Clarification Mode."
- **Action:** Use the "Rubber Duck" protocol: ask the user to explain the entire flow and fill the gaps.
- **Constraint:** Stop all file modifications until the comprehension debt is settled.
- **Integration:** Connects to **Ho-Ren-So** to provide structured explanations of the system state.

## Escalation & Halting

- **Jidoka:** If a user fails 2+ comprehension levels, trigger a Jidoka halt to address the cognitive debt.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to highlight the specific comprehension gaps and propose a "Deep Dive" before continuing.

## Implementation Workflow

1. **Trigger:** User requests a change or encounters a failure.
2. **Execute:** Run the 4-level comprehension protocol.
3. **Verify:** Confirm the user can explain the logic, rationale, edges, and flow.
4. **Output:** A user who is "back in the driver's seat" and a de-risked implementation path.

## Quick Reference

```
COMPREHEND GATES:
□ Can trace execution path?
□ Can explain why this approach?
□ Can identify edge cases?
□ Can describe system connections?

Failed gate → Stop. Explain. Understand. Then proceed.

RUBBER DUCK TRIGGER:
- 2+ failed gates
- User says "I don't know"
- User blames AI for decisions
```
