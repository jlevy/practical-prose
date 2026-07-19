"""`pprose install` and `pprose skill` — install Practical Prose skills into a repo.

`pprose install` runs in one of two **scopes**:

- **Project** (`--project`, the default when cwd is unambiguously inside a git repo)
  writes into `<target>/.agents/skills/<name>/SKILL.md` (Codex/Gemini CLI/pi),
  `<target>/.claude/skills/<name>/SKILL.md` (Claude Code), and a marker-bounded
  block in `<target>/AGENTS.md`, plus a minimal `CLAUDE.md` bridge or managed block.
- **User-global** (`--global`) writes into `$HOME/.agents/skills/<name>/SKILL.md`
  and `$HOME/.claude/skills/<name>/SKILL.md`, making the skills available across
  every project. Global mode never writes `$HOME/.codex/AGENTS.md` (skills are
  on-demand; the global AGENTS.md should stay compact and user-authored).

Outside an unambiguous project context (e.g. `$HOME`, `/tmp/scratch`, or any other
directory not inside a git repo), `--project` or `--global` must be passed explicitly
— there's no silent default.

The `--profile=common-docs|practical-prose` flag selects one scope-wide skill set;
repeatable `--skill <name>` flags select an exact custom set. The
`--surfaces=portable,claude,agents-md,claude-md` flag selects new install destinations.
`portable` → `.agents/skills/`; `claude` → `.claude/skills/`; `agents-md` → marker
block in `AGENTS.md`; `claude-md` → bridge or marker block in `CLAUDE.md` (instruction
files are project mode only). Existing pprose-managed destinations are always reconciled
to the selected set, and instruction files bring along the skill tree they reference.

Every generated artifact carries a `format=fNN` stamp so future pprose versions can
detect and refresh older layouts, and refuse to clobber any artifact stamped with a
newer format than they understand. The artifact type is identified by its location
(a `SKILL.md` under `.agents/skills/<name>/` or `.claude/skills/<name>/`, a
BEGIN/END-bounded block inside `AGENTS.md` or `CLAUDE.md`, or a stamped `CLAUDE.md`
bridge) rather than by a surface tag, so the portable and Claude `SKILL.md` copies stay
byte-identical.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from collections.abc import Callable
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import NamedTuple

from flowmark import reformat_text

from pprose import resources

PACKAGE_NAME = "pprose"
COMMON_EDIT_SKILL = "pprose-common-edit"
DE_SLOP_SKILL = "pprose-de-slop"
COMMON_GUIDELINES_REFERENCE = Path("references") / "common-doc-guidelines.md"
AI_PROSE_REFERENCE = Path("references") / "ai-prose-corrections.md"
RUNTIME_FREE_SKILL_REFERENCES = {
    COMMON_EDIT_SKILL: (COMMON_GUIDELINES_REFERENCE, "common-doc-guidelines"),
    DE_SLOP_SKILL: (AI_PROSE_REFERENCE, "ai-prose-corrections"),
}

# Single monotonically-increasing format version stamped onto every pprose-generated
# artifact. Bump when the on-disk shape changes so a future pprose can upgrade older
# layouts and a forward-compat guard can refuse to clobber a newer format.
PPROSE_FORMAT = "f02"

# Pinned skill bootstrap fallback when an editable/dev pprose is installed. A dev build
# reports a PEP 440 dev/local segment that was never published to PyPI, so
# `uvx pprose@<dev-pin>` won't resolve. Bump on each real PyPI release and re-render
# the committed discovery copies under `skills/` at the repo root (`make generate`).
# Enforced at release time: `devtools/check_release_version.py` (run from publish.yml)
# fails the publish unless this equals the release tag.
DISCOVERY_VERSION = "0.3.0"

# Install scopes.
SCOPE_PROJECT = "project"
SCOPE_GLOBAL = "global"

# Public install profiles. The default preserves the existing `pprose install`
# behavior; `common-docs` is the focused, runtime-free documentation policy.
PROFILE_COMMON_DOCS = "common-docs"
PROFILE_PRACTICAL_PROSE = "practical-prose"
DEFAULT_PROFILE = PROFILE_PRACTICAL_PROSE
ALL_PROFILES = (PROFILE_COMMON_DOCS, PROFILE_PRACTICAL_PROSE)

# Install-selector surfaces (the `--surfaces=` flag values + InstallResult.surface).
# These are install *destinations*, not artifact identities.
SURFACE_PORTABLE = "portable"  # .agents/skills/<name>/SKILL.md
SURFACE_CLAUDE = "claude"  # .claude/skills/<name>/SKILL.md
SURFACE_AGENTS_MD = "agents-md"  # marker block in AGENTS.md (project mode only)
SURFACE_CLAUDE_MD = "claude-md"  # CLAUDE.md bridge/block (project mode only)
ALL_INSTALL_SURFACES = frozenset(
    {SURFACE_PORTABLE, SURFACE_CLAUDE, SURFACE_AGENTS_MD, SURFACE_CLAUDE_MD}
)
_VALID_SURFACE_TOKENS = sorted(ALL_INSTALL_SURFACES | {"all"})

PORTABLE_SKILLS_DIR = Path(".agents") / "skills"
CLAUDE_SKILLS_DIR = Path(".claude") / "skills"

AGENTS_BEGIN_PREFIX = "<!-- BEGIN PPROSE INTEGRATION"
AGENTS_END_MARKER = "<!-- END PPROSE INTEGRATION -->"
_AGENTS_BLOCK_RE = re.compile(
    re.escape(AGENTS_BEGIN_PREFIX) + r".*?" + re.escape(AGENTS_END_MARKER), re.DOTALL
)
# Anchored on the BEGIN prefix so a stray `format=fXX` elsewhere can't fool the guard.
_AGENTS_BEGIN_STAMP_RE = re.compile(re.escape(AGENTS_BEGIN_PREFIX) + r"\s+format=f(\d+)")

# Format stamps in generated skills and the minimal Claude bridge. Each is anchored on
# pprose-specific marker wording so unrelated `format=fNN` text does not trigger the
# forward guard.
_SKILL_STAMP_RE = re.compile(r"generated by `pprose install`.*?format=f(\d+)")
_CLAUDE_BRIDGE_STAMP_RE = re.compile(r"<!-- generated by `pprose install` \(format=f(\d+)\) -->")

# PEP 440 release identifier: digits + dots, optional `.postN`. Dev (`.devN`), pre-
# release (`aN`/`bN`/`rcN`/`cN`), and local (`+<hash>`) versions are rejected — they
# were never uploaded to PyPI, so `uvx pprose@<dev-pin>` against them can't resolve.
_PYPI_RELEASE_RE = re.compile(r"^\d+(?:\.\d+)*(?:\.post\d+)?$")


def profile_skill_names(profile: str) -> tuple[str, ...]:
    """Return the ordered skill names included in a public install profile."""
    if profile == PROFILE_COMMON_DOCS:
        return ("pprose-common-edit",)
    if profile == PROFILE_PRACTICAL_PROSE:
        return tuple(resources.list_names("skills"))
    raise ValueError(f"unknown profile {profile!r}; valid: {', '.join(ALL_PROFILES)}")


# ─────────────────────────────────────────────────────────────────────────────
# Version pin handling
# ─────────────────────────────────────────────────────────────────────────────


def is_pypi_release(version_str: str) -> bool:
    """Whether `version_str` is a real, exact-pinnable published PyPI release."""
    return bool(_PYPI_RELEASE_RE.match(version_str))


def pinned_version() -> str:
    """Version to bake into the `uvx pprose@<pin>` fallback in generated skills.

    Returns the installed pprose version when it is a real PyPI release, otherwise
    `DISCOVERY_VERSION`. Editable/dev checkouts report a PEP 440 dev/local version
    that uvx can't resolve, so we pin to the last published release in that case.
    """
    try:
        installed = version(PACKAGE_NAME)
    except PackageNotFoundError:
        return DISCOVERY_VERSION
    return installed if is_pypi_release(installed) else DISCOVERY_VERSION


def _format_num() -> int:
    return int(PPROSE_FORMAT.lstrip("f"))


# ─────────────────────────────────────────────────────────────────────────────
# Scope resolution and pre-flight guards
# ─────────────────────────────────────────────────────────────────────────────


def _is_within_git_repo(path: Path) -> bool:
    """Whether `path` or any ancestor contains a `.git` entry.

    `.git` is a directory in a regular repo and a file in a worktree/submodule, so
    `.exists()` covers both.
    """
    return any((p / ".git").exists() for p in (path, *path.parents))


def _protected_target_reason(path: Path) -> str | None:
    """Return a human-readable reason if `path` is a path project-mode refuses to write to.

    `$HOME` and the filesystem root are the cases where a project-local install would
    silently land on the user's *global* agent surfaces (`~/.claude/skills/`,
    `~/.agents/skills/`, `~/AGENTS.md`). Anywhere else outside a git repo is caught
    by the git-repo guard.
    """
    resolved = path.resolve()
    if resolved.parent == resolved:
        return "filesystem root"
    try:
        if resolved == Path.home().resolve():
            return "home directory ($HOME)"
    except (OSError, RuntimeError):
        # Path.home() can raise on misconfigured systems; better safe than sorry.
        pass
    return None


# ─────────────────────────────────────────────────────────────────────────────
# Surface parsing
# ─────────────────────────────────────────────────────────────────────────────


class SurfaceSpec(NamedTuple):
    """Parsed surfaces plus flags for explicitly named project instruction files.

    Global mode silently drops project-only files from `all`, but rejects an explicit
    `agents-md` or `claude-md` request.
    """

    surfaces: frozenset[str]
    agents_md_explicit: bool
    claude_md_explicit: bool


def parse_surfaces(raw: str | None) -> SurfaceSpec:
    """Parse a `--surfaces=<comma-list>` value.

    `None` or omitted → all install surfaces.
    Tokens: any subset of `{portable, claude, agents-md, claude-md}` plus `all`.
    Empty or unknown tokens raise `ValueError` with a clear valid-values message.
    """
    if raw is None:
        return SurfaceSpec(
            ALL_INSTALL_SURFACES,
            agents_md_explicit=False,
            claude_md_explicit=False,
        )
    tokens = [t.strip() for t in raw.split(",") if t.strip()]
    if not tokens:
        raise ValueError(
            "--surfaces is empty; pass a comma-separated list of: "
            + ", ".join(_VALID_SURFACE_TOKENS)
        )
    expanded: set[str] = set()
    agents_md_explicit = False
    claude_md_explicit = False
    for tok in tokens:
        if tok == "all":
            expanded |= ALL_INSTALL_SURFACES
        elif tok in ALL_INSTALL_SURFACES:
            expanded.add(tok)
            if tok == SURFACE_AGENTS_MD:
                agents_md_explicit = True
            elif tok == SURFACE_CLAUDE_MD:
                claude_md_explicit = True
        else:
            raise ValueError(f"unknown surface {tok!r}; valid: " + ", ".join(_VALID_SURFACE_TOKENS))
    return SurfaceSpec(frozenset(expanded), agents_md_explicit, claude_md_explicit)


# ─────────────────────────────────────────────────────────────────────────────
# Skill content composition
# ─────────────────────────────────────────────────────────────────────────────


def _flowmark(text: str) -> str:
    """Format generated Markdown exactly as the repo's flowmark pre-commit hook would.

    pprose *generates* Markdown (the composed `SKILL.md` files and the `AGENTS.md`
    block); the repo's pre-commit hook then runs `flowmark-rs --auto` over those same
    files. Pre-applying the byte-identical flowmark-py transform here makes generation
    idempotent: `make generate`, `pprose install`, and the `test_resources_sync` drift
    check all emit flowmark-clean output the hook leaves untouched — instead of long
    lines the hook silently rewraps into uncommitted drift (the original CI break).

    The flags mirror flowmark-rs `--auto` and are verified byte-identical against it
    (see tests/test_install.py::test_generated_skills_are_flowmark_stable). flowmark is
    a guaranteed dependency (direct, and transitively via flexdoc), so this never
    falls back to unformatted output.
    """
    return reformat_text(text, width=88, semantic=True, cleanups=True, smartquotes=True)


def _split_frontmatter(raw: str) -> tuple[str, str]:
    """Return (frontmatter_without_delimiters, body). Empty frontmatter if absent."""
    lines = raw.splitlines()
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                return "\n".join(lines[1:i]), "\n".join(lines[i + 1 :]).lstrip("\n")
    return "", raw


def _skill_marker() -> str:
    # No internal `.` in the marker text so a flowmark/sentence-wrap pass leaves the
    # line intact. The artifact type is identified by file location (SKILL.md under a
    # `.agents/skills/<name>/` or `.claude/skills/<name>/` directory); the only
    # load-bearing field here is the format stamp.
    return f"<!-- DO NOT EDIT: generated by `pprose install` (format={PPROSE_FORMAT}) -->"


def _bootstrap_line(pin: str) -> str:
    return (
        f"> Run pprose as `pprose <command>` if on PATH, else `uvx pprose@{pin} <command>` "
        f"(zero-install via uv). Run `pprose --help` for every command, `pprose skill` "
        f"for the other Practical Prose skills, and `pprose list` for all on-demand "
        f"playbooks, style guides, and procedures (`pprose shortcut`, `pprose guidelines`, "
        f"`pprose runbook` each print one by name)."
    )


def compose_skill(name: str, pin: str | None = None) -> str:
    """Render a deterministic installable `SKILL.md` from its resource body.

    CLI-backed skills include a pinned bootstrap. Skills with bundled guideline
    references are runtime-free.
    """
    pin = pin if pin is not None else pinned_version()
    fm, body = _split_frontmatter(resources.read_doc("skills", name))
    head = f"---\n{fm}\n---\n" if fm else ""
    bootstrap = "" if name in RUNTIME_FREE_SKILL_REFERENCES else f"\n\n{_bootstrap_line(pin)}"
    composed = f"{head}{_skill_marker()}{bootstrap}\n\n{body}"
    return _flowmark(composed).rstrip() + "\n"


def compose_skill_files(
    name: str,
    pin: str | None = None,
    guideline_text: Callable[[str], str] | None = None,
) -> dict[Path, str]:
    """Render every file in an installable skill directory.

    `guideline_text` overrides where a runtime-free skill's bundled guideline body is
    read from (guideline name → markdown). Install-time callers omit it and read the
    wheel resources; `devtools/sync_resources.py` passes the same-run synced content so
    a single sync pass cannot bake a stale guideline into a bundled reference.
    """
    files = {Path("SKILL.md"): compose_skill(name, pin)}
    if reference := RUNTIME_FREE_SKILL_REFERENCES.get(name):
        path, guideline = reference
        text = (
            guideline_text(guideline)
            if guideline_text is not None
            else resources.read_doc("guidelines", guideline)
        )
        files[path] = _flowmark(text).rstrip() + "\n"
    return files


def _skill_description(name: str) -> str:
    fm, _ = _split_frontmatter(resources.read_doc("skills", name))
    for line in fm.splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip()
    return ""


def _print_skill_table() -> None:
    for name in resources.list_names("skills"):
        print(f"{name}\t{_skill_description(name)}")


def _print_skill_overview() -> None:
    """Intro paragraph + skill table + routing footer.

    The natural entry-point answer to "what does pprose do?" — `pprose skill` (no
    args) is short enough to skim and points the agent at the full bundled
    inventory (`pprose list`) for everything else.
    """
    print(
        "Practical Prose skills are workflow entry points for improving, auditing,\n"
        "scoring, or comparing practical documents. Each names a clear capability;\n"
        "run `pprose skill <name>` for the full composed SKILL.md.\n"
    )
    _print_skill_table()
    print(
        "\nFor deeper detail, the skills route to:\n"
        "  pprose list      — every bundled guideline, shortcut, runbook, and skill\n"
        "  pprose guidelines <name>   — a bundled style guide or writing rules\n"
        "  pprose shortcut <name>     — a workflow playbook the skills invoke\n"
        "  pprose runbook <name>      — an operational procedure (eval, compare)\n"
        "  pprose about               — the Practical Prose project narrative\n"
    )


def skill_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Print a Practical Prose skill: `pprose skill <name>` for the full composed "
            "SKILL.md, or `pprose skill` with no name for an overview of all skills."
        )
    )
    parser.add_argument("name", nargs="?", help="skill name; omit for an overview")
    args = parser.parse_args(argv)

    if args.name:
        try:
            print(compose_skill(args.name))
        except FileNotFoundError as exc:
            parser.error(str(exc))
        return 0
    _print_skill_overview()
    return 0


def agents_md_block(pin: str | None = None, skill_names: tuple[str, ...] | None = None) -> str:
    """The marker-bounded pprose block for a project's `AGENTS.md`.

    Minimal by design because it sits in always-on context. A common-only selection
    carries the standing documentation rule without a runtime; broader selections add
    CLI discovery pointers. The format stamp supports upgrades and forward guards.
    """
    pin = pin if pin is not None else pinned_version()
    selected = (
        skill_names if skill_names is not None else profile_skill_names(PROFILE_PRACTICAL_PROSE)
    )
    has_common = COMMON_EDIT_SKILL in selected
    has_de_slop = DE_SLOP_SKILL in selected
    has_cli_skill = any(name not in RUNTIME_FREE_SKILL_REFERENCES for name in selected)
    common_only = selected == (COMMON_EDIT_SKILL,)
    de_slop_only = selected == (DE_SLOP_SKILL,)
    # Authored as long lines; _flowmark applies the same semantic wrapping the
    # pre-commit hook would, so the block stays idempotent inside AGENTS.md.
    lines = [
        f"{AGENTS_BEGIN_PREFIX} format={PPROSE_FORMAT} -->",
        "## Practical Prose (pprose)",
        "",
    ]
    if common_only:
        lines.extend(
            [
                "Use `pprose-common-edit` whenever creating, editing, reviewing, or "
                "reorganizing Markdown documentation, unless the task is explicitly "
                "read-only. Read its bundled `references/common-doc-guidelines.md` in "
                "full, apply all applicable rules, and keep exactly one required footer "
                "on every governed document.",
            ]
        )
    elif de_slop_only:
        lines.extend(
            [
                "Use `pprose-de-slop` whenever prose is drafted or edited, and when "
                "asked to remove AI-writing tells, formulaic LLM prose, or machine-like "
                "phrasing. Read its bundled `references/ai-prose-corrections.md` in "
                "full, apply contextual judgment instead of a word blacklist, and "
                "preserve meaning, evidence, and voice.",
            ]
        )
    else:
        lines.extend(
            [
                "Practical Prose: an evaluation toolkit and editorial workflows for practical "
                "documents. Use when the user asks to improve, audit, score, or compare "
                "practical documents.",
                "",
            ]
        )
        if has_common:
            lines.extend(
                [
                    "For durable Markdown documentation, use `pprose-common-edit` whenever "
                    "creating, editing, reviewing, or reorganizing it, unless the task is "
                    "explicitly read-only. Keep the required guideline footer intact.",
                    "",
                ]
            )
        if has_de_slop:
            lines.extend(
                [
                    "Apply AI-slop reduction whenever drafting or editing prose, not "
                    "only on request: use `pprose-de-slop` to remove AI-writing tells "
                    "and formulaic LLM prose, applying its bundled catalog contextually "
                    "and preserving meaning and voice.",
                    "",
                ]
            )
        if has_cli_skill:
            lines.extend(
                [
                    "Discover the tool from the CLI itself: `pprose --help` for commands, "
                    "`pprose about` for the project narrative, `pprose skill` for the "
                    "workflow skills, and `pprose list` for every on-demand guideline, "
                    "shortcut, and runbook (`pprose guidelines|shortcut|runbook <name>` "
                    "prints one).",
                    "",
                    f"Run pprose as `pprose <command>` if on PATH, else `uvx pprose@{pin} "
                    "<command>` (zero-install via uv).",
                ]
            )
    lines.extend(["", AGENTS_END_MARKER])
    block = "\n".join(lines)
    return _flowmark(block).rstrip()


# ─────────────────────────────────────────────────────────────────────────────
# Filesystem writes
# ─────────────────────────────────────────────────────────────────────────────


class InstallResult(NamedTuple):
    """Per-artifact result from a `pprose install` run."""

    surface: str  # One of the SURFACE_* constants.
    skill: str | None  # skill name for a SKILL.md write, else None
    path: Path
    action: str  # "installed" | "updated" | "removed" | "unchanged" | "blocked-newer"


def _existing_skill_format(path: Path) -> int | None:
    """Format number stamped on an existing generated SKILL.md; 0 if unmarked; None if absent."""
    if not path.is_file():
        return None
    m = _SKILL_STAMP_RE.search(path.read_text(encoding="utf-8"))
    return int(m.group(1)) if m else 0


def _existing_instruction_format(path: Path) -> int | None:
    """Highest pprose block format in an instruction file, or 0 if unversioned."""
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    formats = [int(match.group(1)) for match in _AGENTS_BEGIN_STAMP_RE.finditer(text)]
    formats.extend(int(match.group(1)) for match in _CLAUDE_BRIDGE_STAMP_RE.finditer(text))
    return max(formats, default=0)


def _preflight_newer_formats(target_root: Path, surfaces: frozenset[str]) -> list[InstallResult]:
    """Find newer managed artifacts before any write or removal occurs."""
    blocked: list[InstallResult] = []
    skill_surfaces = (
        (SURFACE_PORTABLE, PORTABLE_SKILLS_DIR),
        (SURFACE_CLAUDE, CLAUDE_SKILLS_DIR),
    )
    for surface, relative_root in skill_surfaces:
        if surface not in surfaces:
            continue
        for name in resources.list_names("skills"):
            path = target_root / relative_root / name / "SKILL.md"
            existing = _existing_skill_format(path)
            if existing is not None and existing > _format_num():
                blocked.append(InstallResult(surface, name, path, "blocked-newer"))
    instruction_surfaces = (
        (SURFACE_AGENTS_MD, target_root / "AGENTS.md"),
        (SURFACE_CLAUDE_MD, target_root / "CLAUDE.md"),
    )
    for surface, path in instruction_surfaces:
        if surface not in surfaces:
            continue
        existing = _existing_instruction_format(path)
        if existing is not None and existing > _format_num():
            blocked.append(InstallResult(surface, None, path, "blocked-newer"))
    return blocked


def _has_managed_skill_tree(skills_root: Path) -> bool:
    """Whether a skill tree contains at least one pprose-generated skill."""
    for name in resources.list_names("skills"):
        existing = _existing_skill_format(skills_root / name / "SKILL.md")
        if existing is not None and existing > 0:
            return True
    return False


def _has_managed_instruction(path: Path) -> bool:
    """Whether an instruction file contains a pprose block or Claude bridge."""
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8")
    return AGENTS_BEGIN_PREFIX in text or _CLAUDE_BRIDGE_STAMP_RE.search(text) is not None


def _resolve_install_surfaces(
    target_root: Path,
    requested: frozenset[str],
    *,
    project_mode: bool,
) -> frozenset[str]:
    """Return every surface that must be reconciled in this install.

    `requested` controls which new destinations are created. Once pprose manages a
    destination, later profile or exact-skill changes must reach it even when a narrower
    `--surfaces` value is passed; otherwise different agents can silently use different
    skill sets. Instruction surfaces also require the matching skill tree so their
    always-on policy never names a skill or bundled reference that is absent.
    """
    surfaces = set(requested)
    if _has_managed_skill_tree(target_root / PORTABLE_SKILLS_DIR):
        surfaces.add(SURFACE_PORTABLE)
    if _has_managed_skill_tree(target_root / CLAUDE_SKILLS_DIR):
        surfaces.add(SURFACE_CLAUDE)

    if project_mode:
        if _has_managed_instruction(target_root / "AGENTS.md"):
            surfaces.add(SURFACE_AGENTS_MD)
        if _has_managed_instruction(target_root / "CLAUDE.md"):
            surfaces.add(SURFACE_CLAUDE_MD)

        if SURFACE_AGENTS_MD in surfaces:
            surfaces.add(SURFACE_PORTABLE)
        if SURFACE_CLAUDE_MD in surfaces:
            surfaces.add(SURFACE_CLAUDE)

    return frozenset(surfaces)


def _write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _write_skill_files(
    skill_dir: Path, surface: str, name: str, files: dict[Path, str]
) -> InstallResult:
    out = skill_dir / "SKILL.md"
    existing = _existing_skill_format(out)
    # Forward-compatibility guard: never clobber a newer-format artifact.
    if existing is not None and existing > _format_num():
        return InstallResult(surface, name, out, "blocked-newer")
    unchanged = all(
        (skill_dir / relative).is_file()
        and (skill_dir / relative).read_text(encoding="utf-8") == content
        for relative, content in files.items()
    )
    if unchanged:
        return InstallResult(surface, name, out, "unchanged")
    action = "updated" if out.exists() else "installed"
    for relative, content in files.items():
        _write_atomic(skill_dir / relative, content)
    return InstallResult(surface, name, out, action)


def _remove_unselected_skill_dirs(
    skills_root: Path,
    surface: str,
    selected: tuple[str, ...],
) -> list[InstallResult]:
    """Remove deselected pprose-owned skill directories and preserve user-owned ones."""
    results: list[InstallResult] = []
    for name in resources.list_names("skills"):
        if name in selected:
            continue
        skill_dir = skills_root / name
        skill_md = skill_dir / "SKILL.md"
        existing = _existing_skill_format(skill_md)
        if existing is None or existing == 0:
            continue
        if existing > _format_num():
            results.append(InstallResult(surface, name, skill_md, "blocked-newer"))
            continue
        if skill_dir.is_symlink():
            skill_dir.unlink()
        else:
            shutil.rmtree(skill_dir)
        results.append(InstallResult(surface, name, skill_md, "removed"))
    return results


def _update_agents_md(path: Path, block: str, surface: str = SURFACE_AGENTS_MD) -> InstallResult:
    """Insert or refresh the pprose block in `AGENTS.md`, preserving content outside markers.

    Collapses duplicate or stale blocks to one current block at the position of the
    first stale block.
    """
    existing = path.read_text(encoding="utf-8") if path.is_file() else None

    if existing is not None:
        formats = [int(match.group(1)) for match in _AGENTS_BEGIN_STAMP_RE.finditer(existing)]
        if formats and max(formats) > _format_num():
            return InstallResult(surface, None, path, "blocked-newer")

    if existing is None or AGENTS_BEGIN_PREFIX not in existing:
        if not existing:
            new_content = block + "\n"
        else:
            sep = "\n" if existing.endswith("\n") else "\n\n"
            new_content = existing + sep + block + "\n"
    else:
        # Replace every existing block (collapses stale duplicates to one).
        matches = list(_AGENTS_BLOCK_RE.finditer(existing))
        head = existing[: matches[0].start()]
        tail_parts = [
            existing[matches[i - 1].end() : matches[i].start()] for i in range(1, len(matches))
        ]
        tail_parts.append(existing[matches[-1].end() :])
        new_content = head + block + "".join(tail_parts)

    if existing == new_content:
        return InstallResult(surface, None, path, "unchanged")
    action = "updated" if existing is not None else "installed"
    _write_atomic(path, new_content)
    return InstallResult(surface, None, path, action)


def _update_claude_md(path: Path, block: str, agents_md_available: bool) -> InstallResult:
    """Make the pprose policy visible to Claude Code without replacing user content."""
    existing = path.read_text(encoding="utf-8") if path.is_file() else None
    imports_agents = existing is not None and re.search(r"(?m)^\s*@AGENTS\.md\s*$", existing)
    if agents_md_available and imports_agents:
        return InstallResult(SURFACE_CLAUDE_MD, None, path, "unchanged")
    if agents_md_available and existing is None:
        bridge = f"@AGENTS.md\n\n<!-- generated by `pprose install` (format={PPROSE_FORMAT}) -->\n"
        _write_atomic(path, bridge)
        return InstallResult(SURFACE_CLAUDE_MD, None, path, "installed")
    return _update_agents_md(path, block, surface=SURFACE_CLAUDE_MD)


def install(
    target_root: Path,
    surfaces: frozenset[str] = ALL_INSTALL_SURFACES,
    *,
    pin: str | None = None,
    skill_names: tuple[str, ...] | None = None,
) -> list[InstallResult]:
    """Install pprose skills into `target_root`, returning per-artifact results.

    `surfaces` is any subset of the `SURFACE_*` constants. The caller is responsible
    for scope-specific filtering (user-global mode drops project instruction files).

    `pin` overrides the version baked into CLI-backed skills (defaults to the running
    pprose version when it is a real PyPI release, else `DISCOVERY_VERSION`).

    Idempotent: re-running an up-to-date install reports `unchanged` and writes nothing.
    """
    pin = pin if pin is not None else pinned_version()
    skills = skill_names if skill_names is not None else tuple(resources.list_names("skills"))
    if blocked := _preflight_newer_formats(target_root, surfaces):
        return blocked
    results: list[InstallResult] = []

    if SURFACE_PORTABLE in surfaces:
        portable_root = target_root / PORTABLE_SKILLS_DIR
        results.extend(_remove_unselected_skill_dirs(portable_root, SURFACE_PORTABLE, skills))
        for name in skills:
            files = compose_skill_files(name, pin)
            results.append(
                _write_skill_files(
                    portable_root / name,
                    SURFACE_PORTABLE,
                    name,
                    files,
                )
            )
    if SURFACE_CLAUDE in surfaces:
        claude_root = target_root / CLAUDE_SKILLS_DIR
        results.extend(_remove_unselected_skill_dirs(claude_root, SURFACE_CLAUDE, skills))
        for name in skills:
            files = compose_skill_files(name, pin)
            results.append(
                _write_skill_files(
                    claude_root / name,
                    SURFACE_CLAUDE,
                    name,
                    files,
                )
            )
    if SURFACE_AGENTS_MD in surfaces:
        block = agents_md_block(pin, skills)
        results.append(_update_agents_md(target_root / "AGENTS.md", block))
    if SURFACE_CLAUDE_MD in surfaces:
        block = agents_md_block(pin, skills)
        agents_path = target_root / "AGENTS.md"
        agents_md_available = SURFACE_AGENTS_MD in surfaces or (
            agents_path.is_file() and AGENTS_BEGIN_PREFIX in agents_path.read_text(encoding="utf-8")
        )
        results.append(
            _update_claude_md(
                target_root / "CLAUDE.md",
                block,
                agents_md_available=agents_md_available,
            )
        )

    return results


# ─────────────────────────────────────────────────────────────────────────────
# CLI entry point
# ─────────────────────────────────────────────────────────────────────────────


def _print_summary(results: list[InstallResult], pin: str, skill_names: tuple[str, ...]) -> None:
    if not results:
        print("\npprose install: no surfaces selected (nothing to do).")
        return
    has_cli_skill = any(name not in RUNTIME_FREE_SKILL_REFERENCES for name in skill_names)
    qualifier = f"CLI fallback pprose@{pin}" if has_cli_skill else "runtime-free skills"
    print(f"\npprose skill installation ({qualifier}):")
    counts: dict[str, int] = {}
    blocked: list[InstallResult] = []
    for r in results:
        counts[r.action] = counts.get(r.action, 0) + 1
        if r.action == "blocked-newer":
            blocked.append(r)
    for action in ("installed", "updated", "removed", "unchanged", "blocked-newer"):
        if action in counts:
            print(f"  {action}: {counts[action]}")
    for r in results:
        tag = f"{r.surface}:{r.skill}" if r.skill else r.surface
        marker = "!" if r.action == "blocked-newer" else " "
        print(f"  {marker} [{r.action}] {tag}\t{r.path}")
    if blocked:
        print(
            "\nA newer pprose generated some of those artifacts. Upgrade pprose "
            "(`uv tool upgrade pprose` or `uvx pprose --help`) "
            "and re-run install."
        )


_HELP_EPILOG = """\
Scope:
  In a git repo (and not $HOME), --project is implicit.
  Outside a git repo or in $HOME, pass --project or --global explicitly.
  $HOME is always refused in --project mode; use --global for a user-wide install.

