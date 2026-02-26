---
name: Kaizen (Continuous Improvement)
version: 1.0.0
description: The practice of continuous, incremental improvement. Enables agents to learn from past executions, Jidoka halts, and Hansei reflections to permanently optimize their own workflows.
category: continuous-improvement
tags: [kaizen, optimization, learning, evolution, pdca]
references:
  - name: Lean Principles (Muda Eradication)
    path: ./lean-principles-muda.md
  - name: Hansei (Self-reflection)
    path: ./hansei-self-reflection.md
  - name: Poka-yoke (Mistake-proofing)
    path: ./poka-yoke-mistake-proofing.md
---

# Kaizen: Continuous Agentic Improvement

Kaizen is the commitment to constant, incremental evolution. While **Hansei** is the act of reflecting on a specific mistake, Kaizen is the systemic application of that learning to permanently improve the standard operating procedure.

## Core Mandates: The PDCA Cycle

Kaizen relies on the Plan-Do-Check-Act (PDCA) loop to ensure improvements are scientifically validated.

### 1. Plan (Standardize & Hypothesize)
- **Action:** Identify a baseline workflow that frequently experiences **Jidoka** halts or generates waste (Muda). 
- **Hypothesis:** Formulate a small, specific change to the system prompt, schema, or **Poka-yoke** constraint that will reduce friction.

### 2. Do (Execute the Experiment)
- **Action:** Implement the small change in the next execution cycle.
- **Constraint:** Kaizen changes MUST be small and isolated. Do not overhaul the entire architecture at once.

### 3. Check (Measure via Hansei)
- **Action:** Use **Hansei (Self-reflection)** to evaluate the results. Did the change reduce token usage? Did it lower the error rate? Did it speed up execution?

### 4. Act (Standardize the New Baseline)
- **Action:** If the experiment was successful, permanently update the skill documentation, system prompt, or **Poka-yoke** schema to make this the new standard.

## Integration Workflow

1. **Trigger:** A successful **Hansei** analysis identifies a recurring root cause.
2. **Kaizen Event:** The agent proposes a structural update to a constraint or prompt.
3. **Evolution:** The standard is updated, ensuring the agent never makes the exact same class of mistake twice.
