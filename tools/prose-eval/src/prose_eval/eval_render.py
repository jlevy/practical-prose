"""
Single-doc rollup rendering: per-artifact Markdown produced from an EvalReport.

Lives in its own module so `eval_compare`, `eval_report`, and `eval_score` can
all import the renderer at module level without circular dependencies. The
output is reused as:

  - the body of each `.eval.md` file (frontmatter + body; body is regenerated
    whenever the frontmatter is updated),
  - the per-section content of `eval-compare --format by-doc`.

The frontmatter is canonical; this body is derived presentation.
"""

from __future__ import annotations

from typing import Any

from prose_eval import rubric_schema as rs

# Reports are typed `Any` here rather than `EvalReport` because eval_report
# imports this module at top level. Annotating with `EvalReport` (even under
# TYPE_CHECKING) trips basedpyright's `reportImportCycles` check, and the
# render functions duck-type the report shape — they only read `.artifact`,
# `.qual`, `.qual_reasons`, `.derived`, `.violations`, `.metadata`, `.quant`.
EvalReportLike = Any


# Formatting primitives shared with eval_compare's other renderers.


def fmt_int_comma(v: float | int) -> str:
    return f"{int(v):,}"


def fmt_int(v: float | int) -> str:
    return str(int(v))


def fmt_score(v: int | str) -> str:
    """Format a rubric score that may be the sentinel string "NA"."""
    if v == "NA":
        return "NA"
    return str(int(v))


def fmt_float_1(v: float) -> str:
    return f"{v:.1f}"


def fmt_float_2(v: float) -> str:
    return f"{v:.2f}"


# Per-doc quantitative breakdown.


def quant_rows_for(report: EvalReportLike) -> list[tuple[str, str, str]]:
    """Per-doc quant rows as (section, measure, value) tuples.

    Sections mirror eval_compare.render_section_drilldown's quant groupings
    (Size, Headings, Structural, Provenance, Links, Lint, Derived density / structure).
    """
    q = report.quant
    d = report.derived
    rows: list[tuple[str, str, str]] = []

    # Size
    rows += [
        ("Size", "Words", fmt_int_comma(q.size.words)),
        ("Size", "Sentences", fmt_int_comma(q.size.sentences)),
        ("Size", "Paragraphs", fmt_int_comma(q.size.paragraphs)),
        ("Size", "Lines", fmt_int_comma(q.size.lines)),
        ("Size", "Pages (275 wpp)", fmt_float_1(q.size.pages_275wpp)),
    ]
    if q.size.bytes_kb is not None:
        rows.append(("Size", "Bytes (KB)", fmt_float_1(q.size.bytes_kb)))

    # Headings (single row showing total with the h1..h4 breakdown).
    heads = q.headings
    rows.append(
        (
            "Headings",
            "Total (h1/h2/h3/h4)",
            f"{heads.total} ({heads.h1}/{heads.h2}/{heads.h3}/{heads.h4})",
        )
    )

    # Structural
    rows += [
        ("Structural", "Tables", fmt_int(q.structural.tables)),
        ("Structural", "Code blocks", fmt_int(q.structural.code_blocks)),
        ("Structural", "Images", fmt_int(q.structural.images)),
    ]

    # Links
    rows += [
        ("Links", "Total", fmt_int(q.links.total)),
        ("Links", "External", fmt_int(q.links.external)),
        ("Links", "Internal", fmt_int(q.links.internal)),
        ("Links", "Bare URLs", fmt_int(q.links.bare_urls)),
    ]

    # Provenance
    rows += [
        ("Provenance", "Bracket tags", fmt_int(q.provenance.bracket_tags)),
        ("Provenance", "Footnote refs", fmt_int(q.provenance.footnote_refs)),
        ("Provenance", "Footnote defs", fmt_int(q.provenance.footnote_defs)),
    ]

    # Lint
    rows.append(("Lint", "Banned-register hits", fmt_int(q.lint.banned_register_hits)))

    # Derived density
    dens = d.density
    rows += [
        ("Density", "Words / sentence", fmt_float_2(dens.words_per_sentence)),
        ("Density", "Words / paragraph", fmt_float_2(dens.words_per_paragraph)),
        ("Density", "Sentences / paragraph", fmt_float_2(dens.sentences_per_paragraph)),
        ("Density", "Links / 1k words", fmt_float_2(dens.links_per_1k_words)),
        ("Density", "Links / page", fmt_float_2(dens.links_per_page)),
        ("Density", "Tables / 1k words", fmt_float_2(dens.tables_per_1k_words)),
        ("Density", "Tables / page", fmt_float_2(dens.tables_per_page)),
        ("Density", "Tags / 1k words", fmt_float_2(dens.tags_per_1k_words)),
        ("Density", "Tags / page", fmt_float_2(dens.tags_per_page)),
    ]

    # Derived structure
    rows.append(
        (
            "Structure (derived)",
            "h4 share of headings",
            fmt_float_2(d.structure.h4_share_of_headings),
        )
    )

    return rows


