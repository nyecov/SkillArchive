---
name: gemba
version: 1.0.0
description: >
  Use to ensure situational awareness by observing the "Real Place" (the codebase). 
  Prioritizes empirical data over assumptions or model-cached knowledge.
category: lean-principles
tags: [gemba, observation, facts, reality, lean]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko-vibecoding/SKILL.md
  - name: Genchi Genbutsu (Go and See)
    path: ../genchi-genbutsu/SKILL.md
---

# Gemba (The Real Place)

Gemba is the principle of going to the actual place where value is created. For an AI agent, the "Gemba" is the filesystem and the runtime environment. This skill prevents "Hallucination-by-Assumpton" by mandating direct observation of the source code.

## Core Mandates

### 1. Direct Observation
- **Action:** The agent MUST read the actual content of a file or directory before making any statement about its state or contents.
- **Constraint:** NEVER rely on "memory" of a file from a previous turn or guess its structure based on its name.
- **Integration:** Acts as a prerequisite for **Nemawashi** and **Poka-Yoke**.

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
