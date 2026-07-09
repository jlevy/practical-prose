---
title: Practical Prose Metrics and Frontmatter
description: Operational appendix to the practical-prose system; maps each of the 20 review dimensions to quantitative metrics and qualitative checks, and documents the recommended frontmatter schema for practical-prose documents.
date: 2026-05-11
status: active
---
# Practical Prose Metrics and Frontmatter

Version: v0.1 (last update 2026-06-12)\
Joshua Levy (github.com/jlevy) with agent assistance

An operational appendix to the practical-prose system.
The rubric (`pprose guidelines practical-prose-rubric`) is the descriptive 1-5 instrument; this doc
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
check. *“Tooling”* names the operational tool today; **`pprose metrics`** is the
deterministic metrics command, **`pprose score`** runs an LLM scorer against the rubric,
and **manual** denotes a human reviewer.

| § | Dimension | Quantitative metric(s) | Qualitative check | Tooling |
| ---: | --- | --- | --- | --- |
| 1 | Suitability | Presence of explicit `purpose`, `audience`, `scope` fields (frontmatter); presence of recommendation/findings/milestones section by doc type | Can a target reader say what the doc is for after 30 seconds? | frontmatter check; manual skim test |
| 2 | Scope | Presence of `scope` and optionally `out_of_scope` fields; count of headings outside declared scope | Does the body honor the declared boundary? | frontmatter check; manual |
| 3 | Breadth | Count of relevant case classes addressed (out of a domain-specific expected set) | Are the obvious affected areas covered? | manual; SME |
| 4 | Depth | Count of vague magnitude words (“rapid,” “large”) not paired with quantification; count of endpoints cited where a series exists | Is section depth proportional to section importance? | manual; LLM-assist |
| 5 | Clarity | Banned-register hits (count and examples; full common-doc-guidelines §4.2 list); pedantic-marker hits (canonicality declarations, word-choice justifications, reading-order instructions); vague-word hits; sentence length distribution; mean and p95 sentence length | Does prose read cleanly aloud; is the document free of self-referential pedantry? | `pprose metrics` (banned-register and pedantic-marker hits); manual for the rest |
| 6 | Coherence | Paragraph length distribution; presence of stub transitions (“As shown above” without recap) | Does each paragraph have one job; do transitions bridge? | manual; LLM-assist |
| 7 | Concision | Word count vs target by doc type; repeated n-gram count; low-information paragraph flag; replacement-history phrase hits (regex set: “previously named,” “formerly,” “under the new layout,” “removed,” etc.) | Does removing a section lose information; is replacement history absent outside history-genre exceptions? | `pprose metrics` words/paragraphs; manual cut test |
| 8 | Organization | Heading-level skip count (h1→h3 without h2); generic-heading hits (“Overview,” “Background,” “Notes,” “Details”); table count and column densities; figure-caption presence; link-target stability (no commit-less URLs to mutable refs) | Are sections sequenced for the task; do tables earn their tabular shape; do headings cleave to subject contours? | `pprose metrics` headings/tables; manual |
| 9 | Consistency | Acronym casing variance; dialect mixing; date-format variance; parallel-list violations; spaced em-dash count and em-dash density per 1000 words | Does the document follow the chosen style guide; are em dashes used sparingly and in American style? | linter; manual |
| 10 | Formatting | Markdown lint pass/fail; frontmatter present and valid; footer present | Renders correctly across mediums? | flowmark / md-lint; `pprose metrics` footnote round-trip |
| 11 | Discipline | Rung-tag count (`[observed]`, `[judged]`, `[interpreted]`, `[implied]`) in audit/eval modes; multi-rung-per-sentence flag | Are observation, judgment, interpretation, and implication worked through in order, each higher rung supported by the prior? | `pprose metrics` bracket tags (audit mode); LLM-assist; manual |
| 12 | Soundness | `[ASSUMING:]` tag count where assumptions are load-bearing; count of unbridged “signal → outcome” leaps | Are mechanisms named where causation is asserted; is counter-evidence engaged? | `pprose metrics` bracket tags; manual / SME |
| 13 | Precision | Vague-countable hits (“several,” “various,” “many”); umbrella-term hits (“users,” “latency”) where domain sub-distinctions matter | Is the most specific term the audience can parse used throughout? | banned-register / linter extension; manual |
| 14 | Parsimony | Count of chains where a shorter sound chain exists (citable fact re-derived without adding inspectability or confidence; weaker warrant where a stronger one is available); count of non-load-bearing rungs flagged within load-bearing chains; per-doc parsimony-gap flag count | For each load-bearing chain, is it the minimum sufficient given its purpose and per-step warrants? | LLM-assist; manual |
| 15 | Verifiability | % quantitative claims with source pointer; bracket-tag count by type (`[VERIFIED]`, `[UNVERIFIED]`, `[ESTIMATED]`, `[DERIVED:]`, `[ASSUMING:]`); footnote/citation count | Can a competent reader trace claims to evidence without external lookup? | `pprose metrics` bracket tags and footnotes; manual claim audit |
| 16 | Factuality | Broken-link rate; stale-source count; numeric discrepancies vs cited source | Do cited sources actually support the claim at the asserted strength? | link checker; manual / SME audit |
| 17 | Relevance | Count of cited sources flagged as ancillary or tangential to the document’s purpose; count of sections marked as digression/background that load-bear on a headline claim (mislabel); count of unmarked digressions exceeding the length threshold for the doc type | For each source and each section, does it bear on the document’s stated purpose? | LLM-assist; manual |
| 18 | Calibration | Count of probability claims; count of those with cited base rate; small-sample shrinkage explicit; scenario probabilities sum check | Does claim strength match evidence strength? | LLM-assist; manual |
| 19 | Fairness | Opposing-vs-supporting paragraph count *(flag only; see note below)*; depth asymmetry ratio; risk-inventory class coverage | Are opposing positions argued at depth proportional to their plausibility, materiality, and strength? | LLM-assist; manual / SME |
| 20 | Robustness | Count of explicit interpretive-lens statements; count of alternative-lens tests | Do key claims survive plausible alternative interpretations? | manual; LLM-assist |

