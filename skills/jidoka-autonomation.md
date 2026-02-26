---
name: Jidoka (Autonomation)
version: 1.1.0
description: >
  Use when an abnormality, unexpected API response, or validation failure occurs during execution.
  Handles autonomous halt, root-cause analysis, and structured human escalation.
category: agent-safety
tags: [jidoka, lean, ai-safety, escalation, monitoring]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ./shisa-kanko-vibecoding.md
  - name: Poka-yoke (Mistake-proofing)
    path: ./poka-yoke-mistake-proofing.md
  - name: Hansei (Self-reflection)
    path: ./hansei-self-reflection.md
  - name: KYT (Hazard Prediction)
    path: ./kyt-hazard-prediction.md
  - name: Hō-Ren-Sō (Communication)
    path: ./ho-ren-so-communication.md
  - name: Kaizen (Continuous Improvement)
    path: ./kaizen-continuous-improvement.md
  - name: Lean Principles (Muda Eradication)
    path: ./lean-principles-muda.md
  - name: Value Stream Mapping (VSM)
    path: ./vsm-value-stream-mapping.md
---

# Jidoka: Autonomation for AI Agents

Jidoka ensures that AI agents do not produce 'defects' (hallucinations or incorrect actions) by empowering them to stop and alert a human when an abnormality is detected. It is the ultimate emergency brake in an agentic workflow, acting as the fail-safe when **Poka-yoke** constraints are breached or **KYT** protocols fail.

## Core Mandates

### 1. Abnormality Detection (The Sensor)
The agent MUST continuously monitor its own state, inputs, and outputs for 'anomalous' patterns.
- **Criteria for Stopping:**
  - A **Poka-yoke (Mistake-proofing)** interlock is triggered (e.g., schema validation failure).
  - API responses deviate from the expected contract or return unexpected 5xx errors.
  - **Shisa Kanko Pointing Failure:** The target code snippet cannot be exactly matched.
  - A **KYT (Hazard Prediction)** pass identifies an unmitigable critical danger point.

### 2. Autonomous Halt (The Brake)
When an abnormality is detected, the agent MUST immediately stop all execution.
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

## Implementation Workflow

1. **Monitor:** Run a validation check after every internal reasoning step.
2. **Detect:** If an interlock trips or an abnormality is detected, trigger the HALT protocol.
3. **Reflect:** Run Hansei to determine the root cause.
4. **Escalate:** Format the diagnostic report using Hō-Ren-Sō principles and wait for human input before proceeding.
