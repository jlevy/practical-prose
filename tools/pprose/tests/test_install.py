"""Tests for the resources loader, reference subcommands, and `pprose install`."""

from __future__ import annotations

from pathlib import Path

import pytest

from pprose import cli, install, resources


def test_resources_list_and_read():
    assert "common-doc-guidelines" in resources.list_names("guidelines")
    assert "shortcut-full-edit" in resources.list_names("shortcuts")
    assert set(resources.list_names("skills")) >= {
        "pprose-common-edit",
        "pprose-copy-edit",
        "pprose-full-edit",
        "pprose-eval",
        "pprose-compare",
    }
    assert "# Practical Prose Guidelines" in resources.read_doc(
        "guidelines", "practical-prose-guidelines"
    )


def test_resources_missing_name_lists_valid():
    with pytest.raises(FileNotFoundError, match="available:"):
        resources.read_doc("guidelines", "does-not-exist")


def test_guidelines_and_shortcut_subcommands(capsys: pytest.CaptureFixture[str]):
    assert cli.main(["guidelines", "--list"]) == 0
    assert "common-doc-guidelines" in capsys.readouterr().out

    assert cli.main(["shortcut", "shortcut-full-edit"]) == 0
    assert "Editorial review" in capsys.readouterr().out


def test_unknown_reference_name_errors(capsys: pytest.CaptureFixture[str]):
    rc = cli.main(["guidelines", "bogus-doc"])
    assert rc == 2
    assert "available:" in capsys.readouterr().err


def test_skill_compose_has_pinned_invocation_and_marker(capsys: pytest.CaptureFixture[str]):
    assert cli.main(["skill", "pprose-full-edit"]) == 0
    out = capsys.readouterr().out
    assert "DO NOT EDIT" in out
    assert f"uvx --from practical-prose@{install.pinned_version()} pprose" in out
    # The local-first + tell-the-user fallback must be present.
    assert "if `pprose` is on the PATH" in out
    assert "pprose needs `uvx`" in out


def test_install_writes_pinned_skills(tmp_path: Path):
    rc = install.install_main(["--dir", str(tmp_path)])
    assert rc == 0
    pin = install.pinned_version()
    skills_root = tmp_path / ".claude" / "skills"
    installed = sorted(p.parent.name for p in skills_root.glob("*/SKILL.md"))
    assert installed == sorted(resources.list_names("skills"))
    for skill_md in skills_root.glob("*/SKILL.md"):
        text = skill_md.read_text(encoding="utf-8")
        assert "DO NOT EDIT" in text
        assert f"uvx --from practical-prose@{pin} pprose" in text
        assert "pprose needs `uvx`" in text


def test_install_agents_md_marker(tmp_path: Path):
    (tmp_path / "AGENTS.md").write_text("# Project\n\nUser content.\n", encoding="utf-8")
    assert install.install_main(["--dir", str(tmp_path), "--agents-md"]) == 0
    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert "User content." in agents  # preserved
    assert "<!-- BEGIN PPROSE -->" in agents and "<!-- END PPROSE -->" in agents
    assert f"uvx --from practical-prose@{install.pinned_version()} pprose" in agents


def test_install_print_writes_nothing(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    assert install.install_main(["--dir", str(tmp_path), "--print"]) == 0
    assert "SKILL.md" in capsys.readouterr().out
    assert not (tmp_path / ".claude").exists()
