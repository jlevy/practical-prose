# Practical Writing Eval: Qualitative Scoring Prompt

You are scoring a practical writing artifact against the practical writing rubric.
Your output is consumed by a script: it must include a single JSON block in the exact
shape specified at the bottom.

## Inputs

You will be given, in order:

1. **The rubric** (`practical-prose-rubric.md`): the rubric dimensions across five
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
3. For every dimension scored 1-4, identify at least one specific guideline-rule
   violation. Cite:
   - the dimension by its canonical name (the exact label used in the rubric:
     {{CANONICAL_NAMES}}),
   - the `rule_number` (the integer in `practical-prose-guidelines.md` for that
     dimension’s rule),
   - a one-line description,
   - a location pointer (line range like `L412-418`, section heading like `§2.8`, or
     quoted phrase).
4. For every dimension scored 5, `NA`, or `ERR`, do not cite any violation for that
   dimension. Score 5 means every rule followed; `NA` means the dimension does not
   engage; `ERR` means you could not apply the rubric.
5. Cross-check: every score 1-4 must have at least one matching violation; every score
   5, `NA`, or `ERR` must have zero matching violations.
6. When using `NA`, the reason must explain why the dimension does not engage (not just
   “not applicable”). For example:
   `NA — the document makes no probability, forecast, confidence, or uncertainty claims; the task does not require them.`
7. When using `ERR`, the reason must name the procedural cause (truncated artifact,
   tool failure, etc.). Never use ERR to register a quality complaint.

## Output format

Print a brief reasoning paragraph (under 200 words) summarizing your overall read of the
artifact. Then emit a single JSON code fence with the shape below.
Use the exact dimension keys listed in the rubric’s “Dimensions” table (snake_case,
derived from the canonical label by lowercasing).

{{SCORES_JSON}}

Hard requirements:

- One score entry per dimension defined in the rubric, all {{DIMENSION_COUNT}} keys present, snake_case.
- Each `score` is either an integer 1-5 or the literal string `"NA"` or `"ERR"` (no 0).
- Each `reason` is a short string (under 200 chars).
- `violations` may be empty only if every dimension scored 5, `NA`, or `ERR`.
- `dimension` in each violation matches one of the canonical names exactly (all
  single-word labels: e.g. “Discipline”, “Consistency”).
- Output exactly one JSON code fence; the parser extracts the first ```json block.
