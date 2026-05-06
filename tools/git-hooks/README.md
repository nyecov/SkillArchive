# git-hooks

Pre-commit hook setup scripts for projects using the `pre-commit` framework. Handles framework installation, optional Go tooling, and a native pre-commit auto-fixer to prevent double-pass commit failures.

## Scripts

### install-hooks.ps1

One-shot installer. Idempotent — safe to re-run.

```powershell
# Install for any project
.\install-hooks.ps1

# Install for a non-Go project (skip goimports / golangci-lint)
.\install-hooks.ps1 -SkipGoTools

# Force reinstall
.\install-hooks.ps1 -Force
```

After install, hooks fire automatically on `git commit`.

```powershell
# Run manually
pre-commit run --all-files
pre-commit run --all-files --hook-stage manual
```

### git-pre-commit.ps1

Native auto-fixer for Go projects. Runs goimports and go mod tidy on staged files BEFORE the pre-commit framework, preventing the "files were modified by this hook" double-pass abort.

**Configure via environment variable:**
```powershell
$env:GOIMPORTS_LOCAL_PREFIX = "github.com/myorg/myrepo"
```

This script is called from a `.git/hooks/pre-commit` shim; it is not intended to be run directly.

## Requirements

- `install-hooks.ps1` requires Python and pip for the `pre-commit` framework.
- `git-pre-commit.ps1` requires `goimports` (`go install golang.org/x/tools/cmd/goimports@latest`).
- Both require Git and PowerShell 5.1+.
