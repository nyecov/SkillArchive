#Requires -Version 5.1
<#
.SYNOPSIS
    Reports the current ISSUE backlog grouped by RoutedTo, severity, and age.
    Detects recurrence patterns. Compatible with PowerShell 5.1 and 7.

.PARAMETER BacklogRoot
    Path to the SDLC backlog root. Default: <repo-root>/sdlc_backlog.

.PARAMETER Json
    Emit machine-readable JSON instead of a formatted table.

.PARAMETER Recurrence
    Print only the recurrence-pattern report (>=3 issues with same Pattern field).

.PARAMETER Open
    Restrict to OPEN/TRIAGED/ROUTED status only.

.EXAMPLE
    .\Triage-Issues.ps1
    .\Triage-Issues.ps1 -Open
    .\Triage-Issues.ps1 -Recurrence
    .\Triage-Issues.ps1 -Open -Json
#>

param(
    [switch]$Json,
    [switch]$Recurrence,
    [switch]$Open,
    [string]$BacklogRoot = ""
)

$RepoRoot = if ($PSScriptRoot) { Split-Path -Parent $PSScriptRoot } else { Get-Location }
if (-not $BacklogRoot) { $BacklogRoot = Join-Path $RepoRoot "sdlc_backlog" }
$IssuesDir = Join-Path $BacklogRoot "backlog\issues"

if (-not (Test-Path $IssuesDir)) {
    Write-Host "No issues directory: $IssuesDir" -ForegroundColor Yellow
    exit 0
}

function Get-FieldValue { param($Content, $Label)
    if ($Content -match "(?m)^- \*\*$Label\*\*:\s*(.+?)\s*$") { return $Matches[1].Trim() }
    return $null
}

$Today  = (Get-Date).ToUniversalTime()
$Issues = @()

Get-ChildItem -Path $IssuesDir -Filter "ISSUE-*.md" | ForEach-Object {
    $content  = Get-Content $_.FullName -Raw
    $idMatch  = if ($_.BaseName -match "^(ISSUE-\d+)") { $Matches[1] } else { $_.BaseName }
    $status   = Get-FieldValue $content "Status"
    $severity = Get-FieldValue $content "Severity"
    $routedTo = Get-FieldValue $content "Routed To"
    $opened   = Get-FieldValue $content "Opened"
    $pattern  = Get-FieldValue $content "Pattern"
    if ($pattern -match "^\(none\)" -or $pattern -match "^\[") { $pattern = $null }

    $age = $null
    if ($opened -match "^\d{4}-\d{2}-\d{2}$") {
        try { $age = ($Today - [datetime]::Parse($opened)).Days } catch {}
    }

    $stale = $false
    switch ($status) {
        "OPEN"    { if ($age -gt 1)  { $stale = $true } }
        "TRIAGED" { if ($age -gt 3)  { $stale = $true } }
        "ROUTED"  { if ($age -gt 7)  { $stale = $true } }
    }

    $title = ""
    if ($content -match "(?m)^# Issue:\s*ISSUE-\d+(?:-\S+)?\s+(.+?)\s*$") { $title = $Matches[1].Trim() }

    $Issues += [PSCustomObject]@{
        ID       = $idMatch;  Title    = $title;    Status   = $status
        Severity = $severity; RoutedTo = $routedTo; Opened   = $opened
        AgeDays  = $age;      Stale    = $stale;    Pattern  = $pattern
        File     = $_.Name
    }
}

if ($Open) { $Issues = $Issues | Where-Object { $_.Status -in @("OPEN","TRIAGED","ROUTED") } }

$Patterns        = $Issues | Where-Object { $_.Pattern } | Group-Object Pattern | Where-Object { $_.Count -ge 2 } | Sort-Object Count -Descending
$RecurrencePromote = $Patterns | Where-Object { $_.Count -ge 3 }

if ($Recurrence) {
    if ($Json) {
        $RecurrencePromote | ForEach-Object {
            [PSCustomObject]@{ Pattern=$_.Name; Count=$_.Count; Issues=$_.Group.ID }
        } | ConvertTo-Json -Depth 3
        if ($RecurrencePromote) { exit 1 } else { exit 0 }
    }
    Write-Host "Recurrence Pattern Report" -ForegroundColor Cyan
    Write-Host ("-" * 80)
    if (-not $Patterns) { Write-Host "No recurring patterns." -ForegroundColor Green; exit 0 }
    foreach ($p in $Patterns) {
        $color = if ($p.Count -ge 3) { "Red" } else { "Yellow" }
        Write-Host "`nPattern: $($p.Name) (count: $($p.Count))" -ForegroundColor $color
        if ($p.Count -ge 3) { Write-Host "  -> PO higher-level review trigger" -ForegroundColor Red }
        $p.Group | ForEach-Object { Write-Host "  - $($_.ID) [$($_.Severity)/$($_.Status)] $($_.Title)" }
    }
    if ($RecurrencePromote) { exit 1 } else { exit 0 }
}

if ($Json) { $Issues | ConvertTo-Json -Depth 3; exit 0 }

if ($Issues.Count -eq 0) { Write-Host "No issues on file." -ForegroundColor Green; exit 0 }

Write-Host "`nIssue Triage Report" -ForegroundColor Cyan
Write-Host ("-" * 100)
$summary = $Issues | Group-Object Status | ForEach-Object { "$($_.Name): $($_.Count)" }
Write-Host "Total: $($Issues.Count)    $($summary -join '    ')"

$Active = $Issues | Where-Object { $_.Status -in @("OPEN","TRIAGED","ROUTED") }
if ($Active.Count -eq 0) {
    Write-Host "No active issues." -ForegroundColor Green
} else {
    $Active | Group-Object RoutedTo | Sort-Object Name | ForEach-Object {
        Write-Host "`n[Routed To: $($_.Name)] ($($_.Count) active)" -ForegroundColor Yellow
        $_.Group | Sort-Object Severity, AgeDays -Descending | ForEach-Object {
            $marker = ""
            if ($_.Severity -eq "BLOCKER") { $marker += "[BLOCKER] " }
            if ($_.Stale)                  { $marker += "[STALE>$($_.AgeDays)d] " }
            $color = if ($_.Severity -eq "BLOCKER") { "Red" } elseif ($_.Stale) { "Yellow" } else { "Gray" }
            Write-Host ("  {0,-40} {1,-10} {2,-8} age={3}d  {4}{5}" -f $_.ID, $_.Status, $_.Severity, $_.AgeDays, $marker, $_.Title) -ForegroundColor $color
        }
    }
}

if ($RecurrencePromote) {
    Write-Host "`nRecurrence promoted (>=3 issues per pattern) - PO review:" -ForegroundColor Red
    foreach ($p in $RecurrencePromote) {
        Write-Host "  Pattern '$($p.Name)' across: $(($p.Group | ForEach-Object { $_.ID }) -join ', ')"
    }
}

$bad = $Active | Where-Object { $_.Severity -eq "BLOCKER" -or $_.Stale }
if ($bad) { exit 1 } else { exit 0 }
