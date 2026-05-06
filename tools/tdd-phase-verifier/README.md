# tdd-phase-verifier

Lints a git commit range to enforce the `[Red]/[Green]/[Refactor]` TDD commit-prefix convention defined in the `test-driven-development` skill.

## What it checks

- `[Red]` commits may only touch test files. Any production code change is a violation.
- `[Green]` commits must have a preceding `[Red]` for the same story ID in the scan range.
- `[Refactor]` commits must have a completed Red-Green cycle for the story in the scan range.

## Usage

```bash
# Default: scans origin/main..HEAD (or last 50 commits)
python verify_red_phase.py

# Custom range
python verify_red_phase.py --range HEAD~30..HEAD
python verify_red_phase.py --range a1b2c3..d4e5f6

# Custom story ID pattern (default matches AREA-SUBAREA-NN-NN)
python verify_red_phase.py --story-prefix "TICKET-\d+"

# Custom test file patterns (comma-separated Python regex)
python verify_red_phase.py --test-patterns ".*_test\.go$,.*_test\.py$,.*\.spec\.ts$"
```

## Exit codes

- `0` — all commits in range are clean
- `1` — one or more violations (details printed to stdout)

## Wire as a pre-commit hook

Add to `.pre-commit-config.yaml`:

```yaml
- repo: local
  hooks:
    - id: tdd-verify-red-phase
      name: TDD Red-Phase Verifier
      entry: python tools/tdd-phase-verifier/verify_red_phase.py
      language: python
      pass_filenames: false
      stages: [pre-push]
```
