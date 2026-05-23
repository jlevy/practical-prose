---
type: is
id: is-01ks97rpmhnq79he6aqq15fvkk
title: "Update minor dim-count references: principles, bibliography, shortcuts, skill, runbook, README"
kind: chore
status: closed
priority: 2
version: 3
labels:
  - rubric-rollout
  - parsimony
  - docs
dependencies:
  - type: blocks
    target: is-01ks97s25n1s058wk2nfqbtvx3
parent_id: is-01ks97m4tenhgn7w974et1nrnk
created_at: 2026-05-23T01:39:01.904Z
updated_at: 2026-05-23T02:12:38.430Z
closed_at: 2026-05-23T02:12:38.430Z
close_reason: Implemented as part of the combined 20-dim-v1 rollout (commit on claude/vibrant-goldberg-828VB)
---
Sweep through smaller files updating dim-count mentions and §-number cross-refs. ~7 small files.

## Files and changes

### docs/practical-prose-principles.md
- Lines 125-127: Dimension-to-principle mapping table — confirm Parsimony added with its principle mappings (likely Truthful + Essential).

### docs/practical-prose-bibliography.md
- Line 475: `18 dimensions` → 19.

### shortcuts/practical-prose-quick-checklist.md
- Frontmatter line 3 `18 practical-prose dimensions` → 19.
- Line 22: `audit all 18` → 19.
- Line 80: `## Judgment (§16-§18)` → `(§17-§19)`. Need to add new `## Reasoning` entry for Parsimony at §16.
- Lines 82-88: Renumber §16 Calibration → §17, §17 Fairness → §18, §18 Robustness → §19. Add new §16 Parsimony checklist item.
- Line 102: `§17 Fairness, §18 Robustness` → `§18 Fairness, §19 Robustness`.
- Sub-rule refs like `§16.6` → `§17.6` (line 84).

### shortcuts/practical-prose-agent-policy.md
- Line 58: `(§17 Fairness, §18 Robustness; ...)` → renumber.
- Line 64: `§16.6` → `§17.6`.
- Line 79: `18 dimensions` → 19.

### skills/prose-quick-check/SKILL.md
- Frontmatter line 3: `18-dimension checklist` → `19-dimension checklist`.

### runbooks/practical-prose-eval-single.runbook.md
- Lines 16, 107, 138: `18 qualitative dimensions` → 19.
- Line 222: `18-dim-v1` → `19-dim-v1`.
- Lines 229, 235, 237, 240-243: multiple version-string refs in calibration-set section.

### README.md
- Lines 96-115 (dimension table): add Parsimony row in the Reasoning section. (Note: README groups dims by group.)
- Lines 132-133, 136, 144-146: `18 dimensions` → 19 (4+ occurrences).

## Files touched

- docs/practical-prose-principles.md
- docs/practical-prose-bibliography.md
- shortcuts/practical-prose-quick-checklist.md
- shortcuts/practical-prose-agent-policy.md
- skills/prose-quick-check/SKILL.md
- runbooks/practical-prose-eval-single.runbook.md
- README.md

## Depends on

pp-v2q7 (P1: content)
