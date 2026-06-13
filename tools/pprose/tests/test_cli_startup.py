"""Startup-cost guardrails and the reference-listing contract for the pprose CLI.

The CLI must stay snappy for `--help`, `--version`, and listings: importing
`pprose.cli` must not pull the eval chain (pydantic_ai + provider SDKs), which costs
~1s. These tests fail loudly if a future edit reintroduces an eager heavy import, and
they pin the no-args-lists / `pprose list` contract.
"""

from __future__ import annotations

import subprocess
import sys
import time

import pytest

from pprose import cli

# Heavy modules that must NOT be imported merely by `import pprose.cli`.
# They are only needed when an eval/score/compare command actually runs.
FORBIDDEN_AT_IMPORT = ("pydantic_ai", "anthropic", "openai", "google.genai")


def _importtime_modules() -> set[str]:
    """Module names imported by `import pprose.cli`, via `python -X importtime`."""
    proc = subprocess.run(
        [sys.executable, "-X", "importtime", "-c", "import pprose.cli"],
        capture_output=True,
        text=True,
        check=True,
    )
    names: set[str] = set()
    for line in proc.stderr.splitlines():
        if line.startswith("import time:") and "|" in line:
            names.add(line.rsplit("|", 1)[-1].strip())
    return names


def test_cli_import_excludes_heavy_subsystems() -> None:
    imported = _importtime_modules()
    leaked = sorted(m for m in FORBIDDEN_AT_IMPORT if m in imported)
    assert not leaked, (
        f"importing pprose.cli eagerly pulled in {leaked}; keep cli.py module-level "
        "imports to the standard library and resolve command targets lazily"
    )


def test_cli_import_is_fast() -> None:
    """A generous wall budget so a heavy eager import regresses visibly."""
    start = time.perf_counter()
    subprocess.run(
        [sys.executable, "-c", "import pprose.cli"],
        capture_output=True,
        check=True,
    )
    elapsed = time.perf_counter() - start
    assert elapsed < 1.0, f"import pprose.cli took {elapsed:.2f}s (budget 1.0s)"


@pytest.mark.parametrize("command", sorted(cli.COMMANDS))
def test_every_command_help_dispatches(command: str) -> None:
    """Each command's `--help` resolves its lazy target and exits 0 (argparse help)."""
    rc = cli.main([command, "--help"])
    assert rc == 0


def test_list_command_groups_all_kinds(capsys: pytest.CaptureFixture[str]) -> None:
    rc = cli.main(["list"])
    out = capsys.readouterr().out
    assert rc == 0
    for kind in ("guidelines:", "shortcuts:", "runbooks:", "skills:"):
        assert kind in out


def test_list_kind_filter(capsys: pytest.CaptureFixture[str]) -> None:
    rc = cli.main(["list", "--kind", "guidelines"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "common-doc-guidelines" in out
    assert "shortcuts:" not in out  # filtered to one kind, no group headers


def test_guidelines_no_args_lists(capsys: pytest.CaptureFixture[str]) -> None:
    rc = cli.main(["guidelines"])
    out = capsys.readouterr().out
    assert rc == 0
    assert "common-doc-guidelines" in out


def test_guidelines_name_prints_doc(capsys: pytest.CaptureFixture[str]) -> None:
    rc = cli.main(["guidelines", "common-doc-guidelines"])
    out = capsys.readouterr().out
    assert rc == 0
    assert len(out) > 500  # the full doc, not the one-line listing


def test_list_flag_is_gone(capsys: pytest.CaptureFixture[str]) -> None:
    """`--list` was removed (hard cut); argparse rejects it with exit 2."""
    rc = cli.main(["guidelines", "--list"])
    assert rc == 2
