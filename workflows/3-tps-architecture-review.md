---
description: Run a heavy-duty system-level architectural review for major refactors, cross-domain integrations, or organizational alignment.
---

# TPS Architecture Review Workflow

Execute a rigorous, system-level strategic evaluation based on the Toyota Production System (TPS). This workflow is designed for **System / Organization Level** planning — evaluating entire codebases, orchestrating massive refactors, or aligning multi-system architectures to the core product vision without breaking Harmony (Wa).

## Input

The user provides one of:
- A massive refactoring directive
- A new multi-system integration goal
- A request for a codebase-wide architectural audit

## Execution Phases

Run each phase sequentially. This is a heavy-duty design protocol; take your time resolving each phase deeply.

---

### Phase 1: Shusa Leadership (Vision & Value)
**Skill:** `shusa-leadership` | **Goal:** Strategic Alignment

1. Define the **"Shusa Strategy"**: What is the overarching technical vision and core customer value proposition of this system?
2. Perform a Vision Audit: Which current components are suffering from feature creep or technical debt that do not serve this core vision?
3. **Output:** The Shusa Strategy Statement + Misalignment targets.

---

### Phase 2: Value Stream Mapping (End-to-End Flow)
**Skill:** `vsm` | **Goal:** Find Structural Bottlenecks

1. Document the complete end-to-end flow of the system (data, compute, or process).
2. Locate structural waste: Where does the system suffer from Over-processing, Context Bloat (Transportation), or Waiting?
3. Where are the true architectural bottlenecks blocking the flow of Value?
4. **Output:** End-to-End Current State Map + Future State Architecture Proposal.

---

### Phase 3: Nemawashi (A3 Proposal & Dependencies)
**Skill:** `nemawashi` | **Goal:** Dependency Impact Analysis

1. For the proposed Future State (from Phase 2), map the complete global dependency footprint.
2. Identify cross-domain conflicts: If we change architecture X, what breaks in domain Y?
3. Draft a formal **A3 Proposal** outlining the Background, Current Condition, Goal, Analysis, and specific Countermeasures.
4. **Output:** The Dependency Matrix + Draft A3 Proposal.

---

### Phase 4: Heijunka (Load Leveling)
**Skill:** `heijunka` | **Goal:** Muri Prevention (Decomposition)

1. A massive architectural shift cannot be executed synchronously. Decompose the A3 Proposal into leveled, manageable execution batches.
2. Group tasks to maintain a steady, uniform flow of work that will not overburden (Muri) the developer, the agent, or the CI/CD pipeline.
3. **Output:** The Heijunka Execution Sequence (Batched Milestones).

---

### Phase 5: KYT (System Pre-mortem)
**Skill:** `kyt` | **Goal:** Catastrophe Prevention

1. Execute a system-wide Hazard Prediction on the leveled execution plan.
2. Isolate the "Points of No Return" (e.g., destructive database migrations, irreversible API deprecations).
3. Synthesize system-wide Poka-yoke interlocks for every critical hazard (e.g., enforced database backups, blue-green deployment safeguards).
4. **Output:** System Hazard Matrix + Critical Safety Interlocks.

---

### Phase 6: Jidoka (Andon Cord Definition)
**Skill:** `jidoka` | **Goal:** Autonomous Circuit Breakers

1. Establish the "Stop the Line" thresholds for the entire rollout.
2. What specific metrics, validation failures, or error rates will automatically trip the circuit breaker and halt the massive refactor?
3. Define the exact conditions under which the system MUST revert to the baseline.
4. **Output:** The Jidoka Thresholds (Andon Cord triggers).

---

## Final Output: TPS A3 Strategic Plan

Compile the strategy into a final **TPS Architecture Proposal (A3 format)**:

```markdown
# TPS Architecture Review: [System Name]

## 1. Shusa Strategy & Vision
[The Product Vision & Value Proposition]

## 2. Value Stream Analysis (VSM)
- **Current Bottlenecks:** [Waste and friction]
- **Future State Architecture:** [The Goal]

## 3. Dependency Impact (Nemawashi)
- **Ripple Zones:** [Cross-domain dependencies]
- **Identified Conflicts:** [Potential 'Wa' disruptions]

## 4. Execution Flow (Heijunka & KYT)
- **Batched Rollout Plan:** [Step 1, Step 2...]
- **Critical Hazards Isolated:** [Points of No Return]

## 5. Organizational Guardrails (Jidoka)
- **Andon Cord Triggers:** [What halts the rollout?]
- **Poka-yoke Interlocks:** [System-wide safeguards]
```

Save the proposal as an artifact and notify the user to achieve consensus before any execution begins.
