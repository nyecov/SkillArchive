# TPS Architecture Review: Tools Directory Hardening

## 1. Shusa Strategy & Vision
**Vision:** Transform the `/tools` directory from a collection of fragile scripts into a professional, high-integrity automation suite that powers the repository's CI/CD and self-healing capabilities.
**Misalignment Target:** The current lack of shared utilities and structured logging creates "Information Islands" where scripts fail silently or inconsistently, increasing the cognitive load for maintenance (Muri).

## 2. Value Stream Analysis (VSM)
- **Current Bottlenecks:** 
  - Redundant Code: Frontmatter parsing is implemented 4+ times (Muda).
  - Opaque Failures: `print()` based output makes automated parsing of failure reasons difficult.
- **Future State Architecture:** 
  - **Shared Intelligence:** A core `tools/repo_utils.py` module will provide a single source of truth for repository state, frontmatter extraction, and logging configuration.
  - **Standard Interface:** All scripts will follow a strict pattern: `Parse Config -> Log Intent -> Execute with Atomic Guards -> Explicit Exit Code`.

## 3. Dependency Impact (Nemawashi)
- **Ripple Zones:** All scripts listed in `.git/hooks/pre-commit` will be updated. This requires ensuring the Git Hook remains functional during the transition.
- **Identified Conflicts:** Migrating to `logging` might change the output format seen by users during commits. We will ensure the logging level is set to `INFO` for standard output to maintain a clean terminal experience.

## 4. Execution Flow (Heijunka & KYT)
- **Batched Rollout Plan:**
  1. **Batch 1 (Foundations):** Create `tools/repo_utils.py`. Implement the shared `get_logger()` and `get_frontmatter()` functions.
  2. **Batch 2 (Core Validation):** Harden `validate_frontmatter.py` and `check_refs.py`.
  3. **Batch 3 (Data Sync):** Harden `update_metadata.py`, `sync_skills.py`, and `sync_workflows.py`.
  4. **Batch 4 (Reporting):** Harden `generate_readme.py`.
- **Critical Hazards Isolated:** 
  - **Pre-commit Lockout:** A bug in the new `repo_utils.py` could prevent all commits. **Countermeasure:** Pilot test each batch manually before committing.
  - **Data Corruption:** Atomic write-and-rename will be implemented for all scripts that modify metadata or READMEs.

## 5. Organizational Guardrails (Jidoka)
- **Andon Cord Triggers:** 
  - If `repo_utils.py` fails its own unit test (to be added), the build process MUST halt.
  - If a script encounters an unknown YAML schema, it MUST quarantine the file and exit non-zero rather than proceeding with default values.
- **Poka-yoke Interlocks:** 
  - The shared `get_frontmatter()` utility will perform schema validation natively, ensuring that even if `validate_frontmatter.py` hasn't run yet, subsequent tools don't crash on malformed data.
