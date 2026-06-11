---
type: is
id: is-01ktvstjrc39cpy9dph29f1mqr
title: "Phase 1: lazy imports + listing contract + pprose list"
kind: feature
status: open
priority: 1
version: 2
spec_path: docs/project/specs/active/plan-2026-06-11-cli-snappiness-color-and-listing.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktvstk04s5nr8ywb4p70xph2
parent_id: is-01ktvssrx2tntw63ankhqzk1dq
created_at: 2026-06-11T16:56:39.436Z
updated_at: 2026-06-11T16:56:40.609Z
---
Per spec Phase 1: cli.py keeps only stdlib imports at module level (in-function imports per command, textpress pattern); verify reference.py is import-light; import-graph guard test (no pydantic_ai/anthropic/openai/google in 'import pprose.cli') + startup budget test + per-command --help smoke; no-args-lists contract with --list hidden-deprecated for one release; new top-level 'pprose list' inventory grouped by kind; update every doc surface that mentions --list (help strings, README, AGENTS.md template in install.py, skill preamble, agents-internal-guide) and resync.
