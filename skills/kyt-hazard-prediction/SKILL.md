---
name: KYT (Hazard Prediction)
version: 1.1.0
description: >
  Use before executing high-risk operations, destructive commands, or irreversible changes.
  Handles 4-round hazard identification, countermeasure design, and Go/No-Go gating.
category: risk-management
tags: [kyt, hazard-prediction, safety, critic-agent, pre-mortem, lean]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko-vibecoding/SKILL.md
  - name: Jidoka (Autonomation)
    path: ../jidoka-autonomation/SKILL.md
  - name: Poka-yoke (Mistake-proofing)
    path: ../poka-yoke-mistake-proofing/SKILL.md
  - name: Hansei (Self-reflection)
    path: ../hansei-self-reflection/SKILL.md
  - name: Hō-Ren-Sō (Communication)
    path: ../ho-ren-so-communication/SKILL.md
  - name: Kaizen (Continuous Improvement)
    path: ../kaizen-continuous-improvement/SKILL.md
  - name: Lean Principles (Muda Eradication)
    path: ../lean-principles-muda/SKILL.md
  - name: Value Stream Mapping (VSM)
    path: ../vsm-value-stream-mapping/SKILL.md
---

# KYT: Hazard Prediction Training for Agents

KYT (Kiken Yochi Training) is a systematic, multi-round protocol for identifying dangers before they occur. In an agentic architecture, it serves as the pre-mortem analysis layer, bridging the gap between an Execution Agent's proposed plan and the actual execution of tools.

## The 4-Round KYT Protocol

The Critic Agent MUST run this protocol on the Execution Agent's plan *before* any **Shisa Kanko** execution begins.

### Round 1: Identify the Hazard (Hansei Alignment)
- **Action:** Utilize **Hansei (Self-reflection)** to critically analyze the Execution Agent's proposed 'Logic Declaration'. List all potential dangers, side-effects, or architectural drift associated with the action.
- *Example:* "Executing a raw SQL drop command might cascade and delete user relational data if the foreign keys are not properly constrained."

### Round 2: Determine Critical Danger Points
- **Action:** Narrow the list to the most severe or irreversible 'Points of No Return'.
- *Example:* "The critical point is the `DROP TABLE` command itself, which bypasses application-level soft deletes."

### Round 3: Establish Countermeasures (Poka-yoke Design)
- **Action:** Define specific, deterministic actions to mitigate the critical dangers. Whenever possible, design these countermeasures as **Poka-yoke (Mistake-proofing)** interlocks rather than just 'trying to be careful'.
- *Example:* "Countermeasure: Implement a Poka-yoke interlock that requires a `before_drop_backup.sql` file to exist in the `tmp/` directory before the database tool can be invoked."

### Round 4: Set Action Targets (The Go/No-Go Check)
- **Action:** Create a final, binary checklist that must be passed before execution.
- *Example:* "Checklist: 1. Backup file exists (Poka-yoke check). 2. Impact radius reviewed (Hansei). 3. Maintenance window active."

## Escalation & Halting

- **Unmitigable Hazards (Jidoka):** If Round 3 fails to produce a reliable countermeasure for a catastrophic risk, the Critic Agent MUST trigger a **Jidoka** halt.
- **Human Consultation (Hō-Ren-Sō):** If a halt is triggered, or if the Critical Danger Point involves core security/infrastructure, the system MUST use the **Sōdan (Consult)** protocol to present the KYT findings to a human operator for a final Go/No-Go decision.

## Implementation Workflow

1. **Plan Generation:** Execution Agent drafts a plan.
2. **KYT Pass:** Critic Agent executes the 4 rounds.
3. **Refinement:** Execution Agent integrates the Poka-yoke countermeasures.
4. **Verification:** System checks Action Targets; if cleared, proceed to Shisa Kanko pointing and calling.
