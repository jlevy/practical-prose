---
title: Comprehensive Project Review, 2026-07
description: Whole-repo review of practical-prose — errors found, self-application audit of the guidelines against the repo's own documents, coverage gaps, and open questions — with clear fixes applied on the same branch and the rest tracked as beads.
date: 2026-07-09
status: active
purpose: Record what a full external review of the project found, what was fixed immediately, and what needs the maintainer's judgment.
audience: Repo maintainer and future contributors or agents doing follow-up work.
scope: The whole repository at commit ce6c2bc — reference docs, shortcuts, runbooks, skills, pprose package, design system, CI, and supply-chain posture. Excludes example-texts content (third-party verbatim) and the visual explorations.
owner: Joshua Levy (github.com/jlevy)
last_reviewed: 2026-07-09
risk_level: standard
evaluation_mode: external
---
# Comprehensive Project Review, 2026-07

Review by Claude (agent), 2026-07-09, on branch
`claude/project-comprehensive-review-g9tsdj`.

## Summary

The project is in strong shape: the Principles → Guidelines → Rubric triple is genuinely
tight (the 20-dimension tables are cell-for-cell identical across README, guidelines,
and rubric), the docs largely practice what they prescribe, the test suite is
disciplined (fixture-locked goldens, sync tests), and all 8 committed eval reports
validate.
The defects found were mostly at the seams: code that drifted from docs (schema
vs. guidelines), docs that drifted from code (claimed metrics that don’t exist), and
operational state that drifted from both (an unpublished release that everything pins, a
lockfile CI never actually used, a tbd pin that can’t read its own repo).

Three things need the maintainer soonest:

1. **Publish v0.2.0** — every committed skill and AGENTS.md falls back to
   `uvx pprose@0.2.0`, which does not exist on PyPI (pp-jcou).
2. **Re-lock `uv.lock` from a clean environment** — the committed lock embeds personal
   global uv settings, so CI silently re-resolved dependencies on every run until this
   branch pinned installs with `UV_FROZEN` (pp-ft60).
3. **Decide the canonical four-pass mapping** (pp-fx6c) — the remaining open
   self-application policy; the frontmatter policy was resolved on this branch (finding
   6, pp-2wdi closed).

Clear fixes were applied on this branch in three commits (see *Fixed on This Branch*);
everything else is a bead, listed with IDs throughout and gathered at the end.

## Method

- Read every reference doc, shortcut, runbook, skill, and key project doc end to end.
- Ran the repo’s own tooling on itself: full test suite, ruff, codespell,
  `sync_resources --check`, design-system `--check`, `pprose report validate` on all 8
  committed eval reports, and `pprose metrics` on all 21 canonical docs.
- Scripted cross-checks: the 20-dimension table identity across the three docs;
  `rubric_schema.yaml` questions and rule counts against the guidelines; every relative
  link and anchor in 137 Markdown files; footer presence and placement; frontmatter
  inventory; British-vs-American spelling sweep.
- A separate fresh-context agent code-reviewed the pprose package (per the repo’s own
  two-pass practice); findings were independently verified before fixing.
- External checks: PyPI release state for `pprose` and `flexdoc`, npm state for
  `get-tbd`, arXiv metadata for cited papers, uv lockfile behavior in a clean
  environment.

## Fixed on This Branch

Commits `04f7ec7` (fixes), `aa3b0ad` (tbd refresh), and the commit adding this review.
Highlights, so the rest of this doc can focus on what is *not* fixed:

- **`pprose score --render-html` crashed on every invocation.** The v0.1.0 removal of
  `render --format folder` (pp-sd3z) left `_render_after_score` passing a removed
  dataclass field and importing a deleted function.
  Fixed; regression test added.
- **`rubric_schema.yaml` had drifted from the v0.2 guidelines.** Five dimension
  questions were stale — Factuality still carried the old citation-driven wording the
  docs deliberately replaced with corroboration-driven wording; Verifiability dropped
  “or explicit assumptions” — and G1 was missing rule 7 ("Links serve readers"), so a
  scorer citing G1.7 had its violation dropped as out-of-range, exactly the alignment
  failure the compare runbook warns about.
  Fixed; a new sync test pins schema questions and rule counts to the guidelines doc so
  this class of drift now fails CI.
