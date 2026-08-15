# TODO

Snapshot of active work as of 2026-08-15. **Canonical tracking is tbd** (`tbd ready` for
unblocked work, `tbd list` for everything); this file is a periodically refreshed
orientation map, not a second tracker.
Planning specs live in [docs/project/specs/active/](docs/project/specs/active/)
(finished ones move to [done/](docs/project/specs/done/); the legacy `tools/docs/` tree
was consolidated here on 2026-06-11).

## Now (unblocked, highest value)

- **Reporting CLI redesign** (epic pp-d2j3; spec
  [plan-2026-06-03](docs/project/specs/active/plan-2026-06-03-reporting-cli-redesign.md)):
  the eval → report → show pipeline.
  Not started; phases pp-f86c → pp-qpa2 → pp-3evy, with the metrics-schema chain
  (pp-pd8t → pp-vusm / pp-h75u → pp-is5n) feeding it.
- **Two-phase AI-prose linting** (spec
  [plan-2026-06-09](docs/project/specs/active/plan-2026-06-09-ai-slop-mitigations-and-two-phase-linting.md)):
  Phase 1 (corrections catalog + checklist) shipped; Phase 2-3 (`resources/rules/` YAML,
  `pprose lint`) tracked under pp-ybcx, pp-j9q0, pp-gy7z, pp-65cs, pp-lik1, pp-3kb6,
  pp-ggui, pp-twg4.

## Quality and Reliability

- **Scoring reliability** (pp-aim6): run-to-run variance (±1 on ~6 dims between
  identical runs) and the stubborn sub-5-without-citation alignment miss; consider
  ensemble scoring or an auto-retry.
- **pprose score loose ends** (epic pp-h780): provider adapters (pp-q6es Anthropic,
  pp-kjzj OpenAI), source-check modes (pp-2qk8, pp-0ns4), run executor and summaries
  (pp-f9na, pp-gib1), docs/tests (pp-nhhf).
- **Visual-regression smoke for the eval page** (pp-5zgc) and **manual print
  verification** (pp-kmv5).
- **Cross-agent skill validation**: the mechanical pass is done and now encoded as tests
  (pp-flf2 closed in v0.4.0 — install shape, link integrity, resource-reference
  resolution, upgrade reconciliation, spec conformance).
  What remains under epic pp-mpo1 is the part tests cannot cover: live *activation*
  checks in Claude Code and Codex CLI, confirming each skill loads on natural phrasings
  and stays out of unrelated tasks.

## Tooling Debt

- Design-system: generator tests (pp-i4uh); vendor Zod locally instead of esm.sh
  (pp-tfdk).
- Structural document decomposition for metrics (epic pp-3hg4; spec
  [plan-2026-05-25](docs/project/specs/active/plan-2026-05-25-structural-document-metrics.md)):
  the behavior-preserving regex->flexdoc workaround removal **shipped** on flexdoc 0.2.0
  (pp-bcrw; archived spec
  [plan-2026-06-13](docs/project/specs/done/plan-2026-06-13-metrics-flexdoc-workaround-removal.md)).
  Remaining is the schema rewrite (`*_count` renames, prose-only count semantics,
  heading outline, distributions, eval_report/eval_compare updates) under pp-pd8t and
  successors; docstring sweep pp-ka9t.
- Eval-screenshot tooling (deferred from the README-cards work): snapshot-fit print CSS
  (pp-2gs0), multi-document side-by-side render (pp-39ce), optional in-package
  `pprose snapshot` (pp-w0oz).

## README and Docs Follow-Ups

- Remaining README revision drafts A-E (LLM-as-judge paragraph, positioning section,
  Age-of-AI consolidation, Where-to-Start fold, hero placement) await per-draft approval
  in
  [docs/project/reviews/review-major-rev-02-claude-fable.md](docs/project/reviews/review-major-rev-02-claude-fable.md).
- After material README changes, regenerate the example-evaluation cards per
  [docs/project/eval-screenshots.runbook.md](docs/project/eval-screenshots.runbook.md).

## Recently Shipped (Context)

- v0.4.0 prep (2026-08-15): repaired the zero-install bootstrap — 0.3.1 was prepped and
  merged but never tagged, so every committed skill advertised an unresolvable
  `uvx pprose@0.3.1`. Added a daily published-pin check so a forgotten release surfaces
  within a day; fixed `pprose install` clobbering a symlinked `AGENTS.md` (pp-b7gy);
  made the user-wide install the documented default path with `-g` / `-p` short flags;
  closed the dogfooding drift in both repo skill surfaces and the repo’s own `AGENTS.md`
  block; upgraded tbd to 0.6.5.
- v0.3.0 on PyPI (2026-07-19): de-slop skill and cross-agent zero-install skill
  profiles. (v0.3.1 was prepared 2026-07-24 but never tagged; its fix ships in v0.4.0.)
- v0.2.0 on PyPI (2026-07-12): CLI revamp (lazy-import startup ~1.16s to ~56ms,
  auto-detected color, `pprose list`; `--list` removed), chopdiff -> flexdoc 0.1.0
  migration, and a v0.2 editorial pass across the bundled guideline suite.
- v0.1.1 on PyPI (2026-06-11): writing-practical-guides genre supplement with skill
  routing, ai-prose consolidation, upgrade-path docs, slimmer wheel.
- Post-release repo org (2026-06-11): single specs home under docs/project/specs/
  (legacy tools/docs tree removed), bead spec_paths re-pointed, ghost links fixed,
  README badges added.
- v0.1.0 on PyPI (2026-06-10): first release, OIDC trusted publishing, release-tag
  guard.
- `writing-practical-guides` genre supplement + skill routing; AI-prose corrections
  consolidation; design-system and baseline-evals runbook unbundled from the wheel.
- Calibration pass on the example evals (epic pp-a65z; one follow-up open: pp-aim6).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
