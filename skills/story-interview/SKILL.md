---
name: story-interview
version: 1.0.0
level: methodology
description: 'Use when a user requests feature scoping, requirements definition, or
  wants to plan a new development story, bugfix, or idea. Applies Socratic questioning
  and Deglaze constraint pressure to eliminate waste and verify logic before implementation.'
category: methodology
tags:
- methodology
- lean
- cognition
references:
- name: Deglaze Tactics (Constraint Pressure)
  path: ../deglaze-tactics/SKILL.md
- name: Lean Foundations (Waste Elimination)
  path: ../lean-foundations/SKILL.md
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Ho-Ren-So (Communication)
  path: ../ho-ren-so/SKILL.md
- name: Test-Driven Development
  path: ../test-driven-development/SKILL.md
requires:
- deglaze-tactics
---

# Development Story Interview

This skill codifies the procedure for extracting, challenging, and solidifying user requirements into a robust development story through structured interrogation. Grounded in Lean principles, it actively combats "glaze" (superficial understanding) and Muda (waste from building the wrong thing) by forcing ideas into hard, verifiable edges before any code is written or documents are finalized.

## Core Mandates

### 1. Interrogative Definition (Socratic Verification)
Treat every user proposal as a hypothesis. Shift the burden of proof to the user by asking critical, targeted questions about edge cases, failure states, and core value.
- **Action:** Ask 1–2 specific, challenging questions per turn. Target sad paths ("What happens if X fails?"), scope boundaries ("Can we remove Y and still get value?"), and security implications.
- **Constraint:** Do NOT accept a requirement that lacks verifiable acceptance criteria. A requirement without a test condition is not a requirement — it is a wish.
- **Integration:** Utilizes **Deglaze Tactics** (Compression, Deletion, Adversary tests) to strip assumptions and jargon from proposals.

### 2. Waste Eradication (Muda Prevention)
Ensure the proposed story delivers value and is not bloated with speculative features.
- **Action:** For every proposed feature, ask: "What is the minimum version of this that solves the problem?" If a feature cannot be justified by an immediate user need, flag it for removal.
- **Constraint:** NEVER scope features that aren't strictly required to solve the stated problem. "Just-in-case" features are Over-processing waste.
- **Integration:** Directly implements **Lean Foundations** Muda elimination principles.

### 3. Iterative Refinement
Build the requirement incrementally through back-and-forth dialogue until both parties are completely satisfied with the logic and behavior.
- **Action:** After each answer, validate the user's statements, point out remaining rough spots, and tighten one edge at a time. Summarize confirmed points to prevent regression.
- **Constraint:** Do NOT format the final development document until explicit consensus is reached that all edges are sharp and the logic is watertight.
- **Integration:** Establishes a verified baseline before moving to execution or formal planning phases.

### 4. Standardized Output (Development Document)
Once consensus is reached, serialize the agreed-upon requirements into a clear, actionable format.
- **Action:** Generate a Development Document containing:
  1. **Title** — Concise story name
  2. **User Value (Why)** — The problem being solved and for whom
  3. **Core Logic (How)** — The technical approach agreed upon
  4. **Edge Cases & Constraints** — Every sad path and boundary identified during the interview
  5. **Verification Criteria** — Concrete, testable acceptance conditions
- **Constraint:** The final document MUST only contain what was verified in the interview. No embellishment, no assumed features.
- **Integration:** Serves as the direct input for **Test-Driven Development** and **Shisa Kanko** execution.

## Escalation & Halting

- **Jidoka:** If the user's requirements remain logically inconsistent after 3 rounds of focused questioning on the same contradiction, halt the interview. State the exact contradiction preventing progression and request the user to resolve the conflict before continuing.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to propose a smaller, simpler MVP if the requested story is too complex to define in a single session. Present the reduced scope as a concrete option, not a vague suggestion.

## Implementation Workflow

1. **Trigger:** The user requests a development story, feature scoping, requirement definition, or asks to plan a new idea.
2. **Execute:**
   - Ask the user to state their core goal in one sentence.
   - Apply Deglaze questions iteratively: probe failure states, identify removable scope, challenge assumptions. Limit to 1–2 questions per turn.
   - After each answer, summarize what is confirmed and what remains open.
3. **Verify:** Confirm with the user that all identified rough spots are resolved and every requirement has a testable acceptance condition.
4. **Output:** Format the final Development Document and present it for user sign-off.

## Quick Reference

```
INTERVIEW READINESS CHECKLIST:
□ Core goal stated in one sentence?
□ User value (who benefits and why) defined?
□ All sad paths / failure states identified?
□ Every "nice-to-have" challenged and justified or removed?
□ Each requirement has a testable acceptance condition?
□ No logical contradictions remain?

If 2+ boxes unchecked → continue interview
All boxes checked     → format Development Document
```
