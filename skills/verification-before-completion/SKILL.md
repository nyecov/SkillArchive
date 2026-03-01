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

### 1. The Iron Law of Verification (Final Action Gate)
The VERY LAST tool call before any completion claim, success report, or "Done" status MUST be a terminal verification command (`run_command` or `command_status`).

- **Constraint:** ANY file modification made after a verification run immediately invalidates all previous evidence. You MUST re-verify.
- **Integration:** Directly integrates with **Shisa Kanko** (Point and Call) — you must quote the exact terminal success marker (e.g., "Exit code: 0").

### 2. The Evidence Log (Standardization)
Every major task MUST maintain a timecoded `verification_log.md` within the project root (or a designated logs directory).
- **Action:** Standardize the audit trail by logging every final verification run with a timestamp, the command executed, and the quoted evidence.
- **Constraint:** Do not rely on ephemeral console history. The log is the persistent proof of work.
- **Integration:** Functions as a **Poka-yoke** mechanism preventing "Stale Evidence" errors.

## Escalation & Halting

- **Jidoka:** If verification fails, immediately halt and output the actual state with evidence. Do not proceed to commit, PR, or subsequent tasks.
- **Hō-Ren-Sō:** Report the failure factual state to the user. E.g., "Tests failing (3 failures). Must fix before completing: [Show failures]."

## Implementation Workflow

1. **Trigger:** Approaching the end of a task, about to say "Done", or preparing to commit/PR.
2. **Execute:** Identify the exact command needed (e.g., `npm test`, `cargo build`). Run it.
3. **Verify:** Read the full output, check the exit code, and count failures.
4. **Output:** Only state success IF and ONLY IF the command explicitly proves it. Otherwise, state the failure state.
