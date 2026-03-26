# Development Story: Context Engine Connectivity and Lock Resolution

## 1. User Value (Why)
Ensure the Context Engine MCP server remains reliably connected and successfully negotiates the singleton lock without false positives, avoiding 'offline' states while the container is actually running.

## 2. Core Logic (How)
1. **Connectivity Migration:** Update `mcp_config.json` to utilize **Daemon Mode**. Instead of `docker run` (which attempts to create a new container that collides with the lock), the config will use `docker exec -i context-engine-daemon /context-engine-server` or the provided `connect.ps1` script to connect to the always-on daemon.
2. **Zombie Cleanup:** Implement a robust auto-cleanup script (or one-time purge) to identify and kill any hanging `context-engine-go` containers (e.g., `admiring_agnesi`) that are incorrectly holding the POSIX volume lock.

## 3. Edge Cases & Constraints
- **Daemon Lifecycle:** If the daemon container itself is down or crashes, the MCP connection script must be robust enough to recognize the absence, spin the daemon back up via `docker-compose`, and *then* connect.
- **Cross-Platform:** The connection execution in `mcp_config.json` must be compatible with the current OS (Windows).

## 4. Verification Criteria
- [ ] Zombie containers are killed and removed.
- [ ] `mcp_config.json` is updated to point to the daemon.
- [ ] The `context-engine` tools can be called from the client successfully without returning "Not connected" or singleton lock collisions.
