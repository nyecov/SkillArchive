---
id: 8dea8b48-658e-4d46-bd01-42deef7c3b1a
name: architectural-anchoring
version: 1.2.0
description: Use when making architectural decisions, enforcing layer boundaries, or when AI-suggested changes conflict with established patterns. Mandates ANCHOR.md enforcement, ADR logs, and Clean Architecture layer rules.
category: engineering
tags:
- design
- architecture
- agile
- clean-architecture
- methodology
references:
- name: Crowd Control (Source Repo)
  url: https://github.com/newsbubbles/crowd_control
- name: CC — Deglaze (Anti-Sycophancy)
  path: ../logic-deglazing/SKILL.md
- name: CC — Comprehend (Understanding Gate)
  path: ../comprehension-gate/SKILL.md
- name: CC — Circuit (Iteration Breaker)
  path: ../jidoka/SKILL.md
- name: CC — Isolate (Systematic Debugging)
  path: ../root-cause-isolation/SKILL.md
- name: CC — Secure (Security)
  path: ../security-enforcement/SKILL.md
- name: CC — Ship (Production Readiness)
  path: ../release-management/SKILL.md
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Refactor Safely
  path: ../refactor-safely/SKILL.md
- name: Code Review
  path: ../code-review/SKILL.md
- name: Anchor Template
  path: ./templates/anchor-template.md
level: tactical
---
# Architecture & Anchoring

*Drift is the default. Coherence requires intention.*

This skill ensures the system maintains structural integrity by enforcing Clean Architecture, reviewing interface contracts, and anchoring decisions in the `ANCHOR.md` artifact and ADR (Architecture Decision Record) log.

## Clean Architecture Layer Rules

Dependencies point inward only: Infrastructure → Application → Domain. Never the reverse.

| Layer | Allowed Imports | Forbidden Imports |
|---|---|---|
| Domain | Other domain packages only | Application, Infrastructure, DB drivers, HTTP, SDK |
| Application | Domain interfaces | Infrastructure concretes, DB drivers |
| Infrastructure | Domain interfaces, Application ports | Direct domain business logic |

## Core Mandates

### 1. Artifact Enforcement: The ANCHOR.md Reality
Every project MUST possess an authoritative `ANCHOR.md` document at the project root.
- **Action:** If it doesn't exist, create it. If it does, read it before proceeding.
- **Constraint:** NEVER proceed with a multi-pattern implementation or rely on conversational memory for architecture. 

### 2. Interface-First Design & ADR Discipline
- **Action:** Before any major feature, define or review interface contracts. Every approved architectural change must have an entry in the ADR log.
- **Constraint:** No net-new cross-layer dependency may be introduced without an ADR entry. Intent decays without documentation.
- **Integration:** Connects to **Nemawashi** — get consensus before structural changes.

### 3. Drift Enforcement
Catch and resist drift when patterns are suggested that contradict anchors or Clean Architecture rules.
- **Action:** Compare every proposed implementation against `ANCHOR.md` and the layer import rules.
- **Constraint:** Reject changes that introduce architectural rot or "Hybrid Rot" (inconsistent patterns).

### 4. Decisions Log (ADR) Integrity
- **Action:** Entries must include: the decision, alternatives considered, rationale, and tradeoffs.
- **Integration:** Feeds **Yokoten** — future teams learn from archived decisions.

## Clean Architecture Review Checklist

Walk this for every PR touching domain, application, or infrastructure layers:

- [ ] No outward imports from Domain (no infrastructure or framework types in domain)
- [ ] No business rules in Application (orchestration only, no domain logic)
- [ ] Infrastructure implements Domain interfaces, not concretes
- [ ] Interface segregation: consumers use >30% of a port's methods; split if not
- [ ] No leaky types crossing layers (DB row types, HTTP request types, SDK structs)
- [ ] Construction at the composition root edge, not inside Domain constructors
- [ ] Errors carry domain meaning (infrastructure errors wrapped, not propagated raw)

## Escalation & Halting

- **Jidoka:** If an implementation requires violating an anchor or a checklist item to function, trigger a Jidoka halt.
- **Hō-Ren-Sō:** Use Sōdan (Consult) if a proposed feature requires an architectural shift that contradicts `ANCHOR.md`.

## Execution Flow

1. **Trigger:** Start of a project, architectural decision point, or prior to major feature implementation.
2. **Execute:** Audit `ANCHOR.md` → Apply Clean Architecture checklist → Log decision in ADR.
3. **Verify:** Check every change specifically against the constraints documented in `ANCHOR.md` and the layer rules.
4. **Output:** An updated, authoritative `ANCHOR.md` artifact and a coherent implementation path.

