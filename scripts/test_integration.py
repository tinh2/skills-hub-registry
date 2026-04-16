#!/usr/bin/env python3
"""
test_integration.py — Integration tests for skills-hub-registry

Tests cross-module pipelines end-to-end:
1. Parse → Validate → Package pipeline
2. Benchmark aggregation end-to-end
3. Enhance skills full pipeline
4. Eval loop data flow (with mocked Claude subprocess)
5. Report generation from loop output
6. Registry-wide validation against real skills
"""
import importlib
import json
import math
import os
import shutil
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from concurrent.futures import Future

# Set up import paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
SKILL_CREATOR_ROOT = os.path.join(REPO_ROOT, "meta", "skill-creator")
sys.path.insert(0, SKILL_CREATOR_ROOT)
sys.path.insert(0, SCRIPT_DIR)

from scripts.utils import parse_skill_md
from scripts.quick_validate import validate_skill
from scripts.package_skill import package_skill, should_exclude
from scripts.aggregate_benchmark import (
    calculate_stats,
    load_run_results,
    aggregate_results,
    generate_benchmark,
    generate_markdown,
)
from scripts.generate_report import generate_html
from scripts.run_eval import find_project_root, run_eval
from scripts.run_loop import split_eval_set
from scripts.improve_description import improve_description

enhance = importlib.import_module("enhance-skills")


# ============================================================
# Shared test fixtures
# ============================================================

VALID_SKILL_CONTENT = """\
---
name: integration-test-skill
description: A skill for integration testing
---
# Integration Test Skill

Instructions for the skill go here.

## Phase 1
Do things.

## Phase 2
Do more things.
"""

VALID_SKILL_WITH_VERSION = """\
---
name: versioned-skill
description: A versioned skill for testing
version: 1
---
# Versioned Skill

Instructions here.
"""

EVAL_SET = [
    {"query": "build my app", "should_trigger": True},
    {"query": "deploy to production", "should_trigger": True},
    {"query": "run the tests", "should_trigger": True},
    {"query": "what time is it", "should_trigger": False},
    {"query": "make me coffee", "should_trigger": False},
    {"query": "tell me a joke", "should_trigger": False},
    {"query": "fix the build errors", "should_trigger": True},
    {"query": "ship the feature", "should_trigger": True},
    {"query": "how tall is mount everest", "should_trigger": False},
    {"query": "set up CI pipeline", "should_trigger": True},
]


def make_grading(pass_rate=1.0, passed=5, failed=0, total=5, time_secs=15.0, tokens=500):
    """Create a grading.json-compatible dict."""
    return {
        "summary": {
            "pass_rate": pass_rate,
            "passed": passed,
            "failed": failed,
            "total": total,
        },
        "timing": {"total_duration_seconds": time_secs},
        "execution_metrics": {
            "total_tool_calls": 10,
            "output_chars": tokens,
            "errors_encountered": 0,
        },
        "expectations": [
            {"text": f"expectation-{i}", "passed": i < passed, "evidence": "ok"}
            for i in range(total)
        ],
        "user_notes_summary": {
            "uncertainties": [],
            "needs_review": [],
            "workarounds": [],
        },
    }


# ============================================================
# 1. Parse → Validate → Package Pipeline
# ============================================================

