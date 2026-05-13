# Practical Prose

Joshua Levy (github.com/jlevy) with agent assistance

## Why Practical Prose Matters

Clear writing and clear thinking are inseparable.
A document is an instrument by which thought becomes visible, testable, and useful.

**Practical prose** is writing meant to help a reader—human or agent—understand, decide,
do, verify, or maintain something.
It includes technical documents, research reports, specifications, memos, essays of
practical analysis, operational plans, and all other artifacts whose value depends on
usefulness.

Good prose serves human needs and reflects human qualities.
Usefulness is not in opposition to style, beauty, or human expression.
The best practical writing joins the classic virtues of structure, precision, evidence,
and method with the romantic virtues of voice, proportion, rhythm, and felt meaning.

## Practical Writing in the Age of AI

The rise of AI makes the need to focus on quality more urgent than ever.
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
| **Purpose** | Suitability | Does the document give the reader what they need, in the form the task requires? |
|  | Scope | Is the scope stated, and does it fit the actual scope of the work? |
|  | Breadth | Are the relevant areas within scope covered? |
|  | Depth | Are the important areas developed enough? |
| **Expression** | Clarity | Does the writing read well? |
|  | Coherence | Do the ideas progress smoothly? |
|  | Concision | Does every section earn its place? |
|  | Organization | Are sections, headings, sequence, tables, figures, links, and cross-references arranged for navigation? |
|  | Style Consistency | Does the document follow the chosen style guide or house style consistently? |
|  | Formatting | Is the document visually and syntactically clean in its medium? |
| **Grounding** | Verifiability | Are claims traceable to sources or calculations? |
|  | Factuality | Do cited sources support the claims as asserted? |
| **Reasoning** | Inference Discipline | Are observation, judgment, interpretation, and implication kept distinct? |
|  | Soundness | Do claims follow from evidence through valid mechanisms? |
|  | Precision | Are claims and terms specified at the right granularity? |
| **Judgment** | Calibration | Does claim strength match evidence strength? |
|  | Fairness | Are opposing positions argued at proportional evidentiary depth? |
|  | Robustness | Do key claims survive plausible alternative interpretations? |

Each dimension maps back to one or more principles in
[practical-prose-principles.md](docs/practical-prose-principles.md); prescriptive rules
live in [practical-prose-guidelines.md](docs/practical-prose-guidelines.md) and 0-5
scoring anchors in [practical-prose-rubric.md](docs/practical-prose-rubric.md).

## Layers

The system has five reference layers and two operational layers.
Each layer answers a different question.

| Layer | Doc | Answers |
| --- | --- | --- |
| Common | [docs/common-doc-guidelines.md](docs/common-doc-guidelines.md) | What general document standards do all docs (practical or otherwise) follow? |
| Principles | [docs/practical-prose-principles.md](docs/practical-prose-principles.md) | Why these rules: what seven principles do they descend from? |
| Guidelines | [docs/practical-prose-guidelines.md](docs/practical-prose-guidelines.md) | What should the writer do: prescriptive rules for the 18 dimensions? |
| Rubric | [docs/practical-prose-rubric.md](docs/practical-prose-rubric.md) | How is a document scored: descriptive 0-5 anchors for the same 18 dimensions? |
| Bibliography | [docs/practical-prose-bibliography.md](docs/practical-prose-bibliography.md) | Where do these ideas come from: what works ground each tradition? |
| Metrics | [docs/practical-prose-metrics.md](docs/practical-prose-metrics.md) | Which quantitative metrics and qualitative checks map to which dimensions; recommended frontmatter schema. |
| Shortcut | [shortcuts/practical-prose-quick-checklist.md](shortcuts/practical-prose-quick-checklist.md) | One-page pre-publish self-audit across the 18 dimensions. |
| Runbook | [runbooks/](runbooks/) | Operational steps for single-document evals and N-way comparisons. |

The Common layer is the base substrate.
`common-doc-guidelines.md` captures general organization, structure, style, and
formatting rules that apply to *any* document (technical docs, READMEs, internal memos,
specifications), not just practical prose.
The practical-prose layers (Principles, Guidelines, Rubric) build on top of it with the
seven principles and 18 dimensions specific to evaluating practical writing.
Principles, Guidelines, and Rubric form a tight triple: same seven principles, same 18
dimensions, same five groups (Purpose, Expression, Grounding, Reasoning, Judgment).
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
- **Looking at the tooling:** [tools/prose-eval/](tools/prose-eval/) is the installable
  Python package with the metrics, scoring, and report generators.

## Tooling

[tools/prose-eval/](tools/prose-eval/) is a standalone modern-Python package
(bootstrapped from [`simple-modern-uv`](https://github.com/jlevy/simple-modern-uv)) that
installs four console-script entry points:

- `prose-metrics`: deterministic metrics over a document (banned-register hits,
  vague-word counts, link validity, frontmatter presence, etc.).
- `eval-score`: score a document against the rubric via the Anthropic SDK with prompt
  caching; supports `--batch` for parallel runs over N artifacts.
- `eval-report`: combine metrics and scores into an eval-report YAML; validate /
  compute-derived / from-metrics subcommands.
- `eval-compare`: compare N eval reports across versions or variants.

Quick start:

```bash
cd tools/prose-eval
make install
# Set ANTHROPIC_API_KEY in .env (loaded automatically by the entry points).
eval-report from-metrics path/to/doc.md --label my-doc --scope-class brief --out my-doc.eval.yaml
eval-score my-doc.eval.yaml
eval-report validate my-doc.eval.yaml
```

See the runbooks for end-to-end operation.

<!-- This document follows common-doc-guidelines.md.
Review guidelines before editing.
-->
