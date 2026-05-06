#Requires -Version 5.1
<#
.SYNOPSIS
    Full-text search across backlog, test artifacts, and spec files.
    Compatible with PowerShell 5.1 and 7.

.PARAMETER Query
    Search term (regex supported). Mutually exclusive with -SpecAudit.

.PARAMETER SpecAudit
    Search for critical spec keywords (MUST, SHALL, Rule:, Mandate:, etc.) in the spec directory.

.PARAMETER Type
    Filter by artifact type: Initiative, Epic, Story, Subtask, TestPlan, TestSet, TestDesign, TestExecution.

.PARAMETER Status
    Filter by status value.

.PARAMETER BacklogRoot
    Path to the SDLC backlog root. Default: <repo-root>/sdlc_backlog.

.PARAMETER SpecDir
    Path to the spec documents directory. Default: <repo-root>/obsidian (or <repo-root>/spec if obsidian doesn't exist).

.EXAMPLE
    .\Search-AllArtifacts.ps1 -Query "database"
    .\Search-AllArtifacts.ps1 -Query "parser" -Type Story
    .\Search-AllArtifacts.ps1 -SpecAudit
#>

param (
    [Parameter(ParameterSetName="Default", Mandatory=$true)] [string]$Query,
    [Parameter(ParameterSetName="Audit",   Mandatory=$true)] [switch]$SpecAudit,
    [string]$Type,
    [string]$Status,
    [string]$BacklogRoot = "",
    [string]$SpecDir     = ""
)

$RepoRoot = if ($PSScriptRoot) { Split-Path -Parent $PSScriptRoot } else { Get-Location }
if (-not $BacklogRoot) { $BacklogRoot = Join-Path $RepoRoot "sdlc_backlog" }
$BacklogDir = Join-Path $BacklogRoot "backlog"
$TestsDir   = Join-Path $BacklogRoot "tests"

if (-not $SpecDir) {
    $SpecDir = if (Test-Path (Join-Path $RepoRoot "obsidian")) {
        Join-Path $RepoRoot "obsidian"
    } elseif (Test-Path (Join-Path $RepoRoot "spec")) {
        Join-Path $RepoRoot "spec"
    } else {
        Join-Path $RepoRoot "docs"
    }
}

$Results = @()

function Search-Folder {
    param([string]$Path, [string]$SearchPattern)
    if (-not (Test-Path $Path)) { return }
    $Files = Get-ChildItem -Path $Path -Filter "*.md" -Recurse

    foreach ($File in $Files) {
        $Content  = Get-Content $File.FullName -Raw
        $FileName = $File.BaseName
        if ($Status -and $Content -notmatch "Status:\s*$Status") { continue }
        if ($Content -match $SearchPattern) {
            $Title = "Untitled"
            if ($Content -match "^#\s+(.+)$") { $Title = $Matches[1] }
            $LineNum = 0
            Get-Content $File.FullName | ForEach-Object {
                $LineNum++
                if ($_ -match $SearchPattern) {
                    $Context = $_.Trim()
                    if ($Context.Length -gt 80) { $Context = $Context.Substring(0, 77) + "..." }
                    $script:Results += [PSCustomObject]@{
                        ID = $FileName; Title = $Title
                        Path = $File.FullName.Replace($RepoRoot, "."); Line = $LineNum; Match = $Context
                    }
                }
            }
        }
    }
}

if ($SpecAudit) {
    Write-Host "Scanning spec directory for critical keywords: $SpecDir" -ForegroundColor Cyan
    $Pattern = "\b(MUST|SHALL|Rule:|Mandate:|Crucial:|REQUIRED)\b"
    Search-Folder $SpecDir $Pattern
} else {
    if ($Type -eq "Initiative")    { Search-Folder (Join-Path $BacklogDir "initiatives")  $Query }
    elseif ($Type -eq "Epic")      { Search-Folder (Join-Path $BacklogDir "epics")         $Query }
    elseif ($Type -eq "Story")     { Search-Folder (Join-Path $BacklogDir "stories")       $Query }
    elseif ($Type -eq "Subtask")   { Search-Folder (Join-Path $BacklogDir "subtasks")      $Query }
    elseif ($Type -eq "TestPlan")  { Search-Folder (Join-Path $TestsDir "plans")           $Query }
    elseif ($Type -eq "TestSet")   { Search-Folder (Join-Path $TestsDir "sets")            $Query }
    elseif ($Type -eq "TestDesign"){ Search-Folder (Join-Path $TestsDir "designs")         $Query }
    elseif ($Type -eq "TestExecution"){ Search-Folder (Join-Path $TestsDir "executions")   $Query }
    else {
        Search-Folder $BacklogDir $Query
        Search-Folder $TestsDir   $Query
    }
}

if ($Results.Count -gt 0) {
    Write-Host "Found $($Results.Count) match(es):" -ForegroundColor Cyan
    if ($SpecAudit) {
        $Results | Sort-Object Path, Line | Format-Table @{L='File';E={$_.Path}}, Line, Match -AutoSize
    } else {
        $Results | ForEach-Object {
            Write-Host "`n$($_.ID) - $($_.Title)" -ForegroundColor Green
            Write-Host "  $($_.Path):$($_.Line)" -ForegroundColor Gray
            Write-Host "  > $($_.Match)" -ForegroundColor White
        }
    }
    exit 0
} else {
    Write-Host "No matches found." -ForegroundColor Yellow
    exit 1
}
