# AI-Prose Corrections

Version: v0.1 (last update 2026-05-25)\
Joshua Levy (github.com/jlevy) with agent assistance

## Purpose

A catalog of LLM-register tells paired with the correction practical prose should reach
for instead. Binding under F2.6 of
[practical-prose-guidelines.md](practical-prose-guidelines.md).

The common-doc-guidelines §4.2 banned-register list catches *overclaim*; E1, E2, and F2
in the practical-prose guidelines catch *meta-commentary*. This file catches *hollow*,
*mechanical*, and *marketing-register* fingerprints that survive both audits and still
read as machine-generated.

Voice-matching is out of scope: these corrections remove the machine’s fingerprints, not
install a person’s. The catalog is not exhaustive and shifts with model releases.
Most entries have legitimate uses in some genre; the test is whether the word carries
information for the reader, or fills a slot the LLM was trained to fill.

Supporting evidence is in the *Critique of AI-Authored Prose* section of
[practical-prose-bibliography.md](practical-prose-bibliography.md).

## Use in Practice

1. **Lint-time check.** A grep pass is the cheapest first audit.
   Most entries below can be encoded as a regex.
2. **Edit-time judgment.** Each hit is a *flag*, not an automatic removal.
   Apply the genre carve-outs.

## AI-Tell Vocabulary

Words that read as LLM register even when they pass the §4.2 extravagance bar.
Kobak et al. (2025) measures their post-ChatGPT excess frequency across millions of
biomedical abstracts; Juzek and Ward (2024) locate the cause in RLHF feedback rather
than in the training corpus.

- *delve*, *dive into*, *unpack*, *explore* (as connector verb): used to introduce a
  topic rather than to do anything.
  **Correction:** name the actual operation: *analyze*, *measure*, *audit*, *list*,
  *compare*.
- *harness*, *leverage*, *utilize*: generic action verbs in place of the specific verb.
  **Correction:** *use*, *apply*, *deploy*, *combine*, or *call* almost always beats
  *utilize*. *Leverage* is legitimate in finance and engineering when something specific
  is being amplified; non-load-bearing elsewhere.
- *robust*: legitimate in engineering when paired with the named failure mode it
  survives (*robust to packet loss*, *robust to adversarial inputs*). **Correction:**
  when generic, name the failure mode the system survives, or cut.
- *landscape*, *realm*, *space* (as metaphor for *field*): the domain name is almost
  always clearer. **Correction:** *the AI landscape* → *current AI systems*; *the
  regulatory realm* → *current regulations*.
- *straightforward*: almost always padding.
  **Correction:** describe the thing; let the reader judge whether it is easy.
- *seamless*, *streamlined*, *intuitive*: marketing-register adjectives presented as
  factual descriptions.
  **Correction:** give the measurement (number of clicks, setup time, error rate) when
  the property is genuine.
- *holistic*, *comprehensive*, *thorough*: claims of completeness without enumeration.
  **Correction:** list the things covered, or cut.
- *game-changer*, *cutting-edge*, *state-of-the-art*: marketing-register magnitude
  claims. **Correction:** *state-of-the-art* with a benchmark, dataset, and citation is
  load-bearing in ML papers; without those, filler.

**Exception:** domain terms of art override.
*Robust authentication* with a stated threat model and *state-of-the-art* with a
benchmark and citation carry information; the same words in marketing copy do not.

## Mechanical Transitions

These connectors fail when they are the only signal of a connection that doesn’t exist,
or when the sentence they introduce restates rather than advances.

- *Furthermore*, *Additionally*, *Moreover*, *In addition*: paragraph-opening adders
  that don’t name the relationship.
  **Correction:** if a logical relationship exists, name it (*because*, *in contrast*,
  *as a corollary*, *which means*). If no relationship exists beyond *and also*, drop
  the connector and start the sentence.
- *Moving forward*, *Going forward*, *At the end of the day*: temporal fillers without
  temporal content. **Correction:** cut, or replace with a date, condition, or named
  milestone.
- *In other words*: usually signals that the prior sentence was unclear.
  **Correction:** rewrite the prior sentence; do not append a paraphrase.
- *It goes without saying*, *Needless to say*: assert something obvious then say it.
  **Correction:** cut.
- *To put this in perspective*, *What makes this particularly interesting is*, *The
  implications here are*, *This raises the question*: meta-commentary on what the
  document is about to say.
  (Cross-references E1.3 in
  [practical-prose-guidelines.md](practical-prose-guidelines.md).) **Correction:** state
  the perspective, the interest, or the implication directly.
