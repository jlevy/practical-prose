---
type: is
id: is-01kx52wnrh7tzp3arjjy4jy3fb
title: Make generated tbd bootstrap reject incompatible installed versions
kind: bug
status: open
priority: 2
version: 2
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:59:38.768Z
updated_at: 2026-07-12T20:23:24.342Z
---
PR #31 generated tbd session scripts prefer any tbd on PATH; an installed 0.2.x still wins over pinned 0.3.0 and cannot read f06. Fix upstream generator to check compatibility or fall back after prime failure; also remove generated @latest install advice under exact-pin repos.

## Notes

tbd 0.4.0 setup still prefers any local tbd and exits on prime failure instead of invoking the pinned runner. The v0.2.0 release PR preserves the repo-local fallback and updates it to get-tbd@0.4.0 in both session and closing-reminder hooks; rerunning setup overwrites this customization, so the upstream generator issue remains open.
