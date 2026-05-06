#Requires -Version 5.1
<#
.SYNOPSIS
    One-shot installer for project pre-commit hooks via the pre-commit framework.
    Idempotent — safe to re-run. Compatible with PowerShell 5.1 and 7.

.DESCRIPTION
    Installs the `pre-commit` Python framework (if missing) and wires the
    .pre-commit-config.yaml hooks into .git/hooks/pre-commit.

    After install, hooks fire automatically on `git commit`. To run manually:
        pre-commit run --all-files
        pre-commit run --all-files --hook-stage manual

.PARAMETER Force
    Re-install even if already installed.

.PARAMETER SkipGoTools
    Skip installation of Go-specific tools (goimports, golangci-lint).
    Use when the project is not a Go project.

.EXAMPLE
    .\install-hooks.ps1
    .\install-hooks.ps1 -Force
    .\install-hooks.ps1 -SkipGoTools
#>

param(
    [switch]$Force,
    [switch]$SkipGoTools
)

$ErrorActionPreference = 'Stop'

Write-Host '==> Pre-commit hook installer' -ForegroundColor Cyan

# 1. pre-commit framework
$preCommitVersion = & pre-commit --version 2>$null
if ($LASTEXITCODE -ne 0 -or $Force) {
    Write-Host '    pre-commit not found; installing via pip...' -ForegroundColor Yellow
    & pip install --upgrade pre-commit
    if ($LASTEXITCODE -ne 0) {
        Write-Host '    pip install pre-commit failed.' -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "    pre-commit detected: $preCommitVersion" -ForegroundColor Green
}

# 2. Optional Go tooling
if (-not $SkipGoTools) {
    foreach ($tool in @(
        @{ Name = 'goimports';     Pkg = 'golang.org/x/tools/cmd/goimports@latest' },
        @{ Name = 'golangci-lint'; Pkg = 'github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest' }
    )) {
        & $tool.Name --version 2>$null > $null
        if ($LASTEXITCODE -ne 0 -or $Force) {
            Write-Host "    installing $($tool.Name) via go install..." -ForegroundColor Yellow
            & go install $tool.Pkg
            if ($LASTEXITCODE -ne 0) {
                Write-Host "    go install $($tool.Pkg) failed. Use -SkipGoTools to skip." -ForegroundColor Yellow
            }
        } else {
            Write-Host "    $($tool.Name) detected" -ForegroundColor Green
        }
    }
}

# 3. Wire pre-commit framework hook into .git/hooks/
Write-Host '    wiring .git/hooks/pre-commit...' -ForegroundColor Yellow
& pre-commit install
if ($LASTEXITCODE -ne 0) {
    Write-Host '    pre-commit install failed.' -ForegroundColor Red
    exit 1
}

# 4. Smoke-test
Write-Host '    smoke-testing required hooks against current tree...' -ForegroundColor Yellow
& pre-commit run --all-files
$smokeExit = $LASTEXITCODE

Write-Host ''
Write-Host '==> Install complete' -ForegroundColor Cyan
if ($smokeExit -eq 0) {
    Write-Host '    Required hooks: GREEN' -ForegroundColor Green
} else {
    Write-Host "    Required hooks reported issues (exit $smokeExit). Address them before relying on the gate." -ForegroundColor Yellow
}
Write-Host '    Manual-stage hooks are not run automatically.'
Write-Host '    Run on demand: pre-commit run --all-files --hook-stage manual'
