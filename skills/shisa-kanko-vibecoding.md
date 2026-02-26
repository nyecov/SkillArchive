---
name: Shisa Kanko Software Engineering & Vibecoding
version: 1.2.0
description: A high-integrity development workflow applying the 'Pointing and Calling' principle to AI-assisted coding. Eliminates hallucinations via intentional friction, context isolation, and pre-mortem validation.
category: software-engineering
tags: [vibecoding, ai-safety, testing, shisa-kanko, agentic-workflows]
references:
  - name: Shisa Kanko Architecture Report
    url: https://docs.google.com/document/d/1TdP7WJTRgWYJJ5157Ug3vussKCUM9bU5frnkeQFeWYI/edit?usp=sharing
---

# Shisa Kanko Software Engineering & Vibecoding

This skill implements the **Shisa Kanko (Pointing and Calling)** architecture. It transforms 'vibecoding' from intuitive execution into a deterministic engineering discipline by replacing automaticity with intentional friction.

## Core Mandates

### 1. Precise Pointing (Isolation)
Before any modification, you MUST 'point' to the target with high precision to lock the context.
- **Action:** Output a `[TARGET_ISOLATION]` block.
  - **Contents:** File path, line ranges, and the **Exact Code Snippet** being replaced.
  - **Constraint:** Use the `read_file` tool immediately before this to ensure zero drift.
- **Why:** Prevents 'lost-in-context' hallucinations and ensures the target hasn't moved or changed.

### 2. Explicit Calling (Intent & Success Criteria)
Never execute a tool call without 'calling out' the expected outcome and verification method.
- **Action:** Output a `[LOGIC_DECLARATION]` block.
  - **Intent:** What is the specific code change?
  - **Success Criteria:** What *exactly* must happen for this to be considered successful?
  - **Validation Method:** What command or visual check will verify the success? (e.g., `npm test`, `ls -l`).
- **Why:** Forces 'System 2' reasoning and defines the finish line before the race starts.

### 3. Pre-Mortem (The Swiss Cheese Layer)
Emulate a multi-agent workflow by performing a risk assessment.
- **Action:** In the `[LOGIC_DECLARATION]`, include a `[RISK_ASSESSMENT]` line.
  - **Question:** "If this change causes a regression, where is the most likely failure point?"
  - **Mitigation:** What is the immediate recovery step?

## The High-Integrity Vibecoding Workflow

### Phase A: Vibe Alignment (Intent)
1. **Define the Vibe:** State the architectural goal (e.g., "Modular, typed, side-effect free").
2. **Point:** Identify existing patterns that support this vibe.
3. **Call:** Declare how the new feature preserves this vibe.

### Phase B: Deterministic Execution
1. **Point:** Isolate the target (Phase 1).
2. **Call:** Declare the logic and risk (Phase 2 & 3).
3. **Act:** Execute the surgical update.
4. **Point (Re-verify):** Read the file back to ensure the replacement was perfect.

### Phase C: Multi-Sensory Verification
1. **Reproduction:** Point to a failing test or broken state.
2. **Execution:** Apply the fix.
3. **Validation:** Run the validation command defined in 'Calling'.
4. **Vibe Audit:** Confirm the output (logs, UI, or structure) *feels* correct and aligns with the Vibe Check.

## The "Red Stop" Protocol (HITL Trigger)
You MUST stop and ask the user for confirmation if:
1. **Discrepancy:** 'Pointing' reveals the codebase differs from your internal model.
2. **High Risk:** The `[RISK_ASSESSMENT]` identifies a failure mode that is unrecoverable or affects core authentication/security.
3. **Vibe Decay:** The only way to implement the feature requires "hacking" around the established architectural vibe.

## Path Rules
- Internal references MUST use relative paths (e.g., `./templates/skill-template.md`).
- External resources MUST use absolute URLs.
