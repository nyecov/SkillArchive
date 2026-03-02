#!/bin/bash
# Connects the MCP Client to the running Context Engine Daemon
# This eliminates "Cold Start" latency by reusing a persistent container.

CONTAINER="context-engine-daemon"
COMPOSE_FILE="g:/Skill Archive/temp__mem/Head/server/docker-compose.yml"

# Verify if container is running
if [ "$(docker inspect -f '{{.State.Running}}' $CONTAINER 2>/dev/null)" != "true" ]; then
    echo "Starting Context Engine Daemon..."
    docker-compose -f "$COMPOSE_FILE" up -d context-engine-daemon
fi

# Execute the server binary inside the running container
docker exec -i "$CONTAINER" /context-engine-server
