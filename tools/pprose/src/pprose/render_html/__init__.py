"""Static-HTML rendering of practical-prose eval reports.

Public API:
  - `renderer.render(input_path, opts) -> str`: input-kind dispatch entry point.
  - `renderer.render_eval_report(report, opts) -> str`: render an EvalReport directly.
  - `renderer.detect_kind(path) -> str | None`: detect the input kind.
  - `cli.main(argv) -> int`: argparse entry point wired into `pprose render`.

Bundled assets (templates, styles, icons) live next to this module and are
loaded via Path(__file__).parent so they ship with the wheel.
"""

from __future__ import annotations
