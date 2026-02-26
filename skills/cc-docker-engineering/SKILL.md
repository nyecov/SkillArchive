---
name: cc-docker-engineering
version: 1.1.0
description: >
  Comprehensive Docker engineering standards. 
  Covers multi-stage builds, layer caching, BuildKit optimization, security (non-root), and production-grade Dockerfile patterns.
category: engineering-standards
tags: [docker, devops, multi-stage, BuildKit, security, optimization, production]
references:
  - name: "Ship: Production Readiness"
    path: ../cc-ship-production/SKILL.md
  - name: Lean Principles (Muda Eradication)
    path: ../lean-principles-muda/SKILL.md
---

# Docker Engineering Standards

*Effective Docker usage is about minimizing build time, image size, and the attack surface.*

This skill provides the authoritative standard for building production-grade containers. It moves beyond "working" images to "optimized and secure" artifacts by applying Lean principles to the container lifecycle.

## Core Mandates

### 1. BuildKit Optimization (The Speed Gate)
You MUST utilize Docker BuildKit features to eliminate redundant work across builds.

- **Action:** Use `RUN --mount=type=cache` for package managers (apt, pip, npm, cargo).
- **Action:** Use `RUN --mount=type=bind` to access files without creating a layer.
- **Constraint:** DO NOT rely on simple layer caching for large dependency installations; it is too brittle.
- **Goal:** Sub-30 second rebuilds for minor code changes.

### 2. Manifest-First Caching & Stage Decoupling
Layer ordering MUST prioritize stability.

- **Action:** Copy dependency manifests (`package.json`, `requirements.txt`) BEFORE the source code.
- **Action:** Use `AS builder` stages for compilers/build-tools and a minimal final stage (alpine, distroless) for runtime.
- **Constraint:** The final image MUST NOT contain build-time secrets, git, or compilers.

### 3. Security & Non-Root Execution
Images MUST be secure by default.

- **Action:** Explicitly `USER` to a non-privileged account.
- **Action:** Use specific version tags (e.g., `python:3.12-slim`) instead of `latest`.
- **Constraint:** Never run processes as `root` unless absolutely required for low-level system access.

### 4. Context Optimization (Muda Reduction)
The build context MUST be as small as possible.

- **Action:** Maintain a strict `.dockerignore` to exclude `.git`, `node_modules`, `venv`, and local artifacts.
- **Goal:** Minimize "Sending build context to Docker daemon" time.

### 5. Deterministic CI Installation
Installation commands MUST prioritize lockfile integrity and speed.

- **Action:** Use `npm ci` (Node), `poetry install --sync` (Python), or equivalent "frozen" commands.
- **Constraint:** DO NOT use `npm install` or `pip install .` in CI/production stages as they may mutate the lockfile or resolve new versions unexpectedly.
- **Integration:** Directly supports **Jidoka** by halting the build if dependencies are inconsistent.

### 6. Observability & Portability
Images MUST be self-describing and architecture-aware.

- **Action:** Include a `HEALTHCHECK` that tests the actual application port (not just the process).
- **Action:** Use OCI labels for traceability (e.g., `LABEL org.opencontainers.image.source=...`).
- **Action:** Use `ARG` for platform-specific builds if the image will run on multiple architectures (AMD64/ARM64).

### 7. Signal-Aware Entrypoints (Clean Exit)
Entrypoints MUST handle termination signals (`SIGTERM`) correctly to avoid 10-second wait times and zombie processes.

- **Action:** ALWAYS use the **Exec Form** (`["executable", "param"]`) for `CMD` and `ENTRYPOINT`.
- **Constraint:** DO NOT use the "Shell Form" (raw string) as it wraps the process in `/bin/sh -c`, which does not forward signals.

### 8. Immutable Executables & Reduced Capabilities
The runtime environment MUST be hardened against runtime modification.

- **Action:** Ensure executables and system files are owned by `root` and are NOT world-writable, even when running as a non-root user.
- **Action:** Use `distroless` or `scratch` for compiled binaries to eliminate shell-based attack vectors.
- **Constraint:** Drop all Linux capabilities (`--cap-drop=ALL`) at runtime unless specific ones are required.

### 9. Stream-Based Observability
Logging MUST follow the Twelve-Factor App methodology.

- **Action:** Log everything to `stdout` and `stderr`.
- **Constraint:** DO NOT log to files inside the container; this complicates log rotation and persistence.

## Implementation Patterns

### Go (Distroless) Example
```dockerfile
# syntax=docker/dockerfile:1
FROM golang:1.22-alpine AS builder
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

FROM gcr.io/distroless/static-debian12
COPY --from=builder /app/main /main
# Immutable: Owned by root, executed by non-root
USER 65532:65532
ENTRYPOINT ["/main"]
```

### Python (Poetry) Example
```dockerfile
# syntax=docker/dockerfile:1
FROM python:3.12-slim AS builder
WORKDIR /app
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && \
    apt-get install -y --no-install-recommends build-essential
RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN --mount=type=cache,target=/root/.cache/pypoetry \
    poetry install --no-root

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1
COPY src/ src/
# Non-root UID
USER 1000
ENTRYPOINT ["python"]
CMD ["-m", "src.main"]
```

## Escalation & Halting

- **Jidoka:** Halt if `secrets.env` or similar sensitive files are detected in the build context.
- **Hō-Ren-Sō:** If a build takes >5 minutes, escalate for architectural review of the layers.

## Implementation Workflow

1. **Trigger:** Creation of a new service or optimization of an existing Dockerfile.
2. **Scaffold:** Use the standard multi-stage template.
3. **Optimize:** Add BuildKit cache mounts for the specific language/runtime.
4. **Secure:** Add non-root user and minimal base image.
5. **Verify:** Run `docker build --progress=plain` to verify cache hits.
