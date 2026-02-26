---
name: skill-external-synthesis
version: 1.0.0
description: >
  Use when researching, designing, or authoring new agent skills.
  Guides the agent to search external repositories like the Claude Cookbook and Clawhub
  to identify existing patterns and synthesize them into high-quality local skills.
category: meta
tags: [skill-authoring, synthesis, research, external-resources, clawhub]
references:
  - name: Skill of Skill Authoring
    path: ../skill-of-skill-authoring/SKILL.md
  - name: Claude Cookbook
    url: https://platform.claude.com/cookbook/
  - name: Clawhub (Skills)
    url: https://clawhub.ai/skills?sort=downloads
---

# Skill External Synthesis

A skill for extending the internal knowledge base by leveraging established patterns from the global agent ecosystem. This skill acts as a research phase for `skill-of-skill-authoring`, ensuring that new skills are not built in a vacuum but are synthesized from the best available community practices.

## Core Mandates

### 1. Mandatory External Discovery
Before drafting a new skill, the agent MUST search external reference points to see if the problem has already been solved or if relevant prompt patterns exist.
- **Action:** Visit `https://platform.claude.com/cookbook/` and `https://clawhub.ai/skills?sort=downloads`.
- **Constraint:** Do not blindly copy-paste. Evaluate external content for "Skill Archive" compatibility (token efficiency, procedural style).
- **Integration:** Feeds directly into the "Research" phase of the `skill-of-skill-authoring` workflow.

### 2. Analytical Synthesis
Identify the "delta" between existing community solutions and local requirements.
- **Action:** Extract core logic, tool-use patterns, and failure modes from external examples.
- **Constraint:** Ensure all synthesized content is adapted to the Three-Stage Loading Model defined in `skill-of-skill-authoring`.
- **Integration:** Uses `Kaizen` to refine the synthesized procedure until it meets local standards.

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
