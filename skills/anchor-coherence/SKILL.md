---
name: anchor-coherence
version: 1.1.0
description: Use when starting a project, making architectural decisions, or when AI-suggested changes conflict with established patterns. Mandates the creation and enforcement of the ANCHOR.md artifact.
category: engineering
tags:
- design
- architecture
references:
- name: Crowd Control (Source Repo)
  url: https://github.com/newsbubbles/crowd_control
- name: CC — Deglaze (Anti-Sycophancy)
  path: ../deglaze-tactics/SKILL.md
- name: CC — Comprehend (Understanding Gate)
  path: ../comprehend-understanding/SKILL.md
- name: CC — Circuit (Iteration Breaker)
  path: ../jidoka/SKILL.md
- name: CC — Isolate (Systematic Debugging)
  path: ../isolate-debugging/SKILL.md
- name: CC — Secure (Security)
  path: ../secure-security/SKILL.md
- name: CC — Ship (Production Readiness)
  path: ../ship-production/SKILL.md
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Anchor Template
  path: ./templates/anchor-template.md
level: tactical
---

# Anchor

*Drift is the default. Coherence requires intention.*

An **anchor** is an explicit architectural decision that resists prompt pressure. Once anchored, the decision holds until deliberately changed. The AI will happily introduce a fourth state management approach if you let it — it's not malicious, it just doesn't remember the first three. This skill makes you the architectural memory the LLM lacks.

## Core Mandates

### 1. Artifact Enforcement: The ANCHOR.md Reality
Every project MUST possess a physical, authoritative `ANCHOR.md` document located at the project root.
- **Action:** If it doesn't exist, create it. If it does exist, read it before proceeding.
- **Constraint:** NEVER proceed with a multi-pattern implementation or rely on conversational memory for architecture. 
- **Integration:** The `ANCHOR.md` file serves as the strict "Ground Truth" for **Shisa Kanko** pointing.

### 2. Drift Enforcement
Catch and resist drift when the AI suggests patterns that contradict anchors.
- **Action:** Compare every proposed architectural implementation against `ANCHOR.md`.
- **Constraint:** Do not silently override anchors. Reject changes that introduce architectural rot.

### 3. Deliberate Evolution
Update anchors intentionally, not as a side effect of a feature implementation.
- **Action:** When an anchor becomes a bottleneck, formally update the `ANCHOR.md` document and simultaneously refactor affected areas.
- **Constraint:** Anchors MUST be updated globally or not at all to prevent "Hybrid Rot."

## Escalation & Halting

- **Jidoka:** If an implementation requires violating an anchor to function, trigger a Jidoka halt.
- **Hō-Ren-Sō:** Use Sōdan (Consult) if a proposed feature requires an architectural shift that contradicts `ANCHOR.md`.

## Implementation Strategy

### The ANCHOR.md Template
When executing this skill to establish architecture, generate `ANCHOR.md` at the project root using the standard template:
[Anchor Template](./templates/anchor-template.md)

## Execution Flow

1. **Trigger:** Start of a project, architectural decision point, or prior to major feature implementation.
2. **Execute:** Create `ANCHOR.md` using the template or audit the existing file.
3. **Verify:** Check every proposed technical change specifically against the constraints documented in `ANCHOR.md`.
4. **Output:** An updated, authoritative `ANCHOR.md` artifact and a coherent implementation path.

## Quick Reference

```
ANCHOR CHECKLIST:
□ Does ANCHOR.md exist in the project root?
□ Does this code change explicitly align with ANCHOR.md?
□ Is the AI suggesting a pattern that contradicts ANCHOR.md?
□ Are we evolving the anchor deliberately or allowing drift?
```
