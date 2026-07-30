#!/usr/bin/env python3
"""
test_css_token_sweep.py — Unit tests for review/css-token-sweep/scripts/sweep.py

Tests CSS custom property extraction, parsing, analysis, and report rendering.
"""
import os
import sys
import tempfile
import shutil
import unittest
from pathlib import Path

CSS_SWEEP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "review", "css-token-sweep", "scripts")
sys.path.insert(0, CSS_SWEEP_DIR)
import sweep as css_sweep


class TestExtractCssFromHtml(unittest.TestCase):
    """Tests for extract_css_from_html() — inline CSS extraction from HTML."""

    def test_empty_string_returns_empty(self):
        result = css_sweep.extract_css_from_html("")
        self.assertEqual(result, [])

    def test_html_with_no_style_tags_returns_empty(self):
        html = "<html><body><p>Hello world</p></body></html>"
        result = css_sweep.extract_css_from_html(html)
        self.assertEqual(result, [])

    def test_single_style_block_extracted(self):
        html = "<html><head><style>:root { --color: red; }</style></head></html>"
        result = css_sweep.extract_css_from_html(html)
        self.assertEqual(len(result), 1)
        self.assertIn("--color: red", result[0][0])

    def test_style_block_preserves_line_offset(self):
        html = "line1\nline2\n<style>\n:root{}</style>"
        result = css_sweep.extract_css_from_html(html)
        self.assertEqual(len(result), 1)
        css_text, offset = result[0]
        self.assertGreater(offset, 0)

    def test_multiple_style_blocks(self):
        html = "<style>a { color: red; }</style><p>text</p><style>b { color: blue; }</style>"
        result = css_sweep.extract_css_from_html(html)
        self.assertEqual(len(result), 2)

    def test_inline_style_attribute_extracted(self):
        html = '<div style="color: var(--primary)"></div>'
        result = css_sweep.extract_css_from_html(html)
        self.assertEqual(len(result), 1)
        css_text, _ = result[0]
        self.assertIn("var(--primary)", css_text)
        self.assertIn(".__inline__", css_text)

    def test_inline_style_wrapped_in_fake_selector(self):
        html = '<button style="background: var(--btn-bg)"></button>'
        result = css_sweep.extract_css_from_html(html)
        self.assertEqual(len(result), 1)
        self.assertIn(".__inline__", result[0][0])

    def test_style_tag_case_insensitive(self):
        html = "<STYLE>:root { --x: 1; }</STYLE>"
        result = css_sweep.extract_css_from_html(html)
        self.assertEqual(len(result), 1)

    def test_style_block_and_inline_both_extracted(self):
        html = '<style>:root { --a: 1; }</style><p style="color: red;"></p>'
        result = css_sweep.extract_css_from_html(html)
        self.assertEqual(len(result), 2)


