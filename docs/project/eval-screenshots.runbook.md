# Regenerating the README Eval Screenshots

The two evaluation cards in the top-level [README.md](../../README.md) live in
[images/](../../images/):

- `images/as-we-may-think.png` — Vannevar Bush, “As We May Think” (The Atlantic, 1945)
- `images/apple-media-services-terms.png` — Apple Media Services Terms

Both are rendered from source documents in [example-texts/](../../example-texts/) and
captured as light-mode PNGs.
This is a development workflow, not part of the shipped package: it shells out to a
locally installed Chrome plus `pdftoppm` and `magick`, so it adds no Python or JS
dependencies to `pprose`.

## Prerequisites

- An `ANTHROPIC_API_KEY` in `.env` (or the environment) for the scoring step.

- Google Chrome (used headless for HTML → PDF).

- Poppler (`pdftoppm`) and ImageMagick (`magick`) for PDF → trimmed PNG:

  ```bash
  brew install poppler imagemagick
  ```

## Pipeline

The flow is `metrics → report → score → render → snapshot`:

1. `pprose report from-metrics` builds an eval stub with deterministic metrics.
2. `pprose score` fills the rubric scores via an LLM. The model occasionally returns a
   sub-5 score without a matching rule citation, which trips the alignment check; pass
   `--allow-misaligned` to write the report anyway (fine for a demo — scores are the
   model’s real assessment).
3. `pprose render` emits a static HTML card.
4. Chrome prints it to PDF. The print stylesheet
   ([print.css](../../tools/pprose/src/pprose/render_html/styles/print.css)) forces the
   light theme and hides the theme toggle and hover panels, so the printed page is
   clean.
5. `pdftoppm` rasterizes page 1 and `magick -trim` crops the surrounding margin.

Scores depend on the model and will vary slightly between runs.

## Script

Run from the repo root.
Edit `MODEL` or the document list as needed.

```bash
#!/usr/bin/env bash
set -euo pipefail

REPO="$(git rev-parse --show-toplevel)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
MODEL="anthropic:claude-opus-4-8"
WORK="$(mktemp -d)"
mkdir -p "$REPO/images"

# label|source-path (label is the card title)
DOCS=(
  "As We May Think|example-texts/as-we-may-think.md|as-we-may-think"
  "Apple Media Services Terms|example-texts/apple-media-services-terms.md|apple-media-services-terms"
)

cd "$REPO/tools/pprose"
for entry in "${DOCS[@]}"; do
  IFS='|' read -r label src stem <<<"$entry"
  uv run pprose report from-metrics "$REPO/$src" --label "$label" \
    --evaluator "Claude Opus 4.8 (pprose demo)" --method subagent \
    --out "$WORK/$stem.eval.md"
  uv run pprose score "$WORK/$stem.eval.md" --model "$MODEL" --allow-misaligned \
    --evaluator "Claude Opus 4.8 (pprose demo)"
  uv run pprose render "$WORK/$stem.eval.md" -o "$WORK/$stem.html"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer \
    --virtual-time-budget=3000 \
    --print-to-pdf="$WORK/$stem.pdf" "file://$WORK/$stem.html"
  pdftoppm -png -r 200 -f 1 -l 1 "$WORK/$stem.pdf" "$WORK/$stem-page"
  magick "$WORK/$stem-page-1.png" -trim +repage "$REPO/images/$stem.png"
  echo "wrote images/$stem.png"
done
```

## Notes

- The captured PNGs are about 1100 × 1635 px at 200 dpi.
- To regenerate at a different resolution, change `-r 200` in `pdftoppm`.
- The interactive HTML (with theme toggle and hover detail panels) is the on-screen
  experience; the print path is only for static snapshots.

## Interpreting the scores (don’t headline `overall_mean`)

`overall_mean` is reductive and **not comparable across genres**. NA dimensions are
excluded from the mean rather than scored low, so a document that legitimately doesn’t
engage many dimensions can outscore a richer one.
In this exact pair the Apple terms (~4.3, with 5 NA dimensions — all of Judgment and two
of Reasoning, since a contract neither calibrates claims nor weighs alternatives)
outrank Bush’s essay (~3.6, all 20 dimensions scored) on the mean alone, even though the
essay is the stronger piece of writing.
Present the per-dimension and per-group view (what the cards show); treat `overall_mean`
as a rough within-genre signal at most.
See the “Scores are reductive” note in
[practical-prose-rubric.md](../practical-prose-rubric.md).
