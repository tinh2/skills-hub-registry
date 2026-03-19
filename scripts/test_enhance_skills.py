#!/usr/bin/env python3
"""
test_enhance_skills.py — Unit tests for enhance-skills.py

Tests all pure functions: bump_version, has_section, find_output_section,
find_end_position, get_category, get_skill_name, and process_skill.
"""
import os
import sys
import tempfile
import shutil
import unittest

# Import module under test
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib

enhance = importlib.import_module("enhance-skills")


class TestBumpVersion(unittest.TestCase):
    """Tests for bump_version() — version string incrementing."""

    def test_simple_integer_version(self):
        content = '---\nname: test\nversion: 1\n---\nBody.'
        result = enhance.bump_version(content)
        self.assertIn('version: "2"', result)

    def test_dotted_version_bumps_major(self):
        content = '---\nname: test\nversion: 1.0.0\n---\nBody.'
        result = enhance.bump_version(content)
        self.assertIn('version: "2.0.0"', result)

    def test_quoted_version(self):
        content = '---\nname: test\nversion: "3"\n---\nBody.'
        result = enhance.bump_version(content)
        self.assertIn('version: "4"', result)

    def test_single_quoted_version(self):
        content = "---\nname: test\nversion: '5'\n---\nBody."
        result = enhance.bump_version(content)
        self.assertIn('version: "6"', result)

    def test_dotted_quoted_version(self):
        content = '---\nname: test\nversion: "2.1.3"\n---\nBody.'
        result = enhance.bump_version(content)
        self.assertIn('version: "3.1.3"', result)

    def test_only_bumps_first_occurrence(self):
        content = '---\nversion: 1\n---\nSome text with version: 10 in body.'
        result = enhance.bump_version(content)
        self.assertIn('version: "2"', result)
        # Body version should remain untouched
        self.assertIn("version: 10", result)

    def test_version_with_spaces(self):
        content = '---\nversion:   7\n---\nBody.'
        result = enhance.bump_version(content)
        self.assertIn('version: "8"', result)

    def test_large_version_number(self):
        content = '---\nversion: 99\n---\nBody.'
        result = enhance.bump_version(content)
        self.assertIn('version: "100"', result)

    def test_dotted_version_with_high_major(self):
        content = '---\nversion: 10.5.2\n---\nBody.'
        result = enhance.bump_version(content)
        self.assertIn('version: "11.5.2"', result)


class TestHasSection(unittest.TestCase):
    """Tests for has_section() — section existence checking."""

    def test_section_exists_exact_case(self):
        content = "Some text\nSELF-HEALING validation\nMore text"
        self.assertTrue(enhance.has_section(content, "SELF-HEALING"))

    def test_section_exists_different_case(self):
        content = "Some text\nSelf-Healing Validation\nMore text"
        self.assertTrue(enhance.has_section(content, "SELF-HEALING"))

    def test_section_missing(self):
        content = "Some text\nNo such section here\nMore text"
        self.assertFalse(enhance.has_section(content, "SELF-HEALING"))

    def test_section_telemetry_exists(self):
        content = "Body\nSELF-EVOLUTION TELEMETRY\nend"
        self.assertTrue(enhance.has_section(content, "SELF-EVOLUTION TELEMETRY"))

    def test_section_telemetry_missing(self):
        content = "Body with no telemetry section"
        self.assertFalse(enhance.has_section(content, "SELF-EVOLUTION TELEMETRY"))

    def test_section_parallel_execution(self):
        content = "Some\nPARALLEL EXECUTION: Use agents\nMore"
        self.assertTrue(enhance.has_section(content, "PARALLEL EXECUTION"))

    def test_empty_content(self):
        self.assertFalse(enhance.has_section("", "SELF-HEALING"))

    def test_partial_match(self):
        # "SELF-HEAL" should match content containing "SELF-HEALING"
        content = "SELF-HEALING block present"
        self.assertTrue(enhance.has_section(content, "SELF-HEAL"))


