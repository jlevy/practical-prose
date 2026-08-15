---
type: is
id: is-01krhz2f5wsv5rwkvzz2c6mbaq
title: Run cross-agent skill validation
kind: task
status: closed
priority: 2
version: 6
spec_path: docs/project/specs/done/plan-2026-05-13-cross-agent-skills.md
labels:
  - cross-agent-skills
  - validation
dependencies: []
parent_id: is-01krhz0ckjzn0s26wggjjfays1
created_at: 2026-05-14T00:44:32.827Z
updated_at: 2026-08-15T05:51:02.794Z
closed_at: 2026-08-15T05:51:02.794Z
close_reason: "Cross-agent validation run against a clean wheel install (0.3.1.dev7+112ff1a) in an isolated HOME. Global install: 18 files, only under ~/.agents and ~/.claude, unrelated repo untouched, 4/4 relative links resolve, both self-contained skills runtime-free, 5 CLI-backed skills carry the 0.4.0 pin. All 13 'pprose guidelines|shortcut|runbook <name>' references from installed skills resolve. Deterministic pipeline end to end from an unrelated dir: metrics -> report from-metrics -> validate -> render (112KB page). score failure modes actionable (missing --model, missing API key). Upgrade 0.3.0->0.4.0 reconciles all pins, preserves user content, keeps one block, idempotent on re-run. Symlinked AGENTS.md/CLAUDE.md shared-entry pattern now works unmodified. Spec conformance codified as tests."
---
Manually validate all five skills in Claude Code and Codex CLI: at least three natural-language activation phrasings per skill, end-to-end run on small sample docs, link integrity, and referenced uvx prose-eval commands. Record any trigger wording adjustments needed.

## Notes

Partial validation completed on this branch before the guidelines-doc skill test:
Markdown links and SKILL.md frontmatter validated; skill source-path references
validated; Claude skill symlinks are relative and resolve; local prose-eval
help/report validation passes; tools/prose-eval make passes.

Additional Codex validation on 2026-05-13 used an ignored local workspace,
`.skill-test-workspace/`, against `docs/practical-prose-guidelines.md`:

- `prose-apply-common-guidelines`: loaded the common guidelines source, mirrored
  linked docs into the workspace, checked headings, trailing whitespace, local
  links, and footer. The workflow completed as a no-op pass on the guidelines
  copy.
- `prose-quick-check`: ran metrics and checklist review on the real guidelines
  doc. It found one project-style issue: ordinary prose still contains spaced
  em-dash usage even though the style guide discourages it. Banned-register hits
  were examples inside the guideline list, not defects.
- `prose-copy-edit`: ran on a workspace copy only. It replaced ordinary spaced
  em dashes while preserving the intentional bad-style example; metrics dropped
  `spaced_em_dash_count` from 13 to 1.
- `prose-eval`: generated a metrics-backed draft report, captured metrics YAML,
  validated the draft report shape, confirmed `--complete` correctly fails for
  an incomplete draft, and generated a `score --dry-run` prompt without calling
  the Anthropic API.
- `prose-compare`: validated two complete copied fixture reports for the
  guidelines context and generated a unified comparison. Warnings were limited
  to expected low link-density warnings from the fixture reports.

Remaining requirement: manual activation checks in Claude Code and Codex CLI,
three natural-language phrasings per skill, with end-to-end sample runs. Also
confirm the published `uvx prose-eval` command after the PyPI release bead is
complete; current validation used the equivalent local development entry point,
`cd tools/prose-eval && uv run prose-eval ...`.
