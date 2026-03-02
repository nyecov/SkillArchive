# Kaizen Sprint Report: Context Engine Fine-Tuning

## 1. Targeted Friction (Hansei)
Based on Phase 2 & 3, the current system design fails to account for:
1. Hardcoded latency limits preventing users from optimizing server wait times.
2. Vague error feedback causing agent hallucination when parsing fails.

## 2. Root Cause Analysis (5-Whys)
1. **Why is latency hardcoded?** Because we didn't initially prioritize host-configurable ENV maps for internal Go contexts.
2. **Why does the agent hallucinate on error?** Because standard `panic()` or empty returns give no instructional payload on *how* to fix the malformed query string.

## 3. Implementation (Shisa Kanko)
**The Fix for Latency:**
We will expose an environment variable in `docker-compose.yml`.
```yaml
environment:
  - CONTEXT_TIMEOUT_MS=5000 # Default user-configurable timeout
```
Inside the Go server, the first action of `main.go` will be parsing this env. Every MCP tool execution will be wrapped in a context bound to this timeout threshold.

**The Fix for Feedback:**
The Go server must implement a custom Error wrapper. When JSON mapping fails, instead of "Error parsing", it must return an exact MCP payload containing instruction, e.g.:
`"ToolError: Malformed Query. Ensure your JSON/TOON targets match the schema EXACTLY. Stop, review the input file format, and retry the ingest_context tool."`

## 4. Yokoten Standard
These two principles (Configurable Host Bounds, Guiding Error Signatures) are now formally approved and must be written into the `Head/Context_Engine_Specification.md`.
