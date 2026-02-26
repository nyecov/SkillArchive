---
name: Shisa Kanko Software Engineering & Vibecoding
version: 1.1.0
description: A high-integrity development workflow applying the 'Pointing and Calling' principle to AI-assisted coding. Eliminates hallucinations via intentional friction, context isolation, and multi-layered verification.
category: software-engineering
tags: [vibecoding, ai-safety, testing, shisa-kanko, agentic-workflows]
references:
  - name: Shisa Kanko Architecture Report
    url: https://docs.google.com/document/d/1TdP7WJTRgWYJJ5157Ug3vussKCUM9bU5frnkeQFeWYI/edit?usp=sharing
---

# Shisa Kanko Software Engineering & Vibecoding

This skill implements the **Shisa Kanko (Pointing and Calling)** architecture. It transforms 'vibecoding' from intuitive execution into a deterministic engineering discipline by replacing automaticity with intentional friction.

## Core Mandates

### 1. Digital Pointing (Context Isolation)
Before any modification, you MUST 'point' to the target with high precision.
- **Action:** Output a `[TARGET_ISOLATION]` block.
  - **Contents:** File path, line ranges, and the specific symbol/variable signature.
  - **Constraint:** If the code doesn't exist yet, 'point' to the exact insertion point (e.g., "After the last export in `src/utils.ts`").
- **Why:** Prevents 'lost-in-context' hallucinations and ensures the LLM is not 'guessing' where code lives.

### 2. Digital Calling (Logic & Dependency Declaration)
Never execute a tool call without 'calling out' the logic first.
- **Action:** Output a `[LOGIC_DECLARATION]` block.
  - **Contents:** **Intent** (What), **Rationale** (Why), and **Side-Effects** (Dependencies).
  - *Example:* "I am updating the `Auth` hook to use `sessionStorage`. This will break the 'Stay Logged In' feature until I migrate the storage key."
- **Why:** Forces 'System 2' reasoning, breaking the 'System 1' automaticity that leads to "rubber-stamping" errors.

### 3. The Swiss Cheese Layer (Self-Criticism)
Emulate a multi-agent workflow by performing an internal 'Critic' pass.
- **Action:** Before executing the `replace` or `write_file` tool, ask: *"If this change fails, what is the most likely reason?"* 
- **Validation:** If the risk is high (e.g., production config), you MUST propose a fallback or a rollback plan in the `[LOGIC_DECLARATION]`.

## The High-Integrity Vibecoding Workflow

### Phase A: Vibe Alignment (Intent)
1. **Define the Vibe:** State the high-level aesthetic or architectural goal (e.g., "Minimalist, functional, no external dependencies").
2. **Point:** Identify existing patterns that support this vibe.
3. **Call:** Declare how the new feature preserves or enhances this vibe without introducing "architectural rot."

### Phase B: Deterministic Implementation (Execution)
1. **Plan:** Construct the surgical update.
2. **Act:** Execute the change using the **Point -> Call -> Act** sequence.
3. **Reflect:** Immediately after the tool returns, verify the file content matches the *exact* intent.

### Phase C: Safety-First Testing (Verification)
1. **Reproduction:** You MUST point to a failing test or a reproduction script *before* the fix.
2. **Validation:** Use `run_shell_command` to verify the fix. 
3. **Double-Check:** If the test passes, "point" to the code one last time to ensure no linting errors or 'just-in-case' logic was left behind.

## Crisis Protocol: Discrepancy Found
If 'Pointing' (searching) reveals that the code is different from your internal model:
1. **Stop:** Do not proceed with the planned 'Call'.
2. **Re-Map:** Read the file again to update your mental model.
3. **Reset:** Restart the Shisa Kanko cycle from Phase A.

## Path Rules
- Internal references MUST use relative paths (e.g., `./templates/skill-template.md`).
- External resources MUST use absolute URLs.
