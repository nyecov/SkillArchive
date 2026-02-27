---
name: docker-engineering
version: 1.2.0
level: tactical
description: 'Procedure for auditing and optimizing Docker containers. Focuses on
  minimizing build Muda, image size, and attack surface using multi-stage builds and
  BuildKit.

  '
category: engineering
tags:
- docker
- engineering
- optimization
- security
references:
- name: Ship Production
  path: ../ship-production/SKILL.md
- name: Muda (Waste Eradication)
  path: ../muda/SKILL.md
---

# Docker Optimization Procedure

This procedure transforms a "working" Dockerfile into a production-grade artifact by eliminating build-time waste.

## Core Mandates

### 1. Multi-Stage Audit
Audit the Dockerfile for "Inventory Muda" (build tools, source code, or secrets left in the final image).
- **Action:** Refactor into a multi-stage build where the final stage uses `alpine` or `distroless`.
- **Constraint:** The final image MUST contain only the binary/runtime and its direct dependencies.

### 2. Layer Caching (Mura Prevention)
Order commands to maximize cache reuse and minimize "Waiting Muda."
- **Action:** Copy dependency manifests (`package.json`, `go.mod`) BEFORE source code. Use BuildKit `--mount=type=cache`.
- **Integration:** Directly reduces build latency in the **VSM (Value Stream Mapping)**.

## Implementation Workflow

1. **Trigger:** Creation or optimization of a Dockerfile.
2. **Scan:** Identify large layers, root users, and unnecessary build tools.
3. **Refactor:** Apply multi-stage layering and BuildKit cache mounts.
4. **Verify:** Run `docker build --progress=plain` and verify cache hits and final image size.
