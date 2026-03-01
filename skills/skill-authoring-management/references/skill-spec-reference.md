# Skill Authoring Management: Quick Reference & Anti-Patterns

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

SIZE LIMITS (SKILL.md only, excludes auxiliary files):
  Soft limit:  150 lines
  Warning:     200 lines
  Token target: < 3,000 (hard cap: 5,000)
```
