---
name: verification-before-completion
version: 1.0.0
level: methodology
description: 'Use when about to claim work is complete, fixed, or passing, before committing or creating PRs. Requires running verification commands and confirming output before making any success claims.'
category: engineering
tags: [safety, engineering, debugging]
references:
  - name: Shisa Kanko (Master Workflow)
    path: ../shisa-kanko/SKILL.md
  - name: Poka-yoke (Mistake-proofing)
    path: ../poka-yoke/SKILL.md
---

# Verification Before Completion

Claiming work is complete without verification is dishonesty, not efficiency. This skill enforces the Iron Law: "Evidence before claims, always." It acts as a strict behavioral gate to prevent rationalization and ensure that success claims are rooted in empirical evidence.

## Core Mandates

### 1. The Iron Law of Verification
- **Action:** BEFORE claiming any status, expressing satisfaction, or moving to the next task, you must identify the command that proves the claim, run it completely, and read the full output.
- **Constraint:** NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE. Do not rely on "it should work", partial linters, or previous runs.
- **Integration:** Directly integrates with **Shisa Kanko** (Point and Call) — you must point to the test results and call out the exact pass/fail state before proceeding.

### 2. Rationalization Prevention
- **Action:** Stop and recognize red flags: "should work now", "just this once", "the linter passed so the build will".
- **Constraint:** Do not substitute confidence or exhaustion for empirical evidence. If tests fail, do not claim the feature is "mostly done".
- **Integration:** Functions as a **Poka-yoke** mechanism preventing the premature closing of a development loop.

## Escalation & Halting

- **Jidoka:** If verification fails, immediately halt and output the actual state with evidence. Do not proceed to commit, PR, or subsequent tasks.
- **Hō-Ren-Sō:** Report the failure factual state to the user. E.g., "Tests failing (3 failures). Must fix before completing: [Show failures]."

## Implementation Workflow

1. **Trigger:** Approaching the end of a task, about to say "Done", or preparing to commit/PR.
2. **Execute:** Identify the exact command needed (e.g., `npm test`, `cargo build`). Run it.
3. **Verify:** Read the full output, check the exit code, and count failures.
4. **Output:** Only state success IF and ONLY IF the command explicitly proves it. Otherwise, state the failure state.
