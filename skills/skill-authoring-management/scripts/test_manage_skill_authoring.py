import unittest
import os
import tempfile
from pathlib import Path
import sys

# Add the root directory to the python path to allow imports
sys.path.append(str(Path(__file__).parent.parent.parent.parent))

try:
    import manage_skill_authoring
except ImportError:
    import importlib.util
    spec = importlib.util.spec_from_file_location("manage_skill_authoring", str(Path(__file__).parent / "manage_skill_authoring.py"))
    manage_skill_authoring = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(manage_skill_authoring)

class TestManageSkillAuthoring(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)
        
    def tearDown(self):
        self.test_dir.cleanup()

    def test_should_auto_inject_missing_headers_like_core_mandates(self):
        # Arrange
        invalid_skill = self.test_path / "bad-skill.md"
        # Has frontmatter but missing Core Mandates header
        malformed_content = """---
name: bad-skill
description: 'A mock skill that has a description and enough text to avoid the unrecoverable garbage filter, but is missing headers.'
---
# Bad Skill
Just some text here that explains the skill vaguely but doesn't have any mandates.
"""
        invalid_skill.write_text(malformed_content, encoding="utf-8")
        
        # Act
        result = manage_skill_authoring.validate_and_repair_skill(invalid_skill)
        
        # Assert
        self.assertTrue(result.was_repaired)
        self.assertEqual(result.status, "auto_corrected")
        
        fixed_content = invalid_skill.read_text(encoding="utf-8")
        self.assertIn("## Core Mandates", fixed_content)
        self.assertIn("## Escalation & Halting", fixed_content)

    def test_should_escalate_to_story_interview_when_constraints_are_missing(self):
        # Arrange
        unrecoverable_skill = self.test_path / "terrible-skill.md"
        # Missing frontmatter, empty body, no constraints
        garbage_content = """
# Just a header
"""
        unrecoverable_skill.write_text(garbage_content, encoding="utf-8")
        
        # Act
        result = manage_skill_authoring.validate_and_repair_skill(unrecoverable_skill)
        
        # Assert
        self.assertFalse(result.was_repaired)
        self.assertEqual(result.status, "unrecoverable")
        self.assertEqual(result.recommended_action, "invoke_story_interview")

if __name__ == '__main__':
    unittest.main()