class TestParseRootBlocks(unittest.TestCase):
    """Tests for parse_root_blocks() — :root block token extraction."""

    def test_empty_css_returns_empty(self):
        result = css_sweep.parse_root_blocks("", "test.css", 0)
        self.assertEqual(result, [])

    def test_simple_root_block_extracts_tokens(self):
        css = ":root { --primary: #007bff; --secondary: #6c757d; }"
        result = css_sweep.parse_root_blocks(css, "test.css", 0)
        self.assertEqual(len(result), 1)
        self.assertIn("--primary", result[0]["tokens"])
        self.assertIn("--secondary", result[0]["tokens"])
        self.assertEqual(result[0]["tokens"]["--primary"], "#007bff")

    def test_default_variant_assigned(self):
        css = ":root { --color: red; }"
        result = css_sweep.parse_root_blocks(css, "test.css", 0)
        self.assertEqual(result[0]["variant"], "_default")

    def test_theme_variant_extracted(self):
        css = ':root[data-theme="dark"] { --bg: #1a1a1a; }'
        result = css_sweep.parse_root_blocks(css, "test.css", 0)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["variant"], "dark")

    def test_multiple_root_blocks(self):
        css = ":root { --a: 1; } :root[data-theme=\"dark\"] { --a: 2; }"
        result = css_sweep.parse_root_blocks(css, "theme.css", 0)
        self.assertEqual(len(result), 2)
        variants = {r["variant"] for r in result}
        self.assertIn("_default", variants)
        self.assertIn("dark", variants)

    def test_src_field_preserved(self):
        css = ":root { --x: 1; }"
        result = css_sweep.parse_root_blocks(css, "styles/main.css", 0)
        self.assertEqual(result[0]["src"], "styles/main.css")

    def test_line_offset_applied(self):
        css = ":root { --x: 1; }"
        result_no_offset = css_sweep.parse_root_blocks(css, "f.css", 0)
        result_with_offset = css_sweep.parse_root_blocks(css, "f.css", 10)
        self.assertEqual(result_with_offset[0]["line"], result_no_offset[0]["line"] + 10)

    def test_empty_root_block(self):
        css = ":root {}"
        result = css_sweep.parse_root_blocks(css, "test.css", 0)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["tokens"], {})

    def test_token_values_stripped_of_whitespace(self):
        css = ":root { --gap:   16px   ; }"
        result = css_sweep.parse_root_blocks(css, "test.css", 0)
        self.assertEqual(result[0]["tokens"]["--gap"], "16px")


class TestFindVarRefs(unittest.TestCase):
    """Tests for find_var_refs() — var() reference scanning."""

    def test_empty_css_returns_empty(self):
        result = css_sweep.find_var_refs("", "test.css", 0)
        self.assertEqual(result, [])

    def test_single_var_ref(self):
        css = "a { color: var(--primary); }"
        result = css_sweep.find_var_refs(css, "test.css", 0)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "--primary")

    def test_var_without_fallback(self):
        css = "a { color: var(--color); }"
        result = css_sweep.find_var_refs(css, "test.css", 0)
        self.assertFalse(result[0]["has_fallback"])

    def test_var_with_fallback(self):
        css = "a { color: var(--color, red); }"
        result = css_sweep.find_var_refs(css, "test.css", 0)
        self.assertTrue(result[0]["has_fallback"])

    def test_multiple_var_refs(self):
        css = "a { color: var(--text); background: var(--bg); }"
        result = css_sweep.find_var_refs(css, "test.css", 0)
        self.assertEqual(len(result), 2)
        names = {r["name"] for r in result}
        self.assertIn("--text", names)
        self.assertIn("--bg", names)

    def test_src_preserved(self):
        css = "a { color: var(--x); }"
        result = css_sweep.find_var_refs(css, "components/button.css", 0)
        self.assertEqual(result[0]["src"], "components/button.css")

    def test_context_snippet_included(self):
        css = "button { background-color: var(--btn-bg); }"
        result = css_sweep.find_var_refs(css, "test.css", 0)
        self.assertIn("var(--btn-bg)", result[0]["context"])

    def test_var_with_whitespace_in_parens(self):
        css = "a { color: var( --primary ); }"
        result = css_sweep.find_var_refs(css, "test.css", 0)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "--primary")

    def test_line_offset_applied(self):
        css = "a { color: var(--x); }"
        result_no_offset = css_sweep.find_var_refs(css, "f.css", 0)
        result_with_offset = css_sweep.find_var_refs(css, "f.css", 5)
        self.assertEqual(result_with_offset[0]["line"], result_no_offset[0]["line"] + 5)