class TestParseValidatePackagePipeline(unittest.TestCase):
    """Integration: Parse a SKILL.md → validate it → package it → verify package."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _create_skill_dir(self, name, content, extra_files=None):
        """Create a skill directory with SKILL.md and optional extra files."""
        skill_dir = Path(self.tmpdir) / name
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text(content)
        if extra_files:
            for fname, fcontent in extra_files.items():
                fpath = skill_dir / fname
                fpath.parent.mkdir(parents=True, exist_ok=True)
                fpath.write_text(fcontent)
        return skill_dir

    def test_valid_skill_parses_validates_and_packages(self):
        """Full pipeline: parse → validate → package → verify zip contents."""
        skill_dir = self._create_skill_dir(
            "my-skill",
            VALID_SKILL_CONTENT,
            extra_files={
                "scripts/helper.py": "print('helper')",
                "references/guide.md": "# Guide\nSome docs.",
            },
        )

        # Step 1: Parse
        name, desc, content = parse_skill_md(skill_dir)
        self.assertEqual(name, "integration-test-skill")
        self.assertEqual(desc, "A skill for integration testing")
        self.assertIn("Phase 1", content)

        # Step 2: Validate
        valid, msg = validate_skill(skill_dir)
        self.assertTrue(valid, f"Validation failed: {msg}")

        # Step 3: Package
        output_dir = Path(self.tmpdir) / "dist"
        output_dir.mkdir()
        result = package_skill(skill_dir, str(output_dir))
        self.assertIsNotNone(result, "Packaging returned None")
        self.assertTrue(result.exists(), f"Package file missing: {result}")

        # Step 4: Verify zip contents
        with zipfile.ZipFile(result, "r") as zf:
            names = zf.namelist()
            self.assertTrue(any("SKILL.md" in n for n in names))
            self.assertTrue(any("helper.py" in n for n in names))
            self.assertTrue(any("guide.md" in n for n in names))

    def test_invalid_skill_blocks_packaging(self):
        """A skill that fails validation should not be packaged."""
        skill_dir = self._create_skill_dir(
            "bad-skill",
            "---\ndescription: Missing name field\n---\nBody.",
        )

        # Parse should still work (it extracts what it can)
        name, desc, content = parse_skill_md(skill_dir)
        self.assertEqual(name, "")

        # Validate should fail
        valid, msg = validate_skill(skill_dir)
        self.assertFalse(valid)
        self.assertIn("name", msg.lower())

        # Package should refuse
        output_dir = Path(self.tmpdir) / "dist"
        output_dir.mkdir()
        result = package_skill(skill_dir, str(output_dir))
        self.assertIsNone(result)

    def test_package_excludes_pycache_and_node_modules(self):
        """Packaging should exclude __pycache__, node_modules, .DS_Store."""
        skill_dir = self._create_skill_dir(
            "clean-skill",
            VALID_SKILL_CONTENT,
            extra_files={
                "__pycache__/mod.pyc": "binary",
                "node_modules/pkg/index.js": "module.exports = {}",
                ".DS_Store": "binary",
                "scripts/real.py": "print('real')",
            },
        )

        output_dir = Path(self.tmpdir) / "dist"
        output_dir.mkdir()
        result = package_skill(skill_dir, str(output_dir))
        self.assertIsNotNone(result)

        with zipfile.ZipFile(result, "r") as zf:
            names = zf.namelist()
            self.assertFalse(any("__pycache__" in n for n in names))
            self.assertFalse(any("node_modules" in n for n in names))
            self.assertFalse(any(".DS_Store" in n for n in names))
            self.assertTrue(any("real.py" in n for n in names))

    def test_package_excludes_root_evals_dir(self):
        """Packaging should exclude evals/ at skill root but not nested evals."""
        skill_dir = self._create_skill_dir(
            "eval-skill",
            VALID_SKILL_CONTENT,
            extra_files={
                "evals/test.json": '{"queries": []}',
                "references/evals/nested.json": '{"ok": true}',
            },
        )

        output_dir = Path(self.tmpdir) / "dist"
        output_dir.mkdir()
        result = package_skill(skill_dir, str(output_dir))
        self.assertIsNotNone(result)

        with zipfile.ZipFile(result, "r") as zf:
            names = zf.namelist()
            # Root evals/ excluded
            self.assertFalse(any(n.endswith("evals/test.json") and n.count("/") == 2 for n in names)
                             or any("eval-skill/evals/" in n for n in names))
            # Nested evals/ NOT excluded
            self.assertTrue(any("nested.json" in n for n in names))


# ============================================================
# 2. Benchmark Aggregation End-to-End
# ============================================================

class TestBenchmarkAggregationPipeline(unittest.TestCase):
    """Integration: Create grading files → load → aggregate → generate markdown + JSON."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _create_benchmark_structure(self, configs, n_evals=2, n_runs=3):
        """Create a full benchmark directory with grading.json files."""
        for eval_idx in range(n_evals):
            for config_name, base_pass_rate in configs.items():
                for run_idx in range(1, n_runs + 1):
                    # Vary pass rate slightly per run
                    variation = (run_idx - 2) * 0.05
                    pass_rate = min(1.0, max(0.0, base_pass_rate + variation))
                    passed = int(pass_rate * 5)
                    grading = make_grading(
                        pass_rate=pass_rate,
                        passed=passed,
                        failed=5 - passed,
                        total=5,
                        time_secs=10.0 + run_idx,
                        tokens=400 + run_idx * 50,
                    )
                    run_dir = Path(self.tmpdir) / f"eval-{eval_idx}" / config_name / f"run-{run_idx}"
                    run_dir.mkdir(parents=True)
                    (run_dir / "grading.json").write_text(json.dumps(grading))

    def test_full_benchmark_pipeline(self):
        """Load → aggregate → generate benchmark JSON → generate markdown."""
        self._create_benchmark_structure({
            "with_skill": 0.85,
            "without_skill": 0.55,
        })

        # Step 1: Load
        results = load_run_results(Path(self.tmpdir))
        self.assertIn("with_skill", results)
        self.assertIn("without_skill", results)
        self.assertEqual(len(results["with_skill"]), 6)  # 2 evals × 3 runs
        self.assertEqual(len(results["without_skill"]), 6)

        # Step 2: Aggregate
        summary = aggregate_results(results)
        self.assertIn("with_skill", summary)
        self.assertIn("without_skill", summary)
        self.assertIn("delta", summary)

        # with_skill should have higher pass rate
        ws_mean = summary["with_skill"]["pass_rate"]["mean"]
        wos_mean = summary["without_skill"]["pass_rate"]["mean"]
        self.assertGreater(ws_mean, wos_mean)

        # Delta should be positive
        delta_pr = float(summary["delta"]["pass_rate"])
        self.assertGreater(delta_pr, 0)

        # Step 3: Generate full benchmark
        benchmark = generate_benchmark(Path(self.tmpdir), skill_name="test-skill")
        self.assertEqual(benchmark["metadata"]["skill_name"], "test-skill")
        self.assertEqual(len(benchmark["runs"]), 12)  # 2 configs × 2 evals × 3 runs
        self.assertIn("run_summary", benchmark)

        # Step 4: Generate markdown
        markdown = generate_markdown(benchmark)
        self.assertIn("test-skill", markdown)
        self.assertIn("With Skill", markdown)
        self.assertIn("Without Skill", markdown)
        self.assertIn("Pass Rate", markdown)
        self.assertIn("Delta", markdown)

    def test_benchmark_with_timing_json_fallback(self):
        """Timing data should fall back to timing.json when not in grading."""
        run_dir = Path(self.tmpdir) / "eval-0" / "config-a" / "run-1"
        run_dir.mkdir(parents=True)
        # Grading without timing
        grading = make_grading(time_secs=0.0)
        del grading["timing"]
        (run_dir / "grading.json").write_text(json.dumps(grading))
        # Separate timing file
        (run_dir / "timing.json").write_text(json.dumps({
            "total_duration_seconds": 42.5,
            "total_tokens": 1500,
        }))

        results = load_run_results(Path(self.tmpdir))
        self.assertEqual(results["config-a"][0]["time_seconds"], 42.5)
        self.assertEqual(results["config-a"][0]["tokens"], 1500)

    def test_benchmark_with_corrupted_runs(self):
        """Pipeline should gracefully skip corrupted grading files."""
        # One valid run
        self._create_benchmark_structure({"config-a": 0.9}, n_evals=1, n_runs=1)
        # One corrupted run
        bad_dir = Path(self.tmpdir) / "eval-0" / "config-a" / "run-2"
        bad_dir.mkdir(parents=True)
        (bad_dir / "grading.json").write_text("{corrupted json!!")

        results = load_run_results(Path(self.tmpdir))
        # Should have 1 valid result, not crash
        self.assertEqual(len(results["config-a"]), 1)

    def test_stats_through_aggregation(self):
        """Verify statistical calculations are correct through the pipeline."""
        # Create known data: 3 runs with pass rates 0.6, 0.8, 1.0
        for i, pr in enumerate([0.6, 0.8, 1.0]):
            run_dir = Path(self.tmpdir) / "eval-0" / "tested" / f"run-{i+1}"
            run_dir.mkdir(parents=True)
            (run_dir / "grading.json").write_text(json.dumps(make_grading(pass_rate=pr)))

        results = load_run_results(Path(self.tmpdir))
        summary = aggregate_results(results)

        self.assertAlmostEqual(summary["tested"]["pass_rate"]["mean"], 0.8, places=3)
        self.assertAlmostEqual(summary["tested"]["pass_rate"]["min"], 0.6, places=3)
        self.assertAlmostEqual(summary["tested"]["pass_rate"]["max"], 1.0, places=3)
        expected_stddev = math.sqrt(((0.6-0.8)**2 + (0.8-0.8)**2 + (1.0-0.8)**2) / 2)
        self.assertAlmostEqual(summary["tested"]["pass_rate"]["stddev"], round(expected_stddev, 4), places=3)