- **The flexdoc supply-chain bridge never worked and had expired.** uv requires a full
  RFC 3339 timestamp in `[tool.uv] exclude-newer-package`; the date-only value made uv
  warn and ignore the whole table.
  flexdoc 0.2.0 also aged out of the 14-day window on 2026-06-28, so the entry was
  removed per its own removal rule, and SUPPLY-CHAIN-SECURITY.md was trued up (it still
  described `flexdoc==0.1.0`; the pin is 0.2.0) including the correct syntax for future
  in-window bridges.
- **CI now installs from the lockfile.** `UV_FROZEN` set in ci.yml and publish.yml (see
  finding 2 below for why plain `uv sync` was not doing this).
- **tbd was unusable in this repo.** The pinned `get-tbd@0.2.1` supports config format
  f04; the repo’s `.tbd/config.yml` was already f05, so the documented fallback gave
  agents a blank tracker.
  `tbd setup --auto` at 0.3.0 (first-party exemption) bumped the pins, upgraded the
  config to f06, and regenerated the AGENTS.md block — whose new template also fixes the
  spaced em dash the old block carried in violation of F2.7.
- **Doc/code truth-ups.** The README claimed `pprose metrics` computes “vague-word
  counts, link validity, frontmatter presence” — none of the three exists today; the
  metrics doc attributed vague-magnitude and sentence-length metrics to the tool (rows 4
  and 5) and is now accurate, including disclosure that the default banned-register list
  is §4.2 *plus* `dominant` and that the bracket-tag counter covers only ALL-CAPS
  colon-less forms. `pprose score` examples now include the required `--model`; provider
  docs no longer claim Anthropic-only; “five skills” → six; pages label `wpm` → `wpp`.
- **Bibliography.** Added the Rallapalli et al.
  and Xia/Stańczak/Roth entries that ai-prose-corrections.md already cited as being “in
  the bibliography” (they were only in the internal research doc); author names and
  dates verified against arXiv.
  Fixed the write-good author (Brian Ford, not “Brett”; verified against the GitHub
  handle btford) and two wording duplications.
- **Self-application fixes.** The rubric’s own `## Notes` heading was a generic heading
  its own F1.9 flags (and its own linter counts); renamed to *Limits of Scores* with the
  one cross-reference updated.
  British spellings normalized per F2.1 (labelled, acknowledgement ×4, signalled,
  catalogue ×2). The copy-edit tier is now described as “Expression **and Form**”
  everywhere (two docs said Expression only, contradicting their own frontmatter).
  Standard footer added to 7 docs missing it.
  Moved-spec sibling links fixed (the done/ spec pointed at files that stayed in
  active/); two `/Users/levy/...` local-filesystem links replaced with GitHub URLs
  (common-doc §1.2 bans local paths).

## Findings Needing Action or Judgment

Ordered by severity.
Each has a bead.

### 1. The pinned `pprose@0.2.0` does not exist (pp-jcou, P1)

`AGENTS.md` and all committed SKILL.md discovery copies (skills/, .agents/skills/,
.claude/skills/, and the wheel mirrors) instruct: “else `uvx pprose@0.2.0`”. PyPI’s
latest is 0.1.1; `uvx pprose@0.2.0` fails with a resolution error for anyone without a
local install. TODO.md has carried “tag/PyPI release pending” since 2026-06-13. The
release machinery is ready (publish.yml, the `check_release_version.py` tag guard,
release-readiness-2026-06.md).
Cut the release, or re-pin the committed copies to a published version until then.

### 2. `uv.lock` embeds personal global settings; CI never installed from it (pp-ft60, P2)

