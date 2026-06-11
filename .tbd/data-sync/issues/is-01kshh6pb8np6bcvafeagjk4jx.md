---
type: is
id: is-01kshh6pb8np6bcvafeagjk4jx
title: Add flowmark as direct pprose dependency; refresh uv.lock
kind: task
status: closed
priority: 1
version: 4
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshh6tswtdm20cjh96cnw166
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T06:57:52.993Z
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-05-26T08:00:21.844Z
close_reason: "Superseded by spec rewrite 2026-05-26: pprose now depends on chopdiff BlockDoc (jlevy/chopdiff#8). Replaced by a slimmer pprose-only bead set under the same epic pp-3hg4."
---
Add 'flowmark' (currently a transitive via chopdiff) to tools/pprose/pyproject.toml under the same supply-chain pin policy used for pydantic-ai-slim. Keep chopdiff as a direct dep. Refresh tools/pprose/uv.lock. Verify 'pprose metrics' still runs unchanged afterwards (no behavior change yet).
