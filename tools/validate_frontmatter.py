import os
import yaml
import glob
import sys
import re
import json

def validate():
    errors = []
    files = glob.glob('skills/*/SKILL.md') + glob.glob('workflows/*.md')
    required_fields = ['id', 'name', 'version', 'level', 'description']
    allowed_levels = ['methodology', 'tactical', 'technical']
    
    for f in files:
        with open(f, 'r', encoding='utf-8') as stream:
            content = stream.read()
            fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if not fm_match:
                errors.append(f"{f}: Missing or invalid YAML frontmatter structure")
                continue
            
            try:
                data = yaml.safe_load(fm_match.group(1))
                if not data:
                    errors.append(f"{f}: Empty YAML frontmatter")
                    continue
                
                # Check for required fields
                for field in required_fields:
                    if field not in data:
                        errors.append(f"{f}: Missing required field '{field}'")
                
                # Enforce UUID format for id
                if 'id' in data:
                    uid = str(data.get('id', ''))
                    if not re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$', uid, re.I):
                         errors.append(f"{f}: Field 'id' must be a valid UUIDv4")

                if 'level' in data and data['level'] not in allowed_levels:
                    errors.append(f"{f}: Invalid level '{data['level']}'. Must be one of {allowed_levels}")
                
                
            except yaml.YAMLError as e:
                errors.append(f"{f}: YAML parsing error: {str(e)}")

    if errors:
        print("Frontmatter Validation Errors:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
    else:
        print("All skill frontmatter valid.")

if __name__ == "__main__":
    validate()
