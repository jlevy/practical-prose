"""
Pydantic schema for practical-writing eval reports.

Defines the canonical YAML shape for a single-document eval report that combines:
  - quantitative metrics (mirrors the `pprose metrics` Metrics)
  - qualitative rubric scores (one per dimension defined in rubric_schema.yaml, 1-5 scale)
  - per-rule findings (verdict + located evidence; the `violations` view is the
    miss subset, used by the alignment check and renderers)
  - derived rollups (density ratios, category means, overall mean)
  - eval metadata (date, evaluator, method)

Companion to:
  - docs/practical-prose-rubric.md (the rubric)
  - runbooks/practical-prose-eval-single.runbook.md (single-doc workflow)
  - `pprose compare` (consumes N validated reports → comparison Markdown)
  - pprose.rubric_schema / rubric_schema.yaml (single source of truth for groups,
    dimensions, version, and rule counts; everything in this file derives from it)

Run `pprose report --help` for the CLI surface.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Iterable
from datetime import date
from pathlib import Path
from typing import Annotated, Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from pprose import metrics as pwm
from pprose import rubric_schema as rs
from pprose.eval_render import render_single_doc_rollup
from pprose.table_styles import with_practical_prose_display_metadata

# Score = integer 1-5, or one of the two sentinels "NA" / "ERR".
#   1-5  = quality score per the rubric anchors. Always truthy, so a numeric score
#          can never be confused with "no score" by accident (`if score: ...`).
#   "NA" = the dimension does not engage this artifact (e.g. Calibration on a doc
#          that makes no probability claims). Decided by the per-dim NA anchor.
#   "ERR" = the scorer could not assess the dimension (a process failure, never a
#          document-quality verdict). Use sparingly; "attempted but materially missing"
#          is a score of 1 with a rule citation, not ERR.
# When aggregating, both "NA" and "ERR" are excluded from any mean; they are counted
# separately (na_dimensions vs err_dimensions) so a reader can tell apart "doesn't
# apply" from "couldn't be scored". See docs/practical-prose-rubric.md.
Score = Annotated[int, Field(ge=1, le=5)] | Literal["NA", "ERR"]

# Re-export from the canonical schema. Bumping the rubric (renaming a dimension,
# adding one, reordering groups) happens in rubric_schema.yaml — never here.
CURRENT_RUBRIC_VERSION = rs.RUBRIC_VERSION


ScopeClass = Literal["status", "brief", "memo", "deep_research", "design_doc"]


class ArtifactMeta(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str
    path: str
    commit_sha: str | None = None
    scope_class: ScopeClass | None = None


# Per-scope density thresholds. A density ratio below the *_min value flags a concern.
# Untagged artifacts (scope_class=None) get no thresholds applied — diagnostic-only mode.
# Tunable: bump these only with concrete evidence from the regression-test artifacts.
DENSITY_THRESHOLDS: dict[ScopeClass, dict[str, float]] = {
    "status": {},  # status updates legitimately have few links / tags
    "memo": {"links_per_1k_words_min": 0.5},
    "brief": {"links_per_1k_words_min": 1.0},
    "deep_research": {
        "links_per_1k_words_min": 1.0,
        "tables_per_1k_words_min": 0.3,
    },
    "design_doc": {"links_per_1k_words_min": 0.5},
}


class SizeMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")
    words: int
    sentences: int
    paragraphs: int
    lines: int
    pages_275wpp: float
    bytes_kb: float | None = None


class HeadingsCounts(BaseModel):
    model_config = ConfigDict(extra="forbid")
    h1: int
    h2: int
    h3: int
    h4: int
    h5: int = 0
    h6: int = 0
    total: int

    @model_validator(mode="after")
    def check_total(self) -> HeadingsCounts:
        computed = self.h1 + self.h2 + self.h3 + self.h4 + self.h5 + self.h6
        if self.total != computed:
            raise ValueError(f"headings.total={self.total} does not equal sum of h1..h6={computed}")
        return self


class StructuralMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")
    tables: int
    code_blocks: int
    images: int


class LinksMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")
    total: int
    external: int
    internal: int
    inline: int
    reference: int
    autolink: int
    bare_urls: int


class ProvenanceMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")
    bracket_tags: int
    footnote_refs: int = 0
    footnote_defs: int = 0


class LintMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")
    banned_register_hits: int


class QuantMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")
    size: SizeMetrics
    headings: HeadingsCounts
    structural: StructuralMetrics
    links: LinksMetrics
    provenance: ProvenanceMetrics
    lint: LintMetrics
    bracket_tag_examples: list[str] = []


# Score group models. Field names match dimension keys in rubric_schema.yaml; group
# class names match the group keys ({key.title()}Scores). Models are still explicit
# (Pydantic needs static field types) but `verify_models_match_schema()` confirms the
# alignment with the schema, so adding a new dimension means: update the YAML, add
# the field here, done.
class PurposeScores(BaseModel):
    model_config = ConfigDict(extra="forbid")
    suitability: Score
    scope: Score
    breadth: Score
    depth: Score


class ExpressionScores(BaseModel):
    model_config = ConfigDict(extra="forbid")
    clarity: Score
    coherence: Score
    concision: Score


class FormScores(BaseModel):
    model_config = ConfigDict(extra="forbid")
    organization: Score
    consistency: Score
    formatting: Score


class GroundingScores(BaseModel):
    model_config = ConfigDict(extra="forbid")
    verifiability: Score
    factuality: Score
    relevance: Score


class ReasoningScores(BaseModel):
    model_config = ConfigDict(extra="forbid")
    discipline: Score
    soundness: Score
    precision: Score
    parsimony: Score


class JudgmentScores(BaseModel):
    model_config = ConfigDict(extra="forbid")
    calibration: Score
    fairness: Score
    robustness: Score


class QualScores(BaseModel):
    model_config = ConfigDict(extra="forbid")
    purpose: PurposeScores
    expression: ExpressionScores
    form: FormScores
    grounding: GroundingScores
    reasoning: ReasoningScores
    judgment: JudgmentScores

    def all_scores(self) -> list[int | str]:
        return [getattr(getattr(self, d.group_key), d.key) for d in rs.DIMENSIONS]


# Parallel reason strings for each qual dimension. Optional so existing fixtures and
# from-metrics stubs validate without reasons; eval_score populates these from the
# model's JSON response, and validate --complete enforces presence for complete evals.
class PurposeReasons(BaseModel):
    model_config = ConfigDict(extra="forbid")
    suitability: str | None = None
    scope: str | None = None
    breadth: str | None = None
    depth: str | None = None


class ExpressionReasons(BaseModel):
    model_config = ConfigDict(extra="forbid")
    clarity: str | None = None
    coherence: str | None = None
    concision: str | None = None


class FormReasons(BaseModel):
    model_config = ConfigDict(extra="forbid")
    organization: str | None = None
    consistency: str | None = None
    formatting: str | None = None


class GroundingReasons(BaseModel):
    model_config = ConfigDict(extra="forbid")
    verifiability: str | None = None
    factuality: str | None = None
    relevance: str | None = None


class ReasoningReasons(BaseModel):
    model_config = ConfigDict(extra="forbid")
    discipline: str | None = None
    soundness: str | None = None
    precision: str | None = None
    parsimony: str | None = None


class JudgmentReasons(BaseModel):
    model_config = ConfigDict(extra="forbid")
    calibration: str | None = None
    fairness: str | None = None
    robustness: str | None = None


class QualReasons(BaseModel):
    model_config = ConfigDict(extra="forbid")
    purpose: PurposeReasons = PurposeReasons()
    expression: ExpressionReasons = ExpressionReasons()
    form: FormReasons = FormReasons()
    grounding: GroundingReasons = GroundingReasons()
    reasoning: ReasoningReasons = ReasoningReasons()
    judgment: JudgmentReasons = JudgmentReasons()

    def all_reasons(self) -> list[str | None]:
        return [getattr(getattr(self, d.group_key), d.key) for d in rs.DIMENSIONS]


# Verdict on a single rubric rule under a dimension.
#   "met"      = the rule was followed.
#   "violated" = the rule was broken; the finding documents how and where.
#   "partial"  = the rule was partly followed; treated like a violation by the
#                alignment check, but lets the scorer flag a near-miss.
#   "na"       = the rule does not engage this artifact (rule-level NA, distinct
#                from a whole dimension's NA score in QualScores).
Verdict = Literal["met", "violated", "partial", "na"]

# Verdicts that count as a rubric miss — surfaced via `EvalReport.violations`
# and used by the alignment check that ties scores 1-4 to at least one cited
# rule miss.
_MISS_VERDICTS: frozenset[str] = frozenset({"violated", "partial"})


class Location(BaseModel):
    """
    Pointer into the artifact for a rule finding.

    Anchors are ranked from most to least robust against doc edits:
      1. `quote` — a verbatim excerpt. Preferred: a doc-grep recovers the
         location even after line shifts; the scorer always has the source
         in context.
      2. `section` — the heading text as written ("Justified Deviations") or
         a numbered section ("§2.8"). Survives line shifts within a section.
      3. `line_start` / `line_end` — only when the scorer has authoritative
         line numbers. Fragile across edits but precise when fresh.
      4. `note` — free-text refinement ("near the top of the deviations
         table"). Fallback when nothing structural fits; prefer the others.

    At least one anchor must be populated. Prefer `quote` (with `section` as
    disambiguation when the same quote appears more than once).

    TODO: tighten the scorer prompt so it emits `line_start`/`line_end` when
    line numbers are known, and runs a doc-grep to ensure `quote` is verbatim
    before serializing.
    """

    model_config = ConfigDict(extra="forbid")
    quote: str | None = None
    section: str | None = None
    line_start: int | None = None
    line_end: int | None = None
    note: str | None = None

    @model_validator(mode="after")
    def at_least_one_anchor(self) -> Location:
        if not any([self.quote, self.section, self.line_start, self.note]):
            raise ValueError(
                "Location needs at least one anchor (quote, section, line_start, or note)"
            )
        if self.line_end is not None and self.line_start is None:
            raise ValueError("Location.line_end requires line_start")
        if (
            self.line_start is not None
            and self.line_end is not None
            and self.line_end < self.line_start
        ):
            raise ValueError(
                f"Location.line_end={self.line_end} < line_start={self.line_start}"
            )
        return self


class RuleFinding(BaseModel):
    """
    A scorer's judgment about one specific rule under one dimension.

    Each dimension in `rubric_schema.yaml` has an ordered list of rules; the
    1-indexed `rule_number` points into that list. The unified `verdict`
    captures both rule misses (the previous `violations` data) and notable
    rule hits, so a downstream reader can see "rule X was followed well" as
    explicitly as "rule Y was broken".

    `EvalReport.violations` is a convenience view over findings whose verdict
    is `violated` or `partial`.
    """

    model_config = ConfigDict(extra="forbid")
    dimension: str
    rule_number: int
    verdict: Verdict
    description: str
    locations: list[Location] = []

    @field_validator("dimension")
    @classmethod
    def check_dimension(cls, v: str) -> str:
        if v not in rs.DIMENSIONS_BY_LABEL:
            valid = ", ".join(rs.dimension_labels())
            raise ValueError(f"unknown dimension {v!r}; expected one of: {valid}")
        return v

    @model_validator(mode="after")
    def check_rule_number(self) -> RuleFinding:
        max_rule = rs.rule_count(self.dimension)
        # rule_count == 0 means the dimension has no numbered rules yet; allow any
        # rule_number (the finding will be cited under that dimension generically).
        if max_rule and not 1 <= self.rule_number <= max_rule:
            raise ValueError(
                f"rule_number={self.rule_number} out of range for dimension "
                f"{self.dimension!r} (1-{max_rule})"
            )
        # TODO: once the prompt + scorer reliably emit a Location for every miss,
        # tighten this validator to require `locations` non-empty when
        # `verdict in _MISS_VERDICTS`. Today the scorer sometimes omits a
        # location when the finding is whole-doc; rejecting those would drop
        # otherwise-useful findings, so we accept empty locations everywhere.
        return self

    @property
    def is_miss(self) -> bool:
        return self.verdict in _MISS_VERDICTS


class DensityRatios(BaseModel):
    model_config = ConfigDict(extra="forbid")
    words_per_sentence: float
    words_per_paragraph: float
    sentences_per_paragraph: float
    tables_per_1k_words: float
    tables_per_page: float
    tags_per_1k_words: float
    tags_per_page: float
    links_per_1k_words: float
    links_per_page: float


class StructureRatios(BaseModel):
    model_config = ConfigDict(extra="forbid")
    h4_share_of_headings: float


class RubricRollup(BaseModel):
    model_config = ConfigDict(extra="forbid")
    purpose_mean: float
    expression_mean: float
    form_mean: float
    grounding_mean: float
    reasoning_mean: float
    judgment_mean: float
    overall_mean: float
    # Count of dimensions actually scored (1-5). NA and ERR are both excluded from
    # rollup means. This field surfaces how many of the rubric's dimensions
    # contributed to overall_mean.
    assessed_dimensions: int = Field(default_factory=rs.dimension_count)
    # Number of dimensions marked NA (dimension does not engage this artifact).
    na_dimensions: int = 0
    # Number of dimensions marked ERR (scorer could not assess). Distinguishing this
    # from na_dimensions lets a reader see "we couldn't score X dims" instead of
    # treating those dims as silently dropped.
    err_dimensions: int = 0


class Tally(BaseModel):
    model_config = ConfigDict(extra="forbid")
    bull: int | None = None
    bear: int | None = None
    neutral: int | None = None

    def compact(self) -> str:
        if self.bull is None and self.bear is None and self.neutral is None:
            return "n/a"
        return f"{self.bull or 0}/{self.bear or 0}/{self.neutral or 0}"


class DerivedRollups(BaseModel):
    model_config = ConfigDict(extra="forbid")
    density: DensityRatios
    structure: StructureRatios
    rubric_rollup: RubricRollup
    tally: Tally | None = None


EvalStatus = Literal["draft", "complete"]


class EvalMetadata(BaseModel):
    model_config = ConfigDict(extra="forbid")
    eval_date: str
    evaluator: str
    # "draft" = stub or in-progress; "complete" = ready for comparison / publication.
    # `eval_report.py from-metrics` writes "draft"; eval_score.py promotes to
    # "complete" on a successful model-scoring merge.
    status: EvalStatus = "draft"
    method: str | None = None
    notes: str | None = None
    rubric_version: str | None = None

    # Reproducibility for model-scored evals. eval_score.py populates these so two
    # YAMLs with the same `method` string can still be told apart when any input
    # (prompt, rubric, guidelines, artifact, model) differs.
    model: str | None = None
    # `model_id` is the exact ID the SDK reported back (may include a date suffix
    # like "claude-sonnet-4-5-20250929" even when `model` was the alias "sonnet").
    model_id: str | None = None
    command: str | None = None
    prompt_sha256: str | None = None
    rubric_sha256: str | None = None
    guidelines_sha256: str | None = None
    artifact_sha256: str | None = None
    # Anthropic SDK metadata captured per call (Phase 1).
    sdk_version: str | None = None
    # cache_stats: {"creation_input_tokens": N, "read_input_tokens": M, "input_tokens": K, "output_tokens": L}
    # Lets a batch run show that docs 2..N hit the cache instead of paying full input cost.
    cache_stats: dict | None = None


class EvalReport(BaseModel):
    model_config = ConfigDict(extra="forbid")
    artifact: ArtifactMeta
    quant: QuantMetrics
    qual: QualScores
    qual_reasons: QualReasons = QualReasons()
    # Per-rule scorer judgments. Misses (`violated` / `partial`) are required for
    # every dimension scored 1-4 (enforced by `alignment_errors`); met / na findings
    # are optional and let a scorer record notable hits.
    rule_findings: list[RuleFinding] = []
    derived: DerivedRollups | None = None
    metadata: EvalMetadata
    # Portable display metadata. Eval semantics do not depend on this block; table-aware
    # browsers may use it to style generated Markdown tables, and other tools may ignore it.
    display: dict[str, Any] | None = None

    @property
    def violations(self) -> list[RuleFinding]:
        """
        Convenience view: findings whose verdict is a miss (`violated` / `partial`).

        Not serialized — `rule_findings` is the canonical store. Downstream
        renderers and the alignment check read this property so the "violations"
        framing stays in the API surface without duplicating data on disk.
        """
        return [f for f in self.rule_findings if f.is_miss]

    @model_validator(mode="after")
    def populate_derived(self) -> EvalReport:
        computed = compute_derived(self.quant, self.qual)
        if self.derived is None:
            self.derived = computed
        else:
            check_derived_consistency(self.derived, computed)
        return self

    def density_concerns(self) -> list[str]:
        """Return human-readable concerns based on the artifact's scope_class.

        Untagged artifacts (no scope_class) return []; the user can still inspect
        derived ratios manually but the schema does not flag them.
        """
        if self.derived is None or self.artifact.scope_class is None:
            return []
        thresholds = DENSITY_THRESHOLDS.get(self.artifact.scope_class, {})
        concerns: list[str] = []
        d = self.derived.density
        checks = (
            ("links_per_1k_words_min", d.links_per_1k_words, "link density (per 1k words)"),
            ("tables_per_1k_words_min", d.tables_per_1k_words, "table density (per 1k words)"),
            ("tags_per_1k_words_min", d.tags_per_1k_words, "bracket-tag density (per 1k words)"),
        )
        for key, value, label in checks:
            if key in thresholds and value < thresholds[key]:
                concerns.append(
                    f"low {label}: {value:.2f} < {thresholds[key]} (scope={self.artifact.scope_class})"
                )
        return concerns

    def alignment_errors(self) -> list[str]:
        """
        Return error messages for any rubric-alignment violations.

        The alignment property (per practical-prose-rubric.md):
          - score 1-4: at least one rule miss must cite the same dimension
          - score 5:   no rule miss may cite that dimension
          - NA / ERR:  no constraint (dimension doesn't engage / scorer couldn't
                       assess; outside the alignment scope)

        A miss is a `RuleFinding` with verdict `violated` or `partial`; surfaced
        via the `violations` property. An empty list means the report is
        alignment-valid.
        """
        errors: list[str] = []
        misses_by_dim: dict[str, list[RuleFinding]] = {}
        for v in self.violations:
            misses_by_dim.setdefault(v.dimension.lower(), []).append(v)

        for dim in rs.DIMENSIONS:
            score = getattr(getattr(self.qual, dim.group_key), dim.key)
            cited = misses_by_dim.get(dim.label.lower(), [])
            if score in ("NA", "ERR"):
                continue  # not-applicable or cannot-assess; outside alignment scope
            if 1 <= score <= 4 and not cited:
                errors.append(f"{dim.label}: score={score} but no rule miss cites this dimension")
            elif score == 5 and cited:
                rules = ", ".join(f"rule {v.rule_number}" for v in cited)
                errors.append(
                    f"{dim.label}: score=5 but {len(cited)} rule miss(es) cite this dimension ({rules})"
                )
        return errors

    @classmethod
    def from_yaml(cls, source: str | Path) -> EvalReport:
        text = source.read_text(encoding="utf-8") if isinstance(source, Path) else source
        data = yaml.safe_load(text)
        return cls.model_validate(data)

    def to_yaml(self, *, include_table_styles: bool = False) -> str:
        data = self.model_dump(mode="json", exclude_none=True)
        if include_table_styles:
            data = with_practical_prose_display_metadata(data)
        return yaml.safe_dump(
            data,
            sort_keys=True,
            default_flow_style=False,
            indent=2,
            allow_unicode=True,
        )

    @classmethod
    def from_eval_md(cls, source: str | Path) -> EvalReport:
        """Load an `.eval.md` file: YAML frontmatter (delimited by ---) + body."""
        text = source.read_text(encoding="utf-8") if isinstance(source, Path) else source
        data = _parse_frontmatter(text)
        return cls.model_validate(data)

    def to_eval_md(self, body: str, *, include_table_styles: bool = True) -> str:
        """Serialize as `.eval.md`: YAML frontmatter + caller-rendered body.

        The frontmatter is canonical structured data; the body is the human-
        readable rendering, regenerated whenever the frontmatter changes.
        """
        frontmatter = self.to_yaml(include_table_styles=include_table_styles)
        return f"---\n{frontmatter}---\n\n{body.rstrip()}\n"


def _parse_frontmatter(text: str) -> dict:
    """Extract the YAML object delimited by leading and trailing '---' lines."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing YAML frontmatter (expected '---' on first line)")
    end = -1
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end < 0:
        raise ValueError("unterminated YAML frontmatter (no closing '---')")
    return yaml.safe_load("\n".join(lines[1:end])) or {}


