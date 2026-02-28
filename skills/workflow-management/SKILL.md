---
name: workflow-management
version: 1.0.0
level: methodology
description: 'Use when creating, reviewing, or managing workflows. Ensures workflows meet the structural standards and prevents documentation bloat.'
category: meta
tags: [meta, architecture]
references:
  - name: Skill Authoring Management
    path: ../skill-authoring-management/SKILL.md
  - name: Story Interview
    path: ../story-interview/SKILL.md
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko/SKILL.md
---

# Workflow Management

Workflows are structurally and procedurally distinct from skills, despite sharing the Markdown medium. This skill acts as the Gold Standard enforcing mechanism for the `workflows/` directory, preventing bloat and ensuring high procedural standards.

## Core Mandates

### 1. Distinct Structural Enforcement
- **Action:** Validate any newly created or modified workflow file using `python scripts/manage_workflows.py`.
- **Constraint:** MUST NOT treat a workflow like a skill. Workflows do not use the Action/Constraint mandate pattern; they use numbered procedural steps.
- **Integration:** Aligns with **Skill Authoring Management**'s goal of preventing library rot by maintaining format integrity specific to workflows.

### 2. Auto-Correction and Recovery
- **Action:** Allow the `manage_workflows.py` deterministic script to auto-correct missing YAML frontmatter or structural formatting errors when possible.
- **Constraint:** If a workflow is logically unrecoverable (e.g., lacks procedural steps or coherent goals), DO NOT try to guess the steps.
- **Integration:** Directly hooks into **Story Interview** for recovery.

## Escalation & Halting

- **Jidoka:** If `manage_workflows.py` fails to auto-correct a file and returns an "unrecoverable" status, halt the current agentic process to prevent saving garbage data.
- **Hō-Ren-Sō:** If a workflow is deemed unrecoverable, autonomously invoke the `story-interview` skill with the user to rebuild the workflow logic from scratch.

## Implementation Workflow

1. **Trigger:** A workflow in `.gemini/workflows/` is created or modified.
2. **Execute:** Run the `manage_workflows.py` validation Python script against the file.
3. **Verify:** Check the output of the script to ensure the file was either validated or repaired (`auto_corrected`).
4. **Output:** A standardized workflow document, or an escalated `story-interview` session.

## Poka-yoke Output Template

When the `manage_workflows.py` script validates or repairs a workflow, the agent MUST format its diagnostic report using exactly this Markdown schema:

```markdown
# Workflow Validation Report: [Workflow Name]

## 1. Action Taken
- **Status:** [validated | auto_corrected | unrecoverable]
- **Script Finding:** [Description of what the python script changed or verified]

## 2. Next Steps
- [ ] [e.g., Save and commit the file]
- [ ] [e.g., Invoke Story Interview to rebuild unrecoverable logic]
```
