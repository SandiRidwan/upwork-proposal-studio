"""
Install the two skills into an agent host's skills folder.

The repo's skills/ folder already uses the layout both opencode and Claude Code
read: skills/<name>/SKILL.md plus references/. This script copies (or symlinks)
them into the right place so the agent host can find them.

    python -m engine.install                 # auto-detect opencode / claude
    python -m engine.install --host opencode # force a host
    python -m engine.install --host claude
    python -m engine.install --target <dir>  # explicit skills directory
    python -m engine.install --list          # show where it would install

Hosts and their skills directories:
    opencode : %USERPROFILE%/.config/opencode/skills   (and ~/.agents/skills)
    claude   : %USERPROFILE%/.claude/skills

Nothing is written outside these folders. Existing installs are overwritten.
"""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SRC = _ROOT / "skills"
_SKILLS = ["upwork-proposal", "upwork-hiring-panel"]


def _home() -> Path:
    return Path(os.path.expanduser("~"))


def host_dirs(host: str) -> list[Path]:
    h = _home()
    if host == "opencode":
        # the documented opencode location
        return [h / ".config" / "opencode" / "skills"]
    if host == "claude":
        return [h / ".claude" / "skills"]
    if host == "both":
        return host_dirs("opencode") + host_dirs("claude")
    return []


def detect_host() -> str:
    """Pick whichever host's skills folder already exists; else opencode."""
    h = _home()
    if (h / ".config" / "opencode").exists():
        return "opencode"
    if (h / ".claude").exists():
        return "claude"
    return "opencode"


def install(target: Path | None = None, host: str = "opencode",
            dry_run: bool = False) -> list[str]:
    if target:
        targets = [Path(target)]
    else:
        targets = host_dirs(host)

    done = []
    for base in targets:
        for name in _SKILLS:
            src = _SRC / name
            if not src.is_dir():
                continue
            dst = base / name
            done.append(str(dst))
            if dry_run:
                continue
            base.mkdir(parents=True, exist_ok=True)
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
    return done


def install_project_local(project: Path) -> list[str]:
    """
    Copy the skills into <project>/.opencode/skills so opencode picks them up
    only while working inside this repo (no global install needed).
    """
    base = Path(project) / ".opencode" / "skills"
    done = []
    for name in _SKILLS:
        src = _SRC / name
        if not src.is_dir():
            continue
        dst = base / name
        base.mkdir(parents=True, exist_ok=True)
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        done.append(str(dst))
    return done


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="python -m engine.install")
    ap.add_argument("--host", default="", help="opencode | claude | both")
    ap.add_argument("--target", default="", help="explicit skills directory")
    ap.add_argument("--project", default="", help="install into "
                    "<project>/.opencode/skills (project-local)")
    ap.add_argument("--list", action="store_true", help="show targets, do nothing")
    args = ap.parse_args(argv)

    if args.project:
        done = install_project_local(Path(args.project))
        print(f"Installed into {args.project}\\.opencode\\skills")
        for d in done:
            print(f"  {d}")
        print("\nStart opencode inside that project; the skills load automatically.")
        return 0

    host = args.host or detect_host()
    target = Path(args.target) if args.target else None

    if args.list:
        locs = [str(target)] if target else [str(d) for d in host_dirs(host)]
        print(f"host: {host}")
        for loc in locs:
            print(f"  {loc}")
        return 0

    done = install(target=target, host=host)
    if not done:
        print("No target found. Use --target <dir> or --host opencode|claude.")
        return 2

    print(f"Installed skills for host: {host}")
    for d in done:
        print(f"  {d}")
    print("\nStart a new agent session (opencode / Claude Code), then ask it to")
    print("write a proposal from a job post. It will pick up these skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
