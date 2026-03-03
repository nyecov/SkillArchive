# Lean Analysis Report: Tools Directory Hardening

## Executive Summary
The repository's automation tools are functional but fragile. They rely on inconsistent coding patterns (mixing `os.path` and `pathlib`), lack structured logging (Muri), and contain redundant logic for parsing YAML frontmatter (Muda). Hardening these scripts is a prerequisite for a stable, self-healing repository.

## Phase Results

### Phase 1: Lean Foundations — 3M & 5S
- **Muri (Overburden):** The absence of structured logging forces developers to add temporary print statements to debug Git Hook failures.
- **Muda (Waste):** Redundant frontmatter parsing logic is duplicated across `sync_skills.py`, `generate_readme.py`, and `validate_frontmatter.py`.
- **Mura (Unevenness):** Documentation is inconsistent; some tools use `description.md`, while others have no documentation at all. Coding styles vary between standard library `os` calls and the more modern `pathlib`.

### Phase 2: Story Interview — Assumptions
- **Assumption:** That all scripts will always be run from the repository root.
- **Assumption:** That the `yaml` and `mark3labs/mcp-go` (for Go tools) dependencies are always present in the environment.

### Phase 3: Value Stream Mapping — Bottlenecks
- **Bottleneck:** The pre-commit hook execution time is extended by multiple scripts performing the same directory walk and file parsing operations independently.

### Phase 4: KYT — Hazard Prediction
- **Critical Hazard:** `sync_skills.py` performs destructive `rmdir` and `unlink` operations. A path calculation error could result in accidental deletion of source skill files if the `TARGET_SKILLS_DIR` logic is flawed.

### Phase 5: Poka-yoke — Guardrails
- **Missing Guardrail:** No validation that a script actually succeeded before the next script in the pre-commit chain runs (other than basic exit codes, which are currently inconsistent).

### Phase 6: Shisa Kanko — Precision Audit
- **Point:** Exit Code Integrity.
- **Call (Verification):** Every script must be audited to ensure it explicitly returns `sys.exit(1)` on any error that should halt the commit process.

### Phase 7: Nemawashi — Dependencies
- **Ripple Effect:** Standardizing the frontmatter parsing logic into a shared utility within `/tools` will require updating all 4+ scripts that currently perform parsing.

### Phase 8: Shusa Leadership — Strategic Alignment
- **Verdict (Aligned):** Hardening the tools directly supports the vision of a "Zero-Maintenance" repository where the system automatically heals structural defects (like the UUID repair we just implemented).

### Phase 9: Yokoten — Horizontal Deployment
- **Pattern Transfer:** The "Self-Healing UUID" pattern from `validate_frontmatter.py` should be used as a template for other validation tools (e.g., auto-fixing broken references).

## Critical Actions
1. **Standardize Logging:** Implement a shared `logging_setup.py` or a standard snippet that configures `logging.basicConfig` with a professional format (Timestamp | Level | Module | Message).
2. **Standardize Docstrings:** Apply Google-style docstrings to every script.
3. **Robust Entry Points:** Wrap all `main()` functions in `try-except Exception as e: logging.error(e); sys.exit(1)`.
4. **Refactor Shared Logic:** Extract the `get_frontmatter` logic into a shared utility file (e.g., `tools/utils.py`) to eliminate Muda.

## Yokoten Broadcast
- The "Atomic Write-and-Rename" pattern should be mandated for any tool that modifies existing files to prevent state corruption during interruptions.
