---
type: is
id: is-01ks97ycmb6hp3mfmz5q8qkbpd
title: "Update minor dim-count references for Relevance: principles, bibliography, shortcuts, skill, runbook, README"
kind: chore
status: closed
priority: 2
version: 3
labels:
  - rubric-rollout
  - relevance
  - docs
dependencies:
  - type: blocks
    target: is-01ks97yme61jy7g3wwczpt9fy0
parent_id: is-01ks97vjxrmnzmxk6ke3hmt505
created_at: 2026-05-23T01:42:08.267Z
updated_at: 2026-05-23T02:12:41.680Z
closed_at: 2026-05-23T02:12:41.680Z
close_reason: Implemented as part of the combined 20-dim-v1 rollout (commit on claude/vibrant-goldberg-828VB)
---
Sweep through smaller files for Relevance — same files as the Parsimony equivalent (pp-zlkh) but adding Relevance row in Grounding group and renumbering §13+ references.

## Files and changes

### docs/practical-prose-principles.md
- Dimension-to-principle mapping table: add Relevance row (likely Truthful + Purposeful).

### docs/practical-prose-bibliography.md
- '18 dimensions' → 19 (or 20).

### shortcuts/practical-prose-quick-checklist.md
- Frontmatter and intro line: dim count → 19 (or 20).
- Grounding section: add §13 Relevance checklist item.
- Renumber §13-§18 references (every section ≥ 13 shifts +1).

### shortcuts/practical-prose-agent-policy.md
- Renumber any §13+ references.
- Dim count → 19 (or 20).

### skills/prose-quick-check/SKILL.md
- Frontmatter '18-dimension checklist' → '19-dimension checklist' (or 20).

### runbooks/practical-prose-eval-single.runbook.md
- '18 qualitative dimensions' → 19 (or 20).
- '18-dim-v1' → '19-dim-v1' (or 20).
- Calibration-set section: any version-string refs.

### README.md
- Dimension table (Grounding section): add Relevance row.
- '18 dimensions' → 19 (or 20) — 4+ occurrences.

## Files touched

- docs/practical-prose-principles.md
- docs/practical-prose-bibliography.md
- shortcuts/practical-prose-quick-checklist.md
- shortcuts/practical-prose-agent-policy.md
- skills/prose-quick-check/SKILL.md
- runbooks/practical-prose-eval-single.runbook.md
- README.md

## Depends on

pp-xt1p (R1: content)
