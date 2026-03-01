---
name: comprehend-understanding
version: 1.1.0
description: Use before debugging, extending, or shipping code. Acts as a strict policy gate implementing Risk-Tiered comprehension checks (conversational vs. Deglaze reporting) to prevent cognitive debt.
category: cognition
tags:
- cognition
- safety
- routing
- methodology
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

# Comprehend

*You can't fix what you can't explain. You can't extend what you don't understand.*

Every piece of code the user or agent doesn't understand is **comprehension debt**. Unlike technical debt, you can't refactor your way out of it — you have to actually learn. This skill serves as the central **Policy Gate** for the system, routing verification effort based on the risk of the proposed action.

## Core Mandates

### 1. Risk-Tiered Comprehension Gating
Gate all forward progress on demonstrated understanding, scaling the verification friction to the risk of the task.
- **Tier 1 (Routine/Trivial):** Cleared via a conversational 4-level check (What, Why, Edge, Flow).
- **Tier 2 (High-Risk/Complex/Architectural):** Hard-locks the execution path. MUST route to **CC — Deglaze** to produce a formal `Deglaze Pressure Report`.
- **Constraint:** NEVER implement a feature on top of code that cannot pass its assigned tier of verification.

### 2. Debt Identification
Identify and "call out" comprehension debt early.
- **Action:** Flag phrases like "The AI wrote this," "I don't know why it works," or "Just run it and see" as critical risks.
- **Constraint:** Do not ignore comprehension gaps to maintain artificial "velocity."
- **Integration:** Feeds into **Hansei** to reflect on why understanding was lost.

### 3. Rubber Duck Escalation
When understanding fails, pivot from "Execution Mode" to "Teaching/Clarification Mode."
- **Action:** Use the "Rubber Duck" protocol: ask the user to explain the flow and fill the gaps.
- **Constraint:** Halt all file modifications until the comprehension debt is settled.

## Escalation & Halting

- **Jidoka:** If a user/agent fails verification at either Tier, trigger a Jidoka halt to address the cognitive debt.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to highlight specific understanding gaps and propose a "Deep Dive" before continuing.

## Implementation Workflow

1. **Trigger:** User requests a change, accepts AI-generated complex code, or encounters a failure.
2. **Evaluate:** Determine the Risk Tier of the proposed action (Tier 1 vs Tier 2).
3. **Execute:** 
    - If Tier 1: Run conversational 4-level check.
    - If Tier 2: Invoke `deglaze-tactics`.
4. **Verify:** Confirm the conversational check passes OR the `Deglaze Pressure Report` is fully populated.
5. **Output:** A de-risked implementation path where the human and agent definitively possess a shared, verified mental model.

## Quick Reference

```
RISK-TIER EVALUATION:
- Routine fix / 1-file change -> TIER 1
- New architecture / Multi-file refactor / Security logic -> TIER 2

TIER 1 GATES (Conversational):
□ Can trace execution path? (What)
□ Can explain why this approach? (Why)
□ Can identify edge cases? (Edge)
□ Can describe system connections? (Flow)

TIER 2 GATES (Hard-Lock):
■ MUST produce a formal Deglaze Pressure Report via deglaze-tactics.

RUBBER DUCK TRIGGER:
- Failed gates at either tier
- User/Agent says "I don't know"
```
