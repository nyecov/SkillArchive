---
name: shisa-kanko-vibecoding
version: 2.0.0
description: >
  Use when executing code changes, tool calls, or multi-step engineering tasks.
  Handles context isolation, intent declaration, deterministic verification, and risk-gated execution through a phased lifecycle.
category: software-engineering
tags: [vibecoding, ai-safety, lean, shisa-kanko, jidoka, poka-yoke, hansei, kyt, ho-ren-so, agentic-workflows]
references:
  - name: Jidoka (Autonomation)
    path: ../jidoka-autonomation/SKILL.md
  - name: Poka-yoke (Mistake-proofing)
    path: ../poka-yoke-mistake-proofing/SKILL.md
  - name: Hansei (Self-reflection)
    path: ../hansei-self-reflection/SKILL.md
  - name: KYT (Hazard Prediction)
    path: ../kyt-hazard-prediction/SKILL.md
  - name: Hō-Ren-Sō (Communication)
    path: ../ho-ren-so-communication/SKILL.md
  - name: Kaizen (Continuous Improvement)
    path: ../kaizen-continuous-improvement/SKILL.md
  - name: Lean Principles (Muda Eradication)
    path: ../lean-principles-muda/SKILL.md
  - name: Value Stream Mapping (VSM)
    path: ../vsm-value-stream-mapping/SKILL.md
---

# Shisa Kanko Engineering Master Workflow

This master skill synthesizes the **Shisa Kanko (Pointing and Calling)** architecture with core Lean manufacturing principles. It transforms 'vibecoding' from intuitive execution into a rigorously safe, deterministic engineering discipline.

## Core Mandates

### 1. Precise Pointing (Context Isolation)
Before any modification, 'point' to the target with absolute precision.
- **Action:** Output a `[TARGET_ISOLATION]` block containing the file path, line ranges, and the **Exact Code Snippet**.
- **Constraint:** If the snippet cannot be perfectly matched via a `read_file` check, you MUST NOT proceed to execution.
- **Integration:** Acts as a **Poka-yoke** interlock.

### 2. Explicit Calling (Intent & Success)
Never execute a tool call without 'calling out' the expected outcome.
- **Action:** Output a strictly formatted `[LOGIC_DECLARATION]` block:
  - **Intent:** Specific code change.
  - **Success Criteria:** What defines success.
  - **Validation Method:** The exact command to verify success.
- **Constraint:** All execution MUST be preceded by this declaration.
- **Integration:** Feeds into the final **Verification** step.

### 3. Jidoka (Autonomation & Self-Monitoring)
Continuously monitor internal confidence and API responses.
- **Action:** If an abnormality (e.g., mismatched schema, unexpected test output) occurs, trigger an immediate **Autonomous Halt** and freeze execution. 
- **Constraint:** Do not attempt blind guesses to fix it.
- **Integration:** Triggers the **Jidoka** skill.

## Escalation & Halting

- **Jidoka:** Any pointing mismatch or abnormal tool response MUST trigger a Jidoka halt.
- **Hō-Ren-Sō:** Use Sōdan (Consult) if pointing reveals severe drift from the mental model or if KYT identifies unrecoverable risk.

## Implementation Workflow

1. **Trigger:** A Directive is received from the user.
2. **Execute:** Follow the Phases A-C (Reflect -> Risk Assessment -> Deterministic Execution).
3. **Verify:** Phase D (Validation + Vibe Audit).
4. **Output:** A verified, high-integrity update and a Hōkoku (Report) to the user.
