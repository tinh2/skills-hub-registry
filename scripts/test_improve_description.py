#!/usr/bin/env python3
"""
test_improve_description.py — Unit tests for meta/skill-creator/scripts/improve_description.py

Tests improve_description() prompt building, response parsing, length enforcement,
and logging. Mocks _call_claude() to avoid subprocess calls.
"""
import json
import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch

SKILL_CREATOR_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "meta", "skill-creator")
sys.path.insert(0, SKILL_CREATOR_ROOT)
from scripts.improve_description import improve_description


class TestImproveDescriptionParsing(unittest.TestCase):
    """Tests for improve_description() — response parsing and description extraction."""

    def _make_eval_results(self, results=None):
        """Build minimal eval results dict."""
        if results is None:
            results = [
                {"query": "build app", "should_trigger": True, "pass": True, "triggers": 3, "runs": 3},
                {"query": "hello world", "should_trigger": False, "pass": True, "triggers": 0, "runs": 3},
            ]
        passed = sum(1 for r in results if r["pass"])
        total = len(results)
        return {
            "results": results,
            "summary": {"passed": passed, "failed": total - passed, "total": total},
        }

    @patch("scripts.improve_description._call_claude")
    def test_extracts_description_from_tags(self, mock_claude):
        """Should extract text between <new_description> tags."""
        mock_claude.return_value = "Here is my suggestion:\n<new_description>Use for deploying apps to production</new_description>\nDone."
        result = improve_description(
            skill_name="deploy",
            skill_content="# Deploy\nDeploys apps.",
            current_description="Deploy stuff",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
        )
        self.assertEqual(result, "Use for deploying apps to production")

    @patch("scripts.improve_description._call_claude")
    def test_strips_quotes_from_description(self, mock_claude):
        """Should strip surrounding quotes from extracted description."""
        mock_claude.return_value = '<new_description>"Build and deploy applications"</new_description>'
        result = improve_description(
            skill_name="deploy",
            skill_content="# Deploy",
            current_description="Old desc",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
        )
        self.assertEqual(result, "Build and deploy applications")

    @patch("scripts.improve_description._call_claude")
    def test_falls_back_to_full_text_without_tags(self, mock_claude):
        """When no <new_description> tags, should use full response stripped."""
        mock_claude.return_value = "Use for building and shipping features"
        result = improve_description(
            skill_name="ship",
            skill_content="# Ship",
            current_description="Old",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
        )
        self.assertEqual(result, "Use for building and shipping features")

    @patch("scripts.improve_description._call_claude")
    def test_multiline_description_extracted(self, mock_claude):
        """Should handle multiline content inside tags."""
        mock_claude.return_value = "<new_description>Line one.\nLine two.\nLine three.</new_description>"
        result = improve_description(
            skill_name="test",
            skill_content="# Test",
            current_description="Old",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
        )
        self.assertIn("Line one.", result)
        self.assertIn("Line three.", result)


class TestImproveDescriptionLengthEnforcement(unittest.TestCase):
    """Tests for the 1024-character length limit enforcement."""

    def _make_eval_results(self):
        return {
            "results": [
                {"query": "q1", "should_trigger": True, "pass": False, "triggers": 0, "runs": 3},
            ],
            "summary": {"passed": 0, "failed": 1, "total": 1},
        }

    @patch("scripts.improve_description._call_claude")
    def test_short_description_not_rewritten(self, mock_claude):
        """Descriptions under 1024 chars should not trigger a rewrite call."""
        short_desc = "Use for deploying apps"
        mock_claude.return_value = f"<new_description>{short_desc}</new_description>"

        result = improve_description(
            skill_name="deploy",
            skill_content="# Deploy",
            current_description="Old",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
        )

        self.assertEqual(result, short_desc)
        # Should only be called once (no rewrite)
        self.assertEqual(mock_claude.call_count, 1)

    @patch("scripts.improve_description._call_claude")
    def test_long_description_triggers_rewrite(self, mock_claude):
        """Descriptions over 1024 chars should trigger a second call for shortening."""
        long_desc = "x" * 1100
        short_desc = "x" * 500
        mock_claude.side_effect = [
            f"<new_description>{long_desc}</new_description>",
            f"<new_description>{short_desc}</new_description>",
        ]

        result = improve_description(
            skill_name="deploy",
            skill_content="# Deploy",
            current_description="Old",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
        )

        self.assertEqual(result, short_desc)
        self.assertEqual(mock_claude.call_count, 2)


