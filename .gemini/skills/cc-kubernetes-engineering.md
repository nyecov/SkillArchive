---
name: cc-kubernetes-engineering
version: 1.0.0
description: >
  Production-grade Kubernetes engineering standards. 
  Covers resource management, resilience (probes), security (PodSecurityContext), and manifest optimization.
category: engineering-standards
tags: [kubernetes, k8s, devops, orchestration, security, resilience, production]
references:
  - name: "Docker Engineering Standards"
    path: ../cc-docker-engineering/SKILL.md
  - name: "Ship: Production Readiness"
    path: ../cc-ship-production/SKILL.md
  - name: Lean Principles (Muda Eradication)
    path: ../lean-principles-muda/SKILL.md
---

# Kubernetes Engineering Standards

*A running Pod is not necessarily a healthy or secure Pod.*

This skill defines the standards for deploying applications to Kubernetes. It focuses on stability, resource efficiency, and security by ensuring manifests move beyond basic functionality to production-grade resilience.

## Core Mandates

### 1. Resource Discipline (Muda Reduction)
Every container MUST have explicit CPU and Memory `requests` and `limits`.

- **Action:** Set `requests` based on typical load and `limits` to prevent noisy-neighbor syndromes.
- **Constraint:** DO NOT leave resource blocks empty; this leads to unpredictable scheduling (waste).
- **Integration:** Directly implements **Seiri** (Sort) by allocating only what is necessary.

### 2. Resilience Gates (Jidoka)
Workloads MUST implement the three types of probes to allow the orchestrator to make informed decisions.

- **Action:** `livenessProbe` (is the process dead?), `readinessProbe` (is it ready for traffic?), and `startupProbe` (is it still initializing?).
- **Constraint:** DO NOT point probes at dependencies (e.g., checking the DB in an app probe); probes should only reflect the local container health.
- **Integration:** Supports **Jidoka** by allowing K8s to autonomously restart or isolate failing components.

### 3. Hardened Security Context (Poka-yoke)
Pods MUST run with the principle of least privilege.

- **Action:** Set `runAsNonRoot: true`, `allowPrivilegeEscalation: false`, and `readOnlyRootFilesystem: true` where possible.
- **Constraint:** Never run containers with `privileged: true` unless they are low-level system daemons.
- **Integration:** **Poka-yoke** for the runtime environment.

### 4. Configuration Decoupling
Application code and configuration MUST be separated using ConfigMaps and Secrets.

- **Action:** Use `envFrom` or volume mounts for configurations.
- **Constraint:** DO NOT bake environment-specific strings or secrets into the image layers.
- **Goal:** Single image for all environments (Dev -> Staging -> Prod).

### 5. Graceful Termination (Hō-Ren-Sō)
Applications MUST handle the `SIGTERM` signal to ensure zero-downtime deployments.

- **Action:** Implement a shutdown handler that closes database connections and finishes active requests.
- **Action:** Set `terminationGracePeriodSeconds` appropriately (default is 30s).
- **Goal:** Ensure the application "reports" its departure cleanly to the cluster.

## Implementation Patterns

### Standard Deployment Template
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-gateway
  labels:
    app: nomos-gateway
spec:
  replicas: 3
  template:
    spec:
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
      containers:
      - name: gateway
        image: nomos-gateway:v2.0.1
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        ports:
        - containerPort: 8008
        livenessProbe:
          httpGet:
            path: /health
            port: 8008
        readinessProbe:
          httpGet:
            path: /ready
            port: 8008
```

## Escalation & Halting

- **Jidoka:** Halt if a Deployment causes a `CrashLoopBackOff` that persists beyond 5 minutes.
- **Hō-Ren-Sō:** Report any resource "OOMKilled" events as an urgent need for resource re-allocation.

## Implementation Workflow

1. **Trigger:** Creation of a new K8s manifest or auditing of an existing deployment.
2. **Review:** Check for missing resource blocks and probes.
3. **Harden:** Apply `securityContext` and decouple configs into ConfigMaps.
4. **Verify:** Use `kubectl apply --dry-run=client` followed by `kube-linter` or similar validation tools.