Selection:
  --profile common-docs installs the runtime-free documentation policy.
  --profile practical-prose installs the complete suite and is the default.
  Repeat --skill for an exact custom set. Profiles and --skill are mutually exclusive.
  The selected set is scope-wide. Changing it reconciles every existing
  pprose-managed destination and removes only deselected, generated skill directories.

Surfaces:
  --surfaces controls which new destinations are created. Existing managed destinations
  stay in sync. agents-md includes portable skills; claude-md includes Claude skills so
  an instruction file never references an absent skill or bundled guideline.

Cross-scope coexistence: project-scope skills shadow user-scope skills of the same
name in modern agents (Codex documents this; Claude Code's two discovery paths
imply the same layering). Installing both globally and per-project is a supported
pattern, not a conflict.
"""


def install_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="pprose install",
        description=(
            "Install Practical Prose skills into a project (--project, default when "
            "cwd is unambiguously inside a git repo) or globally for the current user "
            "(--global). Outside an unambiguous project context, --project or --global "
            "must be passed explicitly."
        ),
        epilog=_HELP_EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    # `--project` and `--global` are mutually exclusive, but we check that manually
    # so the error message uses our own wording (and returns an exit code rather
    # than the SystemExit that add_mutually_exclusive_group raises).
    parser.add_argument(
        "--project",
        action="store_true",
        help="install project-locally (default when cwd is inside a git repo)",
    )
    # `dest='global_'` because `global` is a Python keyword.
    parser.add_argument(
        "--global",
        action="store_true",
        dest="global_",
        help=f"install for the current user ({PORTABLE_SKILLS_DIR} + {CLAUDE_SKILLS_DIR} under $HOME)",
    )
    parser.add_argument(
        "--dir",
        default=None,
        help="project root for --project (default: cwd; incompatible with --global)",
    )
    parser.add_argument(
        "--no-repo-check",
        action="store_true",
        help="allow --project outside a git repo (still refuses $HOME)",
    )
    parser.add_argument(
        "--surfaces",
        default=None,
        metavar="LIST",
        help=(
            "comma-separated subset of new surfaces to install; existing pprose-managed "
            "surfaces are also reconciled. "
            "Values: portable (.agents/skills/), claude (.claude/skills/), "
            "agents-md (AGENTS.md block; project mode only), claude-md "
            "(CLAUDE.md bridge/block; project mode only), all (default if omitted). "
            "Instruction surfaces include their matching skill tree. "
            "Example: --surfaces=portable,agents-md"
        ),
    )
    parser.add_argument(
        "--profile",
        choices=ALL_PROFILES,
        default=None,
        help=(
            "skill set to install: common-docs (one self-contained documentation "
            "policy skill) or practical-prose (the complete editing and evaluation suite; default)"
        ),
    )
    parser.add_argument(
        "--skill",
        action="append",
        choices=resources.list_names("skills"),
        default=None,
        help="install exactly this skill; repeat to select more (incompatible with --profile)",
    )
    parser.add_argument(
        "--pin",
        metavar="VERSION",
        help=(
            "override the pprose version pin baked into generated skills "
            "(default: installed pprose if it's a real PyPI release, else DISCOVERY_VERSION)"
        ),
    )
    parser.add_argument(
        "--auto",
        action="store_true",
        help="non-interactive (for agents); does not relax the ambiguity check",
    )
    args = parser.parse_args(argv)

    if args.profile is not None and args.skill:
        print(
            "pprose install: error: --profile and --skill are mutually exclusive.",
            file=sys.stderr,
        )
        return 2

    # Parse --surfaces first; argument-shape errors return exit 2 (argparse convention).
    try:
        spec = parse_surfaces(args.surfaces)
    except ValueError as exc:
        print(f"pprose install: error: {exc}", file=sys.stderr)
        return 2

    # Mutually exclusive scope flags.
    if args.project and args.global_:
        print(
            "pprose install: error: --project and --global are mutually exclusive.",
            file=sys.stderr,
        )
        return 2
    if args.global_ and args.dir is not None:
        print(
            "pprose install: error: --global and --dir are mutually exclusive "
            "(--global always writes under $HOME).",
            file=sys.stderr,
        )
        return 2

    # Resolve scope and target.
    if args.global_:
        scope = SCOPE_GLOBAL
        target = Path.home()
    else:
        target = Path(args.dir if args.dir is not None else ".").resolve()
        if args.project:
            scope = SCOPE_PROJECT
        else:
            # Implicit: project iff cwd is unambiguously a project.
            protected = _protected_target_reason(target)
            if protected:
                print(
                    f"pprose install: ambiguous scope ({target} is your "
                    f"{protected}). Pass --project (with --dir <project-root>) or "
                    f"--global explicitly.",
                    file=sys.stderr,
                )
                return 2
            if not _is_within_git_repo(target):
                print(
                    f"pprose install: ambiguous scope ({target} is not inside a "
                    f"git repository). Pass --project --no-repo-check or --global "
                    f"explicitly, or cd into your project root.",
                    file=sys.stderr,
                )
                return 2
            scope = SCOPE_PROJECT

    # Scope-specific guards and surface filtering.
    if scope == SCOPE_PROJECT:
        protected = _protected_target_reason(target)
        if protected:
            print(
                f"pprose install --project: refusing to install into {target} "
                f"({protected}). That would write to your global agent surfaces "
                f"(~/.agents/skills/, ~/.claude/skills/, ~/AGENTS.md). Use "
                f"--global for a user-wide install, or pass --dir <project-root>.",
                file=sys.stderr,
            )
            return 2
        if not args.no_repo_check and not _is_within_git_repo(target):
            print(
                f"pprose install --project: {target} is not inside a git repository. "
                f"Pass --no-repo-check to install here anyway, or cd into your project root.",
                file=sys.stderr,
            )
            return 2
        selected = spec.surfaces
        mode_label = "project mode"
    else:  # SCOPE_GLOBAL
        if spec.agents_md_explicit or spec.claude_md_explicit:
            named = "agents-md" if spec.agents_md_explicit else "claude-md"
            print(
                f"pprose install --global: {named} is not supported in --global mode "
                "(the global Codex AGENTS.md at ~/.codex/AGENTS.md should stay "
                "user-authored). Drop project instruction files from --surfaces, "
                "or use --project.",
                file=sys.stderr,
            )
            return 2
        # `--surfaces=all` (or omitted) silently drops project instruction files.
        selected = spec.surfaces - {SURFACE_AGENTS_MD, SURFACE_CLAUDE_MD}
        mode_label = "user-global mode"

    pin = args.pin if args.pin else pinned_version()
    selected_skills = (
        tuple(dict.fromkeys(args.skill))
        if args.skill
        else profile_skill_names(args.profile or DEFAULT_PROFILE)
    )
    selected = _resolve_install_surfaces(
        target,
        selected,
        project_mode=scope == SCOPE_PROJECT,
    )

    # Pre-write target message — last thing printed before any filesystem writes,
    # so an interactive user can ctrl-c if the resolved target or surface list is wrong.
    print(f"Installing pprose skills ({mode_label}) into: {target}")
    print(f"  skills: {', '.join(selected_skills)}")
    if selected:
        print(f"  surfaces: {', '.join(sorted(selected))}")

    results = install(
        target,
        selected,
        pin=pin,
        skill_names=selected_skills,
    )
    _print_summary(results, pin, selected_skills)

    blocked = any(r.action == "blocked-newer" for r in results)
    return 1 if blocked else 0


def main(argv: list[str] | None = None) -> int:
    return install_main(argv)


if __name__ == "__main__":
    sys.exit(main())
