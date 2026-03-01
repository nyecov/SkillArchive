# Planning Triad Template

When creating the `task_plan.md`, `findings.md`, and `progress.md` files in the temporary directory, the agent MUST use this exact schema to maintain deterministic state tracking.

## 1. task_plan.md
```markdown
# Task Plan: [Task Name]

## Goal
[One sentence objective]

## Phases
- [ ] Phase 1: [Name]
- [ ] Phase 2: [Name]

## Current Status
- **Active Phase:** [Phase Number]
- **Blockers:** [None / List blockers]
```

## 2. findings.md
```markdown
# Research & Findings

## [Date/Time] - [Topic/Component]
- **Observation:** [What was discovered]
- **Decision:** [Architectural or logic decision made based on observation]
- **Source:** [File path or URL]
```

## 3. progress.md
```markdown
# Execution Log

## [Date/Time]
- **Action:** [What was done, e.g., "Updated auth logic in auth.py"]
- **Result:** [PASS / FAIL - Error log snippet if failed]
- **Next Step:** [What happens immediately next]
```
