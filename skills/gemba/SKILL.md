---
id: 60b3bfe6-d38c-455e-9b6e-0284d98d59c6
name: gemba
version: 1.3.0
level: methodology
description: Use to establish a factual baseline of the codebase and navigate unfamiliar systems. Mandates direct observation before reasoning and enforces structured discovery via tactical scanning and symbol-driven mapping.
category: cognition
tags:
- context
- methodology
- research
- lean
- TPS
- exploration
- codebase
- search
- engineering
references:
- name: context-engine
  path: ../context-engine/SKILL.md
- name: shisa-kanko
  path: ../shisa-kanko/SKILL.md
- name: Genchi-Genbutsu
  path: ../genchi-genbutsu/SKILL.md
- name: Root Cause Isolation
  path: ../root-cause-isolation/SKILL.md
- name: Refactor Safely
  path: ../refactor-safely/SKILL.md
- name: Gemba Report Template
  path: ./templates/gemba-report-template.md
requires:
- context-engine
---
# Gemba (The Real Place)

Gemba is the "Real Place." This skill mandates that the agent establish a verified factual baseline before any reasoning. It orchestrates tactical discovery and enforces a rigid output reporting structure to avoid assumptions.

## Core Mandates

### 1. Scan Before Reading
- **Action:** Start with high-level directory listing (`list_directory`) at the repo root to understand the macro-architecture. Then use glob patterns to see file distribution.
- **Constraint:** NEVER open a full file before knowing where the relevant section is. Use grep to locate the section first, then read with start/end line bounds.
- **Integration:** Ensures you observe the actual structure before drawing conclusions.

### 2. Symbol-Driven Discovery
- **Action:** Use grep to find interface definitions, struct declarations, function signatures, and import statements. Follow the dependency graph by tracing `import` chains rather than reading files sequentially.
- **Constraint:** Do not read implementation details until the interface/contract is understood.
- **Integration:** Supports **Root Cause Isolation** — understand dependencies before changing them.

### 3. Surgical Reads
- **Action:** Always provide start and end line bounds when reading files over 100 lines. Read only the section relevant to the current question.
- **Constraint:** Do not read entire files "just in case." If a file needs to be read in full, it must be under 100 lines.
- **Integration:** Enforces **Heijunka** token efficiency — avoid context overburden.

### 4. Discovery Mode Selection
- **Action:**
  - **Local/Direct (Gemba):** Reading known files (`read_file`).
  - **Global/Structural/Session (Context Engine):** Using MCP tools for searching, graph querying, and findings (`context-engine`).
- **Constraint:** NEVER guess a file path or a symbol's usage. 

### 5. Fact Verification (Genchi Genbutsu)
- **Action:** Read the actual content of the discovered file or record the tool's raw output.
- **Constraint:** DO NOT rely on cached summaries or previous-turn assumptions. All discovery MUST culminate in a formal Gemba Discovery Report.

## Exploration Workflow

1. **High-Level Scan** — List root directory and key subdirectories to understand layers (domain, application, infrastructure).
2. **Deep Discovery** — Use glob patterns to see file distribution across the workspace.
3. **Symbol Search** — Grep for interface definitions, key types, or core structs.
4. **Dependency Mapping** — Grep for import statements to understand package relationships.
5. **Fact Verification** — Read only the relevant sections of the identified files.

## Escalation & Halting

- **Jidoka:** If a file's content contradicts the user's description or if the codebase structure is inconsistent with documentation, trigger a Jidoka halt.
- **Hō-Ren-Sō:** Report any "Hidden Waste" (unused code, broken links) discovered during the observation.

## Output: Gemba Discovery Report

A task is not complete until it has been empirically verified. You MUST output the `Gemba Discovery Report` using the template.

[Gemba Report Template](./templates/gemba-report-template.md)
