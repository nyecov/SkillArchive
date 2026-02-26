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

    # Group by Category (or you could group by Primary Tag)
    # We will group by category, then list tags.
    from collections import defaultdict
    grouped_skills = defaultdict(list)
    for skill in skills:
        cat = str(skill.get('category', 'Uncategorized')).title()
        grouped_skills[cat].append(skill)

    # Generate Markdown Content
    md_lines = [
        "# Skill Archive",
        "",
        "Management and storage for AI agent skills.",
        "",
        "## Structure",
        "- `skills/`: Markdown skill files with YAML frontmatter. Contains high-level cognitive methodologies.",
        "- `tools/`: Low-level standalone execution scripts (Bash/Python).",
        "- `templates/`: Standard formats for new skills.",
        "",
        "## Rules",
        "- All paths within the project MUST be relative.",
        "- Absolute paths are ONLY allowed if they point to external repositories.",
        "",
        "## 📚 Skill Directory",
        ""
    ]

    for category in sorted(grouped_skills.keys()):
        md_lines.append(f"### {category}")
        md_lines.append("")
        for skill in sorted(grouped_skills[category], key=lambda x: x.get('display_name', '')):
            name = skill.get('display_name', 'Unknown Skill')
            path = skill['path']
            desc = str(skill.get('description', '')).strip().replace('\n', ' ')
            # Truncate long descriptions slightly for readability
            if len(desc) > 150:
                desc = desc[:147] + "..."
            
            tags = skill.get('tags', [])
            tag_str = " ".join([f"`#{t}`" for t in tags])
            
            md_lines.append(f"- **[{name}]({path})**")
            if desc:
                md_lines.append(f"  > {desc}")
            if tag_str:
                md_lines.append(f"  > *Tags:* {tag_str}")
            md_lines.append("")

    # Add Tools Section
    tools_dir = Path("tools")
    if tools_dir.exists():
        md_lines.append("## 🛠️ Tools Directory")
        md_lines.append("> Standalone, low-level execution scripts. See [Tools Management Strategy](skills/tools-management/SKILL.md).")
        md_lines.append("")
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
                                desc_text = line
                                break
                
                md_lines.append(f"- **[{tool_folder}](tools/{tool_folder})**")
                if desc_text:
                    md_lines.append(f"  > {desc_text}")
                md_lines.append("")

    new_readme_content = "\n".join(md_lines)
    
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_readme_content)
        
    print(f"Successfully generated README.md with {len(skills)} skills.")

if __name__ == "__main__":
    main()
