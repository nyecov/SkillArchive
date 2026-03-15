---
id: f9b6e8a1-3c5d-4f7e-9a2b-8d1c6e4a2b3c
name: interview
version: 1.1.0
level: methodology
description: 'Use when a user requests feature scoping, requirement definition, or planning a new idea. Applies Socratic questioning and Deglaze constraint pressure. Dynamically leverages Context Engine memory if available, or gracefully degrades to local state tracking.'
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

### 2. Waste Eradication (Graceful Degradation)
Socratic loops can cause severe context bloat (Transportation Waste). Do not rely solely on conversational history.
- **Action (Primary):** Use the `context-engine` tiered memory tools (`log_session_finding`, `commit_ontology_edge`) to maintain the deterministic state of the interview. Record volatile notes using `log_session_finding` with the `phase: "planning"` parameter.
- **Action (Fallback):** If the `context-engine` tools return an error (e.g., "Not connected"), gracefully degrade by initializing and tracking the `[INTERVIEW_STATE]` in a local `.gemini/tmp/interview_state.json` file.
- **Constraint:** NEVER proceed to the next phase without ensuring the significant requirements from the current phase are recorded deterministically.
- **Integration:** Aligns with **Heijunka** to prevent Overburden and ensures universal availability.

### 3. Iterative Refinement
Build the requirement incrementally through back-and-forth dialogue until both parties are completely satisfied with the logic and behavior.
- **Action:** Regularly call `read_ontology_graph` to cross-reference current findings with historical patterns in the Ontology Graph.
- **Maturation:** Once a core requirement is verified, "Harden" it into the permanent Knowledge Graph by calling `commit_ontology_edge`.
- **Constraint:** Do NOT format the final development document until explicit consensus is reached that all edges are sharp and the logic is watertight.
- **Integration:** Establishes a verified baseline before moving to execution or formal planning phases.

### 4. Standardized Output (Development Document)
Once consensus is reached, serialize the agreed-upon requirements into a clear, actionable format.
- **Action:** Generate a Development Document using the strict template provided at the bottom of this skill, populating it from the gathered state findings.
- **Cleanup:** Execute `clear_session_state` after the document is finalized to minimize context window waste.
- **Constraint:** The final document MUST strictly follow the template schema and only contain what was verified. No embellishment, no assumed features.
- **Integration:** Serves as the direct input for **Test-Driven Development** and **Shisa Kanko** execution.

### 5. Kaizen Ingestion (Continuous Learning)
To ensure the system learns from structural logic debates, the core conflict of the interview must be permanently logged.
- **Action (Primary):** After the final Development Document is approved, summarize the session's defining insight into an architectural relationship and call `commit_ontology_edge`.
- **Action (Fallback):** If the `commit_ontology_edge` tool returns an error, log the relationship to the scratchpad using `log_session_finding`.

## Escalation & Halting

- **Jidoka:** 
  - If logical contradictions persist through 3 probing attempts, invoke an autonomous halt.
  - **Tool Failure:** If `context-engine` returns a "Parameter Missing" error (e.g., missing `phase`), immediately halt and correct the tool call parameters.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to propose a smaller, simpler MVP if the requested story is too complex.

## Implementation Workflow

1. **Trigger:** The user requests a development story or feature scoping.
2. **Execute:**
   - **(Initialize):** Call `clear_session_state`.
   - **(Recall):** Call `read_ontology_graph` to identify if this topic overlaps with existing system logic.
   - **(Interrogate):** Iterate logic. After every turn, update the Memory:
     - Use `commit_ontology_edge` for stable, verified insights.
     - Use `log_session_finding(phase: "planning")` for transient state notes.
   - **(Maturation):** For every finalized requirement, call `commit_ontology_edge(edge_type: "REQUIRES")`.
3. **Verify:** Confirm consensus on the final logic.
4. **Output:** Render the final **Story Template**.
5. **Pruning:** Call `clear_session_state` to reset the volatile buffer while retaining the stable database edits.

## Quick Reference

```
INTERVIEW READINESS CHECKLIST:
□ Core goal stated in one sentence?
□ Findings appended to Ontology Graph?
□ Stable requirements matured to Ontology Table?
□ All sad paths / failure states identified?
□ Each requirement has a testable acceptance condition?
□ Session state pruned after completion?

If 2+ boxes unchecked → continue interview
All boxes checked     → format Development Document
```

## Poka-yoke Output Template

When consensus is reached, the agent MUST output the final requirements using the standard schema:
[Story Template](./templates/story-template.md)
