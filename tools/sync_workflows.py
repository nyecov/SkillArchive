"""
Workflow Synchronization Tool
----------------------------
Synchronizes source workflows from /workflows into the .gemini/workflows directory
using OS-native hard links (Windows) or symbolic links (Unix).

Usage: python tools/sync_workflows.py
"""

import os
import sys
import json
import logging
import platform
import subprocess
from pathlib import Path
from repo_utils import setup_logging, get_frontmatter, atomic_write

# Initialize standardized logging
log = setup_logging("workflow_syncer")

def create_link(source: Path, target: Path):
    """
    Creates a hard link (Windows) or a symlink (Unix).
    """
    if target.exists() or target.is_symlink():
        try:
            target.unlink()
        except Exception as e:
            log.warning(f"Could not remove existing target {target}: {e}")

    try:
        if platform.system() == "Windows":
            # Using 'mklink /H' for hard links which does not require admin rights.
            subprocess.run(['cmd', '/c', 'mklink', '/H', str(target), str(source)], check=True, capture_output=True)
        else:
            os.symlink(source, target)
        log.info(f"  [LINKED] {source.name} -> {target.name}")
    except Exception as e:
        log.error(f"  [FAILED] Failed to link {source.name}: {e}")

def sync_workflows():
    """Main synchronization loop."""
    root_dir = Path(".")
    source_dir = root_dir / "workflows"
    target_dir = root_dir / ".gemini" / "workflows"
    config_file = root_dir / "local-agent-config.json"

    # KYT Safeguard
    if not str(target_dir).endswith(".gemini/workflows") and not str(target_dir).endswith(".gemini\\workflows"):
        log.critical(f"KYT Safeguard: Target directory '{target_dir}' path is suspicious. Halting.")
        sys.exit(1)

    if not source_dir.exists():
        log.error(f"Source workflows directory not found at {source_dir.absolute()}")
        sys.exit(1)

    # 1. Load Config
    discovery_mode = "dynamic"
    synced_workflow_ids = []
    if config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                discovery_mode = config.get("discovery_mode", "dynamic")
                synced_workflow_ids = list(config.get("synced_workflows", {}).keys())
        except Exception as e:
            log.warning(f"Could not read config file {config_file}: {e}")

    # 2. Discover Workflows
    log.info(f"Discovering workflows (Mode: {discovery_mode})...")
    active_workflows = {} # id -> target_filename
    workflow_links = {} # target_filename -> source_path
    
    for f in sorted(os.listdir(source_dir)):
        if f.endswith('.md'):
            source_path = source_dir / f
            data = get_frontmatter(source_path)
            
            if data and data.get('id') and data.get('name'):
                workflow_id = data['id']
                if discovery_mode == "manual" and workflow_id not in synced_workflow_ids:
                    continue
                
                target_filename = f"{data['name']}.md"
                workflow_links[target_filename] = source_path
                active_workflows[workflow_id] = target_filename
            else:
                log.warning(f"  [SKIP] Invalid metadata in {f}")

    # 3. Diff-Based Sync (Calculate Delta)
    if not target_dir.exists():
        log.info(f"Creating missing target directory: {target_dir}")
        target_dir.mkdir(parents=True, exist_ok=True)
        existing_links = set()
    else:
        existing_links = set(os.listdir(target_dir))
        existing_links.discard(".gemini") # Ignore internal structures if they exist

    desired_links = set(workflow_links.keys())
    
    links_to_remove = existing_links - desired_links
    links_to_create = desired_links - existing_links

    # 4. Clean Stale Links
    if links_to_remove:
        log.info(f"Removing {len(links_to_remove)} stale workflows...")
        for item in links_to_remove:
            item_path = target_dir / item
            try:
                item_path.unlink()
                log.info(f"  [REMOVED] {item}")
            except Exception as e:
                log.warning(f"Failed to clear {item}: {e}")

    # 5. Link Active Workflows
    if links_to_create:
        log.info(f"Linking {len(links_to_create)} new workflows...")
        for target_filename in links_to_create:
            src = workflow_links[target_filename]
            dst = (target_dir / target_filename).resolve()
            create_link(src.resolve(), dst)
    else:
        log.info("All workflows are already synchronized.")

    # 5. Update Config
    if discovery_mode == "dynamic" and config_file.exists():
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            config["synced_workflows"] = active_workflows
            atomic_write(config_file, json.dumps(config, indent=2))
        except Exception as e:
            log.error(f"Failed to update config discovery mapping: {e}")

    log.info("Workflow synchronization complete.")

if __name__ == "__main__":
    try:
        sync_workflows()
    except Exception as e:
        log.critical(f"Unhandled exception during workflow sync: {e}", exc_info=True)
        sys.exit(1)
