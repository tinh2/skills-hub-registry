#!/usr/bin/env python3
"""
test_verify_viewport.py — Unit tests for ux/design-claude/scripts/verify.py

Tests parse_viewport() — the only pure function testable without Playwright.
"""
import os
import sys
import unittest

VERIFY_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ux", "design-claude", "scripts")
sys.path.insert(0, VERIFY_DIR)
import verify


class TestParseViewport(unittest.TestCase):
    """Tests for parse_viewport() — WxH string to dict."""

    def test_standard_desktop_viewport(self):
        result = verify.parse_viewport("1440x900")
        self.assertEqual(result, {"width": 1440, "height": 900})

    def test_mobile_viewport(self):
        result = verify.parse_viewport("375x667")
        self.assertEqual(result, {"width": 375, "height": 667})

    def test_hd_viewport(self):
        result = verify.parse_viewport("1920x1080")
        self.assertEqual(result, {"width": 1920, "height": 1080})

    def test_small_square_viewport(self):
        result = verify.parse_viewport("320x320")
        self.assertEqual(result, {"width": 320, "height": 320})

    def test_returns_integer_values(self):
        result = verify.parse_viewport("800x600")
        self.assertIsInstance(result["width"], int)
        self.assertIsInstance(result["height"], int)

    def test_large_viewport(self):
        result = verify.parse_viewport("3840x2160")
        self.assertEqual(result["width"], 3840)
        self.assertEqual(result["height"], 2160)

    def test_returns_dict_with_width_and_height_keys(self):
        result = verify.parse_viewport("1280x720")
        self.assertIn("width", result)
        self.assertIn("height", result)

    def test_tablet_viewport(self):
        result = verify.parse_viewport("768x1024")
        self.assertEqual(result, {"width": 768, "height": 1024})

    def test_invalid_format_raises(self):
        with self.assertRaises((ValueError, TypeError)):
            verify.parse_viewport("1920-1080")

    def test_non_numeric_raises(self):
        with self.assertRaises((ValueError, TypeError)):
            verify.parse_viewport("widthxheight")


if __name__ == "__main__":
    unittest.main()
