"""Tests for the resources loader, reference subcommands, and `pprose install`."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from pprose import cli, install, resources


@pytest.fixture
def git_repo_tmp(tmp_path: Path) -> Path:
    """A `tmp_path` with a `.git/` directory so `_is_within_git_repo` returns True.

    Project-mode installs require this; without it the implicit-scope rule errors
    out as "not inside a git repository."
    """
    (tmp_path / ".git").mkdir()
    return tmp_path


@pytest.fixture
def home_tmp(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Set `$HOME` to `tmp_path` so `Path.home()` returns it.

    Used by --global tests so the install goes into `tmp_path/.agents/skills/` and
    `tmp_path/.claude/skills/` rather than the test runner's real home directory.
    """
    monkeypatch.setenv("HOME", str(tmp_path))
    return tmp_path


# ─────────────────────────────────────────────────────────────────────────────
# Resources loader / reference subcommands
# ─────────────────────────────────────────────────────────────────────────────


def test_generated_skills_are_flowmark_stable():
    """compose_skill / agents_md_block output is already flowmark-formatted.

    Generation must be idempotent under the repo's flowmark pre-commit hook: running
    flowmark over a freshly generated artifact must be a no-op, or `make generate`
    would emit long lines the hook silently rewraps into uncommitted drift (the
    original CI break). install._flowmark uses the same flags, verified byte-identical
    to flowmark-rs --auto.
    """
    from flowmark import reformat_text

    def _is_stable(text: str) -> bool:
        formatted = reformat_text(text, width=88, semantic=True, cleanups=True, smartquotes=True)
        return formatted == text.rstrip() + "\n"

    for name in resources.list_names("skills"):
        for relative, content in install.compose_skill_files(name, pin="0.1.0").items():
            assert _is_stable(content), f"compose_skill_files({name!r})[{relative}] is unstable"

    block = install.agents_md_block(pin="0.1.0")
    assert _is_stable(block), "agents_md_block() is not flowmark-stable"


