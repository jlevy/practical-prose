---
title: AI-Prose Corrections
description: Reference catalog of LLM-register tells (lexical entries, structural patterns, and density flags) paired with corrections; binding under F2.6 of the practical-prose guidelines.
date: 2026-05-25
status: active
---
# AI-Prose Corrections

Version: v0.3 (last update 2026-07-19)\
Joshua Levy (github.com/jlevy) with agent assistance.
Several structural patterns adapted from Hardik Pandya’s *stop-slop* (MIT,
github.com/hardikpandya/stop-slop), with moderation noted below.

## Purpose

The reference catalog of LLM-register tells paired with the correction practical prose
should reach for instead.
Binding under F2.6 of `pprose guidelines practical-prose-guidelines`.

The catalog has three parts:

- **Lexical catalog:** vocabulary, transitions, and phrases that are regex-encodable; a
  grep pass over a finished draft catches them.
- **Structural patterns:** failures of sentence and paragraph shape (false agency,
  negative listing, fragmentation) that require parsing or judgment to detect, not
  string matching.
- **Attention flags:** constructions that are legitimate in moderation and become a tell
  only at density.

For a compact digest to load into a drafting context, use
`pprose shortcut ai-prose-checklist`; this document is the full reference behind it,
with exceptions, evidence, and corrections per entry.

The common-doc-guidelines §4.2 banned-register list catches *overclaim*; E1, E2, and F2
in the practical-prose guidelines catch *meta-commentary*. This file catches *hollow*,
*mechanical*, and *marketing-register* fingerprints that survive both audits and still
read as machine-generated.

Voice-matching is out of scope: these corrections remove the machine’s fingerprints, not
install a person’s. The catalog is not exhaustive and shifts with model releases.
Most entries have legitimate uses in some genre; the test is whether the word carries
information for the reader, or fills a slot the LLM was trained to fill.

Supporting evidence is in the *Critique of AI-Authored Prose* section of
`pprose guidelines practical-prose-bibliography`.

## Use in Practice

1. **Drafting.** Load the `pprose shortcut ai-prose-checklist` digest (or the drafting
   directives below) into the writing context before any tell appears on the page.
2. **Lint-time check.** A grep pass over the lexical catalog is the cheapest first
   audit.
3. **Edit-time judgment.** A reviewer or model pass over the structural patterns.
   Each hit is a *flag*, not an automatic removal; apply the genre carve-outs.

## Flags vs. Bans

Some sources (including stop-slop) state rules as absolutes: kill all adverbs, no em
dashes, never start a sentence with a Wh- word.
This catalog moderates those into two classes:

- **Cut on sight.** Patterns with no legitimate use in practical prose (engagement bait,
  throat-clearing openers, vague declaratives).
  A hit is a correction, not a question.
- **Attention flags.** Patterns that are legitimate in moderation but mark AI register
  at high density (intensifier adverbs, Wh- openers, three-item lists, em dashes).
  A hit warrants a look; the test is whether the construction carries information or
  fills a slot.

The genre carve-out rule applies throughout: domain conventions override (see the
*Exception* notes below and F2.6).

## Drafting Directives

Rules an agent should apply *while writing*, stated in the imperative so they can be
loaded directly into a drafting context.
Each compresses one or more catalog sections below.

1. **Name the actor.** Every sentence has a subject doing something.
   No inanimate objects performing human actions; no passive constructions that hide who
   acted (*mistakes were made*). When no specific person fits, use *you* to put the
   reader in the seat.
2. **State the point without announcing it.** No throat-clearing openers, no
   meta-commentary on what the document is about to do, no rhetorical setups.
   If a sentence previews the next sentence, delete the preview.
3. **Be specific or be silent.** No vague declaratives (*the implications are
   significant*); name the implication.
   No lazy extremes (*every*, *always*, *never*) doing the work a specific count or
   example should do.
4. **Earn rhetorical force.** No symmetry-for-its-own-sake: binary contrasts, negative
   listings, and dramatic fragments must clarify a real distinction or be cut
   (cross-references E1.5).
