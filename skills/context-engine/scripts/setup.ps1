# Context Engine: Automated Setup & Verification (Poka-yoke)

$ErrorActionPreference = "Stop"

Write-Host "--- Context Engine: Jidoka Boot Sequence ---" -ForegroundColor Cyan

# 1. Environment Check (Nemawashi)
Write-Host "[1/3] Verifying Docker environment..."
try {
    docker version > $null
} catch {
    Write-Error "FATAL: Docker Engine is not running. Please start Docker and retry."
    exit 1
}

# 2. Build Sequence (Standardization)
Write-Host "[2/3] Building Context Engine image (context-engine-go:latest)..."
docker build -t context-engine-go:latest .
if ($LASTEXITCODE -ne 0) {
    Write-Error "FATAL: Docker build failed. Check logs."
    exit 1
}

# 3. Boot Diagnostics (Shisa Kanko)
Write-Host "[3/3] Running Boot Diagnostics (PRAGMA integrity_check)..."
$DiagOutput = docker run --rm -v "${PWD}:/workspace" -e "WORKSPACE_ROOT=/workspace" context-engine-go:latest /context-engine-server --diag 2>&1
if ($DiagOutput -match "Integrity Check Passed") {
    Write-Host "SUCCESS: Context Engine is healthy and Swarm-ready." -ForegroundColor Green
} else {
    Write-Warning "WARNING: Diagnostics flagged a potential issue. Check engine_diagnostics.log."
    Write-Host "$DiagOutput" -ForegroundColor Red
}

Write-Host "-------------------------------------------"
Write-Host "Setup Complete. Execute ./scripts/connect.ps1 to engage."
