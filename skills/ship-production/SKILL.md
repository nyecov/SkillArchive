---
name: ship-production
version: 1.0.0
description: >
  Use when code is "feature complete" and approaching deployment, or when verifying production readiness.
  Handles staging gates, 6-domain ship checklists, minimum viable production floor, and rollback planning.
category: engineering
tags: [ship, production, deployment, monitoring, staging, crowd-control]
references:
  - name: Crowd Control (Source Repo)
    url: https://github.com/newsbubbles/crowd_control
  - name: CC — Deglaze (Anti-Sycophancy)
    path: ../deglaze-tactics/SKILL.md
  - name: CC — Comprehend (Understanding Gate)
    path: ../comprehend-understanding/SKILL.md
  - name: CC — Anchor (Architectural Coherence)
    path: ../anchor-coherence/SKILL.md
  - name: CC — Circuit (Iteration Breaker)
    path: ../circuit-breaker/SKILL.md
  - name: CC — Isolate (Systematic Debugging)
    path: ../isolate-debugging/SKILL.md
  - name: CC — Secure (Security)
    path: ../secure-security/SKILL.md
  - name: Lean Principles (Muda Eradication)
    path: ../muda/SKILL.md
  - name: Value Stream Mapping (VSM)
    path: ../vsm/SKILL.md
---

# Ship: Production Readiness

*The app isn't shipped until it's running reliably for users.*

Vibe coders think shipping means "code is done." It doesn't. Shipping means code is deployed, monitored, fixable, and rollback-able. This skill bridges the gap between a working localhost and a working production environment.

## Core Mandates

### 1. The Staging Gate
Every deployment MUST pass through a staging environment that mirrors production before reaching real users.
- **Action:** Deploy to staging, run the full test suite, and perform manual smoke tests.
- **Constraint:** NEVER skip staging for a "quick fix." If it hasn't run in staging, it doesn't ship.
- **Integration:** Acts as a final **Poka-yoke** before production exposure.

### 2. Readiness Verification (The 6-Domain Audit)
Verify production readiness across Environment, Database, Errors, Monitoring, Deployment, and Security.
- **Action:** Complete the Ship Checklist and identify any "Minimum Viable Production" (MVP) gaps.
- **Constraint:** No deployment is permitted without a documented and tested **Rollback Plan**.
- **Integration:** Uses **VSM** to ensure the deployment pipeline is free of **Muda (Waste)** and bottlenecks.

### 3. Post-Ship Monitoring
Active verification of system health immediately following a production deployment.
- **Action:** Verify the Health Check endpoint, error rates, and key performance metrics.
- **Constraint:** If the health check fails or error rates spike, trigger an immediate rollback.
- **Integration:** Feeds into **Hansei** to reflect on the success and quality of the deployment.

## Escalation & Halting

- **Jidoka:** If a staging deploy fails or a production health check is red, trigger an immediate Jidoka halt and/or rollback.
- **Hō-Ren-Sō:** Use Sōdan (Consult) if a production issue requires a strategic decision (e.g., "Partial rollback vs. Hotfix").

## Implementation Workflow

1. **Trigger:** A feature is "code complete" and ready for deployment.
2. **Execute:** Deploy to Staging and complete the 6-Domain readiness audit.
3. **Verify:** Confirm staging stability and post-production health check.
4. **Output:** A successful deployment, a stable production environment, and an updated rollback strategy.

## Quick Reference

```
SHIP CHECKLIST:
□ Environment variables configured (not hardcoded)?
□ Production database set up with backups?
□ Error logging and monitoring in place?
□ Health check endpoint exists?
□ Deployment process documented?
□ Rollback plan tested?
□ HTTPS enabled?
□ Rate limiting configured?

MINIMUM VIABLE PRODUCTION:
1. HTTPS
2. Environment variables
3. Error logging
4. Health check
5. Rollback plan

THE STAGING GATE:
Dev → Staging → Production
Never skip staging.
If it hasn't run in staging, it doesn't ship.
```
