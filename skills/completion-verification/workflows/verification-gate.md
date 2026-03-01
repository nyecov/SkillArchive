---
description: Mandatory "Iron Law" verification gate to be executed before any task completion claim. Ensures evidence precedes claims.
---

# Verification Gate Workflow

This workflow MUST be executed before claiming any task is "Done," "Fixed," or "Complete." It acts as a final Poka-yoke to prevent premature success claims.

## 1. Genchi Genbutsu (Go and See)
Identify the exact terminal command(s) that prove the success of your objective (e.g., `npm test`, `python manage_skills.py`, `ls -R`).

1. **Execute:** Run the command in the terminal.
2. **Read:** Completely read the output. Do not assume success based on exit code alone.

## 2. Shisa Kanko (Point and Call)
Point to the specific evidence of success in the terminal output.

1. **Quote:** Extract the specific pass marker (e.g., "15/15 tests passed", "Exit code: 0").
2. **Verify:** Check if any code was modified *after* this run. If yes, restart Step 1.

## 3. Evidence Log (Standardization)
Update the project's `verification_log.md` with a timecoded entry.

**Format:**
```markdown
### [YYYY-MM-DD HH:MM] - [Task Name]
- **Command:** [Exact command]
- **Evidence:** [Quote the success marker]
- **Status:** [VERIFIED / FAILED]
```

## 4. Final Claim
Only after Step 3 is complete can you notify the user of success. Your notification MUST include the quoted evidence from Step 2.
