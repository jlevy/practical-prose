---
type: is
id: is-01kx3zk86x8e9j95tjkybh96hp
title: Handle mention-vs-use in the editorial lints
kind: feature
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-07-09T17:42:49.821Z
updated_at: 2026-07-09T17:42:49.821Z
---
The reference docs quote the patterns they ban, so pprose metrics flags its own guidelines: banned=15/pedantic=5/replacement-history=3/spaced-em-dash=1 on practical-prose-guidelines.md, banned=14 on common-doc-guidelines.md, etc. metrics.py acknowledges the limitation. Options: (a) skip matches inside curly-quoted spans; (b) move quoted counter-examples to inline code (metrics already skips code); (c) commit expected-hit baselines for self-evals. Also: HTML comment text is scanned as prose (README's one pedantic hit is a maintainer comment). From review-2026-07-09.
