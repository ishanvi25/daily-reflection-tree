"""
Daily Reflection Tree — deterministic CLI agent.

Loads the tree from a JSON file (Part A deliverable) and walks it.
NO LLM, NO randomness, NO free text. Same answers -> same path -> same summary.

Usage:
    python agent.py                                   # uses ../tree/reflection-tree.json
    python agent.py path/to/tree.json                 # custom tree file
    python agent.py --replay 2,1,3,2,4,1,2,3,1        # scripted run (1-indexed picks)

The --replay flag is for reproducible transcripts; it does not change behavior.
"""

import json
import re
import sys
from pathlib import Path


# ---------- supported node types ----------
NODE_TYPES = {"start", "question", "decision", "reflection", "bridge", "summary", "end"}


# ---------- pretty-print helpers (CLI-only, no styling beyond ANSI dim) ----------
DIM = "33[2m"
BOLD = "33[1m"
RESET = "33[0m"


def hr():
    print(f"{DIM}{'-' * 60}{RESET}")


def wait_for_continue():
    try:
        input(f"\n{DIM}[press Enter to continue]{RESET} ")
    except EOFError:
        print()  # script piped in


# ---------- the agent ----------
class ReflectionAgent:
    def __init__(self, tree_path: Path, replay=None):
        data = json.loads(tree_path.read_text(encoding="utf-8"))
        self.nodes = data["nodes"]
        self.start_id = data.get("start", "START")
        self.meta = data.get("meta", {})

        # state ----------
        # answers[node_id]   = label string the user picked at that question node
        # signals[axis][pole] = integer tally (e.g. signals["axis1"]["internal"] = 2)
        self.answers = {}
        self.signals = {}

        # replay queue (list of 1-indexed picks). When provided, the agent uses
        # them for question nodes instead of reading stdin.
        self.replay = list(replay) if replay else None

    # ------------------------------------------------------------------
    # main loop
    # ------------------------------------------------------------------
    def run(self):
        node_id = self.start_id
        while node_id is not None:
            node = self.nodes[node_id]
            handler = getattr(self, f"_handle_{node['type']}", None)
            if handler is None:
                raise ValueError(f"Unknown node type: {node['type']} at {node_id}")
            node_id = handler(node)

    # ------------------------------------------------------------------
    # node handlers
    # ------------------------------------------------------------------
    def _handle_start(self, node):
        hr()
        print(self._interp(node["text"]))
        hr()
        return node.get("next")

    def _handle_question(self, node):
        print()
        print(f"{BOLD}{self._interp(node['text'])}{RESET}")
        options = node["options"]
        for i, opt in enumerate(options, 1):
            label = opt["label"] if isinstance(opt, dict) else opt
            print(f"  {i}) {label}")

        choice_idx = self._read_choice(len(options), node_id=node["id"])
        opt = options[choice_idx]
        label = opt["label"] if isinstance(opt, dict) else opt

        # record answer
        self.answers[node["id"]] = label

        # record signal (if any)
        if isinstance(opt, dict) and opt.get("signal"):
            self._add_signal(opt["signal"])

        return node.get("next")

    def _handle_decision(self, node):
        # decision nodes are invisible; they just route.
        for rule in node["rules"]:
            if self._matches(rule["when"]):
                return rule["goto"]
        # fallback: explicit default, or first rule, or stop.
        if "default" in node:
            return node["default"]
        if node["rules"]:
            return node["rules"][0]["goto"]
        return None

    def _handle_reflection(self, node):
        print()
        print(self._interp(node["text"]))
        wait_for_continue()
        return node.get("next")

    def _handle_bridge(self, node):
        print()
        hr()
        print(f"{DIM}{self._interp(node['text'])}{RESET}")
        hr()
        return node.get("next")

    def _handle_summary(self, node):
        print()
        hr()
        print(self._interp(node["text"]))
        hr()
        wait_for_continue()
        return node.get("next")

    def _handle_end(self, node):
        print()
        print(self._interp(node["text"]))
        print()
        return None

    # ------------------------------------------------------------------
    # signals + decisions
    # ------------------------------------------------------------------
    def _add_signal(self, signal_str):
        # format: "axisN:pole"
        axis, pole = signal_str.split(":", 1)
        self.signals.setdefault(axis, {})[pole] = self.signals.get(axis, {}).get(pole, 0) + 1

    def _signal(self, axis, pole):
        return self.signals.get(axis, {}).get(pole, 0)

    def _dominant(self, axis):
        """Return the pole with the highest tally, or 'balanced' on a tie."""
        bucket = self.signals.get(axis, {})
        if not bucket:
            return "balanced"
        max_v = max(bucket.values())
        winners = [p for p, v in bucket.items() if v == max_v]
        return winners[0] if len(winners) == 1 else "balanced"

    def _matches(self, cond):
        """
        Supported forms:
          { "answer_of": "NODE_ID", "in": ["label", ...] }
          { "signal_compare": "axis1.internal > axis1.external" }
          { "signal_compare": "axisN.poleA == axisN.poleB" }
          { "signal_compare": "expr_A and expr_B" }      (and/or only)
        """
        if "answer_of" in cond:
            return self.answers.get(cond["answer_of"]) in cond["in"]
        if "signal_compare" in cond:
            return self._eval_signal_expr(cond["signal_compare"])
        return False

    # very small, safe expression evaluator for signal comparisons.
    _TOKEN_RE = re.compile(r"\s*(\(|\)|and|or|>=|<=|==|!=|>|<|[A-Za-z][A-Za-z0-9_]*\.[A-Za-z][A-Za-z0-9_]*|\d+)")

    def _eval_signal_expr(self, expr):
        # Tokenize, replace `axisN.pole` with their integer tallies,
        # then evaluate using Python on a whitelisted token set only.
        tokens = []
        i = 0
        while i < len(expr):
            m = self._TOKEN_RE.match(expr, i)
            if not m:
                raise ValueError(f"Bad signal_compare expression near: {expr[i:]}")
            tok = m.group(1)
            i = m.end()
            if "." in tok and tok not in ("and", "or"):
                axis, pole = tok.split(".")
                tok = str(self._signal(axis, pole))
            tokens.append(tok)
        safe_expr = " ".join(tokens)
        if not re.fullmatch(r"[\d\s\(\)<>=!andor]+", safe_expr):
            raise ValueError(f"Refusing to eval unsafe expression: {safe_expr}")
        return bool(eval(safe_expr, {"__builtins__": {}}, {}))  # noqa: S307 (whitelisted)

    # ------------------------------------------------------------------
    # text interpolation
    # ------------------------------------------------------------------
    _PLACEHOLDER_RE = re.compile(r"\{([A-Za-z0-9_]+)\.([A-Za-z0-9_]+)\}")

    def _interp(self, text):
        def repl(m):
            scope, field = m.group(1), m.group(2)
            if field == "answer":
                return self.answers.get(scope, f"<{scope}.answer not yet set>")
            if field == "dominant" and scope.startswith("axis"):
                return self._dominant(scope)
            return m.group(0)
        return self._PLACEHOLDER_RE.sub(repl, text)

    # ------------------------------------------------------------------
    # input
    # ------------------------------------------------------------------
    def _read_choice(self, n_options, node_id):
        if self.replay:
            pick = self.replay.pop(0)
            if not (1 <= pick <= n_options):
                raise ValueError(f"Replay value {pick} out of range at {node_id} (1..{n_options})")
            print(f"{DIM}> {pick}{RESET}")
            return pick - 1

        while True:
            try:
                raw = input(f"{DIM}> {RESET}").strip()
            except EOFError:
                raise SystemExit("\nEOF on input. Exiting.")
            if raw.isdigit():
                pick = int(raw)
                if 1 <= pick <= n_options:
                    return pick - 1
            print(f"  {DIM}please enter a number 1-{n_options}{RESET}")


# ----------------------------------------------------------------------
# CLI entrypoint
# ----------------------------------------------------------------------
def parse_argv(argv):
    tree_path = Path(__file__).parent.parent / "tree" / "reflection-tree.json"
    replay = None
    args = list(argv[1:])
    while args:
        a = args.pop(0)
        if a == "--replay":
            replay = [int(x) for x in args.pop(0).split(",") if x.strip()]
        elif a in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        else:
            tree_path = Path(a)
    return tree_path, replay


def main():
    tree_path, replay = parse_argv(sys.argv)
    if not tree_path.exists():
        print(f"Tree file not found: {tree_path}", file=sys.stderr)
        sys.exit(1)
    ReflectionAgent(tree_path, replay=replay).run()


if __name__ == "__main__":
    main()


