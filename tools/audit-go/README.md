# audit-go

Code quality audit scripts for Go projects. Each script is standalone, accepts `--path` and `--json` flags, and integrates with CI or the `code-review` / `refactor-safely` skills.

## Scripts

| Script | Tool | What it checks |
|---|---|---|
| `audit_go_lint.py` | golangci-lint | Lint violations across all linters configured in `.golangci.yml` |
| `audit_go_naming.py` | AST regex | Package names (lowercase), exported functions (PascalCase), constants (UPPER_CASE) |
| `audit_go_unused_deps.py` | go vet | Unused imports via `go vet ./...` |
| `audit_go_standards.py` | AST regex | Missing error handling, undocumented exported symbols |

## Usage

```bash
# Human-readable output (default)
python audit_go_lint.py
python audit_go_naming.py --path ./internal/domain
python audit_go_unused_deps.py
python audit_go_standards.py --path ./internal

# JSON output for scripting/CI
python audit_go_lint.py --json
python audit_go_naming.py --json --path ./internal
```

## Requirements

- `audit_go_lint.py` requires `golangci-lint`: `go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest`
- `audit_go_unused_deps.py` requires Go 1.21+
- `audit_go_naming.py` and `audit_go_standards.py` require only Python 3.8+

## Exit Codes

- `audit_go_lint.py` and `audit_go_unused_deps.py`: exit 1 if issues found (fail-closed for CI).
- `audit_go_naming.py` and `audit_go_standards.py`: exit 0 always (report-only).
