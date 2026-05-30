"""`pprose install` and `pprose skill` — install Practical Prose skills into a repo.

`pprose install` writes generated `SKILL.md` files into a target repo's project-local
agent surfaces — `.agents/skills/<name>/SKILL.md` for Codex/Gemini CLI/pi, plus a Claude
Code mirror at `.claude/skills/<name>/SKILL.md` — and a marker-bounded block in
`AGENTS.md`. Each generated artifact carries a `format=fNN surface=<id>` stamp so a
future pprose can detect older layouts and refresh them, and refuses to clobber any
artifact stamped with a newer format than it understands.

The bootstrap line baked into each generated skill points at the *installed* pprose
version, so the same `pprose <cmd>` invocations in the skill body work even when the
agent doesn't have `pprose` on its PATH (the `uvx pprose@<ver>` fallback handles it).
"""

from __future__ import annotations

import argparse
import re
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path
from typing import NamedTuple

from pprose import resources

PACKAGE_NAME = "pprose"

# Single monotonically-increasing format version stamped onto every pprose-generated
# artifact (skill SKILL.md mirrors + the AGENTS.md block). Bump when the on-disk shape
# of any generated artifact changes so a future pprose can detect and upgrade older
# layouts (and a forward-compat guard can refuse to clobber a newer format).
PPROSE_FORMAT = "f01"

# Pinned skill bootstrap fallback when an editable/dev pprose is installed. A dev build
# reports a PEP 440 dev/local segment (e.g. `0.0.1.dev53+f22b2cb`) that was never
# published to PyPI, so `uvx pprose@<dev-pin>` won't resolve. Bump this on each real
# PyPI release so the bootstrap line points at an installable version, and re-render
# the committed discovery copies under `skills/` at the repo root.
DISCOVERY_VERSION = "0.1.0"

# Surfaces touched by a project-local install. Two skill surfaces are byte-identical
# (`SURFACE_SKILL_MD`) — both portable (`.agents/skills/`) and Claude
# (`.claude/skills/`) write the same file; the marker only needs to identify it as a
# generated skill artifact, not which directory it lives in. `agents-md` is a
# marker-bounded block inside an `AGENTS.md` shared with other tools.
SURFACE_SKILL_MD = "skill-md"
SURFACE_AGENTS_MD = "agents-md"

# Per-target identifiers used for action reporting and the `--<target>` / `--skip-<target>`
# flag tri-state. `codex` covers `.agents/skills/` and the `AGENTS.md` block (Codex reads
# `.agents/skills/` natively and `AGENTS.md` is its primary instruction surface).
TARGET_CLAUDE = "claude"
TARGET_CODEX = "codex"
ALL_TARGETS = frozenset({TARGET_CLAUDE, TARGET_CODEX})

PORTABLE_SKILLS_DIR = Path(".agents") / "skills"
CLAUDE_SKILLS_DIR = Path(".claude") / "skills"

AGENTS_BEGIN_PREFIX = "<!-- BEGIN PPROSE INTEGRATION"
AGENTS_END_MARKER = "<!-- END PPROSE INTEGRATION -->"
_AGENTS_BLOCK_RE = re.compile(
    re.escape(AGENTS_BEGIN_PREFIX) + r".*?" + re.escape(AGENTS_END_MARKER), re.DOTALL
)
# Anchored on the BEGIN prefix so a stray `format=fXX` elsewhere in the file can't
# fool the forward-compatibility guard.
_AGENTS_BEGIN_STAMP_RE = re.compile(re.escape(AGENTS_BEGIN_PREFIX) + r"\s+format=f(\d+)")

# Format-stamp inside a generated SKILL.md (DO NOT EDIT marker line).
_SKILL_STAMP_RE = re.compile(r"format=f(\d+)\s+surface=skill-md")

