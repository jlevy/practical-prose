---
type: is
id: is-01krhz2f5wsv5rwkvzz2c6mbaq
title: Run cross-agent skill validation
kind: task
status: open
priority: 2
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-13-cross-agent-skills.md
labels:
  - cross-agent-skills
  - validation
dependencies: []
parent_id: is-01krhz0ckjzn0s26wggjjfays1
created_at: 2026-05-14T00:44:32.827Z
updated_at: 2026-05-14T01:06:22.816Z
---
Manually validate all five skills in Claude Code and Codex CLI: at least three natural-language activation phrasings per skill, end-to-end run on small sample docs, link integrity, and referenced uvx prose-eval commands. Record any trigger wording adjustments needed.

## Notes

Partial validation completed on this branch: markdown links and SKILL.md frontmatter validated; skill source-path references validated; Claude skill symlinks are relative and resolve; local prose-eval help/report validation passes; tools/prose-eval make passes. Remaining requirement: manual activation checks in Claude Code and Codex CLI, three phrasings per skill, with end-to-end sample runs.
