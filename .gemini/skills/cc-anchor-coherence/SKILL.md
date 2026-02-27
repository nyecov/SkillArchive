---
name: cc-anchor-coherence
version: 1.0.0
description: >
  Use when starting a project, making architectural decisions, or when AI-suggested changes conflict with established patterns.
  Handles anchor document creation, drift detection, anchor audits, and deliberate evolution of design decisions.
category: engineering-standards
tags: [anchor, architecture, coherence, drift-prevention, crowd-control]
references:
  - name: Crowd Control (Source Repo)
    url: https://github.com/newsbubbles/crowd_control
  - name: CC — Deglaze (Anti-Sycophancy)
    path: ../cc-deglaze-anti-sycophancy/SKILL.md
  - name: CC — Comprehend (Understanding Gate)
    path: ../cc-comprehend-understanding/SKILL.md
  - name: CC — Circuit (Iteration Breaker)
    path: ../cc-circuit-iteration-breaker/SKILL.md
  - name: CC — Isolate (Systematic Debugging)
    path: ../cc-isolate-debugging/SKILL.md
  - name: CC — Secure (Security)
    path: ../cc-secure-security/SKILL.md
  - name: CC — Ship (Production Readiness)
    path: ../cc-ship-production/SKILL.md
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko-vibecoding/SKILL.md
---

# Anchor: Architectural Coherence

*Drift is the default. Coherence requires intention.*

An **anchor** is an explicit architectural decision that resists prompt pressure. Once anchored, the decision holds until deliberately changed. The AI will happily introduce a fourth state management approach if you let it — it's not malicious, it just doesn't remember the first three. This skill makes you the architectural memory the LLM lacks.

## Core Mandates

### 1. Establish Anchors Early
Every project needs an anchor document — it doesn't need to be long, it needs to be **authoritative**.

- **Key domains to anchor:**

| Domain | Anchor Examples |
|--------|----------------|
| **State** | "State lives in [X]. Components read via [Y]." |
| **Auth** | "Auth uses [approach]. Tokens stored in [location]." |
| **Data** | "Database is [X]. ORM is [Y]. Queries go through [Z]." |
| **API** | "Endpoints follow [pattern]. Errors return [format]." |
| **Files** | "Components in /components. Utils in /utils. No exceptions." |

- **Integration:** The Anchor Document is the reference artifact for **Shisa Kanko** Precise Pointing (Mandate 1) — it defines what "correct" looks like.

### 2. Enforce Anchors During Implementation
- **Before Implementation:** Does this change align with existing anchors?
- **During Implementation:** Catch drift when AI suggests something that contradicts anchors.
- **After Implementation:** Audit the new code against anchors.

### 3. Evolve Anchors Deliberately
Anchors are not forever. When they need to change, change them **deliberately** — not as a side effect of a prompt-driven implementation.

## Anchor Hygiene

### Signs of Anchor Rot
- "I'm not sure which pattern to use here"
- Multiple ways to do the same thing
- New code doesn't match old code style
- "The AI suggested a different approach"

### The Anchor Audit
Periodically (every major feature, or weekly), audit anchors:
```
ANCHOR AUDIT:
□ State management consistent across codebase?
□ Auth approach uniform?
□ API patterns followed?
□ File structure respected?
□ Any new patterns that should be anchored?
```

## When Anchors Conflict
If a proposed change conflicts with an anchor:
1. **Stop** — do not silently override the anchor.
2. **Evaluate** — is the anchor outdated, or is the change wrong?
3. **Decide** — update the anchor deliberately, or reject the change.
4. **Document** — if the anchor changes, update the anchor document immediately.

## Implementation Workflow

1. **Trigger:** Start of project or any architectural decision point.
2. **Establish:** Create or update the anchor document for the affected domain.
3. **Enforce:** Check every change against existing anchors before, during, and after.
4. **Evolve:** When anchors need updating, do it deliberately and document the change.

## Quick Reference

```
ANCHOR CHECKLIST:
□ Does project have anchor document?
□ Does this change align with anchors?
□ Is AI suggesting something that contradicts anchors?
□ Should we update anchors (deliberate) or resist drift?

KEY DOMAINS TO ANCHOR:
- State management
- Authentication
- Data/database patterns
- API design
- File structure
- Error handling
- Testing approach
```
