---
type: is
id: is-01kx52wnrh7tzp3arjjy4jy3fb
title: Make generated tbd bootstrap reject incompatible installed versions
kind: bug
status: open
priority: 2
version: 1
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:59:38.768Z
updated_at: 2026-07-10T03:59:38.768Z
---
PR #31 generated tbd session scripts prefer any tbd on PATH; an installed 0.2.x still wins over pinned 0.3.0 and cannot read f06. Fix upstream generator to check compatibility or fall back after prime failure; also remove generated @latest install advice under exact-pin repos.