Most rows have a deterministic component and a judgment component.
The deterministic component runs in CI and catches regressions cheaply; the judgment
component runs at review time and catches substantive failures the lint will never
notice. Where a row lists several quantitative metrics, `pprose metrics` computes only
the subset named in the *Tooling Map* below; the rest are review-time checks (some are
tracked for the planned `pprose lint`).

**Note on J2 Fairness.** The opposing-vs-supporting paragraph count and depth-ratio
metrics are review flags, not measures of fairness.
The guidelines define fairness as proportional representation by plausibility,
materiality, and evidence strength (J2.1), not equal airtime.
Symmetric paragraph counts can be a sign of false balance, not fairness; treat the count
as a prompt to inspect the underlying evidence, never as proof that the document is
fair.

## Tooling Map

- `pprose metrics`: the deterministic metrics command.
  Computes headings by depth, link counts (external/internal, by markdown form),
  footnote references and definitions, bracket-tag counts and examples (ALL-CAPS forms
  like `[VERIFIED]`; lowercase rung tags and colon-suffixed forms like `[ASSUMING: ...]`
  are not counted), bare URLs, tables, code blocks, banned-register hits (the
  common-doc-guidelines §4.2 list plus `dominant`, an advocacy-register extension;
  override the whole list with `--banned-words-file`), word/sentence/paragraph/line
  counts, and page estimate.
- `pprose score`: LLM-based rubric scorer.
- `pprose report`: creates, validates, and recomputes eval reports (combining metrics
  and scores).
