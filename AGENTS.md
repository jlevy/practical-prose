# Practical Prose: Agent Guide

Practical Prose is a reference system and evaluation toolkit for writing that helps a
reader understand, decide, do, verify, or maintain something. Use it when the user asks
to improve, audit, score, or compare practical documents.

Keep this file short. Load the skill or source document for the specific workflow rather
than copying the full guidelines into every context.

## Workflows

| User intent | Use | Source |
| --- | --- | --- |
| Apply the common Markdown documentation standards (basic, universal) | [prose-common-edit](skills/prose-common-edit/SKILL.md) | [common-doc-guidelines.md](docs/common-doc-guidelines.md) |
| Copy edit for language and formatting (the Expression dimensions) | [prose-copy-edit](skills/prose-copy-edit/SKILL.md) | [shortcut-copy-edit.md](shortcuts/shortcut-copy-edit.md) |
| Full editorial pass across all 20 dimensions + editorial review (also covers audit-only review) | [prose-full-edit](skills/prose-full-edit/SKILL.md) | [shortcut-full-edit.md](shortcuts/shortcut-full-edit.md) |
| Score one document with metrics and rubric grading | [prose-eval](skills/prose-eval/SKILL.md) | [practical-prose-eval-single.runbook.md](runbooks/practical-prose-eval-single.runbook.md) |
| Compare multiple evaluated drafts or variants | [prose-compare](skills/prose-compare/SKILL.md) | [practical-prose-eval-compare.runbook.md](runbooks/practical-prose-eval-compare.runbook.md) |

## Authoring Principles

When generating, summarizing, or rewriting practical prose:

1. Answer the reader's task and make the main output recoverable from a skim.
2. State scope and claim boundaries early.
3. Make material claims traceable to sources, calculations, or explicit assumptions.
4. Keep evidence, inference, and recommendation distinct.
5. Use concrete language and the most specific terms the reader can parse.
6. Cut visible rigor that does not improve inspectability, accuracy, usefulness, or
   reader trust.
7. Apply fairness and robustness only when the task involves disputed or interpretive
   claims.
8. Mark unknowns instead of inventing support.

When a local rule conflicts with the reader outcome, document the justified deviation:
which rule is set aside, what reader outcome it serves, and what risk it introduces.

## Tooling

The Python eval package lives in `tools/pprose/`.
After publication, use the package through the single command:

```bash
uvx pprose <command> ...
```

**Evaluate** (action): `pprose metrics`, `pprose report`, `pprose score`, `pprose compare`.

**Reference** (print bundled docs the agent follows; `--list` to enumerate):
`pprose guidelines <name>`, `pprose shortcut <name>`, `pprose runbook <name>`,
`pprose skill <name>`. The guidelines, shortcuts, runbooks, and rubric are bundled in the
wheel, so these work in any repo without this source tree.

**Setup**: `pprose install` writes the five Practical Prose skills into a repo's
`.claude/skills/`. The generated skills reference `pprose` with a pinned, local-first
invocation: `pprose` if on PATH, else `uvx pprose@<version>` (the version that ran
install — a trusted pin, never an unpinned runner), else they tell the user to install
uv or pprose.

For local development before publication, run from the package workspace:

```bash
cd tools/pprose
uv run pprose <command> ...
```

`score` requires `ANTHROPIC_API_KEY`; the package auto-loads `.env` and `.env.local`
from the current directory hierarchy and `$HOME`.
