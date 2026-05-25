---
type: is
id: is-01ksey5rcgvrbvy9r5m08pqkrr
title: Sync packaged resources after doc updates
kind: task
status: closed
priority: 2
version: 3
labels: []
dependencies: []
parent_id: is-01ksey4hc3txw0a3f13445ahrm
created_at: 2026-05-25T06:46:50.511Z
updated_at: 2026-05-25T07:05:35.743Z
closed_at: 2026-05-25T07:05:35.742Z
close_reason: Ran tools/pprose/devtools/sync_resources.py to mirror updated docs/shortcuts/skills into tools/pprose/src/pprose/resources/; --check confirms in sync; tests/test_resources_sync.py passes.
---
Run the resource sync to propagate doc/shortcut/skill changes into tools/pprose/src/pprose/resources/:

  uv run python tools/pprose/devtools/sync_resources.py

Then verify nothing drifted:

  uv run python tools/pprose/devtools/sync_resources.py --check
  cd tools/pprose && uv run pytest tests/test_resources_sync.py

The wheel must stay self-contained, so resources/ should never be hand-edited — it's a mirror of docs/, shortcuts/, runbooks/, and skills/ from the repo root.
