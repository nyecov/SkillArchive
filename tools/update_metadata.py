"""
Metadata Discovery Tool
----------------------
Scans all skills to extract categories, tags, and levels.
Updates 'local-agent-config.json' with a reference block for discovery.

Usage: python tools/update_metadata.py
"""

import os
import sys
import json
import logging
from pathlib import Path
from repo_utils import setup_logging, get_frontmatter, atomic_write

# Initialize standardized logging
log = setup_logging("metadata_updater")

def update_metadata():
    """Scans repository and updates the local agent configuration."""
    config_path = Path("local-agent-config.json")
    skills_dir = Path("skills")
    
    all_categories = set()
    all_tags = set()
    all_levels = set()

    if not skills_dir.exists():
        log.error(f"Skills directory not found at {skills_dir.absolute()}")
        sys.exit(1)

    log.info("Scanning skills for discovery metadata...")
    
    for skill_folder in sorted(os.listdir(skills_dir)):
        skill_file = skills_dir / skill_folder / "SKILL.md"
        if not skill_file.exists():
            continue

        data = get_frontmatter(skill_file)
        if data:
            # Extract data
            category = data.get('category')
            if category:
                all_categories.add(category)
            
            level = data.get('level')
            if level:
                all_levels.add(level)
            
            tags = data.get('tags', [])
            if isinstance(tags, list):
                for tag in tags:
                    all_tags.add(tag)
            elif isinstance(tags, str):
                for tag in [t.strip() for t in tags.split(',')]:
                    all_tags.add(tag)

    # Load existing config
    config = {}
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            log.warning(f"Malformed JSON in {config_path}. Initializing new config.")
            config = {}
    else:
        log.info(f"Creating new {config_path}")

    # Add the "_discovery_reference" metadata section
    config["_discovery_reference"] = {
        "HELP": "This section is auto-generated and serves as a reference for available options.",
        "available_categories": sorted(list(all_categories)),
        "available_tags": sorted(list(all_tags)),
        "available_levels": sorted(list(all_levels))
    }

    # Save back to config file atomically
    log.info(f"Updating {config_path} with {len(all_categories)} categories and {len(all_tags)} tags...")
    atomic_write(config_path, json.dumps(config, indent=2))
    log.info("Metadata synchronization successful.")

if __name__ == "__main__":
    try:
        update_metadata()
    except Exception as e:
        log.critical(f"Unhandled exception during metadata update: {e}", exc_info=True)
        sys.exit(1)
