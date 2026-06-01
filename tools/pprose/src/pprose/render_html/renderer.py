"""Input-kind dispatch + HTML rendering of an EvalReport.

`render(path, opts)` detects the input kind from the file extension and
frontmatter shape, then routes to the appropriate renderer. Phase 1
ships one entry: `eval_report`. Adding a new kind (a plain Markdown
document, an advanced eval profile that embeds the source body) is a
new entry in `_DISPATCH` and a new render function; the CLI stays the
same.

`render_eval_report(report, opts)` is the public entrypoint when the
caller already has an EvalReport in memory (used by
`pprose score --render-html` to skip the disk-read round trip).

The card DOM is a verbatim port of `biCard()` + `biDim9B()` from
tools/explorations/visual-design/dimension-visualizations.html, driven
by EvalReport data. Only differences from the source mockup:
  - Hover-driven tip panels removed (their content moves to the
    per-dim detail page).
  - The `repoCredit()` footer below the card is omitted.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pprose import rubric_schema as rs
from pprose.eval_report import EvalReport
from pprose.render_html import inliner

_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

# Layout per Visual 9B: Purpose/Expression/Form on the left,
# Reasoning/Grounding/Judgment on the right. Reasoning at the top so its
# 4 dims pair row-for-row with Purpose's 4.
_LEFT_GROUPS = ("purpose", "expression", "form")
_RIGHT_GROUPS = ("reasoning", "grounding", "judgment")

_DEFAULT_SECTIONS = ("card", "detail", "metrics", "footer")

# Per the explorations file, the alpha-step default is 0.0 (segments and
# the score chip all render at full vividness). The design system can dial
# this via a CSS slider in the playground, but the static surface uses the
# documented default.
_SCORE_ALPHA_STEP = 0.0


@dataclass(frozen=True)
class RenderOpts:
    page_size: str = "letter"
    sections: tuple[str, ...] = _DEFAULT_SECTIONS
    pprose_version: str = "dev"
    folder_mode: bool = False


@dataclass
class _Segment:
    idx: int
    background: str
    offset_pct: int


@dataclass
class _DimRow:
    id: str  # P1..J3 — design-system dim id used in CSS var lookups
    key: str  # snake_case key in the EvalReport schema (e.g., "suitability")
    label: str
    section: int
    group_key: str
    group_label: str
    score: int | str
    score_display: str
    is_na: bool
    is_err: bool
    segments: list[_Segment]
    fill_bg: str | None
    circle_bg: str | None
    tick_positions: tuple[int, ...]
    question: str
    rules: tuple[str, ...]
    reason: str | None
    findings: list[dict[str, Any]] = field(default_factory=list)


def detect_kind(path: Path) -> str | None:
    """Return the dispatch kind for `path`, or None if unrecognized.

    Detection rules (Phase 1):
      - `*.eval.md`  -> "eval_report"
      - `*.md` whose YAML frontmatter validates as EvalReport -> "eval_report"
      - anything else -> None (renderer raises with a clear list of kinds)
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
    """Render an EvalReport to a complete HTML string."""
    from jinja2 import Environment, FileSystemLoader, select_autoescape

    env = Environment(
        loader=FileSystemLoader(str(_TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "jinja"]),
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )

    dim_rows = _build_dim_rows(report)
    rows_by_group = _group_rows(dim_rows)
    columns = [
        {
            "side": "left",
            "groups": [_group_payload(g, rows_by_group) for g in _LEFT_GROUPS],
        },
        {
            "side": "right",
            "groups": [_group_payload(g, rows_by_group) for g in _RIGHT_GROUPS],
        },
    ]

    context: dict[str, Any] = {
        "title": f"Eval — {report.artifact.label}",
        "css": inliner.bundled_css(opts.page_size),
        "icons_svg": inliner.bundled_icons_svg(),
        "pprose_version": opts.pprose_version,
        "sections": list(opts.sections),
        "report": report,
        "doc_name": report.artifact.label,
        "columns": columns,
        "dimensions": dim_rows,
        "stats": _build_stats(report),
        "ratios": _build_ratios(report),
        "provenance": _build_provenance(report, opts),
    }
    return env.get_template("base.html.jinja").render(**context)


