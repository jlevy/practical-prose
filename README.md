# Practical Prose

Joshua Levy (github.com/jlevy) with agent assistance

## Quick Start

After the package is published, use the Practical Prose CLI in any repo with
[uv](https://docs.astral.sh/uv/):

```bash
uvx pprose --help
uvx pprose install --agents-md
```

The package name and command are both `pprose`. `pprose install` writes portable agent
skills into `.claude/skills/`; `--agents-md` also adds a short routing block to
`AGENTS.md` when a repo uses that file.

## Why Practical Prose Matters

Clear writing and clear thinking are inseparable.
A document is an instrument by which thought becomes visible, testable, and useful.

Good prose serves human needs and reflects human qualities.
Usefulness is not in opposition to style, beauty, or human expression.
The best practical writing often joins the classic virtues of structure, precision, and
evidence with the romantic virtues of voice, rhythm, and feeling.

**Practical prose** is writing that helps a reader—human or agent—understand, decide,
do, or verify something.
It includes technical documents, research reports, specifications, memos, essays of
practical analysis, operational plans, and all other artifacts where value depends on
usefulness.

## Practical Writing in the Age of AI

The rise of AI makes the need to focus on quality more acute.
Language is now drafted, transformed, summarized, and evaluated by LLMs in greater
volume than by humans.

Fluency is cheap. Judgment remains precious.

There is not enough human attention for the job of filtering and editing AI slop.
By codifying standards for quality, we can not only help humans remember how to write
clearly but help machines assist us in the process.
Evidence can be checked, reasoning can be inspected, uncertainty can be calibrated.
As technical writers and editors have known for centuries, the best way to validate
written ideas is through disciplined editorial review.

## What is This Project?

The Practical Prose project aims to improve practical writing in several ways:

1. **Principles** for improving the quality of practical writing
2. **Guidelines** with normative advice
3. **Tooling** and a **rubric** to help humans and agents evaluate quality consistently
4. A **bibliography** of notable works on practical writing

These are intended for humans and for AI systems.

These tools also aim to serve a higher goal: a durable standard for practical thought
expressed in language.
The documents in this repository attempt to reunite traditions that are too often
separated. From plain-language writers we inherit economy, directness, and respect for
the reader’s time. From scientists and engineers we inherit accuracy, mechanism,
calibration, and reproducibility.
From journalists and historians we inherit verification, proportion, and fairness.
From literary writers we inherit attention to language, structure, narrative, and the
human force of a sentence.
From technical communicators we inherit maintainability, usability, and documents that
work as part of larger systems.

This project focuses on English practical prose.
But its principles—purpose, truth, proportion, verifiability, maintainability, respect
for the reader—are deeper than any one language.
With the help of sensitive native speakers and increasingly powerful AI translations,
it’s likely we could adapt them to other languages effectively while preserving nuances
common to each language.

The aim of standards is not simply to follow rules but to promote quality in service of
a purpose: prose where form, evidence, reasoning, and human effect fit the work to be
done.

## Principles of Quality in Practical Writing

Quality is fit: the parts of a document work when purpose, truth, form, evidence,
language, and reader need support the same task.

A clear sentence can still mislead; a cited claim can still overstate the evidence; a
well-organized document can still fail if it does not help the reader do the needed
work.

The seven principles below decompose that fit into specific attributes.

| # | Principle | One-line definition |
| --- | --- | --- |
| 1 | **Purposeful** | The document’s content, form, order, depth, and output shape fit the reader’s task. |
| 2 | **Truthful** | Claims are accurate, source-supported, framed at the right strength, and stated so they can be checked or refuted. |
| 3 | **Essential** | Surface the necessary detail and complexity; remove everything else. |
| 4 | **Lucid** | Argument and language help a reader who hasn’t done the work follow the spine. |
| 5 | **Verifiable** | Claims trace to sources, observations, calculations, or explicit assumptions, cited specifically enough to find the passage. |
| 6 | **Maintainable** | Organized for the shelf life and update workflow the document needs. |
| 7 | **Humane** | The document respects the human reader and serves human needs. |

## Qualitative Measures of Writing

Principles are of value, but when an editor evaluates a piece of writing, they are
looking at specific qualities or dimensions.

| Area | Dimension | Question |
| --- | --- | --- |
| **Purpose** | P1. Suitability | Does the document give the reader what they need, in the form the task requires? |
|  | P2. Scope | Is the scope stated, and does it fit the actual scope of the work? |
|  | P3. Breadth | Are the relevant areas within scope covered? |
|  | P4. Depth | Are the important areas developed enough? |
| **Expression** | E1. Clarity | Does the writing read well? |
|  | E2. Coherence | Do the ideas progress smoothly? |
|  | E3. Concision | Does every section earn its place? |
| **Form** | F1. Organization | Are sections, headings, sequence, tables, figures, links, and cross-references arranged for navigation? |
|  | F2. Consistency | Does the document follow the chosen style guide or house style consistently? |
|  | F3. Formatting | Is the document visually and syntactically clean in its medium? |
| **Reasoning** | R1. Discipline | Are observation, judgment, interpretation, and implication worked through in order, with each higher rung supported by the prior? |
|  | R2. Soundness | Do claims follow from evidence through valid mechanisms? |
|  | R3. Precision | Are claims and terms specified at the right granularity? |
|  | R4. Parsimony | Is each load-bearing reasoning chain the cleanest, simplest sound argument possible for its conclusion? |
| **Grounding** | G1. Verifiability | Are claims traceable to sources or calculations? |
|  | G2. Factuality | Do cited sources support the claims as asserted? |
|  | G3. Relevance | Do sources, citations, and reasoning chains bear on the document’s stated purpose? |
| **Judgment** | J1. Calibration | Does claim strength match evidence strength? |
|  | J2. Fairness | Are opposing positions argued at proportional evidentiary depth? |
|  | J3. Robustness | Do key claims survive plausible alternative interpretations? |

Each dimension maps back to one or more principles in
[practical-prose-principles.md](docs/practical-prose-principles.md); prescriptive rules
live in [practical-prose-guidelines.md](docs/practical-prose-guidelines.md) and 0-5
scoring anchors in [practical-prose-rubric.md](docs/practical-prose-rubric.md).

## Layers

The system has five reference layers and two operational layers.
Each layer answers a different question.

| Layer | Doc | Answers |
| --- | --- | --- |
| **Common** | [common-doc-guidelines.md](docs/common-doc-guidelines.md) | What general document standards do all docs (practical or otherwise) follow? |
| **Principles** | [practical-prose-principles.md](docs/practical-prose-principles.md) | Why these rules: what seven principles do they descend from? |
| **Guidelines** | [practical-prose-guidelines.md](docs/practical-prose-guidelines.md) | What should the writer do: prescriptive rules for the 20 dimensions? |
| **Rubric** | [practical-prose-rubric.md](docs/practical-prose-rubric.md) | How is a document scored: descriptive 0-5 anchors for the same 20 dimensions? |
| **Bibliography** | [practical-prose-bibliography.md](docs/practical-prose-bibliography.md) | Where do these ideas come from: what works ground each tradition? |
| **Metrics** | [practical-prose-metrics.md](docs/practical-prose-metrics.md) | Which quantitative metrics and qualitative checks map to which dimensions; recommended frontmatter schema. |
| **Shortcut** | [practical-prose-quick-checklist.md](shortcuts/practical-prose-quick-checklist.md) | One-page pre-publish self-audit across the 20 dimensions. |
| **Runbook** | [runbooks/](runbooks/) | Operational steps for single-document evals and N-way comparisons. |

The Common layer is the base substrate.
`common-doc-guidelines.md` captures general organization, structure, style, and
formatting rules that apply to *any* document—technical docs, READMEs, internal memos,
specifications—not just practical prose.
The practical-prose layers (Principles, Guidelines, Rubric) build on top of it with the
seven principles and 20 dimensions specific to evaluating practical writing.
Principles, Guidelines, and Rubric form a tight triple: same seven principles, same 20
dimensions, same six groups (Purpose, Expression, Form, Reasoning, Grounding, Judgment).
The bibliography supplies the intellectual basis; the shortcuts and runbooks are how the
system gets used in practice.

## Where to Start

- **Writing a document and want the rules:**
  [practical-prose-guidelines.md](docs/practical-prose-guidelines.md).
- **Scoring a document and want the anchors:**
  [practical-prose-rubric.md](docs/practical-prose-rubric.md).
- **Running a pre-publish self-audit:**
  [practical-prose-quick-checklist.md](shortcuts/practical-prose-quick-checklist.md).
- **Running a formal eval:** the [runbooks/](runbooks/) directory.
- **Understanding why a rule exists:** the corresponding principle in
  [practical-prose-principles.md](docs/practical-prose-principles.md), and the source
  tradition in [practical-prose-bibliography.md](docs/practical-prose-bibliography.md).
- **Looking at the tooling:** [tools/pprose/](tools/pprose/) is the installable Python
  package with the metrics, scoring, and report generators.

## Agent Skills

This repo can be used directly by modern coding agents through `AGENTS.md` and portable
Agent Skills under [skills/](skills/). The eval skills use the
[`pprose` tooling](#tooling) described below.

| Skill | Kind | Use When |
| --- | --- | --- |
| [pprose-common-edit](skills/pprose-common-edit/SKILL.md) | Apply | Tidy, clean up, conform, fix formatting/structure, or add the documentation footer. The basic, universal tier. |
| [pprose-copy-edit](skills/pprose-copy-edit/SKILL.md) | Apply | Copy edit, proofread, polish, tighten, or line edit — language and formatting (Expression). Superset of common-edit. |
| [pprose-full-edit](skills/pprose-full-edit/SKILL.md) | Apply | Deep edit across all 20 dimensions; also writes an editorial review (strengths, weaknesses, suggested fixes). Superset of copy-edit; covers audit-only review. |
| [pprose-eval](skills/pprose-eval/SKILL.md) | Evaluate | Score, grade, rubric-check, or measure the quality of one document. |
| [pprose-compare](skills/pprose-compare/SKILL.md) | Evaluate | Compare drafts, A/B versions, quality-diff documents, or pick a best variant. |

Install paths:

1. Point the agent at this repo and let `AGENTS.md` route to the right skill.
2. Symlink `skills/*` into the agent’s skill directory.
   Claude Code can use the committed `.claude/skills/` symlinks.
3. If a Claude Code plugin marketplace entry exists, install that as a Claude-only
   convenience.

Do not copy only the `skills/*` directories into another location unless you also
preserve this repo’s sibling `docs/`, `shortcuts/`, and `runbooks/` layout or update the
relative links inside each `SKILL.md`. The skill files are intentionally small routers
into those canonical source documents.

## Tooling

[tools/pprose/](tools/pprose/) is a standalone modern-Python package (bootstrapped from
[`simple-modern-uv`](https://github.com/jlevy/simple-modern-uv)). The distribution and
console-script entry point are both `pprose`:

- `pprose metrics`: deterministic metrics over a document (banned-register hits,
  vague-word counts, link validity, frontmatter presence, etc.).
- `pprose score`: score a document against the rubric via the Anthropic SDK with prompt
  caching; supports `--batch` for parallel runs over N artifacts.
- `pprose report`: combine metrics and scores into an eval report; validate,
  compute-derived, and from-metrics subcommands.
- `pprose compare`: compare N eval reports across versions or variants.

It also bundles the guidelines, shortcuts, runbooks, and rubric and serves them as
reference subcommands (`pprose guidelines|shortcut|runbook|skill <name>`, `--list` to
enumerate), so the skills work in any repo.
`pprose install` writes the five Practical Prose skills into a repo’s `.claude/skills/`,
each referencing pprose with a pinned, local-first invocation (`pprose` if on PATH, else
`uvx pprose@<version>` — the trusted version that ran install — else a message telling
the user to install uv or pprose).

Quick start:

```bash
# Run with no install via uv (https://docs.astral.sh/uv/). `score` needs ANTHROPIC_API_KEY.
uvx pprose report from-metrics path/to/doc.md --label my-doc --scope-class brief --out my-doc.eval.md
uvx pprose score my-doc.eval.md
uvx pprose report validate my-doc.eval.md
```

See the runbooks for end-to-end operation and
[tools/pprose/docs/development.md](tools/pprose/docs/development.md) for local
development.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
