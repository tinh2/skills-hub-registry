#!/usr/bin/env python3
"""
test_generate_report.py — Unit tests for meta/skill-creator/scripts/generate_report.py

Tests generate_html() with various history data, empty states, edge cases,
and HTML structure validation.
"""
import os
import sys
import unittest

SKILL_CREATOR_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "meta", "skill-creator")
sys.path.insert(0, SKILL_CREATOR_ROOT)
from scripts.generate_report import generate_html


class TestGenerateHtmlBasic(unittest.TestCase):
    """Tests for generate_html() — basic HTML structure."""

    def _make_data(self, history=None, **overrides):
        """Build minimal valid data dict for generate_html."""
        data = {
            "original_description": "Original skill description",
            "best_description": "Improved skill description",
            "best_score": "8/10",
            "iterations_run": 1,
            "holdout": 0.3,
            "train_size": 7,
            "test_size": 3,
            "history": history or [],
        }
        data.update(overrides)
        return data

    def _make_history_entry(self, iteration=1, description="Test description",
                            train_passed=3, train_total=5, test_passed=2, test_total=3,
                            train_results=None, test_results=None):
        """Build a history entry with sensible defaults."""
        if train_results is None:
            train_results = [
                {"query": "build my app", "should_trigger": True, "pass": True, "triggers": 3, "runs": 3},
                {"query": "fix the bug", "should_trigger": True, "pass": True, "triggers": 2, "runs": 3},
                {"query": "what time is it", "should_trigger": False, "pass": True, "triggers": 0, "runs": 3},
                {"query": "deploy to prod", "should_trigger": True, "pass": True, "triggers": 3, "runs": 3},
                {"query": "make coffee", "should_trigger": False, "pass": False, "triggers": 2, "runs": 3},
            ]
        if test_results is None:
            test_results = [
                {"query": "ship it", "should_trigger": True, "pass": True, "triggers": 3, "runs": 3},
                {"query": "hello world", "should_trigger": False, "pass": True, "triggers": 0, "runs": 3},
                {"query": "run tests", "should_trigger": True, "pass": False, "triggers": 1, "runs": 3},
            ]
        return {
            "iteration": iteration,
            "description": description,
            "train_passed": train_passed,
            "train_failed": train_total - train_passed,
            "train_total": train_total,
            "train_results": train_results,
            "test_passed": test_passed,
            "test_failed": test_total - test_passed,
            "test_total": test_total,
            "test_results": test_results,
            "passed": train_passed,
            "failed": train_total - train_passed,
            "total": train_total,
            "results": train_results,
        }

    def test_returns_valid_html(self):
        data = self._make_data()
        html = generate_html(data)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("<html>", html)
        self.assertIn("</html>", html)

    def test_contains_title(self):
        data = self._make_data()
        html = generate_html(data)
        self.assertIn("Skill Description Optimization", html)

    def test_contains_original_description(self):
        data = self._make_data()
        html = generate_html(data)
        self.assertIn("Original skill description", html)

    def test_contains_best_description(self):
        data = self._make_data()
        html = generate_html(data)
        self.assertIn("Improved skill description", html)

    def test_contains_best_score(self):
        data = self._make_data()
        html = generate_html(data)
        self.assertIn("8/10", html)

    def test_contains_iterations_count(self):
        data = self._make_data(iterations_run=5)
        html = generate_html(data)
        self.assertIn("5", html)

    def test_empty_history(self):
        data = self._make_data(history=[])
        html = generate_html(data)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("</table>", html)


