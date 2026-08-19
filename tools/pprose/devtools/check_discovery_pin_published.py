#!/usr/bin/env python3
"""Drift guard: the baked discovery pin must name a version that exists on PyPI.

`check_release_version.py` chains `tag == DISCOVERY_VERSION == committed pin` at publish
time, which proves a release ships a self-consistent bootstrap. It cannot prove the
release happened at all. Bumping `DISCOVERY_VERSION`, merging, and then never tagging
leaves `main` advertising `uvx pprose@<pin>` for a version PyPI has never heard of, and
every skill installed from the committed `skills/` tree gets a hard resolver failure on
its zero-install fallback. That is exactly how 0.3.1 shipped a broken bootstrap: prepped,
merged, never tagged, undetected.

This check closes that gap from the other side by asking PyPI whether the pin resolves.

It is deliberately NOT a pull-request gate. The release procedure bumps the pin in one
commit and tags shortly after, so `main` is legitimately ahead of PyPI for that window;
failing PRs during it would train maintainers to ignore the signal. Running it on a
schedule instead means a forgotten release surfaces within a day, while a normal release
window closes long before the next run.

Usage:
  uv run python devtools/check_discovery_pin_published.py    # exit 1 if unpublished
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

from pprose import install

PYPI_JSON_URL = "https://pypi.org/pypi/{package}/json"
TIMEOUT_SECONDS = 30


def published_versions(package: str = install.PACKAGE_NAME) -> set[str]:
    """Every version PyPI lists for `package`.

    Raises `RuntimeError` on any transport or payload problem so a network blip reads as
    an infrastructure failure rather than as "the pin is unpublished".
    """
    url = PYPI_JSON_URL.format(package=package)
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_SECONDS) as response:  # noqa: S310
            payload = json.load(response)
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"could not read {url}: {exc}") from exc
    releases = payload.get("releases")
    if not isinstance(releases, dict):
        raise RuntimeError(f"unexpected PyPI payload for {package!r}: no releases mapping")
    return set(releases)


def main(argv: list[str]) -> int:
    if argv:
        print("error: this check takes no arguments", file=sys.stderr)
        return 2
    pin = install.DISCOVERY_VERSION
    try:
        available = published_versions()
    except RuntimeError as exc:
        print(f"Discovery pin check INCONCLUSIVE: {exc}", file=sys.stderr)
        return 2
    if pin in available:
        print(f"Discovery pin check OK: pprose {pin} is published on PyPI")
        return 0
    newest = max(available, default="none")
    print("Discovery pin check FAILED:", file=sys.stderr)
    print(
        f"  - install.DISCOVERY_VERSION is {pin!r}, which is not published on PyPI "
        f"(newest published: {newest}).",
        file=sys.stderr,
    )
    print(
        f"  - Every committed skill under skills/ tells agents to run "
        f"`uvx pprose@{pin}`, which cannot resolve.",
        file=sys.stderr,
    )
    print(
        f"  - Fix by tagging and publishing v{pin}, or by lowering DISCOVERY_VERSION to "
        f"a published release and re-running `make generate`.",
        file=sys.stderr,
    )
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
