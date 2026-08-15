"""Unified command entry point for the pprose package."""

from __future__ import annotations

import importlib
import sys
from collections.abc import Callable, Generator
from contextlib import contextmanager
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version

# Keep module-level imports to the standard library and pprose.term (stdlib-only).
# The subsystems are imported lazily in `_resolve()` at dispatch time so `pprose --help`,
# `--version`, and the reference listings stay fast: the eval chain
# (`eval_score`/`eval_compare`) pulls in pydantic_ai and the provider SDKs (~1s of import
# cost) that help never needs.
from pprose import term

CommandMain = Callable[[list[str] | None], int]
COLOR_CHOICES = ("auto", "always", "never")


@dataclass(frozen=True)
class CommandSpec:
    summary: str
    target: str  # "module:attr", imported lazily at dispatch (see _resolve)
    group: str


# Groups print in this order.
GROUPS = ("Evaluate", "Reference", "Setup")
PROGRAM = "pprose"

COMMANDS: dict[str, CommandSpec] = {
    "metrics": CommandSpec(
        "Compute deterministic metrics for one or more Markdown artifacts.",
        "pprose.metrics:main",
        "Evaluate",
    ),
    "report": CommandSpec(
        "Create, validate, and recompute eval reports.",
        "pprose.eval_report:main",
        "Evaluate",
    ),
    "score": CommandSpec(
        "Fill qualitative scores and rule_findings in eval reports via Pydantic AI.",
        "pprose.eval_score:main",
        "Evaluate",
    ),
    "compare": CommandSpec(
        "Compare multiple eval reports in Markdown tables.",
        "pprose.eval_compare:main",
        "Evaluate",
    ),
    "render": CommandSpec(
        "Render an eval report (.eval.md) as a print-friendly static HTML page.",
        "pprose.render_html.cli:main",
        "Evaluate",
    ),
    "list": CommandSpec(
        "List all bundled guidelines, shortcuts, runbooks, and skills.",
        "pprose.reference:inventory_main",
        "Reference",
    ),
    "guidelines": CommandSpec(
        "Print a bundled guideline doc; run with no name to list them.",
        "pprose.reference:guidelines_main",
        "Reference",
    ),
    "shortcut": CommandSpec(
        "Print a bundled workflow shortcut; run with no name to list them.",
        "pprose.reference:shortcut_main",
        "Reference",
    ),
    "runbook": CommandSpec(
        "Print a bundled runbook; run with no name to list them.",
        "pprose.reference:runbook_main",
        "Reference",
    ),
    "skill": CommandSpec(
        "Print a composed Practical Prose skill; run with no name for an overview.",
        "pprose.install:skill_main",
        "Reference",
    ),
    "about": CommandSpec(
        "Print the Practical Prose project narrative (bundled README).",
        "pprose.reference:about_main",
        "Reference",
    ),
    "install": CommandSpec(
        "Install skill profiles or an exact skill set (project or user scope).",
        "pprose.install:install_main",
        "Setup",
    ),
}


def _resolve(target: str) -> CommandMain:
    """Import a command's `module:attr` target lazily, at dispatch time."""
    module_name, _, attr = target.partition(":")
    module = importlib.import_module(module_name)
    return getattr(module, attr)


def _print_help() -> None:
    command_width = max(len(name) for name in COMMANDS)
    lines = [
        term.bold("pprose — Practical Prose evaluation and editing tooling"),
        "",
        term.heading("Usage:"),
        f"  {term.command(PROGRAM)} <command> [args]",
    ]
    for group in GROUPS:
        lines.append("")
        lines.append(term.heading(f"{group}:"))
        for name, spec in COMMANDS.items():
            if spec.group == group:
                pad = " " * (command_width - len(name))
                lines.append(f"  {term.command(name)}{pad}  {spec.summary}")
    lines.extend(
        [
            "",
            f"Run `{PROGRAM} <command> --help` for command-specific options, "
            f"`{PROGRAM} --version` for the installed version, "
            f"`--color auto|always|never` to control styling.",
            "",
            "Getting started:",
            f"  uvx {PROGRAM} install -g     # every skill, for you, in every repo",
            f"  uvx {PROGRAM} install        # complete suite in the current project",
            f"  uvx {PROGRAM} install --profile common-docs  # standing documentation policy",
            f"  {PROGRAM} about              # the Practical Prose project narrative",
            f"  {PROGRAM} skill              # workflow skills overview + routing pointers",
            f"  {PROGRAM} list               # all bundled guidelines, shortcuts, runbooks, skills",
            "  `score` needs --model and a provider API key in the environment",
            "  (ANTHROPIC_API_KEY, OPENAI_API_KEY, or GOOGLE_API_KEY; .env / .env.local",
            "  are auto-loaded). Run `pprose score --list-models` for suggestions.",
        ]
    )
    print("\n".join(lines))


@contextmanager
def _program_name(name: str) -> Generator[None]:
    original = sys.argv[0]
    sys.argv[0] = name
    try:
        yield
    finally:
        sys.argv[0] = original


def _run_with_prog(command: str, func: CommandMain, args: list[str]) -> int:
    with _program_name(f"{PROGRAM} {command}"):
        try:
            return func(args)
        except SystemExit as exc:
            return exc.code if isinstance(exc.code, int) else 1


def _version() -> str:
    """Installed pprose version, or 'unknown' if not resolvable (e.g. odd dev layout)."""
    try:
        return version(PROGRAM)
    except PackageNotFoundError:
        return "unknown"


def _extract_color(args: list[str]) -> tuple[list[str], str | None]:
    """Pull the global `--color [auto|always|never]` flag out from any position."""
    override: str | None = None
    rest: list[str] = []
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--color":
            override = args[i + 1] if i + 1 < len(args) else ""
            i += 2
        elif arg.startswith("--color="):
            override = arg.split("=", 1)[1]
            i += 1
        else:
            rest.append(arg)
            i += 1
    return rest, override


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)

    args, color_override = _extract_color(args)
    if color_override is not None and color_override not in COLOR_CHOICES:
        choices = ", ".join(COLOR_CHOICES)
        print(
            term.error("error:") + f" --color must be one of: {choices}",
            file=sys.stderr,
        )
        return 2
    term.set_enabled(term.use_color(sys.stdout, color_override))

    if args and args[0] in {"-h", "--help"}:
        _print_help()
        return 0
    if args and args[0] in {"-V", "--version"}:
        print(f"{PROGRAM} {_version()}")
        return 0
    if not args:
        _print_help()
        return 0

    command = args[0]
    spec = COMMANDS.get(command)
    if spec is None:
        print(term.error("error:") + f" unknown command: {command}", file=sys.stderr)
        _print_help()
        return 2

    return _run_with_prog(command, _resolve(spec.target), args[1:])


if __name__ == "__main__":
    raise SystemExit(main())
