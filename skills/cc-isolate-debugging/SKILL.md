---
name: Isolate (Systematic Debugging)
version: 1.0.0
description: >
  Use when a bug is reported, unexpected behavior occurs, or a fix attempt has failed.
  Handles 5-step hypothesis-driven debugging, binary search isolation, minimal reproduction, and single-variable testing.
category: engineering-standards
tags: [isolate, debugging, systematic, hypothesis, single-variable, crowd-control]
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
  - name: CC — Secure (Security)
    path: ../cc-secure-security/SKILL.md
  - name: CC — Ship (Production Readiness)
    path: ../cc-ship-production/SKILL.md
  - name: Poka-yoke (Mistake-proofing)
    path: ../poka-yoke-mistake-proofing/SKILL.md
  - name: KYT (Hazard Prediction)
    path: ../kyt-hazard-prediction/SKILL.md
---

# Isolate: Systematic Debugging

*You are a scientist, not a gambler.*

Gamblers try random things hoping something works. Scientists form hypotheses, test them, and learn from results. Debugging is not about luck — it's about systematically eliminating possibilities until only the truth remains.

## Core Mandates: The 5-Step Protocol

### Step 1: Define The Symptom
Before anything else, **precisely define what's broken**.

```
BAD:  "The app is broken"
BAD:  "Auth doesn't work"
GOOD: "When I click login with valid credentials, I get redirected
       to /dashboard but the user object is null"
```

**The test:** Can you reproduce it? If you can't reproduce it, you can't debug it.

### Step 2: Locate The Boundary
Find where things go from **working** to **broken**.

```
✓ User clicks login button          (working - button responds)
✓ Form submits to /api/auth/login   (working - network request fires)
✓ Server receives request           (working - logs show request)
✓ Server validates credentials      (working - returns 200)
✓ Server returns user object        (working - response has data)
✗ Client receives response          (BROKEN - response is empty??)
```

The bug is between "server returns" and "client receives." Now we know where to look.

### Step 3: Form A Hypothesis
**One hypothesis at a time.** Not "maybe it's A or B or C." Pick one.

```
HYPOTHESIS: The response is being transformed incorrectly
            by the API client middleware.

TEST: Log the raw response before middleware processing.

EXPECTED: Raw response will have user data.
```

### Step 4: Test The Hypothesis
**Change only what's necessary to test.** Don't fix while testing.

The moment you "fix while testing," you've lost the ability to verify.

### Step 5: Interpret Results

| Result | Meaning |
|--------|--------|
| Hypothesis confirmed | Proceed to fix |
| Hypothesis rejected | Form new hypothesis |
| Inconclusive | Need better test |

**Never** conclude without evidence. "I think it's fixed" is not evidence. "The test passes" is evidence.

## The Single Variable Rule

Change ONE thing. Test. Then change the next thing. Never change multiple things simultaneously.

- **Integration:** This is the debugging analogue of **Poka-yoke** deterministic validation — one check, one result, no ambiguity.

## The Isolation Toolkit

### Binary Search Debugging
When you don't know where the bug is:
1. Find the midpoint of the code path.
2. Add a log/breakpoint there.
3. Is the data correct at midpoint? Yes → bug is after. No → bug is before.
4. Repeat until isolated.

### The Minimal Reproduction
Strip away everything that isn't necessary to reproduce the bug. The smaller the reproduction, the clearer the bug.

### The Reversion Test
"When did this last work?" → Revert to that state → Confirm it works → Apply changes one at a time until it breaks → The breaking change contains the bug.

## Anti-Patterns to Catch

- **"Let Me Just Try This"** — No. Form a hypothesis first. What do you expect to happen? Why?
- **"I'll Change A Few Things"** — No. One thing. Test. Then the next thing.
- **"The AI Said To Do This"** — The AI is guessing too. It doesn't know more than you do about YOUR bug.
- **"It Works Now" (Without Understanding Why)** — Then you haven't fixed it. You've hidden it. It will return.

## Implementation Workflow

1. **Trigger:** Bug reported or unexpected behavior observed.
2. **Define:** Precisely state the symptom (Step 1).
3. **Locate:** Find the working→broken boundary (Step 2).
4. **Hypothesize:** Form a single hypothesis (Step 3).
5. **Test:** One change, one observation (Step 4).
6. **Interpret:** Evidence-based conclusion (Step 5).
7. **Escalate:** If 3+ hypotheses fail, trigger **Circuit** protocol — the approach may be wrong.

## Quick Reference

```
ISOLATE PROTOCOL:
1. DEFINE symptom precisely
2. LOCATE boundary (working → broken)
3. HYPOTHESIZE one cause
4. TEST with minimal change
5. INTERPRET with evidence

SINGLE VARIABLE RULE:
- Change ONE thing
- Test
- Then change the next thing
- Never change multiple things

QUESTIONS BEFORE FIXING:
□ Can you reproduce it?
□ Where is the boundary?
□ What's your hypothesis?
□ How will you test it?
□ What evidence will confirm/reject?
```
