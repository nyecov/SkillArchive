---
name: ho-ren-so
version: 1.2.0
level: methodology
description: Use when reporting progress, broadcasting state changes, or escalating ambiguous or blocked decisions to a human operator. Handles structured reporting, factual notifications, and consultation-with-options formats.
category: methodology
tags:
- communication
- methodology
- lean
- TPS
references:
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Jidoka (Autonomation)
  path: ../jidoka/SKILL.md
- name: Poka-yoke (Mistake-proofing)
  path: ../poka-yoke/SKILL.md
- name: Hansei (Self-reflection)
  path: ../hansei/SKILL.md
- name: KYT (Hazard Prediction)
  path: ../kyt/SKILL.md
- name: Kaizen (Continuous Improvement)
  path: ../kaizen/SKILL.md
- name: Lean Foundations
  path: ../lean-foundations/SKILL.md
- name: Value Stream Mapping (VSM)
  path: ../vsm/SKILL.md
---

# Hō-Ren-Sō

Hō-Ren-Sō ensures that information flows smoothly across the system, preventing silos and ambiguity. In an agentic architecture, it provides the structured formats for routine operational updates and critical safety escalations.

## Core Mandates

### 1. Hōkoku (Structured Reporting)
Report progress, results, and successful verifications to the user in a brief, factual, and chronological format.
- **Action:** Summarize the outcome of a task, including the specific changes made and the validation results.
- **Constraint:** DO NOT provide generic "I'm done" messages. Always include the evidence of success.
- **Integration:** Triggered at the completion of **Shisa Kanko** Phase D (Verification).

### 2. Renraku (Factual Contact)
Inform the user and sub-agents of environmental changes or system state facts without bias or opinion.
- **Action:** Broadcast that a **Poka-yoke** interlock has been engaged or a **KYT** countermeasure has been applied.
- **Constraint:** Avoid providing "opinions" during Renraku; report only the verifiable facts of the system state.
- **Integration:** Directly communicates the engagement of **Poka-yoke** constraints or **KYT** action targets.

### 3. Sōdan (Decision Consultation)
Seek authorization or a decision when encountering an ambiguous, blocked, or high-risk situation.
- **Action:** Present the problem, the **Hansei** root-cause analysis, and a set of actionable options for the user.
- **Constraint:** Never format a Sōdan request like a routine Hōkoku update. You MUST use the following explicit format:
  - **[HALT REASON]:** The specific contradiction, ambiguity, or failure.
  - **[ROOT CAUSE]:** The Hansei reflection on why it occurred.
  - **[OPTIONS]:** A numbered list of mutually exclusive paths forward.
- **Integration:** Acts as the communication vehicle for **Jidoka** halts and trips.

## Escalation & Halting

- **Jidoka:** This skill *is* the escalation mechanism for Jidoka. If a Sōdan request is ignored or if ambiguity persists, remain in a halted state.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol whenever a "Point of No Return" identified by **KYT** is reached.

## Implementation Workflow

1. **Trigger:** The agent completes a task phase, encounters a state change, or hits an ambiguity/blocker requiring a Jidoka halt.
2. **Execute:** Select the appropriate tier (Hōkoku for status, Renraku for facts, Sōdan for consultation). If Sōdan, strictly apply the formatted template constraint.
3. **Verify:** Ensure the message does not spam the operator with redundant information and clearly differentiates between a status log and a request for action.
4. **Output:** A formatted message delivered to the user via the `notify_user` tool or equivalent output channel.
