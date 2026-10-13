"""
CLI entry point.

    python -m engine.cli --job-file job.txt
    python -m engine.cli --job-file job.txt --out result.json
    echo "job text" | python -m engine.cli

Useful inside opencode: write the job post to a file, run this, read the JSON.
"""

from __future__ import annotations

import argparse
import json
import sys

from . import env
env.load_env()  # read .env before anything inspects keys

from .pipeline import run
from . import llm, knowledge


def _save_win(job_post: str, proposal: str) -> None:
    """Append a hired win to knowledge/wins.md (the 'learn from results' rule)."""
    from datetime import datetime
    from pathlib import Path
    path = Path(__file__).resolve().parent.parent / "knowledge" / "wins.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d")
    block = (
        f"\n\n## {stamp} - hired\n\n"
        f"**Job post**\n\n> " + job_post.strip().replace("\n", "\n> ") + "\n\n"
        f"**Proposal sent**\n\n> " + proposal.strip().replace("\n", "\n> ") + "\n"
    )
    with open(path, "a", encoding="utf-8") as f:
        f.write(block)
    print(f"Appended win to {path}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="upwork-proposal-studio")
    ap.add_argument("--job-file", help="path to the job post text file")
    ap.add_argument("--client-file", help="path to client info text file")
    ap.add_argument("--screening-file", help="path to screening questions file")
    ap.add_argument("--bid", default="", help="your bid / rate")
    ap.add_argument("--out", help="write JSON result to this path")
    ap.add_argument("--no-llm", action="store_true", help="heuristics only")
    ap.add_argument("--rewrite", action="store_true", help="panel also rewrites")
    ap.add_argument("--json", action="store_true", help="print raw JSON")
    ap.add_argument("--save-win", metavar="PROPOSAL_FILE",
                    help="append a hired proposal (file) + this job to "
                         "knowledge/wins.md")
    ap.add_argument("--show-skills", action="store_true",
                    help="print the loaded skill file paths and exit")
    args = ap.parse_args(argv)

    if args.show_skills:
        import json as _json
        from pathlib import Path
        root = Path(__file__).resolve().parent.parent / "skills"
        listing = {str(p.relative_to(root.parent)): p.stat().st_size
                   for p in sorted(root.rglob("*.md"))}
        print(_json.dumps(listing, indent=2))
        return 0

    def read(path, fallback=""):
        if not path:
            return fallback
        # utf-8-sig tolerates a BOM (Windows editors and PowerShell add one)
        with open(path, encoding="utf-8-sig") as f:
            return f.read()

    if args.job_file:
        job = read(args.job_file)
    else:
        job = sys.stdin.read()

    if not job.strip():
        print("No job post provided. Use --job-file or pipe text on stdin.",
              file=sys.stderr)
        return 2

    if args.save_win:
        _save_win(job, read(args.save_win))
        return 0

    result = run(
        job,
        client_info=read(args.client_file),
        screening=read(args.screening_file),
        bid=args.bid,
        use_llm=not args.no_llm,
        rewrite=args.rewrite,
    )
    data = result.to_dict()

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Wrote {args.out}")

    if args.json or not args.out:
        print(json.dumps(data, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
