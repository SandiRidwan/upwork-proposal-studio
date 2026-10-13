"""Load the knowledge/ files (the identity + rule layer)."""

from __future__ import annotations

from pathlib import Path

_KNOWLEDGE_DIR = Path(__file__).resolve().parent.parent / "knowledge"

_FILES = {
    "positioning": "positioning.md",
    "portfolio": "portfolio.md",
    "voice": "voice-rules.md",
    "wins": "winning-proposals.md",
    "research": "client-research.md",
}


def _read(name: str) -> str:
    p = _KNOWLEDGE_DIR / name
    try:
        return p.read_text(encoding="utf-8")
    except OSError:
        return ""


def positioning() -> str:
    return _read(_FILES["positioning"])


def portfolio() -> str:
    return _read(_FILES["portfolio"])


def voice() -> str:
    return _read(_FILES["voice"])


def wins() -> str:
    return _read(_FILES["wins"])


def research() -> str:
    return _read(_FILES["research"])


def all_knowledge() -> dict:
    return {k: _read(v) for k, v in _FILES.items()}
