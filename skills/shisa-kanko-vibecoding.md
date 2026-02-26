---
name: Shisa Kanko Software Engineering & Vibecoding
version: 2.0.0
description: A high-integrity master workflow unifying 'Pointing and Calling' with Lean principles (Jidoka, Poka-yoke, Hansei, KYT, Hō-Ren-Sō) to eliminate hallucinations, enforce safety, and systematize AI-assisted coding.
category: software-engineering
tags: [vibecoding, ai-safety, lean, shisa-kanko, jidoka, poka-yoke, hansei, kyt, ho-ren-so, agentic-workflows]
references:
  - name: Shisa Kanko Architecture Report
    url: https://docs.google.com/document/d/1TdP7WJTRgWYJJ5157Ug3vussKCUM9bU5frnkeQFeWYI/edit?usp=sharing
  - name: Jidoka (Autonomation)
    path: ./jidoka-autonomation.md
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

# Shisa Kanko Engineering Master Workflow

This master skill synthesizes the **Shisa Kanko (Pointing and Calling)** architecture with core Lean manufacturing principles. It transforms 'vibecoding' from intuitive execution into a rigorously safe, deterministic engineering discipline.

## Core Mandates & Constraints

### 1. Precise Pointing (Context Isolation)
Before any modification, 'point' to the target with absolute precision.
- **Action:** Output a `[TARGET_ISOLATION]` block containing the file path, line ranges, and the **Exact Code Snippet**.
- **Poka-yoke Interlock:** If the snippet cannot be perfectly matched via a `read_file` check, you MUST NOT proceed to execution.

### 2. Explicit Calling (Intent & Success)
Never execute a tool call without 'calling out' the expected outcome.
- **Action:** Output a strictly formatted `[LOGIC_DECLARATION]` block:
  - **Intent:** Specific code change.
  - **Success Criteria:** What defines success.
  - **Validation Method:** The exact command to verify success.

### 3. Jidoka (Autonomation & Self-Monitoring)
Continuously monitor internal confidence and API responses.
- **Action:** If an abnormality (e.g., mismatched schema, unexpected test output) occurs, trigger an immediate **Autonomous Halt** and freeze execution. Do not attempt blind guesses to fix it.

## The High-Integrity Vibecoding Lifecycle

### Phase A: Alignment & Reflection (Hansei)
1. **Define the Vibe:** State the architectural goal.
2. **Draft Plan:** Outline the technical implementation.
3. **Hansei (Self-reflection):** Critically review the draft. "Identify three ways this plan could fail or introduce architectural rot."
4. **Refine:** Incorporate countermeasures into the final plan.

### Phase B: Pre-Mortem Risk Assessment (KYT)
Before executing Phase C, run the 4-round KYT protocol:
1. **Hazard:** Identify the primary danger of the change.
2. **Critical Point:** Identify the 'Point of No Return'.
3. **Countermeasure:** Establish a mitigation step.
4. **Action Target:** Create a binary Go/No-Go checklist.

### Phase C: Deterministic Execution
1. **Point:** Isolate the target (Mandate 1).
2. **Call:** Declare logic and validation (Mandate 2).
3. **Act:** Execute the surgical update.
4. **Point (Re-verify):** Read the file back to ensure perfect application.

### Phase D: Multi-Sensory Verification
1. **Validation:** Run the validation command defined in Phase C.
2. **Vibe Audit:** Confirm the output (logs/UI) aligns with Phase A.

## Escalation & Communication (Hō-Ren-Sō)
Replace silent failure or assumption-making with standardized communication.

- **Hōkoku (Report):** Summarize successful completion of Phase D to the user.
- **Renraku (Contact):** Broadcast any unexpected environmental changes (e.g., "Tests are failing locally").
- **Sōdan (Consult) - The Red Stop Trigger:** You MUST halt and consult the user if:
  - Jidoka detects an abnormality (e.g., missing dependencies).
  - The KYT Pre-Mortem identifies unrecoverable risk.
  - 'Pointing' reveals severe drift from your mental model.

## Path Rules
- Internal references MUST use relative paths.
- External resources MUST use absolute URLs.
