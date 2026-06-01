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
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from pprose import rubric_schema as rs
from pprose.eval_report import EvalReport
from pprose.render_html import inliner

_TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"

# Group ids -> Unicode glyphs used as the at-a-glance group icon in the
# card header. Light, theme-neutral; replace with proper SVG symbols when
# the design system ships them.
_GROUP_ICONS: dict[str, str] = {
    "purpose": "◎",
    "expression": "✦",
    "form": "▤",
    "reasoning": "⊕",
    "grounding": "⏚",
    "judgment": "⚖",
}

# Layout per Visual 9B: Purpose/Expression/Form on the left,
# Reasoning/Grounding/Judgment on the right. Reasoning at the top so its
# 4 dims pair row-for-row with Purpose's 4.
_LEFT_GROUPS = ("purpose", "expression", "form")
_RIGHT_GROUPS = ("reasoning", "grounding", "judgment")

_DEFAULT_SECTIONS = ("card", "detail", "metrics", "footer")


@dataclass(frozen=True)
class RenderOpts:
    page_size: str = "letter"
    sections: tuple[str, ...] = _DEFAULT_SECTIONS
    pprose_version: str = "dev"
    folder_mode: bool = False


@dataclass
class _DimRow:
    key: str
    label: str
    section: int
    group_key: str
    group_label: str
    score: int | str
    score_display: str
    fill_pct: int
    is_na: bool
    is_err: bool
    question: str
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
    # Imported here so importing the module doesn't require Jinja2 unless
    # the renderer is actually invoked.
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
        "pprose_version": opts.pprose_version,
        "sections": list(opts.sections),
        "report": report,
        "doc_name": report.artifact.label,
        "doc_meta": _doc_meta_string(report),
        "columns": columns,
        "overall_mean": _safe_overall_mean(report),
        "dimensions": dim_rows,
        "stats": _build_stats(report),
        "ratios": _build_ratios(report),
        "provenance": _build_provenance(report, opts),
    }
    return env.get_template("base.html.jinja").render(**context)


# Build helpers ------------------------------------------------------------


def _build_dim_rows(report: EvalReport) -> list[_DimRow]:
    rows: list[_DimRow] = []
    for d in rs.DIMENSIONS:
        score = _get_score(report, d.group_key, d.key)
        is_na = score == "NA"
        is_err = score == "ERR"
        fill = 0
        score_display: str
        if isinstance(score, int):
            fill = int(round(score / 5.0 * 100))
            score_display = str(score)
        elif is_err:
            score_display = "ERR"
        else:
            score_display = "—"

        reason = _get_reason(report, d.group_key, d.key)
        findings = _findings_for(report, d.label)

        rows.append(
            _DimRow(
                key=d.key,
                label=d.label,
                section=d.section,
                group_key=d.group_key,
                group_label=d.group_label,
                score=score,
                score_display=score_display,
                fill_pct=fill,
                is_na=is_na,
                is_err=is_err,
                question=d.question,
                reason=reason,
                findings=findings,
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
        "key": group_key[0],  # P/E/F/R/G/J for CSS var lookup (--accent-p, ...)
        "label": label,
        "icon": _GROUP_ICONS.get(group_key, "·"),
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
    out: list[dict[str, Any]] = []
    for f in report.rule_findings or []:
        if f.dimension != dim_label:
            continue
        loc_note = _summarize_locations(f.locations)
        note = f.description if not loc_note else f"{f.description} — {loc_note}"
        out.append(
            {
                "verdict": f.verdict,
                "rule_id": f"rule {f.rule_number}",
                "note": note,
            }
        )
    return out


def _summarize_locations(locations: list[Any]) -> str:
    parts: list[str] = []
    for loc in locations:
        if getattr(loc, "quote", None):
            parts.append(f'"{loc.quote.strip()}"')
        elif getattr(loc, "section", None):
            parts.append(str(loc.section))
        elif getattr(loc, "note", None):
            parts.append(str(loc.note))
    return "; ".join(parts)


def _safe_overall_mean(report: EvalReport) -> float | None:
    rollup = getattr(report.derived, "rubric_rollup", None)
    if rollup is None:
        return None
    return getattr(rollup, "overall_mean", None)


def _doc_meta_string(report: EvalReport) -> str:
    parts: list[str] = []
    try:
        parts.append(f"{report.quant.size.words / 1000:.1f}k words")
    except Exception:
        pass
    rubric_version = getattr(report.metadata, "rubric_version", None)
    if rubric_version:
        parts.append(str(rubric_version))
    return " · ".join(parts)


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
    push(
        "Sentences per paragraph",
        getattr(density, "sentences_per_paragraph", None),
    )
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
