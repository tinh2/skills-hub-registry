#!/usr/bin/env python3
"""
test_utils.py — Unit tests for meta/skill-creator/scripts/utils.py

Tests parse_skill_md() with valid frontmatter, multiline descriptions,
missing delimiters, and edge cases.
"""
import os
import sys
import tempfile
import shutil
import unittest

# Import module under test — skill-creator uses `from scripts.X` package imports
SKILL_CREATOR_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "meta", "skill-creator")
sys.path.insert(0, SKILL_CREATOR_ROOT)
from scripts.utils import parse_skill_md
from pathlib import Path


class TestParseSkillMd(unittest.TestCase):
    """Tests for parse_skill_md() — SKILL.md frontmatter parsing."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _write_skill(self, content):
        """Write a SKILL.md file and return the parent directory as Path."""
        skill_dir = Path(self.tmpdir) / "test-skill"
        skill_dir.mkdir(exist_ok=True)
        (skill_dir / "SKILL.md").write_text(content)
        return skill_dir

    def test_basic_frontmatter(self):
        path = self._write_skill(
            "---\nname: my-skill\ndescription: A helpful skill\nversion: 1\n---\nBody content."
        )
        name, desc, content = parse_skill_md(path)
        self.assertEqual(name, "my-skill")
        self.assertEqual(desc, "A helpful skill")
        self.assertIn("Body content.", content)

    def test_quoted_name(self):
        path = self._write_skill(
            '---\nname: "quoted-skill"\ndescription: Test\nversion: 1\n---\nBody.'
        )
        name, desc, _ = parse_skill_md(path)
        self.assertEqual(name, "quoted-skill")

    def test_single_quoted_name(self):
        path = self._write_skill(
            "---\nname: 'single-quoted'\ndescription: Test\nversion: 1\n---\nBody."
        )
        name, desc, _ = parse_skill_md(path)
        self.assertEqual(name, "single-quoted")

    def test_quoted_description(self):
        path = self._write_skill(
            '---\nname: skill\ndescription: "A quoted description"\nversion: 1\n---\nBody.'
        )
        _, desc, _ = parse_skill_md(path)
        self.assertEqual(desc, "A quoted description")

    def test_multiline_description_folded(self):
        content = "---\nname: skill\ndescription: >\n  This is a long\n  multiline description\nversion: 1\n---\nBody."
        path = self._write_skill(content)
        _, desc, _ = parse_skill_md(path)
        self.assertEqual(desc, "This is a long multiline description")

    def test_multiline_description_literal(self):
        content = "---\nname: skill\ndescription: |\n  Line one\n  Line two\nversion: 1\n---\nBody."
        path = self._write_skill(content)
        _, desc, _ = parse_skill_md(path)
        self.assertEqual(desc, "Line one Line two")

    def test_multiline_description_folded_strip(self):
        content = "---\nname: skill\ndescription: >-\n  Stripped folded\nversion: 1\n---\nBody."
        path = self._write_skill(content)
        _, desc, _ = parse_skill_md(path)
        self.assertEqual(desc, "Stripped folded")

    def test_multiline_description_literal_strip(self):
        content = "---\nname: skill\ndescription: |-\n  Stripped literal\nversion: 1\n---\nBody."
        path = self._write_skill(content)
        _, desc, _ = parse_skill_md(path)
        self.assertEqual(desc, "Stripped literal")

    def test_missing_opening_delimiter(self):
        path = self._write_skill("name: skill\ndescription: Test\n---\nBody.")
        with self.assertRaises(ValueError) as ctx:
            parse_skill_md(path)
        self.assertIn("no opening ---", str(ctx.exception))

    def test_missing_closing_delimiter(self):
        path = self._write_skill("---\nname: skill\ndescription: Test\nBody without closing.")
        with self.assertRaises(ValueError) as ctx:
            parse_skill_md(path)
        self.assertIn("no closing ---", str(ctx.exception))

    def test_empty_name_returns_empty_string(self):
        path = self._write_skill("---\ndescription: Has no name field\nversion: 1\n---\nBody.")
        name, _, _ = parse_skill_md(path)
        self.assertEqual(name, "")

    def test_empty_description_returns_empty_string(self):
        path = self._write_skill("---\nname: skill\nversion: 1\n---\nBody.")
        _, desc, _ = parse_skill_md(path)
        self.assertEqual(desc, "")

    def test_returns_full_content(self):
        full = "---\nname: skill\ndescription: Test\nversion: 1\n---\nFull body here."
        path = self._write_skill(full)
        _, _, content = parse_skill_md(path)
        self.assertEqual(content, full)

    def test_extra_frontmatter_fields_ignored(self):
        path = self._write_skill(
            "---\nname: skill\ndescription: Test\nversion: 1\ncategory: build\nlicense: MIT\n---\nBody."
        )
        name, desc, _ = parse_skill_md(path)
        self.assertEqual(name, "skill")
        self.assertEqual(desc, "Test")

    def test_skill_md_not_found(self):
        empty_dir = Path(self.tmpdir) / "empty"
        empty_dir.mkdir()
        with self.assertRaises(FileNotFoundError):
            parse_skill_md(empty_dir)

    def test_multiline_with_tab_indent(self):
        content = "---\nname: skill\ndescription: >\n\tTab indented line\nversion: 1\n---\nBody."
        path = self._write_skill(content)
        _, desc, _ = parse_skill_md(path)
        self.assertEqual(desc, "Tab indented line")


if __name__ == "__main__":
    unittest.main()
