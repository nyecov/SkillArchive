---
name: Comprehend (The Understanding Gate)
version: 1.0.0
description: A 4-level comprehension gate that prevents users from extending, debugging, or shipping code they cannot explain. Enforces understanding as a prerequisite to action.
category: cognition
tags: [comprehend, understanding, explanation, comprehension-debt, crowd-control]
references:
  - name: Crowd Control (Source Repo)
    url: https://github.com/newsbubbles/crowd_control
  - name: CC — Deglaze (Anti-Sycophancy)
    path: ./cc-deglaze-anti-sycophancy.md
  - name: CC — Anchor (Architectural Coherence)
    path: ./cc-anchor-coherence.md
  - name: CC — Circuit (Iteration Breaker)
    path: ./cc-circuit-iteration-breaker.md
  - name: CC — Isolate (Systematic Debugging)
    path: ./cc-isolate-debugging.md
  - name: CC — Secure (Security)
    path: ./cc-secure-security.md
  - name: CC — Ship (Production Readiness)
    path: ./cc-ship-production.md
  - name: Hansei (Self-reflection)
    path: ./hansei-self-reflection.md
---

# Comprehend: The Understanding Gate

*You can't fix what you can't explain. You can't extend what you don't understand.*

Every piece of code the user doesn't understand is **comprehension debt**. Unlike technical debt, you can't refactor your way out of it — you have to actually learn. This skill gates forward progress on demonstrated understanding.

## Core Mandates: The 4-Level Protocol

### Level 1: What Does It Do?
- **The test:** "Walk me through what happens when [trigger event] occurs."
- **Passing:** Step-by-step trace through the code path, identification of key decision points, awareness of data transformations.
- **Failing:** "It handles the [thing]", vague gestures at functionality, "The AI set that up."

### Level 2: Why This Approach?
- **The test:** "Why did you choose [pattern/library/structure] over alternatives?"
- **Passing:** Articulation of tradeoffs, awareness of alternatives considered, understanding of constraints that drove the decision.
- **Failing:** "The AI suggested it", "It's best practice" (without knowing why), "I don't know, but it works."

### Level 3: Where Are The Edges?
- **The test:** "What inputs would make this behave unexpectedly?"
- **Passing:** Identification of boundary conditions, awareness of error states, understanding of assumptions baked in.
- **Failing:** "It should handle everything", "I tested the happy path", blank stare.
- **Integration:** Maps directly to **KYT (Hazard Prediction)** Round 1 — edge cases are hazards.

### Level 4: How Does It Connect?
- **The test:** "How does this interact with [adjacent system/component]?"
- **Passing:** Clear articulation of interfaces, understanding of data contracts, awareness of coupling points.
- **Failing:** "It just calls the API", "That part was already there", confusion about boundaries.

## The Rubber Duck Escalation

When a user fails 2+ comprehension levels, escalate to rubber duck mode:

1. **Stop all implementation.**
2. **Ask them to explain the entire flow** from user action to system response.
3. **Note where they get stuck or vague** — those are the comprehension gaps.
4. **Fill gaps before proceeding.**

## When to Enforce Comprehend

**Hard enforcement** (stop and verify):
- Before debugging a failure
- Before extending existing functionality
- Before touching auth/security code
- When user says "I don't know why this works"
- When user says "the AI wrote this part"

**Soft enforcement** (check but proceed):
- Simple CRUD operations
- Well-established patterns
- User has demonstrated prior understanding
- Isolated changes with clear boundaries

## Implementation Workflow

1. **Trigger:** User requests a change or encounters a failure.
2. **Gate:** Run the 4-level protocol on the relevant code area.
3. **Assess:** Failed gate → stop, explain, understand, then proceed.
4. **Escalate:** 2+ failed gates → rubber duck mode. Feed findings into **Hansei** for reflection on why the gap exists.

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
