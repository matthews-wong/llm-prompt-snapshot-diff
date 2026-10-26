"""`check` and `update` commands."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .cases import load_case, render_case
from .render import RenderError
from .snapshot import compare, snapshot_path

EXIT_OK = 0
EXIT_DRIFT = 1


def run(command: str, root: Path) -> int:
    case_files = sorted((root / "cases").glob("*.json"))
    if not case_files:
        print(f"no cases found in {root / 'cases'}", file=sys.stderr)
        return EXIT_DRIFT
    snapshots_dir = root / "snapshots"
    failures = 0
    for case_file in case_files:
        try:
            case = load_case(case_file)
            actual = render_case(case, root / "prompts")
        except RenderError as error:
            print(f"ERROR {error}", file=sys.stderr)
            failures += 1
            continue
        path = snapshot_path(snapshots_dir, case.name)
        if command == "update":
            snapshots_dir.mkdir(exist_ok=True)
            path.write_text(actual, encoding="utf-8")
            print(f"updated {path}")
            continue
        if not path.is_file():
            print(f"MISSING {path} (run `update` to create it)", file=sys.stderr)
            failures += 1
            continue
        drift = compare(case.name, path.read_text(encoding="utf-8"), actual)
        if drift is None:
            print(f"ok      {case.name}")
            continue
        print(f"DRIFT   {case.name} ({drift.token_delta:+d} tokens, estimated)")
        print(drift.diff, end="")
        failures += 1
    return EXIT_DRIFT if failures else EXIT_OK


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="promptsnap", description=__doc__)
    parser.add_argument("command", choices=["check", "update"])
    parser.add_argument("--root", type=Path, default=Path("."), help="directory holding prompts/, cases/, snapshots/")
    args = parser.parse_args(argv)
    return run(args.command, args.root)
