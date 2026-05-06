# backlog-tools

A collection of PowerShell scripts for managing an Agile SDLC backlog. All scripts auto-detect the backlog root relative to their location, but accept a `-BacklogRoot` parameter for custom layouts.

## Scripts

| Script | Purpose |
|---|---|
| `New-Issue.ps1` | Create a new ISSUE artifact with auto-increment ID, routing, and Affects links |
| `Triage-Issues.ps1` | Report open issues grouped by owner, severity, and age; detect recurrence patterns |
| `Export-BacklogSummary.ps1` | Export a markdown table summary of the full backlog hierarchy |
| `Search-AllArtifacts.ps1` | Full-text search across backlog, test artifacts, and spec files |

## Usage

```powershell
# Create a new issue
.\New-Issue.ps1 -Title "Parser cannot handle edge case" -Slug "Parser-Edge-Case" `
    -RoutedTo Analyst -Severity HIGH -Affects "STORY-AREA-01-04" `
    -Trigger "AC-02 of STORY-AREA-01-04 cannot be satisfied without additional spec clarification."

# Triage report — active issues only
.\Triage-Issues.ps1 -Open

# Triage with recurrence detection
.\Triage-Issues.ps1 -Recurrence

# Export backlog summary
.\Export-BacklogSummary.ps1
.\Export-BacklogSummary.ps1 -OutputFile "reports/my-summary.md"

# Search all artifacts
.\Search-AllArtifacts.ps1 -Query "authentication"
.\Search-AllArtifacts.ps1 -Query "database" -Type Story
.\Search-AllArtifacts.ps1 -SpecAudit   # scan spec dir for critical keywords
```

## Expected Structure

```
<BacklogRoot>/
  backlog/
    initiatives/INIT-*.md
    epics/EPIC-*.md
    stories/STORY-*.md
    subtasks/SUB-*.md
    issues/ISSUE-*.md
  tests/
    plans/TP-*.md
    sets/TS-*.md
    designs/TD-*.md
    executions/TX-*.md
```