def _round(value: float) -> float:
    return round(value, 4)


def compute_derived(quant: QuantMetrics, qual: QualScores) -> DerivedRollups:
    s = quant.size
    structural = quant.structural
    links = quant.links
    provenance = quant.provenance
    headings = quant.headings

    words = s.words or 1
    pages = s.pages_275wpp or 1.0
    sentences = s.sentences or 1
    paragraphs = s.paragraphs or 1
    headings_total = headings.total or 1

    density = DensityRatios(
        words_per_sentence=_round(words / sentences),
        words_per_paragraph=_round(words / paragraphs),
        sentences_per_paragraph=_round(sentences / paragraphs),
        tables_per_1k_words=_round(structural.tables * 1000 / words),
        tables_per_page=_round(structural.tables / pages),
        tags_per_1k_words=_round(provenance.bracket_tags * 1000 / words),
        tags_per_page=_round(provenance.bracket_tags / pages),
        links_per_1k_words=_round(links.total * 1000 / words),
        links_per_page=_round(links.total / pages),
    )

    structure_ratios = StructureRatios(
        h4_share_of_headings=_round(headings.h4 / headings_total),
    )

    # "NA" = not applicable to this artifact; "ERR" = scorer could not assess.
    # Both are excluded from group/overall means so they don't drag the rollup down,
    # but they are counted separately (assessed_dimensions, na_dimensions,
    # err_dimensions) so a reader can tell "doesn't apply" from "couldn't be scored".
    def _is_scored(value: int | str) -> bool:
        return isinstance(value, int)

    def _mean_scored(scores: list[int | str]) -> float:
        scored = [s for s in scores if _is_scored(s)]
        if not scored:
            return 0.0
        return _round(sum(scored) / len(scored))

    group_means: dict[str, float] = {}
    for group in rs.GROUPS:
        group_obj = getattr(qual, group.key)
        scores = [getattr(group_obj, d.key) for d in group.dimensions]
        group_means[group.key] = _mean_scored(scores)

    all_scores = qual.all_scores()
    overall_mean = _mean_scored(all_scores)
    assessed_dimensions = sum(1 for s in all_scores if _is_scored(s))
    na_dimensions = sum(1 for s in all_scores if s == "NA")
    err_dimensions = sum(1 for s in all_scores if s == "ERR")

    rollup = RubricRollup(
        purpose_mean=group_means["purpose"],
        expression_mean=group_means["expression"],
        form_mean=group_means["form"],
        grounding_mean=group_means["grounding"],
        reasoning_mean=group_means["reasoning"],
        judgment_mean=group_means["judgment"],
        overall_mean=overall_mean,
        assessed_dimensions=assessed_dimensions,
        na_dimensions=na_dimensions,
        err_dimensions=err_dimensions,
    )

    return DerivedRollups(
        density=density,
        structure=structure_ratios,
        rubric_rollup=rollup,
        tally=None,
    )