# ============================================================
# 3. Enhance Skills Pipeline
# ============================================================

class TestEnhanceSkillsPipeline(unittest.TestCase):
    """Integration: Parse skill → enhance → verify blocks added → validate still passes."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _create_skill(self, category, skill_name, content):
        skill_dir = os.path.join(self.tmpdir, category, skill_name)
        os.makedirs(skill_dir, exist_ok=True)
        filepath = os.path.join(skill_dir, "SKILL.md")
        with open(filepath, "w") as f:
            f.write(content)
        return filepath

    def test_enhance_then_validate(self):
        """Enhanced skill should still be parseable and contain all expected blocks."""
        content = VALID_SKILL_WITH_VERSION
        filepath = self._create_skill("build", "versioned-skill", content)
        skill_dir = Path(filepath).parent

        # Step 1: Parse before enhancement
        name_before, desc_before, _ = parse_skill_md(skill_dir)
        self.assertEqual(name_before, "versioned-skill")

        # Step 2: Enhance
        result = enhance.process_skill(filepath)
        self.assertTrue(result, "process_skill returned False")

        # Step 3: Verify blocks were added
        enhanced = Path(filepath).read_text()
        self.assertIn("SELF-HEALING VALIDATION", enhanced)
        self.assertIn("SELF-EVOLUTION TELEMETRY", enhanced)
        self.assertIn('version: "2"', enhanced)

        # Step 4: Parse after enhancement (should still parse correctly)
        name_after, desc_after, content_after = parse_skill_md(skill_dir)
        self.assertEqual(name_after, "versioned-skill")
        self.assertEqual(desc_after, "A versioned skill for testing")
        self.assertIn("SELF-HEALING", content_after)

    def test_enhance_combo_skill_gets_parallel_execution(self):
        """Combo skills should get PARALLEL EXECUTION block in addition to standard blocks."""
        content = '---\nname: polish\ndescription: Polish code quality\nversion: 1\n---\nInstructions.'
        filepath = self._create_skill("combo", "polish", content)

        enhance.process_skill(filepath)

        enhanced = Path(filepath).read_text()
        self.assertIn("PARALLEL EXECUTION", enhanced)
        self.assertIn("SELF-HEALING VALIDATION", enhanced)
        self.assertIn("SELF-EVOLUTION TELEMETRY", enhanced)

    def test_enhance_idempotent(self):
        """Running enhance twice should not duplicate blocks."""
        content = VALID_SKILL_WITH_VERSION
        filepath = self._create_skill("security", "sec-skill", content)

        enhance.process_skill(filepath)
        first_pass = Path(filepath).read_text()

        enhance.process_skill(filepath)
        second_pass = Path(filepath).read_text()

        # Count occurrences — should be same after second pass
        self.assertEqual(
            first_pass.upper().count("SELF-HEALING"),
            second_pass.upper().count("SELF-HEALING"),
        )
        self.assertEqual(
            first_pass.upper().count("SELF-EVOLUTION TELEMETRY"),
            second_pass.upper().count("SELF-EVOLUTION TELEMETRY"),
        )

    def test_enhance_all_categories_produce_valid_output(self):
        """Every category in SELF_HEALING produces an enhanced file with correct structure."""
        for category in enhance.SELF_HEALING:
            content = f'---\nname: test-{category}\ndescription: Test for {category}\nversion: 1\n---\nBody.'
            filepath = self._create_skill(category, f"test-{category}", content)
            result = enhance.process_skill(filepath)
            self.assertTrue(result, f"process_skill failed for category '{category}'")

            enhanced = Path(filepath).read_text()
            # Should have frontmatter
            self.assertTrue(enhanced.startswith("---"), f"Category '{category}' lost frontmatter")
            # Should have healing block
            self.assertIn("SELF-HEALING", enhanced.upper(), f"Category '{category}' missing healing")
            # Should have telemetry
            self.assertIn("SELF-EVOLUTION TELEMETRY", enhanced.upper(), f"Category '{category}' missing telemetry")
            # Should still be parseable
            skill_dir = Path(filepath).parent
            name, desc, _ = parse_skill_md(skill_dir)
            self.assertEqual(name, f"test-{category}", f"Category '{category}' broke name parsing")


# ============================================================
# 4. Eval Loop Data Flow (with mocked Claude)
# ============================================================

class TestEvalLoopDataFlow(unittest.TestCase):
    """Integration: eval set → split → run_eval → improve_description → report."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_split_preserves_all_queries(self):
        """Splitting then recombining should preserve all original queries."""
        train, test = split_eval_set(EVAL_SET, holdout=0.3, seed=42)

        all_queries = {e["query"] for e in EVAL_SET}
        split_queries = {e["query"] for e in train} | {e["query"] for e in test}
        self.assertEqual(all_queries, split_queries)

    def test_split_stratification(self):
        """Both train and test should have positive and negative examples."""
        train, test = split_eval_set(EVAL_SET, holdout=0.3, seed=42)

        for split_name, split_data in [("train", train), ("test", test)]:
            positives = [e for e in split_data if e["should_trigger"]]
            negatives = [e for e in split_data if not e["should_trigger"]]
            self.assertGreater(len(positives), 0, f"{split_name} has no positives")
            self.assertGreater(len(negatives), 0, f"{split_name} has no negatives")

    @patch("scripts.run_eval.ProcessPoolExecutor")
    def test_eval_results_feed_into_improve(self, mock_executor_cls):
        """Eval results structure should be consumable by improve_description."""
        eval_set = [
            {"query": "build app", "should_trigger": True},
            {"query": "hello world", "should_trigger": False},
        ]

        # Mock executor to return predictable results
        mock_executor = MagicMock()
        mock_executor_cls.return_value.__enter__ = MagicMock(return_value=mock_executor)
        mock_executor_cls.return_value.__exit__ = MagicMock(return_value=False)

        futures = []
        for item in eval_set:
            f = Future()
            f.set_result(item["should_trigger"])  # Perfect results
            futures.append(f)

        mock_executor.submit.side_effect = futures

        with patch("scripts.run_eval.as_completed", return_value=futures):
            eval_results = run_eval(
                eval_set=eval_set,
                skill_name="test-skill",
                description="A test skill",
                num_workers=1,
                timeout=10,
                project_root=Path("/tmp/fake"),
                runs_per_query=1,
                trigger_threshold=0.5,
            )

        # Verify eval results have the expected structure
        self.assertIn("results", eval_results)
        self.assertIn("summary", eval_results)
        self.assertIn("description", eval_results)

        # Feed into improve_description (with mocked Claude call)
        with patch("scripts.improve_description._call_claude") as mock_claude:
            mock_claude.return_value = "<new_description>Improved test skill description</new_description>"

            new_desc = improve_description(
                skill_name="test-skill",
                skill_content="# Test Skill\nDoes testing.",
                current_description="A test skill",
                eval_results=eval_results,
                history=[],
                model="claude-sonnet-4-20250514",
            )

            self.assertEqual(new_desc, "Improved test skill description")

            # Verify the prompt contained eval result data
            prompt = mock_claude.call_args[0][0]
            self.assertIn("test-skill", prompt)
            self.assertIn("A test skill", prompt)

    @patch("scripts.run_eval.ProcessPoolExecutor")
    def test_eval_results_feed_into_report(self, mock_executor_cls):
        """Eval results → history format → generate_html produces valid report."""
        eval_set = [
            {"query": "build app", "should_trigger": True},
            {"query": "unrelated", "should_trigger": False},
        ]

        mock_executor = MagicMock()
        mock_executor_cls.return_value.__enter__ = MagicMock(return_value=mock_executor)
        mock_executor_cls.return_value.__exit__ = MagicMock(return_value=False)

        futures = []
        for item in eval_set:
            f = Future()
            f.set_result(item["should_trigger"])
            futures.append(f)

        mock_executor.submit.side_effect = futures

        with patch("scripts.run_eval.as_completed", return_value=futures):
            eval_results = run_eval(
                eval_set=eval_set,
                skill_name="report-skill",
                description="A reportable skill",
                num_workers=1,
                timeout=10,
                project_root=Path("/tmp/fake"),
                runs_per_query=1,
                trigger_threshold=0.5,
            )

        # Build history entry as run_loop.py would
        history_entry = {
            "iteration": 1,
            "description": "A reportable skill",
            "train_passed": eval_results["summary"]["passed"],
            "train_failed": eval_results["summary"]["failed"],
            "train_total": eval_results["summary"]["total"],
            "train_results": eval_results["results"],
            "test_passed": None,
            "test_total": None,
            "test_results": None,
            "passed": eval_results["summary"]["passed"],
            "failed": eval_results["summary"]["failed"],
            "total": eval_results["summary"]["total"],
            "results": eval_results["results"],
        }

        report_data = {
            "original_description": "Original",
            "best_description": "A reportable skill",
            "best_score": f"{eval_results['summary']['passed']}/{eval_results['summary']['total']}",
            "iterations_run": 1,
            "holdout": 0,
            "train_size": len(eval_set),
            "test_size": 0,
            "history": [history_entry],
        }

        html = generate_html(report_data, skill_name="report-skill")
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("report-skill", html)
        self.assertIn("build app", html)
        self.assertIn("unrelated", html)
        # Should have pass/fail indicators
        self.assertTrue("✓" in html or "✗" in html)


