# Design Rationale — The Daily Reflection Tree

> Two-page write-up. Source files: [`tree/reflection-tree.json`](./tree/reflection-tree.json), [`tree/tree-diagram.md`](./tree/tree-diagram.md), [`agent/agent.py`](./agent/agent.py).

## 1. Why these specific questions

The brief gives three psychological axes (Locus, Orientation, Radius). My design rule was: **every question must be a question I'd actually want a tired colleague to answer at 7pm — not a Likert item dressed up as prose.** That ruled out three tempting failure modes:

- **Surveys disguised as conversation.** "Rate your sense of agency from 1–5" is technically a question. It is not a thought.
- **Leading questions.** "Did you take ownership today?" only has one socially acceptable answer. The tree learns nothing, and the employee learns less.
- **Diagnostic-sounding questions.** "Do you tend to externalise blame?" turns reflection into self-accusation. People don't reflect under accusation; they defend.

Each question therefore tries to do three things at once: surface the axis, give honest options on both poles (so the "wrong" answer is also pickable without shame), and leave a small gap the person has to fill themselves. The clearest example is **A2_Q_GIVE**: _"If no one would ever have known you did it — no credit, no thanks, no record — would you still have done it?"_ It surfaces entitlement vs contribution without ever using either word. "Probably, but I'd be quietly disappointed" is a real human option, not a trick — it lets an entitled answer come out of hiding.

I also kept questions **concrete** wherever possible. "Name one person you could thank, by name, tomorrow morning, and the specific thing you'd thank them for" beats "How connected do you feel to your team?" by a wide margin, because it forces a search, and the search itself is the reflection.

## 2. How the branching was designed (and the trade-offs)

The tree has **three axes in sequence**, each with the same internal shape:

```
OPEN question -> D1 (route by answer) -> follow-up question (path-specific)
              -> common deepening question -> D2 (route by signal tally) -> reflection (3 variants)
              -> bridge to next axis
```

This shape was a deliberate trade-off:

- **Two splits per axis (D1 + D2) rather than one.** A single branch on the opening question is too coarse — it pigeonholes someone who answered "Mixed" into either the agency-high or agency-low branch and never reconsiders. Two splits give the tree a chance to _change its mind_ about the employee based on accumulated evidence (the signal tally), which is the whole point of having signals at all.
- **Three reflection variants per axis (`INT` / `EXT` / `MIXED`), not two.** The `MIXED` outcome (a tie in the tally) is where the most honest reflection lives, and where most real days actually sit. Collapsing it into either pole would make the tool feel binary in a way real days aren't.
- **Path-specific follow-ups, common deepeners.** `A1_Q2_INT` and `A1_Q2_EXT` ask different things (because someone arriving from "Productive" needs a different prompt than someone arriving from "Frustrating"), but the deepening question on Axis 2 (`A2_Q2`) is shared across both `A2_Q_GIVE` and `A2_Q_EXPECT`. This keeps the tree from blowing up into a per-path snowflake.

**Trade-offs I made consciously:**

- **No mid-axis early exits.** I considered letting strong signals on Axis 1 skip Axis 2 entirely. I rejected this — the brief explicitly says the axes build on each other, and a person high on agency still needs to be asked about contribution. Skipping would feel rewarding ("you're doing great, you can leave"), and reward is the wrong tone.
- **Signal weights are uniform (+1).** I considered weighting the deepening question (`A1_Q2_*`) higher than the opening, because it's a stronger signal. I left it at +1 to keep the data file readable without a points system. The cost is some near-ties that route to `MIXED` reflections; I think that's actually a feature.
- **Three-pole signals on Axis 3 (`self` / `others` / `transcend`)** instead of two. Maslow's self-transcendence is genuinely a third position, not a louder version of "others-focused", and collapsing it would have lost the most distinctive reflection (`A3_R_TRANS`).

## 3. Psychological sources that shaped the design

- **Rotter (1954), _Generalized Expectancies for Internal vs. External Control of Reinforcement_** — for Axis 1. Rotter's locus is _generalised_; my tree only samples a single day. The questions are written so the employee _locates today_, not themselves. This is why the reflections never say "you have an external locus" — they say "today pulled your attention outward."
- **Dweck (2006), _Mindset_** — also Axis 1, especially the framing that agency is a learnable habit of attention rather than a personality trait. This is why `A1_R_EXT` ends with _"Tomorrow has more of those moments than today did — they're just hard to see when you're tired."_
- **Campbell et al. (2004), _Psychological Entitlement Scale_** — Axis 2. The scale's central insight is that entitlement is **stable and invisible to its holder**; you cannot ask "Are you entitled?" and get a useful answer. The tree therefore asks proxy questions about _recognition wanted vs. work named_, which is the diagnostic the scale itself uses.
- **Organ (1988), _Organizational Citizenship Behavior_** — also Axis 2. OCB is exactly "discretionary effort", which is what `A2_Q_GIVE` is testing.
- **Maslow (1969), _Theory Z_ / self-transcendence paper** — Axis 3. Maslow's late position was that the healthiest humans orient outward, _and that this reduces suffering_. The reflection `A3_R_TRANS` lifts directly from this, deliberately without naming Maslow.
- **Batson (2011), _Altruism in Humans_** — Axis 3. Batson's distinction between sympathy (feeling-for) and perspective-taking (cognitive understanding-of) is what `A3_Q_OTHERS` asks: _"held someone else's situation in mind — not to fix it, just to understand it."_

The reflections deliberately **do not cite their sources to the user**. Citations are for me; the employee gets a wise colleague, not a footnote.

## 4. What I'd improve with more time

1. **Adaptive question depth.** A user who clearly leans one way after two questions on an axis could be routed to a _destabilising_ third question on the opposite pole rather than a confirming one. ("You've described a day where you mostly gave — was there a moment you wanted credit and didn't get it?") The tree would learn more, and the employee would too.
2. **Per-axis longitudinal state.** Right now the agent is stateless across sessions. The same tree with persisted history could let `A1_OPEN` open with _"Yesterday you called it 'Productive'. Today?"_ — the same reflection mechanism over a week becomes a small, real diary.
3. **A "challenge" branch on the entitlement reflection.** `A2_R_ENTITLE` is the kindest of the entitled reflections; a more advanced version would route into a short "what would you have _given_ to earn it?" sub-tree before bridging. I left it kinder for v1 because the brief explicitly warns against moralising.
4. **Better reflection authoring tooling.** The hardest part of this assignment was not the structure — it was writing reflection text that sounds like a colleague rather than a coach. A real product would need a reflection-text linter (banned words: _journey_, _unlock_, _empower_; banned forms: rhetorical questions; required: one specific noun the employee actually said).
5. **A second-pass pass through the tree as the employee.** Forty-eight hours is enough to ship the tree; it is barely enough to actually _use_ the tree. The questions I'd most want to rewrite are the ones I haven't yet answered honestly myself.
