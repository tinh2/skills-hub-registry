#!/usr/bin/env python3
"""Smoke tests for the Parallax skill pack: frontmatter, cross-references,
credit to Replica (MIT), and no local paths or emails in published text."""
import os, re, unittest
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
PACK = {"gate": "security", "study": "review", "pain": "review",
        "spec": "spec", "verify": "qa", "ship": "deploy"}

def read(k):
    with open(os.path.join(ROOT, PACK[k], "parallax-" + k, "SKILL.md"), encoding="utf-8") as f:
        return f.read()

class ParallaxPackTest(unittest.TestCase):
    def test_frontmatter(self):
        for k in PACK:
            fm = read(k).split("---")[1]
            self.assertIn("name: parallax-" + k, fm)
            self.assertRegex(fm, r'version: "\d+\.\d+\.\d+"')
            self.assertIn("CLAUDE_CODE", fm)
            self.assertIn("Triggers:", fm)

    def test_gate_required_and_credit(self):
        for k in PACK:
            body = read(k)
            self.assertIn("Replica", body)
            self.assertIn("MIT", body)
            if k != "gate":
                self.assertIn("gate", body)

    def test_hard_stops_present(self):
        g = read("gate")
        for phrase in ("No circumvention", "Clean-room separation", "No copying of expression"):
            self.assertIn(phrase, g)

    def test_no_private_data(self):
        for k in PACK:
            self.assertNotRegex(read(k), r"/Users/|/home/[a-z]|[\w.]+@[\w-]+\.[a-z]{2,}")

if __name__ == "__main__":
    unittest.main()
