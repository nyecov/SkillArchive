---
description: Execute a comprehensive, multi-stage refinement process on a topic using Story Interview, Lean Analysis, TPS Architecture Review, and Kaizen Sprints to achieve the highest possible standard of clarity, efficiency, and structural integrity.
---

# Master Topic Refinement Workflow

Execute a comprehensive, end-to-end refinement protocol on a complex topic, feature, or system. This workflow systematically chains together four critical processes — from initial conceptual verification to system-level architecture to continuous module-level improvement.

## Input

The user provides:
- A raw concept, feature request, existing document, or system architecture that needs to be elevated to the "best possible level."

## Core Mandates (Poka-yoke)

> [!IMPORTANT]
> **Hallucination starts where verification ends.**
> This workflow enforces a strict "Verification-First" architecture. All analysis performed in Phases 2, 3, and 4 MUST be derived exclusively from the Ground Truth established in Phase 1.

### Jidoka (Autonomous Halt)
If any command or phase (Lean Analysis, Architecture Review, etc.) is triggered **WITHOUT a verified Development Story from Phase 1**, the agent MUST immediately invoke the **Jidoka Halt**:
1. Stop all current analysis.
2. Inform the user that the "Baseline Fact" is missing.
3. Automatically pivot to **Phase 1: Story Interview**.
4. Do NOT attempt to "guess" or "hallucinate" the logic to fill the vacuum.

### Meta-Skill & Auxiliary Inspection (For Skills Only)
If the target topic is an Agent Skill:
1. **Holistic Context:** You MUST inspect the entire skill directory for auxiliary materials (e.g., `scripts/`, `templates/`, `references/`) to understand the full context before analysis.
2. **Meta-Skill Alignment:** You MUST check your own active meta-skills (e.g., `skill-authoring-management`, `skill-creator`) to ensure the target skill aligns with the current "Gold Standard" of skill architecture.

## Execution Phases

Run each phase sequentially. Only proceed to the next phase once the outputs of the current phase are fully realized and documented. **Phase 1 is the immutable Fact Baseline for the entire workflow.**

---

### Phase 1: Conceptual Verification (Story Interview)
**Target:** `skills/story-interview` | **Goal:** Define and verify the core logic.

1. **Initialize:** Trigger the `story-interview` skill on the raw topic. Run `python scripts/manage_interview_state.py init` to start the deterministic state tracker.
2. **Interrogate:** Apply Socratic questioning and Deglaze tactics to strip away assumptions. After every turn, update the state file using the exact CLI syntax defined in the `story-interview` skill.
3. **Verify:** Ensure every requirement has a testable acceptance condition and all sad paths are identified.
4. **Output:** Render the finalized **Development Story Document** via `manage_interview_state.py render` containing the verified user value, core logic, constraints, and verification criteria.

---

### Phase 2: Systematic Waste & Risk Audit (Lean Analysis)
**Target:** `workflows/1-lean-analysis.md` | **Goal:** 360-degree analytical scan.

1. **Analyze:** Feed the Development Story Document (from Phase 1) into the `1-lean-analysis.md` workflow.
2. **Execute Lenses:** Run the topic through all 9 lean-tagged analytical lenses. **Constraint:** Use ONLY the verified logic and constraints defined in the Story. If a lens reveals a gap, escalate back to Phase 1.
3. **Output:** A comprehensive **Lean Analysis Report**, detailing bottlenecks, systemic waste, and a prioritized list of critical actions.

---

### Phase 3: System-Level Strategy (TPS Architecture Review)
**Target:** `workflows/3-tps-architecture-review.md` | **Goal:** Structural alignment and safe rollout.

1. **Evaluate:** Review the Critical Actions from Phase 2. Ensure they align with the overarching product vision.
2. **Map Flow & Dependencies:** Run the `3-tps-architecture-review.md` workflow to map end-to-end flow, identify architectural bottlenecks, and map the cross-domain dependency footprint (Nemawashi).
3. **Design Safeguards:** Establish system-wide Poka-yoke interlocks and Jidoka (Andon Cord) thresholds for any major changes.
4. **Output:** A formal **TPS Architecture Proposal (A3)** outlining the future state, leveled rollout plan (Heijunka), and organizational guardrails.

---

### Phase 4: Module-Level Optimization (Kaizen Sprint)
**Target:** `workflows/2-kaizen-sprint.md` | **Goal:** Targeted problem solving and standardization.

1. **Target Friction:** Identify specific, localized friction points, recurring issues, or inefficiencies uncovered in Phases 2 and 3.
2. **Execute PDCA:** For each targeted issue, run the `2-kaizen-sprint.md` workflow.
3. **Root Cause & Fix:** Perform a 5-Whys drilldown (Hansei), implement a poka-yoke interlock, and verify the baseline improvement (Shisa Kanko).
4. **Output:** One or more **Kaizen PDCA Reports**, standardizing the improvements horizontally (Yokoten) and bringing the module to peak efficiency.

---

## Final Output: Master Refinement Dossier

Compile the outputs of all four phases into a consolidated **Master Refinement Dossier**:

1. **The Verified Story:** (Output of Phase 1)
2. **The Lean Audit:** (Output of Phase 2)
3. **The Strategic Architecture:** (Output of Phase 3)
4. **The targeted Kaizen Improvements:** (Outputs of Phase 4)

Save the dossier as an artifact in the brain directory and notify the user that the topic has been brought to the best possible level.
