---
type: is
id: is-01kx51vncf5z2t4sryc51h65vv
title: Correct stale bracket-tag claim in the 0.2.0 changelog
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:41:37.038Z
updated_at: 2026-07-10T04:48:03.441Z
closed_at: 2026-07-10T04:48:03.440Z
close_reason: The 0.2.0 changelog now describes all supported confidence and inference-rung tag forms accurately.
---
PR #31, tools/pprose/CHANGELOG.md: the bundled-docs bullet says the matcher is ALL-CAPS-only, but this branch adds colon-suffixed tags and four lowercase rung tags. Replace with an accurate concise description.