def check_derived_consistency(
    provided: DerivedRollups, computed: DerivedRollups, tol: float = 0.01
) -> None:
    # Compare every recomputable float field. density/structure check all their
    # fields; rubric_rollup checks only the group/overall means (the integer
    # counts are not tolerance-compared).
    checks: list[tuple[str, BaseModel, BaseModel, Iterable[str]]] = [
        ("density", provided.density, computed.density, DensityRatios.model_fields),
        ("structure", provided.structure, computed.structure, StructureRatios.model_fields),
        (
            "rubric_rollup",
            provided.rubric_rollup,
            computed.rubric_rollup,
            (
                "purpose_mean",
                "expression_mean",
                "form_mean",
                "grounding_mean",
                "reasoning_mean",
                "judgment_mean",
                "overall_mean",
            ),
        ),
    ]
    mismatches: list[tuple[str, float, float]] = []
    for prefix, prov, comp, fields in checks:
        for f in fields:
            p, c = getattr(prov, f), getattr(comp, f)
            if abs(p - c) > tol:
                mismatches.append((f"{prefix}.{f}", p, c))
    if mismatches:
        lines = "\n".join(f"  {k}: provided={p} computed={c}" for k, p, c in mismatches)
        raise ValueError(f"derived rollups are inconsistent with quant+qual:\n{lines}")


