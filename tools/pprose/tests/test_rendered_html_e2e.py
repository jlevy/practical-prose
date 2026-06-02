"""End-to-end smoke checks on the rendered HTML output.

Renders a fixture via the production pipeline, then exercises the output
beyond static structural assertions:

  - The inlined JavaScript bundle parses cleanly under Node.js (no syntax
    errors). This catches drift in card.js / tip-panels.js / theme-toggle.js
    that would silently break the rendered page.
  - The inlined eval-data payload is valid JSON and round-trips.

Skips gracefully if `node` is not on PATH (e.g. CI envs that don't install
node). The Python-side static checks in `test_render_html.py` still run.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest

from pprose.eval_report import EvalReport
from pprose.render_html.renderer import RenderOpts, render_eval_report

FIXTURES = Path(__file__).resolve().parent / "fixtures"


def _render() -> str:
    report = EvalReport.from_eval_md(FIXTURES / "rev2-net.eval.md")
    return render_eval_report(report, RenderOpts(pprose_version="test"))


def _extract_inline_js_bundle(html: str) -> str:
    """The bundled JS lives inside the first <script>…</script> of the <head>."""
    m = re.search(r"<head>(.*?)</head>", html, re.DOTALL | re.IGNORECASE)
    assert m, "no <head> in rendered HTML"
    head = m.group(1)
    m2 = re.search(r"<script>(.*?)</script>", head, re.DOTALL)
    assert m2, "no inline <script> bundle in <head>"
    return m2.group(1)


def _extract_data_payload(html: str) -> dict:
    m = re.search(
        r'<script type="application/json" id="pp-eval-data">(.*?)</script>',
        html,
        re.DOTALL,
    )
    assert m, "no pp-eval-data block"
    return json.loads(m.group(1))


def test_inlined_js_bundle_parses_under_node() -> None:
    """The bundled component JS is valid JavaScript.

    Uses `node --check` which parses (but does not execute) the file. This
    catches malformed escapes, runaway template literals, premature EOF,
    and similar drift that the static Python tests would miss.
    """
    node = shutil.which("node")
    if not node:
        pytest.skip("node not on PATH; skipping syntax check")

    bundle = _extract_inline_js_bundle(_render())
    # node --check requires a file path; write to a temp file via tmp_path
    # wouldn't quite work without a fixture, so use stdin via -e if possible.
    # `node --check -` reads stdin and exits non-zero on a syntax error.
    result = subprocess.run(
        [node, "--check", "-"],
        input=bundle,
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, f"rendered JS bundle failed `node --check`:\n{result.stderr}"


def test_inlined_payload_round_trips_through_json() -> None:
    payload = _extract_data_payload(_render())
    # Re-serialize and parse to confirm well-formed.
    redumped = json.dumps(payload)
    reparsed = json.loads(redumped)
    assert reparsed == payload


def test_payload_doc_id_matches_artifact_label() -> None:
    report = EvalReport.from_eval_md(FIXTURES / "rev2-net.eval.md")
    html = render_eval_report(report, RenderOpts(pprose_version="test"))
    payload = _extract_data_payload(html)
    assert payload["doc"]["id"] == report.artifact.label
    assert payload["doc"]["name"] == report.artifact.label
