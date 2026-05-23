"""
Comparison-table generator for practical-writing eval reports.

Reads N validated EvalReport YAMLs (see `pprose report`) and emits a
unified Markdown comparison table, with optional per-section drilldowns.

Output shape (unified mode):
  - Columns: one per input artifact (labels from each YAML's `artifact.label`).
  - Rows are grouped by rubric category (Purpose, Expression, Grounding, Reasoning,
    Judgment) and follow rubric-schema dimension order. Each category section runs
    one row per qualitative dimension, then a "Mean" row, then the analogous
    quantitative rows (raw counts and density ratios).
  - Trailing rows: overall qualitative mean, overall density rollups, schema /
    metadata summary, and a derived-deltas block for per-pair score differences.
  - Cell values are bolded against a configurable rule (`--bold-rule`) to surface
    materially different scores between columns.

The shape is exercised by the renderer regression test in
scripts/test_eval_compare.py, which renders the six `figma-*.eval.md` fixtures
and asserts byte-for-byte equality with `scripts/fixtures/expected-comparison.md`.

Usage:
  pprose compare a.eval.md b.eval.md [c.eval.md ...]
  pprose compare --format unified a.yaml b.yaml > unified.md
  pprose compare --format sections a.yaml b.yaml > sections.md
  pprose compare --format unified --table-styles a.yaml b.yaml > styled.md
  pprose compare --bold-rule materially-different a.yaml b.yaml
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from pprose import rubric_schema as rs
from pprose.eval_render import (
    fmt_float_1,
    fmt_float_2,
    fmt_int,
    fmt_int_comma,
    fmt_score,
    render_per_doc_rollup,
)
from pprose.eval_report import EvalReport
from pprose.table_styles import render_table_style_frontmatter

BoldRule = Literal["max", "min", "none"]
BoldMode = Literal["max", "materially-different"]

QUALITATIVE_SCORE_NOTE = (
    "**Score notes:** Qualitative rows use the rubric's 0-5 scale. `NA` means the "
    "dimension is not applicable and is excluded from group and overall means. Bold "
    "numeric cells mark the best value in that row under the selected bolding rule."
)


@dataclass
class Row:
    approach: str
    aspect: str
    measure: str
    # Rubric-score cells use the sentinel string "NA"; other cells are numeric.
    raw_values: list[float | int | str | None]
    display_values: list[str]
    bold_rule: BoldRule = "max"


def _qual_rows(reports: list[EvalReport]) -> list[Row]:
    rows: list[Row] = []
    for group in rs.GROUPS:
        for dim in group.dimensions:
            vals = [getattr(getattr(r.qual, group.key), dim.key) for r in reports]
            rows.append(
                Row(
                    "Qualitative",
                    group.label,
                    dim.label,
                    vals,
                    [fmt_score(v) for v in vals],
                )
            )
        mean_attr = f"{group.key}_mean"
        means: list[float | None] = []
        for report in reports:
            group_obj = getattr(report.qual, group.key)
            vals = [getattr(group_obj, d.key) for d in group.dimensions]
            if all(v == "NA" for v in vals):
                means.append(None)
            else:
                means.append(getattr(report.derived.rubric_rollup, mean_attr))
        rows.append(
            Row(
                "Qualitative",
                group.label,
                "*Mean*",
                means,
                [fmt_float_2(v) if v is not None else "—" for v in means],
            )
        )

    overall_means = [r.derived.rubric_rollup.overall_mean for r in reports]
    rows.append(
        Row(
            "Qualitative",
            "Overall",
            f"*Mean ({rs.dimension_count()} dims)*",
            overall_means,
            [fmt_float_2(v) for v in overall_means],
        )
    )

    return rows


def _quant_rows(reports: list[EvalReport]) -> list[Row]:
    rows: list[Row] = []

    # Size / heading / structural / link-count metrics are descriptive: more is not
    # automatically better. Use bold_rule="none" so the reader doesn't read row-maxima
    # as wins.
    size_metrics = [
        ("Words", lambda r: r.quant.size.words, fmt_int_comma),
        ("Sentences", lambda r: r.quant.size.sentences, fmt_int_comma),
        ("Paragraphs", lambda r: r.quant.size.paragraphs, fmt_int_comma),
        ("Lines", lambda r: r.quant.size.lines, fmt_int_comma),
        ("Pages (275 wpp)", lambda r: r.quant.size.pages_275wpp, fmt_float_1),
    ]
    for name, getter, fmt in size_metrics:
        vals = [getter(r) for r in reports]
        rows.append(
            Row(
                "Quantitative",
                "Size",
                name,
                vals,
                [fmt(v) for v in vals],
                bold_rule="none",
            )
        )
    if any(r.quant.size.bytes_kb is not None for r in reports):
        vals_bytes: list[float | int | None] = [r.quant.size.bytes_kb for r in reports]
        rows.append(
            Row(
                "Quantitative",
                "Size",
                "Bytes (KB)",
                vals_bytes,
                [fmt_float_1(v) if v is not None else "n/a" for v in vals_bytes],
                bold_rule="none",
            )
        )

    head_vals = [r.quant.headings.total for r in reports]
    head_disp = [
        f"{r.quant.headings.total} ({r.quant.headings.h1}/{r.quant.headings.h2}/"
        f"{r.quant.headings.h3}/{r.quant.headings.h4})"
        for r in reports
    ]
    rows.append(
        Row(
            "Quantitative",
            "Headings",
            "Total (h1/h2/h3/h4)",
            head_vals,
            head_disp,
            bold_rule="none",
        )
    )

    structural_metrics = [
        ("Tables", lambda r: r.quant.structural.tables),
        ("Code blocks", lambda r: r.quant.structural.code_blocks),
        ("Images", lambda r: r.quant.structural.images),
    ]
    for name, getter in structural_metrics:
        vals_s = [getter(r) for r in reports]
        rows.append(
            Row(
                "Quantitative",
                "Structural",
                name,
                vals_s,
                [fmt_int(v) for v in vals_s],
                bold_rule="none",
            )
        )

    links_total = [r.quant.links.total for r in reports]
    links_disp = [
        f"{r.quant.links.total} ({r.quant.links.external}/{r.quant.links.internal})"
        for r in reports
    ]
    rows.append(
        Row(
            "Quantitative",
            "Links",
            "Total (external/internal)",
            links_total,
            links_disp,
            bold_rule="none",
        )
    )
    form_disp = [
        f"{r.quant.links.inline}/{r.quant.links.reference}/{r.quant.links.autolink}"
        for r in reports
    ]
    rows.append(
        Row(
            "Quantitative",
            "Links",
            "Form (inline/reference/autolink)",
            links_total,
            form_disp,
            bold_rule="none",
        )
    )
    bare_vals = [r.quant.links.bare_urls for r in reports]
    rows.append(
        Row(
            "Quantitative",
            "Links",
            "Bare URLs",
            bare_vals,
            [fmt_int(v) for v in bare_vals],
            bold_rule="min",
        )
    )

    tag_vals = [r.quant.provenance.bracket_tags for r in reports]
    rows.append(
        Row(
            "Quantitative",
            "Provenance",
            "Bracket tags",
            tag_vals,
            [fmt_int(v) for v in tag_vals],
            bold_rule="none",
        )
    )
    fn_disp = [
        f"{r.quant.provenance.footnote_refs}/{r.quant.provenance.footnote_defs}" for r in reports
    ]
    rows.append(
        Row(
            "Quantitative",
            "Provenance",
            "Footnotes (refs/defs)",
            [r.quant.provenance.footnote_refs for r in reports],
            fn_disp,
            bold_rule="none",
        )
    )

    lint_vals = [r.quant.lint.banned_register_hits for r in reports]
    rows.append(
        Row(
            "Quantitative",
            "Lint",
            "Banned-register hits",
            lint_vals,
            [fmt_int(v) for v in lint_vals],
            bold_rule="min",
        )
    )

    return rows


def _derived_rows(reports: list[EvalReport]) -> list[Row]:
    rows: list[Row] = []

    # Density and heading-shape ratios are descriptive: more is not automatically
    # better. Use bold_rule="none" so the reader doesn't read row-maxima as wins.
    density_metrics = [
        ("Words / sentence", lambda r: r.derived.density.words_per_sentence),
        ("Words / paragraph", lambda r: r.derived.density.words_per_paragraph),
        ("Sentences / paragraph", lambda r: r.derived.density.sentences_per_paragraph),
        ("Tables / 1k words", lambda r: r.derived.density.tables_per_1k_words),
        ("Tables / page", lambda r: r.derived.density.tables_per_page),
        ("Tags / 1k words", lambda r: r.derived.density.tags_per_1k_words),
        ("Tags / page", lambda r: r.derived.density.tags_per_page),
        ("Links / 1k words", lambda r: r.derived.density.links_per_1k_words),
        ("Links / page", lambda r: r.derived.density.links_per_page),
    ]
    for name, getter in density_metrics:
        vals = [getter(r) for r in reports]
        rows.append(
            Row(
                "Derived",
                "Density",
                name,
                vals,
                [fmt_float_2(v) for v in vals],
                bold_rule="none",
            )
        )

    h4_vals = [r.derived.structure.h4_share_of_headings for r in reports]
    rows.append(
        Row(
            "Derived",
            "Heading shape",
            "H4 share of headings",
            h4_vals,
            [fmt_float_2(v) for v in h4_vals],
            bold_rule="none",
        )
    )

    tally_present = any(r.derived.tally is not None for r in reports)
    if tally_present:
        tally_disp = [r.derived.tally.compact() if r.derived.tally else "n/a" for r in reports]
        rows.append(
            Row(
                "Derived",
                "Tally",
                "Bull / bear / neutral",
                [None] * len(reports),
                tally_disp,
                bold_rule="none",
            )
        )

    return rows


def _bold_indices(
    raw: list[float | int | str | None],
    rule: BoldRule,
    mode: BoldMode,
) -> set[int]:
    """Return indices whose raw_values should be bolded."""
    if rule == "none":
        return set()

    # Treat both None and "NA" as missing for bolding purposes — there is no
    # numeric comparison to make for a not-applicable dimension.
    valid = [(i, v) for i, v in enumerate(raw) if v is not None and v != "NA"]
    if not valid:
        return set()
    values = [v for _, v in valid]
    if max(values) == min(values):
        return set()

    if rule == "max":
        target = max(values)
    else:  # min
        target = min(values)

    if mode == "max":
        return {i for i, v in valid if v == target}

    # materially-different: target must be >= 1 above (or below for min) the median
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    median = sorted_vals[n // 2] if n % 2 else (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2
    if rule == "max":
        if target - median < 1:
            return set()
    else:
        if median - target < 1:
            return set()
    return {i for i, v in valid if v == target}


def _render_row(
    row: Row,
    bold_set: set[int],
    coalesce: tuple[str, str],
) -> str:
    cells = []
    new_approach = "" if row.approach == coalesce[0] else f"**{row.approach}**"
    new_aspect = "" if row.aspect == coalesce[1] else row.aspect
    cells.append(new_approach)
    cells.append(new_aspect)
    cells.append(row.measure)
    for i, disp in enumerate(row.display_values):
        if i in bold_set and disp not in {"n/a", "—"}:
            disp = f"**{disp}**"
        cells.append(disp)
    return "| " + " | ".join(cells) + " |"


def render_unified_table(
    reports: list[EvalReport],
    bold_mode: BoldMode = "max",
) -> str:
    rows = _qual_rows(reports) + _quant_rows(reports) + _derived_rows(reports)
    labels = [r.artifact.label for r in reports]

    header = "| Approach | Aspect | Measure | " + " | ".join(labels) + " |"
    separator = "| --- | --- | --- |" + (" ---: |" * len(labels))

    out = [header, separator]
    last_approach = ""
    last_aspect = ""
    for row in rows:
        bold_set = _bold_indices(row.raw_values, row.bold_rule, bold_mode)
        out.append(_render_row(row, bold_set, (last_approach, last_aspect)))
        last_approach = row.approach
        last_aspect = row.aspect

    return "\n".join(out)


def render_section_drilldown(
    reports: list[EvalReport],
    bold_mode: BoldMode = "max",
) -> str:
    """Per-section drilldown tables (Size, Headings, ..., Density)."""
    labels = [r.artifact.label for r in reports]
    sep = "| --- | " + " | ".join("---:" for _ in labels) + " |"
    out: list[str] = []

    sections: list[tuple[str, list[Row]]] = []
    qrows = _qual_rows(reports)
    quant_rows = _quant_rows(reports)
    drows = _derived_rows(reports)

    def by_aspect(rows: list[Row]) -> dict[str, list[Row]]:
        out_map: dict[str, list[Row]] = {}
        for r in rows:
            out_map.setdefault(r.aspect, []).append(r)
        return out_map

    for aspect, rows in by_aspect(qrows).items():
        sections.append((f"### Qualitative — {aspect}", rows))
    for aspect, rows in by_aspect(quant_rows).items():
        sections.append((f"### Quantitative — {aspect}", rows))
    for aspect, rows in by_aspect(drows).items():
        sections.append((f"### Derived — {aspect}", rows))

    for title, rows in sections:
        out.append(title)
        out.append("")
        out.append("| Measure | " + " | ".join(labels) + " |")
        out.append(sep)
        for row in rows:
            bold_set = _bold_indices(row.raw_values, row.bold_rule, bold_mode)
            cells = [row.measure]
            for i, disp in enumerate(row.display_values):
                if i in bold_set and disp not in {"n/a", "—"}:
                    disp = f"**{disp}**"
                cells.append(disp)
            out.append("| " + " | ".join(cells) + " |")
        out.append("")

    return "\n".join(out).rstrip() + "\n"


def render_per_pair_deltas(
    reports: list[EvalReport],
    pairs: list[tuple[str, str]],
) -> str:
    """For each (label_from, label_to) pair, emit a Δ table over all rubric dimensions."""
    by_label = {r.artifact.label: r for r in reports}
    out: list[str] = []
    for fr, to in pairs:
        if fr not in by_label or to not in by_label:
            raise ValueError(f"unknown label in pair: {fr} or {to}")
        r_from = by_label[fr]
        r_to = by_label[to]
        out.append(f"### Delta: {fr} → {to}")
        out.append("")
        out.append("| Dimension | Δ |")
        out.append("| --- | ---: |")
        for dim in rs.DIMENSIONS:
            v_from = getattr(getattr(r_from.qual, dim.group_key), dim.key)
            v_to = getattr(getattr(r_to.qual, dim.group_key), dim.key)
            # NA on either side makes the numeric delta undefined; report the
            # transition itself so the reader sees what changed.
            if v_from == "NA" or v_to == "NA":
                cell = f"{v_from} → {v_to}" if v_from != v_to else "NA"
            else:
                d = v_to - v_from
                sign = "+" if d > 0 else ""
                cell = f"{sign}{d}"
            out.append(f"| {dim.label} | {cell} |")
        d_mean = r_to.derived.rubric_rollup.overall_mean - r_from.derived.rubric_rollup.overall_mean
        sign_m = "+" if d_mean > 0 else ""
        out.append(f"| **Mean** | **{sign_m}{d_mean:.2f}** |")
        out.append("")
    return "\n".join(out).rstrip() + "\n"


def check_scope_classes(reports: list[EvalReport]) -> str | None:
    """Return a warning when reports span multiple scope classes (or mix tagged/untagged).

    A status update and a deep_research brief have different density expectations;
    comparing them in a single table can mislead unless the reader is told.
    """
    classes: dict[str | None, list[str]] = {}
    for r in reports:
        classes.setdefault(r.artifact.scope_class, []).append(r.artifact.label)
    distinct = {k for k in classes if k is not None}
    has_untagged = None in classes
    if len(distinct) > 1:
        parts = [f"{c}: {', '.join(classes[c])}" for c in sorted(distinct)]
        msg = "comparing across scope classes — " + " | ".join(parts)
        if has_untagged:
            msg += f" | untagged: {', '.join(classes[None])}"
        return msg
    if has_untagged and distinct:
        only = next(iter(distinct))
        return (
            f"some reports lack artifact.scope_class (assumed {only}); "
            f"untagged: {', '.join(classes[None])}"
        )
    return None


def collect_density_concerns(reports: list[EvalReport]) -> list[tuple[str, list[str]]]:
    """Return [(label, [concern strings])] pairs for reports with flagged density."""
    out: list[tuple[str, list[str]]] = []
    for r in reports:
        concerns = r.density_concerns()
        if concerns:
            out.append((r.artifact.label, concerns))
    return out


def check_rubric_versions(reports: list[EvalReport]) -> str | None:
    """Return a one-line warning when reports span >1 rubric version, else None.

    Reports without `metadata.rubric_version` set are reported separately so the user
    can decide whether to tag them.
    """
    versions: dict[str | None, list[str]] = {}
    for r in reports:
        v = r.metadata.rubric_version
        versions.setdefault(v, []).append(r.artifact.label)
    distinct_set = {v for v in versions if v is not None}
    has_untagged = None in versions
    if len(distinct_set) > 1:
        parts = [f"{v}: {', '.join(versions[v])}" for v in sorted(distinct_set)]
        msg = "comparing across rubric versions — " + " | ".join(parts)
        if has_untagged:
            msg += f" | untagged: {', '.join(versions[None])}"
        return msg
    if has_untagged and distinct_set:
        only_v = next(iter(distinct_set))
        return (
            f"some reports lack metadata.rubric_version (assumed {only_v}); "
            f"untagged: {', '.join(versions[None])}"
        )
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown comparison table from N eval reports."
    )
    parser.add_argument(
        "yamls",
        metavar="reports",
        nargs="+",
        help="Paths to validated eval report files.",
    )
    parser.add_argument(
        "--format",
        choices=["unified", "sections", "by-doc", "both"],
        default="unified",
        help=(
            "Output shape: unified comparison table, per-section drilldowns "
            "across docs, per-doc rollups (one self-contained section per doc), "
            "or both unified+sections."
        ),
    )
    parser.add_argument(
        "--bold-rule",
        choices=["max", "materially-different"],
        default="max",
        help="Bold per-row max(es) (default), or only when max is >= 1 above median.",
    )
    parser.add_argument(
        "--pairs",
        nargs="+",
        default=[],
        help="Optional delta pairs: --pairs 'a=b' 'c=d' renders Δ tables for each.",
    )
    parser.add_argument(
        "--table-styles",
        action="store_true",
        help=(
            "Prepend optional display.table_styles frontmatter for table-aware browsers. "
            "The Markdown table body is unchanged and remains portable."
        ),
    )
    parser.add_argument(
        "--allow-draft",
        action="store_true",
        help=(
            "Allow inputs with metadata.status='draft'. Comparisons are where scores "
            "become persuasive, so by default draft / incomplete inputs are rejected."
        ),
    )
    parser.add_argument(
        "--allow-misalignment",
        action="store_true",
        help=(
            "Allow inputs that fail the alignment-property check (score below 5 "
            "with no cited violation, or score 5 with a violation). Use only for "
            "debugging or explicit inspection."
        ),
    )
    args = parser.parse_args(argv)

    reports: list[EvalReport] = []
    blocking_errors: list[str] = []
    for p in args.yamls:
        try:
            r = EvalReport.from_eval_md(Path(p))
        except Exception as exc:
            blocking_errors.append(f"{p}: schema-invalid: {exc}")
            continue
        if not args.allow_draft and r.metadata.status != "complete":
            blocking_errors.append(
                f"{p}: status='{r.metadata.status}' (need 'complete'); pass --allow-draft to override"
            )
        if not args.allow_misalignment:
            align = r.alignment_errors()
            if align:
                blocking_errors.append(
                    f"{p}: alignment-invalid: {'; '.join(align[:3])}"
                    f"{' (...)' if len(align) > 3 else ''}"
                    "; pass --allow-misalignment to override"
                )
        reports.append(r)
    if blocking_errors:
        for e in blocking_errors:
            print(f"error: {e}", file=sys.stderr)
        return 1

    rubric_warning = check_rubric_versions(reports)
    if rubric_warning:
        print(f"warning: {rubric_warning}", file=sys.stderr)
    scope_warning = check_scope_classes(reports)
    if scope_warning:
        print(f"warning: {scope_warning}", file=sys.stderr)
    draft_inputs = [r.artifact.label for r in reports if r.metadata.status != "complete"]
    if draft_inputs:
        print(
            f"warning: draft inputs allowed via --allow-draft: {', '.join(draft_inputs)}",
            file=sys.stderr,
        )
    density_concerns = collect_density_concerns(reports)
    for label, concerns in density_concerns:
        for c in concerns:
            print(f"warning: {label}: {c}", file=sys.stderr)

    misaligned_inputs = [(r.artifact.label, r.alignment_errors()) for r in reports]
    misaligned_inputs = [(label, errs) for label, errs in misaligned_inputs if errs]
    if misaligned_inputs and args.allow_misalignment:
        print(
            f"warning: allowing {len(misaligned_inputs)} misaligned input(s) via "
            f"--allow-misalignment: {', '.join(label for label, _ in misaligned_inputs)}",
            file=sys.stderr,
        )

    bold_mode: BoldMode = "max" if args.bold_rule == "max" else "materially-different"

    chunks: list[str] = []
    if args.table_styles:
        chunks.append(
            render_table_style_frontmatter(comparison_labels=[r.artifact.label for r in reports])
        )
    if rubric_warning:
        chunks.append(f"> **Rubric-version warning:** {rubric_warning}\n")
    if scope_warning:
        chunks.append(f"> **Scope-class warning:** {scope_warning}\n")
    if draft_inputs:
        chunks.append(
            f"> **Draft-input warning:** "
            f"{len(draft_inputs)} input(s) had metadata.status != 'complete' but were "
            f"allowed via --allow-draft: {', '.join(draft_inputs)}\n"
        )
    if misaligned_inputs:
        lines = [
            "> **Alignment warning:**",
            f"> {len(misaligned_inputs)} input(s) failed the alignment property but were "
            "allowed via --allow-misalignment:",
            ">",
        ]
        for label, errs in misaligned_inputs:
            lines.append(f"> - **{label}:** {len(errs)} issue(s); first: {errs[0]}")
        chunks.append("\n".join(lines) + "\n")
    if density_concerns:
        lines = ["> **Density concerns:**", ">"]
        for label, concerns in density_concerns:
            lines.append(f"> - **{label}:** {'; '.join(concerns)}")
        chunks.append("\n".join(lines) + "\n")
    if args.format in ("unified", "both"):
        chunks.append(render_unified_table(reports, bold_mode))
        chunks.append(QUALITATIVE_SCORE_NOTE)
    if args.format in ("sections", "both"):
        chunks.append(render_section_drilldown(reports, bold_mode))
    if args.format == "by-doc":
        chunks.append(render_per_doc_rollup(reports, density_concerns))

    if args.pairs:
        pairs: list[tuple[str, str]] = []
        for spec in args.pairs:
            if "=" not in spec:
                raise SystemExit(f"invalid --pairs spec (need 'a=b'): {spec}")
            a, b = spec.split("=", 1)
            pairs.append((a.strip(), b.strip()))
        chunks.append(render_per_pair_deltas(reports, pairs))

    sys.stdout.write("\n\n".join(chunks).rstrip() + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
