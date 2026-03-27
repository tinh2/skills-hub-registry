#!/usr/bin/env python3
"""
test_aggregate_benchmark.py — Unit tests for meta/skill-creator/scripts/aggregate_benchmark.py

Tests calculate_stats(), load_run_results(), aggregate_results(), and generate_markdown().
"""
import json
import math
import os
import sys
import tempfile
import shutil
import unittest

SKILL_CREATOR_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "meta", "skill-creator")
sys.path.insert(0, SKILL_CREATOR_ROOT)
from scripts.aggregate_benchmark import (
    calculate_stats,
    load_run_results,
    aggregate_results,
    generate_benchmark,
    generate_markdown,
)
from pathlib import Path


class TestCalculateStats(unittest.TestCase):
    """Tests for calculate_stats() — statistical calculations."""

    def test_empty_list(self):
        result = calculate_stats([])
        self.assertEqual(result["mean"], 0.0)
        self.assertEqual(result["stddev"], 0.0)
        self.assertEqual(result["min"], 0.0)
        self.assertEqual(result["max"], 0.0)

    def test_single_value(self):
        result = calculate_stats([5.0])
        self.assertEqual(result["mean"], 5.0)
        self.assertEqual(result["stddev"], 0.0)
        self.assertEqual(result["min"], 5.0)
        self.assertEqual(result["max"], 5.0)

    def test_identical_values(self):
        result = calculate_stats([3.0, 3.0, 3.0])
        self.assertEqual(result["mean"], 3.0)
        self.assertEqual(result["stddev"], 0.0)
        self.assertEqual(result["min"], 3.0)
        self.assertEqual(result["max"], 3.0)

    def test_two_values(self):
        result = calculate_stats([2.0, 4.0])
        self.assertEqual(result["mean"], 3.0)
        self.assertEqual(result["min"], 2.0)
        self.assertEqual(result["max"], 4.0)
        # Sample stddev of [2, 4] = sqrt(2) ≈ 1.4142
        self.assertAlmostEqual(result["stddev"], math.sqrt(2.0), places=3)

    def test_known_values(self):
        values = [1.0, 2.0, 3.0, 4.0, 5.0]
        result = calculate_stats(values)
        self.assertEqual(result["mean"], 3.0)
        self.assertEqual(result["min"], 1.0)
        self.assertEqual(result["max"], 5.0)
        # Sample stddev of 1..5 = sqrt(10/4) = sqrt(2.5) ≈ 1.5811
        self.assertAlmostEqual(result["stddev"], math.sqrt(2.5), places=3)

    def test_values_with_decimals(self):
        result = calculate_stats([0.85, 0.90, 0.95])
        self.assertEqual(result["mean"], 0.9)
        self.assertEqual(result["min"], 0.85)
        self.assertEqual(result["max"], 0.95)

    def test_all_zeros(self):
        result = calculate_stats([0.0, 0.0, 0.0])
        self.assertEqual(result["mean"], 0.0)
        self.assertEqual(result["stddev"], 0.0)

    def test_results_are_rounded(self):
        result = calculate_stats([1.0 / 3.0])
        # Should be rounded to 4 decimal places
        self.assertEqual(result["mean"], round(1.0 / 3.0, 4))