# ─── Card data shaping ─────────────────────────────────────────────────────


def _segment_alpha(seg_idx: int) -> float:
    """Mirror segmentAlpha(i) in the explorations file."""
    return 1.0 - (5 - seg_idx) * _SCORE_ALPHA_STEP


def _dim_color_mix(dim_id: str, alpha: float) -> str:
    """Mirror dimColorMix(dimId, alpha) in the explorations file."""
    a = max(0.0, min(1.0, alpha))
    pct = round(a * 100)
    return f"color-mix(in srgb, var(--dim-{dim_id}) {pct}%, transparent)"


def _score_color(dim_id: str, score: int) -> str:
    """Mirror scoreColor(dimId, score)."""
    return _dim_color_mix(dim_id, 1.0 - (5 - score) * _SCORE_ALPHA_STEP)


def _dim_design_id(dim: rs.Dimension, index_in_group: int) -> str:
    """Map a rubric Dimension to the design-system id (P1..J3).

    The design system uses single-letter group code + 1-indexed position
    within the group, exactly as the per-dim CSS tokens are named
    (--dim-P1, --dim-P2, …).
    """
    return f"{dim.group_key[0].upper()}{index_in_group}"


def _build_dim_rows(report: EvalReport) -> list[_DimRow]:
    rows: list[_DimRow] = []
    # Walk groups in canonical order so the within-group index is stable
    # (matches the design-system's P1..P4, E1..E3, … numbering).
    for group in rs.GROUPS:
        for idx, dim in enumerate(group.dimensions, start=1):
            dim_id = _dim_design_id(dim, idx)
            score = _get_score(report, dim.group_key, dim.key)
            is_na = (not isinstance(score, int)) and score != "ERR"
            is_err = score == "ERR"

            segments: list[_Segment] = []
            fill_bg: str | None = None
            circle_bg: str | None = None
            score_display: str

            if isinstance(score, int):
                score_display = str(score)
                circle_bg = _score_color(dim_id, score)
                for i in range(1, score + 1):
                    segments.append(
                        _Segment(
                            idx=i,
                            background=_dim_color_mix(dim_id, _segment_alpha(i)),
                            offset_pct=(i - 1) * 20,
                        )
                    )
            elif is_err:
                score_display = "ERR"
                fill_bg = "var(--score-err-fill)"
            else:
                score_display = "NA"
                fill_bg = "var(--score-na-fill)"

            rows.append(
                _DimRow(
                    id=dim_id,
                    key=dim.key,
                    label=dim.label,
                    section=dim.section,
                    group_key=dim.group_key,
                    group_label=dim.group_label,
                    score=score,
                    score_display=score_display,
                    is_na=is_na,
                    is_err=is_err,
                    segments=segments,
                    fill_bg=fill_bg,
                    circle_bg=circle_bg,
                    # Tick marks at score positions 1/2/3/4. The .bi-ltr
                    # left-column track is mirrored via CSS transform, so
                    # symmetric tick positions render correctly in both
                    # columns.
                    tick_positions=(20, 40, 60, 80),
                    question=dim.question,
                    rules=dim.rules,
                    reason=_get_reason(report, dim.group_key, dim.key),
                    findings=_findings_for(report, dim.label),
                )
            )
    return rows


def _group_rows(rows: list[_DimRow]) -> dict[str, list[_DimRow]]:
    out: dict[str, list[_DimRow]] = {}
    for r in rows:
        out.setdefault(r.group_key, []).append(r)
    return out