class TestGenerateHtmlWithHistory(unittest.TestCase):
    """Tests for generate_html() with history entries."""

    def _make_history_entry(self, iteration=1, description="Desc", results=None, test_results=None):
        train_results = results or [
            {"query": "build app", "should_trigger": True, "pass": True, "triggers": 3, "runs": 3},
            {"query": "hello", "should_trigger": False, "pass": True, "triggers": 0, "runs": 3},
        ]
        t_results = test_results or [
            {"query": "ship it", "should_trigger": True, "pass": True, "triggers": 2, "runs": 3},
        ]
        return {
            "iteration": iteration,
            "description": description,
            "train_passed": sum(1 for r in train_results if r["pass"]),
            "train_total": len(train_results),
            "train_results": train_results,
            "test_passed": sum(1 for r in t_results if r["pass"]),
            "test_total": len(t_results),
            "test_results": t_results,
            "passed": sum(1 for r in train_results if r["pass"]),
            "total": len(train_results),
            "results": train_results,
        }

    def _make_data(self, history):
        return {
            "original_description": "Original",
            "best_description": "Best",
            "best_score": "5/5",
            "iterations_run": len(history),
            "holdout": 0.3,
            "train_size": 7,
            "test_size": 3,
            "history": history,
        }

    def test_renders_iteration_number(self):
        entry = self._make_history_entry(iteration=3)
        data = self._make_data([entry])
        html = generate_html(data)
        self.assertIn("<td>3</td>", html)

    def test_renders_description_in_row(self):
        entry = self._make_history_entry(description="Trigger on deploy commands")
        data = self._make_data([entry])
        html = generate_html(data)
        self.assertIn("Trigger on deploy commands", html)

    def test_renders_pass_checkmark(self):
        entry = self._make_history_entry()
        data = self._make_data([entry])
        html = generate_html(data)
        self.assertIn("✓", html)

    def test_renders_fail_cross(self):
        results = [
            {"query": "bad query", "should_trigger": True, "pass": False, "triggers": 0, "runs": 3},
        ]
        entry = self._make_history_entry(results=results)
        data = self._make_data([entry])
        html = generate_html(data)
        self.assertIn("✗", html)

    def test_renders_trigger_rate(self):
        results = [
            {"query": "test query", "should_trigger": True, "pass": True, "triggers": 2, "runs": 3},
        ]
        entry = self._make_history_entry(results=results)
        data = self._make_data([entry])
        html = generate_html(data)
        self.assertIn("2/3", html)

    def test_multiple_iterations_rendered(self):
        entries = [
            self._make_history_entry(iteration=1, description="First attempt"),
            self._make_history_entry(iteration=2, description="Second attempt"),
            self._make_history_entry(iteration=3, description="Third attempt"),
        ]
        data = self._make_data(entries)
        html = generate_html(data)
        self.assertIn("First attempt", html)
        self.assertIn("Second attempt", html)
        self.assertIn("Third attempt", html)

    def test_query_columns_in_header(self):
        results = [
            {"query": "deploy my service", "should_trigger": True, "pass": True, "triggers": 3, "runs": 3},
        ]
        entry = self._make_history_entry(results=results)
        data = self._make_data([entry])
        html = generate_html(data)
        self.assertIn("deploy my service", html)

    def test_test_queries_have_test_col_class(self):
        entry = self._make_history_entry()
        data = self._make_data([entry])
        html = generate_html(data)
        self.assertIn("test-col", html)

    def test_positive_query_has_positive_col_class(self):
        results = [
            {"query": "build it", "should_trigger": True, "pass": True, "triggers": 3, "runs": 3},
        ]
        entry = self._make_history_entry(results=results)
        data = self._make_data([entry])
        html = generate_html(data)
        self.assertIn("positive-col", html)

    def test_negative_query_has_negative_col_class(self):
        results = [
            {"query": "unrelated thing", "should_trigger": False, "pass": True, "triggers": 0, "runs": 3},
        ]
        entry = self._make_history_entry(results=results)
        data = self._make_data([entry])
        html = generate_html(data)
        self.assertIn("negative-col", html)


class TestGenerateHtmlAutoRefresh(unittest.TestCase):
    """Tests for auto_refresh parameter."""

    def _make_data(self):
        return {
            "original_description": "Orig",
            "best_description": "Best",
            "best_score": "3/3",
            "iterations_run": 0,
            "holdout": 0,
            "train_size": 3,
            "test_size": 0,
            "history": [],
        }

    def test_auto_refresh_adds_meta_tag(self):
        html = generate_html(self._make_data(), auto_refresh=True)
        self.assertIn('meta http-equiv="refresh"', html)

    def test_no_auto_refresh_by_default(self):
        html = generate_html(self._make_data(), auto_refresh=False)
        self.assertNotIn('meta http-equiv="refresh"', html)

    def test_default_no_auto_refresh(self):
        html = generate_html(self._make_data())
        self.assertNotIn('meta http-equiv="refresh"', html)


class TestGenerateHtmlSkillName(unittest.TestCase):
    """Tests for skill_name parameter."""

    def _make_data(self):
        return {
            "original_description": "Orig",
            "best_description": "Best",
            "best_score": "1/1",
            "iterations_run": 0,
            "holdout": 0,
            "train_size": 1,
            "test_size": 0,
            "history": [],
        }

    def test_skill_name_in_title(self):
        html = generate_html(self._make_data(), skill_name="unit-test")
        self.assertIn("unit-test", html)

    def test_empty_skill_name_no_prefix(self):
        html = generate_html(self._make_data(), skill_name="")
        # Title should just be "Skill Description Optimization" without dash prefix
        self.assertIn("<title>Skill Description Optimization</title>", html)

    def test_skill_name_html_escaped(self):
        html = generate_html(self._make_data(), skill_name="test<script>")
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)


