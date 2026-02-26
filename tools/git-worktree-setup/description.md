# Git Worktree Setup

An automation bash script that streamlines the process of checking out a new feature branch in an isolated directory using Git Worktrees, followed by automated project setup.

**Primary Uses:**
1. Keeping the main repository working directory clean while working on a new feature or bugfix.
2. Auto-detecting project types (`package.json`, `requirements.txt`, `Cargo.toml`, `go.mod`) and running the appropriate dependency installation step automatically.

**Usage:**
```bash
./git_worktree_setup.sh <branch-name> <relative-directory-path>
```
