# audit-python

Code quality audit scripts for Python projects. Each script is standalone, accepts `--path` and `--json` flags, and integrates with CI or the `code-review` / `refactor-safely` skills.

## Scripts

| Script | Tool | What it checks |
|---|---|---|
| `audit_python_lint.py` | pylint + ruff | Lint violations (runs both by default; use `--linter` to select) |
| `audit_python_naming.py` | AST | Function names (snake_case), class names (PascalCase), variables (snake_case) |
| `audit_python_unused_deps.py` | AST | Unused imports detected via import/usage analysis |
| `audit_python_standards.py` | AST | Missing docstrings, long functions (default limit: 50 lines) |

## Usage

```bash
# Human-readable output (default)
python audit_python_lint.py
python audit_python_lint.py --linter ruff --path ./src
python audit_python_naming.py --path ./tools
python audit_python_unused_deps.py
python audit_python_standards.py --max-lines 60

# JSON output for scripting/CI
python audit_python_lint.py --json
python audit_python_naming.py --json --path ./src
```

## Requirements

- `audit_python_lint.py` requires pylint (`pip install pylint`) and/or ruff (`pip install ruff`)
- `audit_python_naming.py`, `audit_python_unused_deps.py`, `audit_python_standards.py` require only Python 3.8+ stdlib (ast module)

## Exit Codes

All scripts exit 0 (report-only). To integrate as CI gates, check the `total` field in JSON output.
