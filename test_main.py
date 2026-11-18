import tempfile
import unittest
from pathlib import Path

from main import (
    brute_force_subset_sum,
    dynamic_subset_sum,
    meet_in_the_middle_subset_sum,
    read_instance,
)


class SubsetSumTests(unittest.TestCase):
    def test_all_algorithms_find_a_subset(self):
        numbers = [3, 7, 8, 10]
        for algorithm in (
            brute_force_subset_sum,
            dynamic_subset_sum,
            meet_in_the_middle_subset_sum,
        ):
            with self.subTest(algorithm=algorithm.__name__):
                self.assertTrue(algorithm(numbers, 15))

    def test_all_algorithms_reject_a_missing_subset(self):
        numbers = [2, 4, 6]
        for algorithm in (
            brute_force_subset_sum,
            dynamic_subset_sum,
            meet_in_the_middle_subset_sum,
        ):
            with self.subTest(algorithm=algorithm.__name__):
                self.assertFalse(algorithm(numbers, 5))

    def test_dynamic_programming_handles_zero_and_negative_targets(self):
        self.assertTrue(dynamic_subset_sum([0, 3], 0))
        self.assertFalse(dynamic_subset_sum([1, 2], -1))

    def test_read_instance(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "instance.txt"
            path.write_text("# sample\ntarget: 12\n1\n5\n7\n", encoding="utf-8")
            target, numbers = read_instance(path)
        self.assertEqual(target, 12)
        self.assertEqual(numbers, [1, 5, 7])


if __name__ == "__main__":
    unittest.main()
