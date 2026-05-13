---
title: Practical Prose Metrics and Frontmatter
description: Operational appendix to the practical-prose system; maps each of the 18 review dimensions to quantitative metrics and qualitative checks, and documents the recommended frontmatter schema for practical-prose documents.
date: 2026-05-11
status: active
---
# Practical Prose Metrics and Frontmatter

Version: v0.1 (last update 2026-05-11)\
Joshua Levy (github.com/jlevy) with agent assistance

An operational appendix to the practical-prose system.
The [rubric](practical-prose-rubric.md) is the descriptive 0-5 instrument; this doc
gathers the **quantitative metrics** and **qualitative checks** that operationalize each
dimension, and the **recommended frontmatter schema** that lets agents apply the
guidelines consistently.

The metrics here are diagnostic, not the rubric.
A document with no banned-register hits and a fully populated frontmatter can still
score 1 on Soundness; conversely, a document with many vague-word hits may still earn a
4 if every hit is in a context where it is the right word.
Use metrics to **catch avoidable defects fast** so that rubric scoring can focus on
substantive judgment.

## Metrics by Dimension

For each dimension, the table lists at least one quantitative metric and one qualitative
check. *“Tooling”* names the operational tool today;
**scripts/practical_prose_metrics.py** is the deterministic metrics script in this
directory, **eval_score.py** runs an LLM scorer against the rubric, and **manual**
denotes a human reviewer.

| § | Dimension | Quantitative metric(s) | Qualitative check | Tooling |
| ---: | --- | --- | --- | --- |
| 1 | Suitability | Presence of explicit `purpose`, `audience`, `scope` fields (frontmatter); presence of recommendation/findings/milestones section by doc type | Can a target reader say what the doc is for after 30 seconds? | frontmatter check; manual skim test |
| 2 | Scope | Presence of `scope` and optionally `out_of_scope` fields; count of headings outside declared scope | Does the body honor the declared boundary? | frontmatter check; manual |
| 3 | Breadth | Count of relevant case classes addressed (out of a domain-specific expected set) | Are the obvious affected areas covered? | manual; SME |
| 4 | Depth | Count of vague magnitude words (“rapid,” “large”) not paired with quantification; count of endpoints cited where a series exists | Is section depth proportional to section importance? | banned-register lint (metrics.py); manual |
| 5 | Clarity | Banned-register hits (count + examples; full common-doc-guidelines §4.2 list); pedantic-marker hits (canonicality declarations, word-choice justifications, reading-order instructions); vague-word hits; sentence length distribution; mean and p95 sentence length | Does prose read cleanly aloud; is the document free of self-referential pedantry? | metrics.py; manual |
| 6 | Coherence | Paragraph length distribution; presence of stub transitions (“As shown above” without recap) | Does each paragraph have one job; do transitions bridge? | manual; LLM-assist |
| 7 | Concision | Word count vs target by doc type; repeated n-gram count; low-information paragraph flag; replacement-history phrase hits (regex set: “previously named,” “formerly,” “under the new layout,” “removed,” etc.) | Does removing a section lose information; is replacement history absent outside history-genre exceptions? | metrics.py words/paragraphs; manual cut test |
| 8 | Organization | Heading-level skip count (h1→h3 without h2); generic-heading hits (“Overview,” “Background,” “Notes,” “Details”); table count and column densities; figure-caption presence; link-target stability (no commit-less URLs to mutable refs) | Are sections sequenced for the task; do tables earn their tabular shape; do headings cleave to subject contours? | metrics.py headings/tables; manual |
| 9 | Style Consistency | Acronym casing variance; dialect mixing; date-format variance; parallel-list violations; spaced em-dash count and em-dash density per 1000 words | Does the document follow the chosen style guide; are em dashes used sparingly and in American style? | linter; manual |
| 10 | Formatting | Markdown lint pass/fail; frontmatter present and valid; footer present | Renders correctly across mediums? | flowmark / md-lint; metrics.py footnote round-trip |
| 11 | Verifiability | % quantitative claims with source pointer; bracket-tag count by type (`[VERIFIED]`, `[UNVERIFIED]`, `[ESTIMATED]`, `[DERIVED:]`, `[ASSUMING:]`); footnote/citation count | Can a competent reader trace claims to evidence without external lookup? | metrics.py bracket tags + footnotes; manual claim audit |
| 12 | Factuality | Broken-link rate; stale-source count; numeric discrepancies vs cited source | Do cited sources actually support the claim at the asserted strength? | link checker; manual / SME audit |
| 13 | Inference Discipline | Rung-tag count (`[observed]`, `[judged]`, `[interpreted]`, `[implied]`) in audit/eval modes; multi-rung-per-sentence flag | Are observation, judgment, interpretation, implication kept distinct? | metrics.py bracket tags (audit mode); LLM-assist; manual |
| 14 | Soundness | `[ASSUMING:]` tag count where assumptions are load-bearing; count of unbridged “signal → outcome” leaps | Are mechanisms named where causation is asserted; is counter-evidence engaged? | metrics.py bracket tags; manual / SME |
| 15 | Precision | Vague-countable hits (“several,” “various,” “many”); umbrella-term hits (“users,” “latency”) where domain sub-distinctions matter | Is the most specific term the audience can parse used throughout? | banned-register / linter extension; manual |
| 16 | Calibration | Count of probability claims; count of those with cited base rate; small-sample shrinkage explicit; scenario probabilities sum check | Does claim strength match evidence strength? | LLM-assist; manual |
| 17 | Fairness | Opposing-vs-supporting paragraph count *(flag only; see note below)*; depth asymmetry ratio; risk-inventory class coverage | Are opposing positions argued at proportional evidentiary depth? | LLM-assist; manual / SME |
| 18 | Robustness | Count of explicit interpretive-lens statements; count of alternative-lens tests | Do key claims survive plausible alternative interpretations? | manual; LLM-assist |

