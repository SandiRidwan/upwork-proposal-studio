"""
Job analyzer.

Reads a pasted Upwork job post and extracts:
  - the niche (A..E, matching knowledge/positioning.md)
  - the failure mode (what went wrong last time, in the client's words)
  - the named symptom (so move 2 can hit it exactly)
  - client type, urgency, budget signal
  - red/green flags
  - which credibility fact and which portfolio link to use
  - variant (short vs process)

Two layers:
  1. **heuristics** - instant, no key needed. Keyword scoring.
  2. **LLM refine** - if a key is available, sharpens failure_mode and the
     one true observation. Falls back silently to heuristics.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field, asdict
from typing import Optional

from . import llm


# ---------------------------------------------------------------- signals

NICHE_SIGNALS = {
    "A": {  # anti-bot / hard-target scraping
        "keywords": [
            "scrap", "scraper", "scraping", "crawl", "crawler", "extract",
            "web data", "captcha", "cloudflare", "akamai", "datadome",
            "blocked", "bypass", "anti-bot", "antibbot", "rotating proxy",
            "proxies", "selenium", "playwright", "puppeteer", "headless",
            "bot detection", "tls", "fingerprint", "login wall", "403",
            "marketplace", "linkedin", "amazon", "indeed", "zillow",
        ],
        "weight": 1.0,
    },
    "B": {  # automation / pipeline / enrichment
        "keywords": [
            "automation", "automate", "pipeline", "workflow", "integrate",
            "integration", "zapier", "make.com", "n8n", "airtable", "notion",
            "webhook", "api connection", "sync", "enrich", "enrichment",
            "crm", "hubspot", "salesforce", "sheets", "google sheets",
            "recurring", "scheduled", "run daily", "ongoing",
        ],
        "weight": 1.0,
    },
    "C": {  # data analysis / dashboard
        "keywords": [
            "analyze", "analysis", "analytics", "dashboard", "report",
            "insight", "insights", "visualization", "visualisation", "chart",
            "kpi", "sql", "power bi", "tableau", "looker", "streamlit",
            "pandas", "data cleaning", "data quality", "forecast", "trend",
            "excel report", "pivot", "cohort", "ab test", "a/b test",
            "statistical", "regression",
        ],
        "weight": 1.0,
    },
    "D": {  # platform / api / infra
        "keywords": [
            "api", "rest api", "fastapi", "flask", "backend", "docker",
            "deploy", "deployment", "server", "cloud", "aws", "gcp",
            "postgres", "database", "microservice", "endpoint", "saas",
        ],
        "weight": 1.0,
    },
    "E": {  # lead gen / market intel
        "keywords": [
            "leads", "lead gen", "lead generation", "b2b", "prospect",
            "contact list", "email list", "company list", "competitor",
            "competition", "market intel", "market intelligence", "pricing data",
            "price monitoring", "google maps", "directory",
        ],
        "weight": 1.0,
    },
}

CLIENT_TYPE_SIGNALS = {
    "enterprise": ["enterprise", "our company", "our team", "ndas", "legal",
                   "compliance", "soc 2", "procurement", "vendor"],
    "agency": ["my client", "for a client", "our client", "agency", "white-label",
               "white label", "reseller"],
    "startup": ["startup", "we're building", "mvp", "seed", "founder",
                "co-founder", "our app", "beta"],
    "first_timer": ["first time", "never hired", "new to upwork", "first project"],
    "serial": ["ongoing", "long term", "long-term", "multiple projects",
               "recurring", "as needed", "retainer"],
}

URGENCY_SIGNALS = {
    "high": ["asap", "urgent", "today", "tonight", "this week", "immediately",
             "right away", "fast", "quick turnaround", "deadline"],
    "low": ["no rush", "flexible", "whenever", "exploratory", "planning",
            "next month", "q1", "q2"],
}

RED_FLAG_SIGNALS = {
    "suspiciously_cheap": ["$5", "$10", "$20 fixed", "simple task", "easy job",
                           "quick task", "small budget"],
    "off_platform": ["whatsapp", "telegram", "email me", "contact me at",
                     "outside upwork", "paypal", "crypto payment"],
    "unrealistic_volume": ["million records", "1m records", "unlimited",
                           "all data", "everything"],
    "account_harm": ["fake accounts", "spam", "bypass login of others",
                     "hack", "crack password", "steal"],
}


# ---------------------------------------------------------------- result

@dataclass
class JobAnalysis:
    niche: str = "A"
    niche_label: str = ""
    failure_mode: str = ""
    named_symptom: str = ""
    client_type: str = "unspecified"
    urgency: str = "medium"
    budget_signal: str = "unspecified"
    red_flags: list = field(default_factory=list)
    green_flags: list = field(default_factory=list)
    one_true_observation: str = "[ADD: a specific detail about the client or target]"
    credibility_fact: str = ""
    portfolio_link: str = ""
    variant: str = "short"
    niche_scores: dict = field(default_factory=dict)
    used_llm: bool = False

    def to_dict(self) -> dict:
        return asdict(self)


NICHE_LABEL = {
    "A": "anti-bot / hard-target scraping",
    "B": "data automation / pipeline / enrichment",
    "C": "data analysis / dashboard",
    "D": "platform / API / infrastructure",
    "E": "lead gen / market intelligence",
}


# ---------------------------------------------------------------- heuristic core

def _score_niches(text: str) -> dict:
    low = text.lower()
    scores = {}
    for niche, spec in NICHE_SIGNALS.items():
        s = 0.0
        for kw in spec["keywords"]:
            if kw in low:
                s += spec["weight"] * (1.0 + (len(kw.split()) - 1) * 0.3)
        scores[niche] = round(s, 2)
    return scores


def _pick_urgency(text: str) -> str:
    low = text.lower()
    for level in ("high", "low"):
        for kw in URGENCY_SIGNALS[level]:
            if kw in low:
                return level
    return "medium"


def _pick_client_type(text: str) -> str:
    low = text.lower()
    for ctype, kws in CLIENT_TYPE_SIGNALS.items():
        for kw in kws:
            if kw in low:
                return ctype
    return "unspecified"


def _detect_red_flags(text: str) -> list:
    low = text.lower()
    found = []
    for flag, kws in RED_FLAG_SIGNALS.items():
        for kw in kws:
            if kw in low:
                found.append(flag)
                break
    return found


def _detect_green_flags(text: str) -> list:
    low = text.lower()
    out = []
    if re.search(r"https?://", text):
        out.append("has_url")
    if re.search(r"\$\s?\d", text):
        out.append("states_budget")
    if any(k in low for k in ["sample", "example", "spreadsheet", "dataset",
                              "csv", "access"]):
        out.append("offers_material")
    if any(k in low for k in ["last freelancer", "previous developer",
                              "before", "tried", "attempted"]):
        out.append("mentions_failure")
    return out


def _budget_signal(text: str) -> str:
    low = text.lower()
    if re.search(r"hourly", low):
        return "hourly"
    if re.search(r"fixed", low):
        return "fixed-price"
    if re.search(r"\$\s?\d", text):
        return "amount mentioned"
    return "unspecified"


# ---------------------------------------------------------------- public

def analyze(job_post: str, *, use_llm: bool = True) -> JobAnalysis:
    """Analyze a job post. Always works; uses LLM only to sharpen prose fields."""
    text = (job_post or "").strip()
    scores = _score_niches(text)
    niche = max(scores, key=scores.get) if any(scores.values()) else "A"

    a = JobAnalysis(
        niche=niche,
        niche_label=NICHE_LABEL[niche],
        niche_scores=scores,
        urgency=_pick_urgency(text),
        client_type=_pick_client_type(text),
        budget_signal=_budget_signal(text),
        red_flags=_detect_red_flags(text),
        green_flags=_detect_green_flags(text),
        portfolio_link=_default_portfolio(niche),
        credibility_fact=_default_credibility(niche),
    )

    a.variant = "short" if (a.urgency == "high" or len(text) < 700) else "process"
    a.failure_mode = _heuristic_failure_mode(text, niche)
    a.named_symptom = _heuristic_symptom(text)

    if use_llm and llm.is_live():
        refined = _refine_with_llm(a, text)
        if refined:
            a.used_llm = True

    return a


def _default_portfolio(niche: str) -> str:
    return {
        "A": "https://github.com/SandiRidwan/ct-appellate-court-scraper",
        "B": "https://github.com/SandiRidwan/lead-intelligence-pipeline",
        "C": "https://github.com/SandiRidwan/morrisons-market-intelligence",
        "D": "https://github.com/SandiRidwan/public-data-api",
        "E": "https://github.com/SandiRidwan/saudi-b2b-leads-validator",
    }[niche]


def _default_credibility(niche: str) -> str:
    return {
        "A": "Bypassed Akamai and DataDome without a browser, by finding the "
             "unguarded path rather than solving the challenge.",
        "B": "Runs pipelines that alert on their own failures and log the "
             "reason, so month three does not go silently wrong.",
        "C": "Caught a silent price-column trap before it reached the client, "
             "then shipped the dashboard a stakeholder could click through.",
        "D": "Ships REST APIs with validation, pagination, and health checks "
             "that survive a real deploy, not just localhost.",
        "E": "Measures coverage before promising volume, after finding a path "
             "that looked complete and only reached part of the catalogue.",
    }[niche]


def _heuristic_failure_mode(text: str, niche: str) -> str:
    low = text.lower()
    if any(k in low for k in ["blocked", "captcha", "403", "cloudflare",
                              "akamai", "datadome", "anti-bot"]):
        return "They tried scraping and the target site blocked them."
    if any(k in low for k in ["manual", "copy paste", "copy-paste",
                              "spend hours", "waste time", "by hand"]):
        return "Their workflow is manual and eating someone's week."
    if any(k in low for k in ["last freelancer", "previous developer",
                              "didn't work", "no show", "ghosted"]):
        return "A previous freelancer did not deliver or disappeared."
    if any(k in low for k in ["don't trust", "can't trust", "wrong numbers",
                              "inaccurate", "not sure if"]):
        return "They cannot trust the numbers they already have."
    if niche == "E":
        return "Their current lead or market data is stale or incomplete."
    if niche == "C":
        return "They have data but no clear decision coming out of it."
    if niche == "B":
        return "Something that should run itself still needs a human."
    return "The current way of doing this is not working, and they want it fixed."


def _heuristic_symptom(text: str) -> str:
    low = text.lower()
    for kw in ["blocked", "captcha", "403", "rate limit", "banned", "ip block",
               "cloudflare", "timeout", "crash", "error", "missing", "inaccurate",
               "manual", "slow", "stale"]:
        if kw in low:
            return kw
    return ""


# ---------------------------------------------------------------- LLM refine

_REFINE_SYSTEM = """You are helping a freelance proposal writer understand a job post.
Return ONLY a JSON object, no prose, with keys:
  "failure_mode": one sentence, phrased as what went wrong for the client before
  "named_symptom": the exact symptom words the client used (short)
  "one_true_observation": a specific, true-sounding observation an expert would make
     after reading this post. If the post is too vague, use a placeholder that starts
     with "[ADD:" and asks for the missing detail.
  "budget_signal": what you can infer about budget (short)
Do not invent client names, numbers, or results. Keep every field under 40 words."""


def _refine_with_llm(a: JobAnalysis, text: str) -> bool:
    user = (
        f"Detected niche: {a.niche} ({a.niche_label})\n"
        f"Client type: {a.client_type}\n"
        f"Urgency: {a.urgency}\n\n"
        f"Job post:\n{text[:4000]}"
    )
    res = llm.ask(_REFINE_SYSTEM, user, temperature=0.3, max_tokens=500)
    if not res.ok:
        return False
    data = _extract_json(res.text)
    if not data:
        return False
    for key in ("failure_mode", "named_symptom", "one_true_observation",
                "budget_signal"):
        val = data.get(key)
        if isinstance(val, str) and val.strip():
            setattr(a, key, val.strip())
    return True


def _extract_json(text: str) -> Optional[dict]:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\n?", "", text)
        text = re.sub(r"\n?```$", "", text)
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        return None
    try:
        return json.loads(text[start:end + 1])
    except Exception:
        return None
