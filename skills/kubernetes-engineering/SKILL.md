---
name: kubernetes-engineering
version: 1.0.0
description: >
  Production-grade Kubernetes engineering standards. 
  Covers resource management, resilience (probes), security (PodSecurityContext), and manifest optimization.
category: engineering
tags: [kubernetes, k8s, devops, orchestration, security, resilience, production]
references:
  - name: "Docker Engineering Standards"
    path: ../docker-engineering/SKILL.md
  - name: "Ship: Production Readiness"
    path: ../ship-production/SKILL.md
  - name: Lean Principles (Muda Eradication)
    path: ../muda/SKILL.md
---

# Kubernetes Engineering Standards

*A running Pod is not necessarily a healthy or secure Pod.*

This skill defines the standards for deploying applications to Kubernetes. It focuses on stability, resource efficiency, and security by ensuring manifests move beyond basic functionality to production-grade resilience.

## Core Mandates

### 1. Resource Discipline (Muda Reduction)
Every container MUST have explicit CPU and Memory `requests` and `limits` to prevent unpredictable scheduling.
- **Action:** Set `requests` based on typical load and `limits` to prevent noisy-neighbor syndromes.
- **Constraint:** DO NOT leave resource blocks empty. Allocation without measurement is **Muda** (Waste).
- **Integration:** Implements **Seiri** (Sort) by allocating only what is necessary.

### 2. Resilience Gates (Jidoka)
Workloads MUST implement liveness, readiness, and startup probes to enable autonomous orchestration decisions.
- **Action:** Configure `livenessProbe`, `readinessProbe`, and `startupProbe` for every container.
- **Constraint:** DO NOT point probes at external dependencies (e.g., a DB); probes must reflect local health only.
- **Integration:** Supports **Jidoka** by allowing the cluster to autonomously restart or isolate failing Pods.

### 3. Hardened Security Context (Poka-yoke)
Pods MUST operate with the principle of least privilege using PodSecurityContext.
- **Action:** Enforce `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, and `readOnlyRootFilesystem: true`.
- **Constraint:** NEVER run containers as `privileged: true` unless they are system-level daemons.
- **Integration:** Acts as a runtime **Poka-yoke** to prevent privilege escalation.

## Escalation & Halting

- **Jidoka:** Halt if a Deployment causes a `CrashLoopBackOff` that persists beyond 5 minutes or if a Pod is `OOMKilled`.
- **Hō-Ren-Sō:** Use the Renraku (Fact) protocol to report persistent scheduling failures or resource exhaustion to the user.

## Implementation Workflow

1. **Trigger:** Creation of a new K8s manifest or auditing of an existing deployment.
2. **Review:** Check for missing resource blocks and probes.
3. **Harden:** Apply `securityContext` and decouple configs into ConfigMaps.
4. **Verify:** Use `kubectl apply --dry-run=client` followed by `kube-linter` or similar validation tools.
