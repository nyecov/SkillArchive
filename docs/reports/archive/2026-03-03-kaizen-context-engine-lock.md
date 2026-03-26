# Kaizen Sprint Report: Context Engine Singleton Lock Flakiness (Revised)

## 1. The Anomaly (Genchi Genbutsu & Hansei)
- **Observed Behavior:** The Context Engine server fails to boot after an unclean shutdown, citing a "stale lock" error. A 15-second "Check-Wait-Seize" mechanism attempts to clear the file lock, but fails to recover on Windows environments due to open file handles held by the OS.
- **Initial Fix Failure (Hansei):** A previous Kaizen attempted to solve this by binding to a local TCP port (`49152`). However, this completely broke the cross-container guardrail. Because the Context Engine runs inside ephemeral Docker containers, each container has its own isolated network namespace. Multiple containers could bind to the same port internally, completely bypassing the Singleton lock and silently corrupting the shared `ontology.wal` memory volume.
- **Root Cause (5-Whys):** The naive file-existence check (`.engine.instance.lock`) combined with `os.Remove()` lacked OS-level process guarantees. The network namespace isolation in Docker rendered internal port binding useless for cross-container locks on shared volume mounts.

## 2. The Solution (Kaizen & Poka-yoke)
- **Hypothesis:** If we replace the naive file-existence check with a true POSIX file lock (`flock`) on the `.engine.instance.lock` file residing in the shared Docker volume (`.gemini/mem`), the OS will inherently guarantee mutual exclusion across all containers mounting that volume.
- **Interlock:** Implementing `github.com/gofrs/flock` acts as a strict, deterministic guardrail. It physically prevents a second process (or container) from acquiring the file descriptor lock. Furthermore, the OS network/filesystem stack guarantees automatic cleanup by releasing the POSIX lock when the process tree terminates (cleanly or via a crash), mechanically preventing "stale locks."

## 3. The Evidence (Shisa Kanko)
- **Baseline vs New State:** 
  - **Baseline:** 15s boot delay after crash, often resulting in permanent boot failure requiring manual file deletion. Broken cross-container safety.
  - **New State:** Instant boot failure if legitimately in use by *any* container on the same host mounting the volume. Instant recovery if the previous container crashed, because the OS releases the `flock` instantly.
- **Verification Result:** PASS (POSIX file locks properly propagate across Docker volumes, securing the memory).

## 4. The Standard (Yokoten)
- **New Standard Operating Procedure:** 
  1. Never use basic file-existence (`os.Stat` + `os.Remove`) for cross-process locking in multi-platform agents. 
  2. **Docker Boundary Awareness:** Never use localhost port binding (`net.Listen`) to prevent cross-container collisions on shared volumes, as network namespaces are isolated.
  3. Always default to OS-managed POSIX file locks (`flock`) on the shared volume itself to enforce cross-container concurrency safety.
- **Horizontal Targets:** This anti-pattern should be hunted and replaced in `nomos-memory` and `phobos-satellite` servers.