5. **Vary rhythm deliberately.** Watch for metronomic sentence lengths, punchy one-liner
   paragraph endings repeated more than once, and three-item lists used by reflex.
6. **Trust the reader.** Skip softening, permission-granting (*and that’s okay*), and
   hand-holding. State facts; let readers draw conclusions.
7. **End when the content ends.** No template conclusions that restate the document, no
   forward-looking closers with no forecast in them (*only time will tell*), and no
   assistant artifacts (*I hope this helps*): a document is not a chat turn.

## Lexical Catalog

Entries in this part are regex-encodable; a grep pass catches them.

### AI-Tell Vocabulary

Words that read as LLM register even when they pass the §4.2 extravagance bar.
Kobak et al. (2025) measures their post-ChatGPT excess frequency across millions of
biomedical abstracts; Juzek and Ward (2024) locate the cause in RLHF feedback rather
than in the training corpus.

- *delve*, *dive into*, *unpack*, *explore* (as connector verb): used to introduce a
  topic rather than to do anything.
  **Correction:** name the actual operation: *analyze*, *measure*, *audit*, *list*,
  *compare*.
- *harness*, *leverage*, *utilize*, *foster*, *facilitate*, *enhance*, *bolster*,
  *elevate*, *streamline* (as verbs): generic action verbs in place of the specific
  verb. **Correction:** *use*, *apply*, *deploy*, *combine*, or *call* almost always
  beats *utilize*; for *enhance* and kin, name what changed and by how much.
  *Leverage* is legitimate in finance and engineering when something specific is being
  amplified; non-load-bearing elsewhere.
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
- *crucial*, *pivotal*, *vital*, *essential*, *key* (as reflexive importance markers):
  assert weight without evidence and dilute with repetition.
  **Correction:** state what depends on the thing; if nothing does, cut the adjective.
- *intricate*, *meticulous*, *nuanced*, *multifaceted*, *invaluable*, *plethora*,
  *myriad*: academic-polish words with measured post-ChatGPT frequency spikes (Kobak et
  al. again). **Correction:** the plain word (*complex*, *careful*, *many*) or the
  specific property.
- *tapestry*, *cornerstone*, *beacon*, *treasure trove* (as stock metaphors): decorative
  nouns that gesture at richness instead of naming it.
  **Correction:** name the parts, the dependency, or the find.

**Exception:** domain terms of art override.
*Robust authentication* with a stated threat model and *state-of-the-art* with a
benchmark and citation carry information; the same words in marketing copy do not.

### Mechanical Transitions

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
- *It is important to note that*, *It’s worth noting that*, *It should be noted that*:
  importance announced instead of shown; among the most-cited LLM filler frames.
  **Correction:** delete the frame and state the point.
  If the note genuinely restricts a claim, name the restriction in its own sentence.
  (Mirrors E1.2’s cut-unnecessary-qualifiers rule.)
- *To put this in perspective*, *What makes this particularly interesting is*, *The
  implications here are*, *This raises the question*: meta-commentary on what the
  document is about to say.
  (Cross-references E1.3 in `pprose guidelines practical-prose-guidelines`.)
  **Correction:** state the perspective, the interest, or the implication directly.
- *That said*, *With that said*, *Having said that*: throat-clearing before a
  qualification. **Correction:** often the prior claim was overconfident and the *That
  said* sentence is the actual claim.
  Lead with the actual claim.

### Throat-Clearing Openers

Announcement phrases before the point.
Cut on sight.

- *Here’s the thing:*, *Here’s what/why/how [X]*
- *The truth is*, *The uncomfortable truth is*, *Let me be clear*
- *It turns out* (when nothing was investigated)
- *I’ll be honest*, *Can we talk about*
- *In today’s fast-paced/digital/modern world*, *In an era where…*, *Now more than
  ever*, *In the ever-evolving landscape of…*, *When it comes to [topic]*: portable
  scene-setting that fits any topic and therefore locates none.
  (The AI-flavored variants, *In the age of AI* and kin, are under AI-Marketing
  Register.)

**Correction:** delete the opener; the sentence that follows is the content.

### Engagement Bait

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
  `pprose guidelines practical-prose-guidelines`.)