Most rows have a deterministic component and a judgment component.
The deterministic component runs in CI and catches regressions cheaply; the judgment
component runs at review time and catches substantive failures the lint will never
notice.

**Note on §17 Fairness.** The opposing-vs-supporting paragraph count and depth-ratio
metrics are review flags, not measures of fairness.
The guidelines define fairness as proportional representation by plausibility,
materiality, and evidence strength (§17.1), not equal airtime.
Symmetric paragraph counts can be a sign of false balance, not fairness; treat the count
as a prompt to inspect the underlying evidence, never as proof that the document is
fair.

## Tooling map

- [scripts/practical_prose_metrics.py](../scripts/practical_prose_metrics.py): the
  deterministic metrics script.
  Computes headings by depth, link counts (external/internal, by markdown form),
  footnote references and definitions, bracket-tag counts and examples, bare URLs,
  tables, code blocks, banned-register hits (Clarity Rule 4 by default; overridable),
  word/sentence/paragraph/line counts, and page estimate.
- [scripts/eval_score.py](../scripts/eval_score.py): LLM-based rubric scorer.
- [scripts/eval_report.py](../scripts/eval_report.py): combines metrics and scores into
  a single eval report.
- [scripts/eval_compare.py](../scripts/eval_compare.py): compare N eval reports across
  versions or variants.
- [scripts/rubric_schema.yaml](../scripts/rubric_schema.yaml): canonical
  machine-readable schema for the 18 dimensions, the five groups, allowed score values,
  and `NA`-eligible dimensions.

## Recommended Frontmatter Schema

For practical-prose documents (the artifacts being written and evaluated, not the eval
reports themselves), the following frontmatter fields help agents apply the guidelines
consistently. Required fields are minimum viable; recommended fields make the document
agent-evaluable; optional fields apply when their condition is relevant.

| Field | Status | Type | Meaning |
| --- | --- | --- | --- |
| `title` | Required | string | Display title. |
| `description` | Required | string | One-sentence summary of what the document does for the reader. |
| `date` | Required | ISO date | Creation date; never silently overwritten. |
| `status` | Required | enum | `draft`, `active`, `archived`, `deprecated`. |
| `purpose` | Recommended | string | What reader need this serves (decision, plan, audit, runbook, reference). Cross-checks §1 Suitability. |
| `audience` | Recommended | string | Intended reader (role, expertise level, agent vs human). |
| `scope` | Recommended | string | One-sentence statement of what is in scope. Cross-checks §2 Scope. |
| `out_of_scope` | Optional | string or list | Explicit out-of-scope items when the boundary is non-obvious. |
| `owner` | Recommended | string | Maintainer or accountable role. Cross-checks §7 Concision (frontmatter holds machine-readable metadata) and the Maintainable principle. |
| `last_reviewed` | Recommended | ISO date | Date the document was last reviewed end-to-end. Useful for staleness alerts. |
| `risk_level` | Recommended | enum | `low`, `standard`, `high`. Drives audit-pass requirements: high-stakes docs require the four-pass review (see [rubric](practical-prose-rubric.md) audit-passes section); standard docs run the two-pass; low-stakes drafts may use a single pass. |
| `source_policy` | Optional | enum | `primary-required`, `secondary-ok`, `internal-only`. Sets the strictness for §11 Verifiability. |
| `update_triggers` | Optional | list | Events that should prompt re-review (release cuts, regulatory changes, dependency upgrades). |
| `evaluation_mode` | Optional | enum | `self`, `external`, `tooling-only`. Records whether the rubric is being applied by the author, by an external reviewer, or by deterministic tooling only. Cross-checks the rubric’s self-eval-overrate note. |
| `rubric_version` | Required for eval YAMLs | string | Pinned rubric revision (e.g., `18-dim-v1`). Set automatically by `eval_report.py from-metrics`. Not required on the underlying artifact. |

