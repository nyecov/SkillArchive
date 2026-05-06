#Requires -Version 5.1
<#
.SYNOPSIS
    Scans a spec directory against a map-spec ledger to find unmapped spec files.
    Compatible with PowerShell 5.1 and 7.

.PARAMETER SpecDir
    Directory containing spec markdown files. Default: <repo-root>/obsidian (or spec/).

.PARAMETER LedgerDir
    Directory containing .map-spec ledger subdirectories. Default: <repo-root>/.map-spec.

.EXAMPLE
    .\Find-SpecGaps.ps1
    .\Find-SpecGaps.ps1 -SpecDir ".\docs\specs" -LedgerDir ".\.map-spec"
#>

param(
    [string]$SpecDir   = "",
    [string]$LedgerDir = ""
)

$RepoRoot = if ($PSScriptRoot) { Split-Path -Parent $PSScriptRoot } else { Get-Location }

if (-not $SpecDir) {
    foreach ($candidate in @("obsidian","spec","docs\specs","docs")) {
        $p = Join-Path $RepoRoot $candidate
        if (Test-Path $p) { $SpecDir = $p; break }
    }
    if (-not $SpecDir) { $SpecDir = Join-Path $RepoRoot "docs" }
}

if (-not $LedgerDir) { $LedgerDir = Join-Path $RepoRoot ".map-spec" }

if (-not (Test-Path $LedgerDir)) {
    Write-Host "No ledger directory found at: $LedgerDir" -ForegroundColor Yellow
    Write-Host "Run the spec-mapping skill to initialize the ledger." -ForegroundColor Yellow
    exit 0
}

# Collect processed spec files from ledger subdirectories
$Processed = @()
Get-ChildItem -Path $LedgerDir -Directory | ForEach-Object {
    if ($_.Name -ne "_templates") {
        $SpecGapsPath = Join-Path $_.FullName "SPEC-GAPS.md"
        if (Test-Path $SpecGapsPath) {
            $Content = Get-Content $SpecGapsPath -Raw
            if ($Content -match "SPEC-GAPS: (.+?)\.md") {
                $Processed += $Matches[1] + ".md"
            }
        }
    }
}

# All spec markdown files
$AllSpec = Get-ChildItem -Path $SpecDir -Filter "*.md" -ErrorAction SilentlyContinue |
    ForEach-Object { $_.Name }

$Unmapped = $AllSpec | Where-Object { $Processed -notcontains $_ }

if ($Unmapped) {
    Write-Host "Unmapped spec files ($($Unmapped.Count)):" -ForegroundColor Yellow
    $Unmapped | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }
    exit 1
} else {
    Write-Host "All spec files mapped. ($($AllSpec.Count) total)" -ForegroundColor Green
    exit 0
}
