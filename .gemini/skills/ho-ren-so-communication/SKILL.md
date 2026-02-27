---
name: ho-ren-so-communication
version: 1.1.0
description: >
  Use when reporting progress, broadcasting state changes, or escalating ambiguous or blocked decisions to a human operator.
  Handles structured reporting, factual notifications, and consultation-with-options formats.
category: communication
tags: [ho-ren-so, collaboration, hitl, reporting, coordination, lean]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko-vibecoding/SKILL.md
  - name: Jidoka (Autonomation)
    path: ../jidoka-autonomation/SKILL.md
  - name: Poka-yoke (Mistake-proofing)
    path: ../poka-yoke-mistake-proofing/SKILL.md
  - name: Hansei (Self-reflection)
    path: ../hansei-self-reflection/SKILL.md
  - name: KYT (Hazard Prediction)
    path: ../kyt-hazard-prediction/SKILL.md
  - name: Kaizen (Continuous Improvement)
    path: ../kaizen-continuous-improvement/SKILL.md
  - name: Lean Principles (Muda Eradication)
    path: ../lean-principles-muda/SKILL.md
  - name: Value Stream Mapping (VSM)
    path: ../vsm-value-stream-mapping/SKILL.md
---

# Hō-Ren-Sō: Communication Standard for Agents

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
- **Constraint:** NEVER silently fail. Every **Jidoka** halt MUST be accompanied by a Sōdan request.
- **Integration:** Acts as the communication vehicle for **Jidoka** halts and **Circuit Breaker** trips.

## Escalation & Halting

- **Jidoka:** This skill *is* the escalation mechanism for Jidoka. If a Sōdan request is ignored or if ambiguity persists, remain in a halted state.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol whenever a "Point of No Return" identified by **KYT** is reached.

## Implementation Workflow

1. **State Tracking:** Maintain a clear log of what has been reported (Hōkoku) and shared (Renraku) to prevent spamming the operator.
2. **Ambiguity & Block Trigger:** If a decision branch has >1 viable path, or if a Jidoka halt is triggered, immediately switch to the Sōdan (Consultation) protocol.
3. **Structured Escalation:** When consulting, always present the problem (the Poka-yoke violation or KYT hazard), the Hansei reflection, and proposed options for the human to choose from.
4. **Feedback Integration:** Incorporate human advice into the current state and resume the workflow.