The committed lock’s `[options]` block records `exclude-newer-span = "P7D"` and
per-package `2100-01-01` sentinels — the maintainer’s global `~/.config/uv/uv.toml`
leaking into the artifact.
Any environment without those globals (CI, every contributor) considers the lock stale:
uv prints “Ignoring existing lockfile due to removal of timestamp cutoff” and silently
re-resolves.
Observed effect in this review: a plain `uv sync` upgraded 57 packages (e.g.
anthropic 0.102.0 → 0.116.0). CI’s `uv sync --all-extras` has therefore been testing
freshly resolved dependencies on every run — not the lock — which also bypasses the
14-day cool-off the repo is careful about everywhere else.

`UV_FROZEN` (this branch) makes installs actually frozen.
The remaining work: re-lock from a clean environment (or commit the intended resolution
policy repo-scoped, e.g. a versioned `uv.toml`, using full timestamps) so every
environment resolves identically; then CI can also gain a `uv lock --check` staleness
gate, which today would fail for the wrong reason.

### 3. The tag metric can’t see the tags the guidelines recommend (pp-hdc0, P2)

`BRACKET_TAG_RE` matches only ALL-CAPS, colon-less tags.
But the guidelines’ own recommended conventions are `[ASSUMING: ...]` and
`[DERIVED: 89.6 / 614.5 = 14.6%]` (G1.4, R2.3) and the lowercase rung tags `[observed]`
/ `[judged]` / `[interpreted]` / `[implied]` (R1.4). A document following the guidelines
to the letter reports zero bracket tags.
The docs now disclose this; the right fix is in the tool: count by tag mnemonic (prefix
before a colon), case-normalize the four rung tags, update the golden fixtures.
Not applied here because the goldens pin current behavior and the change deserves its
own reviewed diff.

### 4. The four-pass audit mapping disagrees across the triple (pp-fx6c, P2)

Three docs describe the lint / claim / reasoning / purpose audit passes with three
different dimension assignments:

| Doc | Reasoning pass | Claim pass | Purpose pass | Unassigned |
| --- | --- | --- | --- | --- |
| rubric §Audit Passes | R1, R2, J2, J3 | G1, G2 | P1-P4 | E2, E3, R3, R4, G3, J1 |
| quick-checklist §Four Audit Passes | R1, R2, **R4**, J2, J3 | G1, G2 | P1-P4 | E2, E3, R3, G3, J1 |
| shortcut-full-edit §Procedure | R1-R4, J2, J3 | G1, G2, **G3** | P1-P4, **J1** | — (adds a 5th Expression pass for E1-E3) |

The rubric’s table says “Primary dimensions”, so non-exhaustiveness is defensible, but
the three should not disagree where they overlap, and J1 Calibration under the *purpose*
audit (full-edit) is hard to defend — claim-strength-vs-evidence fits the reasoning or
claim audit. Recommend: make the rubric’s table the canonical complete mapping (all 20
assigned), then align the checklist and shortcut to it.

### 5. Baseline evals predate the docs they evaluate (pp-wuap, P2)

The three self-eval baselines carry `eval_date: 2026-06-06`; the doc suite had a v0.2
editorial pass on 2026-06-12 and further changes on this branch (rubric heading,
bibliography entries, dialect).
The quant blocks (word counts, lint hits) no longer describe the current files.
Regenerate per the baseline-evals runbook after this branch merges, and re-check the
calibration table pinned in the single-doc runbook (guidelines-self ≈ 4.1 overall).

### 6. Frontmatter: the repo didn’t follow its own recommended schema (pp-2wdi, P3 — resolved on this branch)

practical-prose-metrics.md declares `title`, `description`, `date`, `status` as
**Required**, but the repo’s own durable docs sat in three tiers: none (guidelines,
principles, common-doc, bibliography, writing-practical-guides, ai-prose-corrections),
partial (`title`/`description`/`category`/`author` but no `date`/`status`: all six
shortcuts, authoring-principles), and full (rubric, metrics, both runbooks).

**Resolution applied:** the required four fields are now present on every reference doc,
shortcut, and runbook (`date` taken from each file’s first git commit;
`status: active`). Repo-root operational files (README, TODO, SUPPLY-CHAIN-SECURITY,
AGENTS) are explicitly exempted in the metrics doc’s schema section — GitHub renders
README frontmatter as a literal table, and AGENTS.md is partly generated — and keep the
version byline instead.
The `Version: v0.x` byline remains as a complementary convention on the reference docs,
matching the rubric’s existing practice.
pp-2wdi is closed.