def quant_from_metrics(metrics: pwm.Metrics, *, bytes_kb: float | None = None) -> QuantMetrics:
    """Translate the metrics-script Metrics dataclass into the schema's QuantMetrics."""
    return QuantMetrics(
        size=SizeMetrics(
            words=metrics.words,
            sentences=metrics.sentences,
            paragraphs=metrics.paragraphs,
            lines=metrics.lines,
            pages_275wpp=metrics.pages,
            bytes_kb=bytes_kb,
        ),
        headings=HeadingsCounts(
            h1=metrics.headings["h1"],
            h2=metrics.headings["h2"],
            h3=metrics.headings["h3"],
            h4=metrics.headings["h4"],
            h5=metrics.headings["h5"],
            h6=metrics.headings["h6"],
            total=metrics.headings_total,
        ),
        structural=StructuralMetrics(
            tables=metrics.tables,
            code_blocks=metrics.code_blocks,
            images=metrics.images,
        ),
        links=LinksMetrics(
            total=metrics.links_total,
            external=metrics.links_external,
            internal=metrics.links_internal,
            inline=metrics.links_inline,
            reference=metrics.links_reference_use,
            autolink=metrics.links_autolink,
            bare_urls=metrics.bare_urls,
        ),
        provenance=ProvenanceMetrics(
            bracket_tags=metrics.bracket_tags,
            footnote_refs=metrics.footnote_references,
            footnote_defs=metrics.footnote_definitions,
        ),
        lint=LintMetrics(banned_register_hits=metrics.banned_register_hits),
        bracket_tag_examples=metrics.bracket_tag_examples,
    )


