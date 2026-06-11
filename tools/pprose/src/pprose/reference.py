"""Informational subcommands: print bundled guidelines / shortcuts / runbooks.

These don't act on anything — they emit reference text the agent reads and
follows, so the skills can stay portable (they call `pprose guidelines <name>`
instead of reading a repo-relative path that won't exist elsewhere).
"""

from __future__ import annotations

import argparse

from pprose import resources


def _doc_command(category: str, label: str, argv: list[str] | None) -> int:
    parser = argparse.ArgumentParser(
        description=f"Print a bundled {label} by name, or list them all when run with no name.",
    )
    parser.add_argument("name", nargs="?", help=f"{label} name; omit to list all {label}s")
    args = parser.parse_args(argv)

    if not args.name:
        for name in resources.list_names(category):
            print(f"{name}\t{resources.doc_title(category, name)}")
        return 0
    try:
        print(resources.read_doc(category, args.name))
    except FileNotFoundError as exc:
        parser.error(str(exc))
    return 0


def inventory_main(argv: list[str] | None = None) -> int:
    """`pprose list`: the full bundled inventory, grouped by kind."""
    kinds = ("guidelines", "shortcuts", "runbooks", "skills")
    parser = argparse.ArgumentParser(
        description="List all bundled guidelines, shortcuts, runbooks, and skills.",
    )
    parser.add_argument(
        "--kind",
        choices=kinds,
        help="list only one kind instead of all",
    )
    args = parser.parse_args(argv)

    selected = (args.kind,) if args.kind else kinds
    for i, kind in enumerate(selected):
        if i:
            print()
        if not args.kind:
            print(f"{kind}:")
        for name in resources.list_names(kind):
            print(f"  {name}\t{resources.doc_title(kind, name)}")
    return 0


def guidelines_main(argv: list[str] | None = None) -> int:
    return _doc_command("guidelines", "guideline", argv)


def shortcut_main(argv: list[str] | None = None) -> int:
    return _doc_command("shortcuts", "shortcut", argv)


def runbook_main(argv: list[str] | None = None) -> int:
    return _doc_command("runbooks", "runbook", argv)


def about_main(argv: list[str] | None = None) -> int:
    """Print the bundled `README.md` — the Practical Prose project narrative."""
    parser = argparse.ArgumentParser(
        description="Print the Practical Prose project narrative (the bundled README).",
    )
    parser.parse_args(argv)  # rejects unknown args / positional
    print(resources.read_doc("about", "readme"))
    return 0
