---
name: Skill of Skills (Meta-Skill Authoring)
version: 1.2.0
description: Use when creating, reviewing, or refining agent skills. Provides the authoritative checklist and workflow for writing high-efficiency, token-optimal skill files that activate reliably, follow progressive disclosure, and avoid common anti-patterns.
category: meta
tags: [meta-skill, skill-authoring, progressive-disclosure, token-efficiency, agent-skills]
references:
  - name: Agent Skills 101 (Serghei Plutenko)
    url: https://blog.serghei.pl/posts/agent-skills-101/
  - name: 10 Practical Techniques (Shibui Yusuke)
    url: https://shibuiyusuke.medium.com/10-practical-techniques-for-mastering-agent-skills-in-ai-coding-agents-6070e4038cf1
  - name: AI Agent Skills — What, Why, How (Somnio Software)
    url: https://somniosoftware.com/blog/ai-agent-skills-what-they-are-why-they-matter-and-how-they-work
  - name: Agent Skills Open Specification
    url: https://agentskills.io
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko-vibecoding/SKILL.md
  - name: Lean Principles (Muda Eradication)
    path: ../lean-principles-muda/SKILL.md
  - name: Kaizen (Continuous Improvement)
    path: ../kaizen-continuous-improvement/SKILL.md
  - name: Poka-yoke (Mistake-proofing)
    path: ../poka-yoke-mistake-proofing/SKILL.md
---

# Skill of Skills: Meta-Skill Authoring Guide

A skill is not a configuration file, not a prompt template, and not documentation. It is a **procedure** — a set of instructions that tells an agent how to accomplish a specific task the way your team does it. Skills represent a paradigm shift: from transient prompt instructions to **persistent capability modules**, from ad-hoc task handling to **repeatable, tested workflows**, from one-off interactions to **scalable agent infrastructure**. This meta-skill codifies the principles of writing skills that activate correctly, execute reliably, and use tokens efficiently.

## The Three-Stage Loading Model

Every design decision flows from progressive disclosure — the architecture that makes skills scale.

| Stage | Content | Token Cost | Loaded When |
|-------|---------|-----------|-------------|
| **L1: Metadata** | `name` + `description` (frontmatter) | ~100 tokens | Always, at session start |
| **L2: Instructions** | Body of SKILL.md (workflow, rules) | <5,000 tokens | On activation (description match) |
| **L3: Resources** | `scripts/`, `references/`, `assets/` | On demand | When the agent reaches a step that references them |

**Critical implication:** Every token in the description is paid *every session*, even when the skill never activates. Every token in the body is paid *every activation*. Reference files are paid only when accessed. Design accordingly.

## Core Mandates

### 1. Description as Trigger, Not Summary

The description is the single most important field. It is NOT documentation — it is the mechanism by which the agent decides whether to activate the skill.

**The fatal mistake:** If your description explains *how* the skill works, the agent may conclude it already knows the procedure and skip loading the body entirely.

❌ **Bad** — contains the procedure:
```
description: "Analyzes git diff, identifies the change type, generates a commit message in conventional format with scope detection"
```

✅ **Good** — states when to activate and what capabilities exist:
```
description: >
  Use when generating commit messages or reviewing staged changes.
  Handles conventional commits, scope detection, and breaking change notation.
```

**Rules:**
- Stay under **1,024 characters** (spec limit). Aim for 2–4 sentences.
- Use **third person, declarative** voice: "Handles…", "Use when…", "Generates…". Never "I can help you" or "You should use this" — the description is injected into the system prompt.
- Include **concrete trigger keywords** users actually type: not "Python testing" but "pytest", not "database queries" but "PostgreSQL migrations".
- Add **negative triggers** when over-activation is a risk: "Do NOT use for basic data exploration."

### 2. Procedures, Not Documentation

The body of a skill must tell the agent **what to do**, not **what things are**.

❌ **Documentation style** (the agent has no actionable steps):
```markdown
# Database Migration Skill
This skill helps with database migrations. Our project uses Drizzle ORM
with SQLite. Migrations are important for keeping the schema in sync.
```

✅ **Procedural style** (the agent can execute immediately):
```markdown
# Database Migration
## Workflow
1. Read the current schema from `src/db/schema.ts`
2. Compare against the latest migration in `drizzle/migrations/`
3. Generate a new migration: `npx drizzle-kit generate`
4. Review the generated SQL for destructive operations (DROP, ALTER)
5. Run the migration: `npx drizzle-kit migrate`
6. Verify by running: `npm test`
```

**Structure recommendations:**
- Start with a **Workflow** section — numbered steps in execution order.
- Follow with **Rules** or **Constraints** that apply across all steps.
- Use **conditional logic** for branching ("If the change modifies a public API → run integration tests").
- Include **verification steps** after every phase — do not assume the agent checks its own work.
- Put **critical constraints at the top** of the body, not buried in the middle (agents may skim long documents).

### 3. One Directory Per Skill

Every skill lives in its own named directory. The directory name IS the skill identifier.

```
skills/
  my-skill-name/          ← directory named after skill
    SKILL.md              ← required: metadata + instructions
    scripts/              ← optional: deterministic operations
    references/           ← optional: large knowledge (loaded on demand)
    assets/               ← optional: templates, static files
```

