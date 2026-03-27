#!/usr/bin/env python3
"""
test_package_skill.py — Unit tests for meta/skill-creator/scripts/package_skill.py

Tests should_exclude() for file filtering logic.
"""
import os
import sys
import unittest

SKILL_CREATOR_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "meta", "skill-creator")
sys.path.insert(0, SKILL_CREATOR_ROOT)
from scripts.package_skill import should_exclude
from pathlib import Path


class TestShouldExclude(unittest.TestCase):
    """Tests for should_exclude() — file exclusion during packaging."""

    def test_excludes_pycache(self):
        self.assertTrue(should_exclude(Path("skill/__pycache__/module.pyc")))

    def test_excludes_node_modules(self):
        self.assertTrue(should_exclude(Path("skill/node_modules/package/index.js")))

    def test_excludes_pyc_files(self):
        self.assertTrue(should_exclude(Path("skill/module.pyc")))

    def test_excludes_ds_store(self):
        self.assertTrue(should_exclude(Path("skill/.DS_Store")))

    def test_excludes_root_evals_dir(self):
        # parts[0]=skill, parts[1]=evals → should be excluded
        self.assertTrue(should_exclude(Path("skill/evals/test.json")))

    def test_allows_nested_evals_dir(self):
        # parts[0]=skill, parts[1]=subdir, parts[2]=evals → NOT root level
        self.assertFalse(should_exclude(Path("skill/subdir/evals/test.json")))

    def test_allows_regular_files(self):
        self.assertFalse(should_exclude(Path("skill/SKILL.md")))

    def test_allows_python_source(self):
        self.assertFalse(should_exclude(Path("skill/scripts/main.py")))

    def test_allows_json_files(self):
        self.assertFalse(should_exclude(Path("skill/config.json")))

    def test_allows_readme(self):
        self.assertFalse(should_exclude(Path("skill/README.md")))

    def test_excludes_deeply_nested_pycache(self):
        self.assertTrue(should_exclude(Path("skill/a/b/__pycache__/mod.pyc")))

    def test_excludes_deeply_nested_node_modules(self):
        self.assertTrue(should_exclude(Path("skill/a/node_modules/pkg.js")))


if __name__ == "__main__":
    unittest.main()
