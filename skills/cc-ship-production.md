---
name: Ship (Production Readiness)
version: 1.0.0
description: >
  Use when code is "feature complete" and approaching deployment, or when verifying production readiness.
  Handles staging gates, 6-domain ship checklists, minimum viable production floor, and rollback planning.
category: engineering-standards
tags: [ship, production, deployment, monitoring, staging, crowd-control]
references:
  - name: Crowd Control (Source Repo)
    url: https://github.com/newsbubbles/crowd_control
  - name: CC — Deglaze (Anti-Sycophancy)
    path: ./cc-deglaze-anti-sycophancy.md
  - name: CC — Comprehend (Understanding Gate)
    path: ./cc-comprehend-understanding.md
  - name: CC — Anchor (Architectural Coherence)
    path: ./cc-anchor-coherence.md
  - name: CC — Circuit (Iteration Breaker)
    path: ./cc-circuit-iteration-breaker.md
  - name: CC — Isolate (Systematic Debugging)
    path: ./cc-isolate-debugging.md
  - name: CC — Secure (Security)
    path: ./cc-secure-security.md
  - name: Lean Principles (Muda Eradication)
    path: ./lean-principles-muda.md
  - name: Value Stream Mapping (VSM)
    path: ./vsm-value-stream-mapping.md
---

# Ship: Production Readiness

*The app isn't shipped until it's running reliably for users.*

Vibe coders think shipping means "code is done." It doesn't. Shipping means code is deployed, monitored, fixable, and rollback-able. This skill bridges the gap between a working localhost and a working production environment.

## Core Mandates

### 1. The Staging Gate
Before production, there MUST be staging — an environment that mirrors production but isn't user-facing.

```
Development → Staging → Production
     ↓            ↓           ↓
  Your laptop   Prod-like    Real users
  Test data     Test data    Real data
  Break freely  Test deploys Must work
```

**Rule:** If it hasn't run in staging, it doesn't ship.

### 2. The Ship Checklist

#### 🌐 Environment Configuration
| Check | Why It Matters |
|-------|---------------|
| Environment variables set | Secrets aren't in code |
| Different configs per environment | Dev ≠ staging ≠ prod |
| No hardcoded URLs | Can deploy anywhere |
| Build process works | Not running dev server in prod |

**The test:** Can someone else deploy this without asking you questions?

#### 🗄️ Database
| Check | Why It Matters |
|-------|---------------|
| Production database configured | Not using SQLite in prod |
| Connection pooling set up | Won't exhaust connections |
| Backups configured | Can recover from disasters |
| Migrations run cleanly | Schema changes don't break |

**The test:** What happens if your database disappears? How do you recover?

#### 🚨 Error Handling
| Check | Why It Matters |
|-------|---------------|
| Errors logged (not just console.log) | Can debug production issues |
| User-friendly error messages | Users don't see stack traces |
| Error monitoring set up | Know when things break |
| Graceful degradation | Partial failures don't crash everything |

**The test:** If something breaks at 3am, how do you find out? How do you diagnose?

#### 📈 Monitoring
| Check | Why It Matters |
|-------|---------------|
| Health check endpoint | Load balancers know if app is alive |
| Basic metrics (requests, errors, latency) | Know how app is performing |
| Alerting configured | Get notified of problems |
| Logs accessible | Can investigate issues |

**The test:** How do you know if your app is slow? How do you know if it's down?

#### 🔄 Deployment
| Check | Why It Matters |
|-------|---------------|
| Deployment automated | Not SSH-ing and running commands |
| Rollback plan exists | Can undo bad deploys |
| Zero-downtime deploys | Users don't see outages |
| Deployment tested | Know it works before production |

**The test:** How do you deploy? How do you rollback? Have you practiced both?

#### 🔒 Security (Production-Specific)
| Check | Why It Matters |
|-------|---------------|
| HTTPS enabled | Traffic is encrypted |
| Security headers set | Basic protections in place |
| Rate limiting configured | Can't be easily DDoS'd |
| CORS configured correctly | Only your frontend can call your API |

**The test:** Is your site HTTPS? What happens if someone hammers your API?

- **Integration:** The production security checks complement the **Secure** skill's development-time checklist. Between them, the full lifecycle is covered.

## The Minimum Viable Production

If nothing else, ensure these five:

1. **HTTPS** — Non-negotiable
2. **Environment variables** — No secrets in code
3. **Error logging** — Know when things break
4. **Health check** — Know if app is alive
5. **Rollback plan** — Know how to undo

Everything else can be added. These five are the floor.

## Common Ship Fails

- **"It Works Locally" Deploy** — Running dev server in production. Slow, insecure, crashes under load. **Fix:** Build for production. Use a proper process manager.
- **Missing Environment Variable** — Works locally because `.env` exists, undefined in production. **Fix:** Document all required env vars. Fail fast if missing.
- **"I'll Add Logging Later"** — `console.log` goes nowhere in production. **Fix:** Real logging from day one. Structured logs. Log aggregation.
- **No-Rollback Deploy** — "I'll fix it quickly." **Fix:** Know how to rollback. Practice it.

## Implementation Workflow

1. **Trigger:** Feature is "code complete" and approaching deployment.
2. **Staging Gate:** Deploy to staging first. Run through the checklist.
3. **Checklist:** Walk through all 6 domains. Every unchecked box must be addressed or explicitly accepted.
4. **Ship:** Deploy to production with the rollback plan ready.
5. **Monitor:** Verify health check, error rates, and performance post-deploy.

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
