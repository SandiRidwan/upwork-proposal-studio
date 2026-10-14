"""
Tiny .env loader (no dependency).

Reads a .env file and sets any key that is not already present in the
environment, so a real shell variable always wins over the file. Handles the
subset of .env syntax that matters here: KEY=VALUE, optional quotes, # comments,
and blank lines.

It also reads opencode's provider credentials (`auth.json`) so the engine can
reuse the exact same provider/model the user already runs in opencode, without
copying keys around.

Search order (first found wins):
  1. $UPS_ENV_FILE, if set
  2. ./.env                         (next to the repo root)
  3. ../clipper-tools/.env          (the author's shared key store, if present)

Call load_env() once at startup (app.py and engine/cli.py both do).
"""

from __future__ import annotations

import json
import os
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent

_SEARCH = [
    _ROOT / ".env",
    _ROOT.parent / "clipper-tools" / ".env",
]

_loaded_from: str | None = None


def _opencode_auth_path() -> Path | None:
    """opencode stores provider credentials here."""
    cand = Path(os.path.expanduser("~")) / ".local" / "share" / "opencode" / "auth.json"
    return cand if cand.is_file() else None


def _load_opencode_auth() -> str | None:
    """
    Map opencode's auth.json providers to our env vars, without overwriting
    anything already set. Sets both a generic opencode provider key and any
    known provider-specific key (gemini, etc.).
    """
    path = _opencode_auth_path()
    if not path:
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return None

    set_any = False
    for name, cred in (data or {}).items():
        if not isinstance(cred, dict):
            continue
        key = cred.get("key") or cred.get("access") or ""
        base = cred.get("baseURL") or cred.get("base_url") or ""
        if not key and not base:
            continue
        # keep the primary opencode provider reachable from the engine
        if "OPENCODE_API_KEY" not in os.environ:
            os.environ["OPENCODE_API_KEY"] = key
            os.environ.setdefault("OPENCODE_BASE_URL", base)
            set_any = True
        # also expose well-known providers by their usual env name
        mapping = {
            "gemini": "GEMINI_API_KEY",
            "openai": "OPENAI_API_KEY",
            "groq": "GROQ_API_KEY",
            "openrouter": "OPENROUTER_API_KEY",
        }
        envname = mapping.get(name)
        if envname and envname not in os.environ and key:
            os.environ[envname] = key
    return str(path) if set_any else None


def _parse(path: Path) -> dict:
    out: dict[str, str] = {}
    try:
        text = path.read_text(encoding="utf-8-sig")
    except OSError:
        return out
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].strip()
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in ("'", '"'):
            val = val[1:-1]
        if key:
            out[key] = val
    return out


def load_env(*, override: bool = False) -> str | None:
    """
    Load the first available .env. Returns the path used, or None.

    Existing environment variables win unless override=True, so a value set in
    the shell is never silently replaced by the file.
    """
    global _loaded_from

    candidates = []
    forced = os.environ.get("UPS_ENV_FILE")
    if forced:
        candidates.append(Path(forced))
    candidates.extend(_SEARCH)

    for path in candidates:
        if not path.is_file():
            continue
        values = _parse(path)
        for k, v in values.items():
            if override or k not in os.environ:
                os.environ[k] = v
        _loaded_from = str(path)
        _load_opencode_auth()
        return _loaded_from

    # no .env file: still try opencode's credentials
    auth = _load_opencode_auth()
    if auth:
        _loaded_from = auth
    return _loaded_from


def loaded_from() -> str | None:
    return _loaded_from


def init() -> None:
    """Load env and, if a key is present, pick a matching default provider."""
    path = load_env()
    # If a provider was not forced but a known key exists, let the llm module
    # auto-detect it (llm._detect_provider does that). Nothing else needed.
    _ = path