**Rules:**
- The entry point is always `SKILL.md` — never a custom filename.
- Cross-reference other skills via relative paths: `../other-skill/SKILL.md`.
- Never inline large reference material — move it to `references/`.
- Keep referenced files one level deep (avoid deep nesting).
- Add a Table of Contents to long reference files to help the agent navigate.
- For operations requiring high precision, provide a **script** in `scripts/` rather than prose instructions — code is deterministic, language interpretation is not.

### 4. Token Efficiency Through Layered Design

| Skill Type | Body Size Target |
|-----------|-----------------|
| Frequently-loaded (style, commits) | Under **200 words** (~300 tokens) |
| Standard workflow | Under **500 lines** (~2,000–3,000 tokens) |
| Complex multi-phase | Split into body + `references/` files loaded on demand |

### 5. Deterministic over Probabilistic

Where possible, replace prose instructions with scripts, schemas, or templates.

- A 10-line validation script will outperform a paragraph of validation instructions every time.
- Scripts should return **specific error messages** (e.g., "Field 'date' not found. Available fields: X, Y"), not vague ones ("An error occurred").
- Use `assets/` for templates that provide structural consistency.

### 6. Portability

Skills should work across platforms and operating systems.
- Use forward slashes (`/`) for paths — never backslashes.
- Do not reference tool-specific commands (e.g., "Use Claude's Read tool"). Use generic instructions (e.g., "Read the file at `path/to/file`").
- Skills should be **self-contained** — do not require network requests or `git clone` operations to function.

### 7. Cross-Functional Design

Skills are not limited to engineering workflows. Any team that has repeatable processes — marketing, operations, compliance, product — can author skills that encode institutional knowledge into executable capabilities.

- Write skills for **any repeatable process**, not just code tasks: SEO checklists, campaign reviews, compliance procedures, user story validation.
- Use **domain-specific trigger keywords** that match how each team describes their work (e.g., "content audit" not "text analysis").
- Skills democratize structured intelligence — they bridge the gap between static documentation and executable action.

## Anti-Patterns Checklist

When reviewing a skill, check for these failure modes:

| Anti-Pattern | Symptom | Fix |
|---|---|---|
| **Workflow in description** | Agent skips the body | Move procedure out of description; keep only trigger conditions |
| **Generic description** | Over- or under-activation | Add concrete keywords, synonyms, and negative triggers |
| **README instead of procedure** | Agent has no actionable steps | Rewrite as numbered workflow with verification |
| **Monolithic skill** | Expensive, imprecise activation | Split into focused single-purpose skills |
| **First/second person description** | Breaks system prompt voice | Use third person declarative |
| **Critical rules buried in body** | Agent skips them | Move to top, use `## Critical` headers |
| **External dependencies** | Fragile, environment-dependent | Bundle what you need in the skill directory |
| **Commands without verification** | Brittle, no error recovery | Add conditional logic, error handling, and verification after every phase |

## Implementation Workflow: Creating a New Skill

1. **Create the skill directory.** Name it with lowercase, hyphens: `skills/my-new-skill/`.
2. **Create `SKILL.md`** inside the directory with YAML frontmatter (`name`, `description`).
3. **Identify the procedure.** What task do you explain repeatedly? That is your first skill.
4. **Define success criteria.** What does a correct execution look like? Quantitative: trigger accuracy (80–90% target), workflow efficiency, error rate. Qualitative: self-sufficiency, consistency across runs, first-try success.
5. **Write the description** as a trigger — when to activate, what capabilities exist, what NOT to use it for.
6. **Write the body** as a procedure — numbered workflow, rules, conditional logic, verification steps.
7. **Extract large references** to `references/`. Provide scripts for deterministic operations in `scripts/`.
8. **Test with a single challenging task.** Iterate on that one task until the agent succeeds, then expand.
9. **Run the three tests:**
   - **Triggering test:** 10–20 queries across should-trigger, paraphrased, and should-NOT-trigger groups.
   - **Functional test:** Run the same request 3–5 times, compare for structural consistency.
   - **Performance test:** Compare the task with and without the skill — if no improvement, simplify or reconsider.
10. **Iterate via Kaizen.** Capture failures, tighten ambiguous instructions, and evolve the skill over time.

## Quick Reference: Specification Constraints

```
STRUCTURE:
  skills/
    my-skill-name/           ← one directory per skill
      SKILL.md               Required — metadata + instructions (entry point)
      scripts/               Optional — deterministic operations
      references/            Optional — large knowledge bases (loaded on demand)
      assets/                Optional — templates, static files

FRONTMATTER (required in SKILL.md):
  name:        1-64 chars, lowercase, digits, hyphens only
  description: 1-1,024 chars, third person, trigger-oriented

BODY:
  Target: <500 lines for standard skills, <200 words for frequently-loaded
  Structure: Workflow → Rules → Edge Cases → Verification
  Critical constraints at the TOP, not the middle

CROSS-REFERENCES:
  Use relative paths from skill directory: ../other-skill/SKILL.md

DESCRIPTION DESIGN:
  ✅ "Use when…" / "Handles…" / "Generates…"
  ❌ "I can help you…" / "You should use this…"
  ❌ Workflow summary in description (agent skips body)
  ✅ Concrete keywords: "pytest" not "Python testing"
  ✅ Negative triggers: "Do NOT use for…"
```

## Ecosystem & Discovery

Skills are an **open standard** — not locked to any one agent platform. Browse and share skills:

- **Specification:** [agentskills.io](https://agentskills.io)
- **Marketplace:** [skillsmp.com](https://skillsmp.com/search)
- **Directory:** [skills.sh](https://skills.sh/)