- *That said*, *With that said*, *Having said that*: throat-clearing before a
  qualification. **Correction:** often the prior claim was overconfident and the *That
  said* sentence is the actual claim.
  Lead with the actual claim.

## Engagement Bait

Hook rhetoric that commands rather than informs.
Always cut.

- *Let that sink in*, *Read that again*, *Full stop*, *Pause* (as imperative): direct
  address that flatters the reader for paying attention.
  **Correction:** the sentence either is striking or it is not; bidding for attention is
  friction.
- *This changes everything*, *You’re not ready for this*, *Are you paying attention?*,
  *Buckle up*: magnitude assertions without evidence.
  **Correction:** cite the magnitude.
  (Cross-references common-doc §4.2 banned register and J1.6 in
  [practical-prose-guidelines.md](practical-prose-guidelines.md).)
- *Here’s the part nobody’s talking about*, *What nobody tells you*, *Most people don’t
  realize*, *The dirty secret*: confident claims of insider knowledge.
  **Correction:** drop the framing and state the claim directly.
  If the claim is genuinely underdiscussed, cite the absence (a search return, a survey
  of the field) rather than asserting it.

## AI-Marketing Register

Words that import commercial product-copy register into prose that purports to be
descriptive or analytical.

- *Supercharge*, *Unlock*, *Future-proof*, *Empower*: verbs that promise reader
  transformation without specifying the mechanism.
  **Correction:** replace with the specific outcome (*reduces deploy time from 12
  minutes to 3*) or cut.
- *10x*, *next-level*, *next-gen*, *AI-powered* (as bare adjective): magnitude or
  category claims without numbers or definitions.
  **Correction:** quantify or cut.
- *In the age of AI*, *The AI revolution*, *As AI continues to evolve*: period-marker
  phrases that anchor claims to a vague civilizational shift.
  **Correction:** name the specific shift (a model release, a regulation, a benchmark
  threshold) or drop the framing.
- *Solutions*, *offerings* (as nouns): bare product-copy nouns.
  **Correction:** use the specific term (*library*, *service*, *workflow*, *contract*,
  *recommendation*).

## Self-Negating Parallel Structure

*This isn’t X. This is Y.* *Not X. Y.* *Less X, more Y.* *Forget X. This is Y.*

One of the highest-frequency AI tells in 2025–2026, governed by
[E1.5 in practical-prose-guidelines.md](practical-prose-guidelines.md#e1-clarity) (*Earn
rhetorical force; cut symmetry-for-its-own-sake*).

**Correction:** if the X-half names a position no one actually holds, drop the X-half
and state Y directly.

The construction is licensed when:

1. X is a position a real reader holds, and the contrast carries meaning.
2. The structure improves recall or clarifies a distinction the reader needs.

## Coverage by Existing Rules

AI failure modes governed by rules outside this file:

| Failure | Covered by |
| --- | --- |
| Extravagant overstatement (*incontrovertibly*, *transformational*, *seismic*) | common-doc §4.2; E1.4 |
| Vague magnitude words (*rapid*, *many*, *significant*) | E1.1, G1.1, R3.5 |
| Meta-commentary (*This section will discuss*, *As we will see*) | E1.3 |
| Self-referential canonicality claims (*this is the canonical X*) | E1.6 |
| Em-dash overuse, especially spaced em dashes | F2.7 |
| Backwards-history pollution (*previously named X*, *removed Y*) | E3.5 |
| Uncalibrated hedging (*possibly*, *might*) on strong evidence | J1.6 |
| Padding bibliographies for performative rigor | G3.5 |

## Related Docs

- [common-doc-guidelines.md](common-doc-guidelines.md): §4.2 holds the
  extravagant-register list.
  The lists here are additive.
- [practical-prose-guidelines.md](practical-prose-guidelines.md): E1.4 (earned
  register), E1.5 (cut symmetry-for-its-own-sake), F2.6 (domain conventions are
  binding).
- [practical-prose-bibliography.md](practical-prose-bibliography.md): the *Critique of
  AI-Authored Prose* section lists sources on AI register, vocabulary fingerprints, the
  editorial response to LLM output, and open-source tools.

<!-- This document follows common-doc-guidelines.md.
Review guidelines before editing.
-->
