#!/usr/bin/env python3
"""Sync canonical repo docs into the packaged pprose resources.

The repo root holds the source of truth (docs/, shortcuts/, skills/). The wheel
must be self-contained so `uvx pprose` works in any repo, so we copy those files
into src/pprose/resources/. Run this whenever the canonical files change;
tests/test_resources_sync.py fails if the bundled copies drift.

Usage:
  uv run python devtools/sync_resources.py            # sync
  uv run python devtools/sync_resources.py --check     # exit 1 if out of sync
"""

from __future__ import annotations

import sys
from pathlib import Path

PKG_DIR = Path(__file__).resolve().parents[1]  # tools/pprose
REPO_ROOT = Path(__file__).resolve().parents[3]  # repo root
RESOURCES = PKG_DIR / "src" / "pprose" / "resources"

# category -> list of (source_path, dest_filename)
def _plan() -> dict[str, list[tuple[Path, str]]]:
    plan: dict[str, list[tuple[Path, str]]] = {"guidelines": [], "shortcuts": [], "skills": []}
    for p in sorted((REPO_ROOT / "docs").glob("*.md")):
        plan["guidelines"].append((p, p.name))
    for p in sorted((REPO_ROOT / "shortcuts").glob("*.md")):
        plan["shortcuts"].append((p, p.name))
    for skill_md in sorted((REPO_ROOT / "skills").glob("*/SKILL.md")):
        plan["skills"].append((skill_md, f"{skill_md.parent.name}.md"))
    return plan


def _expected() -> dict[Path, str]:
    """Map every destination path to its expected content."""
    out: dict[Path, str] = {}
    for category, items in _plan().items():
        for src, dest_name in items:
            out[RESOURCES / category / dest_name] = src.read_text(encoding="utf-8")
    return out


def check() -> list[str]:
    """Return a list of out-of-sync destination paths (empty == in sync)."""
    expected = _expected()
    drift: list[str] = []
    for dest, content in expected.items():
        if not dest.is_file() or dest.read_text(encoding="utf-8") != content:
            drift.append(str(dest.relative_to(PKG_DIR)))
    # Stale files present in resources but no longer in the plan.
    for category in ("guidelines", "shortcuts", "skills"):
        cat_dir = RESOURCES / category
        if cat_dir.is_dir():
            for existing in cat_dir.glob("*.md"):
                if existing not in expected:
                    drift.append(f"stale: {existing.relative_to(PKG_DIR)}")
    return drift


def sync() -> None:
    expected = _expected()
    for dest, content in expected.items():
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
    # Remove stale files.
    for category in ("guidelines", "shortcuts", "skills"):
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
            print("resources out of sync; run `uv run python devtools/sync_resources.py`:")
            for d in drift:
                print(f"  {d}")
            return 1
        print("resources in sync")
        return 0
    sync()
    print(f"synced resources into {RESOURCES.relative_to(PKG_DIR)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
