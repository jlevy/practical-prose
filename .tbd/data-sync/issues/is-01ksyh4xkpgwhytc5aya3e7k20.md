---
type: is
id: is-01ksyh4xkpgwhytc5aya3e7k20
title: Expand pprose skill no-args to overview mode
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
created_at: 2026-05-31T08:07:02.517Z
updated_at: 2026-05-31T08:12:56.263Z
closed_at: 2026-05-31T08:12:56.258Z
close_reason: pprose skill no-args prints intro + table + routing footer to guidelines/shortcut/runbook/about; --list stays terse; <name> unchanged. 2 new tests green; old test_skill_list_outputs_descriptions renamed/tightened to test_skill_list_outputs_terse_table.
---
TDD: test pprose skill (no args) prints intro paragraph + skill table + routing footer; --list stays terse; <name> unchanged. Refactor skill_main to branch on --list vs no-args.
