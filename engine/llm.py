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
    UPS_PROVIDER   = gemini | openai | groq | openrouter | ollama
                     (default: auto-detect by which key is present)
    UPS_MODEL      = model name (default per provider)
    GEMINI_API_KEY / OPENAI_API_KEY / GROQ_API_KEY / OPENROUTER_API_KEY
    UPS_BASE_URL   = override base url
    UPS_LLM_MODE   = auto | provider | prompt   (default: auto)

Keys are read from a .env file automatically (./env then ../clipper-tools/.env);
see engine/env.py. No key is required to use this repo.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Optional

from . import env as _env

# load .env once, so key auto-detection below sees the file's values
_env.load_env()


# ---------------------------------------------------------------- providers

PROVIDERS = {
    "gemini": {
        # Google's OpenAI-compatible endpoint.
        # gemini-flash-lite-latest works across both older and newer Cloud
        # projects; gemini-2.5-flash is 404 for new projects and 429 once the
        # free daily quota is spent, so it is only a fallback here.
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai",
        "key_env": "GEMINI_API_KEY",
        "default_model": "gemini-flash-lite-latest",
        "alt_models": ["gemini-flash-latest", "gemini-2.5-flash"],
    },
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
        "keys": len(_keys_for(prov, PROVIDERS[prov])) if prov else 0,
    }


def _keys_for(prov: str, cfg: dict) -> list:
    """
    All usable keys for a provider, primary first.

    Reads <KEY_ENV> and an optional plural <KEY_ENV>S (e.g. GEMINI_API_KEY and
    GEMINI_API_KEYS), the latter comma/space/newline separated. Deduped, order
    preserved. Empty for providers that need no key (ollama).
    """
    import re
    env_name = cfg.get("key_env") or ""
    if not env_name:
        return []
    found: list[str] = []

    def add(raw: str):
        for k in re.split(r"[\s,]+", raw or ""):
            k = k.strip()
            if k and k not in found:
                found.append(k)

    add(os.environ.get(env_name, ""))
    plural = env_name + "S"
    if plural != env_name:
        add(os.environ.get(plural, ""))
    return found


# ---------------------------------------------------------------- call

def ask(
    system: str,
    user: str,
    *,
    temperature: float = 0.7,
    max_tokens: int = 2000,
    timeout: int = 120,
) -> LLMResult:
    """Send a chat completion. Falls back to prompt mode on any failure."""
    mode = llm_mode()
    prov = _detect_provider()

    assembled = f"### SYSTEM\n{system}\n\n### USER\n{user}"

    if mode == "prompt" or prov is None:
        why = (
            "prompt mode requested"
            if mode == "prompt"
            else "no API key found (set GEMINI_API_KEY / OPENAI_API_KEY / "
            "GROQ_API_KEY / OPENROUTER_API_KEY, or UPS_PROVIDER=ollama)"
        )
        return LLMResult(
            ok=False, text=assembled, provider="prompt", prompt=assembled, error=why
        )

    cfg = PROVIDERS[prov]
    base_url = os.environ.get("UPS_BASE_URL") or cfg["base_url"]
    model = os.environ.get("UPS_MODEL") or cfg["default_model"]
    keys = _keys_for(prov, cfg)

    # Reasoning models (e.g. gemini-2.5-flash) spend part of the budget on
    # hidden thinking tokens, so a small max_tokens truncates the visible text.
    # Give them a much bigger budget unless the caller asked for something tiny.
    thinking = "gemini-2.5" in model.lower() or "thinking" in model.lower()
    if thinking and max_tokens < 4000:
        max_tokens = max(max_tokens * 4, 4000)

    def _post(mt: int, mdl: str, key: str):
        payload = {
            "model": mdl,
            "temperature": temperature,
            "max_tokens": mt,
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
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    # Try (model x key) combinations until one works. Handles the two failure
    # modes seen with shared key pools:
    #   - 429: this key's quota for the model is spent -> next key
    #   - 404: this model is not enabled on that key's project -> next model
    # Each pair is tried once, with a growing backoff on transient errors.
    import time
    models = [os.environ.get("UPS_MODEL") or model]
    for alt in cfg.get("alt_models", []):
        if alt not in models:
            models.append(alt)
    combos = [(m, k) for m in models for k in (keys or [""])]
    if not combos:
        combos = [(model, "")]

    max_tries = int(os.environ.get("UPS_LLM_RETRIES", str(len(combos))))
    max_tries = max(1, min(max_tries, len(combos)))

    last_err = ""
    data = None
    for attempt, (m, k) in enumerate(combos[:max_tries]):
        try:
            data = _post(max_tokens, m, k)
            model = m  # remember which model actually answered
            break
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read().decode("utf-8", "replace")[:200]
            except Exception:
                pass
            last_err = f"HTTP {e.code} ({m}): {body}"
            if e.code in (429, 404, 500, 502, 503, 504):
                time.sleep(1.0)
                continue
            return LLMResult(False, assembled, "prompt", assembled, last_err)
        except Exception as e:  # timeout, connection reset, parse
            last_err = f"{type(e).__name__} ({m}): {e}"
            time.sleep(1.0)
            continue

    if data is None:
        return LLMResult(False, assembled, "prompt", assembled, last_err)

    try:
        choice = data["choices"][0]
        text = (choice["message"].get("content") or "").strip()
        finish = choice.get("finish_reason")

        # Truncated by the token cap: retry once with a much bigger budget,
        # on the same model/key that just worked.
        if finish == "length" or not text:
            try:
                bigger = max(max_tokens * 3, 8000)
                data = _post(bigger, model, k)
                choice = data["choices"][0]
                new_text = (choice["message"].get("content") or "").strip()
                if new_text:
                    text = new_text
                    finish = choice.get("finish_reason")
            except Exception:
                pass

        if not text:
            return LLMResult(False, assembled, "prompt", assembled,
                             "empty completion (finish_reason=%s)" % finish)

        ok = finish != "length"
        return LLMResult(ok=ok, text=text, provider=prov, prompt=assembled,
                         error="" if ok else "truncated at max_tokens")
    except (KeyError, IndexError, TypeError) as e:
        return LLMResult(False, assembled, "prompt", assembled,
                         f"unexpected response shape: {e}")
