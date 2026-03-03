#!/bin/bash
# Connects the MCP Client to the running Context Engine Daemon
# This eliminates "Cold Start" latency by reusing a persistent container.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"
COMPOSE_FILE="$SCRIPT_DIR/../docker-compose/docker-compose.yml"
CONTAINER="context-engine-daemon"

# Verify if container is running
if [ "$(docker inspect -f '{{.State.Running}}' $CONTAINER 2>/dev/null)" != "true" ]; then
    echo "Starting Context Engine Daemon..." >&2
    docker compose -f "$COMPOSE_FILE" up -d context-engine-daemon
fi

# Kill any orphaned server process from a previous session to prevent
# 15-second singleton lock contention on every agent reconnect.
docker exec "$CONTAINER" sh -c 'kill $(pidof context-engine-server) 2>/dev/null' 2>/dev/null || true
sleep 0.5  # Brief pause to allow lock file cleanup from graceful shutdown

# Execute the server binary inside the running container
exec docker exec -i "$CONTAINER" /context-engine-server
