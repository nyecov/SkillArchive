---
name: skill-name-id
version: 1.0.0
level: methodology | tactical | technical
description: A brief description of the skill's purpose and how it integrates with the broader agentic architecture.
category: general
tags: [tag1, tag2]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko/SKILL.md
---

# Skill Name


A concise paragraph explaining the skill's role in the agentic system and how it relates to other Lean principles.

## Core Mandates

### 1. First Mandate
- **Action:** What the agent MUST do.
- **Constraint:** What the agent MUST NOT do.
- **Integration:** How this mandate connects to other skills (e.g., Poka-yoke, Jidoka, Hansei).

### 2. Second Mandate
- **Action:** …
- **Constraint:** …
- **Integration:** …

## Escalation & Halting

- **Jidoka:** Under what conditions this skill triggers an autonomous halt.
- **Hō-Ren-Sō:** How findings or failures are communicated to the human operator.

## Implementation Workflow

1. **Trigger:** What initiates this skill.
2. **Execute:** The core steps.
3. **Verify:** How success is confirmed.
4. **Output:** What is produced and where it feeds into the system.

## Poka-yoke Output Template (Optional)

If this skill generates a formal report, code scaffold, or structured data output, explicitly define the strict Markdown or JSON schema here.

```markdown
# [Output Title]

## 1. [Section Name]
- **[Data Point]:** [Description]
```
