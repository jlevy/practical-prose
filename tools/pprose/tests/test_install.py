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


def test_is_pypi_release_recognizes_dev_and_release_versions():
    assert install.is_pypi_release("0.1.0")
    assert install.is_pypi_release("1.2.3")
    assert install.is_pypi_release("0.7.2.post1")
    # Dev/local/pre-release builds are not exact-pinnable on PyPI.
    assert not install.is_pypi_release("0.0.1.dev53+f22b2cb")
    assert not install.is_pypi_release("1.0.0a1")
    assert not install.is_pypi_release("1.0.0rc1")


def test_skill_compose_has_format_stamp_and_bootstrap(capsys: pytest.CaptureFixture[str]):
    assert cli.main(["skill", "pprose-full-edit"]) == 0
    out = capsys.readouterr().out
    assert "DO NOT EDIT" in out
    assert f"format={install.PPROSE_FORMAT}" in out
    assert f"surface={install.SURFACE_SKILL_MD}" in out
    assert f"uvx pprose@{install.pinned_version()}" in out
    # The body must still be present after the bootstrap (route, don't restate).
    assert "pprose shortcut shortcut-full-edit" in out


def test_skill_list_outputs_descriptions(capsys: pytest.CaptureFixture[str]):
    assert cli.main(["skill", "--list"]) == 0
    out = capsys.readouterr().out
    for name in resources.list_names("skills"):
        assert name in out


def test_compose_skill_is_deterministic():
    """Same inputs must produce byte-identical output (drift-test safety)."""
    a = install.compose_skill("pprose-eval", pin="0.1.0")
    b = install.compose_skill("pprose-eval", pin="0.1.0")
    assert a == b


def test_install_writes_both_skill_surfaces(tmp_path: Path):
    rc = install.install_main(["--dir", str(tmp_path)])
    assert rc == 0
    skills = set(resources.list_names("skills"))
    portable = tmp_path / install.PORTABLE_SKILLS_DIR
    claude = tmp_path / install.CLAUDE_SKILLS_DIR
    assert {p.parent.name for p in portable.glob("*/SKILL.md")} == skills
    assert {p.parent.name for p in claude.glob("*/SKILL.md")} == skills
    pin = install.pinned_version()
    for skill_md in (*portable.glob("*/SKILL.md"), *claude.glob("*/SKILL.md")):
        text = skill_md.read_text(encoding="utf-8")
        assert f"format={install.PPROSE_FORMAT}" in text
        assert f"surface={install.SURFACE_SKILL_MD}" in text
        assert f"uvx pprose@{pin}" in text


