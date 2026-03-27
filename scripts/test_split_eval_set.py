#!/usr/bin/env python3
"""
test_split_eval_set.py — Unit tests for split_eval_set() from run_loop.py

Tests stratified train/test splitting with deterministic seeding.
"""
import os
import sys
import unittest

SKILL_CREATOR_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "meta", "skill-creator")
sys.path.insert(0, SKILL_CREATOR_ROOT)
from scripts.run_loop import split_eval_set


class TestSplitEvalSet(unittest.TestCase):
    """Tests for split_eval_set() — stratified train/test splitting."""

    def _make_eval_set(self, n_trigger, n_no_trigger):
        """Create an eval set with specified counts."""
        evals = []
        for i in range(n_trigger):
            evals.append({"query": f"trigger-{i}", "should_trigger": True})
        for i in range(n_no_trigger):
            evals.append({"query": f"no-trigger-{i}", "should_trigger": False})
        return evals

    def test_basic_split(self):
        eval_set = self._make_eval_set(10, 10)
        train, test = split_eval_set(eval_set, holdout=0.2)
        self.assertEqual(len(train) + len(test), len(eval_set))

    def test_train_has_both_classes(self):
        eval_set = self._make_eval_set(10, 10)
        train, test = split_eval_set(eval_set, holdout=0.2)
        train_triggers = [e for e in train if e["should_trigger"]]
        train_no_triggers = [e for e in train if not e["should_trigger"]]
        self.assertGreater(len(train_triggers), 0)
        self.assertGreater(len(train_no_triggers), 0)

    def test_test_has_both_classes(self):
        eval_set = self._make_eval_set(10, 10)
        train, test = split_eval_set(eval_set, holdout=0.2)
        test_triggers = [e for e in test if e["should_trigger"]]
        test_no_triggers = [e for e in test if not e["should_trigger"]]
        self.assertGreater(len(test_triggers), 0)
        self.assertGreater(len(test_no_triggers), 0)

    def test_deterministic_with_same_seed(self):
        eval_set = self._make_eval_set(10, 10)
        train1, test1 = split_eval_set(eval_set, holdout=0.2, seed=42)
        train2, test2 = split_eval_set(eval_set, holdout=0.2, seed=42)
        self.assertEqual(
            [e["query"] for e in train1],
            [e["query"] for e in train2]
        )

    def test_different_seed_different_split(self):
        eval_set = self._make_eval_set(10, 10)
        train1, _ = split_eval_set(eval_set, holdout=0.2, seed=42)
        train2, _ = split_eval_set(eval_set, holdout=0.2, seed=99)
        # Different seeds should produce different orderings
        q1 = [e["query"] for e in train1]
        q2 = [e["query"] for e in train2]
        self.assertNotEqual(q1, q2)

    def test_minimum_one_in_test_per_class(self):
        """Even with small groups, at least 1 from each class goes to test."""
        eval_set = self._make_eval_set(2, 2)
        train, test = split_eval_set(eval_set, holdout=0.1)
        test_triggers = [e for e in test if e["should_trigger"]]
        test_no_triggers = [e for e in test if not e["should_trigger"]]
        self.assertGreaterEqual(len(test_triggers), 1)
        self.assertGreaterEqual(len(test_no_triggers), 1)

    def test_holdout_proportion(self):
        eval_set = self._make_eval_set(20, 20)
        train, test = split_eval_set(eval_set, holdout=0.3)
        # Roughly 30% holdout: ~6 trigger + ~6 no-trigger = ~12
        self.assertGreater(len(test), 4)  # At least some in test
        self.assertGreater(len(train), len(test))  # Train should be larger

    def test_no_item_in_both_sets(self):
        eval_set = self._make_eval_set(10, 10)
        train, test = split_eval_set(eval_set, holdout=0.3)
        train_queries = {e["query"] for e in train}
        test_queries = {e["query"] for e in test}
        self.assertEqual(len(train_queries & test_queries), 0)

    def test_all_items_preserved(self):
        eval_set = self._make_eval_set(8, 8)
        train, test = split_eval_set(eval_set, holdout=0.25)
        all_queries = {e["query"] for e in eval_set}
        result_queries = {e["query"] for e in train} | {e["query"] for e in test}
        self.assertEqual(all_queries, result_queries)


if __name__ == "__main__":
    unittest.main()
