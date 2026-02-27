---
name: andon
version: 1.0.0
description: >
  Use to "Stop the Line" when an abnormality is detected. 
  Provides a clear signal of failure and prevents the agent from compounding errors through desperate retry-loops.
category: lean-principles
tags: [andon, signal, circuit-breaker, halting, lean]
references:
  - name: Jidoka (Autonomation)
    path: ../jidoka-autonomation/SKILL.md
  - name: Hansei (Self-Reflection)
    path: ../hansei-self-reflection/SKILL.md
---

# Andon (The Signal Cord)

Andon is a visual signaling system that empowers any worker to stop production when a defect is found. In agentic workflows, it acts as a "Circuit Breaker" that stops the agent from making random changes when a tool fails or a test breaks.

## Core Mandates

### 1. Stop the Line (Circuit Breaking)
- **Action:** At the first sign of a non-deterministic error (e.g., build failure, test regression, tool timeout), the agent MUST "Pull the Andon Cord" (Stop and Analyze).
- **Constraint:** NEVER ignore a shell error code or a failed assertion to "try something else." Fix the *abnormality* before continuing the *workflow*.
- **Integration:** This is the execution phase of **Jidoka**.

### 2. Clear Signaling
- **Action:** When stopped, the agent MUST clearly state the **Abnormality** (the error), the **Location** (the file/line), and the **Hypothesis** (why it happened).
- **Constraint:** Avoid vague error reports. Use the `cc-isolate-debugging` pattern to provide a high-signal failure report.
- **Integration:** Connects to **Ho-Ren-So** for immediate escalation if the "Line" cannot be restarted autonomously.

## Escalation & Halting

- **Jidoka:** This skill *is* the halting mechanism. 
- **Hō-Ren-Sō:** If a fix attempt for the abnormality fails, escalate to the user with the "Red Light" status.

## Implementation Workflow

1. **Trigger:** A tool call returns a non-zero exit code or a test fails.
2. **Execute:** 
   - Immediate halt of the current execution plan.
   - Capture the full error log.
   - Trace the error back to the most recent change.
3. **Verify:** Perform a "Root Cause Analysis" (RCA) before restarting the line.
4. **Output:** A resolution to the abnormality or a clear escalation to the user.