class TestFindOutputSection(unittest.TestCase):
    """Tests for find_output_section() — locating OUTPUT section."""

    def test_finds_output_with_equals_delimiters(self):
        content = "Phase 1\n\n====\nOUTPUT\n====\nReport here"
        pos = enhance.find_output_section(content)
        self.assertIsNotNone(pos)

    def test_finds_output_with_hash_header(self):
        content = "Phase 1\n\n## Output\nReport here"
        pos = enhance.find_output_section(content)
        self.assertIsNotNone(pos)

    def test_finds_next_steps_fallback(self):
        content = "Phase 1\n\n====\nNEXT STEPS\n====\nDo this"
        pos = enhance.find_output_section(content)
        self.assertIsNotNone(pos)

    def test_finds_hash_next_steps_fallback(self):
        content = "Phase 1\n\n## Next Steps\nDo this"
        pos = enhance.find_output_section(content)
        self.assertIsNotNone(pos)

    def test_returns_none_when_no_output_section(self):
        content = "Phase 1\nPhase 2\nDone."
        pos = enhance.find_output_section(content)
        self.assertIsNone(pos)

    def test_output_position_is_before_section(self):
        content = "Instructions\n\n====\nOUTPUT\n====\nReport"
        pos = enhance.find_output_section(content)
        # Position should be at the newline before the === delimiter
        self.assertGreater(pos, 0)
        self.assertLess(pos, len(content))

    def test_prefers_output_over_next_steps(self):
        content = "Body\n\n## Output\nReport\n\n## Next Steps\nDo this"
        pos = enhance.find_output_section(content)
        # Should find Output first, not Next Steps
        self.assertLess(pos, content.index("Next Steps"))


class TestFindEndPosition(unittest.TestCase):
    """Tests for find_end_position() — locating end of instructions."""

    def test_finds_do_not_section_with_equals(self):
        content = "Instructions\n\n====\nDO NOT\n====\n- Don't do this"
        pos = enhance.find_end_position(content)
        self.assertIsNotNone(pos)
        self.assertLess(pos, len(content))

    def test_finds_do_not_section_with_hash(self):
        content = "Instructions\n\n## DO NOT\n- Don't do this"
        pos = enhance.find_end_position(content)
        self.assertLess(pos, len(content))

    def test_finds_strict_rules(self):
        content = "Instructions\n\nSTRICT RULES:\n- Rule 1"
        pos = enhance.find_end_position(content)
        self.assertLess(pos, len(content))

    def test_returns_end_of_content_when_no_do_not(self):
        content = "Instructions\nPhase 1\nPhase 2\nDone."
        pos = enhance.find_end_position(content)
        self.assertEqual(pos, len(content))

    def test_empty_content(self):
        pos = enhance.find_end_position("")
        self.assertEqual(pos, 0)


class TestGetCategory(unittest.TestCase):
    """Tests for get_category() — extracting category from file paths."""

    def test_build_category(self):
        path = "/some/root/build/ship/SKILL.md"
        self.assertEqual(enhance.get_category(path), "build")

    def test_security_category(self):
        path = "/registry/security/owasp/SKILL.md"
        self.assertEqual(enhance.get_category(path), "security")

    def test_test_category(self):
        path = "/registry/test/unit-test/SKILL.md"
        self.assertEqual(enhance.get_category(path), "test")

    def test_qa_category(self):
        path = "/registry/qa/lint/SKILL.md"
        self.assertEqual(enhance.get_category(path), "qa")

    def test_combo_category(self):
        path = "/registry/combo/polish/SKILL.md"
        self.assertEqual(enhance.get_category(path), "combo")

    def test_unknown_category_returns_none(self):
        path = "/registry/unknown-cat/skill/SKILL.md"
        self.assertIsNone(enhance.get_category(path))

    def test_all_known_categories(self):
        for cat in enhance.SELF_HEALING:
            path = f"/root/{cat}/skill/SKILL.md"
            self.assertEqual(enhance.get_category(path), cat)


class TestGetSkillName(unittest.TestCase):
    """Tests for get_skill_name() — extracting skill name from file paths."""

    def test_simple_skill_name(self):
        path = "/registry/build/ship/SKILL.md"
        self.assertEqual(enhance.get_skill_name(path), "ship")

    def test_hyphenated_skill_name(self):
        path = "/registry/test/unit-test/SKILL.md"
        self.assertEqual(enhance.get_skill_name(path), "unit-test")

    def test_deeply_nested_path(self):
        path = "/a/b/c/d/my-skill/SKILL.md"
        self.assertEqual(enhance.get_skill_name(path), "my-skill")


