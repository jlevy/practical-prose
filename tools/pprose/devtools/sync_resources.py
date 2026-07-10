#!/usr/bin/env python3
"""Sync canonical repo docs into the packaged pprose resources, and render the
committed discovery copies under `skills/` at the repo root.

Two flows:

1.  Bundled resources (`docs/`, `shortcuts/`, `runbooks/` → `src/pprose/resources/`):
    the repo root holds the source of truth; this script copies the files into the
    wheel so `pprose` works standalone in any repo.

2.  Discovery skills (`src/pprose/resources/skills/*.md` → `skills/<name>/SKILL.md`):
    the *in-package* skill bodies are the source of truth; this script renders each
    one through `pprose install`'s compose path with `DISCOVERY_VERSION` baked into
    the bootstrap line, so the committed `skills/` directory at the repo root works
    as a `npx skills add` / `skills.sh` landing page (an unpinned discovery copy
    would silently re-resolve to the latest pprose on every run, bypassing the
    14-day cool-off window — see cli-agent-skill-patterns §6.7).

Link policy (flow 1): the repo-root sources keep ordinary relative links, which
work on GitHub; the bundled copies are read via `pprose <category> <name>` on
stdout in arbitrary repos, where relative paths mean nothing. So the sync
rewrites every Markdown link by where its target lives:

- target is another bundled resource → the `pprose` command that serves it
  (e.g. `pprose guidelines practical-prose-rubric`);
- target is a bundled category directory → the bare command that lists that category;
- target is repo content that is *not* bundled → an absolute GitHub URL;
- external URLs and same-document `#anchors` → left unchanged.

Run this whenever the canonical docs or the in-package skill bodies change.
`tests/test_resources_sync.py` fails if either drifts.

Usage:
  make generate        # from the repository root: sync everything
  make generate-check  # from the repository root: exit 1 if out of sync
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parents[1]  # tools/pprose
REPO_ROOT = Path(__file__).resolve().parents[3]  # repo root
RESOURCES = PKG_DIR / "src" / "pprose" / "resources"

# Categories synced from the repo root into the wheel. Skills are *not* in this list:
# their authored source now lives in the wheel at `resources/skills/`, and the repo-root
# `skills/` directory is a generated discovery surface rendered from those bodies.
SYNCED_CATEGORIES = ("guidelines", "shortcuts", "runbooks", "about")

GITHUB_BLOB = "https://github.com/jlevy/practical-prose/blob/main"
GITHUB_TREE = "https://github.com/jlevy/practical-prose/tree/main"

# Bundled source directory (repo-root-relative) → the pprose command that serves
# its files. This is the single mapping the link rewriter keys off.
DIR_TO_COMMAND = {
    "docs": "pprose guidelines",
    "shortcuts": "pprose shortcut",
    "runbooks": "pprose runbook",
}

_LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)\)")


def _command_for(rel: Path) -> str | None:
    """The `pprose` command that serves a bundled repo file, or None if not bundled."""
    parts = rel.parts
    if rel == Path("README.md"):
        return "pprose about"
    if len(parts) == 3 and parts[0] == "skills" and parts[2] == "SKILL.md":
        return f"pprose skill {parts[1]}"
    if len(parts) != 2 or parts[0] not in DIR_TO_COMMAND or rel.suffix != ".md":
        return None
    name = rel.name.replace(".runbook.md", ".md").removesuffix(".md")
    return f"{DIR_TO_COMMAND[parts[0]]} {name}"


def _rewrite_links(text: str, src: Path) -> str:
    """Rewrite Markdown links in a source doc for its bundled (wheel) copy."""

    def repl(m: re.Match[str]) -> str:
        bang, label, target = m.groups()
        if target.startswith("#") or re.match(r"^[a-z][a-z0-9+.-]*:", target):
            return m.group(0)
        path_part = target.partition("#")[0]
        resolved = Path(os.path.normpath(src.parent / path_part))
        try:
            rel = resolved.relative_to(REPO_ROOT)
        except ValueError:
            return m.group(0)
        if not bang:
            command = _command_for(rel)
            if command is not None:
                # The label usually *is* the target filename; then the command
                # replaces the whole link. Otherwise keep the prose label.
                if label.strip("*_` ") == resolved.name:
                    return f"`{command}`"
                return f"{label} (`{command}`)"
            if resolved.is_dir() and rel.as_posix() in DIR_TO_COMMAND:
                return f"`{DIR_TO_COMMAND[rel.as_posix()]}`"
        if not resolved.exists():
            return m.group(0)
        base = GITHUB_TREE if resolved.is_dir() else GITHUB_BLOB
        return f"{bang}[{label}]({base}/{rel.as_posix()})"

    return _LINK_RE.sub(repl, text)


def _synced_plan() -> dict[Path, str]:
    """Map every wheel resource path to its expected content (from the repo root).

    Bundles **public, cross-repo content only**. Repo-internal docs live under
    `/docs/project/` (excluded by the non-recursive `/docs/*.md` glob), and the
    repo's own `/AGENTS.md` is never bundled — pprose's job is to install a
    marker-bounded block into whatever AGENTS.md a project has, not to dictate
    its content.
    """
    plan: dict[Path, str] = {}

    def bundle(src: Path, dest: Path) -> None:
        plan[dest] = _rewrite_links(src.read_text(encoding="utf-8"), src)

    # /docs/*.md → guidelines (non-recursive; /docs/project/ stays internal).
    for p in sorted((REPO_ROOT / "docs").glob("*.md")):
        bundle(p, RESOURCES / "guidelines" / p.name)

    # /shortcuts/*.md → shortcuts.
    for p in sorted((REPO_ROOT / "shortcuts").glob("*.md")):
        bundle(p, RESOURCES / "shortcuts" / p.name)

    # /runbooks/*.runbook.md → runbooks (drop the `.runbook` infix so the command
    # reads `pprose runbook <name>`).
    for p in sorted((REPO_ROOT / "runbooks").glob("*.md")):
        bundle(p, RESOURCES / "runbooks" / p.name.replace(".runbook.md", ".md"))

    # README.md → about (the project narrative; surfaced as `pprose about`).
    readme = REPO_ROOT / "README.md"
    if readme.is_file():
        bundle(readme, RESOURCES / "about" / "readme.md")

    return plan


def _discovery_plan() -> dict[Path, str]:
    """Map every repo-root discovery skill path to its expected content."""
    # Imported here to avoid a circular dep at module-load time (install.py imports
    # from `pprose.resources`, which only loads its category dirs lazily).
    from pprose import install, resources

    plan: dict[Path, str] = {}
    for name in resources.list_names("skills"):
        rendered = install.compose_skill(name, pin=install.DISCOVERY_VERSION)
        plan[REPO_ROOT / "skills" / name / "SKILL.md"] = rendered
    return plan


def _expected_with_unmanaged() -> tuple[dict[Path, str], set[Path]]:
    """Combine the bundled + discovery plans; return (expected_map, unmanaged_files_seen).

    `unmanaged_files_seen` is empty for now; it exists so `check()` can distinguish
    "stale wheel resource" from "stale discovery skill" in the future.
    """
    expected: dict[Path, str] = {}
    expected.update(_synced_plan())
    expected.update(_discovery_plan())
    return expected, set()


def check() -> list[str]:
    """Return out-of-sync destination paths (empty == in sync)."""
    expected, _ = _expected_with_unmanaged()
    drift: list[str] = []
    for dest, content in expected.items():
        if not dest.is_file() or dest.read_text(encoding="utf-8") != content:
            drift.append(str(dest.relative_to(REPO_ROOT)))

    # Stale wheel resources (the bundled side; the in-package `skills/` dir is
    # authored and not managed here).
    for category in SYNCED_CATEGORIES:
        cat_dir = RESOURCES / category
        if cat_dir.is_dir():
            for existing in cat_dir.glob("*.md"):
                if existing not in expected:
                    drift.append(f"stale: {existing.relative_to(REPO_ROOT)}")
    return drift


def sync() -> None:
    expected, _ = _expected_with_unmanaged()
    for dest, content in expected.items():
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")

    # Remove stale bundled resources only (the discovery `skills/` dir at the repo
    # root is authored above and pruning there could discard user-authored files).
    for category in SYNCED_CATEGORIES:
        cat_dir = RESOURCES / category
        if cat_dir.is_dir():
            for existing in cat_dir.glob("*.md"):
                if existing not in expected:
                    existing.unlink()


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if "--check" in args:
        drift = check()
        if drift:
            print(
                "resources/discovery skills out of sync; "
                "run `make generate` from the repository root:"
            )
            for d in drift:
                print(f"  {d}")
            return 1
        print("resources and discovery skills in sync")
        return 0
    sync()
    print(
        f"synced wheel resources into {RESOURCES.relative_to(REPO_ROOT)} "
        f"and rendered discovery skills under skills/"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
