---
type: is
id: is-01kt0wdn9eh9m81ct8n1gr8k7y
title: Rewrite test_render_html.py + add drift-check test
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0wdsdxen1z505jfgq70k2e
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:02:32.109Z
updated_at: 2026-06-01T06:14:58.655Z
closed_at: 2026-06-01T06:14:58.654Z
close_reason: Implemented in Phase 1 commit.
---
Rewrite tools/pprose/tests/test_render_html.py for the new shape: (a) detect_kind tests stay unchanged. (b) Replace DOM-shape assertions with payload-shape assertions: render the rev2-net fixture, parse the inlined <script type="application/json" id="pp-eval-data">, assert it contains groups/dimensions/rubric/doc with the expected keys. (c) Assert the bootstrap <script> calls PracticalProseBiCard.mount, PracticalProseTipPanels.mount, PracticalProseDesignColorControls.mountThemeToggle. (d) Assert .theme-toggle markup is present. (e) Schema-coverage: build an EvalReport in memory with 1-5, NA, ERR scores; payload renders without error. (f) NEW: add tests/test_render_html_sync.py that runs  via subprocess and asserts exit code 0 — CI fails on any drift between render-components/ + design-system/ and the synced wheel files.
