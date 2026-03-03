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

    # 1. Prepare Target Directory
    if not target_dir.exists():
        log.info(f"Creating missing target directory: {target_dir}")
        target_dir.mkdir(parents=True, exist_ok=True)
    else:
        log.info(f"Cleaning existing links in {target_dir}...")
        for item in os.listdir(target_dir):
            item_path = target_dir / item
            try:
                item_path.unlink()
            except Exception as e:
                log.warning(f"Failed to clear {item}: {e}")

    # 2. Load Config
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

    # 3. Discover Workflows
    log.info(f"Discovering workflows (Mode: {discovery_mode})...")
    active_workflows = {} # id -> target_filename
    workflow_links = [] # list of (source, target_filename)
    
    for f in sorted(os.listdir(source_dir)):
        if f.endswith('.md'):
            source_path = source_dir / f
            data = get_frontmatter(source_path)
            
            if data and data.get('id') and data.get('name'):
                workflow_id = data['id']
                if discovery_mode == "manual" and workflow_id not in synced_workflow_ids:
                    continue
                
                target_filename = f"{data['name']}.md"
                workflow_links.append((source_path, target_filename))
                active_workflows[workflow_id] = target_filename
            else:
                log.warning(f"  [SKIP] Invalid metadata in {f}")

    # 4. Link Active Workflows
    log.info(f"Linking {len(workflow_links)} active workflows...")
    for src, target_filename in workflow_links:
        dst = (target_dir / target_filename).resolve()
        create_link(src.resolve(), dst)

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
