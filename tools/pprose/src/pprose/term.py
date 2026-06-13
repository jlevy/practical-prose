"""Minimal terminal styling for the pprose CLI (standard library only).

Color is opt-in by detection: on for an interactive terminal, off for pipes, CI,
agents, and `NO_COLOR`. Call sites never branch — the style helpers emit plain text
when color is disabled, so the same code path produces clean output for a human and
byte-stable output for a machine.

Precedence for `use_color` (highest first):

1. explicit override (`--color always|never`),
2. `NO_COLOR` set -> off (https://no-color.org/),
3. `FORCE_COLOR` set -> on,
4. `CI` set or `TERM=dumb` or not a TTY -> off,
5. otherwise the stream's `isatty()`.
"""

from __future__ import annotations

import os
import shutil
import sys
from typing import TextIO

_MIN_WIDTH = 40
_MAX_WIDTH = 100
_DEFAULT_WIDTH = 80

# Set once by the CLI entry point; the style helpers read it.
_enabled = False


def use_color(stream: TextIO | None = None, override: str | None = None) -> bool:
    """Decide whether to emit ANSI color for `stream`.

    `override` is the value of `--color` (`"auto"`, `"always"`, `"never"`, or None).
    """
    if override == "always":
        return True
    if override == "never":
        return False
    stream = stream if stream is not None else sys.stdout
    if os.environ.get("NO_COLOR") is not None:
        return False
    if os.environ.get("FORCE_COLOR"):
        return True
    if os.environ.get("CI"):
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    try:
        return bool(stream.isatty())
    except Exception:
        return False


def set_enabled(enabled: bool) -> None:
    """Set whether the style helpers emit ANSI codes (called once by the CLI)."""
    global _enabled
    _enabled = enabled


def enabled() -> bool:
    return _enabled


def terminal_width(stream: TextIO | None = None) -> int:
    """Readable width: the terminal's columns clamped to [40, 100], else 80."""
    stream = stream if stream is not None else sys.stdout
    try:
        if not stream.isatty():
            return _DEFAULT_WIDTH
    except Exception:
        return _DEFAULT_WIDTH
    try:
        cols = shutil.get_terminal_size().columns
    except Exception:
        return _DEFAULT_WIDTH
    return max(_MIN_WIDTH, min(_MAX_WIDTH, cols))


def _sgr(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m" if _enabled else text


def bold(text: str) -> str:
    return _sgr("1", text)


def dim(text: str) -> str:
    return _sgr("2", text)


def heading(text: str) -> str:
    """Section headers in help and listings (bold)."""
    return _sgr("1", text)


def command(text: str) -> str:
    """A command or subcommand name (cyan)."""
    return _sgr("36", text)


def warn(text: str) -> str:
    return _sgr("33", text)


def error(text: str) -> str:
    return _sgr("1;31", text)