# PEP 440 release identifier: digits + dots, optional `.postN`. Dev (`.devN`), pre-release
# (`aN`/`bN`/`rcN`/`cN`), and local (`+<hash>`) versions are deliberately rejected — they
# were never uploaded to PyPI, so `uvx pprose@<dev-pin>` against them can't resolve.
_PYPI_RELEASE_RE = re.compile(r"^\d+(?:\.\d+)*(?:\.post\d+)?$")


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
    # line intact (matches flowmark's pattern).
    return (
        f"<!-- DO NOT EDIT: generated by `pprose install` "
        f"(format={PPROSE_FORMAT} surface={SURFACE_SKILL_MD}) -->"
    )


def _bootstrap_line(pin: str) -> str:
    return (
        f"> Run pprose as `pprose <command>` if on PATH, else `uvx pprose@{pin} <command>` "
        f"(zero-install via uv). Run `pprose --help` for every command, "
        f"`pprose skill --list` for the other Practical Prose skills, and "
        f"`pprose shortcut --list` / `pprose guidelines --list` / `pprose runbook --list` "
        f"for on-demand playbooks, style guides, and procedures."
    )


def compose_skill(name: str, pin: str | None = None) -> str:
    """Render an installable SKILL.md: frontmatter + DO-NOT-EDIT marker + bootstrap + body.

    Deterministic: same inputs produce byte-identical output (no timestamps, no machine
    paths), so the drift test for the committed discovery copies under `skills/` is
    stable across machines and CI.
    """
    pin = pin if pin is not None else pinned_version()
    fm, body = _split_frontmatter(resources.read_doc("skills", name))
    head = f"---\n{fm}\n---\n" if fm else ""
    return (
        f"{head}{_skill_marker()}\n\n{_bootstrap_line(pin)}\n\n{body}"
    ).rstrip() + "\n"


def _skill_description(name: str) -> str:
    fm, _ = _split_frontmatter(resources.read_doc("skills", name))
    for line in fm.splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip()
    return ""


def skill_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Print a composed Practical Prose skill.")
    parser.add_argument("name", nargs="?", help="skill name (omit with --list)")
    parser.add_argument("--list", action="store_true", help="list installable skills")
    args = parser.parse_args(argv)

    if args.list or not args.name:
        for name in resources.list_names("skills"):
            print(f"{name}\t{_skill_description(name)}")
        return 0
    try:
        print(compose_skill(args.name))
    except FileNotFoundError as exc:
        parser.error(str(exc))
    return 0


def agents_md_block(pin: str | None = None, skills: list[str] | None = None) -> str:
    """The marker-bounded pprose block for a project's `AGENTS.md`.

    Compact (so it doesn't dominate the always-on AGENTS.md context). Routes the agent
    to `pprose --help` and the resource list commands rather than duplicating their
    output; the `format=fNN` field on the BEGIN marker lets a future pprose detect and
    upgrade older blocks (and refuse to clobber a newer one).
    """
    pin = pin if pin is not None else pinned_version()
    skills = skills if skills is not None else resources.list_names("skills")
    lines = [
        f"{AGENTS_BEGIN_PREFIX} format={PPROSE_FORMAT} surface={SURFACE_AGENTS_MD} -->",
        "## Practical Prose (pprose)",
        "",
        "Practical Prose tooling: deterministic metrics, rubric scoring, evaluation",
        "reports, and editorial workflows for practical documents.",
        "Use when the user asks to improve, audit, score, or compare practical documents.",
        "",
        f"Run pprose as `pprose <command>` if on PATH, else `uvx pprose@{pin} <command>`.",
        "Discover commands and workflows from the CLI itself:",
        "",
        "- `pprose --help` — every command and its summary.",
        "- `pprose skill --list` — installed workflow skills (also at",
        "  `.agents/skills/pprose-*/SKILL.md` and `.claude/skills/pprose-*/SKILL.md`).",
        "- `pprose shortcut --list`, `pprose guidelines --list`, `pprose runbook --list`",
        "  — on-demand playbooks, style guides, and procedures.",
        "",
        "Installed workflow skills:",
        "",
    ]
    lines += [f"- `{name}`" for name in skills]
    lines += ["", AGENTS_END_MARKER]
    return "\n".join(lines)