# ============================================================
# 5. Report Generation Pipeline
# ============================================================

class TestReportGenerationPipeline(unittest.TestCase):
    """Integration: Multi-iteration loop output → HTML report with all features."""

    def _build_loop_output(self, n_iterations=3):
        """Build a realistic run_loop output with multiple iterations."""
        history = []
        train_queries = [
            {"query": "build my app", "should_trigger": True},
            {"query": "deploy to prod", "should_trigger": True},
            {"query": "what time is it", "should_trigger": False},
        ]
        test_queries = [
            {"query": "ship it", "should_trigger": True},
            {"query": "make coffee", "should_trigger": False},
        ]

        for i in range(1, n_iterations + 1):
            # Simulate improving pass rates over iterations
            train_pass_rate = min(1.0, 0.5 + i * 0.15)
            train_results = []
            for q in train_queries:
                triggered = q["should_trigger"] and (i > 1 or q["query"] != "deploy to prod")
                did_pass = triggered == q["should_trigger"] if q["should_trigger"] else (not triggered) == (not q["should_trigger"])
                if not q["should_trigger"]:
                    triggered = False
                    did_pass = True
                train_results.append({
                    "query": q["query"],
                    "should_trigger": q["should_trigger"],
                    "pass": did_pass,
                    "triggers": 3 if triggered else 0,
                    "runs": 3,
                })

            test_results = []
            for q in test_queries:
                triggered = q["should_trigger"] and i >= 2
                did_pass = (triggered == q["should_trigger"]) if q["should_trigger"] else not triggered
                if not q["should_trigger"]:
                    triggered = False
                    did_pass = True
                test_results.append({
                    "query": q["query"],
                    "should_trigger": q["should_trigger"],
                    "pass": did_pass,
                    "triggers": 3 if triggered else 0,
                    "runs": 3,
                })

            train_passed = sum(1 for r in train_results if r["pass"])
            test_passed = sum(1 for r in test_results if r["pass"])

            history.append({
                "iteration": i,
                "description": f"Description iteration {i}",
                "train_passed": train_passed,
                "train_failed": len(train_results) - train_passed,
                "train_total": len(train_results),
                "train_results": train_results,
                "test_passed": test_passed,
                "test_failed": len(test_results) - test_passed,
                "test_total": len(test_results),
                "test_results": test_results,
                "passed": train_passed,
                "failed": len(train_results) - train_passed,
                "total": len(train_results),
                "results": train_results,
            })

        best = max(history, key=lambda h: h["test_passed"])
        return {
            "exit_reason": "max_iterations (3)",
            "original_description": "Original description",
            "best_description": best["description"],
            "best_score": f"{best['test_passed']}/{best['test_total']}",
            "best_train_score": f"{best['train_passed']}/{best['train_total']}",
            "best_test_score": f"{best['test_passed']}/{best['test_total']}",
            "final_description": history[-1]["description"],
            "iterations_run": n_iterations,
            "holdout": 0.4,
            "train_size": len(train_queries),
            "test_size": len(test_queries),
            "history": history,
        }

    def test_multi_iteration_report(self):
        """Report should contain all iterations, queries, and scores."""
        data = self._build_loop_output(3)
        html = generate_html(data, skill_name="multi-iter-skill")

        # Structure checks
        self.assertIn("<!DOCTYPE html>", html)
        self.assertIn("multi-iter-skill", html)

        # All iterations present
        self.assertIn("Description iteration 1", html)
        self.assertIn("Description iteration 2", html)
        self.assertIn("Description iteration 3", html)

        # All queries in headers
        self.assertIn("build my app", html)
        self.assertIn("deploy to prod", html)
        self.assertIn("what time is it", html)
        self.assertIn("ship it", html)
        self.assertIn("make coffee", html)

        # Test columns distinguished
        self.assertIn("test-col", html)
        self.assertIn("test-result", html)

        # Score indicators present
        self.assertIn("score-", html)

    def test_report_with_auto_refresh(self):
        """Auto-refresh report should have meta refresh tag."""
        data = self._build_loop_output(1)
        html = generate_html(data, auto_refresh=True)
        self.assertIn('meta http-equiv="refresh"', html)

    def test_report_without_test_set(self):
        """Report should handle holdout=0 (no test set)."""
        data = self._build_loop_output(2)
        # Remove test data
        for h in data["history"]:
            h["test_passed"] = None
            h["test_failed"] = None
            h["test_total"] = None
            h["test_results"] = None
        data["test_size"] = 0
        data["holdout"] = 0
        data["best_test_score"] = None

        html = generate_html(data)
        self.assertIn("<!DOCTYPE html>", html)
        self.assertNotIn("test-result", html)

    def test_report_escapes_xss(self):
        """Report should escape HTML entities in descriptions and queries."""
        data = self._build_loop_output(1)
        data["history"][0]["description"] = '<script>alert("xss")</script>'
        data["original_description"] = '<img src=x onerror=alert(1)>'

        html = generate_html(data)
        self.assertNotIn("<script>", html)
        self.assertNotIn("onerror=", html)
        self.assertIn("&lt;script&gt;", html)


