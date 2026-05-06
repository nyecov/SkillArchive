#Requires -Version 5.1
<#
.SYNOPSIS
    Validates the strict parentage hierarchy and link integrity across backlog and testing artifacts.
    Compatible with PowerShell 5.1 and 7.

    Run before every batch commit. Also called automatically by Complete-AgileTurn.ps1.

.PARAMETER BacklogRoot
    Root of the SDLC backlog directory (default: <repo-root>/sdlc_backlog).

.EXAMPLE
    .\Validate-AgileHierarchy.ps1
    .\Validate-AgileHierarchy.ps1 -BacklogRoot ".\my-backlog"
#>

param(
    [string]$BacklogRoot = ""
)

$RepoRoot = if ($PSScriptRoot) { Split-Path -Parent $PSScriptRoot } else { Get-Location }
if (-not $BacklogRoot) {
    $BacklogRoot = Join-Path $RepoRoot "sdlc_backlog"
}

$BacklogDir = Join-Path $BacklogRoot "backlog"
$TestsDir   = Join-Path $BacklogRoot "tests"

$Errors = @()

function Test-Artifact {
    param($Path, $Type, $ParentPrefix)

    $Content  = Get-Content $Path -Raw
    $FileName = [System.IO.Path]::GetFileNameWithoutExtension($Path)

    $ParentHeader = switch ($Type) {
        "Epic"          { "Parent Initiative" }
        "Story"         { "Parent Epic" }
        "Subtask"       { "Parent Story" }
        "TestSet"       { "Parent Test Plan" }
        "TestDesign"    { "Parent Test Set" }
        "TestExecution" { "Executes" }
        default         { "" }
    }

    if ($ParentHeader) {
        if ($Content -match "## $ParentHeader\r?\n\[($ParentPrefix-.*?)\]\((.*?)\)") {
            $ParentRelPath  = $Matches[2]
            $ParentFullPath = Join-Path (Split-Path $Path) $ParentRelPath
            if (-not (Test-Path $ParentFullPath)) {
                $script:Errors += "[$FileName] Parent link broken: $($Matches[1]) -> $ParentRelPath"
            }
        } else {
            $script:Errors += "[$FileName] Missing or malformed parent link for '$ParentHeader'"
        }
    }
}

# Epics (parent: INIT)
$EpicsDir = Join-Path $BacklogDir "epics"
if (Test-Path $EpicsDir) {
    Get-ChildItem -Path $EpicsDir -Filter "*.md" | ForEach-Object {
        Test-Artifact $_.FullName "Epic" "INIT"
    }
}

# Stories (parent: EPIC)
$StoriesDir = Join-Path $BacklogDir "stories"
if (Test-Path $StoriesDir) {
    Get-ChildItem -Path $StoriesDir -Filter "*.md" | ForEach-Object {
        Test-Artifact $_.FullName "Story" "EPIC"
    }
}

# Subtasks (parent: STORY)
$SubDir = Join-Path $BacklogDir "subtasks"
if (Test-Path $SubDir) {
    Get-ChildItem -Path $SubDir -Filter "*.md" | ForEach-Object {
        Test-Artifact $_.FullName "Subtask" "STORY"
    }
}

# Test Sets (parent: TP)
$SetsDir = Join-Path $TestsDir "sets"
if (Test-Path $SetsDir) {
    Get-ChildItem -Path $SetsDir -Filter "*.md" -ErrorAction SilentlyContinue | ForEach-Object {
        Test-Artifact $_.FullName "TestSet" "TP"
    }
}

# Test Designs (parent: TS)
$DesignsDir = Join-Path $TestsDir "designs"
if (Test-Path $DesignsDir) {
    Get-ChildItem -Path $DesignsDir -Filter "*.md" -ErrorAction SilentlyContinue | ForEach-Object {
        Test-Artifact $_.FullName "TestDesign" "TS"
    }
}

# Test Executions (parent: TD or TC)
$ExecDir = Join-Path $TestsDir "executions"
if (Test-Path $ExecDir) {
    Get-ChildItem -Path $ExecDir -Filter "*.md" -ErrorAction SilentlyContinue | ForEach-Object {
        Test-Artifact $_.FullName "TestExecution" "TD|TC"
    }
}

# Issues (flat-namespaced; validate enum fields and Affects links)
$IssuesDir = Join-Path $BacklogDir "issues"
$ValidStatus   = @("OPEN", "TRIAGED", "ROUTED", "RESOLVED", "CLOSED")
$ValidSeverity = @("BLOCKER", "HIGH", "MEDIUM", "LOW")
$ValidRoutedTo = @("Analyst", "Architect", "PO", "Security-Lead", "UX-Designer", "DevOps", "Scrum-Master")

if (Test-Path $IssuesDir) {
    Get-ChildItem -Path $IssuesDir -Filter "ISSUE-*.md" -ErrorAction SilentlyContinue | ForEach-Object {
        $Path     = $_.FullName
        $FileName = $_.BaseName
        $Content  = Get-Content $Path -Raw

        if ($FileName -notmatch "^ISSUE-\d{2}-[A-Za-z0-9\-]+$") {
            $script:Errors += "[$FileName] Bad ISSUE filename — expected ISSUE-<NN>-<Slug>"
        }

        foreach ($pair in @(
            @{ Label = "Status";    Set = $ValidStatus    },
            @{ Label = "Severity";  Set = $ValidSeverity  },
            @{ Label = "Routed To"; Set = $ValidRoutedTo  }
        )) {
            $label = $pair.Label
            if ($Content -match "(?m)^- \*\*$label\*\*:\s*(.+?)\s*$") {
                $val = $Matches[1].Trim()
                if ($val -notin $pair.Set) {
                    $script:Errors += "[$FileName] Invalid $label value: '$val'"
                }
            } else {
                $script:Errors += "[$FileName] Missing required field: $label"
            }
        }

        if ($Content -match "(?s)## Affects(.*?)(?=\r?\n## )") {
            $block = $Matches[1]
            $links = [regex]::Matches($block, "\(([^)]+\.md)\)")
            foreach ($m in $links) {
                $relPath    = $m.Groups[1].Value
                $targetPath = Join-Path (Split-Path $Path) $relPath
                if (-not (Test-Path $targetPath)) {
                    $script:Errors += "[$FileName] Affects link broken: $relPath"
                }
            }
        } else {
            $script:Errors += "[$FileName] Missing '## Affects' section"
        }
    }
}

if ($Errors.Count -gt 0) {
    Write-Host "Hierarchy Validation Failed:" -ForegroundColor Red
    $Errors | ForEach-Object { Write-Host " - $_" -ForegroundColor Yellow }
    exit 1
} else {
    Write-Host "Hierarchy Validation Passed." -ForegroundColor Green
    exit 0
}
