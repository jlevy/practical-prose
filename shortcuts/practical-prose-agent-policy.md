---
title: Practical Prose Agent Policy
description: One-page generation-time priority list for agents drafting practical prose; the operational companion to the pre-publish quick-checklist.
category: documentation
author: Joshua Levy (github.com/jlevy) with agent assistance
---
# Practical Prose Agent Policy

A one-page priority list for agents drafting practical documents.
Where the [quick-checklist](practical-prose-quick-checklist.md) is for pre-publish
self-audit, this doc is for generation-time guidance: load it instead of the full
guidelines (~800 lines) when generating, summarizing, or rewriting prose for a reader
who will act on it.

The order matters. When two priorities conflict, the earlier one wins.

## Priority order

1. **Answer the reader’s task.** State the question, decision, plan, or audience need
   the document serves; make the main output recoverable from a skim of intro plus
   headings; name the reader burden the document removes.
   (§1 Suitability, §1.6 reader-burden.)

2. **State scope and main output early.** Name what the document covers, and name what
   its evidence in scope is not competent to conclude.
   (§2 Scope, §2.5 claim-boundary.)

3. **Make material claims traceable.** Every quantitative or load-bearing factual claim
   points to a source the reader can check.
   Confidence tags (`[VERIFIED]`, `[ESTIMATED]`, `[UNVERIFIED]`, `[ASSUMING: ...]`) pair
   with specific source pointers.
   For central claims, also name what would invalidate them.
   (§11 Verifiability, §12 Factuality.)

4. **Keep evidence, inference, and recommendation distinct.** Observation, judgment,
   interpretation, and implication on separate rungs.
   Mechanism named where causation is asserted; counterfactual named where the
   explanation could be wrong.
   (§13 Inference Discipline, §14 Soundness.)

5. **Use concrete language and specific terms.** Most specific word the audience can
   parse. No vague magnitudes; no umbrella nouns where sub-distinctions matter;
   quantitative precision matches measurement precision.
   Rhetorical force is licensed only when it carries information, clarifies a
   distinction, or preserves a hard-won idea.
   (§5 Clarity, §15 Precision.)

6. **Be concise; don’t add visible rigor unless it improves inspectability.** More tags,
   more citations, more caveats, more structure, more words does not make a document
   better; it makes it more compliant.
   Cut anything that advances no purpose.
   (§7 Concision; rubric §Notes “metrics are evidence, not quality”.)

7. **Apply fairness and robustness only when the task involves disputed or interpretive
   claims.** Skipping these on a reference doc or status note is not a failure; forcing
   them onto a doc that doesn’t need them is performative rigor.
   Default to the Standard profile; mark dimensions NA when they genuinely don’t apply.
   (§17 Fairness, §18 Robustness; metrics §Applicability Profiles.)

8. **Mark unknowns rather than inventing support.** `[UNVERIFIED]`, `[ASSUMING: ...]`,
   or an explicit “I don’t know” line is preferable to a fluent fabrication.
   Confidence without cowardice runs in both directions: don’t hedge on strong evidence,
   but don’t fabricate on weak evidence either.
   (§16.6 confidence without cowardice; the Humane principle: trust before polish.)

## When the rules conflict with reader outcome

When following a rule would hurt the reader’s ability to understand, decide, do, verify,
or maintain the work, document the deviation (the rule set aside, the reader outcome
served, the risk introduced) and proceed.
See the **Justified Deviations** section in
[practical-prose-rubric.md](../docs/practical-prose-rubric.md).

Local rule compliance is in service of reader outcome, not the other way around.

## Related artifacts

- [practical-prose-quick-checklist.md](practical-prose-quick-checklist.md): pre-publish
  self-audit for the 18 dimensions.
- [practical-prose-guidelines.md](../docs/practical-prose-guidelines.md):
  prescriptive rules, full version (~800 lines).
- [practical-prose-rubric.md](../docs/practical-prose-rubric.md): scoring anchors,
  Justified Deviations, applicability profiles, audit passes, and the Failure-Mode
  Questions table.
- [practical-prose-metrics.md](../docs/practical-prose-metrics.md): operational
  metrics \+ applicability profiles by `risk_level`.

<!-- This document follows common-doc-guidelines.md.
Review guidelines before editing.
-->
