---
name: skill-authoring-management
version: 1.4.0
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
- name: Skill Specification Reference
  path: ./references/skill-spec-reference.md
level: methodology
---

# Skill Authoring Management

A skill is not documentation; it is a **procedure**. This meta-skill codifies the "Gold Standard" for authoring and managing agentic capabilities. It ensures that skills are not just written, but are maintained as high-integrity, deterministic capability modules that scale with the system.

## The Gold Standard: Content & Formatting

Every skill in the library MUST adhere to these structural and qualitative requirements:

### 1. Metadata (Frontmatter)
- **name**: Lowercase, hyphenated (e.g., `cc-security-enforcement`).
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
- **## Poka-yoke Output Template**: (Optional) required for any skill that generates structured data.

## Core Mandates

### 1. Trigger-Oriented Activation
The description is the primary mechanism for activation.
- **Action:** Use third-person, declarative voice with concrete keywords (e.g., "pytest" not "testing").
- **Constraint:** NEVER include the procedure in the description.
- **Integration:** Directly impacts L1 token efficiency and activation reliability.

### 2. Gold Standard Compliance (Management)
Every skill MUST be strictly audited to maintain the highest formatting and content standards.
- **Action:** You must initialize and run `python scripts/manage_skill_authoring.py` when drafting or modifying ANY skill.
- **Constraint:** Do not assume your generated file is correct. Allow the python script to parse and auto-correct structural omissions.
- **Constraint:** `Action Targets` in safety-critical skills (e.g., KYT) MUST be expressed as verifiable tool calls or commands, not subjective text.
- **Integration:** Connects to **Poka-yoke** mistake-proofing by physically preventing malformed or "soft" safety plans from entering orchestration.

### 3. Environment & Path Verification
Prevent operational friction from pathing mismatches or environment drift.
- **Action:** Before executing any bulk automated scripts (e.g., library-wide audits), you MUST perform a "Pilot" execution on a single, isolated module to verify pathing, whitespace handling, and script access.
- **Constraint:** NEVER proceed to bulk execution if the Pilot fails or requires manual path correction.
- **Constraint:** You MUST use ONLY relative filepaths across all skills, scripts, links, and references. Absolute filepaths are strictly forbidden.
- **Integration:** Reduces **Transportation Waste** and prevents cascading tool failures.

### 4. Progressive Disclosure (Structure)
Optimize token costs by layering instructions and offloading large data.
- **Action:** Move large knowledge bases to `references/` and deterministic logic to `scripts/`.
- **Constraint:** Keep the `SKILL.md` body under 5,000 tokens (target < 3,000). Enforce a **soft line limit of 150 lines** and a **warning at 200 lines**.
- **Constraint:** NEVER use emojis (e.g., 👉, ✅, ⚠️) in any skill documentation or templates. Use standard Markdown syntax or bold text for emphasis.
- **Integration:** Supports **Lean Foundations** by reducing context transportation waste and maintaining professional engineering standards.

## Escalation & Halting

- **Jidoka:** If a skill fails a compliance audit or triggers reasoning drift, trigger a Jidoka halt to perform a structural refactor.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol to propose architectural shifts in how skills are categorized or linked.

## Implementation Workflow

1. **Trigger:** A repeatable process is identified, or a skill needs maintenance.
2. **Execute:** Scaffold from the `templates/skill-template.md`. Author or update content. Then, MUST run `python scripts/manage_skill_authoring.py <path_to_skill>`.
3. **Verify:** Check the python script output. If the script repaired errors, log them. If it returned "unrecoverable", halt immediately.
4. **Output:** Render the final compliance state using the Poka-yoke Output Template.

## Progressive Resources

For detailed sizing limits, required structure, and anti-pattern checklists, Read:
[Skill Specification Reference](references/skill-spec-reference.md)

For the exact diagnostic output schema to use post-validation, read:
[Poka-yoke Output Template](templates/poka-yoke-output.md)

