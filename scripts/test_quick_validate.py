#!/usr/bin/env python3
"""
test_quick_validate.py — Unit tests for meta/skill-creator/scripts/quick_validate.py

Tests validate_skill() with valid skills, missing fields, invalid names,
long descriptions, and edge cases.
"""
import os
import sys
import tempfile
import shutil
import unittest

SKILL_CREATOR_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "meta", "skill-creator")
sys.path.insert(0, SKILL_CREATOR_ROOT)
from scripts.quick_validate import validate_skill
from pathlib import Path


class TestValidateSkill(unittest.TestCase):
    """Tests for validate_skill() — skill directory validation."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _create_skill(self, content, skill_name="test-skill"):
        skill_dir = Path(self.tmpdir) / skill_name
        skill_dir.mkdir(exist_ok=True)
        (skill_dir / "SKILL.md").write_text(content)
        return skill_dir

    def test_valid_skill_passes(self):
        path = self._create_skill(
            "---\nname: my-skill\ndescription: A valid skill\n---\nInstructions."
        )
        valid, msg = validate_skill(path)
        self.assertTrue(valid)

    def test_missing_skill_md(self):
        empty_dir = Path(self.tmpdir) / "no-skill"
        empty_dir.mkdir()
        valid, msg = validate_skill(empty_dir)
        self.assertFalse(valid)
        self.assertIn("SKILL.md not found", msg)

    def test_missing_frontmatter_opening(self):
        path = self._create_skill("name: bad\ndescription: No delimiters\n---\nBody.")
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("No YAML frontmatter", msg)

    def test_missing_closing_delimiter(self):
        path = self._create_skill("---\nname: bad\ndescription: No closing\nBody.")
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("Invalid frontmatter", msg)

    def test_missing_name_field(self):
        path = self._create_skill("---\ndescription: Has no name\n---\nBody.")
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("Missing 'name'", msg)

    def test_missing_description_field(self):
        path = self._create_skill("---\nname: skill\n---\nBody.")
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("Missing 'description'", msg)

    def test_name_not_kebab_case(self):
        path = self._create_skill("---\nname: MySkill\ndescription: Bad name\n---\nBody.")
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("kebab-case", msg)

    def test_name_with_uppercase(self):
        path = self._create_skill("---\nname: My-Skill\ndescription: Bad name\n---\nBody.")
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("kebab-case", msg)

    def test_name_starts_with_hyphen(self):
        path = self._create_skill("---\nname: -bad-name\ndescription: Starts with hyphen\n---\nBody.")
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("cannot start/end with hyphen", msg)

    def test_name_ends_with_hyphen(self):
        path = self._create_skill("---\nname: bad-name-\ndescription: Ends with hyphen\n---\nBody.")
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("cannot start/end with hyphen", msg)

    def test_name_consecutive_hyphens(self):
        path = self._create_skill("---\nname: bad--name\ndescription: Double hyphens\n---\nBody.")
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("consecutive hyphens", msg)

    def test_name_too_long(self):
        long_name = "a" * 65
        path = self._create_skill(f"---\nname: {long_name}\ndescription: Too long\n---\nBody.")
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("too long", msg)

    def test_name_max_length_passes(self):
        max_name = "a" * 64
        path = self._create_skill(f"---\nname: {max_name}\ndescription: Max length\n---\nBody.")
        valid, msg = validate_skill(path)
        self.assertTrue(valid)

    def test_description_with_angle_brackets(self):
        path = self._create_skill("---\nname: skill\ndescription: Has <html> tags\n---\nBody.")
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("angle brackets", msg)

    def test_description_too_long(self):
        long_desc = "x" * 1025
        path = self._create_skill(f"---\nname: skill\ndescription: {long_desc}\n---\nBody.")
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("too long", msg)

    def test_description_max_length_passes(self):
        max_desc = "x" * 1024
        path = self._create_skill(f"---\nname: skill\ndescription: {max_desc}\n---\nBody.")
        valid, msg = validate_skill(path)
        self.assertTrue(valid)

    def test_unexpected_frontmatter_key(self):
        path = self._create_skill(
            "---\nname: skill\ndescription: Test\nunknown-key: value\n---\nBody."
        )
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("Unexpected key", msg)

    def test_allowed_optional_fields_pass(self):
        path = self._create_skill(
            "---\nname: skill\ndescription: Test\nlicense: MIT\ncompatibility: any\n---\nBody."
        )
        valid, msg = validate_skill(path)
        self.assertTrue(valid)

    def test_compatibility_too_long(self):
        long_compat = "x" * 501
        path = self._create_skill(
            f"---\nname: skill\ndescription: Test\ncompatibility: {long_compat}\n---\nBody."
        )
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("too long", msg)

    def test_name_with_digits(self):
        path = self._create_skill("---\nname: skill-2\ndescription: With digits\n---\nBody.")
        valid, msg = validate_skill(path)
        self.assertTrue(valid)

    def test_invalid_yaml(self):
        path = self._create_skill("---\nname: skill\n  bad indent:\n    broken\n---\nBody.")
        valid, msg = validate_skill(path)
        # yaml.safe_load may or may not error on this, but validation should handle it
        # Either it fails YAML parse or passes with unexpected structure
        # The key thing is it doesn't crash
        self.assertIsInstance(valid, bool)

    def test_string_as_path(self):
        """validate_skill accepts string paths, not just Path objects."""
        skill_dir = Path(self.tmpdir) / "string-path"
        skill_dir.mkdir()
        (skill_dir / "SKILL.md").write_text(
            "---\nname: skill\ndescription: Test\n---\nBody."
        )
        valid, msg = validate_skill(str(skill_dir))
        self.assertTrue(valid)


class TestValidateSkillEdgeCases(unittest.TestCase):
    """Edge case tests for validate_skill()."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _create_skill(self, content, skill_name="edge-skill"):
        skill_dir = Path(self.tmpdir) / skill_name
        skill_dir.mkdir(exist_ok=True)
        (skill_dir / "SKILL.md").write_text(content)
        return skill_dir

    def test_empty_file(self):
        path = self._create_skill("")
        valid, msg = validate_skill(path)
        self.assertFalse(valid)

    def test_only_delimiters(self):
        path = self._create_skill("---\n---")
        valid, msg = validate_skill(path)
        self.assertFalse(valid)  # Missing name and description

    def test_name_is_integer(self):
        path = self._create_skill("---\nname: 123\ndescription: Numeric name\n---\nBody.")
        valid, msg = validate_skill(path)
        # YAML parses 123 as int, not string
        self.assertFalse(valid)
        self.assertIn("string", msg)

    def test_description_is_list(self):
        path = self._create_skill(
            "---\nname: skill\ndescription:\n  - item1\n  - item2\n---\nBody."
        )
        valid, msg = validate_skill(path)
        self.assertFalse(valid)
        self.assertIn("string", msg)


if __name__ == "__main__":
    unittest.main()
