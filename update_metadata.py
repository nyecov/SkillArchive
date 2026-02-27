import os
import json
import yaml

# Paths
ROOT_DIR = "."
SOURCE_SKILLS_DIR = os.path.join(ROOT_DIR, "skills")
CONFIG_FILE = os.path.join(ROOT_DIR, "skills-config.json")

def main():
    all_categories = set()
    all_tags = set()
    all_levels = set()

    print("Scanning skills for metadata...")
    # Iterate through source skills
    for skill_folder in os.listdir(SOURCE_SKILLS_DIR):
        skill_path = os.path.join(SOURCE_SKILLS_DIR, skill_folder)
        if not os.path.isdir(skill_path):
            continue

        skill_file = os.path.join(skill_path, "SKILL.md")
        if not os.path.exists(skill_file):
            continue

        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
                if content.startswith('---'):
                    parts = content.split('---')
                    if len(parts) >= 3:
                        metadata = yaml.safe_load(parts[1])
                        
                        category = metadata.get('category')
                        if category:
                            all_categories.add(category)
                        
                        level = metadata.get('level')
                        if level:
                            all_levels.add(level)
                        
                        tags = metadata.get('tags', [])
                        if isinstance(tags, list):
                            for tag in tags:
                                all_tags.add(tag)
        except Exception as e:
            print(f"  [ERROR] Processing {skill_folder}: {e}")

    # Load existing config
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                config = {}
    else:
        config = {"allowed_tags": [], "allowed_categories": [], "allowed_skills": []}

    # Ensure keys exist
    for key in ["allowed_tags", "allowed_categories", "allowed_skills"]:
        if key not in config:
            config[key] = []

    # Add the "comment" metadata section
    config["_discovery_reference"] = {
        "HELP": "This section is auto-generated and serves as a reference for available options.",
        "available_categories": sorted(list(all_categories)),
        "available_tags": sorted(list(all_tags)),
        "available_levels": sorted(list(all_levels))
    }

    # Save back to config file
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"Updated {CONFIG_FILE} with discovery metadata.")
    print(f"Found {len(all_categories)} categories, {len(all_levels)} levels, and {len(all_tags)} unique tags.")

if __name__ == "__main__":
    main()
