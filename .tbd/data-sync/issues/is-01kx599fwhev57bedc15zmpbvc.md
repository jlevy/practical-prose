---
type: is
id: is-01kx599fwhev57bedc15zmpbvc
title: Handle non-batch render failures per input
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01kx599fjed9w5y77xswj8ab2t
created_at: 2026-07-10T05:51:30.192Z
updated_at: 2026-07-10T05:58:23.077Z
closed_at: 2026-07-10T05:58:23.076Z
close_reason: Non-batch render failures now report partial success, return non-zero, and continue later reports; regression coverage is committed and pushed.
---
PR #31 thread PRRT_kwDOSbwK686Pxn3C: tools/pprose/src/pprose/eval_score.py non-batch score --render-html must report render failures, continue later inputs, and return non-zero.
