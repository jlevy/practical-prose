---
type: is
id: is-01kt0wdsdxen1z505jfgq70k2e
title: Manual browser verification + AGENTS.md docs update
kind: task
status: closed
priority: 2
version: 3
spec_path: docs/project/specs/active/plan-2026-05-31-shared-render-components.md
labels: []
dependencies: []
parent_id: is-01kt0wbjcdtg8pyezcwrkhk69j
created_at: 2026-06-01T06:02:36.348Z
updated_at: 2026-06-01T06:32:03.172Z
closed_at: 2026-06-01T06:32:03.162Z
close_reason: "Docs portion done: agents-internal-guide.md updated with --variant, --list-variants, and the shared-components architecture. Manual browser verification remains for the user — render /tmp/rev2-net-eval.html and confirm card + hover panels + theme toggle + print preview work in Chrome and Safari (Letter + A4)."
---
Manual browser verification — open /tmp/rev2-net-eval.html (or run pprose render --open) in Chrome + Safari. Verify: card renders, hover panels populate, theme toggle flips Auto/Light/Dark, Cmd-P preview is light-only with toggle hidden, both Letter and A4 paginate sensibly. Then update docs/project/agents-internal-guide.md Tooling section to document --variant + the shared-components architecture.
