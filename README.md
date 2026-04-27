# The Daily Reflection Tree

A deterministic, end-of-day reflection tool. The tree is the product. No LLM
runs at runtime — the agent walks a static JSON file and produces the same
reflection every time for the same answers.

> **Assignment**: DT Fellowship — _Design a Deterministic Reflection Agent (no LLM in the product)_.

---

## Repository layout

```
.
├── tree/
│   ├── reflection-tree.json     <- Part A: the tree as data (33 nodes)
│   └── tree-diagram.md          <- Part A: Mermaid diagram (renders on GitHub)
├── agent/
│   └── agent.py                 <- Part B: Python CLI walker (stdlib only)
├── transcripts/
│   ├── persona-1-victim.md      <- "victim / entitled / self-centric" path
│   └── persona-2-victor.md      <- "victor / contributing / altrocentric" path
├── write-up.md                  <- Part A: 2-page design rationale
└── README.md                    <- this file
```

## Part A — reading the tree

Open [`tree/reflection-tree.json`](./tree/reflection-tree.json). The schema:

```jsonc
{
  "meta": { ... },                      // axes, interpolation rules, notes
  "start": "START",                     // entry node id
  "nodes": {
    "<NODE_ID>": {
      "id":   "<NODE_ID>",
      "type": "start | question | decision | reflection | bridge | summary | end",
      "axis": "axis1 | axis2 | axis3",  // questions/reflections only
      "text": "...",                    // shown to the user; may contain {NODE.answer} or {axisN.dominant}
      "options": [                      // question nodes only
        { "label": "...", "signal": "axisN:pole" }
      ],
      "rules": [                        // decision nodes only
        { "when": { "answer_of": "NODE_ID", "in": ["..."] }, "goto": "NODE_ID" },
        { "when": { "signal_compare": "axis1.internal > axis1.external" }, "goto": "NODE_ID" }
      ],
      "next": "NODE_ID"                 // everything except decision/end
    }
  }
}
```

Two routing primitives, both fully deterministic:

- `answer_of` — match on the literal label the user picked at an earlier question.
- `signal_compare` — boolean over signal tallies (`axis1.internal`, etc.) using `>`, `<`, `>=`, `<=`, `==`, `!=`, `and`, `or`. Numbers and operators only — no LLM, no `eval` of arbitrary text. See `_eval_signal_expr` in `agent/agent.py`.

Two interpolation primitives, applied to every node's `text`:

- `{NODE_ID.answer}` — the option label picked at that node.
- `{axisN.dominant}` — the pole with the highest tally on that axis (`balanced` on a tie).

The tree visualised: [`tree/tree-diagram.md`](./tree/tree-diagram.md).

## Part B — running the agent

Requires Python 3.8+, no third-party dependencies.

```bash
# interactive
python3 agent/agent.py

# point at a different tree file
python3 agent/agent.py path/to/other-tree.json

# scripted / reproducible run (1-indexed picks, in order)
python3 agent/agent.py --replay 1,1,1,1,1,1,1,1,1
```

The two persona transcripts in [`transcripts/`](./transcripts/) were generated with
`--replay` and committed verbatim — they are reproducible.

## Determinism guarantees

- No randomness anywhere in `agent/agent.py` (no `random`, no time-based seeding).
- No network calls, no model APIs, no environment lookups beyond loading the JSON file.
- `signal_compare` expressions are tokenised and verified to contain only digits, whitespace, parentheses, comparison operators, `and`, `or` — anything else raises before evaluation.
- Same `--replay` argument → byte-identical transcript.

## Design write-up

[`write-up.md`](./write-up.md) — why the questions, how the branching, what'd be improved.
