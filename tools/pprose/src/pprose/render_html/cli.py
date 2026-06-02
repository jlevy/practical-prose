"""argparse entry point for `pprose render`.

Takes an input path (an `.eval.md` today; other kinds in the future),
detects the kind, renders an HTML string, and writes it to disk —
either as a single self-contained file (default) or as an HTML +
sidecar `assets/` directory (`--format folder`).
"""

from __future__ import annotations

import argparse
import sys
import webbrowser
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

from pprose.render_html.inliner import write_folder_assets
from pprose.render_html.renderer import (
    RenderOpts,
    available_variants,
    render,
)


def _pprose_version() -> str:
    try:
        return version("pprose")
    except PackageNotFoundError:
        return "dev"


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="pprose render",
        description=(
            "Render a Practical Prose eval report (.eval.md) to a clean, "
            "print-friendly static HTML page."
        ),
    )
    p.add_argument(
        "input",
        type=Path,
        nargs="?",
        help="Path to an .eval.md report. Omit when using --list-variants.",
    )
    p.add_argument(
        "-o",
        "--output",
        type=Path,
        default=None,
        help="Output HTML path. Default: <input-stem>.html alongside the input.",
    )
    p.add_argument(
        "--format",
        choices=("single", "folder"),
        default="single",
        help=(
            "single: self-contained HTML with inlined CSS and assets (default). "
            "folder: HTML + sibling assets/ directory."
        ),
    )
    p.add_argument(
        "--page-size",
        choices=("letter", "a4"),
        default="letter",
        help="Print page size. Default: letter.",
    )
    p.add_argument(
        "--variant",
        default="interactive",
        help=(
            "Page-layout variant. Default: interactive (one card + two "
            "hover-driven tip panels + theme toggle). Run `pprose render "
            "--list-variants` to see what's available."
        ),
    )
    p.add_argument(
        "--list-variants",
        action="store_true",
        help="Print the available variant names and exit.",
    )
    p.add_argument(
        "--open",
        action="store_true",
        dest="open_after",
        help="Open the rendered HTML in the default browser after writing.",
    )
    return p


def _default_output_path(input_path: Path) -> Path:
    name = input_path.name
    if name.endswith(".eval.md"):
        return input_path.with_name(name[: -len(".md")] + ".html")
    return input_path.with_suffix(".html")


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.list_variants:
        for name in available_variants():
            print(name)
        return 0

    if args.input is None:
        print("error: input path is required (or pass --list-variants)", file=sys.stderr)
        return 2

    input_path: Path = args.input
    if not input_path.is_file():
        print(f"error: input not found: {input_path}", file=sys.stderr)
        return 2

    opts = RenderOpts(
        page_size=args.page_size,
        variant=args.variant,
        pprose_version=_pprose_version(),
        folder_mode=(args.format == "folder"),
    )

    try:
        html = render(input_path, opts)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    out_path: Path = args.output if args.output else _default_output_path(input_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding="utf-8")

    if opts.folder_mode:
        write_folder_assets(out_path.parent)

    print(f"wrote {out_path}")
    if args.open_after:
        webbrowser.open(out_path.resolve().as_uri())
    return 0
