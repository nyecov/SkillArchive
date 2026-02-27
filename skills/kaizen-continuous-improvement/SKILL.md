---
name: kaizen-continuous-improvement
version: 1.1.0
description: >
  Use when a recurring error, structural bottleneck, or workflow inefficiency is identified.
  Handles PDCA-based experiment design, controlled rollout, measurement, and permanent standard updates.
category: continuous-improvement
tags: [kaizen, optimization, learning, evolution, pdca, lean]
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
  - name: Hō-Ren-Sō (Communication)
    path: ../ho-ren-so-communication/SKILL.md
  - name: Lean Principles (Muda Eradication)
    path: ../lean-principles-muda/SKILL.md
  - name: Value Stream Mapping (VSM)
    path: ../vsm-value-stream-mapping/SKILL.md
---

# Kaizen: Continuous Agentic Improvement

Kaizen is the commitment to constant, incremental evolution. While **Hansei** is the act of reflecting on a specific mistake, Kaizen is the systemic application of that learning to permanently improve the standard operating procedure. It transforms isolated lessons into durable architectural upgrades.

## Core Mandates

### 1. Systematic PDCA
Apply the Plan-Do-Check-Act cycle to transform isolated lessons (Hansei) into durable architectural upgrades.
- **Action:** Formulate a small, testable hypothesis to reduce friction or waste in a baseline workflow.
- **Constraint:** Kaizen changes MUST be incremental. NEVER overhaul the entire architecture in a single experiment.
- **Integration:** Uses **VSM (Value Stream Mapping)** to identify the specific bottleneck for the "Plan" phase.

### 2. Experimental Validation
Execute the proposed improvement in a controlled cycle and measure its impact against the baseline.
- **Action:** Run the experiment and use **Hansei** to evaluate metrics (token usage, error rate, execution speed).
- **Constraint:** Revert immediately if the experiment introduces new **Jidoka** halts or regressions.
- **Integration:** Connects to **KYT** to assess the risks of the proposed improvement itself.

### 3. Standardization (New Baseline)
If an experiment is successful, permanently update the skill documentation or system prompt to establish a new standard.
- **Action:** Update the `SKILL.md` or schema once the improvement is verified.
- **Constraint:** Do not consider an improvement complete until it is documented and standardized for all future executions.
- **Integration:** Supports the "Sustain" (Shitsuke) phase of **Lean Foundations (5S)**.

## Escalation & Halting

- **Jidoka:** If an improvement experiment causes a system-wide failure or multiple tool errors, trigger an immediate Jidoka halt and revert.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol if PDCA results are ambiguous, or the Hōkoku (Report) protocol to announce a new verified standard to the user.

## Implementation Workflow

1. **Trigger:** A successful **Hansei** analysis identifies a recurring root cause or a **VSM** map reveals a structural bottleneck.
2. **Kaizen Event:** The agent proposes a structural update to a constraint, prompt, or workflow step.
3. **PDCA Execution:** Run the four phases above with discipline — plan, execute, measure, and standardize.
4. **Evolution:** The standard is updated, ensuring the agent never makes the exact same class of mistake twice.
