import os
import yaml
import glob
import sys
import re
import uuid

def is_valid_uuid(val):
    try:
        uuid_obj = uuid.UUID(str(val), version=4)
        return str(uuid_obj) == str(val)
    except ValueError:
        return False

def inject_or_replace_uuid(file_path, current_content, fm_content):
    new_id = str(uuid.uuid4())
    
    # Check if 'id:' exists at all
    if re.search(r'^id:\s*.*$', fm_content, flags=re.MULTILINE):
        # Replace existing id
        new_fm = re.sub(r'^id:\s*.*$', f'id: {new_id}', fm_content, flags=re.MULTILINE)
    else:
        # Prepend id
        new_fm = f"id: {new_id}\n{fm_content}"
        
    full_new_content = re.sub(r'^---\s*\n(.*?)\n---\s*\n', f'---\n{new_fm}\n---\n', current_content, flags=re.DOTALL)
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(full_new_content)
        
    return new_id

def validate_and_repair():
    errors = []
    files = glob.glob('skills/*/SKILL.md') + glob.glob('workflows/*.md')
    required_fields = ['id', 'name', 'version', 'level', 'description']
    allowed_levels = ['methodology', 'tactical', 'technical']
    
    seen_uuids = {} # map UUID -> file_path
    repaired_files = 0
    
    for f in files:
        # Resolve windows paths for display
        norm_f = os.path.normpath(f)
        
        with open(norm_f, 'r', encoding='utf-8') as stream:
            content = stream.read()
            
        fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
        if not fm_match:
            errors.append(f"{norm_f}: Missing or invalid YAML frontmatter structure")
            continue
            
        fm_content = fm_match.group(1)
        try:
            data = yaml.safe_load(fm_content)
            if not data:
                errors.append(f"{norm_f}: Empty YAML frontmatter")
                continue
            
            # Check for required fields (excluding id which we auto-fix)
            for field in required_fields:
                if field not in data and field != 'id':
                    errors.append(f"{norm_f}: Missing required field '{field}'")
            
            if 'level' in data and data['level'] not in allowed_levels:
                errors.append(f"{norm_f}: Invalid level '{data['level']}'. Must be one of {allowed_levels}")
                
            # -- UUID VALIDATION & REPAIR --
            needs_repair = False
            current_uid = str(data.get('id', '')).strip()
            
            if not current_uid:
                print(f"[REPAIR] Missing UUID in {norm_f}")
                needs_repair = True
            elif not is_valid_uuid(current_uid):
                print(f"[REPAIR] Malformed UUID '{current_uid}' in {norm_f}")
                needs_repair = True
            elif current_uid in seen_uuids:
                print(f"[REPAIR] Duplicate UUID '{current_uid}' found in {norm_f} (already exists in {seen_uuids[current_uid]})")
                needs_repair = True
                
            if needs_repair:
                new_uid = inject_or_replace_uuid(norm_f, content, fm_content)
                seen_uuids[new_uid] = norm_f
                repaired_files += 1
                print(f"  -> Generated new UUID: {new_uid}")
            else:
                seen_uuids[current_uid] = norm_f
            
        except yaml.YAMLError as e:
            errors.append(f"{norm_f}: YAML parsing error: {str(e)}")

    if repaired_files > 0:
        print(f"\n[AUTO-FIX] Successfully repaired {repaired_files} file(s).")
        # We exit 1 if we modified files so the commit hook pauses,
        # forcing the user to stage the auto-repaired files.
        print("Please review the changes, `git add` the modified files, and commit again.")
        sys.exit(1)

    if errors:
        print("\nFrontmatter Validation Errors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("All skill frontmatter valid and UUIDs are globally unique.")

if __name__ == "__main__":
    validate_and_repair()
