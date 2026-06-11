# Changelog

All notable changes to the `pprose` package are recorded here.
The format loosely follows [Keep a Changelog](https://keepachangelog.com/), and the
project aims to follow [semantic versioning](https://semver.org/). Versions are produced
from git tags by dynamic versioning (see [docs/publishing.md](docs/publishing.md)).

## [Unreleased]

### Changed

- **Faster startup.** CLI command targets are imported lazily at dispatch, so
  `pprose --help`, `--version`, and the reference listings no longer load the eval chain
  (pydantic_ai + provider SDKs).
  `import pprose.cli` drops from ~1.16s to ~56ms.
- **Auto-detected color output.** Help, listings, and errors are styled on an
  interactive terminal and emitted as plain text when piped, in CI, under `NO_COLOR`, or
  driven by an agent. A `--color {auto,always,never}` flag overrides detection.
- **Simpler listing UX (breaking).** The redundant `--list` flag is removed.
  `pprose guidelines|shortcut|runbook` with no name lists that kind; with a name prints
  one. `pprose skill` prints the skills overview.
  New top-level `pprose list` prints the full bundled inventory (guidelines, shortcuts,
  runbooks, skills), with `--kind` to filter.

## [0.1.1] - 2026-06-11

Documentation and bundled-resource update; no code-behavior or breaking changes.

### Added

- **writing-practical-guides** genre supplement: guidelines for comprehensive practical
  guides, wired into skill routing.
- `ai-prose-corrections` checklist shortcut, with mitigations consolidated into the
  corrections guideline.

### Changed

- writing-practical-guides: sharpen the contrast with Wikipedia (linking its
  no-original-research, not-a-how-to-guide, and neutral-point-of-view policies) and add
  Voice qualities (rigor, clarity, warmth) plus Scientific / Story / Example / Resources
  callout types.
- common-doc-guidelines (v0.2): add Chicago Manual of Style hyphenation guidance.
- Bundled-resource links now resolve through systemic location rules.
- Document the skill upgrade path; replace stale `eval_report.py` references with
  `pprose report`.
- Slimmer wheel: unbundle the design-system and baseline-evals runbooks.
- README: tactical fixes from an editorial review.

## [0.1.0] - 2026-06-09

First public release.

- Add `pprose --version`.
- Accept `GEMINI_API_KEY` as an alias for `GOOGLE_API_KEY` for the `google` provider.
- Documentation: dual-license note (code MIT, bundled prose CC BY 4.0); dotenv-autoload
  and default-model cost note on `pprose score`; metrics-vs-eval-report lint-signal
  asymmetry note; corrected install flags and PyPI/trusted-publisher setup docs.