def _group_payload(group_key: str, rows_by_group: dict[str, list[_DimRow]]) -> dict[str, Any]:
    dims = rows_by_group.get(group_key, [])
    numeric = [d.score for d in dims if isinstance(d.score, int)]
    avg = sum(numeric) / len(numeric) if numeric else None
    label = dims[0].group_label if dims else group_key.title()
    return {
        "key": group_key,
        "key_lower": group_key[0].lower(),  # p/e/f/r/g/j for --accent-* CSS vars
        "label": label,
        "label_lower": label.lower(),  # for #icon-<label> sprite reference
        "avg": avg,
        "dims": dims,
    }


def _get_score(report: EvalReport, group_key: str, dim_key: str) -> int | str:
    group = getattr(report.qual, group_key)
    return getattr(group, dim_key)


def _get_reason(report: EvalReport, group_key: str, dim_key: str) -> str | None:
    group = getattr(report.qual_reasons, group_key, None)
    if group is None:
        return None
    return getattr(group, dim_key, None)


def _findings_for(report: EvalReport, dim_label: str) -> list[dict[str, Any]]:
    """Per-dim rule findings, shaped to match the tip-panel `renderDim` output.

    Mirrors the markdown the explorations file emits per finding:
      `**Rule N · verdict** — description`
    so the template can render the same `<li><strong>…</strong> — …</li>` shape
    without extra formatting logic.
    """
    out: list[dict[str, Any]] = []
    for f in report.rule_findings or []:
        if f.dimension != dim_label:
            continue
        out.append(
            {
                "rule_number": f.rule_number,
                "verdict": f.verdict or "noted",
                "description": f.description,
            }
        )
    return out


# ─── Supplemental section data ─────────────────────────────────────────────


def _build_stats(report: EvalReport) -> list[dict[str, str]]:
    size = report.quant.size
    headings = report.quant.headings
    return [
        {"label": "Words", "value": f"{size.words:,}"},
        {"label": "Sentences", "value": f"{size.sentences:,}"},
        {"label": "Paragraphs", "value": f"{size.paragraphs:,}"},
        {"label": "Pages (~275 wpp)", "value": f"{size.pages_275wpp:.1f}"},
        {"label": "Headings", "value": f"{headings.total:,}"},
    ]


def _build_ratios(report: EvalReport) -> list[dict[str, str]]:
    derived = report.derived
    density = getattr(derived, "density", None)
    if density is None:
        return []
    out: list[dict[str, str]] = []

    def push(label: str, value: float | None, fmt: str = "{:.2f}") -> None:
        if value is None:
            return
        out.append({"label": label, "value": fmt.format(value)})

    push("Words per sentence", getattr(density, "words_per_sentence", None))
    push("Words per paragraph", getattr(density, "words_per_paragraph", None))
    push("Sentences per paragraph", getattr(density, "sentences_per_paragraph", None))
    push("Links per 1k words", getattr(density, "links_per_1k_words", None))
    push("Tables per 1k words", getattr(density, "tables_per_1k_words", None))
    push("Tags per 1k words", getattr(density, "tags_per_1k_words", None))
    return out


def _build_provenance(report: EvalReport, opts: RenderOpts) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    meta = report.metadata
    if meta.eval_date:
        rows.append({"label": "Eval date", "value": str(meta.eval_date)})
    if meta.evaluator:
        rows.append({"label": "Evaluator", "value": str(meta.evaluator)})
    if meta.method:
        rows.append({"label": "Method", "value": str(meta.method)})
    if meta.model:
        rows.append({"label": "Model", "value": str(meta.model)})
    if meta.rubric_version:
        rows.append({"label": "Rubric version", "value": str(meta.rubric_version)})
    artifact = report.artifact
    if artifact.path:
        rows.append({"label": "Source", "value": str(artifact.path)})
    if artifact.commit_sha:
        rows.append({"label": "Commit", "value": str(artifact.commit_sha)})
    rows.append({"label": "pprose version", "value": opts.pprose_version})
    return rows


# Dispatch table -----------------------------------------------------------

_DISPATCH = {
    "eval_report": _render_eval_report_from_path,
}