class TestSuggest(unittest.TestCase):
    """Tests for _suggest() — token name fuzzy matching."""

    def test_exact_match_returned(self):
        defined = {"--primary", "--secondary", "--bg"}
        matches = css_sweep._suggest("--primary", defined)
        self.assertIn("--primary", matches)

    def test_close_match_returned(self):
        defined = {"--primary-color", "--secondary", "--bg"}
        matches = css_sweep._suggest("--primary-colour", defined)
        self.assertIsInstance(matches, list)

    def test_no_match_returns_empty(self):
        defined = {"--completely-unrelated"}
        matches = css_sweep._suggest("--xyz123", defined)
        self.assertEqual(matches, [])

    def test_empty_defined_returns_empty(self):
        matches = css_sweep._suggest("--primary", set())
        self.assertEqual(matches, [])

    def test_returns_at_most_3_matches(self):
        defined = {"--color-1", "--color-2", "--color-3", "--color-4", "--color-5"}
        matches = css_sweep._suggest("--color-0", defined)
        self.assertLessEqual(len(matches), 3)


class TestFixSuggestion(unittest.TestCase):
    """Tests for _fix_suggestion() — fix message generation."""

    def test_close_match_generates_did_you_mean(self):
        ref = {"name": "--primary-colour", "src": "test.css", "line": 5}
        defined = {"--primary-color", "--secondary"}
        fix = css_sweep._fix_suggestion(ref, defined)
        self.assertIn("Did you mean", fix)
        self.assertIn("var(", fix)

    def test_no_match_generates_define_or_replace(self):
        ref = {"name": "--nonexistent-token", "src": "test.css", "line": 3}
        defined = {"--completely-different"}
        fix = css_sweep._fix_suggestion(ref, defined)
        self.assertIn("--nonexistent-token", fix)

    def test_empty_defined_returns_generic_fix(self):
        ref = {"name": "--missing", "src": "a.css", "line": 1}
        fix = css_sweep._fix_suggestion(ref, set())
        self.assertIsInstance(fix, str)
        self.assertGreater(len(fix), 0)


class TestRenderMarkdown(unittest.TestCase):
    """Tests for render_markdown() — markdown report generation."""

    def _make_clean_result(self):
        return {
            "errors": [],
            "warnings": [],
            "info": [],
            "stats": {"sources": 5, "tokens_default": 12, "tokens_variants": {}, "var_refs": 20, "errors": 0, "warnings": 0},
        }

    def test_clean_result_shows_no_issues_message(self):
        result = self._make_clean_result()
        md = css_sweep.render_markdown(result, "/project")
        self.assertIn("Clean", md)

    def test_stats_line_shows_counts(self):
        result = self._make_clean_result()
        md = css_sweep.render_markdown(result, "/project")
        self.assertIn("5 files scanned", md)
        self.assertIn("12 default tokens", md)

    def test_errors_section_present_when_errors_exist(self):
        result = self._make_clean_result()
        result["errors"] = [{
            "kind": "undefined-var",
            "var": "--missing-token",
            "src": "app.css",
            "line": 42,
            "context": "background: var(--missing-token)",
            "fix": "Define --missing-token in :root.",
        }]
        result["stats"]["errors"] = 1
        md = css_sweep.render_markdown(result, "/project")
        self.assertIn("Errors", md)
        self.assertIn("--missing-token", md)
        self.assertIn("app.css:42", md)

    def test_warnings_section_present_when_warnings_exist(self):
        result = self._make_clean_result()
        result["warnings"] = [{
            "kind": "undefined-var-with-fallback",
            "var": "--maybe-missing",
            "src": "app.css",
            "line": 10,
            "context": "color: var(--maybe-missing, red)",
            "fix": "Check if --maybe-missing should be defined.",
        }]
        result["stats"]["warnings"] = 1
        md = css_sweep.render_markdown(result, "/project")
        self.assertIn("--maybe-missing", md)

    def test_header_contains_root_path(self):
        result = self._make_clean_result()
        md = css_sweep.render_markdown(result, "/my/project/path")
        self.assertIn("/my/project/path", md)

    def test_no_clean_message_when_errors_present(self):
        result = self._make_clean_result()
        result["errors"] = [{
            "kind": "undefined-var",
            "var": "--x",
            "src": "a.css",
            "line": 1,
            "context": "color: var(--x)",
            "fix": "Define it.",
        }]
        md = css_sweep.render_markdown(result, "/project")
        self.assertNotIn("Clean.", md)


