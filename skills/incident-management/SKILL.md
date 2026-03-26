---
id: a1dae000-6416-4cbf-806b-258ea756a394
name: incident-management
version: 1.0.0
level: methodology
category: methodology
tags:
- debugging
- cognition
- context
- research
description: Use when creating, updating, resolving, or referencing incident reports. Handles the lifecycle of incidents (active/resolved) and ensures they are recorded as a permanent memory with problem, symptoms, root cause, and resolution.
---

# Incident Management

This skill governs the creation and management of incident reports, which serve as a long-term memory for issues, symptoms, root causes, and resolutions.

## Directory Structure

Incident reports MUST be stored in the `docs/incidents/` directory.

- `docs/incidents/active/`: For ongoing incidents that are currently being investigated.
- `docs/incidents/resolved/`: For incidents where the root cause is understood and a resolution has been applied.

## File Naming Convention

Name files using the ISO date and a concise, hyphenated description:
`YYYY-MM-DD-short-description-of-incident.md`

Example: `2026-03-26-pwsh-explorer-incident-report.md`

## Incident Report Format

Every incident report MUST contain the following sections at a minimum:

```markdown
# Incident Report: [Clear Title]

## Date
[Date of the incident]

## Problem
[High-level description of what went wrong or the user-facing issue]

## Symptoms
- [Bullet points of specific errors, logs, or behaviors observed]
- [Context on when/where the symptoms occur]

## Root Cause
[Detailed technical explanation of why the problem occurred. What was the underlying mechanism or conflict?]

## Resolution
[Step-by-step description of how the issue was fixed. Include specific commands, configuration changes, or code edits.]

## Outcome (Optional)
[Confirmation that the fix worked and current state of the system.]
```

## Workflows

### 1. Creating a New Incident Report (Active)
When an issue is identified but not yet fixed, create a stub in `docs/incidents/active/` capturing the **Problem** and **Symptoms**.

### 2. Resolving an Incident
Once an issue is fixed:
1. Move the report from `docs/incidents/active/` to `docs/incidents/resolved/` (if it was previously tracked).
2. Fully flesh out the **Root Cause** and **Resolution** sections.
3. Ensure the formatting matches the template above.

### 3. Referencing Past Incidents
When encountering an error, search the `docs/incidents/resolved/` directory for similar symptoms or root causes to leverage past memories instead of debugging from scratch. Use search tools to find relevant keywords in the incidents folder.