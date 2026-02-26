---
name: Kaizen (Continuous Improvement)
version: 1.1.0
description: The practice of continuous, incremental improvement. Enables agents to learn from past executions, Jidoka halts, and Hansei reflections to permanently optimize their own workflows.
category: continuous-improvement
tags: [kaizen, optimization, learning, evolution, pdca, lean]
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
  - name: Hō-Ren-Sō (Communication)
    path: ./ho-ren-so-communication.md
  - name: Lean Principles (Muda Eradication)
    path: ./lean-principles-muda.md
  - name: Value Stream Mapping (VSM)
    path: ./vsm-value-stream-mapping.md
---

# Kaizen: Continuous Agentic Improvement

Kaizen is the commitment to constant, incremental evolution. While **Hansei** is the act of reflecting on a specific mistake, Kaizen is the systemic application of that learning to permanently improve the standard operating procedure. It transforms isolated lessons into durable architectural upgrades.

## Core Mandates: The PDCA Cycle

Kaizen relies on the Plan-Do-Check-Act (PDCA) loop to ensure improvements are scientifically validated.

### 1. Plan (Standardize & Hypothesize)
- **Action:** Identify a baseline workflow that frequently experiences **Jidoka** halts or generates waste (Muda).
- **Hypothesis:** Formulate a small, specific change to the system prompt, schema, or **Poka-yoke** constraint that will reduce friction.
- **VSM Input:** Use **Value Stream Mapping** output to pinpoint the exact bottleneck or waste category to target.

### 2. Do (Execute the Experiment)
- **Action:** Implement the small change in the next execution cycle.
- **Constraint:** Kaizen changes MUST be small and isolated. Do not overhaul the entire architecture at once.
- **KYT Pre-Check:** Run a lightweight **KYT** assessment on the proposed change itself — even improvement experiments carry risk.

### 3. Check (Measure via Hansei)
- **Action:** Use **Hansei (Self-reflection)** to evaluate the results. Did the change reduce token usage? Did it lower the error rate? Did it speed up execution?
- **Metrics:** Compare against the baseline established in Phase 1 using concrete, observable criteria.

### 4. Act (Standardize the New Baseline)
- **Action:** If the experiment was successful, permanently update the skill documentation, system prompt, or **Poka-yoke** schema to make this the new standard.
- **Hō-Ren-Sō (Hōkoku):** Report the outcome — whether success or failure — to the human operator so the team maintains visibility of evolving standards.

## Escalation & Halting

- **Failed Experiment (Jidoka):** If the Kaizen change introduces regressions or new **Jidoka** halts, immediately revert to the previous standard. Do not compound a failed improvement with further speculative changes.
- **Ambiguous Results (Hō-Ren-Sō):** If the Check phase produces ambiguous or inconclusive results, use the **Sōdan (Consult)** protocol to present the data to the human operator and request a judgment call on whether to adopt, modify, or discard the change.

## Implementation Workflow

1. **Trigger:** A successful **Hansei** analysis identifies a recurring root cause or a **VSM** map reveals a structural bottleneck.
2. **Kaizen Event:** The agent proposes a structural update to a constraint, prompt, or workflow step.
3. **PDCA Execution:** Run the four phases above with discipline — plan, execute, measure, and standardize.
4. **Evolution:** The standard is updated, ensuring the agent never makes the exact same class of mistake twice.
