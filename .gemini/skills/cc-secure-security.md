---
name: cc-secure-security
version: 1.0.0
description: >
  Use when implementing authentication, handling user input, storing secrets, or exposing API endpoints.
  Handles trust boundary analysis, 5-domain security checklists (secrets, auth, authorization, input, data exposure), and common vulnerability patterns.
category: agent-safety
tags: [secure, security, trust-boundary, secrets, authentication, authorization, crowd-control]
references:
  - name: Crowd Control (Source Repo)
    url: https://github.com/newsbubbles/crowd_control
  - name: CC — Deglaze (Anti-Sycophancy)
    path: ../cc-deglaze-anti-sycophancy/SKILL.md
  - name: CC — Comprehend (Understanding Gate)
    path: ../cc-comprehend-understanding/SKILL.md
  - name: CC — Anchor (Architectural Coherence)
    path: ../cc-anchor-coherence/SKILL.md
  - name: CC — Circuit (Iteration Breaker)
    path: ../cc-circuit-iteration-breaker/SKILL.md
  - name: CC — Isolate (Systematic Debugging)
    path: ../cc-isolate-debugging/SKILL.md
  - name: CC — Ship (Production Readiness)
    path: ../cc-ship-production/SKILL.md
  - name: KYT (Hazard Prediction)
    path: ../kyt-hazard-prediction/SKILL.md
  - name: Poka-yoke (Mistake-proofing)
    path: ../poka-yoke-mistake-proofing/SKILL.md
---

# Secure: Security for the Uninitiated

*You are the paranoid friend they need.*

Assume users will try to break things, the frontend will be bypassed, secrets will leak if exposed, and permissions will be tested. Security isn't about perfect defense — it's about **not making it easy**.

## Core Mandates

### 1. The Three Questions
Before any feature ships, ask:

1. **What can a user see?** (Data exposure)
2. **What can a user do?** (Authorization)
3. **What can a user send?** (Input validation)

If you can't answer these confidently, you have security gaps.

- **Integration:** These map directly to **KYT (Hazard Prediction)** Round 1 — each unanswered question is an identified hazard.

### 2. The Trust Boundary

```
┌─────────────────────────────────────────┐
│              UNTRUSTED                  │
│  - Browser                              │
│  - User input                           │
│  - URL parameters                       │
│  - Cookies (can be manipulated)         │
│  - localStorage (can be read by script) │
└─────────────────────────────────────────┘
                    │
            TRUST BOUNDARY
                    │
┌─────────────────────────────────────────┐
│              TRUSTED                    │
│  - Server-side code                     │
│  - Database                             │
│  - Environment variables                │
│  - Server-only secrets                  │
└─────────────────────────────────────────┘
```

**Rule:** Never trust anything from above the line. Always validate on the server.

## The Security Checklist

### 🔑 Secrets
| ✗ Wrong | ✓ Right |
|---------|--------|
| API keys in frontend code | API keys in server environment variables |
| Secrets in git repo | Secrets in .env (gitignored) or secret manager |
| Hardcoded passwords | Environment-specific credentials |
| Same keys for dev/prod | Separate keys per environment |

**The test:** Search your codebase for your API key. If you find it in frontend code, it's exposed.

### 🔐 Authentication
| ✗ Wrong | ✓ Right |
|---------|--------|
| Tokens in localStorage | Tokens in httpOnly cookies |
| Auth state in React only | Auth verified on every server request |
| "Remember me" forever | Token expiration + refresh flow |
| Password in URL params | Password in POST body only |

**The test:** Open DevTools → Application → Local Storage. If you see auth tokens, they're stealable.

### 🛡️ Authorization
| ✗ Wrong | ✓ Right |
|---------|--------|
| Hide admin button in UI | Check permissions on server |
| `if (user.role === 'admin')` in frontend | Permission check in API handler |
| Trust user ID from request | Verify user ID from session |
| Check once at login | Check on every protected action |

**The test:** Can you access /admin by typing the URL directly? If yes, your auth is UI-only.

### 📝 Input Validation
| ✗ Wrong | ✓ Right |
|---------|--------|
| Trust user input | Validate and sanitize everything |
| Build SQL with string concat | Use parameterized queries |
| Render user content as HTML | Escape or use safe rendering |
| Accept any file upload | Validate file type, size, content |

**The test:** What happens if someone submits `<script>alert('xss')</script>` in a form field?

- **Integration:** Input validation is a **Poka-yoke** interlock — make invalid input physically impossible to process.

### 📡 Data Exposure
| ✗ Wrong | ✓ Right |
|---------|--------|
| Return full user object | Return only needed fields |
| Log sensitive data | Redact passwords, tokens, PII |
| Error messages show stack traces | Generic errors to client, detailed logs server-side |
| All data to all users | Filter data by user permissions |

**The test:** Check your API responses. Are you sending passwords, tokens, or internal IDs?

## Common Vibe Coding Security Fails

### The Stripe Key Incident
Secret key (`sk_live_`) in production frontend code → anyone could issue refunds and access customer data. **Fix:** Secret key on server only; only publishable key (`pk_`) goes to frontend.

### The Admin URL Incident
Frontend hides the admin link, but no server-side route protection → anyone who guesses /admin gets in. **Fix:** Every admin endpoint checks permissions server-side.

### The User ID Incident
API endpoint accepts user ID from URL without verifying the requester → change the ID, get anyone's data. **Fix:** Verify `req.params.id` matches authenticated user (or user has admin rights).

## Escalation & Halting

- **Jidoka:** Trigger an autonomous halt if a trust boundary violation is detected or if secrets are found exposed in the frontend codebase.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol if the "Three Questions" reveal unmitigable data exposure risks or if authorization logic is ambiguous.

## Implementation Workflow

1. **Trigger:** Any feature that touches auth, data, or user input.
2. **Three Questions:** Run the three questions against the feature.
3. **Checklist:** Walk through the 5-domain security checklist.
4. **Escalate:** Any unchecked box is a **KYT** hazard — establish a **Poka-yoke** countermeasure before shipping.

## Quick Reference

```
SECURITY CHECKLIST:
□ Secrets in environment variables (not code)?
□ Auth tokens in httpOnly cookies (not localStorage)?
□ Permissions checked on SERVER (not just UI)?
□ User input validated and sanitized?
□ API responses filtered to necessary data?
□ Errors don't expose internal details?

THE TRUST BOUNDARY:
Everything from the browser is UNTRUSTED.
Validate EVERYTHING on the server.
```
