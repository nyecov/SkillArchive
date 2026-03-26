# Lean Analysis Report: Context Engine

## Executive Summary
The Context Engine's core logic is sound, but its implementation relies on naive file I/O and locking mechanisms that create significant bottlenecks and cross-platform instability (particularly on Windows). The reliance on full-file JSON rewrites for every mutation and file-based singleton locks are the primary sources of structural waste and flakiness.

## Phase Results

### Phase 1: Lean Foundations — 3M & 5S
- **Muri (Overburden):** The 10k hard limit on the scratchpad forces premature pruning. Full file rewrites (`saveOntologyState` with `Sync()`) overburden the disk/system on every small edge change.
- **Muda (Waste):** Redundant synchronization and serialization of the entire ontology graph on every single edge mutation.
- **Mura (Unevenness):** Performance variability when the ontology graph grows; graph traversal and serialization time scales poorly.

### Phase 2: Story Interview — Assumptions
- **Key finding:** The singleton lock's "Check-Wait-Seize" mechanism assumes that `os.Remove(lockPath)` is always sufficient to clear a stale lock. It fails to account for zombie processes holding file handles (especially on Windows), which will block the remove/rename operations.

### Phase 3: Value Stream Mapping — Bottlenecks
- **Key finding:** The primary bottleneck is the read-modify-write cycle. The entire JSON file is read, unmarshalled, mutated, marshalled, and written to disk synchronously for every single edge addition. A future state should implement an append-only WAL (Write-Ahead Log) or an embedded DB (e.g., SQLite/bbolt).

### Phase 4: KYT — Hazard Prediction
- **Key finding:** Ontology Corruption on Windows. `os.Rename(tmpPath, path)` in `saveOntologyState` is used for atomic writes. On Windows, `os.Rename` fails if the target file exists and is open/locked by another process (like an antivirus or an overlapping read), breaking the atomic guarantee and potentially corrupting state.

### Phase 5: Poka-yoke — Guardrails
- **Key finding:** Missing in-memory concurrency guardrails. While file-level locks exist, concurrent map reads/writes to `graph.Entities` from different MCP tool handlers within the *same* process could trigger a Go panic if not protected by a `sync.Mutex` or `sync.RWMutex`.
- **Key finding:** Missing input validation for `target_path` in `ingest_context`, posing a directory traversal risk.

### Phase 6: Shisa Kanko — Verification
- **Singleton Lock:** Intent is to prevent multiple instances. Verification requires simulating a crash holding the file handle to ensure the recovery mechanism actually works on Windows.
- **Ontology Atomic Save:** Intent is to prevent corrupted JSON writes. Verification requires injecting a fault during `f.Write` and ensuring `os.Rename` robustness across OS platforms.

### Phase 7: Nemawashi — Dependencies
- **Key finding:** Ripple Risk. Upgrading the storage mechanism to a more robust solution (like an embedded DB or WAL) will require a migration path for existing `ontology.json` and `current_session.json` files to avoid breaking existing agents.

### Phase 8: Shusa Leadership — Alignment
- **Key finding:** Misaligned execution. The vision of a robust context engine is compromised by naive file I/O operations that are notoriously flaky in concurrent, cross-platform environments. 

### Phase 9: Yokoten — Pattern Transfer
- **Key finding:** The anti-pattern of using basic file existence checks for cross-process locking (`os.Stat` -> `os.Remove`) must be broadcasted. Any other Go-based MCP servers in the project (e.g., `nomos-memory`, `phobos-satellite`) must be audited to ensure they do not replicate this flaky locking mechanism.

## Critical Actions
1. **Refactor Singleton Lock:** Replace the file-based singleton lock with a more robust, OS-agnostic inter-process locking mechanism (e.g., socket binding or an established cross-platform locking library like `gofrs/flock`).
2. **Implement In-Memory Mutexes:** Add `sync.RWMutex` to the internal maps (Scratchpad and Ontology) to prevent concurrent map read/write panics from simultaneous MCP requests.
3. **Overhaul Storage Layer:** Replace the full-file read-modify-write cycle for the Ontology with either an append-only WAL (Write-Ahead Log) or an embedded database (like SQLite or bbolt) to eliminate Muri and Muda.
4. **Harden File Operations:** Ensure all file operations (especially `os.Rename`) use robust wrappers that handle Windows-specific file locking quirks.
5. **Add Input Validation:** Sanitize `target_path` in `ingest_context` to prevent directory traversal.

## Yokoten Broadcast
- Broadcast the dangers of naive file-based cross-process locking to the authors of `nomos-memory` and `phobos-satellite`.