class TestProcessSkill(unittest.TestCase):
    """Tests for process_skill() — full file processing pipeline."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _create_skill(self, category, skill_name, content):
        """Create a SKILL.md in tmpdir and return its path."""
        skill_dir = os.path.join(self.tmpdir, category, skill_name)
        os.makedirs(skill_dir, exist_ok=True)
        filepath = os.path.join(skill_dir, "SKILL.md")
        with open(filepath, "w") as f:
            f.write(content)
        return filepath

    def _read_skill(self, filepath):
        with open(filepath) as f:
            return f.read()

    def test_adds_self_healing_to_build_skill(self):
        content = '---\nname: test-skill\ndescription: A test\nversion: 1\n---\nInstructions here.'
        filepath = self._create_skill("build", "test-skill", content)
        result = enhance.process_skill(filepath)
        self.assertTrue(result)
        updated = self._read_skill(filepath)
        self.assertIn("SELF-HEALING VALIDATION", updated)

    def test_adds_telemetry(self):
        content = '---\nname: my-skill\ndescription: Test\nversion: 1\n---\nInstructions.'
        filepath = self._create_skill("build", "my-skill", content)
        enhance.process_skill(filepath)
        updated = self._read_skill(filepath)
        self.assertIn("SELF-EVOLUTION TELEMETRY", updated)
        self.assertIn("/my-skill", updated)

    def test_bumps_version(self):
        content = '---\nname: test\ndescription: Test\nversion: 3\n---\nInstructions.'
        filepath = self._create_skill("security", "test", content)
        enhance.process_skill(filepath)
        updated = self._read_skill(filepath)
        self.assertIn('version: "4"', updated)

    def test_skips_unknown_category(self):
        content = '---\nname: zz-skill\ndescription: Test\nversion: 1\n---\nBody.'
        filepath = self._create_skill("unknown-category", "zz-skill", content)
        result = enhance.process_skill(filepath)
        # Returns False because get_category returns None for unknown-category
        self.assertFalse(result)
        updated = self._read_skill(filepath)
        self.assertNotIn("SELF-HEALING", updated)

    def test_does_not_duplicate_self_healing(self):
        content = '---\nname: test\ndescription: Test\nversion: 1\n---\nSELF-HEALING existing.\nInstructions.'
        filepath = self._create_skill("build", "test", content)
        enhance.process_skill(filepath)
        updated = self._read_skill(filepath)
        # Should only have the original occurrence, not add another
        count = updated.upper().count("SELF-HEALING")
        # Original "SELF-HEALING existing" plus no additional block
        self.assertEqual(count, 1)

    def test_does_not_duplicate_telemetry(self):
        content = '---\nname: test\ndescription: Test\nversion: 1\n---\nSELF-EVOLUTION TELEMETRY exists.\nBody.'
        filepath = self._create_skill("build", "test", content)
        enhance.process_skill(filepath)
        updated = self._read_skill(filepath)
        count = updated.upper().count("SELF-EVOLUTION TELEMETRY")
        self.assertEqual(count, 1)

    def test_inserts_healing_before_output_section(self):
        content = (
            '---\nname: test\ndescription: Test\nversion: 1\n---\n'
            'Instructions\n\n====\nOUTPUT\n====\nReport here.'
        )
        filepath = self._create_skill("qa", "test", content)
        enhance.process_skill(filepath)
        updated = self._read_skill(filepath)
        healing_pos = updated.upper().find("SELF-HEALING")
        output_pos = updated.find("OUTPUT\n====\nReport")
        self.assertLess(healing_pos, output_pos)

    def test_adds_subagent_block_for_combo_skill(self):
        content = '---\nname: polish\ndescription: Polish\nversion: 1\n---\nInstructions.'
        filepath = self._create_skill("combo", "polish", content)
        enhance.process_skill(filepath)
        updated = self._read_skill(filepath)
        self.assertIn("PARALLEL EXECUTION", updated)

    def test_no_subagent_block_for_non_combo_skill(self):
        content = '---\nname: ship\ndescription: Ship\nversion: 1\n---\nInstructions.'
        filepath = self._create_skill("build", "ship", content)
        enhance.process_skill(filepath)
        updated = self._read_skill(filepath)
        self.assertNotIn("PARALLEL EXECUTION", updated)

    def test_inserts_healing_before_do_not_section(self):
        content = (
            '---\nname: test\ndescription: Test\nversion: 1\n---\n'
            'Instructions\n\n====\nDO NOT\n====\n- Never do this.'
        )
        filepath = self._create_skill("test", "test", content)
        enhance.process_skill(filepath)
        updated = self._read_skill(filepath)
        healing_pos = updated.upper().find("SELF-HEALING")
        do_not_pos = updated.find("DO NOT\n====\n- Never")
        self.assertLess(healing_pos, do_not_pos)

    def test_telemetry_before_do_not_section(self):
        content = (
            '---\nname: test\ndescription: Test\nversion: 1\n---\n'
            'Instructions\n\n====\nDO NOT\n====\n- Never do this.'
        )
        filepath = self._create_skill("security", "test", content)
        enhance.process_skill(filepath)
        updated = self._read_skill(filepath)
        telemetry_pos = updated.upper().find("SELF-EVOLUTION TELEMETRY")
        do_not_pos = updated.upper().find("DO NOT\n====\n- NEVER")
        self.assertLess(telemetry_pos, do_not_pos)

    def test_all_category_healing_blocks_used(self):
        """Each category in SELF_HEALING dict produces a unique healing block."""
        for category, expected_text in enhance.SELF_HEALING.items():
            content = f'---\nname: test-{category}\ndescription: Test\nversion: 1\n---\nBody.'
            filepath = self._create_skill(category, f"test-{category}", content)
            enhance.process_skill(filepath)
            updated = self._read_skill(filepath)
            self.assertIn("SELF-HEALING VALIDATION", updated,
                          f"Category '{category}' should get healing block")


class TestSubagentPatterns(unittest.TestCase):
    """Tests for SUBAGENT_PATTERNS coverage."""

    def test_all_subagent_skills_have_parallel_execution(self):
        for skill_name, block in enhance.SUBAGENT_PATTERNS.items():
            self.assertIn("PARALLEL EXECUTION", block,
                          f"Subagent pattern for '{skill_name}' must contain PARALLEL EXECUTION")
            self.assertIn("Agent", block,
                          f"Subagent pattern for '{skill_name}' must reference Agent tool")

    def test_known_combo_skills_have_patterns(self):
        expected = ["polish", "full-test", "cleanup-sprint", "research",
                    "retro", "review-implement", "secure-ship", "compliance-suite"]
        for skill in expected:
            self.assertIn(skill, enhance.SUBAGENT_PATTERNS,
                          f"Expected subagent pattern for '{skill}'")


class TestSelfHealingDict(unittest.TestCase):
    """Tests for SELF_HEALING dict completeness."""

    def test_all_categories_have_max_iterations(self):
        for category, block in enhance.SELF_HEALING.items():
            self.assertIn("max", block.lower(),
                          f"Category '{category}' healing block should specify max iterations")

    def test_all_categories_have_failure_fallback_guidance(self):
        """Every category must have guidance for what to do when healing doesn't converge."""
        for category, block in enhance.SELF_HEALING.items():
            has_fallback = ("STILL FAILING" in block or
                            "STILL INCOMPLETE" in block or
                            "IF VALIDATION FAILS" in block)
            self.assertTrue(has_fallback,
                            f"Category '{category}' should have failure fallback guidance")

    def test_expected_categories_present(self):
        expected = ["analysis", "build", "combo", "deploy", "docs",
                    "integration", "meta", "productivity", "qa",
                    "review", "security", "test", "ux"]
        for cat in expected:
            self.assertIn(cat, enhance.SELF_HEALING,
                          f"Expected category '{cat}' in SELF_HEALING")


if __name__ == "__main__":
    unittest.main()