def stub_qual() -> QualScores:
    """An ERR-everywhere qual block. ERR means 'scorer could not assess' per the
    rubric; the stub is unscored placeholder content.

    The user must replace these with real 1-5 scores (or NA where the dimension does
    not engage the artifact) before the YAML is meaningful.
    """
    return QualScores(
        purpose=PurposeScores(suitability="ERR", scope="ERR", breadth="ERR", depth="ERR"),
        expression=ExpressionScores(
            clarity="ERR",
            coherence="ERR",
            concision="ERR",
        ),
        form=FormScores(
            organization="ERR",
            consistency="ERR",
            formatting="ERR",
        ),
        grounding=GroundingScores(verifiability="ERR", factuality="ERR", relevance="ERR"),
        reasoning=ReasoningScores(
            discipline="ERR", soundness="ERR", precision="ERR", parsimony="ERR"
        ),
        judgment=JudgmentScores(calibration="ERR", fairness="ERR", robustness="ERR"),
    )


def completeness_errors(report: EvalReport) -> list[str]:
    """Return a list of reasons the report is not "complete".

    Used by `validate --complete` and (downstream) by eval_compare to reject draft
    inputs by default. A complete eval has all of: status=complete, evaluator set
    (not "TODO"), rubric_version present, at least one dimension actually scored
    (not all NA/ERR), and a non-null reason for every dimension scored 1-5.
    """
    errors: list[str] = []
    if report.metadata.status != "complete":
        errors.append(
            f"metadata.status='{report.metadata.status}' (expected 'complete'); "
            "eval_score.py promotes to 'complete' on a successful model-scoring merge"
        )
    if report.metadata.evaluator == "TODO":
        errors.append("metadata.evaluator='TODO' (set the human or model identity)")
    if report.metadata.rubric_version is None:
        errors.append("metadata.rubric_version missing")
    if all(s in ("NA", "ERR") for s in report.qual.all_scores()):
        errors.append(
            "qual has no scored dimensions (all NA or ERR); run eval_score.py or fill manually"
        )
    scores = report.qual.all_scores()
    reasons = report.qual_reasons.all_reasons()
    canonical_names = [d.label for d in rs.DIMENSIONS]
    for name, score, reason in zip(canonical_names, scores, reasons, strict=True):
        if isinstance(score, int) and 1 <= score <= 5 and reason is None:
            errors.append(
                f"qual_reasons.{name} missing (every score 1-5 needs a reason on complete evals)"
            )
        if score == "NA" and reason is None:
            errors.append(
                f"qual_reasons.{name} missing (every NA needs a reason explaining why the dimension does not apply)"
            )
    return errors


