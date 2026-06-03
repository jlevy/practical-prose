---
type: is
id: is-01kskbs2nwx1aveqsnpn9txak8
title: "[chopdiff v0.4.x] (optional) Add TextDoc.frontmatter"
kind: task
status: open
priority: 3
version: 3
spec_path: tools/docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md
labels:
  - cross-repo
  - upstream-chopdiff
dependencies: []
parent_id: is-01kshh6agcz1skz71dx3ychz3s
created_at: 2026-05-27T00:01:32.858Z
updated_at: 2026-06-03T05:05:02.823Z
---
Tracked here; work in jlevy/chopdiff. Optional polish: detect YAML frontmatter at the start of the document (^---\s*\n.*?\n---\s*$ in DOTALL) and expose it as TextDoc.frontmatter: str | None. Exclude it from the paragraphs list so it never inflates counts. If this doesn't land, pprose detects and skips the leading block itself; the metric outputs are identical either way.

## Notes

chopdiff 0.3.1 audit: not exposed in 0.3.1. pprose has a clean source-text workaround, so this is an OPTIONAL upstream follow-up, not blocking. To file against jlevy/chopdiff before its next release — see docs/project/chopdiff-upstream-requests.md.
