#!/usr/bin/env python3
"""One-shot refactor: delete duplicated inline CSS+JS from the workbench.

Phase 1b of epic pp-ict2. The workbench at
tools/explorations/visual-design/dimension-visualizations.html still
carries inline copies of the .bi-* CSS, the bi-card / tip-panel JS
function definitions, and the .theme-toggle CSS — the same content the
shared render-components/ files now own. After this script runs, the
workbench sources those from the shared <link>/<script src> imports
that were added in Phase 1a.

Steps:
  1. Delete top-level CSS rules from the inline <style> whose primary
     selector starts with `.bi-`, `.grp-icon`, or `.theme-toggle` (the
     `.surface-toggle` rules stay — they're workbench-only).
  2. Delete top-level function declarations matching the shared names
     (biCard, biDim9B, _biDimPrep, groupAvgChip, _readScoreAlphaStep,
     dimColorMix, scoreColor, segmentAlpha, setupTipPanel) from the
     workbench's main inline <script>. KEEP: `el`, `groupIcon`, `biDim`
     (used by other visuals or 9A only).
  3. Rewire the workbench's main script:
       - Right after `dims` + `groups` + `rubric` are populated, insert
         a destructuring assignment that pulls the shared API from
         `PracticalProseBiCard.makeApi({groups, dimensions: dims})`.
       - Replace `setupTipPanel(detailEl, assessEl)` calls with a call
         to `PracticalProseTipPanels.mount(detailEl, assessEl, data,
         biCardApi, { scope: layout })`.

Run once; commit the resulting workbench HTML. The script is idempotent
(re-running on already-refactored input is a no-op for deletions).

Usage:
    uv run python tools/explorations/visual-design/_refactor_workbench.py
"""

from __future__ import annotations

import re
import sys
from collections.abc import Iterator
from pathlib import Path

WORKBENCH = (
    Path(__file__).resolve().parent / "dimension-visualizations.html"
)

# Top-level CSS rules to delete (selector prefix match on the first
# selector group). Patterns are applied to each rule's first selector
# group's first compound (e.g. ".bi-card", ".grp-icon", ".theme-toggle").
CSS_DELETE_PREFIXES = (".bi-", ".grp-icon", ".theme-toggle")

# Function names to delete from the main inline <script> (top-level
# definitions only). The workbench's `el`, `groupIcon`, and `biDim`
# stay because they're consumed by other visualizations (Visual 8 etc.)
# or by Visual 9A (workbench-only).
JS_DELETE_FN_NAMES = (
    "biCard",
    "biDim9B",
    "_biDimPrep",
    "groupAvgChip",
    "_readScoreAlphaStep",
    "dimColorMix",
    "scoreColor",
    "segmentAlpha",
    "setupTipPanel",
)


# ─── CSS parser (brace-depth state machine, shared with sync script) ───────


def iter_top_level_rules(css: str) -> Iterator[tuple[int, int, str]]:
    """Yield (start, end, text) for each top-level CSS rule incl. @-rules.

    Tracks string + comment escapes. Returned (start, end) are absolute
    indices in the input; text is the raw rule including any preceding
    comment and whitespace that came right before the selector.
    """
    i, n = 0, len(css)
    rule_start = 0
    while i < n:
        c = css[i]
        if c in ('"', "'"):
            q = c
            i += 1
            while i < n and css[i] != q:
                if css[i] == "\\" and i + 1 < n:
                    i += 2
                else:
                    i += 1
            i += 1
            continue
        if c == "/" and i + 1 < n and css[i + 1] == "*":
            end = css.find("*/", i + 2)
            i = (end + 2) if end != -1 else n
            continue
        if c == "{":
            depth = 1
            j = i + 1
            while j < n and depth > 0:
                cc = css[j]
                if cc in ('"', "'"):
                    q = cc
                    j += 1
                    while j < n and css[j] != q:
                        if css[j] == "\\" and j + 1 < n:
                            j += 2
                        else:
                            j += 1
                    j += 1
                    continue
                if cc == "/" and j + 1 < n and css[j + 1] == "*":
                    end = css.find("*/", j + 2)
                    j = (end + 2) if end != -1 else n
                    continue
                if cc == "{":
                    depth += 1
                elif cc == "}":
                    depth -= 1
                j += 1
            yield rule_start, j, css[rule_start:j]
            while j < n and css[j] in " \t\r\n":
                j += 1
            rule_start = j
            i = j
            continue
        i += 1