# ============================================================
# 6. Registry-Wide Validation
# ============================================================

class TestRegistryValidation(unittest.TestCase):
    """Integration: Validate actual skills in the registry with quick_validate."""

    def _get_skill_dirs(self, max_skills=20):
        """Get a sample of real skill directories from the registry."""
        skill_dirs = []
        for skill_md in sorted(Path(REPO_ROOT).rglob("SKILL.md")):
            # Skip .claude worktrees and test fixtures
            if ".claude" in str(skill_md) or "scripts" in str(skill_md):
                continue
            # Skip meta/skill-creator internal skills
            if "meta/skill-creator" in str(skill_md):
                continue
            skill_dirs.append(skill_md.parent)
            if len(skill_dirs) >= max_skills:
                break
        return skill_dirs

    def test_sample_registry_skills_are_parseable(self):
        """A sample of real registry skills should parse without errors."""
        skill_dirs = self._get_skill_dirs(20)
        self.assertGreater(len(skill_dirs), 0, "No skills found in registry")

        for skill_dir in skill_dirs:
            with self.subTest(skill=skill_dir.name):
                name, desc, content = parse_skill_md(skill_dir)
                self.assertTrue(len(name) > 0, f"{skill_dir.name}: empty name")
                self.assertTrue(len(desc) > 0, f"{skill_dir.name}: empty description")
                self.assertTrue(len(content) > 100, f"{skill_dir.name}: suspiciously short content")

    def test_sample_registry_skills_validate(self):
        """A sample of real registry skills should pass quick_validate."""
        skill_dirs = self._get_skill_dirs(20)
        self.assertGreater(len(skill_dirs), 0, "No skills found in registry")

        for skill_dir in skill_dirs:
            with self.subTest(skill=skill_dir.name):
                valid, msg = validate_skill(skill_dir)
                self.assertTrue(valid, f"{skill_dir.name} failed validation: {msg}")

    def test_no_duplicate_names_in_registry(self):
        """All skills in the registry should have unique names."""
        all_skill_dirs = []
        for skill_md in Path(REPO_ROOT).rglob("SKILL.md"):
            if ".claude" in str(skill_md) or "scripts" in str(skill_md):
                continue
            if "meta/skill-creator" in str(skill_md):
                continue
            all_skill_dirs.append(skill_md.parent)

        seen_names = {}
        for skill_dir in all_skill_dirs:
            try:
                name, _, _ = parse_skill_md(skill_dir)
            except (ValueError, FileNotFoundError):
                continue
            if name in seen_names:
                self.fail(
                    f"Duplicate skill name '{name}': "
                    f"found in {skill_dir} and {seen_names[name]}"
                )
            seen_names[name] = skill_dir


