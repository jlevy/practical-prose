---
type: is
id: is-01krfgkr6rtn0sj8e5r82ct367
title: "Phase 2: Update single-doc + compare runbooks with batch form and ANTHROPIC_API_KEY note"
kind: task
status: closed
priority: 2
version: 2
spec_path: docs/project/specs/active/plan-2026-05-12-eval-scoring-rearchitecture.md
labels: []
dependencies: []
parent_id: is-01krfgdgghp4x3rtpyk0kd4r1n
created_at: 2026-05-13T01:53:21.623Z
updated_at: 2026-05-13T02:28:09.866Z
closed_at: 2026-05-13T02:28:09.858Z
close_reason: "Both runbooks updated for the final Phase 2 reality: single-doc runbook documents --batch with --max-concurrent 8 / --max-rps 4 defaults (already done in pp-17m4); compare runbook now sharpens the wall-clock figure with the observed ~1m33s, explains gather_limited fan-out, the cache-priming behavior we saw (concurrent first-fire creates the cache, subsequent calls hit it), and the F3a alignment-failure recovery path with --allow-misaligned. ANTHROPIC_API_KEY via .env / .env.local is covered in single-doc §Setup."
---
runbooks/practical-prose-eval-single.runbook.md: add 'batch' usage example, document ANTHROPIC_API_KEY env-var requirement, note that --use-cli is the escape hatch using local 'claude' agent auth. runbooks/practical-prose-eval-compare.runbook.md: note that step 1 (score each artifact) now runs as a single batch call.
