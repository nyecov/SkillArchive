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

### 1. Anchor Establishment
Every project needs an authoritative anchor document that resists prompt pressure.
- **Action:** Identify key domains (State, Auth, Data, API, Files) and document the "Sovereign Decision" for each.
- **Constraint:** NEVER proceed with a multi-pattern implementation. Choose one and anchor it.
- **Integration:** The Anchor Document serves as the "Ground Truth" for **Shisa Kanko** pointing.

### 2. Drift Enforcement
Catch and resist drift when the AI suggests patterns that contradict anchors.
- **Action:** Compare every proposed implementation against the anchor document.
- **Constraint:** Do not silently override anchors. Reject changes that introduce architectural rot.
- **Integration:** Use **KYT** to identify if a change poses a risk to architectural coherence.

### 3. Deliberate Evolution
Update anchors intentionally, not as a side effect of a feature implementation.
- **Action:** When an anchor becomes a bottleneck, explicitly update the anchor document and refactor affected areas.
- **Constraint:** Anchors MUST be updated globally or not at all to prevent "Hybrid Rot."
- **Integration:** Use **Kaizen** to manage the evolution of anchors.

## Escalation & Halting

- **Jidoka:** If an implementation requires violating an anchor to function, trigger a Jidoka halt.
- **Hō-Ren-Sō:** Use Sōdan (Consult) if a proposed feature requires an architectural shift that contradicts existing anchors.

## Implementation Workflow

1. **Trigger:** Start of a project or any architectural decision point.
2. **Execute:** Establish or audit the anchor document for the affected domain.
3. **Verify:** Check every change against existing anchors before, during, and after.
4. **Output:** A coherent codebase and an updated, authoritative anchor document.

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
