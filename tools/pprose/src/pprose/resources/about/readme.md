# Practical Prose

Joshua Levy (github.com/jlevy) with agent assistance

## What is This Project?

Clear writing and clear thinking are inseparable.
A document is an instrument by which thought becomes visible, testable, and useful.

This project is an attempt at assembling principles, guidelines, and tools to improve
the quality of practical writing by humans and by agents.

The goal is not just to add polish but to improve thinking as expressed in language.

The documents and tools here are organized so humans and agents can use them.
Agents can use the principles and guidelines in any project when they are creating
documents. Or the skills and evaluation framework can help agents in supporting humans
review documents for quality or improve what they write.

## Scope

The focus here is **practical prose**: writing that helps a reader—human or
agent—understand, decide, do, or verify something.
Practical prose includes technical documents, research reports, specifications, memos,
plans, and other artifacts where value depends on usefulness.

The aim is not consistency for its own sake but to encourage prose where the form,
practial utility, and human fit the work to be done.

Three key points:

- The focus is on practical writing, which means many elements do not apply to creative
  writing, personal essays, fiction, or other writing where the primary goals are
  expressive or creative.

- We focus only on English.
  In the future this, could be extended to other languages.
  With the help of sensitive native speakers and increasingly powerful AI translations,
  it’s likely we could adapt them to other languages effectively while preserving the
  nuances specific to each language.

- However, the focus on utility does not mean rejecting the needs of human readers.
  Good prose serves human needs and reflects human qualities.
  Usefulness is not in opposition to style, beauty, or human expression.
  The best practical writing often joins the classic virtues of structure, precision,
  and evidence with the romantic virtues of voice, rhythm, and feeling.

## What is Here?

1. Guiding **principles** for quality in practical writing
2. Metrics of writing quality that include **6 areas of quality** divided into **20
   dimensions**
3. An **evaluation rubric** on how to evaluate text according to these dimensions
4. An automated **visualization tool** that uses an LLM to assess quality and visualize
   it
5. **Skills** that use **a CLI** to package these features
6. A **bibliography** of notable works on practical writing

## A Personal Note

As a reader, I’ve always admired good writing, both fiction and nonfiction.
As a writer, editor, and publisher, I’ve spent years thinking about editorial processes.
As a engineer and designer, I’ve built tools print and digital publishing.

Now I use agents to write millions of lines of code and documents each month, including
software documentation, technical specifications, and business or financial analsysis.

I am in a perpetual state of amazement both at how the latest models can be both
incredibly capable yet write and think in such sloppy ways.
LLMs tend toward mediocrity because they tend to write “in distribution” of the training
data. But just as with human writers, many shortcomings are correctable errors or bad
habits.

So many of the challenges in working with AI involve improving the quality of thinking
of both the agents and the people who oversee the work.

I think at its best, AI does not replace but rather augments human intellect.
Sometimes human traditions diverge by historical accident.
But agents let us combine insights from many sources.
I’ve tried to draw from the best thinkers and sources, such as writing classics, the
plain-language writing tradition, science and engineering writing, and journalistic
practices.

You can now outsource writing and thinking to agents.
But you can’t outsource your understanding or your judgement.

## Practical Writing in the Age of AI

Technical writers and editors have known for centuries that the best way to validate
written ideas is through disciplined editorial review.
Evidence can be checked, reasoning can be inspected, uncertainty can be calibrated.
By enforcing standards for quality writing, we think more clearly.

What is now different is that language is now drafted, transformed, summarized, and
evaluated by LLMs in greater volume than by humans.
In many professional and technical domains, documents are increasingly written in mostly
two ways:

- humans writing with agent review or assistance
- agents writing with human oversight

As we all know, poor quality AI writing is everywhere.
Slop and spam are not just distateful; they are often inaccurate or even harmfully
misleading.

Fluency is cheap. Judgment remains precious.

There is not enough human attention for the job of filtering and editing AI slop.
By codifying standards for quality, we can not only help humans write better but help
machines assist us in thinking and writing clearly.
Evidence can be checked, reasoning can be inspected, uncertainty can be calibrated.
As technical writers and editors have known for centuries, the best way to validate
written ideas is through disciplined editorial review.

## Quick Start

Use the Practical Prose CLI in any repo with [uv](https://docs.astral.sh/uv/):

```bash
uvx pprose --help
uvx pprose install
```

The package name and command are both `pprose`. `pprose install` writes one `SKILL.md`
per workflow into both `.agents/skills/` (Codex, Gemini CLI, pi read this natively) and
`.claude/skills/` (Claude Code mirror), and maintains a marker-bounded `pprose` block in
`AGENTS.md` (preserving any other content).
Re-running it is idempotent, and `--claude` / `--codex` / `--skip-claude` /
`--skip-codex` target specific surfaces.

## Principles of Quality in Practical Writing

Entire books have been written on what “quality” really is.
For our purposes, quality is fit: the parts of a document work when purpose, truth,
form, evidence, language, and reader needs support the same task.

The seven principles below decompose that fit into specific attributes.

| # | Principle | One-line definition |
| --- | --- | --- |
| 1 | **Purposeful** | The document’s content, form, order, depth, and output shape fit the reader’s needs or tasks. |
| 2 | **Truthful** | The claims are accurate based on the sources and uncertainty is accurately expressed. |
| 3 | **Essential** | The work surfaces necessary details and complexity and omits anything not relevant. |
| 4 | **Lucid** | The language and presentation help a reader orient themselves and understand the material. |
| 5 | **Verifiable** | The claims trace to verifiable sources, observations, calculations, or explicit assumptions. |
| 6 | **Maintainable** | The work is organized in a way that is maintainable for its intended shelf life and workflows. |
| 7 | **Humane** | The document respects the human reader, is understandable by humans, and serves human needs. |

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

The system has six reference layers and two operational layers.
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

1. **Recommended** — let `pprose install` set up every supported surface in any repo:
   `uvx pprose install` writes one `SKILL.md` per workflow into both `.agents/skills/`
   (Codex, Gemini CLI, pi) and `.claude/skills/` (Claude Code), and maintains a
   marker-bounded `pprose` block in `AGENTS.md`.
2. Point the agent at *this* repo and let `AGENTS.md` route to the right skill — the
   committed `skills/<name>/SKILL.md` files are version-pinned discovery copies that
   work as a `npx skills add` / skills.sh landing page.
3. If a Claude Code plugin marketplace entry exists, install that as a Claude-only
   convenience.

The skills are intentionally small routers: each names the workflow once and points at
`pprose <command>` / `pprose guidelines <name>` / `pprose shortcut <name>` rather than
duplicating that content.
The `pprose` CLI bundles the guidelines, shortcuts, runbooks, and rubric inside its
wheel, so an installed skill works in any repo with no other files present.

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
`pprose install` writes the five Practical Prose skills into both `.agents/skills/` and
`.claude/skills/`, plus a marker-bounded block in `AGENTS.md`. Every generated artifact
carries a `format=fNN surface=…` stamp, so re-running install is idempotent and a
newer-format artifact is never clobbered by an older pprose.
Each generated skill references pprose with a pinned, local-first invocation (`pprose`
if on PATH, else `uvx pprose@<version>`—the trusted version that ran install—else a
message telling the user to install uv or pprose).

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
