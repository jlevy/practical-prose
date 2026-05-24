"""Access to the docs/shortcuts/skill bodies bundled in the wheel.

The canonical files live at the repo root (docs/, shortcuts/, skills/);
devtools/sync_resources.py copies them here so `uvx pprose` is self-contained
and works in any repo. See tests/test_resources_sync.py for the drift check.
"""

from __future__ import annotations

from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
RESOURCES_DIR = PACKAGE_ROOT / "resources"
CATEGORIES = ("guidelines", "shortcuts", "skills")


def _category_dir(category: str) -> Path:
    if category not in CATEGORIES:
        raise ValueError(f"unknown category {category!r}; valid: {', '.join(CATEGORIES)}")
    return RESOURCES_DIR / category


def list_names(category: str) -> list[str]:
    """Sorted doc names (filename stems) available in a category."""
    return sorted(p.stem for p in _category_dir(category).glob("*.md"))


def doc_path(category: str, name: str) -> Path:
    """Path to a bundled doc, raising a clear error (with valid names) if missing."""
    path = _category_dir(category) / f"{name}.md"
    if not path.is_file():
        valid = ", ".join(list_names(category)) or "(none)"
        raise FileNotFoundError(f"no {category} named {name!r}; available: {valid}")
    return path


def read_doc(category: str, name: str) -> str:
    return doc_path(category, name).read_text(encoding="utf-8")


def doc_title(category: str, name: str) -> str:
    """Best-effort human title: frontmatter `title:`, else first `# ` heading, else name."""
    text = read_doc(category, name)
    lines = text.splitlines()
    if lines and lines[0].strip() == "---":
        for line in lines[1:]:
            if line.strip() == "---":
                break
            if line.startswith("title:"):
                return line.split(":", 1)[1].strip().strip("\"'")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return name
