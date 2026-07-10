---
type: is
id: is-01kx52bew98qbqacvcyk87w5sf
title: Remove obsolete --list commands from bundled resource links
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:50:14.664Z
updated_at: 2026-07-10T04:48:04.270Z
closed_at: 2026-07-10T04:48:04.270Z
close_reason: Bundled directory links now render bare listing commands; resources were regenerated and regression-tested.
---
PR #31, tools/pprose/devtools/sync_resources.py and README: directory-link rewriting still emits removed pprose <category> --list commands; the packaged about output gives commands that exit 2. Rewrite category links to bare listing commands, update tests/docstrings, fix README's stale --list claim, and resync resources.
