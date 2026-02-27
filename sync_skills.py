import os
import json
import yaml
import shutil
import platform
import subprocess

# Paths
ROOT_DIR = r"G:\Skill Archive"
SOURCE_SKILLS_DIR = os.path.join(ROOT_DIR, "skills")
TARGET_SKILLS_DIR = os.path.join(ROOT_DIR, ".gemini", "skills")
CONFIG_FILE = os.path.join(ROOT_DIR, "skills-config.json")

def create_symlink(source, target):
    """
    Creates a junction point (Windows) or a symlink (others).
    On Windows, junction points (/J) do not require administrator privileges.
    """
    try:
        if platform.system() == "Windows":
            # For directories, /J (Junction) is often more permissive than /D (Symlink)
            subprocess.run(['cmd', '/c', 'mklink', '/J', target, source], check=True, capture_output=True)
        else:
            os.symlink(source, target, target_is_directory=True)
        print(f"  [OK] Linked: {os.path.basename(source)}")
    except Exception as e:
        print(f"  [ERROR] Failed to link {os.path.basename(source)}: {e}")

def main():
    # Load config
    if not os.path.exists(CONFIG_FILE):
        print(f"Config file not found at {CONFIG_FILE}")
        return

    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    
    allowed_tags = set(config.get("allowed_tags", []))
    allowed_categories = set(config.get("allowed_categories", []))

    # Clear target directory
    if os.path.exists(TARGET_SKILLS_DIR):
        print(f"Clearing existing links in {TARGET_SKILLS_DIR}...")
        for item in os.listdir(TARGET_SKILLS_DIR):
            item_path = os.path.join(TARGET_SKILLS_DIR, item)
            try:
                if platform.system() == "Windows":
                    # For junctions/links on Windows, use rmdir for directories or unlink for files
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

    print("Scanning skills for matches...")
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
                # Extract YAML frontmatter
                if content.startswith('---'):
                    parts = content.split('---')
                    if len(parts) >= 3:
                        metadata = yaml.safe_load(parts[1])
                        
                        skill_tags = set(metadata.get('tags', []))
                        skill_category = metadata.get('category', '')

                        # Check if any tag or category matches
                        if (skill_tags & allowed_tags) or (skill_category in allowed_categories):
                            target_path = os.path.join(TARGET_SKILLS_DIR, skill_folder)
                            create_symlink(skill_path, target_path)
        except Exception as e:
            print(f"  [ERROR] Processing {skill_folder}: {e}")

if __name__ == "__main__":
    main()
