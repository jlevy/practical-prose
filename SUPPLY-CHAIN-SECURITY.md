# Supply-Chain Security

This repo follows the **Supply-Chain Hardening** policy
(`tbd guidelines supply-chain-hardening`; full playbooks at
<https://github.com/jlevy/supply-chain-hardening>). This file is the portable flag any
agent or contributor should read before adding or upgrading a dependency.

## The Policy Here

- **14-day cool-off.** Do not add or upgrade to a dependency version less than 14 days
  old unless a documented exception below applies.
  Registries yank malicious versions within minutes to days, so waiting is nearly free.
- **Lockfiles are committed; installs are frozen.** `uv.lock` and `package-lock.json`
  are checked in. Routine Python commands ignore personal resolver config and use
  `UV_LOCKED`; JS installs use `npm ci`. Never auto-update without reviewing the
  lockfile diff like a code diff.
- **No unpinned zero-install runners.** Every `uvx` / `npx` invocation pins an exact
  `@version` (see the `FLOWMARK_VERSION` pin in the [Makefile](Makefile) and the
  `--no-install` biome/lefthook calls in [lefthook.yml](lefthook.yml), which resolve the
  locked local binary rather than fetching latest).
- **Pin fresh-ish or sensitive deps exactly.** Runtime deps that need a specific version
  are pinned with a dated comment (see `pydantic-ai-slim` in
  [tools/pprose/pyproject.toml](tools/pprose/pyproject.toml)).
- **Audit and don’t update for its own sake.** The safest update is the one you skip;
  bump only for a concrete, stated reason.

### Per-Ecosystem Controls

| Tool | Control in this repo |
| --- | --- |
| uv (Python, `tools/pprose`) | `uv.lock` committed and **environment-neutral** (see below); routine commands use `UV_NO_CONFIG` + `UV_LOCKED`; CI and publish gate on `uv lock --check`; isolated build requirements have a separate hashed constraint set. |
| npm (JS tooling, `tools/`) | `package-lock.json` committed; CI uses `npm ci`; cool-off enforced at upgrade time via `npm-check-updates --cooldown 14` and `npm view <pkg> time.<ver>`. |

**The lockfile must stay environment-neutral.** A plain `uv lock` run under a global
`exclude-newer` config embeds that machine’s resolution settings as an `[options]` block
in `uv.lock`; any environment *without* those settings (CI, other contributors) then
treats the lock as stale, and a plain `uv sync` silently re-resolves instead of
installing what was reviewed.
The root and package Makefiles, git hooks, CI, and publish workflow therefore ignore
personal uv config and fail on lock drift.
CI also rejects any `[options]` table.

For a dependency change, use a two-pass lock:

```bash
cd tools/pprose
uv lock --no-config --exclude-newer '14 days'
# Review every selected-version and hash change here.
uv lock --no-config
```

The first pass applies the 14-day gate to direct and transitive packages.
It records the cutoff in a temporary `[options]` table.
With the selected versions already locked, the second pass removes the resolver setting
while preserving those selections.
Review the second diff and confirm it removes only `[options]`; CI independently
verifies the final lock is current and environment-neutral.

**Build requirements are locked separately.** `uv build` resolves its isolated PEP 517
environment independently of `uv.lock`, so `tools/pprose/build-requires.in` exact-pins
the direct build tools and `build-constraints.txt` records their full transitive closure
with hashes. Regenerate it under the same cool-off:

```bash
cd tools/pprose
uv pip compile --no-config --exclude-newer '14 days' --generate-hashes \
  --output-file build-constraints.txt build-requires.in
```

Keep the two direct pins synchronized with `[build-system].requires` in
`pyproject.toml`. CI and publish pass the constraint file to `uv build` with
`--require-hashes`.

## First-Party Exemption

Packages **maintained by this repo’s author** (the `github.com/jlevy` org, e.g.
`flowmark` / `flowmark-rs`, `flexdoc`) are **exempt from the 14-day cool-off**. The
trust basis the cool-off substitutes for is already satisfied: the source is
author-controlled and auditable, and the published artifact is verified against its git
tag. First-party deps are still **pinned to an exact version**, and any in-window
override stays **surgical** (per-invocation, never relaxing the global cool-off).

This is a standing exemption, recorded here rather than re-approved per bump.

## Active Exceptions

- **`flowmark-rs@0.3.1`**: first-party (see above).
  Published 2026-05-30; adopted 2026-06-02 while inside the 14-day window.
  Applied surgically in the [Makefile](Makefile) via
  `uvx --exclude-newer-package 'flowmark-rs=2026-06-02'`, which overrides the cool-off
  for this one package only and does not touch global uv config.
  Reviewed-by: Joshua Levy.
- **`flexdoc==0.2.0`**: first-party (see above).
  Published 2026-06-14 (UTC); adopted the same day in PR #30, inside the 14-day window
  (0.1.0 was adopted the same way on 2026-06-13). flexdoc is the document-layer subset
  extracted from `chopdiff` (`TextDoc` → `FlexDoc`); pprose depends on it directly and
  not on `chopdiff`, since metrics.py uses only the document model, not chopdiff’s
  diff/windowed-transform machinery.
  Pinned exact in [tools/pprose/pyproject.toml](tools/pprose/pyproject.toml).
  The in-window `[tool.uv] exclude-newer-package` bridge was removed once 0.2.0 aged out
  of the window (2026-06-28). For any future in-window first-party adoption, note the
  value must be a full RFC 3339 timestamp (`{ pkg = "2026-06-15T00:00:00Z" }`): uv (as
  of 0.8.17) rejects date-only values in `pyproject.toml` with only a warning and then
  ignores the whole `[tool.uv]` table, so the bridge silently never applies.
  CI installs from the committed `uv.lock`. Reviewed-by: Joshua Levy.

## Known Gap

- **npm lifecycle scripts are not globally blocked.** The headline control
  (`ignore-scripts=true`) is not set because `lefthook`’s npm package relies on a
  `postinstall` to fetch its binary, and npm has no clean per-package script allowlist
  (unlike pnpm’s `allowBuilds`). The residual risk is bounded by the small, pinned,
  lockfiled JS dependency set (`@biomejs/biome`, `lefthook`) and the cool-off.
  Revisit by migrating the JS tooling to pnpm (`minimumReleaseAge` + `allowBuilds`) if
  the dependency surface grows.

## References

- `tbd guidelines supply-chain-hardening`: the concise cross-ecosystem policy.
- <https://github.com/jlevy/supply-chain-hardening>: full playbooks, audit script,
  incident watch list, and CI/publish-side hardening.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
