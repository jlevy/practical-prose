# Regenerating the README Eval Screenshots

The two evaluation cards in the top-level [README.md](../../README.md) live in
[images/](../../images/):

- `images/as-we-may-think.png` — Vannevar Bush, “As We May Think” (The Atlantic, 1945)
- `images/apple-media-services-terms.png` — Apple Media Services Terms

The **scores** for each card are committed as `.eval.md` files in
[evals/readme-cards/](../../evals/readme-cards/), and the **PNGs** are rendered from
those. Scoring (an LLM call) and rendering (look-and-feel) are deliberately separate:

- Change the **look and feel** (design tokens, `print.css`, the card template)?
  Run **Flow A — Re-render** only.
  No API call, no score change — the cards just pick up the new styling.
  This is the common case.
- Want **fresh scores**? Run **Flow B — Re-score** to regenerate the committed
  `.eval.md`, then run Flow A to re-render.

This is a development workflow, not part of the shipped package: it shells out to a
locally installed Chrome plus `pdftoppm` and `magick`, so it adds no Python or JS
dependencies to `pprose`.

## Prerequisites

- Google Chrome (headless HTML → PDF) — both flows.

- Poppler (`pdftoppm`) and ImageMagick (`magick`) for PDF → trimmed PNG — both flows:

  ```bash
  brew install poppler imagemagick
  ```

- An `ANTHROPIC_API_KEY` in `.env` (or the environment) — **Flow B only** (scoring).

## Flow A — Re-render (look-and-feel changes)

Rebuilds the PNGs from the committed `evals/readme-cards/*.eval.md` with the current
styles. No scoring, so the numbers on the cards do not change.
Run this after editing the design system, `print.css`, or the card template (regenerate
the design tokens first with `uv run python tools/design-system/generate.py` if you
changed `design-system.yaml`).

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO="$(git rev-parse --show-toplevel)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
WORK="$(mktemp -d)"
cd "$REPO"

for stem in as-we-may-think apple-media-services-terms; do
  uv run --project tools/pprose pprose render "evals/readme-cards/$stem.eval.md" \
    -o "$WORK/$stem.html"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
    --virtual-time-budget=3000 --print-to-pdf="$WORK/$stem.pdf" "file://$WORK/$stem.html"
  pdftoppm -png -r 200 -f 1 -l 1 "$WORK/$stem.pdf" "$WORK/$stem-page"
  magick "$WORK/$stem-page-1.png" -trim +repage "images/$stem.png"
  echo "rendered images/$stem.png"
done
```

The print stylesheet
([print.css](../../tools/pprose/src/pprose/render_html/styles/print.css)) forces the
light theme and hides the theme toggle and hover panels, so the printed page is clean.

## Flow B — Re-score (refresh the numbers)

Regenerates the committed `.eval.md` from the source documents in
[example-texts/](../../example-texts/), then you run Flow A to re-render.
Scores depend on the model and vary slightly between runs, so re-scoring will shift the
numbers — update the README caption to match.

```bash
#!/usr/bin/env bash
set -euo pipefail
REPO="$(git rev-parse --show-toplevel)"
cd "$REPO"
set -a; source .env; set +a   # ANTHROPIC_API_KEY
PP() { uv run --project tools/pprose pprose "$@"; }

# label|source-path|stem
DOCS=(
  "As We May Think|example-texts/as-we-may-think.md|as-we-may-think"
  "Apple Media Services Terms|example-texts/apple-media-services-terms.md|apple-media-services-terms"
)
for entry in "${DOCS[@]}"; do
  IFS='|' read -r label src stem <<<"$entry"
  PP report from-metrics "$src" --label "$label" \
    --evaluator "Claude Opus 4.8 (pprose demo)" --method subagent \
    --out "evals/readme-cards/$stem.eval.md"
  PP score "evals/readme-cards/$stem.eval.md" --model opus --allow-misaligned \
    --evaluator "Claude Opus 4.8 (pprose demo)"
done
# Now run Flow A to re-render the PNGs from the refreshed .eval.md.
```

`--model opus` resolves to the current default (Anthropic Claude Opus).
`pprose score` occasionally returns a sub-5 score without a matching rule citation,
which trips the alignment check; `--allow-misaligned` writes the report anyway (fine for
a demo — the scores are the model’s real assessment).

## Notes

- The captured PNGs are about 1100 × 1635 px at 200 dpi.
  To regenerate at a different resolution, change `-r 200` in `pdftoppm`.
- The interactive HTML (with theme toggle and hover detail panels) is the on-screen
  experience; the print path is only for static snapshots.
- The cards show per-group means and an `Assessed: N/20` count, not a single
  cross-dimension average: `overall_mean` is reductive and not comparable across genres
  (N/A dimensions drop out of any average, so a document that doesn’t engage many
  dimensions can outscore a richer one).
  The Apple terms, for instance, leave several Reasoning and Judgment dimensions N/A — a
  contract states terms rather than arguing or weighing them.
  See the “Scores are reductive” note in
  [practical-prose-rubric.md](../practical-prose-rubric.md).

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
