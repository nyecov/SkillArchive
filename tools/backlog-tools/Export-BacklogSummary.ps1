#Requires -Version 5.1
<#
.SYNOPSIS
    Exports a markdown table summary of the entire backlog hierarchy.
    Compatible with PowerShell 5.1 and 7.

.PARAMETER OutputFile
    Output file path (default: BACKLOG_SUMMARY.md in repo root).

.PARAMETER BacklogRoot
    Path to the SDLC backlog root. Default: <repo-root>/sdlc_backlog.

.EXAMPLE
    .\Export-BacklogSummary.ps1
    .\Export-BacklogSummary.ps1 -OutputFile "reports/summary.md"
#>

param (
    [string]$OutputFile  = "BACKLOG_SUMMARY.md",
    [string]$BacklogRoot = ""
)

$RepoRoot = if ($PSScriptRoot) { Split-Path -Parent $PSScriptRoot } else { Get-Location }
if (-not $BacklogRoot) { $BacklogRoot = Join-Path $RepoRoot "sdlc_backlog" }
$BacklogDir = Join-Path $BacklogRoot "backlog"

function Get-ArtifactMeta {
    param([string]$Path)
    $Content = Get-Content $Path -Raw
    $Title   = "Untitled"
    if ($Content -match "^#\s+(.+)$") { $Title = $Matches[1] }
    $Status  = "?"
    if ($Content -match "Status:\s*(\S+)")  { $Status = $Matches[1] }
    return @{ Title = $Title; Status = $Status }
}

$Lines = @()
$Lines += "# Backlog Summary"
$Lines += ""
$Lines += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
$Lines += ""

foreach ($section in @(
    @{ Name = "Initiatives"; Dir = "initiatives"; Cols = "| ID | Title | Status |"; Header = "|---|---|---|"; ParentField = $null },
    @{ Name = "Epics";       Dir = "epics";       Cols = "| ID | Parent | Title | Status |"; Header = "|---|---|---|---|"; ParentField = "Parent Initiative" },
    @{ Name = "Stories";     Dir = "stories";     Cols = "| ID | Parent Epic | Title | Status |"; Header = "|---|---|---|---|"; ParentField = "Parent Epic" },
    @{ Name = "Subtasks";    Dir = "subtasks";    Cols = "| ID | Parent Story | Title | Status |"; Header = "|---|---|---|---|"; ParentField = "Parent Story" }
)) {
    $Dir = Join-Path $BacklogDir $section.Dir
    $Lines += "## $($section.Name)"
    $Lines += ""
    $Lines += $section.Cols
    $Lines += $section.Header

    if (Test-Path $Dir) {
        Get-ChildItem -Path $Dir -Filter "*.md" | Sort-Object Name | ForEach-Object {
            $Meta = Get-ArtifactMeta $_.FullName
            if ($section.ParentField) {
                $Content = Get-Content $_.FullName -Raw
                $Parent  = "?"
                if ($Content -match "\[$($section.ParentField)\]\((.+?)\)") {
                    $Parent = (Split-Path $Matches[1] -Leaf) -replace "\.md", ""
                }
                $Lines += "| $($_.BaseName) | $Parent | $($Meta.Title) | $($Meta.Status) |"
            } else {
                $Lines += "| $($_.BaseName) | $($Meta.Title) | $($Meta.Status) |"
            }
        }
    }
    $Lines += ""
}

$OutputPath = Join-Path $RepoRoot $OutputFile
$Lines | Out-File -FilePath $OutputPath -Encoding UTF8

$counts = foreach ($d in @("initiatives","epics","stories","subtasks")) {
    $p = Join-Path $BacklogDir $d
    $n = if (Test-Path $p) { (Get-ChildItem $p -Filter "*.md").Count } else { 0 }
    "$d=$n"
}
Write-Host "Exported to: $OutputPath  ($($counts -join ' | '))" -ForegroundColor Green
