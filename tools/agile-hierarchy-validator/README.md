# agile-hierarchy-validator

Validates strict parentage hierarchy and link integrity across backlog and testing artifacts. Enforces the Initiative → Epic → Story → Subtask chain and the TP → TS → TD → TX test chain.

## Usage

```powershell
# Auto-detects sdlc_backlog/ relative to script location
.\Validate-AgileHierarchy.ps1

# Custom backlog root
.\Validate-AgileHierarchy.ps1 -BacklogRoot ".\my-project\backlog"
```

## Expected Structure

```
<BacklogRoot>/
  backlog/
    epics/EPIC-*.md
    stories/STORY-*.md
    subtasks/SUB-*.md (or SUBTASK-*.md)
    issues/ISSUE-*.md
  tests/
    sets/TS-*.md
    designs/TD-*.md
    executions/TX-*.md
```

## What it checks

- Every Epic has a valid `## Parent Initiative` link pointing to an existing file
- Every Story has a valid `## Parent Epic` link
- Every Subtask has a valid `## Parent Story` link
- Every Test Set has a valid `## Parent Test Plan` link
- Every Test Design has a valid `## Parent Test Set` link
- Every Test Execution has a valid `## Executes` link
- Every ISSUE has valid Status/Severity/Routed To enum values
- Every ISSUE has an `## Affects` section with links that resolve

## Exit codes

- `0` — all links valid
- `1` — one or more broken links or invalid fields (details printed to stdout)

## Integration

Wire as a pre-commit hook or call from `Complete-AgileTurn.ps1` before every commit.
