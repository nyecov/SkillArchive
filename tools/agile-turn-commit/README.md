# agile-turn-commit

Automates the end-of-turn validation, staging, committing, and pushing of Agile SDLC updates. Enforces the `[Phase] ID: Message` commit-prefix convention used by the `test-driven-development` skill.

## Usage

```powershell
# Basic use
.\Complete-AgileTurn.ps1 -Phase Red     -ID STORY-AREA-01-04 -Message "Add failing test for AC-02"
.\Complete-AgileTurn.ps1 -Phase Green   -ID STORY-AREA-01-04 -Message "Implement minimum code to pass AC-02"
.\Complete-AgileTurn.ps1 -Phase Refactor -ID STORY-AREA-01-04 -Message "Clean up handler logic"
.\Complete-AgileTurn.ps1 -Phase Carving -ID STORY-AREA-01-04 -Message "Mapped spec phase 3"

# Custom backlog root
.\Complete-AgileTurn.ps1 -Phase Meta -ID META-01 -Message "Update skill templates" -BacklogRoot ".\my-backlog"

# Commit only — no push
.\Complete-AgileTurn.ps1 -Phase Fix -ID BUG-03 -Message "Fix null pointer in parser" -SkipPush
```

## Phases

| Phase | Use when |
|---|---|
| `Red` | Writing failing tests (test files only) |
| `Green` | Writing minimum production code to pass |
| `Refactor` | Behavior-preserving cleanup |
| `Fix` | Bug fix |
| `Carving` | Mapping spec to backlog |
| `Refining` | Refining backlog artifacts |
| `TestDesign` | Authoring test designs |
| `TestExecution` | Recording test results |
| `Implementation` | Non-TDD-tracked implementation |
| `Validation` | Validation/verification work |
| `Maintenance` | Tooling or process maintenance |
| `Epic`, `Initiative` | Creating or updating high-level artifacts |
| `Foundations`, `UX` | Foundational or UX work |
| `Meta` | Skill / tooling / process changes |

## What it does

1. Runs `Validate-AgileHierarchy.ps1` (if present alongside this script) — blocks commit on failures.
2. Runs `Triage-Issues.ps1 -Open` (advisory — non-blocking).
3. Stages standard SDLC paths: `.map-spec/`, `sdlc_backlog/`, `skills/`, `tools/`.
4. Commits with the formatted message `[Phase] ID: Message`.
5. Retries once if a pre-commit auto-fix hook modified staged files.
6. Pushes to remote (unless `-SkipPush` is set).