class TestAnalyze(unittest.TestCase):
    """Tests for analyze() — full CSS token analysis pipeline."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _write_css(self, filename, content):
        path = Path(self.tmpdir) / filename
        path.write_text(content)
        return path

    def test_empty_directory_returns_no_findings(self):
        result = css_sweep.analyze(Path(self.tmpdir))
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])

    def test_no_sources_returns_empty_stats(self):
        result = css_sweep.analyze(Path(self.tmpdir))
        self.assertEqual(result["stats"]["sources"], 0)

    def test_defined_and_referenced_token_no_error(self):
        self._write_css("styles.css", ":root { --primary: #007bff; } a { color: var(--primary); }")
        result = css_sweep.analyze(Path(self.tmpdir))
        self.assertEqual(result["errors"], [])

    def test_undefined_referenced_token_is_error(self):
        self._write_css("styles.css", "a { color: var(--undefined-token); }")
        result = css_sweep.analyze(Path(self.tmpdir))
        self.assertEqual(len(result["errors"]), 1)
        self.assertEqual(result["errors"][0]["kind"], "undefined-var")
        self.assertEqual(result["errors"][0]["var"], "--undefined-token")

    def test_undefined_with_fallback_is_warning_not_error(self):
        self._write_css("styles.css", "a { color: var(--undefined-token, red); }")
        result = css_sweep.analyze(Path(self.tmpdir))
        self.assertEqual(result["errors"], [])
        warning_kinds = [w["kind"] for w in result["warnings"]]
        self.assertIn("undefined-var-with-fallback", warning_kinds)

    def test_ignored_tokens_not_reported(self):
        self._write_css("styles.css", "a { color: var(--runtime-set); }")
        result = css_sweep.analyze(Path(self.tmpdir), ignore=["--runtime-set"])
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["warnings"], [])

    def test_skip_warnings_suppresses_theme_and_color_warnings(self):
        # skip_warnings suppresses theme-token-not-overridden and hardcoded-color,
        # but NOT undefined-var-with-fallback (that's a separate error-level smell)
        self._write_css("styles.css",
            ':root { --ink: #000; } '
            ':root[data-theme="dark"] { } '
            'p { color: var(--ink); }')
        result_with = css_sweep.analyze(Path(self.tmpdir), skip_warnings=False)
        result_without = css_sweep.analyze(Path(self.tmpdir), skip_warnings=True)
        theme_warns_with = [w for w in result_with["warnings"] if w["kind"] == "theme-token-not-overridden"]
        theme_warns_without = [w for w in result_without["warnings"] if w["kind"] == "theme-token-not-overridden"]
        self.assertGreater(len(theme_warns_with), 0)
        self.assertEqual(len(theme_warns_without), 0)

    def test_stats_count_sources(self):
        self._write_css("a.css", ":root { --x: 1; }")
        self._write_css("b.css", "p { color: red; }")
        result = css_sweep.analyze(Path(self.tmpdir))
        self.assertGreaterEqual(result["stats"]["sources"], 2)

    def test_stats_count_tokens(self):
        self._write_css("styles.css", ":root { --color-a: red; --color-b: blue; }")
        result = css_sweep.analyze(Path(self.tmpdir))
        self.assertEqual(result["stats"]["tokens_default"], 2)

    def test_hardcoded_color_duplicating_token_is_warning(self):
        self._write_css("styles.css", ":root { --primary: #ff0000; } a { color: #ff0000; }")
        result = css_sweep.analyze(Path(self.tmpdir))
        hardcoded = [w for w in result["warnings"] if w["kind"] == "hardcoded-color"]
        self.assertEqual(len(hardcoded), 1)
        self.assertEqual(hardcoded[0]["token"], "--primary")

    def test_theme_variant_token_missing_is_warning(self):
        self._write_css("styles.css",
            ':root { --ink: #000; } '
            ':root[data-theme="dark"] { --other: #fff; } '
            'p { color: var(--ink); }')
        result = css_sweep.analyze(Path(self.tmpdir))
        theme_warns = [w for w in result["warnings"] if w["kind"] == "theme-token-not-overridden"]
        self.assertGreater(len(theme_warns), 0)
        self.assertEqual(theme_warns[0]["variant"], "dark")

    def test_html_file_inline_style_scanned(self):
        path = Path(self.tmpdir) / "index.html"
        path.write_text('<html><head><style>a { color: var(--undefined); }</style></head></html>')
        result = css_sweep.analyze(Path(self.tmpdir))
        self.assertEqual(len(result["errors"]), 1)

    def test_node_modules_skipped(self):
        nm = Path(self.tmpdir) / "node_modules"
        nm.mkdir()
        (nm / "lib.css").write_text("a { color: var(--not-defined); }")
        result = css_sweep.analyze(Path(self.tmpdir))
        self.assertEqual(result["errors"], [])

    def test_multiple_errors_reported(self):
        self._write_css("styles.css",
            "a { color: var(--missing-a); background: var(--missing-b); }")
        result = css_sweep.analyze(Path(self.tmpdir))
        self.assertEqual(len(result["errors"]), 2)


class TestDiscoverSources(unittest.TestCase):
    """Tests for discover_sources() — source file discovery."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_css_file_discovered(self):
        (Path(self.tmpdir) / "styles.css").write_text(":root { --x: 1; }")
        sources = list(css_sweep.discover_sources(Path(self.tmpdir)))
        paths = [str(p) for p, _ in sources]
        self.assertTrue(any("styles.css" in p for p in paths))
        kinds = [k for _, k in sources]
        self.assertIn("css", kinds)

    def test_html_file_discovered(self):
        (Path(self.tmpdir) / "index.html").write_text("<html></html>")
        sources = list(css_sweep.discover_sources(Path(self.tmpdir)))
        kinds = [k for _, k in sources]
        self.assertIn("html", kinds)

    def test_tsx_file_discovered(self):
        (Path(self.tmpdir) / "Button.tsx").write_text("export default () => null;")
        sources = list(css_sweep.discover_sources(Path(self.tmpdir)))
        kinds = [k for _, k in sources]
        self.assertIn("html", kinds)

    def test_node_modules_excluded(self):
        nm = Path(self.tmpdir) / "node_modules"
        nm.mkdir()
        (nm / "lib.css").write_text(":root { --x: 1; }")
        sources = list(css_sweep.discover_sources(Path(self.tmpdir)))
        paths = [str(p) for p, _ in sources]
        self.assertFalse(any("node_modules" in p for p in paths))

    def test_git_dir_excluded(self):
        git = Path(self.tmpdir) / ".git"
        git.mkdir()
        (git / "HEAD").write_text("ref: refs/heads/main")
        sources = list(css_sweep.discover_sources(Path(self.tmpdir)))
        paths = [str(p) for p, _ in sources]
        self.assertFalse(any(".git" in p for p in paths))

    def test_single_css_file_path_yields_css(self):
        css_file = Path(self.tmpdir) / "app.css"
        css_file.write_text(":root {}")
        sources = list(css_sweep.discover_sources(css_file))
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0][1], "css")

    def test_single_html_file_path_yields_html(self):
        html_file = Path(self.tmpdir) / "index.html"
        html_file.write_text("<html></html>")
        sources = list(css_sweep.discover_sources(html_file))
        self.assertEqual(len(sources), 1)
        self.assertEqual(sources[0][1], "html")

    def test_non_css_non_html_file_not_yielded(self):
        (Path(self.tmpdir) / "readme.md").write_text("# Hello")
        sources = list(css_sweep.discover_sources(Path(self.tmpdir)))
        self.assertEqual(sources, [])

    def test_empty_directory_yields_nothing(self):
        sources = list(css_sweep.discover_sources(Path(self.tmpdir)))
        self.assertEqual(sources, [])


if __name__ == "__main__":
    unittest.main()
