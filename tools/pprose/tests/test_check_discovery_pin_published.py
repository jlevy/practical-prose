"""Tests for the scheduled guard that the baked discovery pin exists on PyPI."""

from __future__ import annotations

import pytest

from devtools import check_discovery_pin_published as check


def test_passes_when_the_pin_is_published(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    monkeypatch.setattr(check.install, "DISCOVERY_VERSION", "1.2.3")
    monkeypatch.setattr(check, "published_versions", lambda: {"1.2.2", "1.2.3"})
    assert check.main([]) == 0
    assert "OK" in capsys.readouterr().out


def test_fails_when_the_pin_was_never_released(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    """The 0.3.1 case: prepped and merged, never tagged."""
    monkeypatch.setattr(check.install, "DISCOVERY_VERSION", "0.3.1")
    monkeypatch.setattr(check, "published_versions", lambda: {"0.1.0", "0.2.0", "0.3.0"})
    assert check.main([]) == 1
    err = capsys.readouterr().err
    assert "not published on PyPI" in err
    assert "uvx pprose@0.3.1" in err  # names the exact broken command
    assert "0.3.0" in err  # names the newest published release


def test_unreachable_pypi_is_inconclusive_not_a_failure(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    """A network blip must not be reported as a dangling pin."""

    def boom() -> set[str]:
        raise RuntimeError("could not read https://pypi.org/pypi/pprose/json: timed out")

    monkeypatch.setattr(check, "published_versions", boom)
    assert check.main([]) == 2
    assert "INCONCLUSIVE" in capsys.readouterr().err


def test_rejects_arguments(capsys: pytest.CaptureFixture[str]):
    assert check.main(["v1.2.3"]) == 2
    assert "takes no arguments" in capsys.readouterr().err
