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
    content = file_path.read_text()
    
    # Unrecoverable logic: empty description
    if "description: \n" in content or "description:\n" in content or "description: \r\n" in content:
        return RepairResult(False, "unrecoverable", "invoke_story_interview")
        
    # Auto-formatting logic: missing leading dashes
    if content.startswith("description:"):
        fixed_content = "---\n" + content
        if "\n---" not in fixed_content:
            fixed_content = fixed_content.replace("\n#", "\n---\n#", 1)
        file_path.write_text(fixed_content)
        return RepairResult(True, "auto_corrected")
        
    return RepairResult(False, "unknown")
