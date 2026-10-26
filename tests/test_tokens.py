import unittest

from promptsnap.tokens import estimate_tokens


class TokensTest(unittest.TestCase):
    def test_empty_text_is_zero(self) -> None:
        self.assertEqual(estimate_tokens(""), 0)

    def test_rounds_up(self) -> None:
        self.assertEqual(estimate_tokens("abcde"), 2)


if __name__ == "__main__":
    unittest.main()
