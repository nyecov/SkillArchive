# KYT Hazard Matrix Template

When the KYT pre-mortem is complete, the agent MUST format its findings using exactly this Markdown schema to ensure deterministic hazard prediction and countermeasure design.

```markdown
# KYT Hazard Matrix: [Plan/Command Name]

## 1. Identified Hazards
- **Hazard 1:** [What could go wrong? E.g., Accidental database deletion]
- **Hazard 2:** [...]

## 2. Critical Danger Points
- **Irreversible Step:** [The exact tool call or command that executes the hazard]
- **Trigger Condition:** [What state causes the failure?]

## 3. Poka-yoke Countermeasures
- **Interlock 1:** [The deterministic safeguard to prevent Hazard 1]
- **Verify Method:** [How the safeguard will be tested before proceeding]

## 4. Action Targets
- [ ] Implement [Interlock 1]
- [ ] Await user `Sōdan` approval before executing [Irreversible Step]
```
