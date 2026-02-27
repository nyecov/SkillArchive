import os
import yaml
import re
from pathlib import Path

SKILLS_DIR = Path("skills")
README_PATH = Path("README.md")

def parse_skill_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Extract frontmatter between ---
    meta = {}
    fm_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if fm_match:
        try:
            meta = yaml.safe_load(fm_match.group(1))
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in {file_path}: {e}")

    # Extract H1 title
    title_match = re.search(r'^#\s+(.*)', content, re.MULTILINE)
    if title_match:
        meta['display_name'] = title_match.group(1).strip()
    else:
        meta['display_name'] = meta.get('name', 'Unknown Skill')
        
    return meta

def main():
    if not SKILLS_DIR.exists():
        print("Skills directory not found!")
        return

    skills = []
    
    # Collect all skill data
    for skill_folder in sorted(os.listdir(SKILLS_DIR)):
        skill_file = SKILLS_DIR / skill_folder / "SKILL.md"
        if skill_file.is_file():
            meta = parse_skill_file(skill_file)
            if meta:
                meta['folder'] = skill_folder
                meta['path'] = f"skills/{skill_folder}/SKILL.md"
                # Ensure tags exist as list
                if 'tags' not in meta or not meta['tags']:
                    meta['tags'] = []
                elif isinstance(meta['tags'], str):
                    meta['tags'] = [t.strip() for t in meta['tags'].split(',')]
                
                if 'category' not in meta:
                    meta['category'] = 'Uncategorized'
                    
                skills.append(meta)

    # Group by Category
    from collections import defaultdict
    grouped_skills = defaultdict(list)

    # Dictionary of emojis for categories
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

    # Generate Markdown Content
    md_lines = [
        "# 📚 Skill Archive",
        "",
        "The authoritative index of methodologies, cognitive frameworks, and architectural protocols for agentic workflows.",
        "",
        "## 📂 Repository Structure",
        "",
        "| Directory | Purpose |",
        "|-----------|---------|",
        "| `skills/` | High-level cognitive methodologies and tactical frameworks (Markdown + YAML frontmatter). |",
        "| `tools/` | Low-level, standalone execution scripts (Bash/Python). |",
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
            # Clean up description (remove newlines, escape pipes if any)
            desc = str(skill.get('description', '')).strip().replace('\n', ' ').replace('|', '\\|')
            
            # Truncate long descriptions for table readability
            if len(desc) > 120:
                desc = desc[:117] + "..."
            
            tags = skill.get('tags', [])
            tag_str = " ".join([f"`{t}`" for t in tags])
            
            md_lines.append(f"| **[{name}]({path})** | {desc} | {tag_str} |")
        md_lines.append("")

    # Add Tools Section
    tools_dir = Path("tools")
    if tools_dir.exists():
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
                    with open(desc_path, "r", encoding="utf-8") as f:
                        lines = f.readlines()
                        # try to get the first non-header line
                        for line in lines:
                            line = line.strip()
                            if line and not line.startswith('#') and not line.startswith('**'):
                                desc_text = line.replace('|', '\\|')
                                break
                
                md_lines.append(f"| **[{tool_folder}](tools/{tool_folder})** | {desc_text} |")
        md_lines.append("")

    new_readme_content = "\n".join(md_lines)
    
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme_content)
        
    print(f"Successfully generated README.md with {len(skills)} skills.")

if __name__ == "__main__":
    main()
