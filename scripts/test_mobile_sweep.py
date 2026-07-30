#!/usr/bin/env python3
"""
test_mobile_sweep.py — Unit tests for ux/mobile-sweep/scripts/sweep.py

Tests static_css_scan() and render_report() — the two pure/filesystem
functions that don't require Playwright. sweep_url() is skipped because it
needs a live browser and a real URL.
"""
import importlib.util
import os
import sys
import shutil
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import MagicMock

# sweep.py calls sys.exit(2) at module level when playwright is absent.
# Inject a fake playwright module so the import succeeds without a browser.
_fake_playwright = types.ModuleType("playwright")
_fake_playwright.sync_api = types.ModuleType("playwright.sync_api")
_fake_playwright.sync_api.sync_playwright = MagicMock()
_fake_playwright.sync_api.TimeoutError = Exception
sys.modules.setdefault("playwright", _fake_playwright)
sys.modules.setdefault("playwright.sync_api", _fake_playwright.sync_api)

# Load the mobile sweep module under a unique name to avoid collision with
# review/css-token-sweep/scripts/sweep.py which is also imported as "sweep".
_MOBILE_SWEEP_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "ux", "mobile-sweep", "scripts", "sweep.py"
)
_spec = importlib.util.spec_from_file_location("mobile_sweep_module", _MOBILE_SWEEP_PATH)
mobile_sweep = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mobile_sweep)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

DEFAULT_BREAKPOINTS = [(360, 640, "Small Android"), (390, 844, "iPhone 13/14/15")]


