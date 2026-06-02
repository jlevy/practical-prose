"""Input-kind dispatch + JSON-payload construction for the static HTML render.

`render(path, opts)` detects the input kind from file extension and
frontmatter shape, then routes to the appropriate renderer. Phase 1
ships one kind: `eval_report`.

`render_eval_report(report, opts)` produces the final HTML string by
turning the EvalReport into the JSON payload the shared `bi-card` and
`tip-panels` JS components consume, then rendering the chosen variant
template (default `interactive`).

The Python side does no DOM building anymore — the card and the tip
panels are constructed client-side by the same JavaScript that lives in
the explorations workbench. The renderer's only job is data shaping and
template assembly.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pprose import rubric_schema as rs
from pprose.eval_report import EvalReport
from pprose.render_html import inliner

_RENDER_HTML_DIR = Path(__file__).resolve().parent
_TEMPLATES_DIR = _RENDER_HTML_DIR / "templates"
_VARIANTS_DIR = _TEMPLATES_DIR / "variants"

_DEFAULT_VARIANT = "interactive"


@dataclass(frozen=True)
class RenderOpts:
    page_size: str = "letter"
    variant: str = _DEFAULT_VARIANT
    pprose_version: str = "dev"
    folder_mode: bool = False


def available_variants() -> tuple[str, ...]:
    """List the variant template names available in templates/variants/."""
    if not _VARIANTS_DIR.is_dir():
        return ()
    return tuple(sorted(p.stem.removesuffix(".html") for p in _VARIANTS_DIR.glob("*.html.jinja")))


def detect_kind(path: Path) -> str | None:
    """Return the dispatch kind for `path`, or None if unrecognized.

    Phase 1:
      - `*.eval.md` → "eval_report"
      - `*.md` whose frontmatter validates as EvalReport → "eval_report"
      - anything else → None
    """
    name = path.name.lower()
    if name.endswith(".eval.md"):
        return "eval_report"
    if name.endswith(".md"):
        try:
            EvalReport.from_eval_md(path.read_text(encoding="utf-8"))
        except Exception:
            return None
        return "eval_report"
    return None


def render(path: Path, opts: RenderOpts) -> str:
    """Detect the input kind and dispatch to the matching renderer."""
    kind = detect_kind(path)
    if kind is None:
        supported = ", ".join(sorted(_DISPATCH))
        raise ValueError(f"unsupported input: {path.name} — supported kinds: {supported}")
    return _DISPATCH[kind](path, opts)


def _render_eval_report_from_path(path: Path, opts: RenderOpts) -> str:
    report = EvalReport.from_eval_md(path.read_text(encoding="utf-8"))
    return render_eval_report(report, opts)


def render_eval_report(report: EvalReport, opts: RenderOpts) -> str:
    """Render an EvalReport to a complete HTML string via the chosen variant."""
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    variant = opts.variant or _DEFAULT_VARIANT
    variant_path = _VARIANTS_DIR / f"{variant}.html.jinja"
    if not variant_path.is_file():
        available = ", ".join(available_variants()) or "(none)"
        raise ValueError(f"unknown variant {variant!r}; available: {available}")

    env = Environment(
        loader=FileSystemLoader([str(_VARIANTS_DIR), str(_TEMPLATES_DIR)]),
        autoescape=select_autoescape(["html", "jinja"]),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )

    payload = build_payload(report)

    context: dict[str, Any] = {
        "title": f"Eval — {report.artifact.label}",
        "css": inliner.bundled_css(opts.page_size),
        "js": inliner.bundled_js(),
        "icons_svg": inliner.bundled_icons_svg(),
        "pprose_version": opts.pprose_version,
        "variant": variant,
        # The data payload as a JSON string the template embeds inside a
        # <script type="application/json"> tag for the bootstrap to parse.
        "data_json": json.dumps(payload, ensure_ascii=False, separators=(",", ":")),
    }
    return env.get_template(f"{variant}.html.jinja").render(**context)


# ─── Payload construction ──────────────────────────────────────────────────


def build_payload(report: EvalReport) -> dict[str, Any]:
    """Build the JSON payload the shared bi-card + tip-panels JS consume.

    Shape (mirrors the data contract documented in
    tools/render-components/bi-card/README.md):

        {
          "groups":     [{ "id": "P", "label": "Purpose" }, ...],
          "dimensions": [{ "id": "P1", "label": "Suitability", "g": "P" }, ...],
          "rubric":     { "P1": { "question": "...", "rules": [...], "group": "Purpose" }, ... },
          "doc": {
            "id":       "<artifact-label>",
            "name":     "<artifact-label>",
            "scores":   { "P1": 4, ... },
            "reasons":  { "P1": "...", ... },
            "findings": { "P1": [{ rule_number, verdict, description }, ...], ... }
          }
        }
    """
    # Build per-group, per-dim id maps (P, E, F, R, G, J  and  P1..J3).
    groups_payload: list[dict[str, str]] = []
    dims_payload: list[dict[str, str]] = []
    rubric_payload: dict[str, dict[str, Any]] = {}

    for group in rs.GROUPS:
        group_id = group.key[0].upper()  # 'P', 'E', 'F', 'R', 'G', 'J'
        groups_payload.append({"id": group_id, "label": group.label})
        for index, dim in enumerate(group.dimensions, start=1):
            dim_id = f"{group_id}{index}"
            dims_payload.append({"id": dim_id, "label": dim.label, "g": group_id})
            rubric_payload[dim_id] = {
                "label": dim.label,
                "group": group.label,
                "question": dim.question,
                "rules": list(dim.rules),
            }

    # Build the per-doc scores / reasons / findings, keyed by dim id.
    doc_id = report.artifact.label
    scores: dict[str, int | str] = {}
    reasons: dict[str, str] = {}
    findings_by_dim: dict[str, list[dict[str, Any]]] = {}

    for group in rs.GROUPS:
        group_id = group.key[0].upper()
        scores_group = getattr(report.qual, group.key)
        reasons_group = getattr(report.qual_reasons, group.key, None)
        for index, dim in enumerate(group.dimensions, start=1):
            dim_id = f"{group_id}{index}"
            scores[dim_id] = getattr(scores_group, dim.key)
            if reasons_group is not None:
                reason = getattr(reasons_group, dim.key, None)
                if reason:
                    reasons[dim_id] = reason

    # Find each rule_finding's dim id by dimension label.
    label_to_dim_id = {d["label"]: d["id"] for d in dims_payload}
    for f in report.rule_findings or []:
        dim_id = label_to_dim_id.get(f.dimension)
        if not dim_id:
            continue
        findings_by_dim.setdefault(dim_id, []).append(
            {
                "rule_number": f.rule_number,
                "verdict": f.verdict or "noted",
                "description": f.description,
            }
        )

    return {
        "groups": groups_payload,
        "dimensions": dims_payload,
        "rubric": rubric_payload,
        "doc": {
            "id": doc_id,
            "name": doc_id,
            "scores": scores,
            "reasons": reasons,
            "findings": findings_by_dim,
        },
    }


# Dispatch table ---------------------------------------------------------

_DISPATCH = {
    "eval_report": _render_eval_report_from_path,
}
