---
type: is
id: is-01ktvssrx2tntw63ankhqzk1dq
title: "CLI cleanup: snappiness, color, and listing UX"
kind: epic
status: closed
priority: 1
version: 5
spec_path: docs/project/specs/active/plan-2026-06-11-cli-snappiness-color-and-listing.md
labels: []
dependencies: []
child_order_hints:
  - is-01ktvstjrc39cpy9dph29f1mqr
  - is-01ktvstk04s5nr8ywb4p70xph2
  - is-01ktvt4rf8wazk9y4h4w033t2h
created_at: 2026-06-11T16:56:12.961Z
updated_at: 2026-06-11T17:21:59.237Z
closed_at: 2026-06-11T17:21:59.236Z
close_reason: "Epic complete: pp-mbh2 (lazy imports + listing + pprose list), pp-b7pl (term.py color layer), pp-kzov (e2e + docs) all closed. import pprose.cli ~1.16s->56ms; --list removed; auto color with NO_COLOR/CI/TTY; 326 tests, lint clean."
---
Umbrella for the CLI cleanup spec: ~1.3s --help fixed via lazy imports, repren/textpress-style color layer with NO_COLOR/FORCE_COLOR/CI/TTY detection, and the no-args-lists contract replacing the redundant --list flag (plus top-level 'pprose list'). Research synthesis in the spec (python-cli-patterns guideline, textpress, repren).
