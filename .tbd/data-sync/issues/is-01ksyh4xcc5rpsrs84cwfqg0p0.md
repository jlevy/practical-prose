---
type: is
id: is-01ksyh4xcc5rpsrs84cwfqg0p0
title: Add pprose about command
kind: task
status: closed
priority: 2
version: 4
spec_path: docs/project/specs/active/plan-2026-05-30-pprose-install-scopes-and-surfaces.md
labels: []
dependencies:
  - type: blocks
    target: is-01ksyh4yd2dtt6zrcd0ek46jas
  - type: blocks
    target: is-01ksyh4ympybqjqjnfb0rz3bxs
parent_id: is-01ksyh41ve1a731ww85kxnh54k
created_at: 2026-05-31T08:07:02.283Z
updated_at: 2026-05-31T08:12:03.450Z
closed_at: 2026-05-31T08:12:03.441Z
close_reason: added pprose about command (reference.about_main + cli.py registration). prints bundled README; rejects extra args. 2 tests added, green.
---
TDD: test first that pprose about prints bundled README content (sentinel string). Add the command to cli.py + a small implementation. One-shot, no --list. Update --help epilog mention.
