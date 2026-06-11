---
type: is
id: is-01ktvstjrc39cpy9dph29f1mqr
title: "Phase 1: lazy imports + listing contract + pprose list"
kind: feature
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-06-11-cli-snappiness-color-and-listing.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktvstk04s5nr8ywb4p70xph2
  - type: blocks
    target: is-01ktvt4rf8wazk9y4h4w033t2h
parent_id: is-01ktvssrx2tntw63ankhqzk1dq
created_at: 2026-06-11T16:56:39.436Z
updated_at: 2026-06-11T17:13:21.501Z
closed_at: 2026-06-11T17:13:21.500Z
close_reason: "Implemented: lazy module:attr command targets (import pprose.cli ~1.16s->56ms; pprose --help ~1.3s->0.07s; heavy SDK chain absent, guarded by test_cli_startup.py import-graph + budget tests). --list removed entirely; no-name-lists contract + new 'pprose list' inventory; all surfaces scrubbed and regenerated. 312 tests pass, lint clean."
---
Per spec Phase 1 (hard cut, no backward compat): cli.py keeps only stdlib imports at module level (in-function imports per command, textpress pattern); verify reference.py import-light; import-graph guard test (no pydantic_ai/anthropic/openai/google in 'import pprose.cli') + startup budget + per-command --help smoke; no-args-lists contract with --list REMOVED entirely (argparse, help strings, all docs); new top-level 'pprose list' inventory grouped by kind; scrub every --list mention (README, AGENTS.md template in install.py, skill preamble, agents-internal-guide) and resync.