- `pprose compare`: compare N eval reports across versions or variants.
- [rubric_schema.yaml](https://github.com/jlevy/practical-prose/blob/main/tools/pprose/src/pprose/rubric_schema.yaml): canonical
  machine-readable schema for the 20 dimensions, the six groups, allowed score values,
  and `NA`-eligible dimensions.

> Note: `pprose metrics` reports more lint signals than the eval report carries.
> The replacement-history, pedantic-marker, generic-heading, and em-dash-density lints
> (and bracket-tag examples) appear in `pprose metrics` output but are intentionally
> **not** copied into the eval report’s `quant` block, so `pprose report` /
> `pprose compare` never surface them.
> Run `pprose metrics` directly to see the full lint set.

## Recommended Frontmatter Schema

For practical-prose documents (the artifacts being written and evaluated, not the eval
reports themselves), the following frontmatter fields help agents apply the guidelines
consistently. Required fields are minimum viable; recommended fields make the document
agent-evaluable; optional fields apply when their condition is relevant.

This repo’s own reference docs, shortcuts, and runbooks carry at least the required four
fields. Repo-root operational files (README.md, TODO.md, SUPPLY-CHAIN-SECURITY.md,
AGENTS.md) are exempt: GitHub renders README frontmatter as a literal table, and
AGENTS.md is partly generated; those files carry a version byline or rely on git
metadata instead.

| Field | Status | Type | Meaning |
| --- | --- | --- | --- |
| `title` | Required | string | Display title. |
| `description` | Required | string | One-sentence summary of what the document does for the reader. |
| `date` | Required | ISO date | Creation date; never silently overwritten. |
| `status` | Required | enum | `draft`, `active`, `archived`, `deprecated`. |
| `purpose` | Recommended | string | What reader need this serves (decision, plan, audit, runbook, reference). Cross-checks P1 Suitability. |
| `audience` | Recommended | string | Intended reader (role, expertise level, agent vs human). |
| `scope` | Recommended | string | One-sentence statement of what is in scope. Cross-checks P2 Scope. |
| `out_of_scope` | Optional | string or list | Explicit out-of-scope items when the boundary is non-obvious. |
| `owner` | Recommended | string | Maintainer or accountable role. Cross-checks E3 Concision (frontmatter holds machine-readable metadata) and the Maintainable principle. |
| `last_reviewed` | Recommended | ISO date | Date the document was last reviewed end-to-end. Useful for staleness alerts. |
| `risk_level` | Recommended | enum | `low`, `standard`, `high`. Drives audit-pass requirements: high-stakes docs require the four-pass review (see rubric (`pprose guidelines practical-prose-rubric`) audit-passes section); standard docs run the two-pass; low-stakes drafts may use a single pass. |
| `source_policy` | Optional | enum | `primary-required`, `secondary-ok`, `internal-only`. Sets the strictness for G1 Verifiability. |
| `update_triggers` | Optional | list | Events that should prompt re-review (release cuts, regulatory changes, dependency upgrades). |
| `evaluation_mode` | Optional | enum | `self`, `external`, `tooling-only`. Records whether the rubric is being applied by the author, by an external reviewer, or by deterministic tooling only. Cross-checks the rubric’s self-eval-overrate note. |
| `rubric_version` | Required for eval YAMLs | string | Pinned rubric revision (e.g., `pp20v1`). Set automatically by `pprose report from-metrics`. Not required on the underlying artifact. |

Minimum agent-evaluable set: `title`, `description`, `date`, `status`, `purpose`,
`audience`, `scope`, `owner`, `last_reviewed`, `risk_level`.

Documents without explicit `risk_level` are treated as `standard` for review purposes.
Documents without `last_reviewed` are treated as “last reviewed at `date`” until proven
otherwise.

## Applicability Profiles

The full 20-dimension rubric is sized for high-stakes documents (decision memos, audits,
deep research). Applying it uniformly to a short status note produces performative-rigor
failure: more scoring, less reader value.
The profiles below tell agents and reviewers which dimensions are *required*,
*conditional*, or *typically NA* based on the artifact’s `risk_level` and doc type.
`risk_level` in frontmatter is the primary switch.

| Profile | `risk_level` | Required dimensions | Conditional dimensions | Typically NA |
| --- | --- | --- | --- | --- |
| **Low-stakes note** (status update, standup, brief progress note) | `low` | P1 Suitability, E1 Clarity, E3 Concision, F3 Formatting | G1 Verifiability only for material claims | G3 Relevance, R1-R4 (Discipline, Soundness, Precision, Parsimony), J1-J3 (Calibration, Fairness, Robustness) |
| **Standard internal doc** (memo, brief, internal report) | `standard` | All Purpose (P1-P4); all Expression (E1-E3); all Form (F1-F3); G1 Verifiability; G2 Factuality; R2 Soundness | G3 Relevance, R1 Discipline, R4 Parsimony, J1 Calibration, J2 Fairness, J3 Robustness when the doc makes those kinds of claims | R3 Precision unless terminology is contested |
| **Decision memo / audit / deep research** | `high` | All 20 unless explicitly NA | Four-pass audit (lint / claim / reasoning / purpose; see rubric (`pprose guidelines practical-prose-rubric`) §Audit Passes for High-Stakes Evals) | None by default; NA only when explicitly stated and justified |
| **Reference / runbook** | `standard` (override) | P1 Suitability, P2 Scope, F1 Organization, F3 Formatting, R3 Precision; plus the Maintainable principle | G1-G3 if the reference cites sources or makes verifiable claims; E2 Coherence on extended explanations | J2 Fairness, J3 Robustness unless interpretive claims appear |

Two operational notes:

- **Default is Standard.** When in doubt, score the Standard profile.
  Promoting a document to High requires high-stakes content (binding decisions, audits,
  external research) or an explicit `risk_level: high` setting.
- **NA is honest, not lazy.** A reference doc with no probability claims should mark J1
  Calibration NA, not force a numeric score; NA dimensions are excluded from any mean,
  so genuinely-not-applicable dimensions never drag down the rollup.

The profiles do not override the alignment property: any score 1-4 still requires a
matching violation citation under that dimension.
They only tell the reviewer which dimensions to engage at all.

## How Metrics Interact with the Rubric

Quantitative metrics are not scores.
A banned-register hit is a candidate flag, not an E1 Clarity violation: the reviewer may
accept the hit if the word is earned by an inline citation.
A `[VERIFIED]` tag without a paired source pointer is a G1 Verifiability flag, not a
hard fail: the reviewer may accept if the source is in the surrounding paragraph.

The lint pass uses metrics to catch defects deterministically.
The remaining three passes (claim audit, reasoning audit, purpose audit) use judgment
that metrics cannot substitute for.
See the *Audit Passes for High-Stakes Evals* section in
`pprose guidelines practical-prose-rubric`.

## Related Docs

- ../README.md (`pprose about`): how the practical-prose layers fit together.
- `pprose guidelines practical-prose-rubric`: descriptive 1-5 scoring
  anchors. The metrics here serve the rubric; the rubric serves judgment.
- `pprose guidelines practical-prose-guidelines`: prescriptive rules
  these metrics flag against.
- ../runbooks/practical-prose-eval-single.runbook.md (`pprose runbook practical-prose-eval-single`):
  end-to-end single-document eval procedure.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
