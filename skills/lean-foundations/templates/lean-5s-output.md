# Lean Foundations: 5S Validation Report

When an agent executes the `lean-foundations` workflow to stabilize and clean a workspace, it MUST output its final state using this exact Markdown schema.

```markdown
# 5S Stabilization Report

## 1. Context
- **Trigger Condition:** [e.g., Start of new task, Context window bloating, End of session]

## 2. 5S Execution Log
- [x] **Seiri (Sort):** Removed unnecessary data/files.
- [x] **Seiton (Set in Order):** Verified file structures and paths match conventions.
- [x] **Seiso (Shine):** Cleaned dead code and outdated comments.
- [x] **Seiketsu (Standardize):** Enforced template and naming rules.
- [x] **Shitsuke (Sustain):** System ready for high-signal engineering.

## 3. Poka-yoke Verification
- [x] No files outside the temporary directory (e.g., `.gemini/tmp/`) were deleted without verified redundancy or explicit user permission.
```
