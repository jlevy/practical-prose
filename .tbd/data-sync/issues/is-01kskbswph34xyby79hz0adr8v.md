---
type: is
id: is-01kskbswph34xyby79hz0adr8v
title: Bump chopdiff pin to v0.4.0; refresh uv.lock
kind: task
status: closed
priority: 1
version: 3
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels: []
dependencies:
  - type: blocks
    target: is-01kskbsx1f7fm5cmj1j6hca4qb
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:01:59.497Z
updated_at: 2026-06-03T05:04:25.815Z
closed_at: 2026-06-03T05:04:25.810Z
close_reason: "Done: chopdiff bumped to 0.3.1 in PR (release/v0.1.0-stabilization), uv.lock refreshed, 266 tests pass."
---
Wait for chopdiff v0.4.0 release. Bump the chopdiff pin in tools/pprose/pyproject.toml under the supply-chain 14-day cool-off used for other pins. Refresh tools/pprose/uv.lock. Verify no pprose call sites use TextUnit.tiktokens (renamed to TextUnit.tokens in chopdiff v0.3.0). Verify 'pprose metrics' still runs unchanged afterwards (no behavior change yet — pure dep bump).
