# Incident Report: Catastrophic Directory Deletion via `shutil.rmtree` on Windows Junctions

## Date
March 26, 2026

## Problem
During a refactor of the `tools/sync_skills.py` script, an attempt to replace `cmd /c rmdir` with Python's native `shutil.rmtree()` resulted in the catastrophic deletion of nearly all `SKILL.md` files in the source `skills/` directory when the sync script was executed.

## Symptoms
- After running the modified `sync_skills.py` script, the source `skills/` directory was emptied of almost all its contents.
- Git status showed hundreds of `deleted` files across the repository.
- A subsequent `git checkout` command failed with "Invalid argument" because the junction points were corrupted or in a locked state.
- Attempting to read `skills/jidoka/SKILL.md` resulted in an `ELOOP: too many symbolic links encountered` error.

## Root Cause
The `sync_skills.py` script uses OS-native directory junctions (`mklink /J`) on Windows to link the source `skills/` directory into the hidden `.gemini/skills/` runtime directory. 
When cleaning up the `.gemini/skills/` directory, the AI agent confidently (but incorrectly) assumed that Python's `shutil.rmtree()` handles directory junctions safely without following them. 
However, on Windows, calling `shutil.rmtree()` on a directory junction causes Python to traverse the junction and aggressively delete all the original files located in the *source* directory, rather than just unlinking the junction point itself. The original code (`cmd /c rmdir`) was actually a necessary, platform-specific Poka-yoke (mistake-proofing) technique, as `rmdir` correctly removes the junction without touching the source files.

## Resolution
1. **Immediate Halt:** The Andon Cord (Jidoka) was pulled, and the active Git merge was aborted.
2. **Hard Reset:** Executed `git reset --hard HEAD` to reset the repository state.
3. **Junction Cleanup:** Used PowerShell to force-remove the corrupted hidden `.gemini/skills` folder (`Remove-Item -Path "G:\Skill Archive\.gemini\skills" -Force -Recurse`), breaking the corrupted junction links that were blocking Git.
4. **Source Restoration:** Executed `git restore .` to fully restore the missing `skills/` source files from the last known good commit.
5. **Reverted Code:** The proposed Python refactor was abandoned, leaving the original, safe `cmd /c rmdir` logic in place for Windows junction cleanup.

## Outcome
The repository's source files were 100% recovered with no data loss. The `sync_skills.py` script remains reliant on `cmd /c rmdir` as a proven, safe method for managing Windows junctions.