def rule_first_selector_compound(rule_text: str) -> str:
    """Extract a rule's first selector compound (e.g. ".bi-card" from
    ".bi-card .doc-kicker { ... }").

    Strips leading comments + whitespace + the @-prelude. For nested
    rules (@media), returns the @-prefix itself; the deletion path then
    inspects the inner rules.
    """
    text = rule_text.lstrip()
    while text.startswith("/*"):
        end = text.find("*/")
        if end == -1:
            break
        text = text[end + 2 :].lstrip()
    selector = text.split("{", 1)[0].strip()
    if selector.startswith("@"):
        return selector
    first = selector.split(",", 1)[0].strip()
    return first.split()[0] if first else ""


def rule_inner_selectors(rule_text: str) -> list[str]:
    """For @media rules, return the first selector of each inner rule."""
    sel = rule_first_selector_compound(rule_text)
    if not sel.startswith("@media"):
        return [sel]
    body_start = rule_text.find("{") + 1
    body_end = rule_text.rfind("}")
    body = rule_text[body_start:body_end]
    out: list[str] = []
    for _s, _e, t in iter_top_level_rules(body):
        inner = rule_first_selector_compound(t)
        if inner:
            out.append(inner)
    return out


def is_shared_rule(rule_text: str) -> bool:
    """Decide whether a rule is sourced from a shared render-component."""
    selectors = rule_inner_selectors(rule_text)
    if not selectors:
        return False
    # If ALL inner selectors point at a shared prefix, route the whole
    # rule to deletion. If only some, keep — the rule does double duty.
    return all(
        any(s.startswith(p) for p in CSS_DELETE_PREFIXES) for s in selectors
    )


def strip_shared_css_rules(style_block: str) -> tuple[str, int]:
    """Delete rules from `style_block` that match a shared selector.

    Returns (new_style_block, count_deleted).
    """
    pieces: list[str] = []
    cursor = 0
    deleted = 0
    for start, end, text in iter_top_level_rules(style_block):
        if is_shared_rule(text):
            # Push everything before this rule's start; skip the rule.
            pieces.append(style_block[cursor:start])
            cursor = end
            # Also swallow a single trailing blank line if present.
            while cursor < len(style_block) and style_block[cursor] in " \t":
                cursor += 1
            if cursor < len(style_block) and style_block[cursor] == "\n":
                cursor += 1
            deleted += 1
    pieces.append(style_block[cursor:])
    return "".join(pieces), deleted


# ─── JS function-definition deletion ───────────────────────────────────────


def _find_matching_brace(text: str, open_idx: int) -> int:
    """Given the index of an opening `{` in `text`, return the index of
    its matching `}` (tracking strings, template literals, and comments).
    """
    n = len(text)
    depth = 1
    i = open_idx + 1
    while i < n and depth > 0:
        c = text[i]
        # Strings (single, double, backtick).
        if c in ('"', "'", "`"):
            q = c
            i += 1
            while i < n and text[i] != q:
                if text[i] == "\\" and i + 1 < n:
                    i += 2
                elif q == "`" and text[i] == "$" and i + 1 < n and text[i + 1] == "{":
                    # Template literal interpolation; inside is JS.
                    i += 2
                    interp = 1
                    while i < n and interp > 0:
                        if text[i] == "{":
                            interp += 1
                        elif text[i] == "}":
                            interp -= 1
                        i += 1
                else:
                    i += 1
            i += 1
            continue
        # Block comment.
        if c == "/" and i + 1 < n and text[i + 1] == "*":
            end = text.find("*/", i + 2)
            i = (end + 2) if end != -1 else n
            continue
        # Line comment.
        if c == "/" and i + 1 < n and text[i + 1] == "/":
            end = text.find("\n", i + 2)
            i = (end + 1) if end != -1 else n
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
        i += 1
    return i  # index just past the closing brace


