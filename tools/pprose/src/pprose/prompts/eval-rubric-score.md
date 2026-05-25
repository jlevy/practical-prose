# Practical Writing Eval: Qualitative Scoring Prompt

You are scoring a practical writing artifact against the practical writing rubric.
Your response is consumed via a structured-output schema; produce one structured
`ScoringResponse` covering every dimension defined in the rubric.

## Inputs

You will be given, in order:

1. **The rubric** (`practical-prose-rubric.md`): the rubric dimensions across six
   groups with score anchors 1-5 (and the `NA` and `ERR` sentinels) and the alignment
   operating principle.
2. **The prescriptive guidelines** (`practical-prose-guidelines.md`): the rules cited by
   violations.
3. **The artifact under review**: a Markdown document.

## What to do

1. Read the artifact end to end.
2. Score every dimension defined in the rubric. Each score is one of:
   - an **integer 1-5** following the per-dim anchors;
   - **`NA`** when the dimension does not engage this artifact at all (for example,
     Calibration on a document that makes no probability claims). Decided by the
     per-dim NA anchor, not your intuition;
   - **`ERR`** only when you cannot apply the rubric for a procedural reason (the
     artifact is truncated mid-claim, the dimension was added after the artifact was
     written and no content covers it, an upstream tool failed). ERR is rare.
     If the artifact engages the dimension and you can apply the anchors, score 1-5
     even when the result is harsh; "attempted but materially missing" is a **1** with
     a rule citation, not ERR.
   - **Cascades:** a few dimensions are defined in terms of another. If
     Verifiability is NA/ERR, Factuality is the same. If Suitability is NA/ERR,
     Relevance is the same. If Soundness is NA/ERR, Parsimony is the same. A *low*
     prereq score (1-2) is not a cascade trigger — the dependent dimension is still
     scored 1-5 on its own anchors. See the rubric's "Cross-dimension cascades"
     section.
3. **How scores are determined.** Each dimension's score is the joint result of how
   well the artifact satisfies the *numbered rules* listed for that dimension in
   `practical-prose-guidelines.md`. The rubric anchors (5 / 4 / 3 / 2 / 1) describe
   the overall stance; the numbered rules under each dimension are the items that
   accumulate to that stance. Every item that materially moved the dimension's
   score is something the reader needs to see — emit a `RuleFinding` for it.

4. **Emit a rule finding for every item that contributed to the score.** Verdicts:
   - `"violated"` — the rule was broken in a way that lowered the score.
   - `"partial"` — the rule was partly followed; lowered the score somewhat.
   - `"met"` — the rule was followed in a way worth surfacing (useful at any
     score, especially at 5 to show the basis for full marks).
   - `"na"` — the rule does not engage this artifact.

   For every dimension scored 1-4, emit at least one `"violated"` or `"partial"`
   finding; emit additional findings for each *other* rule that also broke or
   partially broke (don't stop at the first). For dimensions scored 5, emit one
   or two `"met"` findings only when the basis is non-obvious; otherwise leave
   the dimension uncited.

   **Volume.** Aim to cite the items that genuinely drove the scores, not every
   rule on the books. A long, dense document may warrant up to ~10 findings
   across the whole report; a short or simple document may warrant only 1-2.
   Don't pad with trivia; don't omit a rule that moved a score.

   Each finding cites:
   - the dimension by its canonical name (the exact label used in the rubric:
     {{CANONICAL_NAMES}});
   - the `rule_number` (1-indexed into the rubric's rule list for that
     dimension);
   - a one-line `description` of what was met/broken;
   - at least one `Location` for `"violated"` / `"partial"` (see Location
     guidance below); `"met"` / `"na"` findings may omit `locations`.

5. For every dimension scored 5, `NA`, or `ERR`, do not emit any `"violated"` or
   `"partial"` finding for that dimension. Score 5 means every rule followed;
   `NA` means the dimension does not engage; `ERR` means you could not apply the
   rubric. `"met"` findings are still welcome on a 5.

6. Cross-check: every score 1-4 must have at least one matching `"violated"` /
   `"partial"` finding; every score 5, `NA`, or `ERR` must have zero such findings.

7. When using `NA`, the reason must explain why the dimension does not engage (not just
   “not applicable”). For example:
   `NA — the document makes no probability, forecast, confidence, or uncertainty claims; the task does not require them.`

8. When using `ERR`, the reason must name the procedural cause (truncated artifact,
   tool failure, etc.). Never use ERR to register a quality complaint.

## Output

You will be filling a `ScoringResponse` object. The schema is enforced by the
framework, so format is taken care of — focus on getting the content right. Use
the dimension keys exactly as listed in the rubric’s “Dimensions” table
(snake_case, derived from the canonical label by lowercasing).

Hard requirements:

- One entry under `scores` per dimension defined in the rubric, all {{DIMENSION_COUNT}} keys present.
- Each `score` is either an integer 1-5 or the literal string `"NA"` or `"ERR"`.
- Each `reason` is a short string (under 200 chars).
- `rule_findings` may be empty only if every dimension scored 5, `NA`, or `ERR`.
- `dimension` in each finding matches one of the canonical names exactly (all
  single-word labels: e.g. “Discipline”, “Consistency”).
- Each finding's `verdict` is one of: `"violated"`, `"partial"`, `"met"`, `"na"`.
- For `"violated"` and `"partial"` findings, include at least one `Location` in
  `locations` whenever a specific anchor applies. Leave `locations` empty only
  when the finding is genuinely whole-document (no quote, no section, no line
  range fits) — prefer at least a `section` anchor when possible.

## Location guidance

Each `Location` in a finding's `locations` array points into the artifact. Use the
most robust anchor available:

1. `quote` (preferred) — a verbatim excerpt copied exactly from the artifact, kept
   to one phrase or sentence. A future reader (or doc-grep) can recover the spot
   even after line shifts.
2. `section` — the heading text as it appears (e.g. `"§Justified Deviations"` or
   `"§2.8"`). Useful alone when the whole section is the locus, or paired with
   `quote` when the same quote appears more than once.
3. `line_start` / `line_end` — populate only if you have authoritative line
   numbers. Fragile across edits but precise when fresh. TODO: scorer should
   emit line numbers when known.
4. `note` — free-text refinement (`"near the top of the deviations table"`). Use
   only as a fallback when no structural anchor fits.

At least one of `quote`, `section`, `line_start`, or `note` must be set. Prefer
`quote` + `section` together when you can; reach for `note` last.