Minimum agent-evaluable set: `title`, `description`, `date`, `status`, `purpose`,
`audience`, `scope`, `owner`, `last_reviewed`, `risk_level`.

Documents without explicit `risk_level` are treated as `standard` for review purposes.
Documents without `last_reviewed` are treated as “last reviewed at `date`” until proven
otherwise.

## Applicability Profiles

The full 18-dimension rubric is sized for high-stakes documents (decision memos, audits,
deep research). Applying it uniformly to a short status note produces performative-rigor
failure: more scoring, less reader value.
The profiles below tell agents and reviewers which dimensions are *required*,
*conditional*, or *typically NA* based on the artifact’s `risk_level` and doc type.
`risk_level` in frontmatter is the primary switch.

| Profile | `risk_level` | Required dimensions | Conditional dimensions | Typically NA |
| --- | --- | --- | --- | --- |
| **Low-stakes note** (status update, standup, brief progress note) | `low` | §1 Suitability, §5 Clarity, §7 Concision, §10 Formatting | §11 Verifiability only for material claims | §13-§18 (Inference Discipline, Soundness, Precision, Calibration, Fairness, Robustness) |
| **Standard internal doc** (memo, brief, internal report) | `standard` | All Purpose (§1-§4); all Expression (§5-§10); §11 Verifiability; §12 Factuality; §14 Soundness | §13 Inference Discipline, §16 Calibration, §17 Fairness, §18 Robustness when the doc makes those kinds of claims | §15 Precision unless terminology is contested |
| **Decision memo / audit / deep research** | `high` | All 18 unless explicitly NA | Four-pass audit (lint / claim / reasoning / purpose; see [rubric](practical-prose-rubric.md) §Audit passes for high-stakes evals) | None by default; NA only when explicitly stated and justified |
| **Reference / runbook** | `standard` (override) | §1 Suitability, §2 Scope, §8 Organization, §10 Formatting, §15 Precision; plus the Maintainable principle | §11-§12 if the reference makes verifiable claims; §6 Coherence on extended explanations | §17 Fairness, §18 Robustness unless interpretive claims appear |

Two operational notes:

- **Default is Standard.** When in doubt, score the Standard profile.
  Promoting a document to High requires high-stakes content (binding decisions, audits,
  external research) or an explicit `risk_level: high` setting.
- **NA is honest, not lazy.** A reference doc with no probability claims should mark §16
  Calibration NA, not score it 0; aggregating zeros for genuinely-not-applicable
  dimensions punishes the profile rather than the document.

The profiles do not override the alignment property: any score 1-4 still requires a
matching violation citation under that dimension.
They only tell the reviewer which dimensions to engage at all.

## How metrics interact with the rubric

Quantitative metrics are not scores.
A banned-register hit is a candidate flag, not a §5 Clarity violation: the reviewer may
accept the hit if the word is earned by an inline citation.
A `[VERIFIED]` tag without a paired source pointer is a §11 Verifiability flag, not a
hard fail: the reviewer may accept if the source is in the surrounding paragraph.

The lint pass uses metrics to catch defects deterministically.
The remaining three passes (claim audit, reasoning audit, purpose audit) use judgment
that metrics cannot substitute for.
See the *Audit passes for high-stakes evals* section in
[practical-prose-rubric.md](practical-prose-rubric.md).

## Related Docs

- [../README.md](../README.md): how the practical-prose layers fit together.
- [practical-prose-rubric.md](practical-prose-rubric.md): descriptive 0-5 scoring
  anchors. The metrics here serve the rubric; the rubric serves judgment.
- [practical-prose-guidelines.md](practical-prose-guidelines.md): prescriptive rules
  these metrics flag against.
- [../scripts/practical_prose_metrics.py](../scripts/practical_prose_metrics.py): the
  deterministic metrics script.
- [../runbooks/practical-prose-eval-single.runbook.md](../runbooks/practical-prose-eval-single.runbook.md):
  end-to-end single-document eval procedure.

<!-- This document follows common-doc-guidelines.md.
Review guidelines before editing.
-->
