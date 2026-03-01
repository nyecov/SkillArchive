# Poka-yoke Output Template

When `manage_skill_authoring.py` runs against a completed skill, the agent MUST output the script's findings using exactly this Markdown schema:

```markdown
# Skill Authoring Validation Report: [Skill Name]

## 1. Compliance State
- **Status:** [validated | auto_corrected | unrecoverable]
- **Script Finding:** [Description of what missing headers the python script injected, if any]

## 2. Next Steps
- [ ] [e.g., Proceed to run `manage_skills.py` orchestrator]
- [ ] [e.g., Invoke Story Interview to rebuild unrecoverable constraint logic]
```