def cmd_validate(args: argparse.Namespace) -> int:
    path = Path(args.path)
    try:
        report = EvalReport.from_eval_md(path)
    except Exception as exc:
        print(f"INVALID: {path}\n  {exc}", file=sys.stderr)
        return 1
    if not args.allow_misalignment:
        errors = report.alignment_errors()
        if errors:
            print(f"INVALID (alignment): {path}", file=sys.stderr)
            for e in errors:
                print(f"  {e}", file=sys.stderr)
            print(
                "  hint: pass --allow-misalignment to bypass during in-progress drafts",
                file=sys.stderr,
            )
            return 1
    if args.complete:
        errors = completeness_errors(report)
        if errors:
            print(f"INVALID (incomplete): {path}", file=sys.stderr)
            for e in errors:
                print(f"  {e}", file=sys.stderr)
            return 1
    print(f"OK: {path}")
    return 0


def cmd_compute_derived(args: argparse.Namespace) -> int:
    path = Path(args.path)
    raw = _parse_frontmatter(path.read_text(encoding="utf-8"))
    raw.pop("derived", None)
    report = EvalReport.model_validate(raw)
    body = render_single_doc_rollup(report, heading_level=1)
    output = report.to_eval_md(body)
    if args.in_place:
        path.write_text(output, encoding="utf-8")
        print(f"OK: rewrote {path}")
    else:
        sys.stdout.write(output)
    return 0


