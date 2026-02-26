# Importing Skills from the Skill Archive

This document explains how external projects and AI agents can consume skills from the Skill Archive. There are two import modes:

| Mode | Mechanism | Updates | Ownership |
|------|-----------|---------|-----------|
| **Copy** | File copy into your project | Manual — you decide when to re-sync | Full — you can modify the skill |
| **Live Link** | Git submodule / symlink to the archive | Automatic — reflects the latest archive state | Read-only — changes happen upstream |

Choose **Copy** when you need local control, customization, or offline access.
Choose **Live Link** when you want skills to stay current without manual maintenance.

---

## Import Mode 1: Copy (Snapshot)

Copies skill files into your project's own skill directory. The imported files are independent — they do not update when the archive changes.

### When to Use

- You need to **modify** the skill for project-specific conventions.
- You want a **stable snapshot** that won't change unexpectedly.
- Your project runs in an environment **without network access** to the archive repo.
- You need to **vendor** skills for reproducibility.

### How to Import (Manual)

1. **Identify the target directory** in your consuming project. This depends on your AI agent platform:

   | Platform | Default Skill Directory |
   |----------|----------------------|
   | Claude Code | `.claude/skills/` |
   | Gemini CLI | `.gemini/skills/` |
   | OpenAI Codex | `.agents/skills/` |
   | Cursor | `.cursor/skills/` |
   | Generic | `skills/` or `.agent/skills/` |

2. **Copy the desired skill files** from the archive into your project:

   ```bash
   # Copy a single skill
   cp /path/to/skill-archive/skills/jidoka-autonomation.md .claude/skills/

   # Copy all skills
   cp /path/to/skill-archive/skills/*.md .claude/skills/

   # Windows (PowerShell)
   Copy-Item "G:\Skill Archive\skills\jidoka-autonomation.md" ".\.claude\skills\"

   # Copy all skills (Windows)
   Copy-Item "G:\Skill Archive\skills\*.md" ".\.claude\skills\"
   ```

3. **Update internal references** if needed. Skills cross-reference each other via relative paths (e.g., `./jidoka-autonomation.md`). If you only import a subset, either:
   - Import all referenced skills to keep the mesh intact, or
   - Remove `references:` entries that point to skills you didn't import.

4. **Commit the copied files** into your project's version control.

### How to Import (Script)

For repeatable copy imports, use the provided sync script:

```bash
# Sync all skills to your project (one-time snapshot)
node skill-archive/scripts/sync.js --mode copy --target .claude/skills/

# Sync specific skills only
node skill-archive/scripts/sync.js --mode copy --target .claude/skills/ \
  --skills jidoka-autonomation,poka-yoke-mistake-proofing,shisa-kanko-vibecoding
```

### Re-Syncing a Copy

To manually update a previously copied skill to the latest archive version:

```bash
# Re-copy from archive (overwrites local changes)
cp /path/to/skill-archive/skills/jidoka-autonomation.md .claude/skills/
```

> [!WARNING]
> Re-copying will **overwrite** any local modifications you made to the skill. If you customized the skill, diff before overwriting:
> ```bash
> diff .claude/skills/jidoka-autonomation.md /path/to/skill-archive/skills/jidoka-autonomation.md
> ```

---

## Import Mode 2: Live Link (Auto-Updating)

Creates a **read-only** reference to the Skill Archive that automatically reflects the latest state of the archive repository. You never edit these files directly — all changes happen upstream in the Skill Archive.

### When to Use

- You want skills to **stay current** without manual maintenance.
- You trust the archive maintainer to evolve skills responsibly.
- You want a **single source of truth** shared across multiple projects.
- Your team uses the **same skill standards** across all repositories.

### Method A: Git Submodule (Recommended for Git-Based Projects)

Git submodules create a tracked reference to another repository at a specific commit. Combined with a periodic update schedule, this provides live-link semantics.

#### Initial Setup

```bash
# Add the Skill Archive as a submodule in your project
git submodule add <skill-archive-repo-url> .skills/archive

# This creates:
#   .skills/archive/          ← read-only mirror of the Skill Archive
#   .skills/archive/skills/   ← all skill files
#   .gitmodules               ← submodule configuration
```

Then symlink (or configure your agent) to read from the submodule:

