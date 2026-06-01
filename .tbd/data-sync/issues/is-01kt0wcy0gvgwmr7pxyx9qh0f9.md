---
type: is
id: is-01kt0wcy0gvgwmr7pxyx9qh0f9
title: "Rewrite renderer.py: build JSON payload, drop Python-built DOM"
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies:
  - type: blocks
    target: is-01kt0wd442cmyknxtpkvpapfr3
  - type: blocks
    target: is-01kt0wdn9eh9m81ct8n1gr8k7y
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:02:08.271Z
updated_at: 2026-06-01T06:14:57.747Z
closed_at: 2026-06-01T06:14:57.746Z
close_reason: Implemented in Phase 1 commit.
---
Rewrite tools/pprose/src/pprose/render_html/renderer.py: drop _build_dim_rows, _group_rows, _group_payload, _segment_alpha, _dim_color_mix, _score_color and every per-dim/group DOM-shaping helper — these now live in the shared bi-card JS. Renderer's new job: parse the .eval.md, build a JSON payload that matches each component's data contract ({ groups, dimensions, rubric, doc }), and pass that payload to the Jinja template. The payload's  field carries id, name, scores (keyed by dim id like P1/E2), reasons, findings (rule_number/verdict/description), meta (rubric_version, word count for the kicker). The  field carries per-dim question + rules + group context. Detect_kind, render(), and render_eval_report() public entries stay but their internals shrink dramatically.
