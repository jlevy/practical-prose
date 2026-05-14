"""Unified command entry point for the prose-eval package."""

from __future__ import annotations

import sys
from collections.abc import Callable, Generator
from contextlib import contextmanager
from dataclasses import dataclass

from prose_eval import eval_compare, eval_report, eval_score, metrics

CommandMain = Callable[[list[str] | None], int]


@dataclass(frozen=True)
class CommandSpec:
    summary: str
    main: CommandMain


COMMANDS: dict[str, CommandSpec] = {
    "metrics": CommandSpec(
        "Compute deterministic metrics for one or more Markdown artifacts.",
        metrics.main,
    ),
    "score": CommandSpec(
        "Fill qualitative scores and violations in eval reports.",
        eval_score.main,
    ),
    "report": CommandSpec(
        "Create, validate, and recompute eval reports.",
        eval_report.main,
    ),
    "compare": CommandSpec(
        "Compare multiple eval reports in Markdown tables.",
        eval_compare.main,
    ),
}


def _print_help() -> None:
    command_width = max(len(name) for name in COMMANDS)
    lines = [
        "usage: prose-eval <command> [args]",
        "",
        "Practical Prose evaluation tooling.",
        "",
        "Commands:",
    ]
    for name, spec in COMMANDS.items():
        lines.append(f"  {name:<{command_width}}  {spec.summary}")
    lines.extend(
        [
            "",
            "Run `prose-eval <command> --help` for command-specific options.",
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
    with _program_name(f"prose-eval {command}"):
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
        return 2

    command = args[0]
    spec = COMMANDS.get(command)
    if spec is None:
        print(f"error: unknown command: {command}", file=sys.stderr)
        _print_help()
        return 2

    return _run_with_prog(command, spec.main, args[1:])


if __name__ == "__main__":
    raise SystemExit(main())
