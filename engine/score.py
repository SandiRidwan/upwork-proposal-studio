"""
Score any proposal text against the same deterministic rules the engine uses.

Use it to compare what opencode produced against what the engine produced, with
numbers instead of vibes.

    python -m engine.score proposal.txt
    type proposal.txt | python -m engine.score
    python -m engine.score --proposal-text "..." --job-post "..."

It prints a 0-100 score from the deterministic checks, plus the concrete problems.
This is the same linter the engine runs before sending, exposed on its own.
"""

from __future__ import annotations

import argparse
import sys

from .writer import lint


def _weights(issue: dict) -> int:
    return {
        "placeholder_left_in": 25,   # a to-do note in a sent proposal is fatal
        "criticises_post": 15,       # telling the client their brief is weak loses the job
        "banned_phrase": 18,
        "exclamation": 12,
        "emoji": 12,
        "em_dash": 6,
        "ai_tell": 6,
        "pronoun_ratio": 8,
        "marketing_word": 6,
        "too_short": 10,
        "too_long": 6,
    }.get(issue["rule"], 4)


def score(proposal: str) -> tuple[int, list[dict]]:
    issues = lint(proposal)
    penalty = sum(_weights(i) for i in issues)
    return max(0, 100 - penalty), issues


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m engine.score")
    ap.add_argument("file", nargs="?", help="proposal text file (or stdin)")
    ap.add_argument("--proposal-text", default="", help="proposal as a string")
    ap.add_argument("--job-post", default="", help="unused here; kept for symmetry")
    args = ap.parse_args(argv)

    text = args.proposal_text
    if not text and args.file:
        with open(args.file, encoding="utf-8-sig") as f:
            text = f.read()
    if not text:
        text = sys.stdin.read()
    if not text.strip():
        print("No proposal text provided.", file=sys.stderr)
        return 2

    val, issues = score(text)
    words = len(text.split())
    print(f"score: {val}/100   ({words} words)")
    if issues:
        print("problems:")
        for i in issues:
            print(f"  - {i['rule']}: {i['detail']}")
    else:
        print("no problems: passes the voice rules")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
