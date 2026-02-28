import os
import yaml
import glob
import sys
import re
import json

def validate():
    errors = []
    files = glob.glob('skills/*/SKILL.md')
    required_fields = ['name', 'version', 'level', 'description', 'category', 'tags']
    allowed_levels = ['methodology', 'tactical', 'technical']
    
    # Load schema for validation
    config_file = 'skills-config.json'
    allowed_categories = []
    allowed_tags = []
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            try:
                config = json.load(f)
                allowed_categories = config.get('allowed_categories', [])
                allowed_tags = config.get('allowed_tags', [])
            except json.JSONDecodeError:
                print(f"Warning: {config_file} is not valid JSON. Rule enforcement degraded.")

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
                
                for field in required_fields:
                    if field not in data:
                        errors.append(f"{f}: Missing required field '{field}'")
                
                if 'level' in data and data['level'] not in allowed_levels:
                    errors.append(f"{f}: Invalid level '{data['level']}'. Must be one of {allowed_levels}")
                
                # Check category against config
                if allowed_categories and 'category' in data:
                    cat = data.get('category')
                    if cat not in allowed_categories:
                        errors.append(f"{f}: Unrecognized category '{cat}'")

                # Check tags against config
                if allowed_tags and 'tags' in data:
                    tags = data.get('tags')
                    if isinstance(tags, list):
                        for tag in tags:
                            if tag not in allowed_tags:
                                errors.append(f"{f}: Unrecognized tag '{tag}'. Update {config_file} to allow.")
                    else:
                        errors.append(f"{f}: 'tags' must be a list")
                
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