def test_resources_list_and_read():
    assert "common-doc-guidelines" in resources.list_names("guidelines")
    assert "shortcut-full-edit" in resources.list_names("shortcuts")
    assert set(resources.list_names("skills")) >= {
        "pprose-common-edit",
        "pprose-copy-edit",
        "pprose-de-slop",
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
    assert cli.main(["guidelines"]) == 0  # no name lists them
    assert "common-doc-guidelines" in capsys.readouterr().out

    assert cli.main(["shortcut", "shortcut-full-edit"]) == 0
    assert "Editorial review" in capsys.readouterr().out


def test_unknown_reference_name_errors(capsys: pytest.CaptureFixture[str]):
    rc = cli.main(["guidelines", "bogus-doc"])
    assert rc == 2
    assert "available:" in capsys.readouterr().err


# ─────────────────────────────────────────────────────────────────────────────
# Skill composition
# ─────────────────────────────────────────────────────────────────────────────


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
    assert f"uvx pprose@{install.pinned_version()}" in out
    # Body must still be present after the bootstrap (route, don't restate).
    assert "pprose shortcut shortcut-full-edit" in out
    # The single-namespace decision: no `surface=` in the in-file marker.
    assert "surface=" not in out


def test_skill_list_flag_removed(capsys: pytest.CaptureFixture[str]):
    """`--list` was removed (hard cut); `pprose skill --list` is now a usage error."""
    assert cli.main(["skill", "--list"]) == 2


def test_skill_no_args_prints_overview(capsys: pytest.CaptureFixture[str]):
    """`pprose skill` (no args) prints an intro + skill table + routing footer."""
    assert cli.main(["skill"]) == 0
    out = capsys.readouterr().out
    # Intro paragraph.
    assert "Practical Prose skills" in out
    # All skill names listed.
    for name in resources.list_names("skills"):
        assert name in out
    # Routing footer points at the unified inventory, not the removed --list flag.
    assert "pprose list" in out
    assert "--list" not in out


def test_compose_skill_is_deterministic():
    """Same inputs must produce byte-identical output (drift-test safety)."""
    a = install.compose_skill("pprose-eval", pin="0.1.0")
    b = install.compose_skill("pprose-eval", pin="0.1.0")
    assert a == b


def test_common_docs_profile_selects_only_common_edit():
    assert install.profile_skill_names(install.PROFILE_COMMON_DOCS) == ("pprose-common-edit",)
    assert set(install.profile_skill_names(install.PROFILE_PRACTICAL_PROSE)) == set(
        resources.list_names("skills")
    )


def test_common_edit_is_self_contained_and_runtime_free():
    files = install.compose_skill_files("pprose-common-edit", pin="9.9.9")
    assert set(files) == {
        Path("SKILL.md"),
        Path("references") / "common-doc-guidelines.md",
    }
    assert "uvx pprose@9.9.9" not in files[Path("SKILL.md")]
    assert (
        "# Common Documentation Guidelines"
        in files[Path("references") / "common-doc-guidelines.md"]
    )
    skill = files[Path("SKILL.md")]
    assert "creating, editing, reviewing, or reorganizing Markdown" in skill
    assert "references/common-doc-guidelines.md" in skill
    assert "exactly one guideline footer" in skill
    assert skill.count("This document follows common-doc-guidelines.md.") == 1


def test_de_slop_is_self_contained_and_runtime_free():
    files = install.compose_skill_files("pprose-de-slop", pin="9.9.9")
    assert set(files) == {
        Path("SKILL.md"),
        Path("references") / "ai-prose-corrections.md",
    }
    skill = files[Path("SKILL.md")]
    assert "uvx pprose@9.9.9" not in skill
    assert "references/ai-prose-corrections.md" in skill
    assert "Preserve factual meaning, claim strength, citations" in skill
    assert "detector evasion" in skill
    assert "# AI-Prose Corrections" in files[Path("references") / "ai-prose-corrections.md"]


def test_copy_edit_routes_to_the_de_slop_pass():
    skill = install.compose_skill("pprose-copy-edit", pin="9.9.9")
    assert "superset of `pprose-common-edit` and `pprose-de-slop`" in skill
    assert "pprose shortcut shortcut-copy-edit" in skill


def test_agents_block_matches_the_selected_skill_set():
    common = install.agents_md_block(
        pin="9.9.9", skill_names=install.profile_skill_names(install.PROFILE_COMMON_DOCS)
    )
    assert "whenever creating, editing, reviewing, or reorganizing Markdown" in common
    assert "pprose-common-edit" in common
    assert "uvx pprose@9.9.9" not in common

    full = install.agents_md_block(
        pin="9.9.9",
        skill_names=install.profile_skill_names(install.PROFILE_PRACTICAL_PROSE),
    )
    assert "pprose-common-edit" in full
    assert "uvx pprose@9.9.9" in full

    de_slop = install.agents_md_block(pin="9.9.9", skill_names=("pprose-de-slop",))
    assert "pprose-de-slop" in de_slop
    assert "AI-writing tells" in de_slop
    assert "uvx pprose@9.9.9" not in de_slop


# ─────────────────────────────────────────────────────────────────────────────
# --surfaces flag parsing
# ─────────────────────────────────────────────────────────────────────────────


def test_parse_surfaces_default_is_all():
    spec = install.parse_surfaces(None)
    assert spec.surfaces == install.ALL_INSTALL_SURFACES
    assert spec.agents_md_explicit is False
    assert spec.claude_md_explicit is False


def test_parse_surfaces_all_token_expands():
    spec = install.parse_surfaces("all")
    assert spec.surfaces == install.ALL_INSTALL_SURFACES
    assert spec.agents_md_explicit is False  # 'all' expanded, not explicit


def test_parse_surfaces_explicit_subset():
    spec = install.parse_surfaces("portable,claude")
    assert spec.surfaces == frozenset({install.SURFACE_PORTABLE, install.SURFACE_CLAUDE})
    assert spec.agents_md_explicit is False


def test_parse_surfaces_tracks_explicit_agents_md():
    spec = install.parse_surfaces("agents-md")
    assert spec.surfaces == frozenset({install.SURFACE_AGENTS_MD})
    assert spec.agents_md_explicit is True


def test_parse_surfaces_tracks_explicit_claude_md():
    spec = install.parse_surfaces("claude-md")
    assert spec.surfaces == frozenset({install.SURFACE_CLAUDE_MD})
    assert spec.claude_md_explicit is True


def test_parse_surfaces_empty_errors():
    with pytest.raises(ValueError, match="--surfaces is empty"):
        install.parse_surfaces("")


def test_parse_surfaces_bogus_errors():
    with pytest.raises(ValueError, match="unknown surface 'bogus'"):
        install.parse_surfaces("portable,bogus")


# ─────────────────────────────────────────────────────────────────────────────
# Scope disambiguation (implicit) and explicit-flag errors
# ─────────────────────────────────────────────────────────────────────────────


def test_implicit_project_in_git_repo(git_repo_tmp: Path):
    """In a git repo (not $HOME), implicit project mode installs without a scope flag."""
    rc = install.install_main(["--dir", str(git_repo_tmp)])
    assert rc == 0
    assert (git_repo_tmp / install.PORTABLE_SKILLS_DIR).exists()
    assert (git_repo_tmp / install.CLAUDE_SKILLS_DIR).exists()


def test_implicit_scope_in_non_repo_errors(tmp_path: Path, capsys: pytest.CaptureFixture[str]):
    """Outside a git repo, implicit scope must be rejected as ambiguous."""
    rc = install.install_main(["--dir", str(tmp_path)])
    assert rc == 2
    err = capsys.readouterr().err
    assert "ambiguous scope" in err
    assert "not inside a git repository" in err
    assert "--project --no-repo-check" in err
    assert "--global" in err


def test_implicit_scope_in_home_errors(
    home_tmp: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
):
    """In $HOME, implicit scope must be rejected as ambiguous (could be global)."""
    monkeypatch.chdir(home_tmp)
    rc = install.install_main([])
    assert rc == 2
    err = capsys.readouterr().err
    assert "ambiguous scope" in err
    assert "home directory" in err


def test_project_and_global_mutually_exclusive(
    git_repo_tmp: Path, capsys: pytest.CaptureFixture[str]
):
    rc = install.install_main(["--project", "--global", "--dir", str(git_repo_tmp)])
    assert rc == 2
    err = capsys.readouterr().err
    assert "not allowed with argument --project" in err or "mutually exclusive" in err


def test_global_and_dir_mutually_exclusive(home_tmp: Path, capsys: pytest.CaptureFixture[str]):
    rc = install.install_main(["--global", "--dir", str(home_tmp)])
    assert rc == 2
    err = capsys.readouterr().err
    assert "--global and --dir are mutually exclusive" in err


def test_profile_and_skill_are_mutually_exclusive(
    git_repo_tmp: Path, capsys: pytest.CaptureFixture[str]
):
    rc = install.install_main(
        [
            "--project",
            "--dir",
            str(git_repo_tmp),
            "--profile=common-docs",
            "--skill=pprose-eval",
        ]
    )
    assert rc == 2
    assert "--profile and --skill are mutually exclusive" in capsys.readouterr().err
    assert not (git_repo_tmp / install.PORTABLE_SKILLS_DIR).exists()


# ─────────────────────────────────────────────────────────────────────────────
# --project mode
# ─────────────────────────────────────────────────────────────────────────────


def test_project_explicit_in_repo_installs(git_repo_tmp: Path):
    rc = install.install_main(["--project", "--dir", str(git_repo_tmp)])
    assert rc == 0
    skills = set(resources.list_names("skills"))
    assert {
        p.parent.name for p in (git_repo_tmp / install.PORTABLE_SKILLS_DIR).glob("*/SKILL.md")
    } == skills
    assert {
        p.parent.name for p in (git_repo_tmp / install.CLAUDE_SKILLS_DIR).glob("*/SKILL.md")
    } == skills
    assert (git_repo_tmp / "AGENTS.md").exists()


def test_project_common_docs_profile_installs_only_common_edit(git_repo_tmp: Path):
    rc = install.install_main(["--project", "--dir", str(git_repo_tmp), "--profile", "common-docs"])
    assert rc == 0
    for skills_dir in (install.PORTABLE_SKILLS_DIR, install.CLAUDE_SKILLS_DIR):
        installed = {p.parent.name for p in (git_repo_tmp / skills_dir).glob("*/SKILL.md")}
        assert installed == {"pprose-common-edit"}
        reference = (
            git_repo_tmp
            / skills_dir
            / "pprose-common-edit"
            / "references"
            / "common-doc-guidelines.md"
        )
        assert "# Common Documentation Guidelines" in reference.read_text(encoding="utf-8")
    claude_md = (git_repo_tmp / "CLAUDE.md").read_text(encoding="utf-8")
    assert claude_md.startswith("@AGENTS.md\n")
    assert f"format={install.PPROSE_FORMAT}" in claude_md


def test_project_repeatable_skill_flag_installs_exact_selection(git_repo_tmp: Path):
    rc = install.install_main(
        [
            "--project",
            "--dir",
            str(git_repo_tmp),
            "--skill",
            "pprose-review",
            "--skill",
            "pprose-eval",
        ]
    )
    assert rc == 0
    installed = {
        p.parent.name for p in (git_repo_tmp / install.PORTABLE_SKILLS_DIR).glob("*/SKILL.md")
    }
    assert installed == {"pprose-review", "pprose-eval"}


def test_project_exact_de_slop_install_is_self_contained(git_repo_tmp: Path):
    rc = install.install_main(
        [
            "--project",
            "--dir",
            str(git_repo_tmp),
            "--skill",
            "pprose-de-slop",
        ]
    )
    assert rc == 0
    for skills_dir in (install.PORTABLE_SKILLS_DIR, install.CLAUDE_SKILLS_DIR):
        skill_dir = git_repo_tmp / skills_dir / "pprose-de-slop"
        assert "uvx pprose@" not in (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        assert (skill_dir / "references" / "ai-prose-corrections.md").is_file()
    assert "uvx pprose@" not in (git_repo_tmp / "AGENTS.md").read_text(encoding="utf-8")


def test_common_docs_profile_removes_other_generated_pprose_skills(git_repo_tmp: Path):
    assert install.install_main(["--project", "--dir", str(git_repo_tmp)]) == 0
    assert (
        install.install_main(["--project", "--dir", str(git_repo_tmp), "--profile", "common-docs"])
        == 0
    )
    for skills_dir in (install.PORTABLE_SKILLS_DIR, install.CLAUDE_SKILLS_DIR):
        installed = {p.parent.name for p in (git_repo_tmp / skills_dir).glob("*/SKILL.md")}
        assert installed == {"pprose-common-edit"}


def test_profile_pruning_does_not_remove_newer_generated_skill(git_repo_tmp: Path):
    target = git_repo_tmp / install.PORTABLE_SKILLS_DIR / "pprose-eval" / "SKILL.md"
    target.parent.mkdir(parents=True)
    newer_format = f"f{install._format_num() + 1:02d}"
    sentinel = (
        f"<!-- DO NOT EDIT: generated by `pprose install` (format={newer_format}) -->\n"
        "newer-format content\n"
    )
    target.write_text(sentinel, encoding="utf-8")
    rc = install.install_main(
        [
            "--project",
            "--dir",
            str(git_repo_tmp),
            "--profile=common-docs",
            "--surfaces=portable",
        ]
    )
    assert rc == 1
    assert target.read_text(encoding="utf-8") == sentinel


def test_profile_pruning_preserves_unmarked_skill_content(git_repo_tmp: Path):
    target = git_repo_tmp / install.PORTABLE_SKILLS_DIR / "pprose-eval" / "SKILL.md"
    target.parent.mkdir(parents=True)
    target.write_text("user-owned content\n", encoding="utf-8")
    rc = install.install_main(
        [
            "--project",
            "--dir",
            str(git_repo_tmp),
            "--profile=common-docs",
            "--surfaces=portable",
        ]
    )
    assert rc == 0
    assert target.read_text(encoding="utf-8") == "user-owned content\n"


def test_project_in_non_repo_errors_without_no_repo_check(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
):
    rc = install.install_main(["--project", "--dir", str(tmp_path)])
    assert rc == 2
    err = capsys.readouterr().err
    assert "not inside a git repository" in err
    assert "--no-repo-check" in err


def test_project_with_no_repo_check_in_non_repo_installs(tmp_path: Path):
    """Non-git scratch dirs are usable via the explicit override."""
    rc = install.install_main(["--project", "--no-repo-check", "--dir", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / install.PORTABLE_SKILLS_DIR).exists()


def test_project_dir_home_is_refused(home_tmp: Path, capsys: pytest.CaptureFixture[str]):
    """`$HOME` is refused in --project even with --no-repo-check; use --global instead."""
    rc = install.install_main(["--project", "--no-repo-check", "--dir", str(home_tmp)])
    assert rc == 2
    err = capsys.readouterr().err
    assert "refusing to install into" in err
    assert "home directory" in err
    assert "--global" in err


def test_project_writes_both_skill_surfaces_with_format_stamp(git_repo_tmp: Path):
    install.install_main(["--project", "--dir", str(git_repo_tmp)])
    pin = install.pinned_version()
    for skill_md in (
        *(git_repo_tmp / install.PORTABLE_SKILLS_DIR).glob("*/SKILL.md"),
        *(git_repo_tmp / install.CLAUDE_SKILLS_DIR).glob("*/SKILL.md"),
    ):
        text = skill_md.read_text(encoding="utf-8")
        assert f"format={install.PPROSE_FORMAT}" in text
        if skill_md.parent.name in install.RUNTIME_FREE_SKILL_REFERENCES:
            assert f"uvx pprose@{pin}" not in text
        else:
            assert f"uvx pprose@{pin}" in text
        assert "surface=" not in text  # single namespace: no in-file surface tag


def test_project_portable_and_claude_are_byte_identical(git_repo_tmp: Path):
    install.install_main(["--project", "--dir", str(git_repo_tmp)])
    for name in resources.list_names("skills"):
        portable = (git_repo_tmp / install.PORTABLE_SKILLS_DIR / name / "SKILL.md").read_text(
            encoding="utf-8"
        )
        claude = (git_repo_tmp / install.CLAUDE_SKILLS_DIR / name / "SKILL.md").read_text(
            encoding="utf-8"
        )
        assert portable == claude


def test_project_agents_md_block_carries_format_stamp(git_repo_tmp: Path):
    (git_repo_tmp / "AGENTS.md").write_text("# Project\n\nUser content.\n", encoding="utf-8")
    install.install_main(["--project", "--dir", str(git_repo_tmp)])
    agents = (git_repo_tmp / "AGENTS.md").read_text(encoding="utf-8")
    assert "User content." in agents  # preserved
    assert f"{install.AGENTS_BEGIN_PREFIX} format={install.PPROSE_FORMAT} -->" in agents
    assert install.AGENTS_END_MARKER in agents
    assert f"uvx pprose@{install.pinned_version()}" in agents


def test_project_is_idempotent_and_reports_unchanged(
    git_repo_tmp: Path, capsys: pytest.CaptureFixture[str]
):
    install.install_main(["--project", "--dir", str(git_repo_tmp)])
    capsys.readouterr()  # discard first-run output
    assert install.install_main(["--project", "--dir", str(git_repo_tmp)]) == 0
    out = capsys.readouterr().out
    assert "unchanged" in out
    assert "installed" not in out


def test_project_forward_compat_guard_blocks_newer_format(git_repo_tmp: Path):
    """An artifact stamped with a newer format must not be overwritten."""
    target = git_repo_tmp / install.CLAUDE_SKILLS_DIR / "pprose-eval" / "SKILL.md"
    target.parent.mkdir(parents=True)
    newer_format = f"f{install._format_num() + 1:02d}"
    sentinel = (
        f"<!-- DO NOT EDIT: generated by `pprose install` (format={newer_format}) -->\n"
        "newer-format content\n"
    )
    target.write_text(sentinel, encoding="utf-8")
    rc = install.install_main(["--project", "--dir", str(git_repo_tmp), "--surfaces=claude"])
    assert rc == 1  # blocked-newer is reported as a non-zero exit
    assert target.read_text(encoding="utf-8") == sentinel  # untouched


def test_forward_compat_guard_runs_before_any_surface_write(git_repo_tmp: Path):
    target = git_repo_tmp / install.CLAUDE_SKILLS_DIR / "pprose-eval" / "SKILL.md"
    target.parent.mkdir(parents=True)
    newer_format = f"f{install._format_num() + 1:02d}"
    target.write_text(
        f"<!-- DO NOT EDIT: generated by `pprose install` (format={newer_format}) -->\n",
        encoding="utf-8",
    )
    assert install.install_main(["--project", "--dir", str(git_repo_tmp)]) == 1
    assert not (git_repo_tmp / install.PORTABLE_SKILLS_DIR).exists()
    assert not (git_repo_tmp / "AGENTS.md").exists()


def test_claude_bridge_forward_compat_guard_blocks_newer_format(git_repo_tmp: Path):
    target = git_repo_tmp / "CLAUDE.md"
    newer_format = f"f{install._format_num() + 1:02d}"
    sentinel = f"@AGENTS.md\n\n<!-- generated by `pprose install` (format={newer_format}) -->\n"
    target.write_text(sentinel, encoding="utf-8")
    rc = install.install_main(["--project", "--dir", str(git_repo_tmp), "--profile=common-docs"])
    assert rc == 1
    assert target.read_text(encoding="utf-8") == sentinel
    assert not (git_repo_tmp / install.PORTABLE_SKILLS_DIR).exists()


def test_project_collapses_duplicate_agents_md_blocks(git_repo_tmp: Path):
    agents = git_repo_tmp / "AGENTS.md"
    stale_a = f"{install.AGENTS_BEGIN_PREFIX} format=f01 -->\nstale a\n{install.AGENTS_END_MARKER}"
    stale_b = f"{install.AGENTS_BEGIN_PREFIX} format=f01 -->\nstale b\n{install.AGENTS_END_MARKER}"
    agents.write_text(f"# Project\n\n{stale_a}\n\nmiddle\n\n{stale_b}\n\ntail\n", encoding="utf-8")
    assert install.install_main(["--project", "--dir", str(git_repo_tmp)]) == 0
    text = agents.read_text(encoding="utf-8")
    assert text.count(install.AGENTS_END_MARKER) == 1
    assert "stale a" not in text and "stale b" not in text
    assert "middle" in text and "tail" in text  # user content preserved


def test_pin_override_is_baked_into_generated_skills(git_repo_tmp: Path):
    """`--pin` lets sync_resources.py render discovery copies deterministically."""
    rc = install.install_main(["--project", "--dir", str(git_repo_tmp), "--pin", "9.9.9"])
    assert rc == 0
    text = (git_repo_tmp / install.CLAUDE_SKILLS_DIR / "pprose-eval" / "SKILL.md").read_text(
        encoding="utf-8"
    )
    assert "uvx pprose@9.9.9" in text


# ─────────────────────────────────────────────────────────────────────────────
# --global mode
# ─────────────────────────────────────────────────────────────────────────────


def test_global_writes_under_home_and_skips_agents_md(home_tmp: Path):
    rc = install.install_main(["--global"])
    assert rc == 0
    assert (home_tmp / install.PORTABLE_SKILLS_DIR).exists()
    assert (home_tmp / install.CLAUDE_SKILLS_DIR).exists()
    # Global mode must not write a global AGENTS.md.
    assert not (home_tmp / "AGENTS.md").exists()


def test_global_drops_agents_md_silently_with_default_surfaces(home_tmp: Path):
    """--global with implicit --surfaces=all drops agents-md without an error."""
    rc = install.install_main(["--global"])
    assert rc == 0
    # No error printed; only the skill surfaces written.


def test_global_with_explicit_agents_md_errors(home_tmp: Path, capsys: pytest.CaptureFixture[str]):
    """--global with --surfaces=agents-md is unambiguous user intent we can't satisfy."""
    rc = install.install_main(["--global", "--surfaces=agents-md"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "agents-md is not supported in --global mode" in err
    assert not (home_tmp / "AGENTS.md").exists()


def test_global_with_explicit_claude_md_errors(home_tmp: Path, capsys: pytest.CaptureFixture[str]):
    rc = install.install_main(["--global", "--surfaces=claude-md"])
    assert rc == 2
    assert "claude-md is not supported in --global mode" in capsys.readouterr().err
    assert not (home_tmp / "CLAUDE.md").exists()


def test_global_with_explicit_portable_only(home_tmp: Path):
    rc = install.install_main(["--global", "--surfaces=portable"])
    assert rc == 0
    assert (home_tmp / install.PORTABLE_SKILLS_DIR).exists()
    assert not (home_tmp / install.CLAUDE_SKILLS_DIR).exists()
    assert not (home_tmp / "AGENTS.md").exists()


# ─────────────────────────────────────────────────────────────────────────────
# --surfaces filtering inside project mode
# ─────────────────────────────────────────────────────────────────────────────


def test_project_surfaces_portable_only(git_repo_tmp: Path):
    rc = install.install_main(["--project", "--dir", str(git_repo_tmp), "--surfaces=portable"])
    assert rc == 0
    assert (git_repo_tmp / install.PORTABLE_SKILLS_DIR).exists()
    assert not (git_repo_tmp / install.CLAUDE_SKILLS_DIR).exists()
    assert not (git_repo_tmp / "AGENTS.md").exists()


def test_project_surfaces_no_agents_md(git_repo_tmp: Path):
    rc = install.install_main(
        ["--project", "--dir", str(git_repo_tmp), "--surfaces=portable,claude"]
    )
    assert rc == 0
    assert (git_repo_tmp / install.PORTABLE_SKILLS_DIR).exists()
    assert (git_repo_tmp / install.CLAUDE_SKILLS_DIR).exists()
    assert not (git_repo_tmp / "AGENTS.md").exists()


def test_agents_md_only_summary_reports_selected_cli_fallback(
    git_repo_tmp: Path, capsys: pytest.CaptureFixture[str]
):
    rc = install.install_main(["--project", "--dir", str(git_repo_tmp), "--surfaces=agents-md"])
    assert rc == 0
    assert f"CLI fallback pprose@{install.pinned_version()}" in capsys.readouterr().out


def test_project_claude_md_only_preserves_user_content(git_repo_tmp: Path):
    claude_md = git_repo_tmp / "CLAUDE.md"
    claude_md.write_text("# Claude\n\nUser instructions.\n", encoding="utf-8")
    rc = install.install_main(
        [
            "--project",
            "--dir",
            str(git_repo_tmp),
            "--surfaces=claude-md",
            "--profile=common-docs",
        ]
    )
    assert rc == 0
    text = claude_md.read_text(encoding="utf-8")
    assert "User instructions." in text
    assert "pprose-common-edit" in text
    assert not (git_repo_tmp / "AGENTS.md").exists()


def test_project_claude_md_only_does_not_bridge_to_unmanaged_agents_md(
    git_repo_tmp: Path,
):
    (git_repo_tmp / "AGENTS.md").write_text("# Project\n", encoding="utf-8")
    rc = install.install_main(
        [
            "--project",
            "--dir",
            str(git_repo_tmp),
            "--surfaces=claude-md",
            "--profile=common-docs",
        ]
    )
    assert rc == 0
    text = (git_repo_tmp / "CLAUDE.md").read_text(encoding="utf-8")
    assert "pprose-common-edit" in text


def test_project_surfaces_bogus_errors(git_repo_tmp: Path, capsys: pytest.CaptureFixture[str]):
    rc = install.install_main(["--project", "--dir", str(git_repo_tmp), "--surfaces=bogus"])
    assert rc == 2
    err = capsys.readouterr().err
    assert "unknown surface 'bogus'" in err


# ─────────────────────────────────────────────────────────────────────────────
# Pre-write target message
# ─────────────────────────────────────────────────────────────────────────────


def test_pre_write_message_in_project_mode(git_repo_tmp: Path, capsys: pytest.CaptureFixture[str]):
    install.install_main(["--project", "--dir", str(git_repo_tmp)])
    out = capsys.readouterr().out
    assert "(project mode) into:" in out
    assert str(git_repo_tmp.resolve()) in out
    assert "surfaces:" in out
    assert "skills: pprose-common-edit, pprose-compare" in out


def test_pre_write_message_in_global_mode(home_tmp: Path, capsys: pytest.CaptureFixture[str]):
    install.install_main(["--global"])
    out = capsys.readouterr().out
    assert "(user-global mode) into:" in out
    assert str(home_tmp) in out


# ─────────────────────────────────────────────────────────────────────────────
# Committed discovery-copy drift
# ─────────────────────────────────────────────────────────────────────────────


def test_about_prints_bundled_readme(capsys: pytest.CaptureFixture[str]):
    """`pprose about` prints the bundled README (project narrative)."""
    assert cli.main(["about"]) == 0
    out = capsys.readouterr().out
    # Sentinel: the README's H1.
    assert "# Practical Prose" in out
    # Sentinel: a recognizable line from the project description.
    assert "Practical Prose" in out


def test_about_rejects_extra_args(capsys: pytest.CaptureFixture[str]):
    """`pprose about <anything>` errors; it's a one-shot command."""
    rc = cli.main(["about", "bogus"])
    assert rc != 0


def test_discovery_skills_match_committed_repo_root():
    """The committed `skills/<name>/SKILL.md` discovery copies must match what
    `pprose install --pin DISCOVERY_VERSION` would render today."""
    repo_root = Path(__file__).resolve().parents[3]
    for name in resources.list_names("skills"):
        for relative, rendered in install.compose_skill_files(
            name, pin=install.DISCOVERY_VERSION
        ).items():
            committed = repo_root / "skills" / name / relative
            assert committed.is_file(), f"discovery copy missing: {committed}"
            assert committed.read_text(encoding="utf-8") == rendered, (
                f"discovery copy drift: {committed.relative_to(repo_root)}; "
                f"run `make generate` from the repository root"
            )


def test_repo_workflow_skills_are_hidden_from_public_skill_discovery():
    repo_root = Path(__file__).resolve().parents[3]
    for surface in (Path(".agents") / "skills", Path(".claude") / "skills"):
        for name in ("flowmark", "tbd"):
            raw = (repo_root / surface / name / "SKILL.md").read_text(encoding="utf-8")
            frontmatter, _ = install._split_frontmatter(raw)
            metadata = yaml.safe_load(frontmatter)["metadata"]
            assert metadata["internal"] is True


def test_readme_leads_with_short_interactive_skill_commands():
    repo_root = Path(__file__).resolve().parents[3]
    readme = (repo_root / "README.md").read_text(encoding="utf-8")
    assert "npx skills add jlevy/practical-prose@pprose-common-edit" in readme
    assert "npx skills add jlevy/practical-prose@pprose-de-slop" in readme
    assert "npx skills add jlevy/practical-prose\n" in readme
    assert "npx --yes skills@" not in readme