- *Here’s the part nobody’s talking about*, *What nobody tells you*, *Most people don’t
  realize*, *The dirty secret*: confident claims of insider knowledge.
  **Correction:** drop the framing and state the claim directly.
  If the claim is genuinely underdiscussed, cite the absence (a search return, a survey
  of the field) rather than asserting it.
- *Whether you’re a seasoned expert or just starting out*, *no matter your skill level*:
  audience-flattering setups that claim universal fit instead of naming the
  prerequisite. **Correction:** name who the document is for and what it assumes
  (cross-references P2 Scope).

### AI-Marketing Register

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

### Inflated Significance

Formulas that assert importance instead of demonstrating it; Wikipedia’s *Signs of AI
writing* catalog treats this register as its most prominent cluster.
The §4.2 banned list catches single-word overclaim; these are the multi-word shapes.

- *stands as a testament to*, *serves as a testament to*, *is a testament to*:
  significance by declaration.
  **Correction:** state what the thing shows and the evidence that it shows it.
- *plays a vital/crucial/pivotal role in [shaping]*, *underscores/highlights the
  importance of*, *cannot be overstated*: importance asserted, never measured.
  **Correction:** name the dependency or consequence; if none can be named, the
  importance was decorative.
- *watershed moment*, *key turning point*, *enduring legacy*, *lasting impact*, *deeply
  rooted*, *rich cultural heritage*: magnitude-of-history claims without history.
  **Correction:** name the date, the change, and who changed course because of it.
- Trailing participial glaze: *…, highlighting the importance of X*, *…, underscoring
  Y*, *…, reflecting Z*, *…, ensuring W*: a clause of unearned significance appended to
  a factual sentence. **Correction:** end the sentence at the fact, or promote the
  participle to a claim with an actor and evidence.

### Copula Avoidance

Verbose substitutes for *is* and *has*; one of the highest-confidence lexical tells in
community catalogs.

- *serves as*, *stands as*, *functions as*, *acts as*, *represents* (where *is* fits).
- *boasts*, *features*, *offers*, *showcases* (where *has* fits).

**Correction:** write *is* and *has*. The plain copula is not weak writing; the
substitute adds syllables, not information.
**Exception:** the literal senses are fine: *serves as* when something fills a role it
was not built for (*the spreadsheet serves as the team’s database*), *features* in a
changelog.

### Vague Attribution

Authority invoked without a source.
(Sourcing depth is governed by G1 Verifiability; this entry is the register tell.)

- *Experts say*, *Industry reports suggest*, *Studies show*, *Observers have noted*,
  *Some critics argue*, *It is widely regarded as*.

**Correction:** name the expert, the report, or the study, with a pointer the reader can
check, or restate the claim as your own judgment and own it.
An authority that can’t be named isn’t evidence.

### Canned Conclusions

Endings produced by template rather than by the content running out.

- *In conclusion*, *In summary*, *To summarize*, *Overall*, *Ultimately* followed by
  restatement: a summary of what the reader just read.
  **Correction:** end on the last point of substance.
  A conclusion earns its place by adding something: a decision, an implication, a next
  action.
- *The future looks bright*, *Only time will tell*, *It remains to be seen*, *Exciting
  times ahead*, *The possibilities are endless*: forward-looking closers with no
  forecast in them. **Correction:** state the open question and who or what resolves it,
  or cut.
- Reflexive *Key Takeaways* / *Final Thoughts* sections that parrot the body.
  **Correction:** delete, or make the recap do work the reader will reuse (a decision
  table, a checklist).
  **Exception:** long reference documents legitimately end with reference material; the
  tell is a recap of a document short enough to skim.

### Chat-Artifact Leakage

Fragments of the assistant conversation left in the document.
Cut on sight, and treat any hit as evidence the surrounding text was pasted unedited,
which warrants a closer audit of the whole passage.

- Assistant framing: *Certainly!*, *Great question*, *I hope this helps*, *Let me know
  if…*, *Would you like me to…*, *Here’s a revised version…*.
- Self-identification and disclaimers: *As an AI language model…*, *As of my last
  knowledge update…*, refusal fragments (*I cannot provide…*).
