---
name: Hō-Ren-Sō (Report, Contact, Consult)
version: 1.1.0
description: >
  Use when reporting progress, broadcasting state changes, or escalating ambiguous or blocked decisions to a human operator.
  Handles structured reporting, factual notifications, and consultation-with-options formats.
category: communication
tags: [ho-ren-so, collaboration, hitl, reporting, coordination, lean]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ./shisa-kanko-vibecoding.md
  - name: Jidoka (Autonomation)
    path: ./jidoka-autonomation.md
  - name: Poka-yoke (Mistake-proofing)
    path: ./poka-yoke-mistake-proofing.md
  - name: Hansei (Self-reflection)
    path: ./hansei-self-reflection.md
  - name: KYT (Hazard Prediction)
    path: ./kyt-hazard-prediction.md
  - name: Kaizen (Continuous Improvement)
    path: ./kaizen-continuous-improvement.md
  - name: Lean Principles (Muda Eradication)
    path: ./lean-principles-muda.md
  - name: Value Stream Mapping (VSM)
    path: ./vsm-value-stream-mapping.md
---

# Hō-Ren-Sō: Communication Standard for Agents

Hō-Ren-Sō ensures that information flows smoothly across the system, preventing silos and ambiguity. In an agentic architecture, it provides the structured formats for routine operational updates and critical safety escalations.

## The Three Pillars

### 1. Hōkoku (Report)
- **What:** Reporting progress, results, and successful verifications to the supervisor or human operator.
- **Format:** Brief, factual, and chronological.
- **Integration (Shisa Kanko):** Triggered at the successful completion of Phase D (Multi-Sensory Verification) in the **Shisa Kanko** master workflow. Summarizes what was changed and how it was verified.

### 2. Renraku (Contact)
- **What:** Informing peers, sub-agents, or stakeholders of facts without personal opinion or bias.
- **Format:** "Fact X has occurred. System State Y is now active."
- **Integration (Poka-yoke & KYT):** Used to broadcast environmental changes or when a **Poka-yoke** interlock is engaged. For example, broadcasting that a **KYT** countermeasure (like a database snapshot) has been successfully applied before execution.

### 3. Sōdan (Consult) - The Escalation Protocol
- **What:** Seeking advice, authorization, or a decision when encountering an ambiguous, blocked, or high-risk situation.
- **Format:** Must include Context, Root Cause, and Options.
- **Integration (Jidoka & Hansei):** This is the mandatory communication vehicle when a **Jidoka** halt occurs. The agent MUST NOT silently fail. The Sōdan request must include the results of a **Hansei (Self-reflection)** analysis so the human operator understands *why* the halt occurred and what paths are available to resolve it.

## Implementation Workflow

1. **State Tracking:** Maintain a clear log of what has been reported (Hōkoku) and shared (Renraku) to prevent spamming the operator.
2. **Ambiguity & Block Trigger:** If a decision branch has >1 viable path, or if a Jidoka halt is triggered, immediately switch to the Sōdan (Consultation) protocol.
3. **Structured Escalation:** When consulting, always present the problem (the Poka-yoke violation or KYT hazard), the Hansei reflection, and proposed options for the human to choose from.
4. **Feedback Integration:** Incorporate human advice into the current state and resume the workflow.
