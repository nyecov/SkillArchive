---
name: jidoka
version: 1.2.0
level: safety
description: Use when an abnormality, error, validation failure, or workflow loop occurs. Mandates an autonomous halt and root-cause analysis.
category: safety
tags:
- methodology
- safety
references:
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Poka-yoke (Mistake-proofing)
  path: ../poka-yoke/SKILL.md
- name: Hansei (Self-reflection)
  path: ../hansei/SKILL.md
- name: KYT (Hazard Prediction)
  path: ../kyt/SKILL.md
- name: Hō-Ren-Sō (Communication)
  path: ../ho-ren-so/SKILL.md
- name: Kaizen (Continuous Improvement)
  path: ../kaizen/SKILL.md
- name: Lean Foundations (Mura, Muri, Muda)
  path: ../lean-foundations/SKILL.md
- name: Value Stream Mapping (VSM)
  path: ../vsm/SKILL.md
requires:
- hansei
---

# Jidoka: Autonomation for AI Agents (The Andon Cord)

Jidoka ensures that AI agents do not produce 'defects' (hallucinations or incorrect actions) by empowering them to stop and alert a human when an abnormality is detected. It is the ultimate emergency brake in an agentic workflow, acting as the fail-safe when **Poka-yoke** constraints are breached or **KYT** protocols fail.

In practice, this is implemented as the **Andon Cord**: a visual and verbal signal that "Stops the Line" to prevent the compounding of errors.

## Core Mandates

### 1. Abnormality Detection (The Sensor)
The agent MUST continuously monitor its own state, inputs, and outputs for 'anomalous' patterns.
- **Criteria for Stopping:**
  - A **Poka-yoke (Mistake-proofing)** interlock is triggered (e.g., schema validation failure).
  - API responses deviate from the expected contract or return unexpected 5xx errors.
  - **Shisa Kanko Pointing Failure:** The target code snippet cannot be exactly matched.
  - A **KYT (Hazard Prediction)** pass identifies an unmitigable critical danger point.

### 2. Workflow Circuit Breaker (Threshold Monitoring)
Stop the line if the iteration loop becomes unproductive or destructive.
- **Criteria for Stopping:**
  - **Budget Exhaustion:** The same bug persists after 3-5 attempts.
  - **Debt Compounding:** The rate of new bugs/lint errors exceeds the rate of fixes.
  - **Time Overburden:** Spending 2+ hours on a single atomic issue.
- **Action:** Before suggesting "one more fix," trigger a circuit trip.
- **Options:** When tripped, the agent MUST offer exactly three paths: **Stop** (return later), **Revert** (last good state), or **Restart** (pivot strategy).

### 3. Clear Signaling (The Andon Signal)
When an abnormality is detected or a circuit is tripped, the agent MUST clearly signal the failure before halting.
- **Action:** State the **Abnormality**, the **Location**, and the **Hypothesis**.
- **Constraint:** NEVER silently fail or provide vague error reports.

### 4. Autonomous Halt & Root Cause (Hansei)
Immediately stop all execution and initiate a **Hansei (Self-reflection)** cycle.
- **Goal:** Determine if the error was caused by ambiguous instructions, missing context, or a failed external dependency.
- **Constraint:** Do not attempt to 'guess' a fix or 'hallucinate' a workaround during a halt.

### 5. Human Escalation (Hō-Ren-Sō)
Transition from autonomous mode to human-in-the-loop 'Consultation' mode.
- **Action:** Use the **Sōdan (Consult)** protocol to alert the operator.
- **Diagnostic Report:** Include the specific abnormality (Renraku), the root cause analysis (Hansei), and proposed paths forward (Sōdan).

## Escalation & Halting

- **Jidoka:** This skill *is* the primary halting mechanism. It triggers when any abnormality, interlock breach, or workflow threshold is hit.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol immediately after an autonomous halt to provide the diagnostic report to the user.

## Implementation Workflow

1. **Monitor:** Run validation checks and track iteration budgets after every tool call.
2. **Detect:** If an interlock trips, an iteration threshold is hit, or an abnormality is detected, trigger the HALT protocol.
3. **Reflect:** Run Hansei to determine the root cause.
4. **Escalate:** Format the diagnostic report using Hō-Ren-Sō principles and wait for human input before proceeding.
