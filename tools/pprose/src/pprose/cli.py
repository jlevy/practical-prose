"""Unified command entry point for the pprose package."""

from __future__ import annotations

import sys
from collections.abc import Callable, Generator
from contextlib import contextmanager
from dataclasses import dataclass

from pprose import eval_compare, eval_report, eval_score, install, metrics, reference

CommandMain = Callable[[list[str] | None], int]


@dataclass(frozen=True)
class CommandSpec:
    summary: str
    main: CommandMain
    group: str


# Groups print in this order.
GROUPS = ("Evaluate", "Reference", "Setup")
PROGRAM = "pprose"

COMMANDS: dict[str, CommandSpec] = {
    "metrics": CommandSpec(
        "Compute deterministic metrics for one or more Markdown artifacts.",
        metrics.main,
        "Evaluate",
    ),
    "report": CommandSpec(
        "Create, validate, and recompute eval reports.",
        eval_report.main,
        "Evaluate",
    ),
    "score": CommandSpec(
        "Fill qualitative scores and rule_findings in eval reports via Pydantic AI.",
        eval_score.main,
        "Evaluate",
    ),
    "compare": CommandSpec(
        "Compare multiple eval reports in Markdown tables.",
        eval_compare.main,
        "Evaluate",
    ),
    "guidelines": CommandSpec(
        "Print a bundled guideline doc (--list to see them).",
        reference.guidelines_main,
        "Reference",
    ),
    "shortcut": CommandSpec(
        "Print a bundled workflow shortcut (--list to see them).",
        reference.shortcut_main,
        "Reference",
    ),
    "runbook": CommandSpec(
        "Print a bundled runbook (--list to see them).",
        reference.runbook_main,
        "Reference",
    ),
    "skill": CommandSpec(
        "Print a composed Practical Prose skill (--list to see them).",
        install.skill_main,
        "Reference",
    ),
    "install": CommandSpec(
        "Install the Practical Prose skills into a repo "
        "(.agents/skills + .claude/skills + AGENTS.md block).",
        install.install_main,
        "Setup",
    ),
}


def _print_help() -> None:
    command_width = max(len(name) for name in COMMANDS)
    lines = [
        "pprose — Practical Prose evaluation and editing tooling",
        "",
        "Usage:",
        f"  {PROGRAM} <command> [args]",
    ]
    for group in GROUPS:
        lines.append("")
        lines.append(f"{group}:")
        for name, spec in COMMANDS.items():
            if spec.group == group:
                lines.append(f"  {name:<{command_width}}  {spec.summary}")
    lines.extend(
        [
            "",
            f"Run `{PROGRAM} <command> --help` for command-specific options.",
            "",
            "Getting started:",
            f"  uvx {PROGRAM} install        # install skills into the current repo",
            f"  {PROGRAM} skill --list       # list installed Practical Prose skills",
            f"  {PROGRAM} guidelines --list  # bundled style guides and writing rules",
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


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"-h", "--help"}:
        _print_help()
        return 0
    if not args:
        _print_help()
        return 0

    command = args[0]
    spec = COMMANDS.get(command)
    if spec is None:
        print(f"error: unknown command: {command}", file=sys.stderr)
        _print_help()
        return 2

    return _run_with_prog(command, spec.main, args[1:])


if __name__ == "__main__":
    raise SystemExit(main())
