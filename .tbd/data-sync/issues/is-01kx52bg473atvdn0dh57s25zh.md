---
type: is
id: is-01kx52bg473atvdn0dh57s25zh
title: Use locked dependencies for the design-system generator
kind: bug
status: closed
priority: 1
version: 3
labels: []
dependencies: []
parent_id: is-01kx51k0wy3x1b6qf8eyzbpq94
created_at: 2026-07-10T03:50:15.942Z
updated_at: 2026-07-10T04:48:05.109Z
closed_at: 2026-07-10T04:48:05.108Z
close_reason: The design-system generator now runs from the locked project environment in local hooks and CI.
---
PR #31, lint-root/Makefile/lefthook: UV_FROZEN is ignored for PEP 723 script mode without generate.py.lock, so green CI freshly resolves six packages. Run the generator from the frozen tools/pprose project lock or add/review a dedicated script lock; make all official invocations truly frozen.