### 7. Mention vs. use: the docs flag their own linter (pp-5m0m, P3)

The reference docs quote the patterns they ban, so the deterministic lint fires on its
own guidelines — measured on this branch:

| Doc | banned | pedantic | repl-history | spaced em dash |
| --- | ---: | ---: | ---: | ---: |
| practical-prose-guidelines.md | 15 | 5 | 3 | 1 |
| common-doc-guidelines.md | 14 | 1 | 1 | 0 |
| practical-prose-rubric.md | 0 | 5 | 2 | 1 |
| practical-prose-bibliography.md | 14 | 0 | 0 | 4 |
| ai-prose-corrections.md | 3 | 1 | 1 | 0 |

Nearly all are quotations of the banned pattern (the guidelines’ spaced em dash is
F2.7’s own counter-example; the bibliography’s four are verbatim ISO standard titles;
its 14 banned hits are mostly `dominant` used descriptively, which the default list
extends beyond §4.2). Every hit is a justified deviation — but per the rubric’s own
Justified Deviations rule, deviations should be *documented*, and today nothing records
which hits are expected.
Options, roughly in order of appeal: put quoted counter-examples in inline code (the
lint already skips code, but this changes rendered typography); teach the lint to skip
curly-quoted spans; commit expected-hit baselines (see finding 9). Related smaller nit:
HTML-comment text is scanned as prose (README’s single pedantic hit is a maintainer
comment, not rendered text).

### 8. Rule numbers are load-bearing but have no stability policy (pp-j3ot, P3)

Eval reports cite findings as dimension + `rule_number`, and the validator enforces the
range. Inserting a rule mid-list would renumber everything after it and silently
re-target every archived eval.
This review appended G1.7 (safe), but nothing states the policy.
One sentence in the rubric’s Versioning section fixes it: rule additions are
append-only; renumbering requires a version bump.

### 9. Institutionalize the self-application loop (pp-186c, P3)

The most effective single addition this review suggests: a CI step that runs
`pprose metrics` over the repo’s own canonical docs and diffs against committed
expected-hit baselines.
It is deterministic, cheap, on-brand, and would have caught the rubric’s generic “Notes”
heading, the dialect drift, and any future regression — while also serving as the
documentation of expected mention-vs-use hits that finding 7 wants.

## Smaller Observations (no bead; fix opportunistically)

- `.claude/skills/` mixes five symlinked skill directories (the original install) with
  three real directories (later additions).
  Functional, but normalize by re-running a current `pprose install` after the release;
  symlinks are also the one piece of this repo that degrades on Windows checkouts.
- `gather_limited` in `_concurrency.py` acquires the semaphore before the rate-limit
  token, so a task can hold a concurrency slot while waiting for a token.
  At the defaults (8 concurrent, 4 rps) the waste is ≤0.25 s per task; not worth
  changing unless defaults change.
  (Fresh-context code review finding, verified.)
- The compare runbook references “F3a softening” — an internal validator rule name that
  appears nowhere else; a two-word gloss would keep it self-contained.
- The archived README review (review-major-rev-02) trips naive link checkers because its
  quoted draft blocks contain root-relative links; harmless, but future review docs may
  prefer fencing quoted drafts (this doc fences nothing that links).
- `tools/pprose/CHANGELOG.md` has an `[Unreleased]` section ready for the v0.2.0 notes —
  one more reason finding 1 is cheap to close.
- TODO.md’s snapshot header says 2026-06-13; refresh after this branch merges (it
  correctly defers to tbd as canonical, so this is cosmetic).

## Self-Application Audit, by Group

The question the review was asked: are these docs exemplary instances of what they
describe? Verdict per group, on the doc suite as a whole:

- **Purpose — strong.** Every reference doc states its task and scope in the first
  screen; the layered architecture (common → principles → guidelines → rubric → genre)
  is real, not aspirational; skim-recoverability holds (the In Brief section, the
  rubric’s alignment rules up front).
  Gap: the README’s own map omits two docs (pp-t733), and the LLM-as-judge objection is
  still unanswered in the README — that remains the strongest pending item from the
  earlier README review (Draft A).
