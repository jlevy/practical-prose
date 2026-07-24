# Changelog

All notable changes to the `pprose` package are recorded here.
The format loosely follows [Keep a Changelog](https://keepachangelog.com/), and the
project aims to follow [semantic versioning](https://semver.org/). Versions are produced
from git tags by dynamic versioning (see [docs/publishing.md](docs/publishing.md)).

## [Unreleased]

## [0.3.1] - 2026-07-24

### Fixed

- **`pprose-common-edit` is bounded to a correction pass, not a rewrite.** Applying the
  common edit tier in practice showed that “preserving its intended content and voice”
  underspecified the edit scope: an agent could read “apply the guidelines” as license
  to reword paragraphs and rename sections.
  The skill now fixes objective errors (grammar, typos, punctuation, casing, Markdown
  mechanics, broken links) in place, keeps the author’s wording, sentence structure,
  section order, and headings unless a rule is unambiguously violated, and records
  broader guideline-driven changes as suggestions in the report instead of applying
  them.

## [0.3.0] - 2026-07-19

### Added

- **`pprose-de-slop` skill.** A focused apply skill that removes documented AI-writing
  tells and formulaic LLM prose while preserving meaning, evidence, claim strength, and
  voice. It applies the bundled `ai-prose-corrections` catalog contextually, refuses
  detector evasion and manufactured “human” quirks (no fake typos, anecdotes, or
  contractions-for-cover), and sits explicitly in the edit ladder: common-edit, then
  de-slop, then copy-edit, then full-edit (the deeper passes include it).
  Self-contained: the skill bundles its guideline reference, so
  `npx skills add jlevy/practical-prose@pprose-de-slop` needs no Python, uv, or pprose
  runtime.
- **Cross-agent zero-install skill profiles.** `pprose install` gains
  `--profile=common-docs|practical-prose` (the complete suite remains the default),
  repeatable exact `--skill` selection, and
  `--surfaces=portable,claude,agents-md,claude-md`. The selected skill set is
  scope-wide: later runs reconcile every existing pprose-managed destination, prune
  pprose-generated skills safely, and manage marker-bounded `AGENTS.md` and `CLAUDE.md`
  policy blocks. `pprose-common-edit` is likewise self-contained, and clean cross-agent
  installs work via the skills CLI (`npx skills add jlevy/practical-prose[@skill]`).

### Changed

- **De-slop applies by default.** The generated `AGENTS.md` policy blocks (and this
  repo’s root `AGENTS.md`) direct agents to apply AI-slop reduction whenever prose is
  drafted or edited, not only on request.
  The deeper `pprose-copy-edit` and `pprose-full-edit` passes include the de-slop pass
  and remain opt-in.
- **`ai-prose-corrections` catalog v0.3.** Expanded from a survey of documented AI-slop
  tells (Wikipedia’s *Signs of AI writing*, the Kobak et al.
  and Juzek & Ward excess-vocabulary studies, and community complaint patterns): new
  sections for inflated significance, copula avoidance, vague attribution, canned
  conclusions, chat-artifact leakage, boilerplate openers, audience flattery, and
  scaffolding that restates; new attention flags (hedge stacking, structure density,
  elegant variation); extended hollow-verb, importance-adjective, and stock-metaphor
  vocabulary; four new coverage-table rows; and drafting directive 7 (“End when the
  content ends”). The `ai-prose-checklist` digest is synced to the catalog.
- Repo-only `flowmark` and `tbd` workflow skills are marked internal so public skill
  discovery offers only the Practical Prose suite.

### Fixed

- **Installer profiles reconcile across surfaces.** Instruction surfaces bring along the
  skill tree they reference, so installed `AGENTS.md` / `CLAUDE.md` policy never points
  at an absent skill or bundled guideline.
- **Single-pass resource sync.** `make generate` now converges in one run when `docs/`
  change: discovery-skill bundled references are composed from the same-run synced plan
  instead of stale on-disk wheel copies (regression-tested).

### Documentation

- **Clear upgrade path.** The Upgrading notes (README and
  [docs/installation.md](docs/installation.md)) now spell out the per-scope re-run
  (`uvx pprose@latest install`, or
  `uv tool install --upgrade pprose && pprose install`), what reconciliation refreshes
  (artifacts, baked pins, managed `AGENTS.md` / `CLAUDE.md` blocks), that skills new in
  a release are added and deselected generated skills are pruned safely, and that
  skills-CLI installs refresh by re-running
  `npx skills add jlevy/practical-prose[@skill]`. Verified against a live
  `0.2.0 → 0.3.0` project upgrade (f01 artifacts upgrade in place to f02; no stale pins
  remain).

## [0.2.0] - 2026-07-12

### Fixed

- **`pprose score --render-html` works reliably.** The composition path still called the
  folder-mode API removed from `pprose render` in v0.1.0, so the flag crashed on every
  invocation before rendering anything.
  It now renders the single-file page, validates variants before any paid model call,
  renders only successfully scored batch items, and reports rendering failures through
  the process exit code.
- **`rubric_schema.yaml` re-aligned with the v0.2 guidelines.** Five dimension questions
  were stale (notably Factuality’s corroboration-driven wording and Verifiability’s “or
  explicit assumptions”), and G1 was missing rule 7 (“Links serve readers”), so a scorer
  citing G1.7 failed alignment validation.
  A new sync test pins the schema’s questions and ordered rule identities to the
  guidelines, rubric, and README copies so they cannot drift silently.
- Human metrics output labels the page estimate “wpp” (words per page), matching the
  compare and render surfaces; it previously said “wpm”.
  Custom `--words-per-page` values are reflected in the label.
- **Bracket-tag counting covers the documented tag conventions.** The metric matched
  only ALL-CAPS colon-less tags, so the guidelines’ own recommended forms were
  invisible: colon-suffixed confidence tags (`[ASSUMING: ...]`, `[DERIVED: ...]`,
  counted by their mnemonic) and the four lowercase ladder-of-inference rung tags
  (`[observed]`, `[judged]`, `[interpreted]`, `[implied]`) are now counted.
  Other lowercase or mixed-case bracket text is still not a tag.
- Bundled links to guideline, shortcut, and runbook directories use the current bare
  listing commands rather than the removed `--list` flag.

### Changed

- **Typed document model on flexdoc 0.3.0.** `metrics.py` now uses `flexdoc.FlexDoc`
  (the standalone document layer extracted from chopdiff) instead of `chopdiff.TextDoc`,
  and chopdiff is dropped as a dependency.
  Every structural count comes from the typed model instead of hand-rolled regex:
  headings by depth (`Block.heading_level`), links by form (`Link.link_form` plus
  reference definitions), images, footnotes, tables, and code blocks.
  The dependency footprint shrinks because flexdoc omits chopdiff’s diff and
  windowed-transform machinery, which pprose never used.
  Editorial lint **and** word / sentence / paragraph / line counts now run over one
  consistent prose projection, `FlexDoc.prose_text(include_tables=True)`, so a few size
  counts shift slightly (link URLs and inline code are no longer counted as prose
  words). A future flexdoc release may offer configurable counting scopes
  ([jlevy/flexdoc#8](https://github.com/jlevy/flexdoc/issues/8)). A few counts are now
  more correct: footnote references no longer double-count definition lines, headings
  inside code blocks are excluded, indented and `~~~`-fenced code blocks are counted,
  and reference-definition URLs are no longer miscounted as bare URLs.
  flexdoc 0.3.0 also normalizes CRLF and lone-CR input before parsing, keeping source
  offsets and every structural view in one coordinate space.
  flexdoc is admitted under the standing first-party cool-off exemption (see
  [SUPPLY-CHAIN-SECURITY.md](../../SUPPLY-CHAIN-SECURITY.md)).
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
- **Bundled guidelines: v0.2 editorial pass.** A language-and-consistency pass across
  the shipped guideline suite (practical-prose guidelines / rubric / metrics /
  principles / authoring-principles, common-doc-guidelines, ai-prose-corrections): Title
  Case section headings, house-style punctuation (spaced-em-dash removal), and tightened
  wording, including small rubric question refinements (e.g. Soundness now names
  explicit assumptions).
  The rubric id `pp20v1` is unchanged, and the guidelines / rubric / README dimension
  table stays cell-for-cell aligned.
- **Bundled docs: 2026-07 review pass.** All bundled reference docs and shortcuts now
  carry the recommended-schema required frontmatter (`title`, `description`, `date`,
  `status`); the metrics doc describes today’s `pprose metrics` capabilities exactly
  (including the `dominant` banned-register extension, colon-suffixed confidence tags,
  and lowercase inference-rung tags); the rubric’s “Notes” section is renamed “Limits of
  Scores”; the bibliography adds Rallapalli et al.
  (2026) and Xia, Stańczak, and Roth (EACL 2026) and corrects the write-good author;
  American-spelling normalization per F2.1.
- **Packaging and CI hygiene.** Removed the expired `[tool.uv] exclude-newer-package`
  flexdoc bridge (it also never parsed on the affected uv version: the project setting
  required a full RFC 3339 timestamp).
  Routine development, CI, wheel-smoke, and publish installs now reject lock drift and
  use the committed runtime lock.
  Isolated builds use a reviewed, hash-locked build constraint set, including
  `hatchling==1.30.1` and `uv-dynamic-versioning==0.14.0`.

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

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