def test_install_portable_and_claude_are_byte_identical(tmp_path: Path):
    install.install_main(["--dir", str(tmp_path)])
    for name in resources.list_names("skills"):
        portable = (tmp_path / install.PORTABLE_SKILLS_DIR / name / "SKILL.md").read_text(
            encoding="utf-8"
        )
        claude = (tmp_path / install.CLAUDE_SKILLS_DIR / name / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert portable == claude


def test_install_writes_agents_md_block_with_format_stamp(tmp_path: Path):
    (tmp_path / "AGENTS.md").write_text("# Project\n\nUser content.\n", encoding="utf-8")
    assert install.install_main(["--dir", str(tmp_path)]) == 0
    agents = (tmp_path / "AGENTS.md").read_text(encoding="utf-8")
    assert "User content." in agents  # preserved
    assert (
        f"<!-- BEGIN PPROSE INTEGRATION format={install.PPROSE_FORMAT} "
        f"surface={install.SURFACE_AGENTS_MD} -->"
    ) in agents
    assert install.AGENTS_END_MARKER in agents
    assert f"uvx pprose@{install.pinned_version()}" in agents


def test_install_skip_codex_omits_agents_md_and_portable(tmp_path: Path):
    assert install.install_main(["--dir", str(tmp_path), "--skip-codex"]) == 0
    assert not (tmp_path / install.PORTABLE_SKILLS_DIR).exists()
    assert not (tmp_path / "AGENTS.md").exists()
    assert (tmp_path / install.CLAUDE_SKILLS_DIR).exists()


def test_install_skip_claude_keeps_codex_surface(tmp_path: Path):
    assert install.install_main(["--dir", str(tmp_path), "--skip-claude"]) == 0
    assert (tmp_path / install.PORTABLE_SKILLS_DIR).exists()
    assert (tmp_path / "AGENTS.md").exists()
    assert not (tmp_path / install.CLAUDE_SKILLS_DIR).exists()


def test_install_only_claude(tmp_path: Path):
    assert install.install_main(["--dir", str(tmp_path), "--claude"]) == 0
    assert (tmp_path / install.CLAUDE_SKILLS_DIR).exists()
    assert not (tmp_path / install.PORTABLE_SKILLS_DIR).exists()
    assert not (tmp_path / "AGENTS.md").exists()


def test_install_no_agents_md_keeps_portable(tmp_path: Path):
    assert install.install_main(["--dir", str(tmp_path), "--no-agents-md"]) == 0
    assert (tmp_path / install.PORTABLE_SKILLS_DIR).exists()
    assert not (tmp_path / "AGENTS.md").exists()


def test_install_is_idempotent_and_reports_unchanged(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    install.install_main(["--dir", str(tmp_path)])
    capsys.readouterr()  # discard first-run output
    assert install.install_main(["--dir", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "unchanged" in out
    assert "installed" not in out


def test_install_forward_compat_guard_blocks_newer_format(tmp_path: Path):
    """An artifact stamped with a newer format must not be overwritten."""
    target = tmp_path / install.CLAUDE_SKILLS_DIR / "pprose-eval" / "SKILL.md"
    target.parent.mkdir(parents=True)
    newer_format = f"f{install._format_num() + 1:02d}"
    sentinel = (
        f"<!-- DO NOT EDIT: generated by `pprose install` "
        f"(format={newer_format} surface={install.SURFACE_SKILL_MD}) -->\n"
        "newer-format content\n"
    )
    target.write_text(sentinel, encoding="utf-8")
    rc = install.install_main(["--dir", str(tmp_path), "--claude"])
    assert rc == 1  # blocked-newer is reported as a non-zero exit
    assert target.read_text(encoding="utf-8") == sentinel  # untouched


def test_install_collapses_duplicate_agents_md_blocks(tmp_path: Path):
    agents = tmp_path / "AGENTS.md"
    stale_a = (
        f"{install.AGENTS_BEGIN_PREFIX} format=f01 surface=agents-md -->\nstale a\n"
        f"{install.AGENTS_END_MARKER}"
    )
    stale_b = (
        f"{install.AGENTS_BEGIN_PREFIX} format=f01 surface=agents-md -->\nstale b\n"
        f"{install.AGENTS_END_MARKER}"
    )
    agents.write_text(
        f"# Project\n\n{stale_a}\n\nmiddle\n\n{stale_b}\n\ntail\n", encoding="utf-8"
    )
    assert install.install_main(["--dir", str(tmp_path), "--codex"]) == 0
    text = agents.read_text(encoding="utf-8")
    assert text.count(install.AGENTS_END_MARKER) == 1
    assert "stale a" not in text and "stale b" not in text
    assert "middle" in text and "tail" in text  # user content preserved


def test_install_pin_override(tmp_path: Path):
    """`--pin` lets sync_resources.py render committed discovery copies deterministically."""
    rc = install.install_main(["--dir", str(tmp_path), "--pin", "9.9.9"])
    assert rc == 0
    text = (
        tmp_path / install.CLAUDE_SKILLS_DIR / "pprose-eval" / "SKILL.md"
    ).read_text(encoding="utf-8")
    assert "uvx pprose@9.9.9" in text


def test_install_print_writes_nothing(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    assert install.install_main(["--dir", str(tmp_path), "--print"]) == 0
    out = capsys.readouterr().out
    assert "SKILL.md" in out
    assert "AGENTS.md" in out
    assert not (tmp_path / ".claude").exists()
    assert not (tmp_path / ".agents").exists()


def test_discovery_skills_match_committed_repo_root():
    """The committed `skills/<name>/SKILL.md` discovery copies must match what
    `pprose install --pin DISCOVERY_VERSION` would render today."""
    repo_root = Path(__file__).resolve().parents[3]
    for name in resources.list_names("skills"):
        committed = repo_root / "skills" / name / "SKILL.md"
        rendered = install.compose_skill(name, pin=install.DISCOVERY_VERSION)
        assert committed.is_file(), f"discovery copy missing: {committed}"
        assert committed.read_text(encoding="utf-8") == rendered, (
            f"discovery copy drift: {committed.relative_to(repo_root)}; "
            f"run `uv run python devtools/sync_resources.py`"
        )
