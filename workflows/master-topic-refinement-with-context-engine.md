---
id: 79f2c8d1-4b1a-4d9e-9b2c-8d1c6e4a2b3c
name: master-topic-refinement-with-context-engine
version: 1.0.0
level: methodology
description: A multi-phase refinement protocol enhanced by the Context Engine to ensure a topic, documentation, or codebase reaches the highest level of Lean quality.
---
# Master Topic Refinement Workflow (with Context Engine)

Execute a comprehensive, end-to-end refinement protocol on a complex topic, feature, or system, leveraging the **Context Engine** for deep codebase comprehension and persistent session memory. This workflow systematically chains together four critical processes — from initial conceptual verification to system-level architecture to continuous module-level improvement.

## Input

The user provides:
- A raw concept, feature request, existing document, or system architecture that needs to be elevated to the "best possible level."

## Core Mandates (Poka-yoke)

> [!IMPORTANT]
> **Hallucination starts where verification ends.**
> This workflow enforces a strict "Verification-First" architecture. All analysis performed in Phases 2, 3, and 4 MUST be derived exclusively from the Ground Truth established in Phase 1 and the architectural facts indexed by the Context Engine.

### Jidoka (Autonomous Halt)
If any command or phase (Lean Analysis, Architecture Review, etc.) is triggered **WITHOUT a verified Development Story from Phase 1**, or if a Context Engine tool is invoked **WITHOUT required schema parameters** (e.g., missing `phase` for `log_session_finding`), the agent MUST immediately invoke the **Jidoka Halt**:
1. Stop all current analysis.
2. Inform the user of the missing baseline or malformed tool call.
3. Automatically pivot to **Phase 1: Story Interview** or correct the tool call parameters.
4. Do NOT attempt to "guess" or "hallucinate" logic or parameters.

### Meta-Skill & Auxiliary Inspection (For Skills Only)
If the target topic is an Agent Skill:
1. **Holistic Context:** You MUST inspect the entire skill directory for auxiliary materials (e.g., `scripts/`, `templates/`, `references/`) to understand the full context before analysis.
2. **Meta-Skill Alignment:** You MUST check your own active meta-skills (e.g., `skill-authoring-management`, `skill-creator`) to ensure the target skill aligns with the current "Gold Standard" of skill architecture.

## Execution Phases

Run each phase sequentially. Only proceed to the next phase once the outputs of the current phase are fully realized and documented. **Phase 1 is the immutable Fact Baseline for the entire workflow.**

---

### Phase 1: Conceptual Verification (Story Interview with Context Engine)
**Target:** `skills/interview` | **Goal:** Define and verify core logic using MCP Context Engine tools.

1. **Initialize:** Trigger the `interview` skill. Run `clear_session_state` to ensure a fresh scratchpad.
2. **Recall:** Call `read_ontology_graph` with a relevant query to check for historical context, prior interview overlaps, or established patterns in the Ontology Graph.
3. **Interrogate:** Apply Socratic questioning and Deglaze tactics. Update the persistent Knowledge Graph using `commit_ontology_edge` for every finalized insight. Use `log_session_finding` with the `phase: "planning"` parameter for transient session notes.
4. **Verify:** Ensure every requirement has a testable acceptance condition. Use `read_ontology_graph` to confirm findings against existing architectural dependencies.
5. **Harden (Maturation):** Call `commit_ontology_edge` to move the high-level summary of the verified logic into the permanent Knowledge Graph.
6. **Prune:** Execute `clear_session_state` to wipe the scratchpad before Phase 2.
7. **Output:** Render the finalized **Development Story Document**.

---

### Phase 2: Systematic Waste & Risk Audit (Lean Analysis)
**Target:** `workflows/1-lean-analysis.md` | **Goal:** 360-degree analytical scan.

1. **Analyze:** Feed the Development Story Document (from Phase 1) into the `1-lean-analysis.md` workflow.
2. **Execute Lenses:** Run the topic through all 9 lean-tagged analytical lenses. Record findings via `log_session_finding` with `phase: "planning"`.
3. **Harden (Maturation):** Once the audit is complete, call `commit_ontology_edge` to archive the critical bottlenecks in the Knowledge Graph.
4. **Prune:** Execute `clear_session_state`.
5. **Output:** A comprehensive **Lean Analysis Report**.

---

### Phase 3: System-Level Strategy (TPS Architecture Review)
**Target:** `workflows/3-tps-architecture-review.md` | **Goal:** Structural alignment and safe rollout.

1. **Evaluate:** Review critical actions. Call `read_ontology_graph` to map existing structural anchors and end-to-end flow dependencies.
2. **Map Flow:** Run `3-tps-architecture-review.md`. Record rollout steps using `log_session_finding` with `phase: "planning"`.
3. **Design Safeguards:** Establish Poka-yoke interlocks.
4. **Harden (Maturation):** Call `commit_ontology_edge` to link the new A3 strategy to the affected components in the Knowledge Graph.
5. **Prune:** Execute `clear_session_state`.
6. **Output:** A formal **TPS Architecture Proposal (A3)**.

---

### Phase 4: Pilot Verification (Nemawashi)
**Goal:** Confirm environment and tool compatibility before bulk optimization.

1. **Isolate:** Select a single module or skill identified in Phases 2 and 3.
2. **Execute Pilot:** Perform a trial Kaizen Sprint or audit on this single target.
3. **Verify Paths:** Ensure all scripts, templates, and directory paths (especially those containing spaces) are correctly handled and verified via the Context Engine.
4. **Output:** A verified "Operation Baseline." If the pilot reveals pathing friction, resolve the root cause before vertical scaling.

---

### Phase 5: Module-Level Optimization (Kaizen Sprint)
**Target:** `workflows/2-kaizen-sprint.md` | **Goal:** Targeted problem solving and standardization.

1. **Target Friction:** Use `log_session_finding` with `phase: "execution"` to track Kaizen progress.
2. **Execute PDCA:** For each targeted issue, run the `2-kaizen-sprint.md` workflow.
3. **Standardize (Yokoten):** Once fixed, call `commit_ontology_edge` with `edge_type: "IMPLEMENTS"` to record the new standard in the Knowledge Graph.
4. **Prune:** Execute `clear_session_state`.
5. **Output:** **Kaizen PDCA Reports**.

---

## Final Output: Master Refinement Dossier

Compile the outputs of all five phases into a consolidated **Master Refinement Dossier**:

1. **The Verified Story:** (Output of Phase 1)
2. **The Lean Audit:** (Output of Phase 2)
3. **The Strategic Architecture:** (Output of Phase 3)
4. **The Pilot Verification:** (Output of Phase 4)
5. **The targeted Kaizen Improvements:** (Outputs of Phase 5)

Save the dossier as an artifact in the brain directory and notify the user that the topic has been brought to the best possible level.

## Escalation & Halting
- **Jidoka:** If logical or architectural contradictions persist, trigger a halt and revert to the latest verified anchor.
- **Hō-Ren-Sō:** Use Sōdan (Consult) if the refinement reveals a need for a fundamental architectural pivot.
