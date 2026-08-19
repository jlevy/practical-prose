---
type: is
id: is-01m0djwj0t1phrpvtqatdqv679
title: Live activation testing for the seven skills in Claude Code and Codex
kind: task
status: open
priority: 2
version: 1
spec_path: docs/project/specs/done/plan-2026-05-13-cross-agent-skills.md
labels: []
dependencies: []
parent_id: is-01krhz0ckjzn0s26wggjjfays1
created_at: 2026-08-19T18:00:13.082Z
updated_at: 2026-08-19T18:00:13.082Z
---
pp-flf2 closed the mechanical half of cross-agent validation and it is now enforced by tests: install shape, relative-link integrity, that all 13 'pprose guidelines|shortcut|runbook <name>' references resolve, upgrade reconciliation, and Agent Skills spec conformance (name/description/frontmatter/allowed-tools).

What tests cannot cover is activation. Remaining work, against published v0.4.0:

- Confirm each of the seven skills loads on natural user phrasings (not just its literal trigger words) in Claude Code and in Codex CLI.
- Confirm the always-on pair (pprose-common-edit, pprose-de-slop) fires when it should and stays out of unrelated tasks.
- Confirm a global (-g) install activates in an unrelated repo without imposing project policy, which is the property the v0.4.0 docs now promise.
- Note any description wording that triggers too broadly or too narrowly and tune it.

Needs real agent sessions; cannot be done from CI.
