# triage-validator

Validates that bugs and issues have completed the mandatory triage review process. Checks for the presence of a triage review section and validates story cross-references.

## Usage

```bash
# Auto-detects backlog root (looks for sdlc_backlog/backlog, then backlog/, then cwd)
python triage_validator.py

# Explicit backlog root
python triage_validator.py --backlog-root path/to/backlog

# Validate only bugs or issues
python triage_validator.py --type bug
python triage_validator.py --type issue

# Validate a specific artifact
python triage_validator.py --id BUG-01-SomeSlug

# Fail-closed mode for CI / release gate
python triage_validator.py --strict
```

## Expected Structure

```
<backlog-root>/
  bugs/BUG-*.md
  issues/ISSUE-*.md
  stories/STORY-*.md
```

## What it checks

- Presence of a triage review section (`## Bug Triage Review` or `## Triage`)
- Presence of a triage review section in issues (`## Issue Triage Review` or `## Triage`)
- Story cross-references resolve to existing files

## Exit codes

- `0` — all validated artifacts pass (or no artifacts found)
- `1` — one or more failures (only in `--strict` mode)
