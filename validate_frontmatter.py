import os
import yaml
import glob
import sys

def validate():
    errors = []
    files = glob.glob('skills/*/SKILL.md')
    required_fields = ['name', 'version', 'level', 'description', 'category', 'tags']
    allowed_levels = ['methodology', 'tactical', 'technical']

    for f in files:
        with open(f, 'r', encoding='utf-8') as stream:
            content = stream.read()
            if not content.startswith('---'):
                errors.append(f"{f}: Missing YAML frontmatter")
                continue
            parts = content.split('---')
            if len(parts) < 3:
                errors.append(f"{f}: Invalid YAML frontmatter structure")
                continue
            
            try:
                data = yaml.safe_load(parts[1])
                if not data:
                    errors.append(f"{f}: Empty YAML frontmatter")
                    continue
                
                for field in required_fields:
                    if field not in data:
                        errors.append(f"{f}: Missing required field '{field}'")
                
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
