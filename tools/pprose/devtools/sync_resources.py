#!/usr/bin/env python3
"""Sync canonical repo docs into the packaged pprose resources, and render the
committed discovery copies under `skills/` at the repo root.

Three flows:

1.  Bundled resources (`docs/`, `shortcuts/`, `runbooks/` → `src/pprose/resources/`):
    the repo root holds the source of truth; this script copies the files into the
    wheel so `pprose` works standalone in any repo.

2.  Discovery skills (`src/pprose/resources/skills/*.md` → `skills/<name>/SKILL.md`):
    the *in-package* skill bodies are the source of truth; this script renders each
    one through `pprose install`'s compose path with `DISCOVERY_VERSION` baked into
    CLI-backed bootstrap lines, so the committed `skills/` directory at the repo root
    works as a `npx skills add` / `skills.sh` landing page (an unpinned discovery copy
    would silently re-resolve to the latest pprose on every run, bypassing the 14-day
    cool-off window — see cli-agent-skill-patterns §6.7). Self-contained skills are
    runtime-free and carry their guidelines under `references/` instead; those
    references are composed from flow 1's in-memory plan, not the on-disk wheel
    copies, so one sync pass converges even when `docs/` changed (see
    `_discovery_plan`).

3.  Repo workflow skills (`flowmark`, `tbd` under `.agents/skills/` and
    `.claude/skills/`): retain their generated bodies but add
    `metadata.internal: true` so public skill discovery does not offer this repo's
    development tools alongside Practical Prose.

4.  Dogfooded Practical Prose skills (`skills/<name>/` → `.agents/skills/<name>/`):
    this repo installs its own skills for its own agents. The portable surface holds
    real copies because not every agent follows symlinks, so it is mirrored from the
    generated discovery tree and drift-checked here. The Claude surface
    (`.claude/skills/<name>`) instead uses relative symlinks into `skills/`, so it
    cannot drift by construction and needs no plan entry;
    `tests/test_install.py::test_claude_dogfood_skills_are_symlinks_into_discovery`
    holds that convention in place.

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

INTERNAL_REPO_SKILLS = tuple(
    REPO_ROOT / surface / name / "SKILL.md"
    for surface in (Path(".agents") / "skills", Path(".claude") / "skills")
    for name in ("flowmark", "tbd")
)

# This repo's portable agent surface, mirrored from the generated `skills/` tree
# (flow 4). The Claude surface is symlinked into that same tree instead.
DOGFOOD_PORTABLE_ROOT = REPO_ROOT / ".agents" / "skills"


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


def _discovery_plan(synced: dict[Path, str]) -> dict[Path, str]:
    """Map every repo-root discovery skill path to its expected content.

    Bundled guideline references are composed from `synced` (the in-memory guideline
    content just planned from the repo root), NOT from the on-disk wheel resources.
    Reading the disk here once made a single `make generate` bake stale guideline
    content into `skills/<name>/references/` whenever `docs/` changed in the same run
    (two passes were needed to converge). Composing from the plan makes one pass the
    fixed point, and lets `check()` report true expectations even while the wheel
    copies are stale. A runtime-free skill whose guideline is not a synced doc fails
    loudly here (KeyError) rather than silently composing from stale disk.
    """
    # Imported here to avoid a circular dep at module-load time (install.py imports
    # from `pprose.resources`, which only loads its category dirs lazily).
    from pprose import install, resources

    def guideline_text(name: str) -> str:
        return synced[RESOURCES / "guidelines" / f"{name}.md"]

    plan: dict[Path, str] = {}
    for name in resources.list_names("skills"):
        for relative, rendered in install.compose_skill_files(
            name, pin=install.DISCOVERY_VERSION, guideline_text=guideline_text
        ).items():
            plan[REPO_ROOT / "skills" / name / relative] = rendered
    return plan


def _with_internal_metadata(text: str) -> str:
    """Add the skills CLI's repo-internal discovery marker without reserializing YAML."""
    if "\nmetadata:\n  internal: true\n" in text:
        return text
    end = text.find("\n---\n", len("---\n"))
    if not text.startswith("---\n") or end < 0:
        raise ValueError("repo workflow skill must have YAML frontmatter")
    frontmatter = text[:end]
    if "\nmetadata:" in frontmatter:
        raise ValueError("repo workflow skill has metadata but is not marked internal")
    return text[:end] + "\nmetadata:\n  internal: true" + text[end:]


def _repo_workflow_plan() -> dict[Path, str]:
    """Map generated repo workflow skills to their public-discovery-safe content."""
    return {
        path: _with_internal_metadata(path.read_text(encoding="utf-8"))
        for path in INTERNAL_REPO_SKILLS
    }


def _dogfood_plan(discovery: dict[Path, str]) -> dict[Path, str]:
    """Mirror the generated discovery skills into this repo's portable agent surface.

    Without this, `.agents/skills/pprose-*/` were unmanaged copies left behind by some
    past `pprose install`: nothing regenerated them and no check compared them, so this
    repo's own agents could quietly run instructions older than `skills/`.
    """
    mirrored: dict[Path, str] = {}
    for source, content in discovery.items():
        relative = source.relative_to(REPO_ROOT / "skills")
        mirrored[DOGFOOD_PORTABLE_ROOT / relative] = content
    return mirrored


def _expected_with_unmanaged() -> tuple[dict[Path, str], set[Path]]:
    """Combine the bundled + discovery plans; return (expected_map, unmanaged_files_seen).

    `unmanaged_files_seen` is empty for now; it exists so `check()` can distinguish
    "stale wheel resource" from "stale discovery skill" in the future.
    """
    expected: dict[Path, str] = {}
    synced = _synced_plan()
    expected.update(synced)
    discovery = _discovery_plan(synced)
    expected.update(discovery)
    expected.update(_repo_workflow_plan())
    expected.update(_dogfood_plan(discovery))
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
