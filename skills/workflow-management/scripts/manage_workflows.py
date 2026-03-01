import os
import re
from pathlib import Path
from dataclasses import dataclass

@dataclass
class RepairResult:
    was_repaired: bool
    status: str
    recommended_action: str = ""

def validate_and_repair_workflow(file_path: Path) -> RepairResult:
    content = file_path.read_text(encoding="utf-8")
    
    # Unrecoverable logic: Skill Rot check
    if "Action:" in content or "Constraint:" in content:
        return RepairResult(False, "unrecoverable", "invoke_story_interview")
        
    # Unrecoverable logic: empty description
    if "description: \n" in content or "description:\n" in content or "description: \r\n" in content:
        return RepairResult(False, "unrecoverable", "invoke_story_interview")
        
    was_repaired = False
    fixed_content = content
    # Auto-formatting logic: missing leading dashes
    if fixed_content.startswith("description:"):
        fixed_content = "---\n" + fixed_content
        if "\n---" not in fixed_content:
            fixed_content = fixed_content.replace("\n#", "\n---\n#", 1)
        file_path.write_text(fixed_content, encoding="utf-8")
        was_repaired = True
        
    # Check for numbered procedural steps
    has_numbered_steps = bool(re.search(r"^\d+\.\s", fixed_content, re.MULTILINE))
    
    if was_repaired:
        return RepairResult(True, "auto_corrected")
    elif has_numbered_steps:
        return RepairResult(False, "validated")
        
    return RepairResult(False, "unknown")
