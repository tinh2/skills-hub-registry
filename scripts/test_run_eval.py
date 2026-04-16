#!/usr/bin/env python3
"""
test_run_eval.py — Unit tests for meta/skill-creator/scripts/run_eval.py

Tests find_project_root() and run_eval() result aggregation logic.
run_single_query() is excluded as it requires live `claude` subprocess.
"""
import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from concurrent.futures import Future

SKILL_CREATOR_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "meta", "skill-creator")
sys.path.insert(0, SKILL_CREATOR_ROOT)
from scripts.run_eval import find_project_root, run_eval


class TestFindProjectRoot(unittest.TestCase):
    """Tests for find_project_root() — locating project root via .claude/ directory."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()

    def tearDown(self):
        os.chdir(self.original_cwd)
        shutil.rmtree(self.tmpdir)

    def test_finds_root_when_claude_dir_exists(self):
        """Should find the directory containing .claude/."""
        project_root = (Path(self.tmpdir) / "project").resolve()
        project_root.mkdir()
        (project_root / ".claude").mkdir()
        os.chdir(project_root)
        result = find_project_root()
        self.assertEqual(result, project_root)

    def test_finds_root_in_parent(self):
        """Should walk up to find .claude/ in a parent directory."""
        project_root = Path(self.tmpdir) / "project"
        project_root.mkdir()
        (project_root / ".claude").mkdir()
        subdir = project_root / "src" / "components"
        subdir.mkdir(parents=True)
        os.chdir(subdir)
        result = find_project_root()
        self.assertEqual(result, project_root)

    def test_returns_cwd_when_no_claude_dir(self):
        """Should return cwd when no .claude/ directory is found."""
        bare_dir = Path(self.tmpdir) / "no-claude"
        bare_dir.mkdir()
        os.chdir(bare_dir)
        result = find_project_root()
        self.assertEqual(result, bare_dir)

    def test_returns_path_object(self):
        """Should always return a Path object."""
        bare_dir = Path(self.tmpdir) / "test-dir"
        bare_dir.mkdir()
        os.chdir(bare_dir)
        result = find_project_root()
        self.assertIsInstance(result, Path)

    def test_finds_root_at_cwd_level(self):
        """Should find .claude/ at the current directory level."""
        target = Path(self.tmpdir) / "root-level"
        target.mkdir()
        (target / ".claude").mkdir()
        os.chdir(target)
        result = find_project_root()
        self.assertEqual(result, target)


class TestRunEvalResultAggregation(unittest.TestCase):
    """Tests for run_eval() — result aggregation logic.

    Mocks ProcessPoolExecutor to avoid running actual subprocess queries.
    """

    def _make_eval_set(self, queries):
        """Build eval set from list of (query, should_trigger) tuples."""
        return [{"query": q, "should_trigger": st} for q, st in queries]

    @patch("scripts.run_eval.ProcessPoolExecutor")
    def test_all_pass_positive_queries(self, mock_executor_cls):
        """All should_trigger queries trigger correctly."""
        eval_set = self._make_eval_set([
            ("build my app", True),
            ("deploy to prod", True),
        ])

        # Mock futures that all return True (triggered)
        mock_executor = MagicMock()
        mock_executor_cls.return_value.__enter__ = MagicMock(return_value=mock_executor)
        mock_executor_cls.return_value.__exit__ = MagicMock(return_value=False)

        futures = []
        for item in eval_set:
            f = Future()
            f.set_result(True)
            futures.append((f, item))

        mock_executor.submit.side_effect = [f for f, _ in futures]

        # Patch as_completed to return futures in order
        with patch("scripts.run_eval.as_completed", return_value=[f for f, _ in futures]):
            result = run_eval(
                eval_set=eval_set,
                skill_name="test-skill",
                description="A test skill",
                num_workers=1,
                timeout=10,
                project_root=Path("/tmp/fake"),
                runs_per_query=1,
                trigger_threshold=0.5,
            )

        self.assertEqual(result["summary"]["total"], 2)
        self.assertEqual(result["summary"]["passed"], 2)
        self.assertEqual(result["summary"]["failed"], 0)
        self.assertEqual(result["skill_name"], "test-skill")

    @patch("scripts.run_eval.ProcessPoolExecutor")
    def test_negative_query_not_triggered_passes(self, mock_executor_cls):
        """A should_not_trigger query that doesn't trigger should pass."""
        eval_set = self._make_eval_set([
            ("what time is it", False),
        ])

        mock_executor = MagicMock()
        mock_executor_cls.return_value.__enter__ = MagicMock(return_value=mock_executor)
        mock_executor_cls.return_value.__exit__ = MagicMock(return_value=False)

        f = Future()
        f.set_result(False)  # Did not trigger — correct
        mock_executor.submit.return_value = f

        with patch("scripts.run_eval.as_completed", return_value=[f]):
            result = run_eval(
                eval_set=eval_set,
                skill_name="test-skill",
                description="A test skill",
                num_workers=1,
                timeout=10,
                project_root=Path("/tmp/fake"),
                runs_per_query=1,
                trigger_threshold=0.5,
            )

        self.assertEqual(result["summary"]["passed"], 1)
        self.assertTrue(result["results"][0]["pass"])

    @patch("scripts.run_eval.ProcessPoolExecutor")
    def test_negative_query_triggered_fails(self, mock_executor_cls):
        """A should_not_trigger query that triggers is a failure."""
        eval_set = self._make_eval_set([
            ("make coffee", False),
        ])

        mock_executor = MagicMock()
        mock_executor_cls.return_value.__enter__ = MagicMock(return_value=mock_executor)
        mock_executor_cls.return_value.__exit__ = MagicMock(return_value=False)

        f = Future()
        f.set_result(True)  # Triggered — wrong
        mock_executor.submit.return_value = f

        with patch("scripts.run_eval.as_completed", return_value=[f]):
            result = run_eval(
                eval_set=eval_set,
                skill_name="test-skill",
                description="A test skill",
                num_workers=1,
                timeout=10,
                project_root=Path("/tmp/fake"),
                runs_per_query=1,
                trigger_threshold=0.5,
            )

        self.assertEqual(result["summary"]["failed"], 1)
        self.assertFalse(result["results"][0]["pass"])

    @patch("scripts.run_eval.ProcessPoolExecutor")
    def test_trigger_threshold_respected(self, mock_executor_cls):
        """With threshold 0.5, 2/3 triggers should pass but 1/3 should fail."""
        eval_set = self._make_eval_set([
            ("deploy it", True),
        ])

        mock_executor = MagicMock()
        mock_executor_cls.return_value.__enter__ = MagicMock(return_value=mock_executor)
        mock_executor_cls.return_value.__exit__ = MagicMock(return_value=False)

        # 3 runs: True, True, False → trigger_rate = 2/3 ≈ 0.67 > 0.5 → pass
        futures = []
        for triggered in [True, True, False]:
            f = Future()
            f.set_result(triggered)
            futures.append(f)

        mock_executor.submit.side_effect = futures

        with patch("scripts.run_eval.as_completed", return_value=futures):
            result = run_eval(
                eval_set=eval_set,
                skill_name="test-skill",
                description="A test skill",
                num_workers=1,
                timeout=10,
                project_root=Path("/tmp/fake"),
                runs_per_query=3,
                trigger_threshold=0.5,
            )

        self.assertEqual(result["summary"]["passed"], 1)
        self.assertAlmostEqual(result["results"][0]["trigger_rate"], 2 / 3, places=2)

    @patch("scripts.run_eval.ProcessPoolExecutor")
    def test_failed_future_counted_as_not_triggered(self, mock_executor_cls):
        """Exceptions from futures should be counted as False (not triggered)."""
        eval_set = self._make_eval_set([
            ("build app", True),
        ])

        mock_executor = MagicMock()
        mock_executor_cls.return_value.__enter__ = MagicMock(return_value=mock_executor)
        mock_executor_cls.return_value.__exit__ = MagicMock(return_value=False)

        f = Future()
        f.set_exception(RuntimeError("subprocess died"))
        mock_executor.submit.return_value = f

        with patch("scripts.run_eval.as_completed", return_value=[f]):
            result = run_eval(
                eval_set=eval_set,
                skill_name="test-skill",
                description="A test skill",
                num_workers=1,
                timeout=10,
                project_root=Path("/tmp/fake"),
                runs_per_query=1,
                trigger_threshold=0.5,
            )

        # Should not crash; query fails
        self.assertEqual(result["summary"]["total"], 1)
        self.assertEqual(result["results"][0]["trigger_rate"], 0.0)

    @patch("scripts.run_eval.ProcessPoolExecutor")
    def test_result_includes_description(self, mock_executor_cls):
        """Result dict should include the description used."""
        eval_set = self._make_eval_set([("q1", True)])

        mock_executor = MagicMock()
        mock_executor_cls.return_value.__enter__ = MagicMock(return_value=mock_executor)
        mock_executor_cls.return_value.__exit__ = MagicMock(return_value=False)

        f = Future()
        f.set_result(True)
        mock_executor.submit.return_value = f

        with patch("scripts.run_eval.as_completed", return_value=[f]):
            result = run_eval(
                eval_set=eval_set,
                skill_name="my-skill",
                description="The best skill description",
                num_workers=1,
                timeout=10,
                project_root=Path("/tmp/fake"),
                runs_per_query=1,
                trigger_threshold=0.5,
            )

        self.assertEqual(result["description"], "The best skill description")

    @patch("scripts.run_eval.ProcessPoolExecutor")
    def test_empty_eval_set(self, mock_executor_cls):
        """Empty eval set should return zero totals."""
        mock_executor = MagicMock()
        mock_executor_cls.return_value.__enter__ = MagicMock(return_value=mock_executor)
        mock_executor_cls.return_value.__exit__ = MagicMock(return_value=False)

        with patch("scripts.run_eval.as_completed", return_value=[]):
            result = run_eval(
                eval_set=[],
                skill_name="empty",
                description="empty",
                num_workers=1,
                timeout=10,
                project_root=Path("/tmp/fake"),
                runs_per_query=1,
                trigger_threshold=0.5,
            )

        self.assertEqual(result["summary"]["total"], 0)
        self.assertEqual(result["summary"]["passed"], 0)
        self.assertEqual(result["results"], [])


if __name__ == "__main__":
    unittest.main()