def cmd_from_metrics(args: argparse.Namespace) -> int:
    artifact_path = Path(args.artifact)
    if not artifact_path.is_file():
        print(f"error: not a file: {artifact_path}", file=sys.stderr)
        return 1

    metrics = pwm.measure(artifact_path)
    bytes_kb = round(artifact_path.stat().st_size / 1024, 1)

    # Resolve the artifact path to absolute so the stored `path` is unambiguous
    # regardless of the user's cwd when running `from-metrics`. Downstream tools
    # (`eval_score.py`) then don't have to guess what a relative path is
    # relative to.
    abs_artifact_path = artifact_path.resolve()

    report = EvalReport(
        artifact=ArtifactMeta(
            label=args.label or artifact_path.stem,
            path=str(abs_artifact_path),
            commit_sha=args.commit_sha,
            scope_class=args.scope_class,
        ),
        quant=quant_from_metrics(metrics, bytes_kb=bytes_kb),
        qual=stub_qual(),
        rule_findings=[],
        metadata=EvalMetadata(
            eval_date=date.today().isoformat(),
            evaluator=args.evaluator or "TODO",
            status="draft",
            method=args.method,
            notes="Stub — qual scores are ERR (cannot-assess); fill in before validating downstream.",
            rubric_version=args.rubric_version or CURRENT_RUBRIC_VERSION,
        ),
    )

    body = render_single_doc_rollup(report, heading_level=1)
    output = report.to_eval_md(body)
    if args.out:
        Path(args.out).write_text(output, encoding="utf-8")
        print(f"OK: wrote {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(output)
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate and compute derived rollups for eval reports."
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_validate = sub.add_parser("validate", help="Load + validate a single eval report.")
    p_validate.add_argument("path", help="Path to eval report file.")
    p_validate.add_argument(
        "--allow-misalignment",
        action="store_true",
        help="Skip the alignment-property check (use only for in-progress drafts).",
    )
    p_validate.add_argument(
        "--complete",
        action="store_true",
        help=(
            "Additionally require the report to be complete (status=complete, "
            "evaluator set, rubric_version present, all dimensions scored, "
            "reasons present for every score 1-5). Use as a publish gate."
        ),
    )
    p_validate.set_defaults(func=cmd_validate)

    p_compute = sub.add_parser(
        "compute-derived",
        help="Recompute derived rollups from quant+qual; print or rewrite in place.",
    )
    p_compute.add_argument("path", help="Path to eval report file.")
    p_compute.add_argument(
        "--in-place", action="store_true", help="Rewrite the eval report in place."
    )
    p_compute.set_defaults(func=cmd_compute_derived)

    p_from = sub.add_parser(
        "from-metrics",
        help="Build an eval report stub from a Markdown artifact.",
    )
    p_from.add_argument("artifact", help="Path to Markdown artifact.")
    p_from.add_argument("--label", default=None, help="Artifact label (default: file stem).")
    p_from.add_argument("--commit-sha", default=None, help="Artifact commit SHA.")
    p_from.add_argument("--evaluator", default=None, help="Evaluator identity (default: TODO).")
    p_from.add_argument("--method", default=None, help="Eval method (e.g. subagent / human).")
    p_from.add_argument(
        "--rubric-version",
        default=None,
        help=f"Rubric version tag (default: {CURRENT_RUBRIC_VERSION}).",
    )
    p_from.add_argument(
        "--scope-class",
        default=None,
        choices=["status", "brief", "memo", "deep_research", "design_doc"],
        help="Artifact scope class; enables density-threshold flagging in eval_compare.py.",
    )
    p_from.add_argument("--out", default=None, help="Output path (default: stdout).")
    p_from.set_defaults(func=cmd_from_metrics)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
