# Connects the MCP Client to the running Context Engine Daemon
# This eliminates "Cold Start" latency by reusing a persistent container.

$container = "context-engine-daemon"
$compose_file = "g:\Skill Archive\temp__mem\Head\server\docker-compose.yml"

# Verify if container is running
$state = docker inspect -f '{{.State.Running}}' $container 2>$null
if ($state -ne "true") {
    # Attempt to start via compose
    docker-compose -f $compose_file up -d context-engine-daemon
}

# Execute the server binary inside the running container
# stdin/stdout are attached directly for MCP communication
docker exec -i $container /context-engine-server
