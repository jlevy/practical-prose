---
type: is
id: is-01ktvstk04s5nr8ywb4p70xph2
title: "Phase 2: term.py color layer + styled output"
kind: feature
status: open
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-06-11-cli-snappiness-color-and-listing.md
labels: []
dependencies:
  - type: blocks
    target: is-01ktvt4rf8wazk9y4h4w033t2h
parent_id: is-01ktvssrx2tntw63ankhqzk1dq
created_at: 2026-06-11T16:56:39.684Z
updated_at: 2026-06-11T17:02:23.483Z
---
Per spec Phase 2: stdlib-only pprose/term.py with use_color(stream) honoring NO_COLOR, FORCE_COLOR, CI, TERM=dumb, isatty; --color {auto,always,never} top-level flag; minimal style set (bold/dim/heading/command/warn/err) rendering plain when off; data->stdout, errors/hints->stderr; width clamp 40-100 (fixed when non-TTY); style help epilog, command help, reference listings, errors, install report; golden tests pin byte-stable plain output.
