---
type: is
id: is-01kt0wcj8vnf5gk2c92fqzadvr
title: Rewrite sync_render_html_styles.py for the manifest model
kind: task
status: closed
priority: 2
version: 5
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0wcr3c1tsrzp9e34fzv2eg
  - type: blocks
    target: is-01kt0wdfzjjqe6sdawfc77e4v1
  - type: blocks
    target: is-01kt0wdn9eh9m81ct8n1gr8k7y
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:01:56.249Z
updated_at: 2026-06-01T06:14:57.374Z
closed_at: 2026-06-01T06:14:57.374Z
close_reason: Implemented in Phase 1 commit.
---
Rewrite tools/pprose/devtools/sync_render_html_styles.py to operate on a small manifest (COMPONENTS = ('bi-card', 'tip-panels', 'theme-toggle')) plus design-system + vendor sources. On every run, copy verbatim: design_system.css from tools/design-system/_generated/; each component's .css/.js/.html.jinja from tools/render-components/<name>/; vendor/marked.min.js; design-system/assets/icons.svg. Outputs go to tools/pprose/src/pprose/render_html/styles/_generated/, js/_generated/, templates/, and assets/. Stamp each output with a provenance header naming the source path. Support --check mode (exit non-zero on any drift) for CI. Use Path.read_bytes/write_bytes so a binary-equivalent compare works even if line endings differ.
