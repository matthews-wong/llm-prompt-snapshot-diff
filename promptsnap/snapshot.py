"""Compare rendered prompts with stored snapshots."""

from __future__ import annotations

import difflib
from dataclasses import dataclass
from pathlib import Path

from .tokens import estimate_tokens


@dataclass(frozen=True)
class Drift:
    diff: str
    token_delta: int


def compare(name: str, expected: str, actual: str) -> Drift | None:
    """Return None when identical, otherwise the unified diff and token delta."""
    if expected == actual:
        return None
    lines = difflib.unified_diff(
        expected.splitlines(keepends=True),
        actual.splitlines(keepends=True),
        fromfile=f"snapshots/{name}.txt",
        tofile=f"rendered/{name}.txt",
    )
    return Drift(diff="".join(lines), token_delta=estimate_tokens(actual) - estimate_tokens(expected))


def snapshot_path(snapshots_dir: Path, name: str) -> Path:
    return snapshots_dir / f"{name}.txt"
