"""Strict `{{name}}` template rendering."""

from __future__ import annotations

import re
from typing import Mapping

PLACEHOLDER = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")


class RenderError(ValueError):
    """Raised when variables and template placeholders disagree."""


def placeholders(template: str) -> set[str]:
    return set(PLACEHOLDER.findall(template))


def render(template: str, variables: Mapping[str, str], *, source: str = "template") -> str:
    """Substitute every placeholder; reject missing and unused variables.

    Unused variables are an error because a snapshot that silently ignores
    an input would stay green while the case no longer tests what it says.
    """
    needed = placeholders(template)
    missing = sorted(needed - variables.keys())
    if missing:
        raise RenderError(f"{source}: missing variables {missing}")
    unused = sorted(variables.keys() - needed)
    if unused:
        raise RenderError(f"{source}: unused variables {unused}")
    return PLACEHOLDER.sub(lambda match: str(variables[match.group(1)]), template)
