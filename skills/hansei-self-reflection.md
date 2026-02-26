---
name: Hansei (Self-reflection)
version: 1.0.0
description: Deep, honest self-reflection to acknowledge mistakes and develop improvement plans. Used for iterative refinement of agentic plans.
category: cognition
tags: [hansei, reflection, iterative-refinement, cognitive-bias]
---

# Hansei: Agentic Self-Reflection

Hansei is the practice of looking back at a plan or action with a critical eye to identify flaws and areas for improvement.

## Core Mandates

### 1. Objective Acknowledgment
The agent MUST acknowledge any flaws in its initial reasoning without defensiveness.
- **Action:** Run a 'Reflection Pass' after generating a plan but *before* execution.
- **Prompt:** "Identify three ways this plan could fail or lead to a sub-optimal outcome."

### 2. Root Cause Analysis
Identify *why* a flaw exists, not just that it exists.
- **Action:** Trace the flaw back to a specific assumption, missing piece of context, or logical leap.

### 3. Improvement Planning
Create a revised plan that incorporates the findings from the reflection.
- **Action:** Regenerate the plan with explicit 'Countermeasures' for the identified risks.

## Implementation Workflow

1. **Draft:** Generate the initial plan (The 'Idea').
2. **Reflect (Hansei):** Critically analyze the draft for flaws.
3. **Refine:** Produce the 'Final Plan' based on the reflection.
4. **Learn:** Document what was learned for future similar tasks.
