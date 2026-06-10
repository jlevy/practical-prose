# TODO

Snapshot of active work as of 2026-06-10. **Canonical tracking is tbd** (`tbd ready` for
unblocked work, `tbd list` for everything); this file is a periodically refreshed
orientation map, not a second tracker.
Planning specs live in [docs/project/specs/active/](docs/project/specs/active/)
(finished ones move to [done/](docs/project/specs/done/)).

## Now (unblocked, highest value)

- **Cut v0.1.1** (pp-ew5z): ship `writing-practical-guides`, the genre-routed skills,
  and the upgrade docs to published users.
  Requires bumping the baked discovery pin (`DISCOVERY_VERSION`) to 0.1.1 so the release
  guard passes.
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

## Quality and reliability

- **Scoring reliability** (pp-aim6): run-to-run variance (±1 on ~6 dims between
  identical runs) and the stubborn sub-5-without-citation alignment miss; consider
  ensemble scoring or an auto-retry.
- **pprose score loose ends** (epic pp-h780): provider adapters (pp-q6es Anthropic,
  pp-kjzj OpenAI), source-check modes (pp-2qk8, pp-0ns4), run executor and summaries
  (pp-f9na, pp-gib1), docs/tests (pp-nhhf).
- **Visual-regression smoke for the eval page** (pp-5zgc) and **manual print
  verification** (pp-kmv5).
- **Cross-agent skill validation** (pp-flf2, epic pp-mpo1): manual activation checks in
  Claude Code and Codex CLI against the published package.

## Tooling debt

- Design-system: generator tests (pp-i4uh); vendor Zod locally instead of esm.sh
  (pp-tfdk).
- Structural document decomposition for metrics (epic pp-3hg4; chopdiff v0.4.x asks
  pp-9cmv, pp-tg93, pp-eaa2, pp-4hku; docstring sweep pp-ka9t).
- Repo org: single specs home; attic cleanup (pp-wlwj).
- Eval-screenshot tooling (deferred from the README-cards work): snapshot-fit print CSS
  (pp-2gs0), multi-document side-by-side render (pp-39ce), optional in-package
  `pprose snapshot` (pp-w0oz).

## README / docs follow-ups

- Remaining README revision drafts A-E (LLM-as-judge paragraph, positioning section,
  Age-of-AI consolidation, Where-to-Start fold, hero placement) await per-draft approval
  in
  [docs/project/reviews/review-major-rev-02-claude-fable.md](docs/project/reviews/review-major-rev-02-claude-fable.md).
- After material README changes, regenerate the example-evaluation cards per
  [docs/project/eval-screenshots.runbook.md](docs/project/eval-screenshots.runbook.md).

## Recently shipped (context)

- v0.1.0 on PyPI (2026-06-10): first release, OIDC trusted publishing, release-tag
  guard.
- `writing-practical-guides` genre supplement + skill routing; AI-prose corrections
  consolidation; design-system and baseline-evals runbook unbundled from the wheel.
- Calibration pass on the example evals (epic pp-a65z; one follow-up open: pp-aim6).
