"""
Load the skill files (the identity + rule layer).

Mirrors the folder layout of the two source skills so the reference files are
edited in place, exactly as a Claude Skill would be. This repo just reads them
from disk and feeds them to the prompt.

    skills/upwork-proposal/SKILL.md
    skills/upwork-proposal/references/{positioning,portfolio,voice-rules,
        winning-proposals,client-research}.md
    skills/upwork-hiring-panel/SKILL.md
    skills/upwork-hiring-panel/references/{personas,rubric,winning-patterns,
        hook-lab}.md
"""

from __future__ import annotations

from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SKILLS = _ROOT / "skills"

WRITER = _SKILLS / "upwork-proposal"
PANEL = _SKILLS / "upwork-hiring-panel"


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError:
        return ""


# ---- writer skill ------------------------------------------------------

def writer_skill() -> str:
    return _read(WRITER / "SKILL.md")


def positioning() -> str:
    return _read(WRITER / "references" / "positioning.md")


def portfolio() -> str:
    return _read(WRITER / "references" / "portfolio.md")


def voice() -> str:
    return _read(WRITER / "references" / "voice-rules.md")


def wins() -> str:
    return _read(WRITER / "references" / "winning-proposals.md")


def research() -> str:
    return _read(WRITER / "references" / "client-research.md")


# ---- panel skill -------------------------------------------------------

def panel_skill() -> str:
    return _read(PANEL / "SKILL.md")


def personas() -> str:
    return _read(PANEL / "references" / "personas.md")


def rubric() -> str:
    return _read(PANEL / "references" / "rubric.md")


def winning_patterns() -> str:
    return _read(PANEL / "references" / "winning-patterns.md")


def hook_lab() -> str:
    return _read(PANEL / "references" / "hook-lab.md")


# ---- freelancer's own wins (optional) ----------------------------------

def freelancer_wins() -> str:
    """
    knowledge/wins.md - job posts + proposals that actually got hired.
    Strongest evidence available when it exists. Empty if absent.
    """
    return _read(_ROOT / "knowledge" / "wins.md")


def all_knowledge() -> dict:
    return {
        "writer_skill": writer_skill(),
        "positioning": positioning(),
        "portfolio": portfolio(),
        "voice": voice(),
        "wins": wins(),
        "research": research(),
        "panel_skill": panel_skill(),
        "personas": personas(),
        "rubric": rubric(),
        "winning_patterns": winning_patterns(),
        "hook_lab": hook_lab(),
        "freelancer_wins": freelancer_wins(),
    }


def find_forward_compat() -> bool:
    """True if the skill files are present (used by tests)."""
    return bool(writer_skill()) and bool(panel_skill())
