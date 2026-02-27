---
name: secure-security
version: 1.0.0
level: tactical
description: Use when handling auth, user input, secrets, or API endpoints. Mandates
  trust-boundary audits.
category: safety
tags:
- security
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
  path: ../jidoka/SKILL.md
- name: CC — Isolate (Systematic Debugging)
  path: ../isolate-debugging/SKILL.md
- name: CC — Ship (Production Readiness)
  path: ../ship-production/SKILL.md
- name: KYT (Hazard Prediction)
  path: ../kyt/SKILL.md
- name: Poka-yoke (Mistake-proofing)
  path: ../poka-yoke/SKILL.md
requires:
- red-teaming-tactics
---

# Secure: Security for the Uninitiated

*You are the paranoid friend they need.*

Assume users will try to break things, the frontend will be bypassed, secrets will leak if exposed, and permissions will be tested. Security isn't about perfect defense — it's about **not making it easy**.

## Core Mandates

### 1. Trust Boundary Enforcement
Assume everything from the browser (input, params, cookies) is UNTRUSTED and validate it on the server.
- **Action:** Perform server-side validation for every request, regardless of client-side checks.
- **Constraint:** NEVER trust client-provided IDs or roles without verification against the authenticated session.
- **Integration:** Directly implements the **Poka-yoke** principle of "Contact Checks."

### 2. Secret Isolation
Ensure all sensitive credentials (API keys, passwords) are stored in environment variables and never exposed to the frontend.
- **Action:** Use `.env` files (gitignored) or secret managers for all non-public keys.
- **Constraint:** DO NOT commit secrets to the repository or include server-only keys in frontend bundles.
- **Integration:** This is a security **Poka-yoke** — make it impossible to leak secrets via the browser.

### 3. Defensive Data Exposure
Minimize the risk of data leakage by filtering API responses and genericizing error messages.
- **Action:** Return only the minimum required fields to the client and redact sensitive data from logs.
- **Constraint:** NEVER show stack traces or internal system details in user-facing error messages.
- **Integration:** Uses **Lean Foundations** to eliminate "Over-generation" of sensitive data.

## Escalation & Halting

- **Jidoka:** If a trust boundary violation is detected or secrets are found exposed in the frontend, trigger an immediate Jidoka halt.
- **Hō-Ren-Sō:** Use the Sōdan (Consult) protocol if authorization logic is ambiguous or if the "Three Questions" reveal high data-exposure risks.

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
