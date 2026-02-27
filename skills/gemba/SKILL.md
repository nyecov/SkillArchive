---
name: gemba
version: 1.0.0
description: >
  Use to ensure situational awareness by observing the "Real Place" (the codebase). 
  Prioritizes empirical data over assumptions or model-cached knowledge.
category: cognition
tags: [gemba, observation, facts, reality, lean]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko/SKILL.md
  - name: Genchi Genbutsu (Go and See)
    path: ../genchi-genbutsu/SKILL.md
---

# Gemba (Static Observation)

Gemba is the principle of going to the actual place where value is created. For an AI agent, the "Gemba" is the filesystem. This skill mandates **Static Observation** of the source code to prevent "Hallucination-by-Assumption."

## Core Mandates

### 1. Static Observation
- **Action:** The agent MUST read the actual bytes of a file or directory before making any statement about its state or contents.
- **Constraint:** NEVER rely on "memory" of a file from a previous turn. Use `read_file`, `list_directory`, and `grep_search` to gather the facts.
- **Integration:** Provides the factual baseline for **Nemawashi** and **Poka-Yoke**. Use **Genchi Genbutsu** for verifying the dynamic behavior of this code.

### 2. Situational Awareness
- **Action:** When entering a new directory or module, perform a "Walk the Floor" (listing files, reading READMEs, checking `package.json` or equivalent) to understand the local context.
- **Constraint:** Do not make surgical changes until the surrounding "Environment" (contextual lines of code) is fully understood.
- **Integration:** Works with **3M/5S** to ensure the workspace is "Organized" (well-understood) before work begins.

## Escalation & Halting

- **Jidoka:** If a file's content contradicts the user's description or the model's prediction, halt and perform a deeper "Gemba Walk" (search/read) to resolve the discrepancy.
- **Hō-Ren-Sō:** Report any "Hidden Waste" (unused code, broken links, outdated comments) discovered during the observation.

## Implementation Workflow

1. **Trigger:** Every new task or new module interaction.
2. **Execute:** 
   - `list_directory` to see the structure.
   - `read_file` to see the actual implementation.
   - `grep_search` to see the usage context.
3. **Verify:** Confirm that the internal model of the code matches the bytes on disk.
4. **Output:** A verified factual basis for all subsequent reasoning.
