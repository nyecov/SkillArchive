---
name: kubernetes-engineering
version: 1.1.0
level: tactical
description: 'Procedure for auditing and hardening Kubernetes manifests. Ensures resource
  discipline (Muda reduction), resilience gates (Jidoka), and security interlocks.

  '
category: engineering
tags:
- engineering
- kubernetes
- security
references:
- name: Docker Engineering
  path: ../docker-engineering/SKILL.md
- name: Ship Production
  path: ../ship-production/SKILL.md
---

# Kubernetes Hardening Procedure

This procedure ensures that Pods move beyond "running" to "resilient and secure" through mandatory interlocks.

## Core Mandates

### 1. Resource & Probe Audit
Audit manifests for missing resource limits and health probes.
- **Action:** Add explicit CPU/Memory `requests`/`limits` and Liveness/Readiness probes to every container.
- **Constraint:** Allocation without measurement is **Muda** (Waste). NEVER skip resource blocks.

### 2. Security Context Enforcement
Audit Pods for privilege escalation risks.
- **Action:** Apply `securityContext` with `runAsNonRoot: true` and `readOnlyRootFilesystem: true`.
- **Integration:** Acts as a runtime **Poka-yoke** to prevent privilege escalation.

## Escalation & Halting

- **Jidoka:** Halt if a Deployment causes a `CrashLoopBackOff` that persists beyond 5 minutes or if a Pod is `OOMKilled`.
- **Hō-Ren-Sō:** Use the Renraku (Fact) protocol to report persistent scheduling failures or resource exhaustion to the user.

## Implementation Workflow

1. **Trigger:** Creation or auditing of a Kubernetes manifest.
2. **Audit:** Check for Resource Limits, Probes, and SecurityContext.
3. **Apply:** Inject missing production-grade blocks.
4. **Verify:** Confirm manifest validity with `kubectl apply --dry-run=client`.
