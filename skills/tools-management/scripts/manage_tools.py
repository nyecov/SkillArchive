import os
import re
from pathlib import Path

# Patterns that suggest a "Thin Wrapper" skill
THIN_WRAPPER_KEYWORDS = [
    r"wrapper around",
    r"cli for",
    r"run.*command",
    r"simple script",
    r"automates.*the.*calling.*of",
    r"interface.*to.*the.*tool"
]

def audit_archive(skills_path):
    """
    Audits the Skill Archive for categorization errors and high density.
    """
    results = {
        "thin_wrappers": [],
        "misplaced_scripts": [],
        "high_density": []
    }
    
    for skill_name in os.listdir(skills_path):
        skill_dir = os.path.join(skills_path, skill_name)
        if not os.path.isdir(skill_dir):
            continue
            
        skill_file = os.path.join(skill_dir, "SKILL.md")
        if os.path.exists(skill_file):
            with open(skill_file, "r", encoding="utf-8") as f:
                content = f.read().lower()
                
                # Check for Thin Wrapper symptoms
                for pattern in THIN_WRAPPER_KEYWORDS:
                    if re.search(pattern, content):
                        # Bypass if mechanized-override is present
                        if "mechanized-override" not in content:
                            results["thin_wrappers"].append(skill_name)
                            break
        
        # Check for script nesting and density
        scripts_dir = os.path.join(skill_dir, "scripts")
        script_count = 0
        
        # Check for scripts in the root of the skill folder (misplaced)
        for item in os.listdir(skill_dir):
            if item.endswith((".py", ".sh", ".js", ".ps1")) and item != "SKILL.md":
                results["misplaced_scripts"].append(f"{skill_name}/{item}")
        
        if os.path.exists(scripts_dir):
            script_count = len([f for f in os.listdir(scripts_dir) if os.path.isfile(os.path.join(scripts_dir, f))])
            if script_count >= 15:
                results["high_density"].append((skill_name, script_count))
                
    return results

if __name__ == "__main__":
    skills_root = Path(__file__).parent.parent.parent
    audit_results = audit_archive(skills_root)
    
    print("# Tools Management Audit Report\n")
    
    print("## 1. Thin Wrapper Candidates (Forbidden Skills)")
    if audit_results["thin_wrappers"]:
        for sw in audit_results["thin_wrappers"]:
            print(f"- [ ] `{sw}`")
    else:
        print("None found.")
        
    print("\n## 2. Misplaced Scripts (Should be in /scripts)")
    if audit_results["misplaced_scripts"]:
        for ms in audit_results["misplaced_scripts"]:
            print(f"- [ ] `{ms}`")
    else:
        print("None found.")
        
    print("\n## 3. High Density Warning (>15 scripts)")
    if audit_results["high_density"]:
        for hd, count in audit_results["high_density"]:
            print(f"- **{hd}**: {count} scripts (Consider decomposition or MCP)")
    else:
        print("None found.")
