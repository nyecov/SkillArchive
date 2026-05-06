"""
Frontmatter Validator & Repair Tool
---------------------------------
Validates YAML frontmatter across all skills and workflows.
Automatically repairs missing, malformed, or duplicate UUIDv4 IDs.

Usage: python tools/validate_frontmatter.py
Exit Codes: 0 (Success), 1 (Repair/Validation Failure)
"""

import os
import sys
import glob
import uuid
import logging
from pathlib import Path
from repo_utils import setup_logging, get_frontmatter, atomic_write, is_valid_uuid4

# Initialize standardized logging
log = setup_logging("frontmatter_validator")

def repair_uuid(file_path: Path) -> str:
    """
    Injects or replaces a UUIDv4 in the file's frontmatter.
    Returns the new UUID.
    """
    new_id = str(uuid.uuid4())
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if 'id:' exists at all in the file content
    if "id:" in content:
        # Replace existing id (limited to frontmatter block)
        new_content = re.sub(r'id:\s*.*$', f'id: {new_id}', content, count=1, flags=re.MULTILINE)
    else:
        # Prepend id after the first ---
        new_content = content.replace("---\n", f"---\nid: {new_id}\n", 1)
        
    atomic_write(file_path, new_content)
    return new_id

def validate_and_repair():
    """Performs the main validation and repair loop."""
    required_fields = ['id', 'name', 'version', 'level', 'description']
    allowed_levels = ['methodology', 'tactical', 'technical']
    
    files = [Path(f) for f in (glob.glob('skills/*/SKILL.md') + glob.glob('workflows/*.md'))]
    seen_uuids = {} # map UUID -> file_path
    repaired_files = 0
    validation_errors = 0
    
    log.info(f"Validating {len(files)} files...")
    
    for f_path in files:
        data = get_frontmatter(f_path)
        
        if data is None:
            log.error(f"Missing or invalid frontmatter structure in {f_path}")
            validation_errors += 1
            continue
            
        # Check for required fields (excluding id which we auto-fix)
        for field in required_fields:
            if field not in data and field != 'id':
                log.error(f"Missing required field '{field}' in {f_path}")
                validation_errors += 1
        
        if 'level' in data and data['level'] not in allowed_levels:
            log.error(f"Invalid level '{data['level']}' in {f_path}. Must be one of {allowed_levels}")
            validation_errors += 1
            
        # -- UUID VALIDATION & REPAIR --
        needs_repair = False
        current_uid = str(data.get('id', '')).strip()
        
        if not current_uid:
            log.warning(f"Missing UUID in {f_path} -> REPAIRING")
            needs_repair = True
        elif not is_valid_uuid4(current_uid):
            log.warning(f"Malformed UUID '{current_uid}' in {f_path} -> REPAIRING")
            needs_repair = True
        elif current_uid in seen_uuids:
            log.warning(f"Duplicate UUID '{current_uid}' found in {f_path} (exists in {seen_uuids[current_uid]}) -> REPAIRING")
            needs_repair = True
            
        if needs_repair:
            import re # Needed for UUID replacement
            new_uid = str(uuid.uuid4())
            with open(f_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Match frontmatter specifically to avoid replacing 'id:' elsewhere in the doc
            if re.search(r'^id:\s*.*$', content, flags=re.MULTILINE):
                new_content = re.sub(r'^id:\s*.*$', f'id: {new_uid}', content, count=1, flags=re.MULTILINE)
            else:
                new_content = content.replace("---\n", f"---\nid: {new_uid}\n", 1)
                
            atomic_write(f_path, new_content)
            seen_uuids[new_uid] = f_path
            repaired_files += 1
            log.info(f"  -> Successfully generated new UUID: {new_uid}")
        else:
            seen_uuids[current_uid] = f_path

    if repaired_files > 0:
        log.info(f"AUTO-FIX: Successfully repaired {repaired_files} file(s).")
        log.info("Please review changes, `git add` the modified files, and commit again.")
        sys.exit(1)

    if validation_errors > 0:
        log.error(f"Validation failed with {validation_errors} errors.")
        sys.exit(1)
    
    log.info("All skill frontmatter valid and UUIDs are globally unique.")

if __name__ == "__main__":
    try:
        validate_and_repair()
    except Exception as e:
        log.critical(f"Unhandled exception during validation: {e}", exc_info=True)
        sys.exit(1)
