"""
README Generator Tool
--------------------
Automatically generates the root README.md by scanning all skills, 
workflows, and tools. Groups skills by category and provides 
an indexed table for high-level repository discovery.

Usage: python tools/generate_readme.py
"""

import os
import sys
import logging
import re
from pathlib import Path
from collections import defaultdict
from repo_utils import setup_logging, get_frontmatter, atomic_write

# Initialize standardized logging
log = setup_logging("readme_generator")

def get_display_name(file_path: Path, meta: dict) -> str:
    """Extracts H1 title or falls back to name from meta."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
        if title_match:
            return title_match.group(1).strip()
    except Exception:
        pass
    return meta.get('name', file_path.stem.replace('-', ' ').title())

def generate_readme():
    """Main README generation logic."""
    skills_dir = Path("skills")
    workflows_dir = Path("workflows")
    tools_dir = Path("tools")
    readme_path = Path("README.md")

    if not skills_dir.exists():
        log.error("Skills directory not found!")
        sys.exit(1)

    skills = []
    log.info("Collecting skill metadata...")
    
    for skill_folder in sorted(os.listdir(skills_dir)):
        skill_file = skills_dir / skill_folder / "SKILL.md"
        if skill_file.is_file():
            meta = get_frontmatter(skill_file)
            if meta:
                meta['folder'] = skill_folder
                meta['path'] = f"skills/{skill_folder}/SKILL.md"
                meta['display_name'] = get_display_name(skill_file, meta)
                
                # Normalize tags
                tags = meta.get('tags', [])
                if isinstance(tags, str):
                    tags = [t.strip() for t in tags.split(',')]
                meta['tags'] = tags if isinstance(tags, list) else []
                
                if 'category' not in meta:
                    meta['category'] = 'Uncategorized'
                    
                skills.append(meta)

    # Group by Category
    grouped_skills = defaultdict(list)
    category_emojis = {
        'Architecture': '🏗️',
        'Cognition': '🧠',
        'Engineering': '⚙️',
        'Meta': '🔄',
        'Methodology': '📐',
        'Safety': '🛡️'
    }

    for skill in skills:
        cat = str(skill.get('category', 'Uncategorized')).title()
        grouped_skills[cat].append(skill)

    # Start building Markdown
    md_lines = [
        "# 📚 Skill Archive",
        "",
        "A comprehensive library of AI agent skills and cognitive frameworks, structurally organized around Lean manufacturing, Kaizen continuous improvement, and Toyota Production System (TPS) methodologies.",
        "",
        "## 📂 Repository Structure",
        "",
        "| Directory | Purpose |",
        "|-----------|---------|",
        "| `skills/` | High-level cognitive methodologies and tactical frameworks (Markdown + YAML frontmatter). |",
        "| `tools/` | Low-level, standalone execution scripts (Bash/Python). |",
        "| `workflows/`| Multi-step protocols for complex agent tasks. |",
        "| `templates/`| Standardized formatting templates for new skills. |",
        "",
        "## 📋 Skill Index",
        ""
    ]

    for category in sorted(grouped_skills.keys()):
        emoji = category_emojis.get(category, '📌')
        md_lines.append(f"### {emoji} {category}")
        md_lines.append("")
        md_lines.append("| Skill | Description | Tags |")
        md_lines.append("|-------|-------------|------|")
        
        for skill in sorted(grouped_skills[category], key=lambda x: x.get('display_name', '')):
            name = skill.get('display_name', 'Unknown Skill')
            path = skill['path']
            desc = str(skill.get('description', '')).strip().replace('\n', ' ').replace('|', '\\|')
            if len(desc) > 120:
                desc = desc[:117] + "..."
            
            tag_str = " ".join([f"`{t}`" for t in skill.get('tags', [])])
            md_lines.append(f"| **[{name}]({path})** | {desc} | {tag_str} |")
        md_lines.append("")

    # Workflow Index
    if workflows_dir.exists():
        log.info("Collecting workflow metadata...")
        workflows = []
        for wf_file in sorted(os.listdir(workflows_dir)):
            if wf_file.endswith(".md"):
                wf_path = workflows_dir / wf_file
                meta = get_frontmatter(wf_path)
                if meta:
                    meta['path'] = f"workflows/{wf_file}"
                    meta['display_name'] = get_display_name(wf_path, meta)
                    workflows.append(meta)

        if workflows:
            md_lines.append("## 📋 Workflow Index")
            md_lines.append("")
            md_lines.append("| Workflow | Description |")
            md_lines.append("|----------|-------------|")
            for wf in workflows:
                name = wf.get('display_name', wf['path'])
                path = wf['path']
                desc = str(wf.get('description', '')).strip().replace('\n', ' ').replace('|', '\\|')
                if len(desc) > 120:
                    desc = desc[:117] + "..."
                md_lines.append(f"| **[{name}]({path})** | {desc} |")
            md_lines.append("")

    # Tools Index
    if tools_dir.exists():
        log.info("Collecting tools documentation...")
        md_lines.append("## 🛠️ Tools Index")
        md_lines.append("")
        md_lines.append("> Standalone, low-level execution scripts. See the [Tools Management Strategy](skills/tools-management/SKILL.md).")
        md_lines.append("")
        md_lines.append("| Tool | Description |")
        md_lines.append("|------|-------------|")
        
        for tool_folder in sorted(os.listdir(tools_dir)):
            tool_path = tools_dir / tool_folder
            if tool_path.is_dir():
                desc_path = tool_path / "description.md"
                desc_text = ""
                if desc_path.exists():
                    try:
                        with open(desc_path, "r", encoding="utf-8") as f:
                            for line in f:
                                line = line.strip()
                                if line and not line.startswith('#') and not line.startswith('**'):
                                    desc_text = line.replace('|', '\\|')
                                    break
                    except Exception:
                        pass
                
                md_lines.append(f"| **[{tool_folder}](tools/{tool_folder})** | {desc_text} |")
        md_lines.append("")

    # Atomic Commit to README.md
    log.info(f"Writing atomic update to {readme_path}...")
    atomic_write(readme_path, "\n".join(md_lines))
    log.info("README generation successful.")

if __name__ == "__main__":
    try:
        generate_readme()
    except Exception as e:
        log.critical(f"Unhandled exception during README generation: {e}", exc_info=True)
        sys.exit(1)
