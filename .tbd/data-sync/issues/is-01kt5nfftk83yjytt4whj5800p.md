---
type: is
id: is-01kt5nfftk83yjytt4whj5800p
title: Decide and fix pprose render --format folder (dead sidecar files)
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/release-readiness-2026-06.md
labels:
  - release
  - render
dependencies: []
parent_id: is-01kt5nebv6vqtrx17dfy0hy04m
created_at: 2026-06-03T02:37:24.179Z
updated_at: 2026-06-03T06:11:23.894Z
closed_at: 2026-06-03T06:11:23.893Z
close_reason: "Removed render --format folder (and folder_mode / write_folder_assets): it emitted HTML identical to single mode plus an unreferenced assets/ dir. Single self-contained HTML is the only mode now."
---
Risk #6. 'pprose render --format folder' writes HTML that is byte-identical to single mode and never references the sidecar assets/ directory it creates, so it ships dead files. Either wire the folder HTML to use <link>/<script src> (as the workbench does) or remove the option before release. Needs a small design decision, then implementation + test.
