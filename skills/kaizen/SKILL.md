---
name: kaizen
version: 1.2.0
level: methodology
category: methodology
description: 'Use when a recurring error, structural bottleneck, or workflow inefficiency is identified (either manually or via Hansei/VSM). Applies continuous improvement cycles to eliminate the root cause.'
tags:
- methodology
- optimization
- lean
- TPS
- kaizen
references:
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Jidoka (Autonomation)
  path: ../jidoka/SKILL.md
- name: Poka-yoke (Mistake-proofing)
  path: ../poka-yoke/SKILL.md
- name: Hansei (Self-reflection)
  path: ../hansei/SKILL.md
- name: KYT (Hazard Prediction)
  path: ../kyt/SKILL.md
- name: Lean Foundations
  path: ../lean-foundations/SKILL.md
- name: Value Stream Mapping (VSM)
  path: ../vsm/SKILL.md
- name: Skill Authoring Management
  path: ../skill-authoring-management/SKILL.md
---

# Kaizen

Kaizen is the commitment to constant, incremental evolution. While **Hansei** reflects on a specific mistake, Kaizen is the systemic application of that learning to permanently improve the standard operating procedure (SOP). It transforms isolated lessons into durable architectural upgrades.

## Core Mandates

### 1. Systematic PDCA
Apply the Plan-Do-Check-Act cycle to transform lessons into durable upgrades.
- **Action:** Formulate a small, testable hypothesis to reduce friction or waste in a baseline workflow.
- **Constraint:** Kaizen changes MUST be incremental. NEVER overhaul the entire architecture in a single experiment.
- **Integration:** Uses **VSM** or **Hansei** to identify the specific bottleneck for the "Plan" phase.

### 2. Experimental Validation
Execute the proposed improvement in a controlled cycle and measure its impact against the baseline.
- **Action:** Run the experiment and use **Hansei** to evaluate metrics (token usage, error rate, execution speed).
- **Constraint:** If the experiment introduces regressions, revert the codebase immediately AND generate a "Failed Experiment Report" to ensure the exact same bad hypothesis is not repeated.
- **Integration:** Connects to **KYT** to assess the risks of the proposed improvement itself.

### 3. Standardization (Yokoten)
If an experiment is successful, permanently update the skill documentation or system prompt.
- **Action:** Update the `SKILL.md` or schema, and generate the formal Kaizen PDCA Report.
- **Constraint:** Any proposed update to a skill's `SKILL.md` MUST be validated autonomously by running `manage_skill_authoring.py` BEFORE the PDCA report is finalized and success is declared.
- **Integration:** Binds to **Skill Authoring Management** to prevent structural Mura (inconsistency) when updating the library.

## Escalation & Halting

- **Jidoka:** If an improvement experiment causes a system-wide failure, trigger an immediate Jidoka halt, execute the Definitive Rollback, and log the Failed Experiment Report.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol if PDCA results are ambiguous.

## Implementation Workflow

1. **Trigger:** Triggered automatically via a Hansei/VSM evaluation or invoked manually by the user identifying an inefficiency.
2. **Execute:** Run the Kaizen cycle with discipline — plan (formulate hypothesis), execute, measure against baseline, and standardize.
3. **Verify:** Run `manage_skill_authoring.py` against the modified `SKILL.md` to guarantee Gold Standard compliance.
4. **Output:** Render the Kaizen PDCA Report summarizing the fix using the Poka-yoke Output Template.

## Poka-yoke Output Template

When the Kaizen sprint concludes successfully, output the findings exclusively using this exact Markdown format:

```markdown
# Kaizen Sprint Report: [Issue/Process Name]

## 1. The Anomaly (Genchi Genbutsu & Hansei)
- **Observed Behavior:** [Facts]
- **Root Cause (5-Whys):** [Bedrock Cause]

## 2. The Solution (Kaizen & Poka-yoke)
- **Hypothesis:** [If X then Y]
- **Interlock:** [The deterministic guardrail]

## 3. The Evidence (Shisa Kanko)
- **Baseline vs New State:** [Metric shift]
- **Verification Result:** PASS / FAIL

## 4. The Standard (Yokoten)
- **New Standard Operating Procedure:** [What was permanently updated]
- **Horizontal Targets:** [Where else this applies]
```
