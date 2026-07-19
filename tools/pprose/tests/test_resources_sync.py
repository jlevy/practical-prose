"""The bundled resources must match the canonical repo docs (run sync if this fails)."""

from __future__ import annotations

import re

from devtools import sync_resources


def test_bundled_resources_match_canonical():
    drift = sync_resources.check()
    assert not drift, (
        "bundled resources are out of sync with the canonical repo docs; "
        "run `make generate` from the repository root:\n  " + "\n  ".join(drift)
    )


def test_discovery_plan_composes_guidelines_from_synced_plan_not_disk():
    """A single sync pass must be the fixed point when docs/ change.

    Regression: composing bundled references from the on-disk wheel resources made
    `make generate` need two runs to converge after a docs/ edit (the first run wrote
    a stale guideline into skills/<name>/references/).
    """
    synced = sync_resources._synced_plan()
    key = sync_resources.RESOURCES / "guidelines" / "ai-prose-corrections.md"
    marker = "Sentinel sentence proving composition reads the synced plan."
    synced[key] = synced[key].rstrip() + "\n\n" + marker + "\n"
    plan = sync_resources._discovery_plan(synced)
    ref = (
        sync_resources.REPO_ROOT
        / "skills"
        / "pprose-de-slop"
        / "references"
        / "ai-prose-corrections.md"
    )
    assert marker in plan[ref]


def test_link_rewrite_bundled_targets_become_pprose_commands():
    src = sync_resources.REPO_ROOT / "shortcuts" / "example.md"
    text = (
        "See [practical-prose-rubric.md](../docs/practical-prose-rubric.md) and "
        "[the single-doc runbook](../runbooks/practical-prose-eval-single.runbook.md)."
    )
    out = sync_resources._rewrite_links(text, src)
    # Filename label → the command replaces the whole link; prose label is kept.
    assert "`pprose guidelines practical-prose-rubric`" in out
    assert "the single-doc runbook (`pprose runbook practical-prose-eval-single`)" in out


def test_link_rewrite_bundled_category_directory_becomes_bare_listing_command():
    src = sync_resources.REPO_ROOT / "README.md"
    out = sync_resources._rewrite_links(
        "See the [runbooks](runbooks/) and [guidelines](docs/).",
        src,
    )
    assert out == "See the `pprose runbook` and `pprose guidelines`."
    assert "--list" not in out


def test_link_rewrite_unbundled_targets_become_github_urls():
    src = sync_resources.REPO_ROOT / "runbooks" / "example.runbook.md"
    out = sync_resources._rewrite_links(
        "See [fixtures](../tools/pprose/tests/fixtures/) and "
        "[the dev note](../docs/project/eval-screenshots.runbook.md).",
        src,
    )
    assert f"[fixtures]({sync_resources.GITHUB_TREE}/tools/pprose/tests/fixtures)" in out
    assert (
        f"[the dev note]({sync_resources.GITHUB_BLOB}/docs/project/eval-screenshots.runbook.md)"
        in out
    )


def test_link_rewrite_leaves_urls_and_anchors_alone():
    src = sync_resources.REPO_ROOT / "docs" / "example.md"
    text = "[uv](https://docs.astral.sh/uv/) and [skills](#agent-skills)."
    assert sync_resources._rewrite_links(text, src) == text


def test_no_relative_links_remain_in_bundled_resources():
    link_re = re.compile(r"\]\(([^)\s]+)\)")
    for dest, content in sync_resources._synced_plan().items():
        for target in link_re.findall(content):
            assert target.startswith(("http://", "https://", "#")), (
                f"unrewritten link target {target!r} in {dest.name}; the link's "
                "target may not exist in the repo (fix the source doc)"
            )
