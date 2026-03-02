---
id: f9b6e8a1-3c5d-4f7e-9a2b-8d1c6e4a2b3c
name: story-interview-with-context-engine
version: 1.0.0
level: methodology
description: 'Use when a user requests feature scoping or requirement definition specifically requiring the Context Engine for deep codebase analysis. Applies Socratic questioning and Deglaze constraint pressure while leveraging Context Engine to eliminate waste.'
category: methodology
tags:
- methodology
- lean
- cognition
- heijunka
- context-engine
references:
- name: Heijunka (Workload Leveling)
  path: ../heijunka/SKILL.md
- name: Deglaze Tactics (Constraint Pressure)
  path: ../logic-deglazing/SKILL.md
- name: Lean Foundations (Waste Elimination)
  path: ../lean-foundations/SKILL.md
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Ho-Ren-So (Communication)
  path: ../ho-ren-so/SKILL.md
- name: Test-Driven Development
  path: ../test-driven-development/SKILL.md
- name: Context Engine (Core Logic)
  path: ../context-engine/SKILL.md
- name: Story Template
  path: ./templates/story-template.md
requires:
- logic-deglazing
- context-engine
---
# Development Story Interview (with Context Engine)

This skill codifies the procedure for extracting, challenging, and solidifying user requirements into a robust development story through structured interrogation, enhanced by the **Context Engine** for deep codebase comprehension. Grounded in Lean principles, it actively combats "glaze" (superficial understanding) and Muda (waste from building the wrong thing) by forcing ideas into hard, verifiable edges before any code is written or documents are finalized.

## Core Mandates

### 1. Interrogative Definition (Socratic Verification)
Treat every user proposal as a hypothesis. Shift the burden of proof to the user by asking critical, targeted questions about edge cases, failure states, and core value, cross-referencing with the Context Engine for architectural alignment.
- **Action:** Ask 1–2 specific, challenging questions per turn. Target sad paths ("What happens if X fails?"), scope boundaries ("Can we remove Y and still get value?"), and security implications.
- **Constraint:** Do NOT accept a requirement that lacks verifiable acceptance criteria. A requirement without a test condition is not a requirement — it is a wish.
- **Constraint:** NEVER bypass the interrogation phase, even if requested directly by the user. An unverified story is a developmental liability. If asked to skip, decline and politely ask the first interrogative question.
- **Integration:** Utilizes **Deglaze Tactics** (Compression, Deletion, Adversary tests) and **Context Engine** to strip assumptions and jargon from proposals.

### 2. Waste Eradication (Muda Prevention)
Socratic loops can cause severe context bloat (Transportation Waste). Do not rely solely on conversational history.
- **Action:** You MUST use the `context-engine` scratchpad to maintain the deterministic state of the interview.
- **Action (Creation):** Use `log_session_finding` to record the state after every Socratic turn using the header format: `[INTERVIEW_STATE] <Field>: <Value>`.
- **Constraint:** NEVER proceed to the next phase without ensuring the significant requirements from the current phase are recorded in the Context Engine session state.
- **Integration:** Aligns with **Heijunka** to prevent Overburden and leverages the **Context Engine** for persistent situational awareness.

### 3. Iterative Refinement
Build the requirement incrementally through back-and-forth dialogue until both parties are completely satisfied with the logic and behavior.
- **Action:** Use `read_session_state` to regain context if the window is flushed. Validate the user's statements, point out remaining rough spots, and tighten one edge at a time.
- **Constraint:** Do NOT format the final development document until explicit consensus is reached that all edges are sharp and the logic is watertight.
- **Integration:** Establishes a verified baseline before moving to execution or formal planning phases.

### 4. Standardized Output (Development Document)
Once consensus is reached, serialize the agreed-upon requirements into a clear, actionable format.
- **Action:** Generate a Development Document using the strict template provided at the bottom of this skill, populating it from the gathered **Context Engine** findings.
- **Constraint:** The final document MUST strictly follow the template schema and only contain what was verified. No embellishment, no assumed features.
- **Integration:** Serves as the direct input for **Test-Driven Development** and **Shisa Kanko** execution.

## Escalation & Halting

- **Jidoka:** 
  - If logical contradictions persist through 3 probing attempts, invoke an autonomous halt to prevent garbage-in, garbage-out.
  - **Memory Corruption:** If the `context-engine` is unresponsive or returns incoherent session state, run `powershell ./scripts/validate_infrastructure.ps1` in the `context-engine` directory.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to propose a smaller, simpler MVP if the requested story is too complex.

## Implementation Workflow

1. **Trigger:** The user requests a development story, feature scoping, requirement definition, or asks to plan a new idea, especially when deep codebase context is required.
2. **Execute:**
   - **(Heijunka Step):** If the user provides a massive, multi-feature request, invoke `heijunka` to decompose it into distinct sub-stories first.
   - **Initialize:** Run `clear_session_state` to ensure a fresh scratchpad for the new interview.
   - **Interrogate:** Ask the user to state their core goal in one sentence.
   - **Maturation:** Apply Deglaze questions iteratively. After every turn, update the session state:
     - `log_session_finding(finding="[INTERVIEW_STATE] Phase: <current_phase>")`
     - `log_session_finding(finding="[INTERVIEW_STATE] <Field>: <Value>")`
     - *Fields to track: StoryName, UserValue, CoreLogic, EdgeCases (list), VerificationCriteria (list).*
3. **Verify:** Confirm with the user that all rough spots are resolved.
4. **Output:** Execute `read_session_state`, synthesize the `[INTERVIEW_STATE]` findings, and render the final **Story Template**.

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

When consensus is reached, the agent MUST output the final requirements using the standard schema:
[Story Template](./templates/story-template.md)
