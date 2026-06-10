# AI-Prose Mitigations

Version: v0.1 draft (last update 2026-06-09)\
Joshua Levy (github.com/jlevy) with agent assistance.
Several patterns adapted from Hardik Pandya’s *stop-slop* (MIT,
github.com/hardikpandya/stop-slop), with moderation noted below.

## Purpose

Drafting-time guidance for reducing AI-slop tendencies in prose, paired with the
structural patterns that mark unedited LLM output but cannot be caught by a grep pass.

This file complements [ai-prose-corrections.md](ai-prose-corrections.md) and the
division of labor is deliberate:

- **ai-prose-corrections.md** is the *edit-time catalog*: vocabulary, transitions, and
  phrases that are regex-encodable, applied as a lint pass over a finished draft.
- **This file** holds two things corrections cannot: (1) *drafting directives* — rules
  an agent applies while writing, before any tell appears on the page; and (2)
  *structural patterns* — failures of sentence and paragraph shape (false agency,
  negative listing, fragmentation) that require parsing or judgment to detect, not
  string matching.

Both files are binding under F2.6 of
[practical-prose-guidelines.md](practical-prose-guidelines.md).
Neither is a voice-matching document; both remove the machine’s fingerprints without
installing a person’s.

## Flags vs. Bans

Some sources (including stop-slop) state rules as absolutes: kill all adverbs, no em
dashes, never start a sentence with a Wh- word.
This file moderates those into two classes:

- **Cut on sight.** Patterns with no legitimate use in practical prose (engagement bait,
  throat-clearing openers, vague declaratives).
  A hit is a correction, not a question.
- **Attention flags.** Patterns that are legitimate in moderation but mark AI register
  at high density (intensifier adverbs, Wh- openers, three-item lists, em dashes).
  A hit warrants a look; the test is whether the construction carries information or
  fills a slot.

The genre carve-out rule applies throughout: domain conventions override (see the
*Exception* notes in ai-prose-corrections.md and F2.6).

## Drafting Directives

Rules an agent should apply *while writing*, stated in the imperative so they can be
loaded directly into a drafting context:

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

## Structural Patterns

Each pattern below names the failure, gives the template, and states the correction.
These are the patterns a grep pass misses; detection requires sentence parsing or model
judgment (see the planned two-phase checker in the project specs).

### False Agency

Inanimate things performing human verbs.
AI register favors this because it avoids naming the actor.

- *the complaint becomes a fix* — the complaint did nothing; someone fixed it.
- *the decision emerges* — decisions don’t emerge; someone decides.
- *the data tells us* — data sits there; someone reads it and concludes.
- *the culture shifts*, *the conversation moves toward*, *the market rewards*.

**Correction:** name the human.
*The team fixed it that week* beats *the complaint becomes a fix*. **Exception:**
established technical idiom is fine (*the function returns*, *the server accepts
connections*, *the test fails*); the flag is for *social* actions assigned to
abstractions.

### Negative Listing

Listing what something is *not* before revealing what it *is* — a rhetorical striptease.

- *Not a X. Not a Y. A Z.*
- *It wasn’t X. It wasn’t Y. It was Z.*

**Correction:** state Z. The reader doesn’t need the runway.
This is the N-ary cousin of the binary self-negating parallel already governed by
ai-prose-corrections.md; the same licensing test applies (the negated items must be
positions a real reader holds).

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

### Throat-Clearing Openers

Announcement phrases before the point.
Cut on sight; superset of the engagement-bait list in ai-prose-corrections.md.

- *Here’s the thing:*, *Here’s what/why/how [X]*
- *The truth is*, *The uncomfortable truth is*, *Let me be clear*
- *It turns out* (when nothing was investigated)
- *I’ll be honest*, *Can we talk about*

**Correction:** delete the opener; the sentence that follows is the content.

### Vague Declaratives

Sentences that assert importance without naming the specific thing.

- *The reasons are structural.*
- *The implications are significant.*
- *The stakes are high.*

**Correction:** replace with the specific reason, implication, or stake — or cut.
(Cross-references E1.1 vague-magnitude rules.)

### Telling Instead of Showing

Announcing difficulty or significance rather than demonstrating it.

- *This is genuinely hard.*
- *This is what leadership actually looks like.*
- *…actually matters.*

**Correction:** show the difficulty (the failed attempts, the constraint, the cost) and
let the reader conclude it is hard.

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

## Coverage Map

| Failure | Where governed |
| --- | --- |
| Vocabulary tells (*delve*, *robust*, *landscape*) | ai-prose-corrections.md |
| Mechanical transitions (*Furthermore*, *That said*) | ai-prose-corrections.md |
| Engagement bait (*Let that sink in*) | ai-prose-corrections.md |
| Self-negating parallel (*Not X. Y.*) | ai-prose-corrections.md; E1.5 |
| Structural patterns (false agency, negative listing, fragments) | **this file** |
| Drafting directives (name the actor, vary rhythm) | **this file** |
| Attention flags (adverb density, rule-of-three) | **this file** |
| Extravagant overstatement | common-doc §4.2; E1.4 |
| Em-dash conventions | F2.7 |

## Sources and Credit

- **Pandya, stop-slop** (MIT): the false-agency, negative-listing,
  dramatic-fragmentation, rhetorical-setup, and narrator-from-a-distance categories
  originate there, adapted here with genre carve-outs and with absolutist rules (kill
  all adverbs, no em dashes, no Wh- openers) moderated into attention flags.
- **Wikipedia, *Signs of AI writing*** (CC-BY-SA-4.0): corroborating community-curated
  catalog; see the research doc for tells pending adoption.
- The empirical case for structural over lexical rules: Rallapalli et al.
  (2026) and Xia, Stańczak & Roth (EACL 2026) in
  [practical-prose-bibliography.md](practical-prose-bibliography.md).

## Related Docs

- [ai-prose-corrections.md](ai-prose-corrections.md): the edit-time catalog this file
  extends.
- [practical-prose-guidelines.md](practical-prose-guidelines.md): E1.5 (earned
  rhetorical force), F2.6 (domain conventions binding), F2.7 (em-dash conventions).
- [practical-prose-bibliography.md](practical-prose-bibliography.md): *Critique of
  AI-Authored Prose* section.

<!-- This document follows common-doc-guidelines.md.
Review guidelines before editing.
-->
