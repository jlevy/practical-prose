---
type: is
id: is-01kt0wd6xe32z4gjbtjbapgs58
title: Wire --variant CLI flag; drop --sections
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0wdn9eh9m81ct8n1gr8k7y
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:02:17.389Z
updated_at: 2026-06-01T06:14:58.114Z
closed_at: 2026-06-01T06:14:58.113Z
close_reason: Implemented in Phase 1 commit.
---
In tools/pprose/src/pprose/render_html/cli.py: add --variant <name> with default 'interactive'. Drop --sections (subsumed by variants). Pass variant through RenderOpts to renderer.py; renderer loads templates/variants/<name>.html.jinja and raises with a clear 'unknown variant; available: <list>' message if the file doesn't exist. Available list comes from scanning the variants/ dir. Update the same flag plumbing in eval_score.py's --render-html path so 'pprose score --render-html --render-variant interactive' works.
