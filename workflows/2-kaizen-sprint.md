---
description: Run a full PDCA (Plan-Do-Check-Act) continuous improvement cycle on a recurring bug, friction point, or localized process.
---

# Kaizen Sprint Workflow

Execute a rigorous **Continuous Improvement** cycle to permanently fix recurring issues, architectural friction, or inefficient workflows at the **Module / Process Level**. This workflow transforms isolated lessons into durable, standardized upgrades.

## Input

The user provides one of:
- A description of a recurring bug or failure
- A specific module or process that feels slow, brittle, or confusing
- A recent `Hansei` (Self-Reflection) that requires standardization

## Execution Phases

Run each phase sequentially. Document the findings for each phase.

---

### Phase 1: Genchi Genbutsu (Fact Gathering)
**Skill:** `genchi-genbutsu` | **Goal:** Go and See

1. Do not assume the cause of the issue. **Run empirical tests** to observe the failure or friction first-hand.
2. Gather raw execution logs, terminal output, or stack traces.
3. Establish the **Current Baseline** metrics (e.g., token usage, error rate, execution time).
4. **Output:** The verified facts of the abnormality + Baseline Metrics.

---

### Phase 2: Hansei (Root-Cause Analysis)
**Skill:** `hansei` | **Goal:** 5-Whys Drilldown

1. Apply the **5-Whys Protocol** to the facts gathered in Phase 1.
2. Drill down through the direct cause, indirect cause, systemic cause, and architectural cause to isolate the **Root Cause**.
3. Do not accept "User Error" or "AI Hallucination" — find the structural flaw.
4. **Output:** 5-Whys trace + The Isolated Root Cause.

---

### Phase 3: Kaizen (The PDCA Hypothesis)
**Skill:** `kaizen` | **Goal:** Plan a structural update

1. Formulate a small, highly targeted **Hypothesis**: "If we change X, then Y will improve, because Z."
2. Propose a structural update to a constraint, prompt, schema, or tool layer. 
3. Verify that the change is an incremental evolution, not a full rebuild.
4. **Output:** The PDCA Hypothesis + Proposed Structural Update.

---

### Phase 4: Poka-yoke (Interlock Design)
**Skill:** `poka-yoke` | **Goal:** Mistake-proofing

1. Design a deterministic, physical, or logical **Interlock** based on the PDCA hypothesis.
2. How can we make it mechanically impossible for the system to make this exact mistake again?
3. Examples: Schema validation checks, mandatory prerequisite checks, restricted state transitions.
4. **Output:** The Poka-yoke Interlock design.

---

### Phase 5: Shisa Kanko (Execution & Verification)
**Skill:** `shisa-kanko` | **Goal:** Point, Call, Evaluate

1. Execute the Kaizen plan with extreme precision.
2. Use **Genchi Genbutsu** again to execute the modified workflow or fix.
3. **Compare** the new metrics against the Baseline established in Phase 1.
4. **Output:** Test Results (Has the root cause been eliminated? Did we break any constraints?).

---

### Phase 6: Yokoten (Standardization)
**Skill:** `yokoten` | **Goal:** Horizontal Deployment

1. If Phase 5 verification succeeds: How do we permanently standardize this?
2. Update the system prompt, SKILL documentation, or standard operating procedure template.
3. Broadcast: Scan the rest of the workspace for other modules suffering from the same root cause and apply the fix.
4. **Output:** Updated Standard + Broadcast Deployment map.

---

## Final Output: Kaizen PDCA Report

After completing all 6 phases, produce the final **Kaizen PDCA Report**:

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

Save the report as an artifact in the brain directory.
