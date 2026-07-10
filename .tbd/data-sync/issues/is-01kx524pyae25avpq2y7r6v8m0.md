---
type: is
id: is-01kx524pyae25avpq2y7r6v8m0
title: Update metrics output label for expanded bracket-tag conventions
kind: bug
status: closed
priority: 3
version: 3
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:46:33.545Z
updated_at: 2026-07-10T04:48:03.938Z
closed_at: 2026-07-10T04:48:03.937Z
close_reason: Metrics descriptions and human output now name confidence and inference-rung tag families accurately.
---
PR #31, tools/pprose/src/pprose/metrics.py:411: human output still labels the section ALL-CAPS although the branch now counts lowercase rung tags and colon-suffixed tags. Use an accurate concise label and cover it with output assertions.
