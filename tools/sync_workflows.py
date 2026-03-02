import os
import shutil
import platform
import subprocess
import yaml
import re

# Paths
ROOT_DIR = "."
SOURCE_WORKFLOWS_DIR = os.path.join(ROOT_DIR, "workflows")
TARGET_WORKFLOWS_DIR = os.path.join(ROOT_DIR, ".gemini", "workflows")
CONFIG_FILE = os.path.join(ROOT_DIR, "local-agent-config.json")

def create_symlink(source, target):
    """
    Creates a symbolic link for a file.
    """
    try:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        if os.path.exists(target) or os.path.islink(target):
            os.unlink(target)
            
        if platform.system() == "Windows":
            # Using 'mklink /H' for hard links which does not require admin rights.
            subprocess.run(['cmd', '/c', 'mklink', '/H', target, source], check=True, capture_output=True)
        else:
            os.symlink(source, target)
        print(f"  [OK] Linked: {os.path.basename(source)} -> {os.path.basename(target)}")
    except Exception as e:
        print(f"  [ERROR] Linking {os.path.basename(source)}: {e}")

def get_workflow_meta(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
            if fm_match:
                return yaml.safe_load(fm_match.group(1))
    except Exception as e:
        print(f"  [ERROR] Parsing {file_path}: {e}")
    return None

def main():
    # KYT Safeguard
    safe_target = TARGET_WORKFLOWS_DIR.replace('\\', '/')
    if not safe_target.endswith('.gemini/workflows') and not safe_target.endswith('.gemini/workflows/'):
        raise ValueError(f"KYT Safeguard Error: Target directory '{TARGET_WORKFLOWS_DIR}' is unsafe.")

    # Clear target directory
    if os.path.exists(TARGET_WORKFLOWS_DIR):
        print(f"Clearing existing links in {TARGET_WORKFLOWS_DIR}...")
        for item in os.listdir(TARGET_WORKFLOWS_DIR):
            item_path = os.path.join(TARGET_WORKFLOWS_DIR, item)
            try:
                if platform.system() == "Windows":
                    # mklink /H creates hardlinks which appear as files
                    os.unlink(item_path)
                else:
                    os.unlink(item_path)
            except Exception as e:
                print(f"  [ERROR] Could not delete {item}: {e}")
    else:
        os.makedirs(TARGET_WORKFLOWS_DIR, exist_ok=True)

    if not os.path.exists(SOURCE_WORKFLOWS_DIR):
        print(f"Source workflows directory not found at {SOURCE_WORKFLOWS_DIR}")
        return

    # 1. Identify Workflow Files and their IDs
    print("Discovering workflows...")
    workflow_links = []
    discovered_workflow_ids = {}
    
    for f in os.listdir(SOURCE_WORKFLOWS_DIR):
        if f.endswith('.md'):
            source_path = os.path.join(SOURCE_WORKFLOWS_DIR, f)
            meta = get_workflow_meta(source_path)
            if meta and meta.get('id') and meta.get('name'):
                workflow_name = meta.get('name')
                workflow_id = meta.get('id')
                target_filename = f"{workflow_name}.md"
                workflow_links.append((source_path, target_filename))
                discovered_workflow_ids[workflow_id] = target_filename
            else:
                print(f"  [SKIP] Invalid metadata for {f}")

    # 2. Link Workflows
    print(f"Linking {len(workflow_links)} workflows...")
    for source_path, target_filename in workflow_links:
        target_path = os.path.join(TARGET_WORKFLOWS_DIR, target_filename)
        abs_source = os.path.abspath(source_path)
        abs_target = os.path.abspath(target_path)
        create_symlink(abs_source, abs_target)

    # 3. Update discovery reference
    if os.path.exists(CONFIG_FILE):
        import json
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
        config["synced_workflows"] = discovered_workflow_ids
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)

if __name__ == "__main__":
    main()
