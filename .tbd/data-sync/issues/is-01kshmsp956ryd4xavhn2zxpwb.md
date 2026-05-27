---
type: is
id: is-01kshmsp956ryd4xavhn2zxpwb
title: Bump chopdiff pin to BlockDoc-enabled version; refresh uv.lock
kind: task
status: open
priority: 1
version: 4
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kshmspqewmm0rw0c9f0grq4s
  - type: blocks
    target: is-01kshmsq2vfk7ws48rt8vcm1hn
  - type: blocks
    target: is-01kshmsqeapneg35whw8589qq8
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-26T08:00:41.248Z
updated_at: 2026-05-26T08:01:37.980Z
---
Wait for chopdiff to ship BlockDoc (jlevy/chopdiff#8, epic chopdiff-d6js). Bump the chopdiff pin in tools/pprose/pyproject.toml to the version that exports BlockDoc; respect the supply-chain cool-off used for pydantic-ai-slim. Refresh tools/pprose/uv.lock. Verify 'pprose metrics' still runs unchanged afterwards (no behavior change yet — pure dep bump).