class TestLoadRunResults(unittest.TestCase):
    """Tests for load_run_results() — loading grading.json files from benchmark dirs."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _create_grading(self, benchmark_dir, eval_name, config, run_name, grading_data):
        """Create a grading.json at the right path."""
        run_dir = Path(benchmark_dir) / eval_name / config / run_name
        run_dir.mkdir(parents=True, exist_ok=True)
        with open(run_dir / "grading.json", "w") as f:
            json.dump(grading_data, f)

    def _make_grading(self, pass_rate=1.0, passed=5, failed=0, total=5):
        return {
            "summary": {
                "pass_rate": pass_rate,
                "passed": passed,
                "failed": failed,
                "total": total,
            },
            "expectations": [{"text": "test", "passed": True, "evidence": "ok"}],
        }

    def test_empty_directory(self):
        results = load_run_results(Path(self.tmpdir))
        self.assertEqual(results, {})

    def test_single_config_single_run(self):
        self._create_grading(
            self.tmpdir, "eval-0", "with_skill", "run-1",
            self._make_grading(pass_rate=0.8, passed=4, failed=1, total=5)
        )
        results = load_run_results(Path(self.tmpdir))
        self.assertIn("with_skill", results)
        self.assertEqual(len(results["with_skill"]), 1)
        self.assertEqual(results["with_skill"][0]["pass_rate"], 0.8)

    def test_two_configs(self):
        self._create_grading(
            self.tmpdir, "eval-0", "with_skill", "run-1",
            self._make_grading(pass_rate=0.9)
        )
        self._create_grading(
            self.tmpdir, "eval-0", "without_skill", "run-1",
            self._make_grading(pass_rate=0.5)
        )
        results = load_run_results(Path(self.tmpdir))
        self.assertIn("with_skill", results)
        self.assertIn("without_skill", results)

    def test_multiple_runs(self):
        for i in range(1, 4):
            self._create_grading(
                self.tmpdir, "eval-0", "with_skill", f"run-{i}",
                self._make_grading(pass_rate=0.7 + i * 0.05)
            )
        results = load_run_results(Path(self.tmpdir))
        self.assertEqual(len(results["with_skill"]), 3)

    def test_legacy_layout_with_runs_subdir(self):
        runs_dir = Path(self.tmpdir) / "runs"
        self._create_grading(
            str(runs_dir), "eval-0", "with_skill", "run-1",
            self._make_grading(pass_rate=0.85)
        )
        results = load_run_results(Path(self.tmpdir))
        self.assertIn("with_skill", results)
        self.assertEqual(results["with_skill"][0]["pass_rate"], 0.85)

    def test_invalid_json_skipped(self):
        run_dir = Path(self.tmpdir) / "eval-0" / "with_skill" / "run-1"
        run_dir.mkdir(parents=True)
        (run_dir / "grading.json").write_text("{invalid json")
        results = load_run_results(Path(self.tmpdir))
        self.assertEqual(len(results.get("with_skill", [])), 0)

    def test_missing_grading_skipped(self):
        run_dir = Path(self.tmpdir) / "eval-0" / "with_skill" / "run-1"
        run_dir.mkdir(parents=True)
        # No grading.json file
        results = load_run_results(Path(self.tmpdir))
        # Config directory discovered but no runs loaded
        self.assertEqual(len(results.get("with_skill", [])), 0)

    def test_extracts_eval_id_from_dir_name(self):
        self._create_grading(
            self.tmpdir, "eval-5", "with_skill", "run-1",
            self._make_grading()
        )
        results = load_run_results(Path(self.tmpdir))
        self.assertEqual(results["with_skill"][0]["eval_id"], 5)

    def test_extracts_run_number(self):
        self._create_grading(
            self.tmpdir, "eval-0", "with_skill", "run-3",
            self._make_grading()
        )
        results = load_run_results(Path(self.tmpdir))
        self.assertEqual(results["with_skill"][0]["run_number"], 3)

    def test_timing_from_grading(self):
        grading = self._make_grading()
        grading["timing"] = {"total_duration_seconds": 45.2}
        self._create_grading(self.tmpdir, "eval-0", "config-a", "run-1", grading)
        results = load_run_results(Path(self.tmpdir))
        self.assertEqual(results["config-a"][0]["time_seconds"], 45.2)

    def test_timing_fallback_to_timing_json(self):
        self._create_grading(
            self.tmpdir, "eval-0", "with_skill", "run-1",
            self._make_grading()
        )
        timing_dir = Path(self.tmpdir) / "eval-0" / "with_skill" / "run-1"
        with open(timing_dir / "timing.json", "w") as f:
            json.dump({"total_duration_seconds": 30.5, "total_tokens": 1200}, f)
        results = load_run_results(Path(self.tmpdir))
        self.assertEqual(results["with_skill"][0]["time_seconds"], 30.5)
        self.assertEqual(results["with_skill"][0]["tokens"], 1200)


class TestAggregateResults(unittest.TestCase):
    """Tests for aggregate_results() — computing summary statistics from runs."""

    def test_empty_config(self):
        results = {"with_skill": []}
        summary = aggregate_results(results)
        self.assertEqual(summary["with_skill"]["pass_rate"]["mean"], 0.0)

    def test_single_config(self):
        results = {
            "with_skill": [
                {"pass_rate": 0.8, "time_seconds": 10.0, "tokens": 100},
                {"pass_rate": 1.0, "time_seconds": 20.0, "tokens": 200},
            ]
        }
        summary = aggregate_results(results)
        self.assertAlmostEqual(summary["with_skill"]["pass_rate"]["mean"], 0.9, places=3)

    def test_two_configs_delta(self):
        results = {
            "with_skill": [
                {"pass_rate": 0.9, "time_seconds": 15.0, "tokens": 150},
            ],
            "without_skill": [
                {"pass_rate": 0.5, "time_seconds": 10.0, "tokens": 100},
            ],
        }
        summary = aggregate_results(results)
        delta = summary["delta"]
        self.assertEqual(delta["pass_rate"], "+0.40")

    def test_delta_with_single_config(self):
        results = {
            "only_config": [
                {"pass_rate": 0.75, "time_seconds": 5.0, "tokens": 50},
            ]
        }
        summary = aggregate_results(results)
        self.assertIn("delta", summary)

    def test_no_configs(self):
        results = {}
        summary = aggregate_results(results)
        self.assertIn("delta", summary)


class TestGenerateMarkdown(unittest.TestCase):
    """Tests for generate_markdown() — human-readable benchmark output."""

    def _make_benchmark(self):
        return {
            "metadata": {
                "skill_name": "test-skill",
                "executor_model": "claude-sonnet",
                "timestamp": "2026-03-01T00:00:00Z",
                "evals_run": [0, 1],
                "runs_per_configuration": 3,
            },
            "run_summary": {
                "with_skill": {
                    "pass_rate": {"mean": 0.9, "stddev": 0.05, "min": 0.85, "max": 0.95},
                    "time_seconds": {"mean": 15.0, "stddev": 2.0, "min": 12.0, "max": 18.0},
                    "tokens": {"mean": 500, "stddev": 50, "min": 450, "max": 550},
                },
                "without_skill": {
                    "pass_rate": {"mean": 0.5, "stddev": 0.1, "min": 0.4, "max": 0.6},
                    "time_seconds": {"mean": 10.0, "stddev": 1.0, "min": 9.0, "max": 11.0},
                    "tokens": {"mean": 300, "stddev": 30, "min": 270, "max": 330},
                },
                "delta": {
                    "pass_rate": "+0.40",
                    "time_seconds": "+5.0",
                    "tokens": "+200",
                },
            },
            "notes": [],
        }

    def test_contains_skill_name(self):
        md = generate_markdown(self._make_benchmark())
        self.assertIn("test-skill", md)

    def test_contains_summary_table(self):
        md = generate_markdown(self._make_benchmark())
        self.assertIn("| Metric |", md)
        self.assertIn("Pass Rate", md)
        self.assertIn("Time", md)
        self.assertIn("Tokens", md)

    def test_contains_config_labels(self):
        md = generate_markdown(self._make_benchmark())
        self.assertIn("With Skill", md)
        self.assertIn("Without Skill", md)

    def test_contains_delta(self):
        md = generate_markdown(self._make_benchmark())
        self.assertIn("+0.40", md)

    def test_with_notes(self):
        bm = self._make_benchmark()
        bm["notes"] = ["First note", "Second note"]
        md = generate_markdown(bm)
        self.assertIn("## Notes", md)
        self.assertIn("- First note", md)
        self.assertIn("- Second note", md)

    def test_without_notes(self):
        md = generate_markdown(self._make_benchmark())
        self.assertNotIn("## Notes", md)

    def test_pass_rate_as_percentage(self):
        md = generate_markdown(self._make_benchmark())
        self.assertIn("90%", md)  # 0.9 * 100


class TestGenerateBenchmark(unittest.TestCase):
    """Tests for generate_benchmark() — full benchmark generation."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_generates_metadata(self):
        # Create a minimal benchmark structure
        run_dir = Path(self.tmpdir) / "eval-0" / "with_skill" / "run-1"
        run_dir.mkdir(parents=True)
        grading = {
            "summary": {"pass_rate": 0.8, "passed": 4, "failed": 1, "total": 5},
            "expectations": [{"text": "test", "passed": True, "evidence": "ok"}],
        }
        with open(run_dir / "grading.json", "w") as f:
            json.dump(grading, f)

        benchmark = generate_benchmark(Path(self.tmpdir), skill_name="my-skill")
        self.assertEqual(benchmark["metadata"]["skill_name"], "my-skill")
        self.assertIn("timestamp", benchmark["metadata"])
        self.assertIn("runs", benchmark)
        self.assertIn("run_summary", benchmark)

    def test_empty_dir_generates_empty_benchmark(self):
        benchmark = generate_benchmark(Path(self.tmpdir))
        self.assertEqual(benchmark["runs"], [])


if __name__ == "__main__":
    unittest.main()
