#Requires -Version 5.1
<#
.SYNOPSIS
    Automates the validation, staging, committing, and pushing of Agile SDLC updates.
    Compatible with PowerShell 5.1 and 7.

    MANDATE: Commit in reasonable batches. Do not resync parent artifacts
    (e.g., adding story links to an Epic) for every single minute child change.
    Wait until a batch of child items is done, then sync the parent and run this script.

.PARAMETER Phase
    The SDLC phase completed.

.PARAMETER ID
    The ID of the primary artifact updated (e.g., STORY-AREA-01-04).

.PARAMETER Message
    A brief description of the specific work done (no [Phase] prefix — the script adds it).

.PARAMETER BacklogRoot
    Optional: path to the SDLC backlog root. Default: <repo-root>/sdlc_backlog.

.PARAMETER SkipPush
    Do not push to remote after committing.

.EXAMPLE
    .\Complete-AgileTurn.ps1 -Phase Carving -ID STORY-AREA-01-04 -Message "Mapped solver phases"
    .\Complete-AgileTurn.ps1 -Phase Red -ID STORY-AREA-01-04 -Message "Add failing test for AC-02"
#>

[CmdletBinding(PositionalBinding=$false)]
param (
    [Parameter(Mandatory=$true, ValueFromPipeline=$true)]
    [ValidateSet(
        "Carving", "Refining", "TestDesign", "TestSet", "TestPlan", "TestExecution",
        "Implementation", "Validation", "Maintenance", "Epic", "Initiative",
        "Foundations", "UX", "Red", "Green", "Refactor", "Fix", "Meta"
    )]
    [string]$Phase,

    [Parameter(Mandatory=$true)]
    [string]$ID,

    [Parameter(Mandatory=$true)]
    [string]$Message,

    [string]$BacklogRoot = "",

    [switch]$SkipPush
)

$ToolsDir = if ($PSScriptRoot) { $PSScriptRoot } else { Split-Path -Parent $MyInvocation.MyCommand.Definition }
if (-not $ToolsDir) { $ToolsDir = "." }
$RepoRoot = Split-Path -Parent $ToolsDir

if (-not $BacklogRoot) {
    $BacklogRoot = Join-Path $RepoRoot "sdlc_backlog"
}

# 1. Validate Hierarchy (BLOCKING)
$ValidatorPath = Join-Path $ToolsDir "Validate-AgileHierarchy.ps1"
if (Test-Path $ValidatorPath) {
    Write-Host "--- Validating Agile Hierarchy ---" -ForegroundColor Cyan
    & $ValidatorPath -BacklogRoot $BacklogRoot
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Hierarchy validation failed. Commit aborted."
        exit 1
    }
} else {
    Write-Host "  (Validate-AgileHierarchy.ps1 not found next to this script; skipping)" -ForegroundColor DarkYellow
}

# 2. Advisory: Issue Triage
$TriagePath = Join-Path $ToolsDir "Triage-Issues.ps1"
if (Test-Path $TriagePath) {
    Write-Host "--- Advisory: Issue Triage ---" -ForegroundColor Cyan
    & $TriagePath -Open
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  (advisory - BLOCKER or stale issue exists; route owner must act)" -ForegroundColor DarkYellow
    }
}

# 3. Stage standard SDLC paths
Write-Host "--- Staging Changes ---" -ForegroundColor Cyan
$StagePaths = @(
    (Join-Path $RepoRoot ".map-spec"),
    $BacklogRoot,
    (Join-Path $RepoRoot "skills"),
    (Join-Path $RepoRoot "tools")
)
foreach ($p in $StagePaths) {
    if (Test-Path $p) {
        git -C "$RepoRoot" add "$p"
    }
}

# 4. Commit
$CommitMsg = "[$Phase] $ID: $Message"
Write-Host "--- Committing: $CommitMsg ---" -ForegroundColor Cyan
git -C "$RepoRoot" commit -m "$CommitMsg"
$commitExit = $LASTEXITCODE

# Two-pass retry: some pre-commit auto-fix hooks (e.g. goimports) abort the first
# commit when they modify files. A second attempt finds a clean tree and succeeds.
if ($commitExit -ne 0) {
    Write-Host "--- First commit attempt failed (possible auto-fix hook); retrying once ---" -ForegroundColor Yellow
    git -C "$RepoRoot" commit -m "$CommitMsg"
    $commitExit = $LASTEXITCODE
}

if ($commitExit -eq 0) {
    if (-not $SkipPush) {
        Write-Host "--- Pushing to Remote ---" -ForegroundColor Cyan
        git -C "$RepoRoot" push
    }
} else {
    Write-Host "Nothing to commit or commit failed after retry." -ForegroundColor Yellow
}