class TestImproveDescriptionLogging(unittest.TestCase):
    """Tests for log file creation."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _make_eval_results(self):
        return {
            "results": [
                {"query": "q1", "should_trigger": True, "pass": True, "triggers": 3, "runs": 3},
            ],
            "summary": {"passed": 1, "failed": 0, "total": 1},
        }

    @patch("scripts.improve_description._call_claude")
    def test_writes_log_file(self, mock_claude):
        """Should write a log file when log_dir is provided."""
        mock_claude.return_value = "<new_description>Better description</new_description>"
        log_dir = Path(self.tmpdir) / "logs"

        improve_description(
            skill_name="test",
            skill_content="# Test",
            current_description="Old",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
            log_dir=log_dir,
            iteration=3,
        )

        log_file = log_dir / "improve_iter_3.json"
        self.assertTrue(log_file.exists())
        log_data = json.loads(log_file.read_text())
        self.assertEqual(log_data["iteration"], 3)
        self.assertEqual(log_data["final_description"], "Better description")

    @patch("scripts.improve_description._call_claude")
    def test_no_log_when_log_dir_is_none(self, mock_claude):
        """Should not write logs when log_dir is None."""
        mock_claude.return_value = "<new_description>Desc</new_description>"

        # Should not raise
        result = improve_description(
            skill_name="test",
            skill_content="# Test",
            current_description="Old",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
            log_dir=None,
            iteration=1,
        )
        self.assertEqual(result, "Desc")

    @patch("scripts.improve_description._call_claude")
    def test_log_includes_prompt_and_response(self, mock_claude):
        """Log should contain the prompt and raw response."""
        mock_claude.return_value = "<new_description>New desc</new_description>"
        log_dir = Path(self.tmpdir) / "logs"

        improve_description(
            skill_name="test",
            skill_content="# Test content here",
            current_description="Current description",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
            log_dir=log_dir,
            iteration=1,
        )

        log_file = log_dir / "improve_iter_1.json"
        log_data = json.loads(log_file.read_text())
        self.assertIn("prompt", log_data)
        self.assertIn("response", log_data)
        self.assertIn("Current description", log_data["prompt"])
        self.assertIn("char_count", log_data)


class TestImproveDescriptionPromptBuilding(unittest.TestCase):
    """Tests that the prompt includes appropriate context."""

    def _make_eval_results(self, results=None):
        if results is None:
            results = [
                {"query": "build app", "should_trigger": True, "pass": False, "triggers": 0, "runs": 3},
                {"query": "hello world", "should_trigger": False, "pass": False, "triggers": 3, "runs": 3},
            ]
        passed = sum(1 for r in results if r["pass"])
        total = len(results)
        return {
            "results": results,
            "summary": {"passed": passed, "failed": total - passed, "total": total},
        }

    @patch("scripts.improve_description._call_claude")
    def test_prompt_includes_skill_name(self, mock_claude):
        """Prompt should reference the skill name."""
        mock_claude.return_value = "<new_description>desc</new_description>"

        improve_description(
            skill_name="deploy-wizard",
            skill_content="# Deploy Wizard",
            current_description="Old",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
        )

        prompt = mock_claude.call_args[0][0]
        self.assertIn("deploy-wizard", prompt)

    @patch("scripts.improve_description._call_claude")
    def test_prompt_includes_failed_triggers(self, mock_claude):
        """Prompt should list queries that failed to trigger."""
        mock_claude.return_value = "<new_description>desc</new_description>"

        results = [
            {"query": "build my project", "should_trigger": True, "pass": False, "triggers": 0, "runs": 3},
        ]
        improve_description(
            skill_name="build",
            skill_content="# Build",
            current_description="Old",
            eval_results=self._make_eval_results(results),
            history=[],
            model="claude-sonnet-4-20250514",
        )

        prompt = mock_claude.call_args[0][0]
        self.assertIn("FAILED TO TRIGGER", prompt)
        self.assertIn("build my project", prompt)

    @patch("scripts.improve_description._call_claude")
    def test_prompt_includes_false_triggers(self, mock_claude):
        """Prompt should list queries that falsely triggered."""
        mock_claude.return_value = "<new_description>desc</new_description>"

        results = [
            {"query": "make coffee", "should_trigger": False, "pass": False, "triggers": 3, "runs": 3},
        ]
        improve_description(
            skill_name="build",
            skill_content="# Build",
            current_description="Old",
            eval_results=self._make_eval_results(results),
            history=[],
            model="claude-sonnet-4-20250514",
        )

        prompt = mock_claude.call_args[0][0]
        self.assertIn("FALSE TRIGGERS", prompt)
        self.assertIn("make coffee", prompt)

    @patch("scripts.improve_description._call_claude")
    def test_prompt_includes_history(self, mock_claude):
        """Prompt should include previous attempt history."""
        mock_claude.return_value = "<new_description>desc</new_description>"

        history = [
            {
                "description": "First attempt at description",
                "train_passed": 3,
                "train_total": 5,
                "test_passed": 2,
                "test_total": 3,
                "results": [
                    {"query": "q1", "pass": True, "triggers": 3, "runs": 3, "query": "build it"},
                ],
            },
        ]
        improve_description(
            skill_name="build",
            skill_content="# Build",
            current_description="Current",
            eval_results=self._make_eval_results(),
            history=history,
            model="claude-sonnet-4-20250514",
        )

        prompt = mock_claude.call_args[0][0]
        self.assertIn("PREVIOUS ATTEMPTS", prompt)
        self.assertIn("First attempt at description", prompt)

    @patch("scripts.improve_description._call_claude")
    def test_prompt_includes_skill_content(self, mock_claude):
        """Prompt should include the full skill content for context."""
        mock_claude.return_value = "<new_description>desc</new_description>"

        improve_description(
            skill_name="build",
            skill_content="# Build\n\nThis skill builds and compiles projects.",
            current_description="Old",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
        )

        prompt = mock_claude.call_args[0][0]
        self.assertIn("This skill builds and compiles projects.", prompt)

    @patch("scripts.improve_description._call_claude")
    def test_prompt_includes_test_score_when_available(self, mock_claude):
        """Prompt should show test scores when test_results are provided."""
        mock_claude.return_value = "<new_description>desc</new_description>"

        improve_description(
            skill_name="build",
            skill_content="# Build",
            current_description="Old",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
            test_results={
                "results": [],
                "summary": {"passed": 4, "failed": 1, "total": 5},
            },
        )

        prompt = mock_claude.call_args[0][0]
        self.assertIn("Test: 4/5", prompt)

    @patch("scripts.improve_description._call_claude")
    def test_model_passed_to_claude(self, mock_claude):
        """Model argument should be forwarded to _call_claude."""
        mock_claude.return_value = "<new_description>desc</new_description>"

        improve_description(
            skill_name="test",
            skill_content="# Test",
            current_description="Old",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-opus-4-20250514",
        )

        model_arg = mock_claude.call_args[0][1]
        self.assertEqual(model_arg, "claude-opus-4-20250514")


class TestImproveDescriptionEdgeCases(unittest.TestCase):
    """Edge case tests for improve_description()."""

    def _make_eval_results(self):
        return {
            "results": [],
            "summary": {"passed": 0, "failed": 0, "total": 0},
        }

    @patch("scripts.improve_description._call_claude")
    def test_empty_eval_results(self, mock_claude):
        """Should handle empty eval results without crashing."""
        mock_claude.return_value = "<new_description>Fallback</new_description>"

        result = improve_description(
            skill_name="test",
            skill_content="# Test",
            current_description="Old",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
        )
        self.assertEqual(result, "Fallback")

    @patch("scripts.improve_description._call_claude")
    def test_empty_history(self, mock_claude):
        """Should work fine with no history."""
        mock_claude.return_value = "<new_description>Fresh start</new_description>"

        result = improve_description(
            skill_name="test",
            skill_content="# Test",
            current_description="Old",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
        )
        self.assertEqual(result, "Fresh start")

    @patch("scripts.improve_description._call_claude")
    def test_whitespace_only_response(self, mock_claude):
        """Should handle whitespace-only response gracefully."""
        mock_claude.return_value = "   \n\n  "

        result = improve_description(
            skill_name="test",
            skill_content="# Test",
            current_description="Old",
            eval_results=self._make_eval_results(),
            history=[],
            model="claude-sonnet-4-20250514",
        )
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
