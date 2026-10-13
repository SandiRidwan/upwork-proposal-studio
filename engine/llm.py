"""
LLM provider abstraction.

Designed to work in three modes so the tool is useful whether or not the user
has a key:

1. **auto**       - try the configured provider; if unavailable, fall back to
                    "prompt mode" which returns a ready-to-paste prompt you can
                    run in opencode / any chat.
2. **provider**   - call a real API (openai-compatible, groq, openrouter, ollama).
3. **prompt**     - never call an API; assemble the full prompt and return it.

Environment variables (all optional):
    UPS_PROVIDER   = openai | groq | openrouter | ollama   (default: auto-detect)
    UPS_MODEL      = model name (default per provider)
    OPENAI_API_KEY / GROQ_API_KEY / OPENROUTER_API_KEY
    UPS_BASE_URL   = override base url
    UPS_LLM_MODE   = auto | provider | prompt   (default: auto)

No key is required to use this repo.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Optional


# ---------------------------------------------------------------- providers

PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "key_env": "OPENAI_API_KEY",
        "default_model": "gpt-4o-mini",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "key_env": "GROQ_API_KEY",
        "default_model": "llama-3.3-70b-versatile",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "key_env": "OPENROUTER_API_KEY",
        "default_model": "anthropic/claude-3.5-sonnet",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "key_env": "",  # local, no key
        "default_model": "llama3.1",
    },
}


@dataclass
class LLMResult:
    ok: bool
    text: str
    provider: str
    prompt: str = ""
    error: str = ""

    def to_dict(self) -> dict:
        return {
            "ok": self.ok,
            "text": self.text,
            "provider": self.provider,
            "error": self.error,
        }


# ---------------------------------------------------------------- config

def _detect_provider() -> Optional[str]:
    forced = os.environ.get("UPS_PROVIDER", "").strip().lower()
    if forced and forced in PROVIDERS:
        return forced
    for name, cfg in PROVIDERS.items():
        env = cfg["key_env"]
        if env and os.environ.get(env):
            return name
    # ollama is always a candidate if it's running, but we don't probe here
    return None


def llm_mode() -> str:
    """auto | provider | prompt"""
    return os.environ.get("UPS_LLM_MODE", "auto").strip().lower()


def is_live() -> bool:
    """True if a real API call is likely to succeed."""
    mode = llm_mode()
    if mode == "prompt":
        return False
    if mode == "provider":
        return _detect_provider() is not None
    return _detect_provider() is not None


def status() -> dict:
    prov = _detect_provider()
    return {
        "mode": llm_mode(),
        "provider": prov,
        "model": os.environ.get("UPS_MODEL")
        or (PROVIDERS[prov]["default_model"] if prov else None),
        "live": is_live(),
    }


# ---------------------------------------------------------------- call

def ask(
    system: str,
    user: str,
    *,
    temperature: float = 0.7,
    max_tokens: int = 1600,
    timeout: int = 90,
) -> LLMResult:
    """Send a chat completion. Falls back to prompt mode on any failure."""
    mode = llm_mode()
    prov = _detect_provider()

    assembled = f"### SYSTEM\n{system}\n\n### USER\n{user}"

    if mode == "prompt" or prov is None:
        why = (
            "prompt mode requested"
            if mode == "prompt"
            else "no API key found (set OPENAI_API_KEY / GROQ_API_KEY / "
            "OPENROUTER_API_KEY, or UPS_PROVIDER=ollama)"
        )
        return LLMResult(
            ok=False, text=assembled, provider="prompt", prompt=assembled, error=why
        )

    cfg = PROVIDERS[prov]
    base_url = os.environ.get("UPS_BASE_URL") or cfg["base_url"]
    model = os.environ.get("UPS_MODEL") or cfg["default_model"]
    key = os.environ.get(cfg["key_env"], "") if cfg["key_env"] else ""

    payload = {
        "model": model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            **({"Authorization": f"Bearer {key}"} if key else {}),
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        text = data["choices"][0]["message"]["content"].strip()
        return LLMResult(ok=True, text=text, provider=prov, prompt=assembled)
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")[:400]
        except Exception:
            pass
        err = f"HTTP {e.code} from {prov}: {body}"
        return LLMResult(False, assembled, "prompt", assembled, err)
    except Exception as e:  # network, timeout, parse
        err = f"{type(e).__name__}: {e}"
        return LLMResult(False, assembled, "prompt", assembled, err)
