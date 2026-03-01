import os
import re
from pathlib import Path
from dataclasses import dataclass

@dataclass
class RepairResult:
    was_repaired: bool
    status: str
    recommended_action: str = ""

def validate_and_repair_skill(file_path: Path) -> RepairResult:
    content = file_path.read_text(encoding="utf-8")
    
    # Check for unrecoverable content (missing constraints, completely blank)
    # A valid skill must have actionable constraints in its body, not just headers
    if "Constraint" not in content and "Action" not in content and len(content.strip()) < 100:
        return RepairResult(False, "unrecoverable", "invoke_story_interview")
        
    # Auto-formatting logic: Inject missing mandatory headers
    was_repaired = False
    new_content = content
    
    if "## Core Mandates" not in new_content:
        # Inject before Escalation if it exists, otherwise at the end
        if "## Escalation" in new_content:
            new_content = new_content.replace("## Escalation", "## Core Mandates\n- **Action:** \n- **Constraint:** \n- **Integration:** \n\n## Escalation")
        else:
            new_content += "\n\n## Core Mandates\n- **Action:** \n- **Constraint:** \n- **Integration:** \n"
        was_repaired = True
        
    if "## Escalation & Halting" not in new_content and " Escalat" not in new_content:
        new_content += "\n\n## Escalation & Halting\n- **Jidoka:** \n- **Hō-Ren-Sō:** \n"
        was_repaired = True

    if was_repaired:
        file_path.write_text(new_content, encoding="utf-8")
        return RepairResult(True, "auto_corrected")
        
    return RepairResult(False, "unknown")
