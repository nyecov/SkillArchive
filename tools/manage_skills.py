"""
Skill Management CLI Helper
---------------------------
A tool to easily add or remove skills from the local-agent-config.json
using their human-readable name, abstracting away the underlying UUIDs.

Usage:
  python tools/manage_skills.py enable <skill-name>
  python tools/manage_skills.py disable <skill-name>
  python tools/manage_skills.py list
"""

import os
import sys
import json
import argparse
from pathlib import Path
from repo_utils import get_frontmatter, atomic_write, PipelineLock

def get_all_skills():
    """Returns a dictionary mapping skill names to their UUIDs."""
    root_dir = Path(".")
    source_dir = root_dir / "skills"
    
    skills = {}
    if not source_dir.exists():
        return skills
        
    for skill_folder in os.listdir(source_dir):
        skill_path = source_dir / skill_folder
        if not skill_path.is_dir() or skill_folder == ".gemini":
            continue
            
        skill_file = skill_path / "SKILL.md"
        data = get_frontmatter(skill_file)
        
        if data and data.get('id') and data.get('name'):
            skills[data['name']] = data['id']
            
    return skills

def load_config():
    config_file = Path("local-agent-config.json")
    if not config_file.exists():
        print("Error: local-agent-config.json not found.")
        sys.exit(1)
        
    with open(config_file, 'r', encoding='utf-8') as f:
        return json.load(f), config_file

def save_config(config, config_file):
    atomic_write(config_file, json.dumps(config, indent=2))
    print(f"✅ Updated {config_file.name}")

def enable_skill(skill_name):
    available_skills = get_all_skills()
    if skill_name not in available_skills:
        print(f"❌ Error: Skill '{skill_name}' not found in the skills/ directory.")
        sys.exit(1)
        
    skill_uuid = available_skills[skill_name]
    config, config_file = load_config()
    
    synced_skills = config.get("synced_skills", {})
    if skill_uuid in synced_skills:
        print(f"ℹ️ Skill '{skill_name}' is already enabled.")
        return
        
    synced_skills[skill_uuid] = skill_name
    config["synced_skills"] = synced_skills
    save_config(config, config_file)
    
    print(f"🔄 Run 'python tools/sync_skills.py' and '/skills reload' to apply changes.")

def disable_skill(skill_name):
    available_skills = get_all_skills()
    # We still allow disabling even if the folder is gone, as long as we can find it in config
    skill_uuid = available_skills.get(skill_name)
    
    config, config_file = load_config()
    synced_skills = config.get("synced_skills", {})
    
    # Find UUID by name if the folder was deleted
    if not skill_uuid:
        for u, n in synced_skills.items():
            if n == skill_name:
                skill_uuid = u
                break
                
    if not skill_uuid or skill_uuid not in synced_skills:
        print(f"ℹ️ Skill '{skill_name}' is not currently enabled.")
        return
        
    del synced_skills[skill_uuid]
    config["synced_skills"] = synced_skills
    save_config(config, config_file)
    
    print(f"🔄 Run 'python tools/sync_skills.py' and '/skills reload' to apply changes.")

def list_skills():
    available_skills = get_all_skills()
    config, _ = load_config()
    synced_skills = config.get("synced_skills", {})
    
    print("\n--- Skill Archive Status ---")
    for name, uuid in sorted(available_skills.items()):
        status = "✅ ENABLED" if uuid in synced_skills else "❌ DISABLED"
        print(f"{status} | {name}")
    print("----------------------------\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Manage active skills in the local-agent-config.json")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    enable_parser = subparsers.add_parser("enable", help="Enable a skill by name")
    enable_parser.add_argument("name", help="The name of the skill (e.g., jidoka)")
    
    disable_parser = subparsers.add_parser("disable", help="Disable a skill by name")
    disable_parser.add_argument("name", help="The name of the skill (e.g., jidoka)")
    
    list_parser = subparsers.add_parser("list", help="List all skills and their status")
    
    args = parser.parse_args()
    
    with PipelineLock():
        if args.command == "enable":
            enable_skill(args.name)
        elif args.command == "disable":
            disable_skill(args.name)
        elif args.command == "list":
            list_skills()