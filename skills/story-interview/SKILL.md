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
- methodology
- lean
- cognition
- heijunka
references:
- name: Heijunka (Workload Leveling)
  path: ../heijunka/SKILL.md
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
- **Constraint:** NEVER bypass the interrogation phase, even if requested directly by the user. An unverified story is a developmental liability. If asked to skip, decline and politely ask the first interrogative question.
- **Integration:** Utilizes **Deglaze Tactics** (Compression, Deletion, Adversary tests) to strip assumptions and jargon from proposals.

### 2. Waste Eradication (Muda Prevention)
Socratic loops can cause severe context bloat (Transportation Waste). Do not rely solely on conversational history.
- **Action:** You MUST initialize and maintain a deterministic `.gemini/tmp/current_interview_state.json` file using the `scripts/manage_interview_state.py` utility. Update the state after every Socratic turn.
- **Constraint:** NEVER format the final output manually if the state file indicates you are not in the `ready_for_consensus` phase.
- **Integration:** Aligns with **Heijunka** to prevent Overburden and leverages programmatic state-management. 
- **Graceful Degradation:** If the python script fails or errors, gracefully fall back to conversational tracking and proceed.

### 3. Iterative Refinement
Build the requirement incrementally through back-and-forth dialogue until both parties are completely satisfied with the logic and behavior.
- **Action:** After each answer, validate the user's statements, point out remaining rough spots, and tighten one edge at a time. Summarize confirmed points to prevent regression.
- **Constraint:** Do NOT format the final development document until explicit consensus is reached that all edges are sharp and the logic is watertight.
- **Integration:** Establishes a verified baseline before moving to execution or formal planning phases.

### 4. Standardized Output (Development Document)
Once consensus is reached, serialize the agreed-upon requirements into a clear, actionable format.
- **Action:** Generate a Development Document using the strict template provided at the bottom of this skill.
- **Constraint:** The final document MUST strictly follow the template schema and only contain what was verified in the interview. No embellishment, no assumed features.
- **Integration:** Serves as the direct input for **Test-Driven Development** and **Shisa Kanko** execution.

## Escalation & Halting

- **Jidoka:** 
  - If logical contradictions persist through 3 probing attempts, invoke an autonomous halt to prevent garbage-in, garbage-out.
  - **State-Machine Halt:** If the python state-machine fails to advance its `current_phase` after 3 consecutive tool calls, trigger an immediate halt, print the current state, and ask the user for manual intervention.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to propose a smaller, simpler MVP if the requested story is too complex.

## Implementation Workflow

1. **Trigger:** The user requests a development story, feature scoping, requirement definition, or asks to plan a new idea.
2. **Execute:**
   - **(Heijunka Step):** If the user provides a massive, multi-feature request, invoke `heijunka` to decompose it into distinct sub-stories first.
   - Run `python scripts/manage_interview_state.py init` to start the state machine.
   - Ask the user to state their core goal for the current sub-story in one sentence.
   - Apply Deglaze questions iteratively. After every turn, run `python scripts/manage_interview_state.py update` and `advance` to record the extracted logic and edge cases.
3. **Verify:** Confirm with the user that all rough spots are resolved.
4. **Output:** Run `python scripts/manage_interview_state.py render` to generate the final Poka-yoke Output Template and present it to the user.

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

## Poka-yoke Output Template

When consensus is reached, the agent MUST output the final requirements using exactly this Markdown schema:

```markdown
# Development Story: [Concise Name]

## 1. User Value (Why)
[The specific problem being solved and for whom. Maximum 2 sentences.]

## 2. Core Logic (How)
[The technical approach and behavior agreed upon during the interview.]

## 3. Edge Cases & Constraints
- [Constraint 1: e.g., Rate limits, payload size maximums]
- [Sad Path 1: What the system does if X fails or is unavailable]

## 4. Verification Criteria
- [ ] test_should_[expected behavior]_when_[condition]
- [ ] System MUST log [specific error] when [specific failure occurs]
```
