---
type: is
id: is-01kx524pfw8288kfkwbgqknc69
title: Make batch score rendering honor per-file outcomes
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:46:33.082Z
updated_at: 2026-07-10T04:48:03.605Z
closed_at: 2026-07-10T04:48:03.605Z
close_reason: Batch render callbacks now run only after successful scoring, and render failures count as failed items with CLI regression coverage.
---
PR #31, tools/pprose/src/pprose/eval_score.py:985-994: --batch --render-html renders every input path even when scoring failed, can render stale reports, catches render exceptions as warnings, and returns 0 when requested rendering failed. Render only after each successful score and count render failures in the batch exit code; add regression coverage.
