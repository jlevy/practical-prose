"""The bundled resources must match the canonical repo docs (run sync if this fails)."""

from __future__ import annotations

from devtools import sync_resources


def test_bundled_resources_match_canonical():
    drift = sync_resources.check()
    assert not drift, (
        "bundled resources are out of sync with the canonical repo docs; "
        "run `uv run python devtools/sync_resources.py`:\n  " + "\n  ".join(drift)
    )
