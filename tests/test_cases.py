import json
import tempfile
import unittest
from pathlib import Path

from promptsnap.cases import Case, load_case, render_case
from promptsnap.render import RenderError

PROMPTS = Path(__file__).parent / "data" / "prompts"


class CasesTest(unittest.TestCase):
    def test_renders_case_from_template_file(self) -> None:
        case = Case(name="hello", template="say.txt", variables={"word": "hi"})
        self.assertEqual(render_case(case, PROMPTS), "Say hi.\n")

    def test_missing_template_names_case_and_path(self) -> None:
        case = Case(name="hello", template="nope.txt", variables={})
        with self.assertRaisesRegex(RenderError, "case hello: template .*nope.txt not found"):
            render_case(case, PROMPTS)

    def test_load_case_rejects_missing_keys(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps({"template": "say.txt"}))
            with self.assertRaisesRegex(RenderError, "bad.json: invalid case file"):
                load_case(path)

    def test_load_case_uses_file_stem_as_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "greet.json"
            path.write_text(json.dumps({"template": "say.txt", "vars": {"word": "x"}}))
            self.assertEqual(load_case(path).name, "greet")


if __name__ == "__main__":
    unittest.main()
