# Context Engine Infrastructure Validator
# This script performs a Poka-yoke check of the agent's MCP environment.

Write-Host "--- Context Engine: Infrastructure Audit ---" -ForegroundColor Cyan

# 1. Check Docker Daemon
Write-Host "[1/4] Checking Docker Daemon..." -NoNewline
docker ps >$null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host " FAILED" -ForegroundColor Red
    Write-Host "  -> ACTION: Start the Docker Desktop/Daemon immediately." -ForegroundColor Yellow
    exit 1
}
Write-Host " OK" -ForegroundColor Green

# 2. Check Image Existence
Write-Host "[2/4] Checking 'context-engine-go:latest' image..." -NoNewline
docker image inspect context-engine-go:latest >$null 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host " MISSING" -ForegroundColor Red
    Write-Host "  -> ACTION: Run 'docker build -t context-engine-go:latest .' in the server root." -ForegroundColor Yellow
    exit 1
}
Write-Host " OK" -ForegroundColor Green

# 3. Check Workspace Mounting
Write-Host "[3/4] Verifying Workspace Root mapping..." -NoNewline
if ($env:WORKSPACE_ROOT -eq $null) {
    Write-Host " WARNING" -ForegroundColor Yellow
    Write-Host "  -> NOTE: WORKSPACE_ROOT env var is not set locally (may be set inside container)."
} else {
    Write-Host " OK ($env:WORKSPACE_ROOT)" -ForegroundColor Green
}

# 4. Check Singleton Lock
Write-Host "[4/4] Checking for Singleton Residency locks..." -NoNewline
if (Test-Path "g:\Skill Archive\.engine.instance.lock") {
    Write-Host " LOCKED" -ForegroundColor Red
    Write-Host "  -> ACTION: Ensure no other Context Engine instances are running." -ForegroundColor Yellow
    exit 1
}
Write-Host " CLEAR" -ForegroundColor Green

Write-Host "--- Audit Complete: Infrastructure is Green ---" -ForegroundColor Green
