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

### 1. BuildKit Optimization (Speed Gate)
Utilize Docker BuildKit features to eliminate redundant work and achieve sub-30 second rebuilds.
- **Action:** Use `RUN --mount=type=cache` for package managers and `RUN --mount=type=bind` for temporary files.
- **Constraint:** DO NOT rely on simple layer caching for large dependency installations; it is too brittle.
- **Integration:** Directly reduces "Waiting" waste in the **VSM (Value Stream Mapping)**.

### 2. Manifest-First Layering
Prioritize layer stability by decoupling manifests from source code and using multi-stage builds.
- **Action:** Copy dependency manifests BEFORE source code and use minimal final stages (alpine, distroless).
- **Constraint:** The final image MUST NOT contain build-time secrets, git, or compilers.
- **Integration:** Acts as a structural **Poka-yoke** to prevent secret leakage and bloated artifacts.

### 3. Security & Signal Handling
Ensure images are secure by default and exit cleanly without zombie processes.
- **Action:** Use specific version tags, run as a non-root `USER`, and use the **Exec Form** for `ENTRYPOINT`.
- **Constraint:** NEVER run processes as `root` or use the "Shell Form" for `CMD` which blocks signal forwarding.
- **Integration:** Provides the "Point of Origin" for **Jidoka** signals in orchestrated environments.

## Escalation & Halting

- **Jidoka:** Halt if `secrets.env` or sensitive files are detected in the build context or if a `HEALTHCHECK` fails during staging.
- **Hō-Ren-Sō:** Use the Renraku (Fact) protocol to escalate if a build takes >5 minutes or if image size exceeds project thresholds.

## Implementation Workflow

1. **Trigger:** Creation of a new service or optimization of an existing Dockerfile.
2. **Scaffold:** Use the standard multi-stage template.
3. **Optimize:** Add BuildKit cache mounts for the specific language/runtime.
4. **Secure:** Add non-root user and minimal base image.
5. **Verify:** Run `docker build --progress=plain` to verify cache hits.