class InstallResult(NamedTuple):
    """Per-artifact result from a `pprose install` run."""

    target: str  # TARGET_CLAUDE or TARGET_CODEX (or "agents-md" for the shared block)
    surface: str  # SURFACE_SKILL_MD or SURFACE_AGENTS_MD
    skill: str | None  # skill name for a SKILL.md write, else None
    path: Path
    action: str  # "installed" | "updated" | "unchanged" | "blocked-newer"


def _existing_skill_format(path: Path) -> int | None:
    """Format number stamped on an existing generated SKILL.md; 0 if unmarked; None if absent."""
    if not path.is_file():
        return None
    m = _SKILL_STAMP_RE.search(path.read_text(encoding="utf-8"))
    return int(m.group(1)) if m else 0


def _write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _write_skill_file(
    skill_dir: Path, target: str, name: str, content: str
) -> InstallResult:
    out = skill_dir / "SKILL.md"
    existing = _existing_skill_format(out)
    # Forward-compatibility guard: never clobber a newer-format artifact.
    if existing is not None and existing > _format_num():
        return InstallResult(target, SURFACE_SKILL_MD, name, out, "blocked-newer")
    if out.is_file() and out.read_text(encoding="utf-8") == content:
        return InstallResult(target, SURFACE_SKILL_MD, name, out, "unchanged")
    action = "updated" if out.exists() else "installed"
    _write_atomic(out, content)
    return InstallResult(target, SURFACE_SKILL_MD, name, out, action)


def _update_agents_md(path: Path, block: str) -> InstallResult:
    """Insert or refresh the pprose block in `AGENTS.md`, preserving content outside markers.

    Collapses duplicate or stale blocks (e.g. left by an older install) to one current
    block at the position of the first stale block.
    """
    existing = path.read_text(encoding="utf-8") if path.is_file() else None

    if existing is not None and (m := _AGENTS_BEGIN_STAMP_RE.search(existing)):
        if int(m.group(1)) > _format_num():
            return InstallResult(
                "agents-md", SURFACE_AGENTS_MD, None, path, "blocked-newer"
            )

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
            existing[matches[i - 1].end() : matches[i].start()]
            for i in range(1, len(matches))
        ]
        tail_parts.append(existing[matches[-1].end() :])
        new_content = head + block + "".join(tail_parts)

    if existing == new_content:
        return InstallResult("agents-md", SURFACE_AGENTS_MD, None, path, "unchanged")
    action = "updated" if existing is not None else "installed"
    _write_atomic(path, new_content)
    return InstallResult("agents-md", SURFACE_AGENTS_MD, None, path, action)


def install(
    target_root: Path,
    targets: frozenset[str] = ALL_TARGETS,
    *,
    pin: str | None = None,
    write_agents_md: bool = True,
) -> list[InstallResult]:
    """Install pprose skills into `target_root`, returning per-artifact results.

    `targets` selects which agent integrations to write. Pass any subset of
    {`TARGET_CLAUDE`, `TARGET_CODEX`}. The Codex target includes both
    `.agents/skills/<name>/SKILL.md` (read natively by Codex/Gemini CLI/pi) and the
    `AGENTS.md` marker block; pass `write_agents_md=False` to suppress only the
    AGENTS.md update while keeping the portable `.agents/skills/` mirror.

    `pin` overrides the version pin baked into generated skills (defaults to the
    running pprose version when it's a real PyPI release, else `DISCOVERY_VERSION`).

    Idempotent: re-running an up-to-date install reports `unchanged` and writes nothing.
    """
    pin = pin if pin is not None else pinned_version()
    skills = resources.list_names("skills")
    results: list[InstallResult] = []

    if TARGET_CODEX in targets:
        for name in skills:
            content = compose_skill(name, pin)
            results.append(
                _write_skill_file(
                    target_root / PORTABLE_SKILLS_DIR / name, TARGET_CODEX, name, content
                )
            )
        if write_agents_md:
            block = agents_md_block(pin, skills)
            results.append(_update_agents_md(target_root / "AGENTS.md", block))

    if TARGET_CLAUDE in targets:
        for name in skills:
            content = compose_skill(name, pin)
            results.append(
                _write_skill_file(
                    target_root / CLAUDE_SKILLS_DIR / name, TARGET_CLAUDE, name, content
                )
            )

    return results