# Per-doc rollup (the public renderer).


def render_single_doc_rollup(
    report: EvalReportLike,
    density_concerns: list[str] | None = None,
    heading_level: int = 2,
) -> str:
    """Render one doc's full evaluation as a self-contained Markdown section.

    `heading_level=1` is used by `.eval.md` bodies (one doc per file: # title,
    ## sections); `heading_level=2` is used by `by-doc.md` compilations (N
    docs per file: ## title, ### sections).

    Layout:
      <H_n>   <label>
      metadata line (scope, overall mean, model, eval date)
      <H_n+1> Qualitative (table: Group | Dimension | Score | Reason; with group means + overall mean)
      <H_n+1> Violations (numbered list with dimension, rule, description, location)
      <H_n+1> Quantitative (table: Section | Measure | Value)
      <H_n+1> Density concerns (bulleted, if any)
    """
    h_top = "#" * heading_level
    h_sub = "#" * (heading_level + 1)
    out: list[str] = []
    label = report.artifact.label
    overall = report.derived.rubric_rollup.overall_mean
    scope = report.artifact.scope_class or "—"
    meta = report.metadata
    model_str = meta.model_id or meta.model or "—"
    eval_date = meta.eval_date or "—"
    rubric_v = meta.rubric_version or "—"

    out.append(f"{h_top} {label}")
    out.append("")
    out.append(
        f"**Source:** `{report.artifact.path}`  "
        f"**Scope:** `{scope}`  "
        f"**Overall mean (18 dims):** {overall:.2f}  "
        f"**Rubric:** `{rubric_v}`  "
        f"**Model:** `{model_str}`  "
        f"**Eval date:** {eval_date}"
    )
    out.append("")

    # Qualitative table.
    out.append(f"{h_sub} Qualitative")
    out.append("")
    out.append("| Group | Dimension | Score | Reason |")
    out.append("| --- | --- | ---: | --- |")
    rollup = report.derived.rubric_rollup
    group_means: dict[str, float] = {
        "purpose": rollup.purpose_mean,
        "expression": rollup.expression_mean,
        "grounding": rollup.grounding_mean,
        "reasoning": rollup.reasoning_mean,
        "judgment": rollup.judgment_mean,
    }
    for group in rs.GROUPS:
        scores_obj = getattr(report.qual, group.key)
        reasons_obj = getattr(report.qual_reasons, group.key)
        for dim in group.dimensions:
            score = getattr(scores_obj, dim.key)
            reason = getattr(reasons_obj, dim.key) or ""
            # Markdown table cells can't contain raw newlines or unescaped pipes.
            reason_cell = reason.replace("|", "\\|").replace("\n", " ").strip()
            out.append(f"| {group.label} | {dim.label} | {fmt_score(score)} | {reason_cell} |")
        # Group mean row: 0.0 means "no scored dimensions" (all NA).
        mean = group_means[group.key]
        mean_cell = f"**{mean:.2f}**" if mean > 0 else "—"
        out.append(f"| **{group.label}** | **Mean** | {mean_cell} | |")
    out.append(f"| | **Overall mean (18 dims)** | **{overall:.2f}** | |")
    out.append("")

    # Violations.
    if report.violations:
        out.append(f"{h_sub} Violations")
        out.append("")
        for i, v in enumerate(report.violations, 1):
            loc = f" *Location:* {v.location}." if v.location else ""
            desc = v.description.replace("\n", " ").strip()
            out.append(f"{i}. **{v.dimension}** (rule {v.rule_number}) — {desc}{loc}")
        out.append("")

    # Quantitative table.
    out.append(f"{h_sub} Quantitative")
    out.append("")
    out.append("| Section | Measure | Value |")
    out.append("| --- | --- | ---: |")
    last_section = ""
    for section, measure, value in quant_rows_for(report):
        section_cell = section if section != last_section else ""
        out.append(f"| {section_cell} | {measure} | {value} |")
        last_section = section
    out.append("")

    # Density concerns.
    if density_concerns:
        out.append(f"{h_sub} Density concerns")
        out.append("")
        for c in density_concerns:
            out.append(f"- {c}")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def render_per_doc_rollup(
    reports: list[EvalReportLike],
    density_concerns: list[tuple[str, list[str]]] | None = None,
) -> str:
    """Render N docs as N consecutive self-contained sections (used by --format by-doc)."""
    concerns_by_label: dict[str, list[str]] = {}
    if density_concerns:
        concerns_by_label = {label: c for label, c in density_concerns}
    parts: list[str] = []
    for r in reports:
        parts.append(render_single_doc_rollup(r, concerns_by_label.get(r.artifact.label)))
    return "\n".join(parts)
