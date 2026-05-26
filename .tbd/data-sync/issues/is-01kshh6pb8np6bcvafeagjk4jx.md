---
type: is
id: is-01kshh6pb8np6bcvafeagjk4jx
title: Add flowmark as direct pprose dependency; refresh uv.lock
kind: task
status: open
priority: 1
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshh6tswtdm20cjh96cnw166
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T06:57:52.993Z
updated_at: 2026-05-26T06:59:09.406Z
---
Add 'flowmark' (currently a transitive via chopdiff) to tools/pprose/pyproject.toml under the same supply-chain pin policy used for pydantic-ai-slim. Keep chopdiff as a direct dep. Refresh tools/pprose/uv.lock. Verify 'pprose metrics' still runs unchanged afterwards (no behavior change yet).
