#!/usr/bin/env python3
"""Release-time guard: the published version must match the baked discovery pin.

`publish.yml` runs this before building, passing the release tag (e.g. `v0.1.0`). It
fails the publish unless `install.DISCOVERY_VERSION` — the fallback version baked into
the committed discovery skills under `skills/` and the `AGENTS.md` block — equals the tag
being released. Combined with `tests/test_resources_sync.py` (which fails if the
committed skills drift from `DISCOVERY_VERSION`), this chains
`tag == DISCOVERY_VERSION == committed uvx pprose@<pin>` bootstrap, so a release can never
ship skills whose zero-install pin points at a different version than the one published.

Why this is needed: an installed real release already self-pins correctly (see
`install.pinned_version`), but the committed discovery copies are rendered from a *dev*
checkout, so they fall back to the hand-maintained `DISCOVERY_VERSION`. This guard is the
automated check that the fallback was bumped to match the tag before release.

Usage:
  uv run python devtools/check_release_version.py v0.1.0   # exit 1 on mismatch
  uv run python devtools/check_release_version.py          # reads $GITHUB_REF_NAME
"""

from __future__ import annotations

import os
import sys

from pprose import install


def normalize_tag(tag: str) -> str:
    """Strip a leading `v` from a release tag: `v0.1.0` -> `0.1.0`."""
    return tag[1:] if tag.startswith("v") else tag


def verify(tag: str, discovery_version: str | None = None) -> list[str]:
    """Return a list of human-readable problems; an empty list means consistent.

    Checks that the release tag is a plain, pip-resolvable PyPI release version and that
    it equals the discovery pin baked into the committed skills.
    """
    if discovery_version is None:
        discovery_version = install.DISCOVERY_VERSION
    expected = normalize_tag(tag.strip())
    if not expected:
        return ["empty release tag"]
    problems: list[str] = []
    if not install.is_pypi_release(expected):
        problems.append(
            f"release tag {expected!r} is not a plain PyPI release version "
            "(expected digits and dots, optional .postN)"
        )
    if expected != discovery_version:
        problems.append(
            f"release tag {expected!r} != install.DISCOVERY_VERSION {discovery_version!r}; "
            "bump DISCOVERY_VERSION and re-render skills (`make generate`) before tagging"
        )
    return problems


def main(argv: list[str]) -> int:
    tag = argv[0] if argv else os.environ.get("GITHUB_REF_NAME", "")
    if not tag:
        print("error: no release tag given (argv[0] or $GITHUB_REF_NAME)", file=sys.stderr)
        return 2
    problems = verify(tag)
    if problems:
        print("Release version check FAILED:", file=sys.stderr)
        for problem in problems:
            print(f"  - {problem}", file=sys.stderr)
        return 1
    print(
        f"Release version check OK: tag {tag} matches DISCOVERY_VERSION {install.DISCOVERY_VERSION}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
