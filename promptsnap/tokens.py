"""Rough token estimate for reporting prompt size drift."""

CHARS_PER_TOKEN = 4  # common rule of thumb for English; a delta, not a bill


def estimate_tokens(text: str) -> int:
    return -(-len(text) // CHARS_PER_TOKEN)
