#Requires -Version 5.1
<#
.SYNOPSIS
    Native pre-commit auto-fixer for staged Go source files.
    Runs BEFORE the pre-commit framework to avoid double-pass commit failures.

.DESCRIPTION
    Handles two auto-fixes for Go projects:
      1. goimports -w on staged .go files (formats + reconciles imports).
         Set $env:GOIMPORTS_LOCAL_PREFIX to your module path for local grouping.
      2. go mod tidy when any .go / go.mod / go.sum is staged.

    After fixing, re-stages the files via `git add`. Because this script runs
    OUTSIDE the pre-commit framework, the framework sees a clean staged tree
    and never triggers a "files were modified by this hook" abort.

    Caveat: operates on working-tree files (which match staged content when
    there are no unstaged WIP changes for those paths).

.NOTES
    Intended to be called from a .git/hooks/pre-commit shim installed by
    install-hooks.ps1. Not designed to be run directly by the user.

    Set GOIMPORTS_LOCAL_PREFIX environment variable to your Go module path
    (e.g., "github.com/myorg/myrepo") for correct import grouping.
#>

$ErrorActionPreference = 'Stop'

$staged = @(& git diff --cached --name-only --diff-filter=ACM)
if ($staged.Count -eq 0) { exit 0 }

$goFiles   = @($staged | Where-Object { $_ -match '\.go$' -and $_ -notmatch '^vendor/' })
$needsTidy = @($staged | Where-Object { $_ -match '\.go$|^go\.mod$|^go\.sum$' })

if ($goFiles.Count -gt 0) {
    $localPrefix = if ($env:GOIMPORTS_LOCAL_PREFIX) { $env:GOIMPORTS_LOCAL_PREFIX } else { "" }
    if ($localPrefix) {
        & goimports -w -local $localPrefix @goFiles
    } else {
        & goimports -w @goFiles
    }
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    & git add -- @goFiles
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

if ($needsTidy.Count -gt 0) {
    & go mod tidy
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    if (Test-Path go.mod) { & git add -- go.mod }
    if (Test-Path go.sum)  { & git add -- go.sum  }
}

exit 0
