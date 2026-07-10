---
type: is
id: is-01kx52bf4g6g2dhpz778tme7y5
title: Complete schema-to-doc drift guards
kind: bug
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:50:14.927Z
updated_at: 2026-07-10T04:48:04.444Z
closed_at: 2026-07-10T04:48:04.443Z
close_reason: The schema guard now checks all four question copies and ordered rule identities, not only counts.
---
PR #31, test_rubric_schema_docs_sync.py: new guard compares questions and rule counts only, so same-count rule rename/reorder passes despite load-bearing rule numbers and the docstring claim. Compare ordered rule identities and verify all stated question-table copies.
