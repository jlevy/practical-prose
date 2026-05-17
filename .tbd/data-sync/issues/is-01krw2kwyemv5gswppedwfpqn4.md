---
type: is
id: is-01krw2kwyemv5gswppedwfpqn4
title: Add repeat, multi-target, and concurrent run executor
kind: task
status: open
priority: 2
version: 2
spec_path: tools/docs/project/specs/active/plan-2026-05-17-eval-tool-and-model-configuration.md
labels: []
dependencies:
  - type: blocks
    target: is-01krw2m12xa8r5qp2zcmmfqv2b
parent_id: is-01krvxewx2bjm707fh941e3dvk
created_at: 2026-05-17T22:58:54.030Z
updated_at: 2026-05-17T22:59:22.391Z
---
Expand runs deterministically as targets x repeat. Add --repeat, repeated --target, --concurrency, and --out-dir. Default concurrency should be 2 and capped by run count. Execute independent provider calls with bounded concurrency while preserving deterministic run ids, stable report paths, summary ordering, and partial-failure records.
