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

Run this whenever the canonical docs or the in-package skill bodies change.
`tests/test_resources_sync.py` fails if either drifts.

Usage:
  uv run python devtools/sync_resources.py            # sync everything
  uv run python devtools/sync_resources.py --check     # exit 1 if out of sync
"""

from __future__ import annotations

import sys
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parents[1]  # tools/pprose
REPO_ROOT = Path(__file__).resolve().parents[3]  # repo root
RESOURCES = PKG_DIR / "src" / "pprose" / "resources"

# Categories synced from the repo root into the wheel. Skills are *not* in this list:
# their authored source now lives in the wheel at `resources/skills/`, and the repo-root
# `skills/` directory is a generated discovery surface rendered from those bodies.
SYNCED_CATEGORIES = ("guidelines", "shortcuts", "runbooks")


def _synced_plan() -> dict[Path, str]:
    """Map every wheel resource path to its expected content (from the repo root)."""
    plan: dict[Path, str] = {}
    for p in sorted((REPO_ROOT / "docs").glob("*.md")):
        plan[RESOURCES / "guidelines" / p.name] = p.read_text(encoding="utf-8")
    for p in sorted((REPO_ROOT / "shortcuts").glob("*.md")):
        plan[RESOURCES / "shortcuts" / p.name] = p.read_text(encoding="utf-8")
    for p in sorted((REPO_ROOT / "runbooks").glob("*.md")):
        # Drop the ".runbook" infix so the command reads `pprose runbook <name>`.
        dest_name = p.name.replace(".runbook.md", ".md")
        plan[RESOURCES / "runbooks" / dest_name] = p.read_text(encoding="utf-8")
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
                "run `uv run python devtools/sync_resources.py`:"
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
