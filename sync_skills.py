import os
import json
import yaml
import shutil
import platform
import subprocess

# Paths
ROOT_DIR = "."
SOURCE_SKILLS_DIR = os.path.join(ROOT_DIR, "skills")
TARGET_SKILLS_DIR = os.path.join(ROOT_DIR, ".gemini", "skills")
CONFIG_FILE = os.path.join(ROOT_DIR, "skills-config.json")

def create_symlink(source, target):
    """
    Creates a junction point (Windows) or a symlink (others).
    """
    if os.path.exists(target):
        return # Already linked
    try:
        if platform.system() == "Windows":
            subprocess.run(['cmd', '/c', 'mklink', '/J', target, source], check=True, capture_output=True)
        else:
            os.symlink(source, target, target_is_directory=True)
        print(f"  [OK] Linked: {os.path.basename(source)}")
    except Exception as e:
        print(f"  [ERROR] Failed to link {os.path.basename(source)}: {e}")

def get_skill_metadata(skill_folder):
    skill_file = os.path.join(SOURCE_SKILLS_DIR, skill_folder, "SKILL.md")
    if not os.path.exists(skill_file):
        return None
    try:
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
            if content.startswith('---'):
                parts = content.split('---')
                if len(parts) >= 3:
                    return yaml.safe_load(parts[1])
    except:
        pass
    return None

def resolve_dependencies(skill_folder, resolved_set):
    if skill_folder in resolved_set:
        return
    
    meta = get_skill_metadata(skill_folder)
    if not meta:
        return

    resolved_set.add(skill_folder)
    
    # Check for explicit 'requires' list
    requires = meta.get('requires', [])
    for dep in requires:
        # Dependency is a folder name
        resolve_dependencies(dep, resolved_set)

def main():
    if not os.path.exists(CONFIG_FILE):
        print(f"Config file not found at {CONFIG_FILE}")
        return

    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    allowed_tags = set(config.get("allowed_tags", []))
    allowed_categories = set(config.get("allowed_categories", []))
    allowed_skills = set(config.get("allowed_skills", [])) # New: explicit skill pull

    # Clear target directory
    if os.path.exists(TARGET_SKILLS_DIR):
        print(f"Clearing existing links in {TARGET_SKILLS_DIR}...")
        for item in os.listdir(TARGET_SKILLS_DIR):
            item_path = os.path.join(TARGET_SKILLS_DIR, item)
            try:
                if platform.system() == "Windows":
                    if os.path.isdir(item_path):
                        subprocess.run(['cmd', '/c', 'rmdir', item_path], check=True, capture_output=True)
                    else:
                        os.unlink(item_path)
                else:
                    if os.path.islink(item_path) or os.path.isfile(item_path):
                        os.unlink(item_path)
                    elif os.path.isdir(item_path):
                        shutil.rmtree(item_path)
            except Exception as e:
                print(f"  [ERROR] Could not delete {item}: {e}")
    else:
        os.makedirs(TARGET_SKILLS_DIR, exist_ok=True)

    # 1. Identify "Seed" Skills based on Tags/Categories/Explicit list
    seed_skills = set()
    for skill_folder in os.listdir(SOURCE_SKILLS_DIR):
        meta = get_skill_metadata(skill_folder)
        if not meta: continue
        
        skill_tags = set(meta.get('tags', []))
        skill_category = meta.get('category', '')
        skill_name = meta.get('name', '')

        if (skill_tags & allowed_tags) or (skill_category in allowed_categories) or (skill_name in allowed_skills):
            seed_skills.add(skill_folder)

    # 2. Recursively Resolve Dependencies
    final_skills = set()
    print("Resolving dependencies...")
    for seed in seed_skills:
        resolve_dependencies(seed, final_skills)

    # 3. Create Links
    print(f"Linking {len(final_skills)} skills...")
    for skill in sorted(list(final_skills)):
        source_path = os.path.join(SOURCE_SKILLS_DIR, skill)
        target_path = os.path.join(TARGET_SKILLS_DIR, skill)
        create_symlink(source_path, target_path)

if __name__ == "__main__":
    main()
