---
type: is
id: is-01ktqhds86ewzmccb5asxd2h6b
title: "Print CSS: snapshot-fit page sizing (tight card, no excess margin)"
kind: task
status: open
priority: 3
version: 1
labels: []
dependencies: []
created_at: 2026-06-10T01:12:53.764Z
updated_at: 2026-06-10T01:12:53.764Z
---
Deferred from the eval-screenshot work. The print-to-PDF path (print.css) currently paginates to letter, so the card sits on a page with margins that must be cropped with 'magick -trim', and short cards leave an empty 2nd page. Add a snapshot-oriented @page mode that sizes the page to the card with minimal margin (single page, right dimensions), so print-to-PDF output needs no trimming. See docs/project/eval-screenshots.runbook.md.