- Unfilled placeholders: *[insert company name]*, *[Your Name]*,
  *[add specific details]*.
- Stray model markup: citation tokens (*oaicite*, *turn0search…*, *[cite: 1]*), Markdown
  syntax in a non-Markdown medium.

**Correction:** delete the artifact, then re-read the passage it came from against the
rest of this catalog.

### Self-Negating Parallel Structure

*This isn’t X. This is Y.* *Not X. Y.* *Less X, more Y.* *Forget X. This is Y.*

One of the highest-frequency AI tells in 2025–2026, governed by E1.5 in
practical-prose-guidelines.md (`pprose guidelines practical-prose-guidelines`) (*Earn
rhetorical force; cut symmetry-for-its-own-sake*).

**Correction:** if the X-half names a position no one actually holds, drop the X-half
and state Y directly.

The construction is licensed when:

1. X is a position a real reader holds, and the contrast carries meaning.
2. The structure improves recall or clarifies a distinction the reader needs.

## Structural Patterns

Entries in this part require sentence parsing or model judgment to detect; a grep pass
misses them. Each pattern names the failure, gives the template, and states the
correction.

### False Agency

Inanimate things performing human verbs.
AI register favors this because it avoids naming the actor.

- *the complaint becomes a fix*: the complaint did nothing; someone fixed it.
- *the decision emerges*: decisions don’t emerge; someone decides.
- *the data tells us*: data sits there; someone reads it and concludes.
- *the culture shifts*, *the conversation moves toward*, *the market rewards*.

**Correction:** name the human.
*The team fixed it that week* beats *the complaint becomes a fix*. **Exception:**
established technical idiom is fine (*the function returns*, *the server accepts
connections*, *the test fails*); the flag is for *social* actions assigned to
abstractions.

### Negative Listing

Listing what something is *not* before revealing what it *is*: a rhetorical striptease.

- *Not a X. Not a Y. A Z.*
- *It wasn’t X. It wasn’t Y. It was Z.*

**Correction:** state Z. The reader doesn’t need the runway.
This is the N-ary cousin of the binary self-negating parallel in the lexical catalog;
the same licensing test applies (the negated items must be positions a real reader
holds).

### Dramatic Fragmentation

Sentence fragments deployed for manufactured profundity.

- *[Noun]. That’s it. That’s the [thing].*
- *This unlocks something.
  [Single word].*
- Stacked staccato fragments: *X. And Y. And Z.*

**Correction:** complete sentences; trust content over presentation.
**Exception:** an isolated fragment used once for genuine emphasis is a stylistic
choice; the tell is the *template*, especially *that’s it, that’s the X*.

### Rhetorical Setups

Announcing insight rather than delivering it.

- *What if I told you [reframe]?*
- *Here’s what I mean:*
- *Think about it:*
- *And that’s okay.*

**Correction:** make the point; cut the scaffolding.
Questions are licensed when the document actually goes on to investigate them, not when
they decorate a claim the next sentence states anyway.

### Narrator-from-a-Distance

Floating above the scene instead of putting the reader in it.

- *Nobody designed this.*
- *People tend to…*
- *This happens because…* (lecturer voice, repeated)

**Correction:** put the reader in the room.
*You don’t sit down one day and decide to…* beats *Nobody designed this.* **Exception:**
reference documentation legitimately uses neutral third person; the flag is for
narrative and persuasive prose that never lands on a concrete actor or scene.

### Vague Declaratives

Sentences that assert importance without naming the specific thing.

- *The reasons are structural.*
- *The implications are significant.*
- *The stakes are high.*

**Correction:** replace with the specific reason, implication, or stake, or cut.
(Cross-references E1.1 vague-magnitude rules.)

### Telling Instead of Showing

Announcing difficulty or significance rather than demonstrating it.

- *This is genuinely hard.*
- *This is what leadership actually looks like.*
- *…actually matters.*

**Correction:** show the difficulty (the failed attempts, the constraint, the cost) and
let the reader conclude it is hard.

### Scaffolding That Restates

