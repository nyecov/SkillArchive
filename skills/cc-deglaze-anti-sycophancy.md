---
name: Deglaze (Anti-Sycophancy Protocol)
version: 1.0.0
description: >
  Use when reviewing AI-generated solutions, validating user comprehension, or stress-testing proposals.
  Handles 5 constraint-pressure techniques: Compression, Deletion, Adversary, Explain-to-Junior, and Rollback tests.
category: cognition
tags: [deglaze, anti-sycophancy, constraint-pressure, critical-thinking, crowd-control]
references:
  - name: Crowd Control (Source Repo)
    url: https://github.com/newsbubbles/crowd_control
  - name: CC — Comprehend (Understanding Gate)
    path: ./cc-comprehend-understanding.md
  - name: CC — Anchor (Architectural Coherence)
    path: ./cc-anchor-coherence.md
  - name: CC — Circuit (Iteration Breaker)
    path: ./cc-circuit-iteration-breaker.md
  - name: CC — Isolate (Systematic Debugging)
    path: ./cc-isolate-debugging.md
  - name: CC — Secure (Security)
    path: ./cc-secure-security.md
  - name: CC — Ship (Production Readiness)
    path: ./cc-ship-production.md
  - name: Hansei (Self-reflection)
    path: ./hansei-self-reflection.md
---

# Deglaze: Anti-Sycophancy Protocol

*Strip the polish. Reveal the substrate.*

Deglaze combats "glaze" — the false sense of understanding that forms when AI-generated solutions look clean and work on the happy path, but the user cannot explain *why* they work. Experienced practitioners unconsciously apply **constraint pressure** — questions that force ideas into hard edges. This skill makes that pressure explicit.

## Core Mandates: The Five Pressure Techniques

### 1. The Compression Test
- **Method:** Ask the user to explain their solution in one sentence without jargon.
- **Why it works:** Glaze dissolves under compression. If they can't compress it, they don't understand it.
- **Red flags:** "It's complicated, but basically…", restating the problem instead of the solution, describing *what* without *why*.

### 2. The Deletion Test
- **Method:** "What happens if we remove [component X]?"
- **Why it works:** Forces understanding of dependencies. Glazed solutions have components that "feel necessary" but aren't.
- **Red flags:** "I'm not sure, let me check", "The AI added that, I think it's important", inability to trace data flow.

### 3. The Adversary Test
- **Method:** "If someone wanted to break this, how would they?"
- **Why it works:** Shifts from construction to destruction. Exposes assumptions.
- **Red flags:** "I hadn't thought about that", "The AI handled security", no answer beyond "they'd need access."
- **Integration:** Maps directly to **KYT (Hazard Prediction)** Round 1 — identifying the hazard from an adversarial angle.

### 4. The Explain-to-Junior Test
- **Method:** "Explain this to someone who's never seen the codebase."
- **Why it works:** Forces externalization of mental model. Reveals gaps.
- **Red flags:** Starting with implementation details instead of purpose, "You'd need to understand [other thing] first", circular explanations.

### 5. The Rollback Test
- **Method:** "If this fails in production at 3am, how do we revert?"
- **Why it works:** Forces operational thinking. Exposes deployment assumptions.
- **Red flags:** "We'd just fix it", no rollback strategy, "It won't fail."
- **Integration:** Mirrors the **Hansei (Self-reflection)** proactive review — identifying failure modes before they materialize.

## When to Apply Deglaze

**Apply aggressively when:**
- User is excited about an AI-generated solution
- Solution came together "too easily"
- User can't explain why it works
- Architecture was built incrementally via prompts
- User says "the AI suggested this approach"

**Apply gently when:**
- User has demonstrated understanding
- Solution matches established patterns
- User can trace data flow confidently
- User has already stress-tested the design

## Implementation Workflow

1. **Trigger:** New solution proposed or AI-generated code accepted.
2. **Pressure:** Run the five techniques in sequence (Compression → Deletion → Adversary → Explain → Rollback).
3. **Assess:** If 3+ techniques reveal gaps, flag for deeper review.
4. **Escalate:** Feed findings into **Hansei** for root-cause reflection, or **Comprehend** for the understanding gate protocol.

## Quick Reference

```
DEGLAZE CHECKLIST:
□ Can user explain it in one sentence?
□ Can user identify what to delete?
□ Can user describe how to break it?
□ Can user explain it to a newcomer?
□ Can user describe the rollback plan?

If 3+ boxes are unchecked → deeper review needed
```