# ============================================================
# 7. Cross-Module Import Chain
# ============================================================

class TestCrossModuleImports(unittest.TestCase):
    """Integration: Verify import chains between modules work correctly."""

    def test_run_loop_imports_all_dependencies(self):
        """run_loop.py should successfully import from run_eval, improve_description, generate_report, utils."""
        # These imports happening without error IS the test
        from scripts.run_loop import run_loop, split_eval_set
        from scripts.run_eval import run_eval, find_project_root
        from scripts.improve_description import improve_description
        from scripts.generate_report import generate_html
        from scripts.utils import parse_skill_md
        self.assertTrue(callable(run_loop))
        self.assertTrue(callable(split_eval_set))
        self.assertTrue(callable(run_eval))
        self.assertTrue(callable(improve_description))
        self.assertTrue(callable(generate_html))
        self.assertTrue(callable(parse_skill_md))

    def test_package_skill_imports_validate(self):
        """package_skill.py should import and use validate_skill."""
        from scripts.package_skill import package_skill, should_exclude
        from scripts.quick_validate import validate_skill
        self.assertTrue(callable(package_skill))
        self.assertTrue(callable(validate_skill))
        self.assertTrue(callable(should_exclude))


# ============================================================
# 8. Improve Description with History Accumulation
# ============================================================

