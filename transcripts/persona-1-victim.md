# Persona 1 — Sample Transcript: "victim / entitled / self-centric"

> Reproduce with: `python3 agent/agent.py --replay 3,3,4,4,4,3,1,4,4 < /dev/null`
>
> Captured verbatim from `agent/agent.py`. Decision/bridge/start/end nodes
> are auto-advancing — they appear in the transcript as horizontal rules
> (`---`). Picks (`> N`) are 1-indexed.

---

```text
------------------------------------------------------------
Good evening. Take a breath. We're going to look at today together — not to grade it, just to notice it. Eight or nine questions. No right answers.
------------------------------------------------------------

If you had to describe today in a single word, which fits best?
  1) Productive
  2) Mixed
  3) Tough
  4) Frustrating
> 3

You called today "Tough". When things got hard, what was your first move?
  1) I paused and asked: what's actually in my control here?
  2) I named the problem out loud and asked for help
  3) I waited to see if someone else would step in
  4) I pushed through, head down, hoping it would pass
> 3

Even on a hard day, there's usually one moment you steered. Where was yours today?
  1) How I responded to a message I wanted to ignore
  2) When I asked a question instead of assuming
  3) When I chose to keep going instead of stopping
  4) I don't think I steered anything today
> 4

A hard day pulls our attention outward — to what others did, what the system didn't do, what we couldn't shape. That's fair, and it's honest. And still: somewhere in all of it, you made a call. You said it was "I don't think I steered anything today". That's a small lever. Tomorrow has more of those moments than today did — they're just hard to see when you're tired.

[press Enter to continue]

------------------------------------------------------------
We've looked at how you handled today. Now let's turn to something different — not what you did, but what you gave.
------------------------------------------------------------

Pick one interaction from today that comes to mind right now. In that moment, were you mostly giving or mostly expecting?
  1) I helped someone with something that wasn't mine to do
  2) I taught or explained something, even informally
  3) I was hoping for support that didn't come
  4) I felt my work wasn't seen the way it deserved
> 4

Picture the recognition or support you wanted today. What specifically did you contribute that earned it?
  1) A clear, real piece of work I can name
  2) I held the team together in a way that's hard to point to
  3) Effort and time, even if the output was small
  4) I'm not sure — it was more about how hard the day felt
> 4

Think of someone you didn't help today, but could have. What stopped you?
  1) I noticed, and I made a deliberate choice not to
  2) I did help — I'm drawing a blank on someone I missed
  3) I was too deep in my own work to notice
  4) I didn't notice anyone needed it
> 3

There's a quiet voice in most of us that keeps a tally — what we gave, what we got, what we deserved. It's human. But when the tally runs the day, the day runs us. What if tomorrow, just for one stretch of it, you didn't keep score?

[press Enter to continue]

------------------------------------------------------------
We've looked at how you showed up, and what you gave. One last shift — to the size of the world you were holding while you did it.
------------------------------------------------------------

When you think about today's biggest challenge, who actually comes to mind first?
  1) Just me — it was my problem to solve
  2) My team — we were all in it
  3) A specific colleague who had it harder than me
  4) The customer or person we're ultimately serving
> 1

Zoom out for a second. If you replayed today and listed three people affected by your biggest challenge, who'd be on the list?
  1) I can list them now — I just hadn't paused to
  2) One or two teammates would feel it
  3) The whole team plus people downstream
  4) Honestly, I don't see others affected
> 4

Name one person you could thank, by name, tomorrow morning — and the specific thing you'd thank them for.
  1) More than one — today gave me several
  2) I have a name and a clear reason
  3) I have a name, but I'd have to think about why
  4) I'd have to think about both
> 4

Today stayed close to you. That's not failure — sometimes the work demands it, and the day costs what it costs. But notice this: when the world shrinks to you-sized problems, the problems also start to feel you-sized. Tomorrow, look up once, on purpose. Just once.

[press Enter to continue]

------------------------------------------------------------
Here's the shape of your day, in your own answers:

  • Agency (Locus):       you leaned **external**
  • Orientation:          you leaned **entitlement**
  • Radius of concern:    you leaned **self**

You opened by calling today "Tough". When you picked one interaction, it was: "I felt my work wasn't seen the way it deserved". When you thought about the biggest challenge, the person on your mind was: "Just me — it was my problem to solve".

None of this is a grade. It's a mirror. The point of the mirror isn't to like or dislike what you see — it's to recognize it. Tomorrow is another sample.
------------------------------------------------------------

[press Enter to continue]

That's it for tonight. Close the laptop. See you tomorrow.
```

---

## What this transcript demonstrates

| Branch point                          | What happened                                                                        |
| ------------------------------------- | ------------------------------------------------------------------------------------ |
| `A1_D1` (route by opening word)       | "Tough" → routed to the **low-agency** subtree (`A1_Q_LOW`, `A1_Q2_EXT`).            |
| `A1_D2` (signal compare)              | `axis1.external = 2`, `axis1.internal = 0` → routed to `A1_R_EXT`.                   |
| `A2_D1` (route by orientation answer) | "I felt my work wasn't seen…" → routed to the **expecting** subtree (`A2_Q_EXPECT`). |
| `A2_D2` (signal compare)              | `axis2.entitlement = 3`, `axis2.contribution = 0` → routed to `A2_R_ENTITLE`.        |
| `A3_D1` (route by radius answer)      | "Just me — it was my problem" → routed to the **self** subtree (`A3_Q_SELF`).        |
| `A3_D2` (signal compare)              | `axis3.self = 3` → routed to `A3_R_SELF`.                                            |

Note the **interpolation** in `A1_R_EXT` (`"I don't think I steered anything today"` is the literal label picked at `A1_Q2_EXT`) and in `SUMMARY` (three labels + three axis dominants spliced in). No LLM, no string generation — pure lookup.
