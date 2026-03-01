---
name: external-synthesis
version: 1.1.0
level: methodology
description: Use when researching new agent skills. Guides the agent to search external repositories and synthesize patterns into a structured research report for handoff to skill authoring.
category: meta
tags:
- meta
- research
references:
- name: skill-authoring-management
  path: ../skill-authoring-management/SKILL.md
- name: Claude Cookbook
  url: https://platform.claude.com/cookbook/
- name: Clawhub (Skills)
  url: https://clawhub.ai/skills?sort=downloads
requires:
- skill-authoring-management
---

# External Synthesis

A skill for extending the internal knowledge base by discovering and analyzing established patterns from the global agent ecosystem. This skill acts strictly as a **Research Report Generator** and acts as the precursor to `skill-authoring-management`. 

## Core Mandates

### 1. Mandatory External Discovery
Perform a thorough search of external reference points before drafting a new skill to leverage existing community patterns.
- **Action:** Visit the Claude Cookbook and Clawhub to identify similar procedures or architectural patterns.
- **Constraint:** DO NOT blindly copy-paste; evaluate external content for compatibility with local architecture.

### 2. Analytical Synthesis (Report Generation ONLY)
Extract core logic, tool-use patterns, and failure modes from external examples and abstract them into a portable report.
- **Action:** Identify the "delta" between community solutions and the current project needs.
- **Constraint:** DO NOT author or modify `SKILL.md` files directly. This skill ONLY produces research data. Attempting to directly author skills without invoking `skill-authoring-management` is a policy violation (Context Collision Hazard).
- **Integration:** The output of this skill acts as the input payload for the "Research" phase of **skill-authoring-management**.

### 3. Source Citation
Maintain transparency and traceability by documenting the origins of synthesized logic.
- **Action:** Explicitly list external sources in the final report.
- **Constraint:** Do not present external logic as "original" without identifying the foundational source.

## Escalation & Halting

- **Jidoka:** If external resources are found that are highly complex and incompatible with local tools, halt and ask the user if they'd prefer to simplify the logic before proceeding to authoring.
- **Hō-Ren-Sō:** Report findings to the user summary: "Found similar pattern on Clawhub; synthesized core logic into research report."

## Implementation Workflow

1. **Trigger:** Activated during the initial research phase of a new skill request.
2. **Execute:** 
    - Use `web_fetch` or `google_web_search` to query `clawhub.ai` for the specific skill topic.
    - Browse the `Claude Cookbook` for architectural patterns related to the task.
    - Analyze the external skill (Is it procedural? What tools does it use? What are the edge cases?).
3. **Verify:** Confirm the extracted logic resolves the user's need and does not rely on unavailable bespoke external tools.
4. **Output:** You MUST stop modifying the file system and output the following exact template to be handed off to the authoring process:

```markdown
### External Research Report
- **[SOURCE LINKS]:** 
  - `[URLs to Clawhub/Cookbook/etc.]`
- **[CORE LOGIC EXTRACTED]:** 
  - `[The underlying procedural pattern, abstracted from specific foreign code]`
- **[IDENTIFIED EDGE CASES]:** 
  - `[Failure modes handled by the external source]`
- **[TOOL DEPENDENCIES]:** 
  - `[Required tool classes the pattern relies upon]`
```