def _print_summary(results: list[InstallResult], pin: str) -> None:
    print(f"\npprose skill installation (pinned pprose@{pin}):")
    if not results:
        print("  (no surfaces selected)")
        return
    counts: dict[str, int] = {}
    blocked: list[InstallResult] = []
    for r in results:
        counts[r.action] = counts.get(r.action, 0) + 1
        if r.action == "blocked-newer":
            blocked.append(r)
    for action in ("installed", "updated", "unchanged", "blocked-newer"):
        if action in counts:
            print(f"  {action}: {counts[action]}")
    for r in results:
        tag = f"{r.target}:{r.skill}" if r.skill else r.target
        marker = "!" if r.action == "blocked-newer" else " "
        print(f"  {marker} [{r.action}] {tag}\t{r.path}")
    if blocked:
        print(
            "\nA newer pprose generated some of those artifacts. Upgrade pprose "
            "(`uv tool install --upgrade pprose` or `uvx pprose@latest --help`) "
            "and re-run install."
        )


def install_main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Install Practical Prose skills into a repo "
            "(.agents/skills + .claude/skills + an AGENTS.md block)."
        ),
    )
    parser.add_argument("--dir", default=".", help="target repo root (default: cwd)")
    parser.add_argument(
        "--auto", action="store_true", help="non-interactive (for agents)"
    )
    parser.add_argument(
        "--print",
        action="store_true",
        help="print the generated SKILL.md files to stdout; write nothing",
    )
    parser.add_argument(
        "--all", action="store_true", help="install every supported target (default)"
    )
    parser.add_argument(
        "--claude",
        action="store_true",
        help=f"install/refresh the Claude Code target ({CLAUDE_SKILLS_DIR})",
    )
    parser.add_argument(
        "--codex",
        action="store_true",
        help=f"install/refresh the Codex target ({PORTABLE_SKILLS_DIR} + AGENTS.md block)",
    )
    parser.add_argument(
        "--skip-claude", action="store_true", help="suppress the Claude Code target"
    )
    parser.add_argument(
        "--skip-codex", action="store_true", help="suppress the Codex target"
    )
    parser.add_argument(
        "--no-agents-md",
        action="store_true",
        help="suppress only the AGENTS.md block (keep .agents/skills/)",
    )
    parser.add_argument(
        "--pin",
        metavar="VERSION",
        help=(
            "override the pprose version pin baked into generated skills "
            "(default: installed pprose if it's a real PyPI release, else DISCOVERY_VERSION)"
        ),
    )
    args = parser.parse_args(argv)

    pin = args.pin if args.pin else pinned_version()
    skills = resources.list_names("skills")
    target = Path(args.dir).resolve()

    if args.print:
        for name in skills:
            print(f"# === {PORTABLE_SKILLS_DIR}/{name}/SKILL.md ===")
            print(f"# === {CLAUDE_SKILLS_DIR}/{name}/SKILL.md ===")
            print(compose_skill(name, pin))
        print(f"# === AGENTS.md (pprose block) ===\n{agents_md_block(pin, skills)}")
        return 0

    # Surface selection: a positive `--<target>` flag forces just that target
    # (suppressing the unflagged ones); `--skip-<target>` forces it off. No flag
    # means install everything (no detection needed; pprose installs from scratch).
    has_positive = args.all or args.claude or args.codex
    if has_positive:
        selected: set[str] = set()
        if args.all or args.claude:
            selected.add(TARGET_CLAUDE)
        if args.all or args.codex:
            selected.add(TARGET_CODEX)
    else:
        selected = set(ALL_TARGETS)
    if args.skip_claude:
        selected.discard(TARGET_CLAUDE)
    if args.skip_codex:
        selected.discard(TARGET_CODEX)

    results = install(
        target,
        frozenset(selected),
        pin=pin,
        write_agents_md=not args.no_agents_md,
    )
    _print_summary(results, pin)

    blocked = any(r.action == "blocked-newer" for r in results)
    return 1 if blocked else 0


def main(argv: list[str] | None = None) -> int:
    return install_main(argv)


if __name__ == "__main__":
    sys.exit(main())
