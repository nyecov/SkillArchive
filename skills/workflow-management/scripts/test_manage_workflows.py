import unittest
import os
import tempfile
from pathlib import Path

import sys

# Add the root directory to the python path to allow imports
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

try:
    import manage_workflows
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("manage_workflows", str(Path(__file__).parent / "manage_workflows.py"))
    manage_workflows = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(manage_workflows)


class TestManageWorkflows(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)
        
    def tearDown(self):
        self.test_dir.cleanup()

    def test_should_auto_correct_formatting_when_workflow_structure_is_invalid(self):
        # Arrange
        invalid_workflow = self.test_path / "bad-workflow.md"
        # Missing opening frontmatter dashes, weird spacing
        malformed_content = """description: a bad workflow
---
# Just a header
no steps
"""
        invalid_workflow.write_text(malformed_content)
        
        # Act
        # The script should detect it's missing the frontmatter boundary and fix it
        result = manage_workflows.validate_and_repair_workflow(invalid_workflow)
        
        # Assert
        self.assertTrue(result.was_repaired)
        self.assertEqual(result.status, "auto_corrected")
        
        fixed_content = invalid_workflow.read_text()
        self.assertTrue(fixed_content.startswith("---\n"))
        self.assertTrue("description: a bad workflow\n---" in fixed_content)

    def test_should_invoke_story_interview_when_workflow_logic_is_unrecoverable(self):
        # Arrange
        unrecoverable_workflow = self.test_path / "terrible-workflow.md"
        # Empty description, no steps, just garbage
        garbage_content = """---
description: 
---
garbage text with no numbered list
"""
        unrecoverable_workflow.write_text(garbage_content)
        
        # Act
        result = manage_workflows.validate_and_repair_workflow(unrecoverable_workflow)
        
        # Assert
        self.assertFalse(result.was_repaired)
        self.assertEqual(result.status, "unrecoverable")
        self.assertEqual(result.recommended_action, "invoke_story_interview")

    def test_should_return_validated_for_compliant_workflow(self):
        # Arrange
        compliant_workflow = self.test_path / "good-workflow.md"
        content = "---\ndescription: A perfectly good workflow\n---\n# Step 1\n1. Do this\n2. Do that\n"
        compliant_workflow.write_text(content, encoding="utf-8")
        
        # Act
        result = manage_workflows.validate_and_repair_workflow(compliant_workflow)
        
        # Assert
        self.assertFalse(result.was_repaired)
        self.assertEqual(result.status, "validated")

    def test_should_escalate_if_workflow_uses_skill_mandates(self):
        # Arrange
        skill_rot = self.test_path / "rot-workflow.md"
        content = "---\ndescription: A workflow with skill mandates\n---\n## Core Mandates\n- **Action:** Do something\n- **Constraint:** Stop\n"
        skill_rot.write_text(content, encoding="utf-8")
        
        # Act
        result = manage_workflows.validate_and_repair_workflow(skill_rot)
        
        # Assert
        self.assertFalse(result.was_repaired)
        self.assertEqual(result.status, "unrecoverable")
        self.assertEqual(result.recommended_action, "invoke_story_interview")

if __name__ == '__main__':
    unittest.main()
