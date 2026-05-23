"""
Pydantic schema for practical-writing eval reports.

Defines the canonical YAML shape for a single-document eval report that combines:
  - quantitative metrics (mirrors the `pprose metrics` Metrics)
  - qualitative rubric scores (one per dimension defined in rubric_schema.yaml, 0-5 scale)
  - cited guideline-rule violations
  - derived rollups (density ratios, category means, overall mean)
  - eval metadata (date, evaluator, method)

Companion to:
  - docs/practical-prose-rubric.md (the rubric)
  - runbooks/practical-prose-eval-single.runbook.md (single-doc workflow)
  - `pprose compare` (consumes N validated reports → comparison Markdown)
  - pprose.rubric_schema / rubric_schema.yaml (single source of truth for groups,
    dimensions, version, and rule counts; everything in this file derives from it)

Usage:
  pprose report validate path/to/artifact.eval.md
  pprose report compute-derived path/to/artifact.eval.md
  pprose report compute-derived path/to/artifact.eval.md --in-place
  pprose report from-metrics path/to/artifact.md > artifact.eval.md
  pprose report from-metrics path/to/artifact.md --label NAME --out artifact.eval.md
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path
from typing import Annotated, Any, Literal

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from pprose import metrics as pwm
from pprose import rubric_schema as rs
from pprose.eval_render import render_single_doc_rollup
from pprose.table_styles import with_practical_prose_display_metadata

# Score = integer 0-5 or the literal "NA" (not applicable to this artifact).
# 0 means "applicable but unassessable" (content missing); "NA" means the dimension
# does not apply to this artifact at all.
# When aggregating, "NA" is excluded from any mean; 0 is also excluded so that
# unassessable dimensions don't drag the rollup down.
Score = Annotated[int, Field(ge=0, le=5)] | Literal["NA"]
NA: Literal["NA"] = "NA"

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
    # Scope is a newer addition; default 0 ("cannot assess") lets fixtures predating
    # this dimension validate. Re-score to a non-zero value before publication.
    scope: Score = 0
    breadth: Score
    depth: Score


class ExpressionScores(BaseModel):
    model_config = ConfigDict(extra="forbid")
    clarity: Score
    coherence: Score
    concision: Score
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


# Map from group key to its scores class. Used by `all_scores` and the rollup
# computation so the iteration order always matches the schema.
_SCORES_CLASS_BY_GROUP: dict[str, type[BaseModel]] = {
    "purpose": PurposeScores,
    "expression": ExpressionScores,
    "grounding": GroundingScores,
    "reasoning": ReasoningScores,
    "judgment": JudgmentScores,
}


class QualScores(BaseModel):
    model_config = ConfigDict(extra="forbid")
    purpose: PurposeScores
    expression: ExpressionScores
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
    grounding: GroundingReasons = GroundingReasons()
    reasoning: ReasoningReasons = ReasoningReasons()
    judgment: JudgmentReasons = JudgmentReasons()

    def all_reasons(self) -> list[str | None]:
        return [getattr(getattr(self, d.group_key), d.key) for d in rs.DIMENSIONS]


class Violation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    dimension: str
    rule_number: int
    description: str
    location: str | None = None

    @field_validator("dimension")
    @classmethod
    def check_dimension(cls, v: str) -> str:
        if v not in rs.DIMENSIONS_BY_LABEL:
            valid = ", ".join(rs.dimension_labels())
            raise ValueError(f"unknown dimension {v!r}; expected one of: {valid}")
        return v

    @model_validator(mode="after")
    def check_rule_number(self) -> Violation:
        max_rule = rs.rule_count(self.dimension)
        # rule_count == 0 means the dimension has no numbered rules yet; allow any
        # rule_number (the violation will be cited under that dimension generically).
        if max_rule == 0:
            return self
        if not 1 <= self.rule_number <= max_rule:
            raise ValueError(
                f"rule_number={self.rule_number} out of range for dimension "
                f"{self.dimension!r} (1-{max_rule})"
            )
        return self


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
    grounding_mean: float
    reasoning_mean: float
    judgment_mean: float
    overall_mean: float
    # Count of dimensions actually scored (1-5). Score 0 means "applicable but
    # unassessable" and "NA" means "not applicable"; both are excluded from rollup
    # means. This field surfaces how many of the rubric's dimensions contributed
    # to overall_mean.
    assessed_dimensions: int = Field(default_factory=rs.dimension_count)
    # Number of dimensions marked NA. Useful for distinguishing "we couldn't assess
    # this" (score 0, raises a flag) from "this dimension genuinely doesn't apply"
    # (NA, no flag).
    na_dimensions: int = 0


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
    violations: list[Violation] = []
    derived: DerivedRollups | None = None
    metadata: EvalMetadata
    # Portable display metadata. Eval semantics do not depend on this block; table-aware
    # browsers may use it to style generated Markdown tables, and other tools may ignore it.
    display: dict[str, Any] | None = None

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
        """Return error messages for any rubric-alignment violations.

        The alignment property (per practical-prose-rubric.md):
          - score 1-4: at least one Violation must cite the same dimension
          - score 5:   no Violation may cite that dimension
          - score 0:   no constraint (cannot-assess; outside the alignment scope)

        An empty list means the report is alignment-valid.
        """
        errors: list[str] = []
        violations_by_dim: dict[str, list[Violation]] = {}
        for v in self.violations:
            violations_by_dim.setdefault(v.dimension.lower(), []).append(v)

        for dim in rs.DIMENSIONS:
            score = getattr(getattr(self.qual, dim.group_key), dim.key)
            cited = violations_by_dim.get(dim.label.lower(), [])
            if score == 0 or score == "NA":
                continue  # cannot-assess or not-applicable; outside alignment scope
            if 1 <= score <= 4 and not cited:
                errors.append(f"{dim.label}: score={score} but no violation cites this dimension")
            elif score == 5 and cited:
                rules = ", ".join(f"rule {v.rule_number}" for v in cited)
                errors.append(
                    f"{dim.label}: score=5 but {len(cited)} violation(s) cite this dimension ({rules})"
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


def _round(value: float, digits: int = 4) -> float:
    return round(value, digits)


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

    # Score 0 = "applicable but unassessable"; "NA" = "not applicable to this artifact".
    # Both are excluded from group/overall means so they don't drag the rollup down,
    # but they are counted separately (assessed_dimensions vs na_dimensions) so a
    # reader can tell apart "couldn't measure" from "doesn't apply."
    def _is_scored(value: int | str) -> bool:
        return isinstance(value, int) and value != 0

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

    rollup = RubricRollup(
        purpose_mean=group_means["purpose"],
        expression_mean=group_means["expression"],
        grounding_mean=group_means["grounding"],
        reasoning_mean=group_means["reasoning"],
        judgment_mean=group_means["judgment"],
        overall_mean=overall_mean,
        assessed_dimensions=assessed_dimensions,
        na_dimensions=na_dimensions,
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
    pairs = [
        (
            "density.words_per_sentence",
            provided.density.words_per_sentence,
            computed.density.words_per_sentence,
        ),
        (
            "density.words_per_paragraph",
            provided.density.words_per_paragraph,
            computed.density.words_per_paragraph,
        ),
        (
            "density.sentences_per_paragraph",
            provided.density.sentences_per_paragraph,
            computed.density.sentences_per_paragraph,
        ),
        (
            "density.tables_per_1k_words",
            provided.density.tables_per_1k_words,
            computed.density.tables_per_1k_words,
        ),
        (
            "density.tables_per_page",
            provided.density.tables_per_page,
            computed.density.tables_per_page,
        ),
        (
            "density.tags_per_1k_words",
            provided.density.tags_per_1k_words,
            computed.density.tags_per_1k_words,
        ),
        ("density.tags_per_page", provided.density.tags_per_page, computed.density.tags_per_page),
        (
            "density.links_per_1k_words",
            provided.density.links_per_1k_words,
            computed.density.links_per_1k_words,
        ),
        (
            "density.links_per_page",
            provided.density.links_per_page,
            computed.density.links_per_page,
        ),
        (
            "structure.h4_share_of_headings",
            provided.structure.h4_share_of_headings,
            computed.structure.h4_share_of_headings,
        ),
        (
            "rubric_rollup.purpose_mean",
            provided.rubric_rollup.purpose_mean,
            computed.rubric_rollup.purpose_mean,
        ),
        (
            "rubric_rollup.expression_mean",
            provided.rubric_rollup.expression_mean,
            computed.rubric_rollup.expression_mean,
        ),
        (
            "rubric_rollup.grounding_mean",
            provided.rubric_rollup.grounding_mean,
            computed.rubric_rollup.grounding_mean,
        ),
        (
            "rubric_rollup.reasoning_mean",
            provided.rubric_rollup.reasoning_mean,
            computed.rubric_rollup.reasoning_mean,
        ),
        (
            "rubric_rollup.judgment_mean",
            provided.rubric_rollup.judgment_mean,
            computed.rubric_rollup.judgment_mean,
        ),
        (
            "rubric_rollup.overall_mean",
            provided.rubric_rollup.overall_mean,
            computed.rubric_rollup.overall_mean,
        ),
    ]
    mismatches = [(k, p, c) for k, p, c in pairs if abs(p - c) > tol]
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
    """A 0-everywhere qual block. Score 0 means 'applicable but unassessable' per
    the rubric.

    The user must replace these with real scores (or NA where the dimension does
    not apply to the artifact) before the YAML is meaningful.
    """
    return QualScores(
        purpose=PurposeScores(suitability=0, scope=0, breadth=0, depth=0),
        expression=ExpressionScores(
            clarity=0,
            coherence=0,
            concision=0,
            organization=0,
            consistency=0,
            formatting=0,
        ),
        grounding=GroundingScores(verifiability=0, factuality=0, relevance=0),
        reasoning=ReasoningScores(discipline=0, soundness=0, precision=0, parsimony=0),
        judgment=JudgmentScores(calibration=0, fairness=0, robustness=0),
    )


def completeness_errors(report: EvalReport) -> list[str]:
    """Return a list of reasons the report is not "complete".

    Used by `validate --complete` and (downstream) by eval_compare to reject draft
    inputs by default. A complete eval has all of: status=complete, evaluator set
    (not "TODO"), rubric_version present, at least one dimension actually scored
    (not all zeros), and a non-null reason for every dimension scored 1-5.
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
    if all(s == 0 or s == "NA" for s in report.qual.all_scores()):
        errors.append(
            "qual has no scored dimensions (all 0 or NA); run eval_score.py or fill manually"
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
        violations=[],
        metadata=EvalMetadata(
            eval_date=date.today().isoformat(),
            evaluator=args.evaluator or "TODO",
            status="draft",
            method=args.method,
            notes="Stub — qual scores are 0 (cannot-assess); fill in before validating downstream.",
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
