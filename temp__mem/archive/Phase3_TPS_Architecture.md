# TPS Architecture Proposal: Context Engine V2

## 1. Vision & Strategy Alignment
This review takes the Critical Actions from Phase 2 (Timeouts, Enhanced Feedback, Tiered Limits) and maps their integration into the physical Go server and `docker-compose` topology. The strategy remains entirely aligned with "Minimal Footprint, Maximum Determinism."

## 2. Value Stream Modification
The critical update happens at the `server/cmd/server/main.go` load phase:
- **Baseline Stream:** Server boot -> Read ENV -> Start stdio loop -> Handle Tool.
- **Modified Stream:** Server boot -> **Read `CONTEXT_TIMEOUT_MS` from ENV** -> Start stdio loop.
When `ingest_context` or `read_ontology` is called, the context injected into the Go handler is wrapped in a `context.WithTimeout` bound to that Docker configuration.

## 3. Poka-yoke & Jidoka Interlocks

### The Tiered Memory Limit (KYT Resolution)
The "Infinite Growth Problem" requires a structural safeguard:
- **Warning Threshold (Soft Limit):** At 8,000 characters. The tool returns the JSON output appended with a system warning: `[WARNING: SCRATCHPAD SOFT LIMIT REACHED. PRUNE BEFORE 10,000.]`
- **Jidoka Halt (Hard Limit):** At 10,000 characters. The `log_session_finding` tool executes an autonomous halt, completely rejecting the new payload and returning an MCP Error `ToolError: Hard Limit Breached. You must review the session and delete items before continuing.`

### Single-Agent Threading
Because multi-agent support is explicitly denied, the OS-level file lock is now drastically simplified. We do not need complex PID tracking or Mutex wait queues. The lock simply asserts `if lock.Exists() { assume_panic_and_overrule() }` after a 5-second interval, as no other healthy agent could possibly be holding it.

## 4. Rollout Plan (Heijunka)
1. **Pilot Phase:** Implement the Error Feedback format on a single tool (`ingest_context`).
2. **Vertical Rollout:** Add the Tiered Limit array to `log_session_finding`.
3. **Environment Hook:** Push `CONTEXT_TIMEOUT_MS: 3000` to the Docker compose YAML.
