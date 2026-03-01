import os
import shutil
import platform
import subprocess

# Paths
ROOT_DIR = "."
SOURCE_WORKFLOWS_DIR = os.path.join(ROOT_DIR, "workflows")
TARGET_WORKFLOWS_DIR = os.path.join(ROOT_DIR, ".gemini", "workflows")

def create_symlink(source, target):
    """
    Creates a symbolic link for a file.
    """
    if os.path.exists(target):
        return # Already linked
    try:
        if platform.system() == "Windows":
            # For files on Windows, use mklink /H for hardlinks to avoid Admin issues
            subprocess.run(['cmd', '/c', 'mklink', '/H', target, source], check=True, capture_output=True)
        else:
            os.symlink(source, target)
        print(f"  [OK] Linked: {os.path.basename(source)}")
    except Exception as e:
        print(f"  [ERROR] Failed to link {os.path.basename(source)}: {e}")

def main():
    # KYT Safeguard: Prevent accidental directory wipes
    # Ensure that TARGET_WORKFLOWS_DIR unambiguously points to .gemini/workflows
    safe_target = TARGET_WORKFLOWS_DIR.replace('\\', '/')
    if not safe_target.endswith('.gemini/workflows') and not safe_target.endswith('.gemini/workflows/'):
        raise ValueError(f"KYT Safeguard Error: Target directory '{TARGET_WORKFLOWS_DIR}' is unsafe. It must explicitly target '.gemini/workflows' to prevent accidental deletion of source files.")

    # Clear target directory
    if os.path.exists(TARGET_WORKFLOWS_DIR):
        print(f"Clearing existing links in {TARGET_WORKFLOWS_DIR}...")
        for item in os.listdir(TARGET_WORKFLOWS_DIR):
            item_path = os.path.join(TARGET_WORKFLOWS_DIR, item)
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
        os.makedirs(TARGET_WORKFLOWS_DIR, exist_ok=True)

    if not os.path.exists(SOURCE_WORKFLOWS_DIR):
        print(f"Source workflows directory not found at {SOURCE_WORKFLOWS_DIR}")
        return

    # 1. Identify Workflow Files
    workflows = [f for f in os.listdir(SOURCE_WORKFLOWS_DIR) if f.endswith('.md')]

    # 2. Create Links
    print(f"Linking {len(workflows)} workflows...")
    for workflow in sorted(workflows):
        source_path = os.path.join(SOURCE_WORKFLOWS_DIR, workflow)
        target_path = os.path.join(TARGET_WORKFLOWS_DIR, workflow)
        # We need absolute paths for mklink to work reliably if the target is in a different directory depth
        abs_source = os.path.abspath(source_path)
        abs_target = os.path.abspath(target_path)
        create_symlink(abs_source, abs_target)

if __name__ == "__main__":
    main()
