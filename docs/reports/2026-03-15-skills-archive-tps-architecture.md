# TPS Architecture Review: Skills Archive Standardization

## 1. Shusa Strategy & Vision
The vision of the Skill Archive is to provide a perfectly deterministic, error-free library of cognitive methodologies. The current architecture requires manual verification of these Markdown files, leading to structural *Mura* (unevenness) across the 33 skills. The strategy is to enforce the Gold Standard programmatically using the `manage_skill_authoring.py` Meta-Poka-yoke script.

## 2. Value Stream Analysis (VSM)
- **Current Bottlenecks:** Agent misinterprets a skill because it lacks a standard heading or uses absolute paths instead of relative ones.
- **Future State Architecture:** All skills possess perfect YAML frontmatter (UUIDs, semantic versioning, hierarchical levels), strict 150-line soft limits, and verified relative paths.

## 3. Dependency Impact (Nemawashi)
- **Ripple Zones:** Executing an auto-formatter across 33 skills has massive ripple effects on Git history and potential reference breakage.
- **Identified Conflicts:** If the Python script fails to resolve a relative path correctly, it could falsely flag a skill as unrecoverable, requiring manual human intervention.

## 4. Execution Flow (Heijunka & KYT)
- **Batched Rollout Plan:**
  1. **Phase 4 (Pilot):** Run the script on a single, isolated skill (e.g., `architectural-anchoring`) to verify script compatibility with the local Python environment.
  2. **Phase 5 (Kaizen Sprint):** Execute a bulk loop running the script on all remaining 32 skills sequentially.
- **Critical Hazards Isolated:** Mass corruption of Markdown files if the script's regex logic fails.

## 5. Organizational Guardrails (Jidoka)
- **Andon Cord Triggers:** If `manage_skill_authoring.py` outputs "unrecoverable" for any skill, the deployment loop MUST immediately halt. We must pivot to the `interview` skill or manual intervention before resuming the batch.
- **Poka-yoke Interlocks:** The Python script itself acts as the primary interlock, rejecting any `SKILL.md` that lacks a `description` or uses forbidden characters (emojis).