"""Informational subcommands: print bundled guidelines / shortcuts / runbooks.

These don't act on anything — they emit reference text the agent reads and
follows, so the skills can stay portable (they call `pprose guidelines <name>`
instead of reading a repo-relative path that won't exist elsewhere).
"""

from __future__ import annotations

import argparse

from pprose import resources


def _doc_command(category: str, label: str, argv: list[str] | None) -> int:
    parser = argparse.ArgumentParser(description=f"Print a bundled {label}.")
    parser.add_argument("name", nargs="?", help=f"{label} name (omit with --list)")
    parser.add_argument("--list", action="store_true", help=f"list available {label}s")
    args = parser.parse_args(argv)

    if args.list or not args.name:
        for name in resources.list_names(category):
            print(f"{name}\t{resources.doc_title(category, name)}")
        return 0
    try:
        print(resources.read_doc(category, args.name))
    except FileNotFoundError as exc:
        parser.error(str(exc))
    return 0


def guidelines_main(argv: list[str] | None = None) -> int:
    return _doc_command("guidelines", "guideline", argv)


def shortcut_main(argv: list[str] | None = None) -> int:
    return _doc_command("shortcuts", "shortcut", argv)


def runbook_main(argv: list[str] | None = None) -> int:
    return _doc_command("runbooks", "runbook", argv)
