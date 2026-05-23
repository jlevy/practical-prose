# Practical Writing Eval: Qualitative Scoring Prompt

You are scoring a practical writing artifact against the practical writing rubric.
Your output is consumed by a script: it must include a single JSON block in the exact
shape specified at the bottom.

## Inputs

You will be given, in order:

1. **The rubric** (`practical-prose-rubric.md`): the rubric dimensions across five
   groups with score anchors 0-5 (and `NA`) and the alignment operating principle.
2. **The prescriptive guidelines** (`practical-prose-guidelines.md`): the rules cited by
   violations.
3. **The artifact under review**: a Markdown document.

## What to do

1. Read the artifact end to end.
2. Score every dimension defined in the rubric on the 0-5 scale, following the rubric
   anchors. Score 0 means “applicable but unassessable”; use only when content is missing
   for that dimension. `NA` means the dimension does not apply to this artifact at all
   (for example, Calibration on a document that makes no probability claims).
3. For every dimension scored 1-4, identify at least one specific guideline-rule
   violation. Cite:
   - the dimension by its canonical name (the exact label used in the rubric:
     Suitability, Scope, Breadth, Depth, Clarity, Coherence, Concision, Organization,
     Consistency, Formatting, Verifiability, Factuality, Relevance, Discipline,
     Soundness, Precision, Parsimony, Calibration, Fairness, Robustness),
   - the `rule_number` (the integer in `practical-prose-guidelines.md` for that
     dimension’s rule),
   - a one-line description,
   - a location pointer (line range like `L412-418`, section heading like `§2.8`, or
     quoted phrase).
4. For every dimension scored 5, 0, or `NA`, do not cite any violation for that
   dimension. Score 5 means every rule followed; 0 means applicable but unassessable;
   `NA` means the dimension does not apply.
5. Cross-check: every score 1-4 must have at least one matching violation; every score
   5, 0, or `NA` must have zero matching violations.
6. When using `NA`, the reason must explain why the dimension does not apply (not just
   “not applicable”). For example:
   `NA — the document makes no probability, forecast, confidence, or uncertainty claims; the task does not require them.`

## Output format

Print a brief reasoning paragraph (under 200 words) summarizing your overall read of the
artifact. Then emit a single JSON code fence with the shape below.
Use the exact dimension keys listed in the rubric’s “Dimensions” table (snake_case,
derived from the canonical label by lowercasing).

```json
{
  "scores": {
    "suitability":          {"score": 0, "reason": "..."},
    "scope":                {"score": 0, "reason": "..."},
    "breadth":              {"score": 0, "reason": "..."},
    "depth":                {"score": 0, "reason": "..."},
    "clarity":              {"score": 0, "reason": "..."},
    "coherence":            {"score": 0, "reason": "..."},
    "concision":            {"score": 0, "reason": "..."},
    "organization":         {"score": 0, "reason": "..."},
    "consistency":          {"score": 0, "reason": "..."},
    "formatting":           {"score": 0, "reason": "..."},
    "verifiability":        {"score": 0, "reason": "..."},
    "factuality":           {"score": 0, "reason": "..."},
    "relevance":            {"score": 0, "reason": "..."},
    "discipline":           {"score": 0, "reason": "..."},
    "soundness":            {"score": 0, "reason": "..."},
    "precision":            {"score": 0, "reason": "..."},
    "parsimony":            {"score": 0, "reason": "..."},
    "calibration":          {"score": 0, "reason": "..."},
    "fairness":             {"score": 0, "reason": "..."},
    "robustness":           {"score": 0, "reason": "..."}
  },
  "violations": [
    {"dimension": "Clarity", "rule_number": 4, "description": "...", "location": "L412-418"}
  ]
}
```

Hard requirements:

- One score entry per dimension defined in the rubric, all 20 keys present, snake_case.
- Each `score` is either an integer 0-5 or the literal string `"NA"`.
- Each `reason` is a short string (under 200 chars).
- `violations` may be empty only if every dimension scored 5, 0, or `NA`.
- `dimension` in each violation matches one of the canonical names exactly (all
  single-word labels: e.g. “Discipline”, “Consistency”).
- Output exactly one JSON code fence; the parser extracts the first ```json block.