```bash
# Option 1: Symlink into your agent's skill directory
# Linux/macOS
ln -s ../../.skills/archive/skills/*.md .claude/skills/

# Windows (PowerShell, requires admin or Developer Mode)
New-Item -ItemType SymbolicLink -Path ".claude\skills\jidoka-autonomation.md" `
  -Target ".skills\archive\skills\jidoka-autonomation.md"
```

```bash
# Option 2: Configure your agent to read directly from the submodule path
# (Platform-dependent — check your agent's skill directory configuration)
```

#### Updating to Latest

```bash
# Pull the latest skill archive changes
git submodule update --remote .skills/archive

# Commit the updated submodule reference
git add .skills/archive
git commit -m "chore: update skill archive to latest"
```

#### Automated Periodic Updates

Set up a CI job or cron task to periodically update the submodule:

```yaml
# GitHub Actions example: .github/workflows/update-skills.yml
name: Update Skill Archive
on:
  schedule:
    - cron: '0 6 * * 1'  # Every Monday at 06:00 UTC
  workflow_dispatch:       # Allow manual trigger

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: true
          token: ${{ secrets.GITHUB_TOKEN }}

      - name: Update skill archive submodule
        run: |
          git submodule update --remote .skills/archive
          if git diff --quiet; then
            echo "No updates available"
          else
            git config user.name "github-actions[bot]"
            git config user.email "github-actions[bot]@users.noreply.github.com"
            git add .skills/archive
            git commit -m "chore: update skill archive to latest"
            git push
          fi
```

### Method B: Symbolic Links (Recommended for Local / Single-Machine Use)

If the Skill Archive lives on the same machine (e.g., a shared drive or a local clone), symlinks provide zero-copy live links.

#### Setup

```bash
# Linux/macOS — link entire skills directory
ln -s /path/to/skill-archive/skills .claude/skills/archive

# Windows (PowerShell, Developer Mode enabled)
New-Item -ItemType SymbolicLink -Path ".claude\skills\archive" `
  -Target "G:\Skill Archive\skills"
```

The agent then reads directly from the archive. Any `git pull` on the archive immediately reflects in your project.

#### Keeping It Read-Only

Symlinks are inherently read-only in the sense that the file "lives" in the archive, not your project. To enforce discipline:

- **Never edit** files through the symlink — always edit in the Skill Archive repo directly.
- On Windows, use **directory junctions** (`mklink /J`) for broader compatibility if symlinks require elevated permissions.
- Optionally set the archive worktree to read-only:

  ```bash
  # Make the archive read-only at the filesystem level
  chmod -R a-w /path/to/skill-archive/skills/

  # Windows equivalent
  attrib +R "G:\Skill Archive\skills\*.md"
  ```

### Method C: Sync Script with Lock File (For Environments Without Git Submodules)

For environments where git submodules or symlinks aren't practical (e.g., ephemeral CI containers, cloud-based IDEs):

```bash
# Pull latest skills and write a lockfile recording the source commit
node skill-archive/scripts/sync.js --mode live --target .claude/skills/ \
  --source <skill-archive-repo-url>

# This creates:
#   .claude/skills/*.md           ← skill files (read-only copies)
#   .claude/skills/.skill-lock    ← records source repo, commit hash, timestamp
```

The lock file allows verification of freshness:

```json
{
  "source": "https://github.com/org/skill-archive",
  "commit": "a1b2c3d4e5f6",
  "synced_at": "2026-02-26T19:00:00Z",
  "mode": "live",
  "skills": [
    "jidoka-autonomation.md",
    "poka-yoke-mistake-proofing.md"
  ]
}
```

---

## Quick Reference

```
COPY IMPORT:
  1. cp skill-archive/skills/<skill>.md  <your-project>/<agent-skills-dir>/
  2. Update references if importing a subset
  3. Commit into your project
  4. Re-copy manually to update

LIVE LINK (Git Submodule):
  1. git submodule add <repo-url> .skills/archive
  2. Symlink or configure agent to read from submodule
  3. git submodule update --remote to pull latest
  4. Automate with CI cron job

LIVE LINK (Symlink):
  1. ln -s /path/to/skill-archive/skills <agent-skills-dir>/archive
  2. git pull on archive to update
  3. Never edit through the symlink

CHOOSING A MODE:
  Need to customize?             → Copy
  Need auto-updates?             → Live Link
  Multiple projects, same team?  → Live Link (submodule)
  Single machine?                → Live Link (symlink)
  No git submodule support?      → Live Link (sync script)
```
