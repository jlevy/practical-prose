"""Tests for the terminal styling layer and the CLI's color behavior."""

from __future__ import annotations

import pytest

from pprose import cli, term

COLOR_ENV = ("NO_COLOR", "FORCE_COLOR", "CI", "TERM")


@pytest.fixture(autouse=True)
def _clean_color_env(monkeypatch: pytest.MonkeyPatch):
    for var in COLOR_ENV:
        monkeypatch.delenv(var, raising=False)
    yield
    term.set_enabled(False)


class _Stream:
    def __init__(self, tty: bool) -> None:
        self._tty = tty

    def isatty(self) -> bool:
        return self._tty


def test_override_wins_over_everything(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")
    assert term.use_color(_Stream(False), override="always") is True
    monkeypatch.setenv("FORCE_COLOR", "1")
    assert term.use_color(_Stream(True), override="never") is False


def test_no_color_disables(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NO_COLOR", "")  # any value, including empty
    assert term.use_color(_Stream(True)) is False


def test_force_color_enables_over_pipe(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("FORCE_COLOR", "1")
    assert term.use_color(_Stream(False)) is True


def test_ci_and_dumb_terminal_disable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CI", "true")
    assert term.use_color(_Stream(True)) is False
    monkeypatch.delenv("CI")
    monkeypatch.setenv("TERM", "dumb")
    assert term.use_color(_Stream(True)) is False


def test_auto_follows_isatty() -> None:
    assert term.use_color(_Stream(True)) is True
    assert term.use_color(_Stream(False)) is False


def test_width_clamps_and_defaults() -> None:
    assert term.terminal_width(_Stream(False)) == 80  # non-TTY -> fixed default


def test_style_helpers_are_plain_when_disabled() -> None:
    term.set_enabled(False)
    assert term.bold("x") == "x"
    assert term.heading("x") == "x"
    assert "\033" not in term.command("x")


def test_style_helpers_wrap_when_enabled() -> None:
    term.set_enabled(True)
    out = term.bold("x")
    assert out.startswith("\033[") and out.endswith("\033[0m") and "x" in out


def test_cli_list_plain_under_capsys(capsys: pytest.CaptureFixture[str]) -> None:
    """Default (captured stdout, not a TTY) yields byte-stable plain output."""
    assert cli.main(["list"]) == 0
    out = capsys.readouterr().out
    assert "\033" not in out


def test_cli_color_always_emits_ansi(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["--color", "always", "list"]) == 0
    out = capsys.readouterr().out
    assert "\033[" in out


def test_cli_color_never_stays_plain(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["--color", "never", "list"]) == 0
    assert "\033" not in capsys.readouterr().out


def test_cli_invalid_color_is_validation_error(capsys: pytest.CaptureFixture[str]) -> None:
    rc = cli.main(["--color", "purple", "list"])
    assert rc == 2
    assert "must be one of" in capsys.readouterr().err


def test_color_always_help_is_styled(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["--color", "always", "--help"]) == 0
    assert "\033[" in capsys.readouterr().out


def test_force_color_env_colors_output(
    capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("FORCE_COLOR", "1")
    assert cli.main(["list"]) == 0
    assert "\033[" in capsys.readouterr().out
