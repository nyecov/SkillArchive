---
description: Run a full Lean analysis on a document or topic using all 9 lean-tagged skills as analytical lenses
---

# Lean Analysis Workflow

Systematically analyze a document, codebase, or topic through **all 9 lean-tagged skills**, producing a comprehensive Lean Analysis Report. Each phase applies a distinct analytical lens — from waste identification to strategic alignment.

## Input

The user provides one of:
- A **file path** to a document or code to analyze
- A **topic description** or concept to evaluate
- A **URL** to external content to review

## Execution Phases

Run each phase sequentially. For each phase, produce a short findings section (3-5 bullets). If a phase does not apply, state "N/A — [reason]" and move on.

---

### Phase 1: Lean Foundations — Waste & Workspace Scan
**Skill:** `lean-foundations` | **Lens:** 3M + 5S

1. Scan for the **3 Ms** in the subject:
   - **Mura** (Unevenness): Inconsistencies in logic, structure, or style.
   - **Muri** (Overburden): Overloaded sections, excessive complexity, cognitive strain.
   - **Muda** (Waste): Content that adds no value — redundancy, dead logic, speculative features.
2. Scan with the **5S** framework:
   - Is everything **sorted** (necessary vs. unnecessary)?
   - Is it in **order** (well-structured)?
   - Is it **clean** (no dead code, stale references)?
   - Is it **standardized** (follows conventions)?
   - Is it **sustained** (maintained over time)?
3. **Output:** A bullet list of identified Ms and 5S violations.

---

### Phase 2: Story Interview — Socratic Interrogation
**Skill:** `story-interview` | **Lens:** Value & Assumptions

1. State the **core goal** of the document/topic in one sentence.
2. Apply **Deglaze questioning**:
   - "What problem does this actually solve?"
   - "What happens if [component X] fails?"
   - "Can we remove [section Y] and still achieve the goal?"
3. Identify every claim or requirement that **lacks verifiable acceptance criteria**.
4. **Output:** Core value statement + list of unverified assumptions.

---

### Phase 3: Value Stream Mapping — Flow Analysis
**Skill:** `vsm` | **Lens:** Bottlenecks & Flow

1. Map the **current state**: trace the logical flow from input to output.
2. Identify **bottlenecks**: Where does complexity spike? Where is effort disproportionate to value?
3. Identify **silent waste**: processes that work but are inefficient.
4. Propose a **future state**: a leaner path from input to output.
5. **Output:** Current state summary + bottleneck list + future state proposal.

---

### Phase 4: KYT — Hazard Prediction
**Skill:** `kyt` | **Lens:** Risk & Failure Modes

1. **Round 1 — Discover hazards:** What could go wrong with this document/approach?
2. **Round 2 — Critical points:** Which hazards are irreversible or high-impact?
3. **Round 3 — Countermeasures:** What deterministic safeguards exist (or are missing)?
4. **Round 4 — Action targets:** What specific actions should be taken to mitigate each critical hazard?
5. **Output:** Risk matrix (Hazard → Severity → Countermeasure → Status).

---

### Phase 5: Poka-yoke — Guardrails Audit
**Skill:** `poka-yoke` | **Lens:** Error Prevention

1. Check for **schema enforcement**: Are inputs/outputs validated and constrained?
2. Check for **state machine constraints**: Is the process flow enforced in the correct order?
3. Check for **prerequisite interlocks**: Are dependencies checked before proceeding?
4. Identify where the subject **fails open** (allows errors to pass silently).
5. **Output:** List of missing guardrails + proposed interlocks.

---

### Phase 6: Shisa Kanko — Precision Audit
**Skill:** `shisa-kanko` | **Lens:** Point & Call Verification

1. **Point** at the 3 most critical claims, decisions, or code paths in the subject.
2. For each, **call out**:
   - **Intent:** What it's supposed to do.
   - **Success Criteria:** How you know it's working.
   - **Verification Method:** How you would test it.
3. Flag any item where the intent is ambiguous or unverifiable.
4. **Output:** 3 Pointed & Called verification cards.

---

### Phase 7: Nemawashi — Impact Analysis
**Skill:** `nemawashi` | **Lens:** Dependencies & Ripple Effects

1. Map the **dependency footprint**: What does this document/system depend on? What depends on it?
2. Identify **ripple zones**: If this subject changes, what else breaks or must adapt?
3. Flag any **cross-domain conflicts** that require consensus before proceeding.
4. **Output:** Dependency map + ripple risk assessment.

---

### Phase 8: Shusa Leadership — Strategic Alignment
**Skill:** `shusa-leadership` | **Lens:** Vision & Value

1. Does this document/topic **serve the core product vision**?
2. Is there **feature creep** or technical debt that doesn't serve the stated goal?
3. Does it maintain **cross-functional harmony** (Wa) — or does it create friction?
4. **Output:** Strategic alignment verdict (Aligned / Drifting / Misaligned) + rationale.

---

### Phase 9: Yokoten — Horizontal Deployment
**Skill:** `yokoten` | **Lens:** Pattern Transfer

1. What **successful patterns** discovered in this analysis can be applied elsewhere?
2. What **anti-patterns** identified here likely exist in other parts of the system?
3. Propose a **Yokoten broadcast plan**: which other documents/modules should receive the findings?
4. **Output:** List of transferable patterns + broadcast targets.

---

## Final Output: Lean Analysis Report

After completing all 9 phases, compile the findings into a consolidated **Lean Analysis Report** artifact with the following structure:

```markdown
# Lean Analysis Report: [Subject Name]

## Executive Summary
[2-3 sentence overview of the analysis and key findings]

## Phase Results
### Phase 1: Lean Foundations — [key finding]
### Phase 2: Story Interview — [key finding]
### Phase 3: Value Stream Mapping — [key finding]
### Phase 4: KYT — [key finding]
### Phase 5: Poka-yoke — [key finding]
### Phase 6: Shisa Kanko — [key finding]
### Phase 7: Nemawashi — [key finding]
### Phase 8: Shusa Leadership — [key finding]
### Phase 9: Yokoten — [key finding]

## Critical Actions
[Prioritized list of recommended actions from across all phases]

## Yokoten Broadcast
[Patterns to deploy horizontally]
```

Save the report as an artifact in the brain directory.
