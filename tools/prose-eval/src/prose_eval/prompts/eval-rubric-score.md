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
3. **The deterministic metrics context** from the eval report, when available:
   precomputed counts and derived ratios such as word count, headings, links,
   footnotes, tables, banned-register hits, replacement-history hits, pedantic-marker
   hits, generic-heading hits, and density concerns.
4. **The artifact under review**: a Markdown document.

## What to do

1. Read the artifact end to end.
2. Use the deterministic metrics context as evidence, not as an automatic score. Never
   contradict it. If a metric is a candidate flag rather than a true defect, say so in
   the reason (for example, banned-register hits that appear only inside an explicit
   banned-words list).
   Do not cite a violation solely because a count is nonzero; cite a violation only
   after inspecting the metric examples and the artifact text.
   For style metrics, distinguish authorial prose from preserved source text: official
   titles, direct quotations, URLs, code, and explicit negative examples may retain
   punctuation or wording that the house style would not use in ordinary prose.
   Do not cite a Style Consistency or Clarity violation for punctuation that appears
   only inside official titles, citation titles, footnotes preserving source titles,
   direct quotations, URLs, code, or explicit negative examples.
3. Score every dimension defined in the rubric on the 0-5 scale, following the rubric
   anchors. Score 0 means “applicable but unassessable”; use only when content is missing
   for that dimension. `NA` means the dimension does not apply to this artifact at all
   (for example, Calibration on a document that makes no probability claims).
4. For every dimension scored 1-4, identify at least one specific guideline-rule
   violation. Cite:
   - the dimension by its canonical name (the exact label used in the rubric:
     Suitability, Scope, Breadth, Depth, Clarity, Coherence, Concision, Organization,
     Style Consistency, Formatting, Verifiability, Factuality, Inference Discipline,
     Soundness, Precision, Calibration, Fairness, Robustness),
   - the `rule_number` (the integer in `practical-prose-guidelines.md` for that
     dimension’s rule),
   - a one-line description,
   - a location pointer (line range like `L412-418`, section heading like `§2.8`, or
     quoted phrase).
5. For every dimension scored 5, 0, or `NA`, do not cite any violation for that
   dimension. Score 5 means every rule followed; 0 means applicable but unassessable;
   `NA` means the dimension does not apply.
6. Cross-check: every score 1-4 must have at least one matching violation; every score
   5, 0, or `NA` must have zero matching violations.
7. When using `NA`, the reason must explain why the dimension does not apply (not just
   “not applicable”). For example:
   `NA — the document makes no probability, forecast, confidence, or uncertainty claims; the task does not require them.`
8. Be conservative with Grounding `NA`. Prescriptive, reference, and rubric documents
   can still make verifiable claims. Attributions to people, works, institutions, or
   prior documents, historical claims, quantitative counts, and factual claims about
   external sources engage Verifiability and Factuality; score those dimensions 1-5
   instead of `NA`.
   For repository documentation, internal file paths, section references, version
   strings, fixture claims, package names, command names, dates, standard names, and
   claims about what another local document contains are also verifiable claims. If any
   such claim appears, Verifiability and Factuality are not `NA`.
9. Be conservative with Inference Discipline `NA`. A document that gives a decision
   tree, explains why a rule exists, describes failure modes, draws distinctions, or
   links a condition to an implication is reasoning. Score Inference Discipline 1-5 for
   that content. Reserve `NA` only for artifacts that are pure rosters, literal logs, or
   uninterpreted reference tables with no stated rationale.
   Guideline and rubric documents that define rules, anchors, decision trees, examples,
   or failure modes almost always engage Inference Discipline. Annotated bibliographies
   that map traditions to principles, explain source relevance, or distinguish scope
   limits also engage reasoning; they are not pure rosters.
   Apply the same standard to Soundness: if the artifact explains why items matter,
   maps concepts, gives selection rationale, or makes evaluative characterizations,
   Soundness is 1-5, not `NA`.
10. Do not overclaim external verification. Unless source excerpts, link-checker output,
    tool results, or other corroborating evidence are included in the artifact or metrics
    context, do not say you "spot-checked" sources, followed links, verified URLs,
    confirmed facts externally, or found that sources resolve. You may say citations are
    specific enough to check, no contradiction is apparent from the provided context, or
    external corroboration was not performed in this pass. Treat unavailable external
    checking as a reviewer limit when the document provides reasonable source pointers.

## Output format

Print a brief reasoning paragraph (under 200 words) summarizing your overall read of the
artifact. Then emit a single JSON code fence with the shape below.
Use the exact dimension keys listed in the rubric’s “Dimensions” table (snake_case,
derived from the canonical label by lowercasing and replacing spaces with underscores:
`Inference Discipline` → `inference_discipline`, `Style Consistency` →
`style_consistency`).

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
    "style_consistency":    {"score": 0, "reason": "..."},
    "formatting":           {"score": 0, "reason": "..."},
    "verifiability":        {"score": 0, "reason": "..."},
    "factuality":           {"score": 0, "reason": "..."},
    "inference_discipline": {"score": 0, "reason": "..."},
    "soundness":            {"score": 0, "reason": "..."},
    "precision":            {"score": 0, "reason": "..."},
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

- One score entry per dimension defined in the rubric, all 18 keys present, snake_case.
- Each `score` is either an integer 0-5 or the literal string `"NA"`.
- Each `reason` is a short string (under 200 chars).
- `violations` may be empty only if every dimension scored 5, 0, or `NA`.
- `dimension` in each violation matches one of the canonical names exactly.
  Two-word names use a single space (e.g. “Inference Discipline”, “Style Consistency”).
- Output exactly one JSON code fence; the parser extracts the first ```json block.