- **Expression — strong.** Zero real banned-register or AI-tell usage found outside
  quotation; the prose is concrete and register-disciplined.
  The handful of genuine slips (wording duplications, “five skills”) are fixed on this
  branch.
- **Form — good, now better.** The dimension tables were verified identical; heading
  hierarchies are clean; footers are now complete; the genuine misses (generic “Notes”
  heading, dialect drift, two shorthand contradictions about what copy-edit covers) are
  fixed, and the frontmatter policy is now decided and applied (finding 6).
- **Reasoning — exemplary.** The dimension-boundary paragraphs (Parsimony vs.
  Concision vs. Relevance; Discipline vs.
  Soundness; the NA/ERR decision tree and cascades) are the best part of the suite: they
  do the disambiguation work most rubrics skip.
  The four-pass mapping inconsistency (finding 4) is the one seam.
- **Grounding — good.** The bibliography is real and specific (verified spot-wise
  against arXiv, PyPI, GitHub); two cited-but-missing entries and one wrong author are
  fixed. The docs’ claims about their own tooling were the weak spot (five distinct
  overclaims fixed); that class of drift now has a sync test where it was
  machine-checkable.
- **Judgment — exemplary in the prose, pending in the process.** “Is It Mature?
  No.” and the Personal Note’s concession are model calibration; the rubric’s Limits of
  Scores section anticipates rubric-gaming honestly.
  The process gap is that self-evals are stale (finding 5) and nothing forces the loop
  to run (finding 9).

## Coverage Gaps Worth Attention

Beyond the findings above, areas the project does not yet cover that fit its stated
scope:

- **More genre supplements.** writing-practical-guides.md proves the pattern
  (applies-when conditions per guideline).
  The eval tooling already names the genres that would benefit next: decision memos,
  specs/design docs, runbooks, postmortems — each has distinctive output-shape rules
  (P1.5) that a one-page supplement could carry.
  No bead filed; this is roadmap, not defect.
- **Contribution surface (pp-jhs9).** A public repo with unusually careful supply-chain
  rules but no CONTRIBUTING.md or SECURITY.md; both can be one screen.
- **Accessibility of the rendered eval page (pp-abb7).** The bibliography treats WCAG as
  normative; the render pipeline has hover-driven tip panels and an SVG-heavy card with
  no a11y check. An axe-core smoke beside the existing e2e test would close the gap and
  pairs with the visual-regression bead (pp-5zgc).
- **Scoring reliability** is already tracked (pp-aim6); this review adds only the
  observation that the calibration fixtures are the natural place to measure run-to-run
  variance continuously, once baselines are regenerated (pp-wuap).

## Open Questions for the Maintainer

1. Where should J1 Calibration live in the canonical four-pass mapping?
   (pp-fx6c)
2. Should `dominant` stay in the default banned list now that it is documented, move to
   a domain extension list, or gain an “earned when descriptive” carve-out?
   Its presence means the bibliography will always carry ~14 expected hits.
3. Counter-examples in quotes vs.
   inline code: is the typography change acceptable to make the docs lint-clean?
   (pp-5m0m)
4. When does `pp20v1` freeze?
   The rubric says it is refined in place; consumers pinning eval behavior (and the new
   schema sync test) would benefit from a stated freeze trigger, even a rough one.

## Bead Index

Filed this review: pp-jcou (P1, release), pp-ft60 (P2, lockfile), pp-hdc0 (P2, tag
metric), pp-fx6c (P2, four-pass mapping), pp-wuap (P2, baselines), pp-j3ot (P3, rule
numbering), pp-2wdi (P3, frontmatter — closed on this branch), pp-5m0m (P3,
mention-vs-use), pp-jhs9 (P3, CONTRIBUTING/SECURITY), pp-abb7 (P3, a11y), pp-186c (P3,
self-lint CI), pp-t733 (P3, README map).
Pre-existing beads referenced: pp-aim6, pp-5zgc.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
