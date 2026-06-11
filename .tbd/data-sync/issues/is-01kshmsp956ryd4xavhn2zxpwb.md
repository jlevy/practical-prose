---
type: is
id: is-01kshmsp956ryd4xavhn2zxpwb
title: Bump chopdiff pin to BlockDoc-enabled version; refresh uv.lock
kind: task
status: closed
priority: 1
version: 6
spec_path: docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
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
updated_at: 2026-06-11T16:21:46.496Z
closed_at: 2026-05-27T00:00:51.959Z
close_reason: "Superseded by spec rewrite 2026-05-26 (v3). New architecture: chopdiff v0.4.x parses each block once and exposes typed accessors (heading_level, code_language, list_info, table_info, inlines, section_tree). Pprose becomes a thin serializer with no marko import and no per-block re-parse. Replaced by a fresh bead set."
---
Wait for chopdiff to ship BlockDoc (jlevy/chopdiff#8, epic chopdiff-d6js). Bump the chopdiff pin in tools/pprose/pyproject.toml to the version that exports BlockDoc; respect the supply-chain cool-off used for pydantic-ai-slim. Refresh tools/pprose/uv.lock. Verify 'pprose metrics' still runs unchanged afterwards (no behavior change yet — pure dep bump).
