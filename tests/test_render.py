import unittest

from promptsnap.render import RenderError, render


class RenderTest(unittest.TestCase):
    def test_substitutes_placeholders(self) -> None:
        self.assertEqual(render("Hi {{name}}, {{ name }}!", {"name": "Ada"}), "Hi Ada, Ada!")

    def test_missing_variable_names_the_source(self) -> None:
        with self.assertRaisesRegex(RenderError, r"greet.txt: missing variables \['name'\]"):
            render("Hi {{name}}", {}, source="greet.txt")

    def test_unused_variable_is_rejected(self) -> None:
        with self.assertRaisesRegex(RenderError, r"unused variables \['extra'\]"):
            render("Hi", {"extra": "x"})

    def test_substituted_text_is_not_rescanned(self) -> None:
        # A value that looks like a placeholder must stay literal.
        self.assertEqual(render("{{a}}", {"a": "{{b}}"}), "{{b}}")


if __name__ == "__main__":
    unittest.main()