class TestGenerateHtmlScoreClasses(unittest.TestCase):
    """Tests for score CSS class assignment based on correct/total ratio."""

    def _make_entry_with_ratio(self, trigger_count, total_runs):
        """Create an entry where we can control the aggregate ratio."""
        results = [
            {"query": f"q{i}", "should_trigger": True, "pass": True,
             "triggers": trigger_count, "runs": total_runs}
            for i in range(1)
        ]
        return {
            "iteration": 1,
            "description": "test",
            "train_passed": 1,
            "train_total": 1,
            "train_results": results,
            "test_passed": None,
            "test_total": None,
            "test_results": None,
            "passed": 1,
            "total": 1,
            "results": results,
        }

    def _make_data(self, entry):
        return {
            "original_description": "Orig",
            "best_description": "Best",
            "best_score": "1/1",
            "iterations_run": 1,
            "holdout": 0,
            "train_size": 1,
            "test_size": 0,
            "history": [entry],
        }

    def test_high_ratio_gets_score_good(self):
        entry = self._make_entry_with_ratio(9, 10)  # 90%
        html = generate_html(self._make_data(entry))
        self.assertIn("score-good", html)

    def test_medium_ratio_gets_score_ok(self):
        entry = self._make_entry_with_ratio(6, 10)  # 60%
        html = generate_html(self._make_data(entry))
        self.assertIn("score-ok", html)

    def test_low_ratio_gets_score_bad(self):
        entry = self._make_entry_with_ratio(2, 10)  # 20%
        html = generate_html(self._make_data(entry))
        self.assertIn("score-bad", html)


class TestGenerateHtmlBestRow(unittest.TestCase):
    """Tests for best-row highlighting."""

    def _make_entry(self, iteration, test_passed):
        results = [
            {"query": "q1", "should_trigger": True, "pass": True, "triggers": 3, "runs": 3},
        ]
        return {
            "iteration": iteration,
            "description": f"desc {iteration}",
            "train_passed": 1,
            "train_total": 1,
            "train_results": results,
            "test_passed": test_passed,
            "test_total": 3,
            "test_results": [
                {"query": "t1", "should_trigger": True, "pass": test_passed > 0, "triggers": test_passed, "runs": 3},
            ],
            "passed": 1,
            "total": 1,
            "results": results,
        }

    def test_best_iteration_gets_best_row_class(self):
        entries = [
            self._make_entry(1, test_passed=1),
            self._make_entry(2, test_passed=3),  # best
            self._make_entry(3, test_passed=2),
        ]
        data = {
            "original_description": "Orig",
            "best_description": "Best",
            "best_score": "3/3",
            "iterations_run": 3,
            "holdout": 0.3,
            "train_size": 1,
            "test_size": 3,
            "history": entries,
        }
        html = generate_html(data)
        self.assertIn("best-row", html)


class TestGenerateHtmlTrainOnly(unittest.TestCase):
    """Tests for generate_html() with no test set (holdout=0)."""

    def test_no_test_queries_columns(self):
        results = [
            {"query": "build app", "should_trigger": True, "pass": True, "triggers": 3, "runs": 3},
        ]
        entry = {
            "iteration": 1,
            "description": "first try",
            "train_passed": 1,
            "train_total": 1,
            "train_results": results,
            "test_passed": None,
            "test_total": None,
            "test_results": None,
            "passed": 1,
            "total": 1,
            "results": results,
        }
        data = {
            "original_description": "Orig",
            "best_description": "Best",
            "best_score": "1/1",
            "iterations_run": 1,
            "holdout": 0,
            "train_size": 1,
            "test_size": 0,
            "history": [entry],
        }
        html = generate_html(data)
        self.assertIn("build app", html)
        # No test-result cells should be present
        self.assertNotIn("test-result", html)


class TestGenerateHtmlDescriptionEscaping(unittest.TestCase):
    """Tests for HTML escaping of user-supplied content."""

    def test_description_with_html_entities(self):
        entry = {
            "iteration": 1,
            "description": 'Use for <script> & "quotes"',
            "train_passed": 1,
            "train_total": 1,
            "train_results": [
                {"query": "q1", "should_trigger": True, "pass": True, "triggers": 3, "runs": 3},
            ],
            "test_passed": None,
            "test_total": None,
            "test_results": None,
            "passed": 1,
            "total": 1,
            "results": [
                {"query": "q1", "should_trigger": True, "pass": True, "triggers": 3, "runs": 3},
            ],
        }
        data = {
            "original_description": "Orig <b>bold</b>",
            "best_description": "Best & improved",
            "best_score": "1/1",
            "iterations_run": 1,
            "holdout": 0,
            "train_size": 1,
            "test_size": 0,
            "history": [entry],
        }
        html = generate_html(data)
        # Should be escaped, not raw HTML
        self.assertNotIn("<script>", html)
        self.assertIn("&lt;script&gt;", html)
        self.assertIn("&amp;", html)


if __name__ == "__main__":
    unittest.main()
