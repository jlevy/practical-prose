"""Tests for the unified pprose console entry point."""

from __future__ import annotations

from pathlib import Path

import pytest

from pprose import cli
from pprose.metrics import main as metrics_main

FIXTURE_DIR = Path(__file__).parent / "fixtures"
METRICS_FIXTURES = Path(__file__).parent / "test_fixtures" / "practical_prose_metrics"


def test_top_level_help_lists_subcommands(capsys: pytest.CaptureFixture[str]) -> None:
    rc = cli.main(["--help"])

    captured = capsys.readouterr()
    assert rc == 0
    assert "pprose <command> [args]" in captured.out
    for command in ("metrics", "score", "report", "compare"):
        assert command in captured.out
    assert captured.err == ""


@pytest.mark.parametrize("command", ["metrics", "score", "report", "compare"])
def test_subcommand_help_uses_pprose_command_name(
    command: str, capsys: pytest.CaptureFixture[str]
) -> None:
    rc = cli.main([command, "--help"])

    captured = capsys.readouterr()
    assert rc == 0
    assert f"usage: pprose {command}" in captured.out


def test_metrics_subcommand_matches_compatibility_script(
    capsys: pytest.CaptureFixture[str],
) -> None:
    fixture = str(METRICS_FIXTURES / "all_headings.md")

    compat_rc = metrics_main([fixture, "--format", "json"])
    compat = capsys.readouterr()
    unified_rc = cli.main(["metrics", fixture, "--format", "json"])
    unified = capsys.readouterr()

    assert compat_rc == 0
    assert unified_rc == 0
    assert unified.out == compat.out
    assert unified.err == compat.err == ""


def test_report_subcommand_dispatches_validate(capsys: pytest.CaptureFixture[str]) -> None:
    rc = cli.main(["report", "validate", str(FIXTURE_DIR / "rev1-net.eval.md")])

    captured = capsys.readouterr()
    assert rc == 0
    assert "OK" in captured.out


def test_unknown_subcommand_exits_validation_error(
    capsys: pytest.CaptureFixture[str],
) -> None:
    rc = cli.main(["bogus"])

    captured = capsys.readouterr()
    assert rc == 2
    assert "unknown command: bogus" in captured.err
    assert "pprose <command> [args]" in captured.out
