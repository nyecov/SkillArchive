"""
Skill Synchronization Tool
------------------------
Synchronizes source skills from /skills into the .gemini/skills directory
using OS-native symbolic links (junctions on Windows).
Enforces the sovereign discovery of active skills by the agent.

Usage: python tools/sync_skills.py
"""

import os
import sys
import json
import logging
import platform
import subprocess
from pathlib import Path
from repo_utils import setup_logging, get_frontmatter, atomic_write, PipelineLock

# Initialize standardized logging
log = setup_logging("skill_syncer")

def create_link(source: Path, target: Path):
    """
    Creates a junction point (Windows) or a symlink (Unix).
    """
    if target.exists() or target.is_symlink():
        try:
            if platform.system() == "Windows" and target.is_dir() and not target.is_symlink():
                # Junction points are directories, use rmdir via cmd
                subprocess.run(['cmd', '/c', 'rmdir', str(target)], check=True, capture_output=True)
            else:
                # Normal symlinks or files can be unlinked safely
                target.unlink()
        except Exception as e:
            log.warning(f"Could not remove existing target {target}: {e}")

    try:
        if platform.system() == "Windows":
            # /J creates a directory junction (no admin required)
            subprocess.run(['cmd', '/c', 'mklink', '/J', str(target), str(source)], check=True, capture_output=True)
        else:
            # Native Unix symlink
            target.symlink_to(source, target_is_directory=True)
        log.info(f"  [LINKED] {source.name} -> {target.name}")
    except Exception as e:
        log.error(f"  [FAILED] Failed to link {source.name}: {e}")

def sync_skills():
    """Main synchronization loop."""
    with PipelineLock():
        root_dir = Path(".")
        source_dir = root_dir / "skills"
        target_dir = root_dir / ".gemini" / "skills"
        config_file = root_dir / "local-agent-config.json"

        # KYT Safeguard: Prevent accidental deletion of system root
        if not str(target_dir).endswith(".gemini/skills") and not str(target_dir).endswith(".gemini\\skills"):
             log.critical(f"KYT Safeguard: Target directory '{target_dir}' path is suspicious. Halting.")
             sys.exit(1)

        if not source_dir.exists():
            log.error(f"Source skills directory not found at {source_dir.absolute()}")
            sys.exit(1)

        # 1. Load Config
        discovery_mode = "dynamic"
        synced_skill_ids = []
        if config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    discovery_mode = config.get("discovery_mode", "dynamic")
                    synced_skill_ids = list(config.get("synced_skills", {}).keys())
            except Exception as e:
                log.warning(f"Could not read config file {config_file}: {e}")

        # 2. Discover Skills
        log.info(f"Discovering skills (Mode: {discovery_mode})...")
        active_skills = {} # id -> meta
        
        for skill_folder in sorted(os.listdir(source_dir)):
            skill_path = source_dir / skill_folder
            if not skill_path.is_dir():
                continue
                
            skill_file = skill_path / "SKILL.md"
            data = get_frontmatter(skill_file)
            
            if data and data.get('id') and data.get('name'):
                skill_id = data['id']
                if discovery_mode == "manual" and skill_id not in synced_skill_ids:
                    continue
                active_skills[skill_id] = {
                    'name': data['name'],
                    'folder': skill_folder
                }

        # 3. Diff-Based Sync (Calculate Delta)
        if not target_dir.exists():
            log.info(f"Creating missing target directory: {target_dir}")
            target_dir.mkdir(parents=True, exist_ok=True)
            existing_links = set()
        else:
            existing_links = set(os.listdir(target_dir))
            existing_links.discard(".gemini") # Ignore internal structures if they exist

        desired_links = {info['name'] for info in active_skills.values()}
        
        links_to_remove = existing_links - desired_links
        links_to_create = desired_links - existing_links

        # 4. Clean Stale Links
        if links_to_remove:
            log.info(f"Removing {len(links_to_remove)} stale skills...")
            for item in links_to_remove:
                item_path = target_dir / item
                try:
                    if platform.system() == "Windows" and item_path.is_dir() and not item_path.is_symlink():
                        subprocess.run(['cmd', '/c', 'rmdir', str(item_path)], check=True, capture_output=True)
                    else:
                        item_path.unlink()
                    log.info(f"  [REMOVED] {item}")
                except Exception as e:
                    log.warning(f"Failed to clear {item}: {e}")

        # 5. Link Active Skills
        if links_to_create:
            log.info(f"Linking {len(links_to_create)} new skills...")
            for sid, info in active_skills.items():
                if info['name'] in links_to_create:
                    src = (source_dir / info['folder']).resolve()
                    dst = (target_dir / info['name']).resolve()
                    create_link(src, dst)
        else:
            log.info("All skills are already synchronized.")

        # 5. Update Config for Dynamic Discovery
        if discovery_mode == "dynamic" and config_file.exists():
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                config["synced_skills"] = {sid: info['name'] for sid, info in active_skills.items()}
                atomic_write(config_file, json.dumps(config, indent=2))
            except Exception as e:
                log.error(f"Failed to update config discovery mapping: {e}")

    log.info("Skill synchronization complete.")

if __name__ == "__main__":
    try:
        sync_skills()
    except Exception as e:
        log.critical(f"Unhandled exception during skill sync: {e}", exc_info=True)
        sys.exit(1)