class TestStaticCssScan(unittest.TestCase):
    """Tests for static_css_scan() — rigid-grid CSS heuristic scanner."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _write_css(self, filename, content):
        path = Path(self.tmpdir) / filename
        path.write_text(content, encoding="utf-8")
        return path

    # --- Happy path: rigid grid detected ---

    def test_rigid_grid_three_fixed_columns_flagged(self):
        self._write_css("layout.css", ".grid { grid-template-columns: 200px 300px 400px; }")
        warnings = mobile_sweep.static_css_scan(Path(self.tmpdir))
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0]["kind"], "rigid-grid")

    def test_rigid_grid_selector_preserved(self):
        self._write_css("layout.css", ".my-grid { grid-template-columns: 150px 150px 150px; }")
        warnings = mobile_sweep.static_css_scan(Path(self.tmpdir))
        self.assertEqual(len(warnings), 1)
        self.assertIn(".my-grid", warnings[0]["selector"])

    def test_rigid_grid_columns_value_preserved(self):
        self._write_css("layout.css", ".g { grid-template-columns: 100px 100px 100px; }")
        warnings = mobile_sweep.static_css_scan(Path(self.tmpdir))
        self.assertEqual(len(warnings), 1)
        self.assertIn("100px", warnings[0]["columns"])

    def test_rigid_grid_fixed_sum_calculated(self):
        self._write_css("layout.css", ".g { grid-template-columns: 100px 200px 300px; }")
        warnings = mobile_sweep.static_css_scan(Path(self.tmpdir))
        self.assertEqual(len(warnings), 1)
        self.assertAlmostEqual(warnings[0]["fixed_sum"], 600.0)

    def test_rigid_grid_src_path_included(self):
        self._write_css("grid.css", ".g { grid-template-columns: 200px 200px 200px; }")
        warnings = mobile_sweep.static_css_scan(Path(self.tmpdir))
        self.assertEqual(len(warnings), 1)
        self.assertIn("grid.css", warnings[0]["src"])

    def test_rigid_grid_fix_message_present(self):
        self._write_css("layout.css", ".g { grid-template-columns: 200px 200px 200px; }")
        warnings = mobile_sweep.static_css_scan(Path(self.tmpdir))
        self.assertEqual(len(warnings), 1)
        self.assertIsInstance(warnings[0]["fix"], str)
        self.assertGreater(len(warnings[0]["fix"]), 10)

    def test_rigid_grid_severity_is_warn(self):
        self._write_css("layout.css", ".g { grid-template-columns: 200px 200px 200px; }")
        warnings = mobile_sweep.static_css_scan(Path(self.tmpdir))
        self.assertEqual(warnings[0]["severity"], "warn")

    # --- Negative cases: no warning expected ---

    def test_two_fixed_columns_not_flagged(self):
        self._write_css("layout.css", ".g { grid-template-columns: 200px 300px; }")
        warnings = mobile_sweep.static_css_scan(Path(self.tmpdir))
        self.assertEqual(warnings, [])

    def test_fr_columns_not_flagged(self):
        self._write_css("layout.css", ".g { grid-template-columns: 1fr 1fr 1fr; }")
        warnings = mobile_sweep.static_css_scan(Path(self.tmpdir))
        self.assertEqual(warnings, [])

    def test_small_fixed_sum_not_flagged(self):
        # Three fixed columns but total ≤ 200px — should not trigger
        self._write_css("layout.css", ".g { grid-template-columns: 50px 60px 70px; }")
        warnings = mobile_sweep.static_css_scan(Path(self.tmpdir))
        self.assertEqual(warnings, [])

    def test_media_query_override_suppresses_warning(self):
        css = (
            ".g { grid-template-columns: 200px 200px 200px; } "
            "@media (max-width: 640px) { .g { grid-template-columns: 1fr; } }"
        )
        self._write_css("layout.css", css)
        warnings = mobile_sweep.static_css_scan(Path(self.tmpdir))
        self.assertEqual(warnings, [])

    def test_empty_directory_returns_empty(self):
        warnings = mobile_sweep.static_css_scan(Path(self.tmpdir))
        self.assertEqual(warnings, [])

    def test_node_modules_skipped(self):
        nm = Path(self.tmpdir) / "node_modules"
        nm.mkdir()
        (nm / "lib.css").write_text(".g { grid-template-columns: 200px 200px 200px; }")
        warnings = mobile_sweep.static_css_scan(Path(self.tmpdir))
        self.assertEqual(warnings, [])

    # --- Multiple files ---

    def test_multiple_css_files_all_scanned(self):
        self._write_css("a.css", ".g { grid-template-columns: 200px 200px 200px; }")
        self._write_css("b.css", ".h { grid-template-columns: 250px 250px 250px; }")
        warnings = mobile_sweep.static_css_scan(Path(self.tmpdir))
        self.assertEqual(len(warnings), 2)


class TestRenderReport(unittest.TestCase):
    """Tests for render_report() — markdown report generation."""

    _URL = "https://example.com"
    _BREAKPOINTS = DEFAULT_BREAKPOINTS
    _OUT_DIR = "mobile-sweep-out"

    def _render(self, runtime=None, static_warnings=None):
        return mobile_sweep.render_report(
            runtime or [],
            static_warnings or [],
            self._URL,
            self._BREAKPOINTS,
            self._OUT_DIR,
        )

    def _error_finding(self, kind="small-touch-target", **kwargs):
        base = {
            "kind": kind,
            "severity": "error",
            "selector": "#btn",
            "label": "Submit",
            "rect": {"x": 0, "y": 0, "w": 30, "h": 30},
            "breakpoint": "360x640 (Small Android)",
            "state": "default",
        }
        if kind == "small-touch-target":
            base.update({"width": 30, "height": 30})
        elif kind in ("off-screen", "off-screen-left"):
            base.update({"overflowPx": 10})
        elif kind == "clipped-text":
            base.update({"scrollWidth": 200, "clientWidth": 150, "clippedPx": 50})
        base.update(kwargs)
        return base

    def _warn_finding(self, kind="modal-too-wide", **kwargs):
        base = {
            "kind": kind,
            "severity": "warn",
            "selector": ".modal",
            "label": "(dialog)",
            "rect": {"x": 0, "y": 0, "w": 400, "h": 300},
            "breakpoint": "360x640 (Small Android)",
            "state": "default",
            "width": 400,
            "max": 344,
        }
        base.update(kwargs)
        return base

    # --- Header / URL ---

    def test_report_contains_url(self):
        md = self._render()
        self.assertIn("https://example.com", md)

    def test_report_contains_breakpoint_info(self):
        md = self._render()
        self.assertIn("360x640", md)

    # --- Clean state ---

    def test_clean_report_has_no_errors_or_warnings_message(self):
        md = self._render()
        self.assertIn("Clean", md)

    def test_clean_report_shows_zero_errors(self):
        md = self._render()
        self.assertIn("0 errors", md)

    def test_clean_report_shows_zero_warnings(self):
        md = self._render()
        self.assertIn("0 warnings", md)

    # --- Error findings ---

    def test_error_count_in_summary_line(self):
        md = self._render(runtime=[self._error_finding()])
        self.assertIn("1 errors", md)

    def test_errors_section_present_when_errors_exist(self):
        md = self._render(runtime=[self._error_finding()])
        self.assertIn("## Errors", md)

    def test_small_touch_target_selector_in_report(self):
        md = self._render(runtime=[self._error_finding("small-touch-target")])
        self.assertIn("#btn", md)

    def test_small_touch_target_size_in_report(self):
        md = self._render(runtime=[self._error_finding("small-touch-target")])
        self.assertIn("30×30", md)

    def test_off_screen_overflow_px_in_report(self):
        finding = self._error_finding("off-screen")
        finding["overflowPx"] = 42
        md = self._render(runtime=[finding])
        self.assertIn("42", md)

    def test_clipped_text_widths_in_report(self):
        md = self._render(runtime=[self._error_finding("clipped-text")])
        self.assertIn("200", md)
        self.assertIn("150", md)

    def test_breakpoint_in_finding_section(self):
        md = self._render(runtime=[self._error_finding()])
        self.assertIn("360x640", md)

    # --- Warning findings ---

    def test_warning_count_in_summary_line(self):
        md = self._render(runtime=[self._warn_finding()])
        self.assertIn("1 warnings", md)

    def test_runtime_warnings_section_present(self):
        md = self._render(runtime=[self._warn_finding()])
        self.assertIn("Warnings", md)

    def test_modal_width_in_report(self):
        md = self._render(runtime=[self._warn_finding("modal-too-wide")])
        self.assertIn("400", md)

    # --- Static CSS warnings ---

    def test_static_warnings_section_present(self):
        static_warn = {
            "kind": "rigid-grid",
            "severity": "warn",
            "src": "/project/layout.css",
            "line": 5,
            "selector": ".grid",
            "columns": "200px 200px 200px",
            "fixed_sum": 600,
            "fix": "Add a @media override.",
        }
        md = self._render(static_warnings=[static_warn])
        self.assertIn("static CSS scan", md)

    def test_static_warning_selector_in_report(self):
        static_warn = {
            "kind": "rigid-grid",
            "severity": "warn",
            "src": "/project/layout.css",
            "line": 5,
            "selector": ".grid",
            "columns": "200px 200px 200px",
            "fixed_sum": 600,
            "fix": "Add a @media override.",
        }
        md = self._render(static_warnings=[static_warn])
        self.assertIn(".grid", md)

    def test_static_warning_counted_in_summary(self):
        static_warn = {
            "kind": "rigid-grid",
            "severity": "warn",
            "src": "/project/layout.css",
            "line": 5,
            "selector": ".grid",
            "columns": "200px 200px 200px",
            "fixed_sum": 600,
            "fix": "Add a @media override.",
        }
        md = self._render(static_warnings=[static_warn])
        self.assertIn("1 warnings", md)

    # --- Return type ---

    def test_returns_string(self):
        md = self._render()
        self.assertIsInstance(md, str)

    def test_nonempty_report(self):
        md = self._render()
        self.assertGreater(len(md), 0)

    # --- No "Clean" when issues exist ---

    def test_no_clean_message_when_error_present(self):
        md = self._render(runtime=[self._error_finding()])
        self.assertNotIn(
            "Clean. No off-screen overflow",
            md,
        )


if __name__ == "__main__":
    unittest.main()