class TestImproveDescriptionHistoryFlow(unittest.TestCase):
    """Integration: Verify history accumulation across improvement iterations."""

    @patch("scripts.improve_description._call_claude")
    def test_history_accumulates_across_iterations(self, mock_claude):
        """Each iteration's result should feed into the next iteration's history."""
        eval_results_base = {
            "results": [
                {"query": "build app", "should_trigger": True, "pass": False, "triggers": 1, "runs": 3},
                {"query": "hello", "should_trigger": False, "pass": True, "triggers": 0, "runs": 3},
            ],
            "summary": {"passed": 1, "failed": 1, "total": 2},
        }

        history = []
        descriptions = []

        for i in range(3):
            mock_claude.return_value = f"<new_description>Iteration {i+1} description</new_description>"

            current_desc = descriptions[-1] if descriptions else "Original description"
            new_desc = improve_description(
                skill_name="evolving-skill",
                skill_content="# Evolving Skill\nInstructions.",
                current_description=current_desc,
                eval_results=eval_results_base,
                history=list(history),
                model="claude-sonnet-4-20250514",
            )

            descriptions.append(new_desc)
            history.append({
                "description": current_desc,
                "train_passed": eval_results_base["summary"]["passed"],
                "train_total": eval_results_base["summary"]["total"],
                "results": eval_results_base["results"],
            })

        # Verify 3 calls were made
        self.assertEqual(mock_claude.call_count, 3)

        # Verify later prompts include earlier history
        third_prompt = mock_claude.call_args_list[2][0][0]
        self.assertIn("PREVIOUS ATTEMPTS", third_prompt)
        self.assertIn("Original description", third_prompt)
        self.assertIn("Iteration 1 description", third_prompt)

    @patch("scripts.improve_description._call_claude")
    def test_history_with_logging(self, mock_claude):
        """Improvement with logging should create log files with correct content."""
        tmpdir = tempfile.mkdtemp()
        try:
            log_dir = Path(tmpdir) / "logs"
            mock_claude.return_value = "<new_description>Logged description</new_description>"

            eval_results = {
                "results": [
                    {"query": "q1", "should_trigger": True, "pass": True, "triggers": 3, "runs": 3},
                ],
                "summary": {"passed": 1, "failed": 0, "total": 1},
            }

            result = improve_description(
                skill_name="log-test",
                skill_content="# Log Test",
                current_description="Current",
                eval_results=eval_results,
                history=[],
                model="claude-sonnet-4-20250514",
                log_dir=log_dir,
                iteration=5,
            )

            self.assertEqual(result, "Logged description")

            # Verify log file
            log_file = log_dir / "improve_iter_5.json"
            self.assertTrue(log_file.exists())
            log_data = json.loads(log_file.read_text())
            self.assertEqual(log_data["iteration"], 5)
            self.assertEqual(log_data["final_description"], "Logged description")
            self.assertIn("prompt", log_data)
            self.assertIn("response", log_data)
            self.assertFalse(log_data["over_limit"])
        finally:
            shutil.rmtree(tmpdir)


if __name__ == "__main__":
    unittest.main()
