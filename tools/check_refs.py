"""
Reference Integrity Checker
--------------------------
Audits all skills and workflows to ensure that all internal file references 
(links in frontmatter or markdown) point to valid existing files.

Usage: python tools/check_refs.py
Exit Codes: 0 (Success), 1 (Broken References Detected)
"""

import os
import sys
import glob
import logging
from pathlib import Path
from repo_utils import setup_logging, get_frontmatter

# Initialize standardized logging
log = setup_logging("reference_checker")

def check_integrity():
    """Performs the main reference audit."""
    errors = []
    # Check both skills and workflows
    files = [Path(f) for f in (glob.glob('skills/*/SKILL.md') + glob.glob('workflows/*.md'))]
    
    log.info(f"Auditing references across {len(files)} files...")
    
    for f_path in files:
        data = get_frontmatter(f_path)
        if not data:
            continue
            
        # Check 'references' list in frontmatter
        if 'references' in data and isinstance(data['references'], list):
            for ref in data['references']:
                if isinstance(ref, dict) and 'path' in ref:
                    path_val = ref['path']
                    # Calculate absolute path relative to the source file's directory
                    target_path = (f_path.parent / path_val).resolve()
                    
                    if not target_path.exists():
                        err_msg = f"Broken Reference: '{path_val}' in {f_path}"
                        log.error(err_msg)
                        errors.append(err_msg)
        
        # Check 'requires' list in frontmatter (linking to other skills by name)
        if 'requires' in data and isinstance(data['requires'], list):
            for skill_name in data['requires']:
                # Heuristic: required skills should exist in skills/<name>/SKILL.md
                skill_path = Path("skills") / skill_name / "SKILL.md"
                if not skill_path.exists():
                    err_msg = f"Missing Requirement: Skill '{skill_name}' required by {f_path} does not exist."
                    log.error(err_msg)
                    errors.append(err_msg)

    if errors:
        log.error(f"Integrity check failed with {len(errors)} broken references.")
        sys.exit(1)
    else:
        log.info("No broken references found. Repository integrity intact.")

if __name__ == "__main__":
    try:
        check_integrity()
    except Exception as e:
        log.critical(f"Unhandled exception during integrity check: {e}", exc_info=True)
        sys.exit(1)
