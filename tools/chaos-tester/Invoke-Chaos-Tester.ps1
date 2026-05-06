#Requires -Version 5.1
<#
.SYNOPSIS
    Requests edge-case and "chaos" test scenarios for a source file.
    Compatible with PowerShell 5.1 and 7.

.DESCRIPTION
    Prompts for adversarial / edge-case test scenario generation for a given source file.
    Can target a specific resilience guide if one exists in the project spec directory.

    Use during the Red Phase for high-risk logic to surface boundary conditions,
    invalid input combinations, and failure modes before writing the primary test suite.

.PARAMETER SourceFile
    Path to the source file to test.

.PARAMETER ResilienceGuide
    Optional path to an error-handling or resilience spec document for additional context.

.EXAMPLE
    .\Invoke-Chaos-Tester.ps1 -SourceFile ".\internal\domain\solver\solver.go"
    .\Invoke-Chaos-Tester.ps1 -SourceFile ".\src\parser.py" -ResilienceGuide ".\docs\error-handling.md"
#>

param(
    [Parameter(Mandatory=$true)]
    [string]$SourceFile,

    [Parameter(Mandatory=$false)]
    [string]$ResilienceGuide = ""
)

if (-not (Test-Path $SourceFile)) {
    Write-Host "Source file not found: $SourceFile" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "=== Chaos Testing Request ===" -ForegroundColor Cyan
Write-Host "Target file : $SourceFile" -ForegroundColor White

if ($ResilienceGuide -and (Test-Path $ResilienceGuide)) {
    Write-Host "Resilience  : $ResilienceGuide" -ForegroundColor White
    Write-Host ""
    Write-Host "Prompt for your AI model:" -ForegroundColor Yellow
    Write-Host "  Review '$SourceFile' alongside the resilience guide at '$ResilienceGuide'." -ForegroundColor Gray
    Write-Host "  Generate adversarial edge-case and chaos test scenarios covering:" -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "Prompt for your AI model:" -ForegroundColor Yellow
    Write-Host "  Review '$SourceFile' and generate adversarial edge-case and chaos test scenarios covering:" -ForegroundColor Gray
}

Write-Host "    - Boundary conditions (min/max values, empty inputs, null/zero)" -ForegroundColor Gray
Write-Host "    - Invalid input combinations" -ForegroundColor Gray
Write-Host "    - Concurrent access / race conditions (if applicable)" -ForegroundColor Gray
Write-Host "    - Resource exhaustion (large inputs, deep recursion)" -ForegroundColor Gray
Write-Host "    - Error propagation paths" -ForegroundColor Gray
Write-Host "    - State machine transitions that skip required steps" -ForegroundColor Gray
Write-Host ""
Write-Host "Each scenario should include: input, expected failure mode, and the test assertion." -ForegroundColor Gray
Write-Host "===========================" -ForegroundColor Cyan
