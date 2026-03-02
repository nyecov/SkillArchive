import os
import json
import yaml
import shutil
import platform
import subprocess
import re

# Paths
ROOT_DIR = "."
SOURCE_SKILLS_DIR = os.path.join(ROOT_DIR, "skills")
TARGET_SKILLS_DIR = os.path.join(ROOT_DIR, ".gemini", "skills")
CONFIG_FILE = os.path.join(ROOT_DIR, "local-agent-config.json")

def create_symlink(source, target):
    """
    Creates a junction point (Windows) or a symlink (others).
    """
    if os.path.exists(target):
        try:
            if platform.system() == "Windows":
                if os.path.isdir(target):
                    subprocess.run(['cmd', '/c', 'rmdir', target], check=True, capture_output=True)
                else:
                    os.unlink(target)
            else:
                os.unlink(target)
        except Exception:
            pass

    try:
        if platform.system() == "Windows":
            subprocess.run(['cmd', '/c', 'mklink', '/J', target, source], check=True, capture_output=True)
        else:
            os.symlink(source, target, target_is_directory=True)
        print(f"  [OK] Linked: {os.path.basename(source)} -> {os.path.basename(target)}")
    except Exception as e:
        print(f"  [ERROR] Failed to link {os.path.basename(source)}: {e}")

def get_skill_metadata(skill_folder):
    skill_file = os.path.join(SOURCE_SKILLS_DIR, skill_folder, "SKILL.md")
    if not os.path.exists(skill_file):
        return None
    try:
        with open(skill_file, 'r', encoding='utf-8') as f:
            content = f.read()
            fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if fm_match:
                data = yaml.safe_load(fm_match.group(1))
                if data:
                    data['folder'] = skill_folder
                    return data
    except Exception as e:
        print(f"Error parsing metadata for {skill_folder}: {e}")
    return None

def main():
    # KYT Safeguard
    safe_target = TARGET_SKILLS_DIR.replace('\\', '/')
    if not safe_target.endswith('.gemini/skills') and not safe_target.endswith('.gemini/skills/'):
        raise ValueError(f"KYT Safeguard Error: Target directory '{TARGET_SKILLS_DIR}' is unsafe.")

    # Clear target directory accurately
    if os.path.exists(TARGET_SKILLS_DIR):
        print(f"Clearing existing links in {TARGET_SKILLS_DIR}...")
        for item in os.listdir(TARGET_SKILLS_DIR):
            item_path = os.path.join(TARGET_SKILLS_DIR, item)
            try:
                if platform.system() == "Windows":
                    if os.path.isdir(item_path):
                        # Junction points are directories, use rmdir
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

    # 0. Load config to check discovery mode
    discovery_mode = "dynamic"
    synced_skill_ids = []
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            discovery_mode = config.get("discovery_mode", "dynamic")
            synced_skill_ids = list(config.get("synced_skills", {}).keys())

    # 1. Discover all skills with valid IDs
    discovered_skills = {} # id -> meta
    for skill_folder in os.listdir(SOURCE_SKILLS_DIR):
        meta = get_skill_metadata(skill_folder)
        if meta and meta.get('id') and meta.get('name'):
            skill_id = meta['id']
            if discovery_mode == "manual" and skill_id not in synced_skill_ids:
                continue
            discovered_skills[skill_id] = meta

    # 2. Link Skills by Name
    print(f"Linking {len(discovered_skills)} skills...")
    for skill_id, meta in discovered_skills.items():
        folder_name = meta['folder']
        skill_name = meta['name']
        source_path = os.path.abspath(os.path.join(SOURCE_SKILLS_DIR, folder_name))
        target_path = os.path.abspath(os.path.join(TARGET_SKILLS_DIR, skill_name))
        create_symlink(source_path, target_path)

    # 3. Update discovery reference if in dynamic mode
    if discovery_mode == "dynamic" and os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        config["synced_skills"] = {sid: m['name'] for sid, m in discovered_skills.items()}
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)

if __name__ == "__main__":
    main()
