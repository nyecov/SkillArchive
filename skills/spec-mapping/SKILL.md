---
id: 1b3d5f7a-9c2e-4b6d-8f0a-2c4e6b8d0f2a
name: spec-mapping
version: 1.0.0
level: tactical
description: 'Use when mapping a spec document into the SDLC backlog as epics + stories
  with a coverage ledger. CLI-neutral, append-only, anti-hallucination workflow with
  strict convergence (two consecutive zero-new-item gap sweeps). TRIGGER when asked
  to map, carve, ground, or sweep a spec into the backlog, or to run a gap-sweep against
  an existing mapping.'
category: methodology
tags:
- agile
- spec
- mapping
- backlog
- methodology
references:
  - name: Agile Backlog Authoring
    path: ../agile-backlog/SKILL.md
  - name: Agile SDLC Orchestrator
    path: ../agile-sdlc/SKILL.md
---
# Spec Mapping: Surgical Carving & Convergence Workflow

Maps spec documents into the SDLC backlog as traceable epics and stories. Prevents context drowning and hallucination through micro-batching, surgical reads, and a persistent coverage ledger.

## The Convergence Ledger (`.map-spec/<slug>/`)

For every spec source file being mapped, create a ledger directory:

1. `coverage.md` — Checklist of all headers/sections with mapping status: `MAPPED`, `STAGED`, `IGNORED`.
2. `SPEC-GAPS.md` — Running task list and session state (current position, blind pass log, cross-spec findings).

## Core Mandates

### 1. Oracle Discipline (Anti-Hallucination)
- **Action:** The spec file is the Oracle. Every AC created MUST cite the source section (e.g., `cite: spec/Solver.md#Phase-4`). Never guess or infer logic not stated in the spec.
- **Constraint:** If the spec is vague or contradictory, record the ambiguity in `SPEC-GAPS.md` and file an ISSUE for the analyst. Do not hallucinate intent.
- **Integration:** Implements **Genchi Genbutsu** — only map what is actually observed in the source, not what is assumed.

### 2. Surgical Reading
- **Action:** Never read a dense spec file in its entirety. Use `grep` with line numbers to locate sections, then read only the targeted range.
- **Constraint:** Do not load files over 200 lines without first identifying the specific range needed. Token waste from bulk reads is a **Muri** violation.
- **Integration:** Supports **Heijunka** — level the read load by batching only what fits in the current turn.

### 3. Micro-Batching (Resilience)
- **Action:** Commit and return control after every 3–5 stories or 1 major header. Update `SPEC-GAPS.md` before every commit so the next session can resume exactly where this one stopped.
- **Constraint:** Do NOT map an entire spec file in one turn. If context is approaching limits, checkpoint and stop cleanly.
- **Integration:** Prevents turn-limit failures and enables multi-agent handover without rework.

### 4. Convergence Goal
- **Action:** Mapping is only "Done" when two consecutive blind-pass gap sweeps produce zero new items. Each sweep must scan for required keywords (MUST, SHALL, Rule:, Mandate:) and verify every instance is covered by an AC.
- **Constraint:** Do not mark a spec slug as `Healthy` without two zero-new-item rows in the `## Blind Pass Log`.
- **Integration:** Enforces a deterministic done-state — prevents premature closure.

## Workflow: The Carving Loop

1. **Initialize / Resume** — Read `.map-spec/<slug>/SPEC-GAPS.md`. Identify the current scalpel position. If no ledger exists, create it by scanning the spec's table of contents.
2. **Carve** — Identify the next unmapped section. Read it surgically (targeted line range). Create or update the matching Epic/Story in the backlog with an AC citing the spec section.
3. **Checkpoint** — Mark the section as `MAPPED` in `coverage.md`. Update `SPEC-GAPS.md`. Run spec-link validation. Commit changes.
4. **Gap Sweep (Blind Pass)** — Periodically: search for unmapped critical keywords, audit `coverage.md` for `STAGED` items, append a row to the `## Blind Pass Log`, and promote cross-spec findings to the global spec-gaps rollup.

## Verification Tooling

- `Find-SpecGaps.ps1` — list unmapped spec files.
- `Search-AllArtifacts.ps1 -SpecAudit` — find unmapped critical-keyword requirements.
- `coverage.py carving` — comprehensive coverage metrics.
- `Validate-SpecLinks.ps1` — verify all citation anchors resolve.

## Escalation & Halting

- **Jidoka:** If the spec is self-contradictory or a section cannot be mapped without assumptions, halt, file an ISSUE routed to Analyst, and mark the section as `STAGED` with a note.
- **Ho-Ren-So:** Report the blind-pass count and current coverage percentage at the end of every mapping turn.

## Implementation Workflow

1. **Trigger:** A spec document needs to be translated into a backlog, or a coverage audit is requested.
2. **Execute:** Initialize or resume the ledger. Carve 3–5 stories. Checkpoint. Repeat until two consecutive zero-new-item gap sweeps.
3. **Verify:** `coverage.md` shows 100% MAPPED. Blind Pass Log has two consecutive zero-new-item rows. All citation links valid.
4. **Output:** A fully mapped spec slug with a healthy ledger, ready for `agile-sdlc` Planning stage sign-off.
