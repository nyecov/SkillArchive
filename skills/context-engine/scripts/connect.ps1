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

# Execute the server binary inside the running container
docker exec -i $ContainerName /context-engine-server