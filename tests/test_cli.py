import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from promptsnap.cli import EXIT_DRIFT, EXIT_OK, run

CASE = '{"template": "t.txt", "vars": {"word": "hi"}}'


def make_root(tmp: str, template: str = "Say {{word}}.\n") -> Path:
    root = Path(tmp)
    (root / "prompts").mkdir()
    (root / "cases").mkdir()
    (root / "prompts" / "t.txt").write_text(template)
    (root / "cases" / "c.json").write_text(CASE)
    return root


def quiet(command: str, root: Path) -> tuple[int, str, str]:
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = run(command, root)
    return code, out.getvalue(), err.getvalue()


class CliTest(unittest.TestCase):
    def test_missing_snapshot_fails_until_updated(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            self.assertEqual(quiet("check", root)[0], EXIT_DRIFT)
            self.assertEqual(quiet("update", root)[0], EXIT_OK)
            self.assertEqual(quiet("check", root)[0], EXIT_OK)

    def test_template_edit_is_reported_as_drift(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp)
            quiet("update", root)
            (root / "prompts" / "t.txt").write_text("Please say {{word}}.\n")
            code, out, _ = quiet("check", root)
            self.assertEqual(code, EXIT_DRIFT)
            self.assertIn("DRIFT   c", out)
            self.assertIn("+Please say hi.", out)

    def test_render_error_fails_without_aborting_other_cases(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = make_root(tmp, template="Say {{word}} {{other}}.\n")
            code, _, err = quiet("check", root)
            self.assertEqual(code, EXIT_DRIFT)
            self.assertIn("missing variables ['other']", err)

    def test_no_cases_is_a_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(quiet("check", Path(tmp))[0], EXIT_DRIFT)

    def test_committed_snapshots_are_current(self) -> None:
        root = Path(__file__).resolve().parent.parent
        self.assertEqual(quiet("check", root)[0], EXIT_OK)


if __name__ == "__main__":
    unittest.main()
