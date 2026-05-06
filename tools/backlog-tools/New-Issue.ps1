#Requires -Version 5.1
<#
.SYNOPSIS
    Creates a new ISSUE artifact (cross-cutting blocker / spec gap / escalation).
    Compatible with PowerShell 5.1 and 7.

.DESCRIPTION
    ISSUEs are flat-namespaced (ISSUE-<NN>-<Slug>.md) and not parented like
    Story/Subtask. They list Affects: Stories/Epics horizontally and route to
    a single owner role for resolution.

.PARAMETER Title
    Short human title.

.PARAMETER Slug
    URL-safe slug for the filename.

.PARAMETER RoutedTo
    Owner role: Analyst | Architect | PO | Security-Lead | UX-Designer | DevOps | Scrum-Master

.PARAMETER Severity
    BLOCKER | HIGH | MEDIUM | LOW

.PARAMETER Affects
    Comma-separated list of artifact IDs impacted (e.g., "STORY-AREA-01-04,EPIC-AREA-01").

.PARAMETER Trigger
    One-paragraph description of how the issue surfaced.

.PARAMETER Pattern
    Optional recurring-pattern tag for recurrence detection.

.PARAMETER BacklogRoot
    Optional: path to the SDLC backlog root. Default: <repo-root>/sdlc_backlog.

.EXAMPLE
    .\New-Issue.ps1 -Title "Phase 3 scoring contradicts Phase 4 contract" `
        -Slug "Phase3-vs-Phase4-Contract" -RoutedTo Analyst -Severity HIGH `
        -Affects "STORY-AREA-07-35" -Trigger "AC-02 cannot be satisfied without re-reading mid-transaction state."
#>

param (
    [Parameter(Mandatory=$true)]  [string]$Title,
    [Parameter(Mandatory=$true)]  [string]$Slug,
    [Parameter(Mandatory=$true)]
    [ValidateSet("Analyst","Architect","PO","Security-Lead","UX-Designer","DevOps","Scrum-Master")]
    [string]$RoutedTo,
    [Parameter(Mandatory=$true)]
    [ValidateSet("BLOCKER","HIGH","MEDIUM","LOW")]
    [string]$Severity,
    [Parameter(Mandatory=$true)]  [string]$Affects,
    [Parameter(Mandatory=$true)]  [string]$Trigger,
    [Parameter(Mandatory=$false)] [string]$Pattern,
    [Parameter(Mandatory=$false)] [string]$BacklogRoot = ""
)

$RepoRoot = if ($PSScriptRoot) { Split-Path -Parent $PSScriptRoot } else { Get-Location }
if (-not $BacklogRoot) { $BacklogRoot = Join-Path $RepoRoot "sdlc_backlog" }
$IssuesDir  = Join-Path $BacklogRoot "backlog\issues"
$BacklogDir = Join-Path $BacklogRoot "backlog"

if (-not (Test-Path $IssuesDir)) { New-Item -ItemType Directory -Path $IssuesDir -Force | Out-Null }

# Auto-increment NN
$Existing = Get-ChildItem -Path $IssuesDir -Filter "ISSUE-*.md" -ErrorAction SilentlyContinue |
    ForEach-Object {
        if ($_.BaseName -match "^ISSUE-(\d+)-") { [int]$Matches[1] } else { 0 }
    } | Sort-Object -Descending | Select-Object -First 1
$NextNN  = if ($Existing) { ($Existing + 1).ToString("00") } else { "01" }
$IssueID = "ISSUE-$NextNN-$Slug"
$IssueFile = Join-Path $IssuesDir "$IssueID.md"

# Resolve Affects links
$AffectIDs   = $Affects -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ }
$AffectsLines = @()
$Missing     = @()
foreach ($id in $AffectIDs) {
    $found = Get-ChildItem -Path $BacklogDir -Filter "$id*.md" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($found) {
        $parentDir = Split-Path -Leaf (Split-Path $found.FullName)
        $rel       = "../$parentDir/$($found.Name)"
        $AffectsLines += "- [ ] [$id]($rel) -- [how affected]"
    } else {
        $AffectsLines += "- [ ] $id (file not found -- verify ID)"
        $Missing += $id
    }
}
if ($Missing.Count -gt 0) {
    Write-Host "Warning: $($Missing.Count) Affects ID(s) did not resolve: $($Missing -join ', ')" -ForegroundColor Yellow
}

$Today = (Get-Date).ToUniversalTime().ToString("yyyy-MM-dd")

$Content = @"
# Issue: $IssueID $Title

## Metadata
- **Status**: OPEN
- **Severity**: $Severity
- **Routed To**: $RoutedTo
- **Opened**: $Today
- **Last Updated**: $Today
- **Pattern**: $(if ($Pattern) { $Pattern } else { "(none)" })

## Trigger
$Trigger

## Affects
$($AffectsLines -join "`n")

## Routing Rationale
[Explain why this routes to $RoutedTo]

## Resolution
[To be filled when resolved]

## Open Issues
- [ ] (none)
"@

Set-Content -Path $IssueFile -Value $Content -Encoding UTF8 -NoNewline
Write-Host "Created $IssueID at $IssueFile" -ForegroundColor Green
Write-Output $IssueID
