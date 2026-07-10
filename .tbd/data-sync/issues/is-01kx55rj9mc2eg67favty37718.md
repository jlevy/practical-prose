---
type: is
id: is-01kx55rj9mc2eg67favty37718
title: Keep Biome write-mode off generated Markdown
kind: bug
status: closed
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T04:49:49.874Z
updated_at: 2026-07-10T04:50:12.348Z
closed_at: 2026-07-10T04:50:12.347Z
close_reason: Biome now excludes Markdown, leaving it to flowmark; make default passes end to end.
---
The authoritative make default gate failed after resource generation because Biome 2.4 recognizes Markdown but cannot write it. Exclude Markdown from Biome; flowmark remains its formatter.