def strip_top_level_function(script: str, name: str) -> tuple[str, int]:
    """Delete the top-level `function NAME(...) { ... }` from a JS body.

    Top-level = the body's outermost scope. We use the workbench's
    indentation convention: top-level functions sit at 6-space indent
    (`^      function NAME`). The matching closing brace is also at the
    6-space indent. We also pull in a preceding block comment within
    ~10 lines so the rule's documentation goes with the rule.

    Returns (new_script, n_deleted).
    """
    # The workbench's inline <script> is itself indented. We trim a
    # left-margin so the deletion patterns work; restore on write.
    pattern = re.compile(
        rf"^      function {re.escape(name)}\b", re.MULTILINE
    )
    out = script
    n_deleted = 0
    while True:
        m = pattern.search(out)
        if not m:
            break
        start = m.start()
        open_brace = out.find("{", m.end())
        if open_brace == -1:
            break
        close_brace = _find_matching_brace(out, open_brace)
        # Optionally swallow a preceding block comment immediately above.
        prelude_start = start
        # Walk backwards over whitespace lines.
        i = start
        while i > 0 and out[i - 1] in " \t":
            i -= 1
        # Now i is at the column-0 start of the function's line. Look
        # back for blank line(s) and a leading /* ... */ comment block.
        scan = i
        # Skip a leading blank line.
        if scan > 0 and out[scan - 1] == "\n":
            # Scan further back for the `*/` of a preceding comment.
            probe = scan - 2
            # Find the last non-blank line ending.
            while probe > 0 and out[probe] in " \t":
                probe -= 1
            if probe > 1 and out[probe - 1] == "*" and out[probe] == "/":
                # Find the matching `/*` going backwards.
                open_comment = out.rfind("/*", 0, probe - 1)
                if open_comment != -1:
                    # Make sure the comment starts at column 0 of its line.
                    line_start = out.rfind("\n", 0, open_comment) + 1
                    leading = out[line_start:open_comment]
                    if leading.strip() == "":
                        prelude_start = line_start
        # Trim a trailing newline after the closing brace.
        end = close_brace
        while end < len(out) and out[end] in " \t":
            end += 1
        if end < len(out) and out[end] == "\n":
            end += 1
        out = out[:prelude_start] + out[end:]
        n_deleted += 1
    return out, n_deleted


# ─── Workbench rewire ──────────────────────────────────────────────────────


