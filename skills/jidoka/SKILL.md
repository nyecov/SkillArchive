---
name: jidoka
version: 1.1.0
level: safety
description: Use when an abnormality, error, or validation failure occurs. Mandates
  an autonomous halt and root-cause analysis.
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
- name: Lean Principles (Muda Eradication)
  path: ../muda/SKILL.md
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

### 2. Clear Signaling (The Andon Signal)
When an abnormality is detected, the agent MUST clearly signal the failure before halting.
- **Action:** Clearly state the **Abnormality** (the error), the **Location** (the file/line/tool), and the **Hypothesis** (why it happened).
- **Constraint:** NEVER silently fail or provide vague error reports. Use the `cc-isolate-debugging` pattern to provide a high-signal failure report.

### 3. Autonomous Halt (The Brake)
Immediately stop all execution upon signaling the abnormality.
- **Action:** DO NOT attempt to 'guess' a fix or 'hallucinate' a workaround.
- **State:** Freeze the current state. Prevent any further tool calls, API requests, or file writes.

### 3. Root Cause Analysis (Hansei)
Before escalating, the agent must attempt to understand *why* the halt occurred.
- **Action:** Initiate a **Hansei (Self-reflection)** cycle. Was the error caused by ambiguous instructions, missing context, or a failed external dependency? 
- **Goal:** Transform a generic error into a specific, actionable diagnostic.

### 4. Human Escalation (Hō-Ren-Sō)
Transition from autonomous mode to human-in-the-loop 'Consultation' mode.
- **Action:** Use the **Sōdan (Consult)** protocol from **Hō-Ren-Sō** to alert the operator.
- **Provide a Diagnostic Report:**
  - **Renraku (Fact):** What specific abnormality triggered the halt (e.g., "Poka-yoke validation failed on Tool X").
  - **Hansei (Reflection):** The root cause analysis (e.g., "The provided file path did not match the actual directory structure").
  - **Sōdan (Consultation):** Proposed paths for the human to resume, correct the context, or abort the operation entirely.

## Escalation & Halting

- **Jidoka:** This skill *is* the primary halting mechanism. It triggers when any abnormality or interlock breach is detected.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol immediately after an autonomous halt to provide the diagnostic report to the user.

## Implementation Workflow

1. **Monitor:** Run a validation check after every internal reasoning step.
2. **Detect:** If an interlock trips or an abnormality is detected, trigger the HALT protocol.
3. **Reflect:** Run Hansei to determine the root cause.
4. **Escalate:** Format the diagnostic report using Hō-Ren-Sō principles and wait for human input before proceeding.
