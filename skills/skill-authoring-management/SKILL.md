---
name: skill-authoring-management
version: 1.3.0
description: 'Use when creating, reviewing, or managing agent skills.  Provides the
  authoritative "Gold Standard" for content and formatting, management of skill lifecycles,
  and template usage for persistent capability modules.\'
category: meta
tags:
- meta
references:
- name: Skill Template
  path: ./templates/skill-template.md
- name: Shisa Kanko (Master Workflow)
  path: ../shisa-kanko/SKILL.md
- name: Lean Foundations
  path: ../lean-foundations/SKILL.md
- name: Kaizen (Continuous Improvement)
  path: ../kaizen/SKILL.md
- name: Poka-yoke (Mistake-proofing)
  path: ../poka-yoke/SKILL.md
- name: Tools Management Strategy
  path: ../tools-management/SKILL.md
- name: External Resource Synthesis
  path: ../external-synthesis/SKILL.md
level: meta
---

# Skill Authoring & Management (SAM)

A skill is not documentation; it is a **procedure**. This meta-skill codifies the "Gold Standard" for authoring and managing agentic capabilities. It ensures that skills are not just written, but are maintained as high-integrity, deterministic capability modules that scale with the system.

## The Gold Standard: Content & Formatting

Every skill in the library MUST adhere to these structural and qualitative requirements:

### 1. Metadata (Frontmatter)
- **name**: Lowercase, hyphenated (e.g., `cc-secure-security`).
- **version**: Semantic versioning (e.g., `1.0.0`), incremented with every change.
- **description**: Trigger-oriented. NOT a summary. States *when* to activate.
- **category**: Functional grouping for the library index.
- **level**: Cognitive depth of the skill:
  - `methodology`: High-level cognitive frameworks (e.g., Lean, Shisa Kanko).
  - `tactical`: Engineering procedures and task-level workflows (e.g., Debugging, Security).
  - `technical`: Standardized specifications or data formats (e.g., TOON, Docker).
- **references**: Use relative paths (`../other-skill/SKILL.md`) for internal links.

### 2. Standard Markdown Sections
- **# H1 Header**: Clear, concise title of the skill.
- **Intro Paragraph**: Explains the skill's role and its relationship to Lean principles.
- **## Core Mandates**: The non-negotiable rules. Must use the **Action / Constraint / Integration** format.
- **## Escalation & Halting**: Defines the "Red Light" conditions. Must include specific **Jidoka** and **Hō-Ren-Sō** sub-points.
- **## Implementation Workflow**: A 1-4 step numbered list: **1. Trigger**, **2. Execute**, **3. Verify**, **4. Output**.

## Core Mandates

### 1. Trigger-Oriented Activation
The description is the primary mechanism for activation.
- **Action:** Use third-person, declarative voice with concrete keywords (e.g., "pytest" not "testing").
- **Constraint:** NEVER include the procedure in the description.
- **Integration:** Directly impacts L1 token efficiency and activation reliability.

### 2. Gold Standard Compliance (Management)
Every skill MUST be audited and updated to maintain the highest formatting and content standards.
- **Action:** Use the `templates/skill-template.md` for all new skills.
- **Constraint:** DO NOT allow "Skill Rot" (outdated references, broken paths, or missing mandates).
- **Integration:** Connects to **Kaizen** for continuous library refinement.

### 3. Progressive Disclosure (Structure)
Optimize token costs by layering instructions and offloading large data.
- **Action:** Move large knowledge bases to `references/` and deterministic logic to `scripts/`.
- **Constraint:** Keep the frequently-loaded `SKILL.md` body under 5,000 tokens (target < 3,000).
- **Integration:** Supports **Lean Foundations** by reducing context transportation waste.

## Escalation & Halting

- **Jidoka:** If a skill fails a compliance audit or triggers reasoning drift, trigger a Jidoka halt to perform a structural refactor.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to propose architectural shifts in how skills are categorized or linked.

## Implementation Workflow

1. **Trigger:** A repeatable process is identified, or a skill needs maintenance.
2. **Execute:** Scaffold from the `templates/skill-template.md`. Author or update content following the Gold Standard.
3. **Verify:** Run a compliance audit (Metadata, Headers, Mandates, Workflow).
4. **Output:** A verified, high-integrity capability module synchronized via `sync_skills.py`.

## Anti-Patterns Checklist

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| **Workflow in description** | Agent skips the body | Move procedure out of description; keep only trigger conditions. |
| **README style** | Agent has no actionable steps | Rewrite as a numbered workflow with verification. |
| **Broken References** | Path not found errors | Use relative paths: `../folder/SKILL.md`. |
| **Missing Interlocks** | Agent continues through errors | Add mandatory **Escalation & Halting** section. |

## Quick Reference: Specification Constraints

```
STRUCTURE:
  skills/
    my-skill-name/           ← one directory per skill
      SKILL.md               Required — entry point
      templates/             Optional — local templates
      scripts/               Optional — deterministic tools
      references/            Optional — large knowledge bases

FRONTMATTER:
  name:        1-64 chars, lowercase, hyphens
  version:     x.x.x
  description: 1-1,024 chars, third person, trigger-oriented
```