def insert_rewire_after_rubric_population(script: str) -> str:
    """Insert the makeApi destructure right after the rubric is loaded.

    Looks for the marker line that the workbench uses to signal
    'rubric has finished populating' — the closing of the
    `for (const g of rubricDoc.groups || []) { ... }` block that walks
    the rubric YAML. We insert after that block so `groups`, `dims`,
    `rubric`, and `biRealDocs` are all populated.

    Inserts (idempotent: skip if already present):

        // Phase 1b rewire — source shared bi-card helpers + tip panels
        // from tools/render-components/. Verbatim copies (kept in sync
        // by tools/pprose/devtools/sync_render_html_styles.py).
        const biCardApi = PracticalProseBiCard.makeApi({
          groups,
          dimensions: dims,
        });
        const {
          biCard,
          biDim9B,
          _biDimPrep,
          groupAvgChip,
          dimColorMix,
          scoreColor,
          _readScoreAlphaStep,
          segmentAlpha,
        } = biCardApi;
        function setupTipPanel(detailEl, assessEl, opts = {}) {
          return PracticalProseTipPanels.mount(
            detailEl,
            assessEl,
            { groups, dimensions: dims, rubric, docs: biRealDocs },
            biCardApi,
            opts,
          );
        }
    """
    sentinel = "// Phase 1b rewire — source shared bi-card helpers"
    if sentinel in script:
        return script  # idempotent
    # Insertion point: right before the comment "/* Canonical baseline evals"
    # is the safe spot — but simpler: insert right before the
    # first `const _groupById = (id) =>` (which begins the bi-card layout
    # section that consumes biLeftGroups/biRightGroups + dims).
    marker = "const _groupById = (id) => groups.find((g) => g.id === id);"
    idx = script.find(marker)
    if idx == -1:
        print(
            f"WARN: could not find rewire marker {marker!r}; "
            "skipping inline rewire insertion.",
            file=sys.stderr,
        )
        return script

    # The line above `_groupById` should be at the same indent (6 spaces).
    line_start = script.rfind("\n", 0, idx) + 1
    indent = script[line_start:idx]
    # Drop the indent line (likely all whitespace from `\n      `) for
    # the insertion's leading newline.

    insertion = (
        f"{indent}{sentinel}\n"
        f"{indent}// (Phase 1b of epic pp-ict2 — see\n"
        f"{indent}// docs/project/specs/active/plan-2026-05-31-shared-render-components.md.)\n"
        f"{indent}const biCardApi = PracticalProseBiCard.makeApi({{\n"
        f"{indent}  groups,\n"
        f"{indent}  dimensions: dims,\n"
        f"{indent}}});\n"
        f"{indent}const {{\n"
        f"{indent}  biCard,\n"
        f"{indent}  biDim9B,\n"
        f"{indent}  _biDimPrep,\n"
        f"{indent}  groupAvgChip,\n"
        f"{indent}  dimColorMix,\n"
        f"{indent}  scoreColor,\n"
        f"{indent}  _readScoreAlphaStep,\n"
        f"{indent}  segmentAlpha,\n"
        f"{indent}}} = biCardApi;\n"
        f"{indent}// Tip-panel adapter: workbench `setupTipPanel(detailEl, assessEl)` is now a\n"
        f"{indent}// thin wrapper over the shared PracticalProseTipPanels.mount() that scopes\n"
        f"{indent}// hover to each visualization's layout via opts.scope (per-viz, not document).\n"
        f"{indent}function setupTipPanel(detailEl, assessEl, opts = {{}}) {{\n"
        f"{indent}  return PracticalProseTipPanels.mount(\n"
        f"{indent}    detailEl,\n"
        f"{indent}    assessEl,\n"
        f"{indent}    {{ groups, dimensions: dims, rubric, docs: biRealDocs }},\n"
        f"{indent}    biCardApi,\n"
        f"{indent}    opts,\n"
        f"{indent}  );\n"
        f"{indent}}}\n"
        f"\n"
    )
    return script[:line_start] + insertion + script[line_start:]


# ─── Main ──────────────────────────────────────────────────────────────────


def main() -> int:
    html = WORKBENCH.read_text(encoding="utf-8")

    # 1) Strip shared CSS rules from the first <style> block.
    style_match = re.search(r"<style>(.*?)</style>", html, re.DOTALL)
    if not style_match:
        print("error: no <style> block", file=sys.stderr)
        return 1
    style_body = style_match.group(1)
    new_style_body, css_deleted = strip_shared_css_rules(style_body)
    html = html[: style_match.start(1)] + new_style_body + html[style_match.end(1) :]

    # 2) Strip shared function definitions from the main inline <script>.
    # The main script is the LAST <script>...</script> (without a src=).
    script_matches = list(
        re.finditer(r"<script(?:\s[^>]*)?>(.*?)</script>", html, re.DOTALL)
    )
    inline_blocks = [
        m
        for m in script_matches
        if not re.search(r"<script\s[^>]*\bsrc=", html[m.start() : m.end()])
    ]
    inline_blocks.sort(key=lambda m: len(m.group(1)), reverse=True)
    if not inline_blocks:
        print("error: no inline <script> block", file=sys.stderr)
        return 1
    main_script_match = inline_blocks[0]
    main_script = main_script_match.group(1)
    js_deletions = 0
    for name in JS_DELETE_FN_NAMES:
        main_script, n = strip_top_level_function(main_script, name)
        if n:
            print(f"deleted inline function: {name}  ({n}x)")
            js_deletions += n
        else:
            print(f"(no inline definition for {name} — already gone)")

    # 3) Insert the rewire (biCardApi destructure + setupTipPanel adapter).
    main_script = insert_rewire_after_rubric_population(main_script)

    html = (
        html[: main_script_match.start(1)]
        + main_script
        + html[main_script_match.end(1) :]
    )

    WORKBENCH.write_text(html, encoding="utf-8")
    print(
        f"\nrefactored {WORKBENCH.name}: "
        f"deleted {css_deleted} CSS rule(s), {js_deletions} JS function(s)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
