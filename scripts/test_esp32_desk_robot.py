#!/usr/bin/env python3
"""Smoke tests for build/esp32-desk-robot: frontmatter, shipped firmware, and
the facts the skill teaches (wiring and the display constructor) staying in
sync between SKILL.md and the starter firmware."""
import os
import re
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "build", "esp32-desk-robot")


def read(*p):
    with open(os.path.join(ROOT, *p), encoding="utf-8") as f:
        return f.read()


class Esp32DeskRobotTest(unittest.TestCase):
    def test_frontmatter(self):
        fm = read("SKILL.md").split("---")[1]
        self.assertIn("name: esp32-desk-robot", fm)
        self.assertRegex(fm, r'version: "\d+\.\d+\.\d+"')
        self.assertIn("category: build", fm)
        self.assertIn("CLAUDE_CODE", fm)

    def test_starter_files_shipped(self):
        for p in ("platformio.ini", "src/main.cpp", "src/secrets.h.example", ".gitignore"):
            self.assertTrue(os.path.exists(os.path.join(ROOT, "references", "firmware", p)), p)

    def test_wiring_matches_firmware(self):
        main = read("references", "firmware", "src", "main.cpp")
        skill = read("SKILL.md")
        self.assertIn("PIN_SDA = 21", main)
        self.assertIn("PIN_SCL = 22", main)
        self.assertRegex(skill, r"SDA\s*\|\s*GPIO21")
        self.assertRegex(skill, r"SCK / SCL\s*\|\s*GPIO22")

    def test_sh1106_constructor_and_no_secrets(self):
        main = read("references", "firmware", "src", "main.cpp")
        self.assertIn("U8G2_SH1106_128X64_NONAME_F_HW_I2C", main)
        self.assertIn("src/secrets.h", read("references", "firmware", ".gitignore"))
        self.assertFalse(re.search(r'WIFI_PASS\s+"[^"]+"', main), "no hardcoded Wi-Fi password")

    def test_loop_never_blocks(self):
        main = read("references", "firmware", "src", "main.cpp")
        loop = main[main.index("void loop()"):]
        self.assertNotIn("delay(", loop)


if __name__ == "__main__":
    unittest.main()
