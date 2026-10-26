"""Load case files and render them to text."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from .render import RenderError, render


@dataclass(frozen=True)
class Case:
    name: str
    template: str
    variables: dict[str, str]


def load_case(path: Path) -> Case:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return Case(name=path.stem, template=data["template"], variables=data["vars"])
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        raise RenderError(f"{path}: invalid case file ({error!r})") from error


def render_case(case: Case, prompts_dir: Path) -> str:
    template_path = prompts_dir / case.template
    if not template_path.is_file():
        raise RenderError(f"case {case.name}: template {template_path} not found")
    return render(template_path.read_text(encoding="utf-8"), case.variables, source=case.name)
