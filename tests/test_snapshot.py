import unittest

from promptsnap.snapshot import compare


class CompareTest(unittest.TestCase):
    def test_identical_text_has_no_drift(self) -> None:
        self.assertIsNone(compare("a", "same\n", "same\n"))

    def test_diff_names_both_sides_and_marks_changes(self) -> None:
        drift = compare("a", "Be brief.\n", "Be very brief.\n")
        self.assertIn("--- snapshots/a.txt", drift.diff)
        self.assertIn("+++ rendered/a.txt", drift.diff)
        self.assertIn("-Be brief.", drift.diff)
        self.assertIn("+Be very brief.", drift.diff)

    def test_token_delta_is_signed(self) -> None:
        self.assertGreater(compare("a", "x", "x" * 40).token_delta, 0)
        self.assertLess(compare("a", "x" * 40, "x").token_delta, 0)


if __name__ == "__main__":
    unittest.main()
