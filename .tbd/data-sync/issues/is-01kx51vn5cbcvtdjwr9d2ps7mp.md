---
type: is
id: is-01kx51vn5cbcvtdjwr9d2ps7mp
title: Keep routine uv workflows from rewriting the neutral lockfile
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:41:36.812Z
updated_at: 2026-07-10T04:48:03.261Z
closed_at: 2026-07-10T04:48:03.260Z
close_reason: Routine Makefiles, hooks, CI, and publishing now use no-config locked uv workflows; the two-pass lock procedure is documented.
---
PR #31, Makefile/lefthook/docs: routine uv run/sync commands honor the contributor's global exclude-newer config, immediately re-embed [options] in tools/pprose/uv.lock, and create a CI-rejected diff. Reproduced on 2026-07-09. Freeze routine installs/runs; keep deliberate re-locks explicit with --no-config.
