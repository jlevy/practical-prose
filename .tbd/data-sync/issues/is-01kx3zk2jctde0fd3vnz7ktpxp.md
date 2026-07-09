---
type: is
id: is-01kx3zk2jctde0fd3vnz7ktpxp
title: Count colon-suffixed and lowercase rung bracket tags in pprose metrics
kind: feature
status: closed
priority: 2
version: 2
labels: []
dependencies: []
created_at: 2026-07-09T17:42:44.043Z
updated_at: 2026-07-09T19:26:11.826Z
closed_at: 2026-07-09T19:26:11.826Z
close_reason: "Resolved on review branch: BRACKET_TAG_RE now matches colon-suffixed confidence tags (counted by mnemonic) and the four lowercase R1.4 rung tags; fixture and tests extended; pinned goldens unchanged; metrics doc and module docstring updated."
---
BRACKET_TAG_RE only matches ALL-CAPS colon-less tags, so the tag conventions the guidelines themselves recommend are invisible to the metric: [ASSUMING: ...] and [DERIVED: ...] (G1.4, R2.3) and the lowercase rung tags [observed]/[judged]/[interpreted]/[implied] (R1.4). Count by tag mnemonic (prefix before any colon), case-normalize the four rung tags. Requires updating metric golden fixtures. The metrics doc's Tooling Map was trued up to disclose the limitation on 2026-07-09.
