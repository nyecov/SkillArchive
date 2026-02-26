---
name: Jidoka (Autonomation)
version: 1.0.0
description: Automation with a human touch. Enables AI agents to autonomously detect abnormalities, halt operations, and escalate to humans to prevent cascading errors.
category: agent-safety
tags: [jidoka, lean, ai-safety, escalation, monitoring]
---

# Jidoka: Autonomation for AI Agents

Jidoka ensures that AI agents do not produce 'defects' (hallucinations or incorrect actions) by empowering them to stop and alert a human when an abnormality is detected.

## Core Mandates

### 1. Abnormality Detection (The Sensor)
The agent MUST continuously monitor its own inputs and outputs for 'anomalous' patterns.
- **Criteria for Stopping:**
  - LLM confidence scores below a specific threshold.
  - API responses that deviate from the expected schema.
  - Contradictions between the 'Logic Declaration' and the 'Target Isolation'.
  - Missing mandatory parameters in a tool call.

### 2. Autonomous Halt (The Brake)
When an abnormality is detected, the agent MUST immediately stop all execution.
- **Action:** DO NOT attempt to 'guess' a fix.
- **State:** Freeze the current state and prevent any further tool calls or file writes.

### 3. Human Escalation (The Alert)
Transition from autonomous mode to 'Consultation' mode.
- **Action:** Provide a 'Diagnostic Report' to the human operator.
  - **What happened:** The specific abnormality detected.
  - **Context:** The state of the system at the time of the halt.
  - **Proposed Path:** Options for the human to resume, fix, or abort.

## Implementation Workflow

1. **Monitor:** Run a validation check after every internal reasoning step.
2. **Detect:** If a check fails, trigger the HALT protocol.
3. **Escalate:** Format the diagnostic report and wait for human input before proceeding.
