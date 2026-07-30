#!/usr/bin/env python3
"""
test_generate_review.py — Unit tests for meta/skill-creator/eval-viewer/generate_review.py

Tests file embedding, run discovery, HTML generation, and feedback loading.
"""
import base64
import json
import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path

EVAL_VIEWER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "meta", "skill-creator", "eval-viewer")
sys.path.insert(0, EVAL_VIEWER_DIR)
import generate_review


class TestGetMimeType(unittest.TestCase):
    """Tests for get_mime_type() — MIME type resolution."""

    def _path(self, filename):
        return Path(filename)

    def test_svg_returns_override(self):
        mime = generate_review.get_mime_type(self._path("icon.svg"))
        self.assertEqual(mime, "image/svg+xml")

    def test_xlsx_returns_override(self):
        mime = generate_review.get_mime_type(self._path("report.xlsx"))
        self.assertEqual(mime, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    def test_docx_returns_override(self):
        mime = generate_review.get_mime_type(self._path("doc.docx"))
        self.assertEqual(mime, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")

    def test_pptx_returns_override(self):
        mime = generate_review.get_mime_type(self._path("slides.pptx"))
        self.assertEqual(mime, "application/vnd.openxmlformats-officedocument.presentationml.presentation")

    def test_png_returns_image_mime(self):
        mime = generate_review.get_mime_type(self._path("screenshot.png"))
        self.assertIn("image", mime)

    def test_unknown_extension_returns_octet_stream(self):
        mime = generate_review.get_mime_type(self._path("data.xyzzy"))
        self.assertEqual(mime, "application/octet-stream")

    def test_extension_check_is_case_insensitive(self):
        mime_lower = generate_review.get_mime_type(self._path("image.SVG"))
        mime_upper = generate_review.get_mime_type(self._path("image.svg"))
        self.assertEqual(mime_lower, mime_upper)


class TestEmbedFile(unittest.TestCase):
    """Tests for embed_file() — file content embedding."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _write(self, filename, content, mode="w"):
        path = Path(self.tmpdir) / filename
        with open(path, mode) as f:
            f.write(content)
        return path

    def test_markdown_file_embedded_as_text(self):
        path = self._write("output.md", "# Result\nSome content here.")
        result = generate_review.embed_file(path)
        self.assertEqual(result["type"], "text")
        self.assertEqual(result["name"], "output.md")
        self.assertIn("# Result", result["content"])

    def test_python_file_embedded_as_text(self):
        path = self._write("script.py", "print('hello')")
        result = generate_review.embed_file(path)
        self.assertEqual(result["type"], "text")

    def test_json_file_embedded_as_text(self):
        path = self._write("data.json", '{"key": "value"}')
        result = generate_review.embed_file(path)
        self.assertEqual(result["type"], "text")

    def test_png_file_embedded_as_image(self):
        # Write minimal valid PNG (1x1 transparent)
        png_bytes = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="
        )
        path = Path(self.tmpdir) / "test.png"
        path.write_bytes(png_bytes)
        result = generate_review.embed_file(path)
        self.assertEqual(result["type"], "image")
        self.assertIn("data:image/", result["data_uri"])
        self.assertIn(";base64,", result["data_uri"])

    def test_xlsx_file_embedded_as_xlsx(self):
        path = Path(self.tmpdir) / "report.xlsx"
        path.write_bytes(b"PK\x03\x04fakezip")
        result = generate_review.embed_file(path)
        self.assertEqual(result["type"], "xlsx")
        self.assertIn("data_b64", result)

    def test_pdf_file_embedded_as_pdf(self):
        path = Path(self.tmpdir) / "doc.pdf"
        path.write_bytes(b"%PDF-1.4 fake content")
        result = generate_review.embed_file(path)
        self.assertEqual(result["type"], "pdf")
        self.assertIn("data_uri", result)

    def test_unknown_binary_embedded_as_binary(self):
        path = Path(self.tmpdir) / "data.bin"
        path.write_bytes(b"\x00\x01\x02\x03\xff\xfe")
        result = generate_review.embed_file(path)
        self.assertEqual(result["type"], "binary")
        self.assertIn("data_uri", result)

    def test_name_field_is_filename_only(self):
        path = self._write("nested_output.txt", "content")
        result = generate_review.embed_file(path)
        self.assertEqual(result["name"], "nested_output.txt")

    def test_text_file_replaces_unreadable_bytes(self):
        path = Path(self.tmpdir) / "latin.txt"
        path.write_bytes(b"hello \xff world")
        result = generate_review.embed_file(path)
        self.assertEqual(result["type"], "text")
        self.assertIn("hello", result["content"])


class TestBuildRun(unittest.TestCase):
    """Tests for build_run() — run directory parsing."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.root = Path(self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _make_run_dir(self, name="run-001"):
        run_dir = self.root / name
        run_dir.mkdir(parents=True)
        outputs = run_dir / "outputs"
        outputs.mkdir()
        return run_dir

    def test_run_with_eval_metadata_extracts_prompt(self):
        run_dir = self._make_run_dir()
        (run_dir / "eval_metadata.json").write_text(
            json.dumps({"prompt": "Write a function to sort a list.", "eval_id": 1})
        )
        result = generate_review.build_run(self.root, run_dir)
        self.assertEqual(result["prompt"], "Write a function to sort a list.")

    def test_run_with_eval_metadata_extracts_eval_id(self):
        run_dir = self._make_run_dir()
        (run_dir / "eval_metadata.json").write_text(json.dumps({"prompt": "Test", "eval_id": 42}))
        result = generate_review.build_run(self.root, run_dir)
        self.assertEqual(result["eval_id"], 42)

    def test_run_without_prompt_uses_fallback(self):
        run_dir = self._make_run_dir()
        result = generate_review.build_run(self.root, run_dir)
        self.assertEqual(result["prompt"], "(No prompt found)")

    def test_run_with_transcript_md_extracts_prompt(self):
        run_dir = self._make_run_dir()
        (run_dir / "transcript.md").write_text(
            "# Session\n\n## Eval Prompt\n\nImplement a binary search.\n\n## Response\n\nHere it is."
        )
        result = generate_review.build_run(self.root, run_dir)
        self.assertIn("binary search", result["prompt"])

    def test_run_with_output_files_collects_them(self):
        run_dir = self._make_run_dir()
        (run_dir / "outputs" / "solution.py").write_text("def sort(lst): return sorted(lst)")
        result = generate_review.build_run(self.root, run_dir)
        self.assertEqual(len(result["outputs"]), 1)
        self.assertEqual(result["outputs"][0]["name"], "solution.py")

    def test_metadata_files_excluded_from_outputs(self):
        run_dir = self._make_run_dir()
        for fname in ["transcript.md", "user_notes.md", "metrics.json", "result.py"]:
            (run_dir / "outputs" / fname).write_text("content")
        result = generate_review.build_run(self.root, run_dir)
        output_names = [o["name"] for o in result["outputs"]]
        self.assertNotIn("transcript.md", output_names)
        self.assertNotIn("user_notes.md", output_names)
        self.assertNotIn("metrics.json", output_names)
        self.assertIn("result.py", output_names)

    def test_run_with_grading_json_includes_grading(self):
        run_dir = self._make_run_dir()
        grading_data = {"score": 8, "max": 10, "notes": "Good work"}
        (run_dir / "grading.json").write_text(json.dumps(grading_data))
        result = generate_review.build_run(self.root, run_dir)
        self.assertIsNotNone(result["grading"])
        self.assertEqual(result["grading"]["score"], 8)

    def test_run_without_grading_has_none(self):
        run_dir = self._make_run_dir()
        result = generate_review.build_run(self.root, run_dir)
        self.assertIsNone(result["grading"])

    def test_run_id_is_relative_path(self):
        run_dir = self._make_run_dir("eval-01/run-001")
        result = generate_review.build_run(self.root, run_dir)
        self.assertIn("run-001", result["id"])
        self.assertNotIn("/", result["id"])

    def test_directory_without_outputs_has_empty_outputs_list(self):
        # build_run always returns a dict; it's the caller (_find_runs_recursive)
        # that filters out directories lacking an outputs/ subdirectory.
        empty_dir = self.root / "no-outputs"
        empty_dir.mkdir()
        result = generate_review.build_run(self.root, empty_dir)
        self.assertIsInstance(result, dict)
        self.assertEqual(result["outputs"], [])


class TestFindRuns(unittest.TestCase):
    """Tests for find_runs() — workspace run discovery."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.workspace = Path(self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _make_run(self, name, prompt="Test prompt"):
        run_dir = self.workspace / name
        run_dir.mkdir(parents=True)
        (run_dir / "outputs").mkdir()
        (run_dir / "eval_metadata.json").write_text(json.dumps({"prompt": prompt}))
        return run_dir

    def test_empty_workspace_returns_empty(self):
        result = generate_review.find_runs(self.workspace)
        self.assertEqual(result, [])

    def test_single_run_found(self):
        self._make_run("run-001")
        result = generate_review.find_runs(self.workspace)
        self.assertEqual(len(result), 1)

    def test_multiple_runs_found(self):
        self._make_run("run-001")
        self._make_run("run-002")
        self._make_run("run-003")
        result = generate_review.find_runs(self.workspace)
        self.assertEqual(len(result), 3)

    def test_runs_sorted_by_id(self):
        self._make_run("run-003")
        self._make_run("run-001")
        self._make_run("run-002")
        result = generate_review.find_runs(self.workspace)
        ids = [r["id"] for r in result]
        self.assertEqual(ids, sorted(ids))

    def test_node_modules_skipped(self):
        nm = self.workspace / "node_modules"
        nm.mkdir()
        (nm / "outputs").mkdir()
        result = generate_review.find_runs(self.workspace)
        self.assertEqual(result, [])

    def test_nested_runs_discovered(self):
        nested = self.workspace / "group-a" / "run-001"
        nested.mkdir(parents=True)
        (nested / "outputs").mkdir()
        result = generate_review.find_runs(self.workspace)
        self.assertEqual(len(result), 1)

    def test_result_has_required_keys(self):
        self._make_run("run-001", prompt="Write a test")
        result = generate_review.find_runs(self.workspace)
        run = result[0]
        self.assertIn("id", run)
        self.assertIn("prompt", run)
        self.assertIn("outputs", run)
        self.assertIn("grading", run)


class TestLoadPreviousIteration(unittest.TestCase):
    """Tests for load_previous_iteration() — previous feedback loading."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.workspace = Path(self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _make_run(self, name):
        run_dir = self.workspace / name
        run_dir.mkdir(parents=True)
        (run_dir / "outputs").mkdir()
        return run_dir

    def test_empty_workspace_returns_empty(self):
        result = generate_review.load_previous_iteration(self.workspace)
        self.assertEqual(result, {})

    def test_feedback_json_loaded(self):
        run_dir = self._make_run("run-001")
        feedback_data = {
            "reviews": [{"run_id": "run-001", "feedback": "Good output"}]
        }
        (self.workspace / "feedback.json").write_text(json.dumps(feedback_data))
        result = generate_review.load_previous_iteration(self.workspace)
        self.assertIn("run-001", result)
        self.assertEqual(result["run-001"]["feedback"], "Good output")

    def test_empty_feedback_not_included(self):
        self._make_run("run-001")
        feedback_data = {
            "reviews": [{"run_id": "run-001", "feedback": "   "}]
        }
        (self.workspace / "feedback.json").write_text(json.dumps(feedback_data))
        result = generate_review.load_previous_iteration(self.workspace)
        if "run-001" in result:
            self.assertEqual(result["run-001"].get("feedback", ""), "")

    def test_run_outputs_included_in_result(self):
        run_dir = self._make_run("run-001")
        (run_dir / "outputs" / "answer.md").write_text("# Answer")
        result = generate_review.load_previous_iteration(self.workspace)
        self.assertIn("run-001", result)
        self.assertIn("outputs", result["run-001"])

    def test_malformed_feedback_json_handled_gracefully(self):
        (self.workspace / "feedback.json").write_text("not valid json {{{{")
        result = generate_review.load_previous_iteration(self.workspace)
        self.assertIsInstance(result, dict)


class TestGenerateHtml(unittest.TestCase):
    """Tests for generate_html() — standalone HTML page generation."""

    def _make_run(self, run_id="run-001", prompt="Test prompt", outputs=None):
        return {
            "id": run_id,
            "prompt": prompt,
            "eval_id": 1,
            "outputs": outputs or [],
            "grading": None,
        }

    def test_returns_string(self):
        html = generate_review.generate_html([self._make_run()], "my-skill")
        self.assertIsInstance(html, str)

    def test_html_contains_embedded_data(self):
        html = generate_review.generate_html([self._make_run()], "my-skill")
        self.assertIn("EMBEDDED_DATA", html)

    def test_skill_name_in_embedded_data(self):
        html = generate_review.generate_html([self._make_run()], "test-skill-name")
        self.assertIn("test-skill-name", html)

    def test_run_prompt_embedded(self):
        html = generate_review.generate_html([self._make_run(prompt="Sort a list")], "skill")
        self.assertIn("Sort a list", html)

    def test_empty_runs_still_generates_html(self):
        html = generate_review.generate_html([], "empty-skill")
        self.assertIsInstance(html, str)
        self.assertGreater(len(html), 100)

    def test_previous_feedback_embedded(self):
        previous = {"run-001": {"feedback": "Needs improvement", "outputs": []}}
        html = generate_review.generate_html([self._make_run()], "skill", previous=previous)
        self.assertIn("Needs improvement", html)

    def test_benchmark_data_embedded(self):
        benchmark = {"score": 9, "runs": 10}
        html = generate_review.generate_html([self._make_run()], "skill", benchmark=benchmark)
        self.assertIn("benchmark", html)

    def test_multiple_runs_all_embedded(self):
        runs = [
            self._make_run("run-001", "First prompt"),
            self._make_run("run-002", "Second prompt"),
            self._make_run("run-003", "Third prompt"),
        ]
        html = generate_review.generate_html(runs, "skill")
        self.assertIn("First prompt", html)
        self.assertIn("Second prompt", html)
        self.assertIn("Third prompt", html)


if __name__ == "__main__":
    unittest.main()