The five-paragraph-essay reflex: an introduction that previews the sections, a summary
at the end of each section, a conclusion that restates the introduction, a heading for
every paragraph.

**Correction:** structure should organize content, not repeat it.
Delete previews and recaps that duplicate adjacent text; merge headings that govern a
single short paragraph.
**Exception:** skim structure in long documents is a virtue (common-doc §2 requires it);
the tell is scaffolding that *restates* rather than *organizes*. A table of contents
earns its place; a paragraph repeating the section above it does not.

## Attention Flags

Legitimate constructions that mark AI register at high density.
Flag, inspect, keep what carries information.

- **Intensifier adverbs** (*really*, *just*, *literally*, *genuinely*, *fundamentally*,
  *deeply*, *truly*, *honestly*, *simply*, *actually*): empty emphasis when stacked;
  occasionally load-bearing.
  Test each occurrence; a density above roughly one per paragraph is a register problem,
  not a word problem.
- **Wh- sentence openers** (*What makes this hard is…*): fine occasionally; a crutch
  when repeated. *The constraint is…* or the named constraint itself is usually tighter.
- **Three-item lists:** the rule-of-three is a reflex in AI register.
  List as many items as the material has; symmetry is not a virtue.
- **Em dashes:** governed by F2.7 (zero spaced em dashes; unspaced for sharp
  parentheticals). Density is the tell, not presence.
- **Punchy paragraph endings:** one is style; every paragraph ending on a one-liner is a
  template.
- **Questions answered immediately:** a question the next sentence answers was
  decoration; either let it breathe or state the answer directly.
- **Hedge stacking:** *may*, *might*, *could*, *potentially*, *perhaps* are each
  legitimate; several per paragraph is calibration-free mush.
  One hedge per claim, sized to the actual uncertainty (J1.6 governs calibration).
- **Structure density:** bullets, bold, emoji, and headings are formatting tools, and
  each is an AI tell at reflex density: connected reasoning fragmented into bullets,
  bold scattered mid-paragraph, emoji decorating headings, a heading per paragraph.
  Formatting conventions are governed by common-doc §5 and F3.4; the flag here is
  density without function.
- **Elegant variation:** rotating synonyms for one referent (*the tool*, *the utility*,
  *the solution* in one passage) to avoid repetition.
  Practical prose repeats the term (F2.2); varied names read as varied things.

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
| Bold, list, heading, and emphasis conventions | common-doc §5; F3.4 |
| Both-sides balance that never lands on a position | J1.6, J2 |
| Redundant restatement across a document | E3 |
| Fabricated or broken citations, dead links, wrong DOIs | G1, G2 |

## Sources and Credit

- **Pandya, stop-slop** (MIT): the false-agency, negative-listing,
  dramatic-fragmentation, rhetorical-setup, and narrator-from-a-distance categories
  originate there, adapted here with genre carve-outs and with absolutist rules (kill
  all adverbs, no em dashes, no Wh- openers) moderated into attention flags.
- **Wikipedia, *Signs of AI writing*** (CC-BY-SA-4.0): community-curated catalog; the
  inflated-significance, copula-avoidance, vague-attribution, canned-conclusion, and
  chat-artifact categories draw on it.
- The empirical case for structural over lexical rules: Rallapalli et al.
  (2026) and Xia, Stańczak, and Roth (EACL 2026) in
  `pprose guidelines practical-prose-bibliography`.

## Related Docs

- `pprose shortcut ai-prose-checklist`: the compact digest of this catalog for loading
  into a drafting context.
- `pprose guidelines common-doc-guidelines`: §4.2 holds the extravagant-register list.
  The lists here are additive.
- `pprose guidelines practical-prose-guidelines`: E1.4 (earned register), E1.5 (cut
  symmetry-for-its-own-sake), F2.6 (domain conventions are binding), F2.7 (em-dash
  conventions).
- `pprose guidelines practical-prose-bibliography`: the *Critique of AI-Authored Prose*
  section lists sources on AI register, vocabulary fingerprints, the editorial response
  to LLM output, and open-source tools.

<!-- This document follows common-doc-guidelines.md.
See github.com/jlevy/practical-prose and review guidelines before editing.
-->
