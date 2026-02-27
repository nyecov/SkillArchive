---
name: external-synthesis
version: 1.0.0
description: 'Use when researching, designing, or authoring new agent skills. Guides
  the agent to search external repositories like the Claude Cookbook and Clawhub to
  identify existing patterns and synthesize them into high-quality local skills.\'
category: meta
tags:
- meta
- research
references:
- name: Skill of Skill Authoring
  path: ../skill-authoring-management/SKILL.md
- name: Claude Cookbook
  url: https://platform.claude.com/cookbook/
- name: Clawhub (Skills)
  url: https://clawhub.ai/skills?sort=downloads
level: meta
---

# Skill External Synthesis

A skill for extending the internal knowledge base by leveraging established patterns from the global agent ecosystem. This skill acts as a research phase for `skill-of-skill-authoring`, ensuring that new skills are not built in a vacuum but are synthesized from the best available community practices.

## Core Mandates

### 1. Mandatory External Discovery
Perform a thorough search of external reference points before drafting a new skill to leverage existing community patterns.
- **Action:** Visit the Claude Cookbook and Clawhub to identify similar procedures or architectural patterns.
- **Constraint:** DO NOT blindly copy-paste; evaluate external content for compatibility with the Three-Stage Loading Model.
- **Integration:** Directly informs the "Research" phase of **Skill of Skill Authoring**.

### 2. Analytical Synthesis
Extract core logic, tool-use patterns, and failure modes from external examples and adapt them to local requirements.
- **Action:** Identify the "delta" between community solutions and the current project needs.
- **Constraint:** All synthesized content MUST be transformed into a procedural, actionable workflow.
- **Integration:** Uses **Kaizen** to refine and improve upon the synthesized community patterns.

### 3. Source Citation
Maintain transparency and traceability by documenting the origins of synthesized logic.
- **Action:** Cite external sources in the `references` section of the new skill's frontmatter.
- **Constraint:** Do not present external logic as "original" without identifying the foundational source.
- **Integration:** Supports the "Shine" (Seiso) phase of **Lean Foundations** by keeping the knowledge source clear.

## Implementation Workflow

1. **Trigger:** Activated during the initial research phase of a new skill request.
2. **Search:**
    - Use `web_fetch` or `google_web_search` to query `clawhub.ai` for the specific skill topic.
    - Browse the `Claude Cookbook` for architectural patterns related to the task (e.g., "tool use", "RAG", "structured output").
3. **Analyze:**
    - Is the external skill procedural or just a prompt?
    - Does it use tools we have available?
    - What are the "Golden Paths" and "Edge Cases" it covers?
4. **Synthesize:**
    - Incorporate the best ideas into the local `SKILL.md`.
    - Cite the source in the `references` section of the new skill's frontmatter.
5. **Verify:** Confirm the new skill is more robust than the external version by applying `Poka-yoke` and `Lean` principles.

## Escalation & Halting

- **Jidoka:** If external resources are found that are strictly superior to the proposed local implementation, halt and ask the user if they'd prefer to simply reference the external source or continue with a customized local version.
- **Hō-Ren-Sō:** Report findings to the user: "Found similar pattern on Clawhub; incorporating their error-handling logic into our local skill."
