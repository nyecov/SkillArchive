$ErrorActionPreference = "Stop"

$ContainerName = "context-engine-daemon"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$ComposeFile = Join-Path $ScriptDir "..\docker-compose\docker-compose.yml"

# Check if container is running
$IsRunning = "false"
try {
    $IsRunning = docker inspect -f '{{.State.Running}}' $ContainerName 2>$null
} catch {
    $IsRunning = "false"
}

if ($IsRunning -ne "true") {
    Write-Host "Starting Context Engine Daemon..."
    docker compose -f $ComposeFile up -d context-engine-daemon
    if ($LASTEXITCODE -ne 0) {
        Write-Error "FATAL (Jidoka): Failed to start Context Engine daemon."
        exit 1
    }
}

# Kill any orphaned server process from a previous session to prevent
# 15-second singleton lock contention on every agent reconnect.
try {
    docker exec $ContainerName sh -c 'kill $(pidof context-engine-server) 2>/dev/null' 2>$null
    # Brief pause to allow lock file cleanup from graceful shutdown
    Start-Sleep -Milliseconds 500
} catch {
    # No orphan found — clean state
}

# Execute the server binary inside the running container
docker exec -i $ContainerName /context-engine-server