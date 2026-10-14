"""
The writer.

Turns a JobAnalysis into two labeled proposal variants (short + process), then
runs a deterministic pre-send linter that enforces the voice rules regardless of
whether an LLM was used.

Two modes:
  - live  : LLM writes the prose, then we lint and report violations.
  - prompt: we assemble the exact prompt for the user to paste into opencode;
            we also generate a deterministic skeleton so the UI is never empty.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field

from . import llm, knowledge
from .analyzer import JobAnalysis, NICHE_LABEL


BANNED_PHRASES = [
    "i read your posting", "i came across your job", "dear hiring manager",
    "hello sir", "hello ma'am", "hello maam", "looking forward to hearing",
    "i am a professional", "i am confident that i can",
    "high-quality work on time", "on time and within budget",
    "i would love the opportunity", "i am excited", "passionate about",
    "cutting-edge", "state-of-the-art", "game-changing", "best-in-class",
    "synergy", "seamless", "robust solution", "dynamic individual",
]

AI_TELLS = ["i will ", "i am ", "i have ", "i can "]


@dataclass
class Variant:
    label: str
    title: str
    body: str
    word_count: int
    lint: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "label": self.label,
            "title": self.title,
            "body": self.body,
            "word_count": self.word_count,
            "lint": self.lint,
        }


@dataclass
class ProposalBundle:
    variants: list = field(default_factory=list)
    screening_answers: list = field(default_factory=list)
    needs: list = field(default_factory=list)   # facts to fill before sending
    used_llm: bool = False
    prompt: str = ""
    notes: str = ""

    @property
    def primary(self) -> Variant:
        """The single proposal the panel judges."""
        return self.variants[0] if self.variants else Variant("proposal", "", "", 0)

    def to_dict(self) -> dict:
        return {
            "variants": [v.to_dict() for v in self.variants],
            "screening_answers": self.screening_answers,
            "needs": self.needs,
            "used_llm": self.used_llm,
            "notes": self.notes,
        }


# ---------------------------------------------------------------- prompt build

SYSTEM = """You are Sandi Ridwan's proposal writer. You write Upwork proposals that get
replies, in a fast, human, specific voice. You follow a fixed five-move structure and a
strict voice rulebook.

THE FIVE MOVES (in order):
1. Open on the client's failure mode, in their words. No greeting. Never open with
   credentials or "I read your posting".
2. Prove domain knowledge with ONE precise technical detail only an insider would say.
3. Land exactly ONE credibility line, mid-proposal. Never the opener. Never a list.
4. Kill the hiring risk: a free sample, mini-audit, or one concrete first step.
5. Close with a scoped, easy-to-answer question. Never "looking forward to hearing".

VOICE RULES (hard):
- Contractions everywhere ("I'll", never "I will").
- No exclamation points, no emoji, no em dashes, no colons in casual copy.
- "you"/"your" must outnumber "I"/"my".
- 3-5 deliberate rhythm breaks (fragments, sentences starting with And/But, one-word).
- 2-3 minor, intentional grammar relaxations max (comma splice, dropped Oxford comma).
- Numbers must be exact and real. Never invent a client, result, metric, or claim.
- If a required fact is missing, write [ADD: ...] and ask.

Use ONLY the credibility facts and portfolio links provided. Do not invent any."""


# The single proposal the panel will judge. It blends both parents:
# fahad's process-led depth (moves 1-5) with aahk's "answer the client's real
# question" framing, aimed at a winnable job.
ONE_SYSTEM = """You are Sandi Ridwan, writing ONE Upwork proposal that will win this job.

Write a single, complete proposal (180-280 words). It must be the best possible
version of both skills combined:
- the five-move structure (problem -> proof -> credibility -> risk-kill -> question)
- a clear read of what the client is actually afraid of, and a direct answer to it

Structure (prose, no headings, no labels):
1. Open on the client's failure mode, in their words. No greeting. Never credentials.
   The FIRST TWO LINES must contain the client's own key nouns (their industry, their
   target, their data type - for example "Australian real estate directories"). Upwork
   ranks proposals by match, and a busy client only sees the first two lines.
2. One precise technical detail only an insider would say.
3. Exactly one credibility line, mid-proposal. Never the opener. If a portfolio link
   is provided, include it as a real, clickable URL (never described, never dropped).
4. Kill the hiring risk: a free sample, mini-audit, or one concrete first step.
5. Close with a scoped, easy-to-answer question. Never "looking forward to hearing".

CRITICAL - placeholders never go in the proposal body:
- The proposal body must be READY TO SEND. It must contain no square-bracket text,
  no [ADD], no to-do notes, no commentary.
- If a fact you want is marked [ADD: ...] or is missing, DO NOT put it in the body.
  Write the sentence without it, or leave it out entirely.
- Collect every missing fact into a separate block AFTER the proposal, under the
  exact heading: NEED FROM YOU:  (one per line, each a short question). If nothing is
  missing, omit the block.

Also: address the deliverable the client actually asked for, not a neighbouring task.
If they asked for research and insights, the proof is about findings and patterns,
not about the mechanics of scraping.

Also: if the post lists explicit requirements, deliverables, formatting rules, or
handling instructions (for example "deliver CSV and XLSX", "leave blanks empty, no
N/A", "delete credentials after the job", "send a failure summary", "state your
start date"), address each of the MATERIAL ones in the body, briefly and plainly.
A requirement left silent reads as one you did not notice.

IMPORTANT - numbers: never put a number in the body that is not in the provided
facts, EXCEPT a price or timeframe. When the client explicitly asks for a price,
a rate, a volume or a timeline, you MUST give a concrete number or a narrow range
anchored to a stated assumption. Refusing to quote ("any number would be a guess")
loses the job. The only exception is when the client gave no signal at all about
scope or budget, in which case give a range and name the one variable that moves it.
Anything you genuinely cannot estimate goes in the NEED FROM YOU block, not as a
refusal in the body.

Pricing shape: "Roughly $X per 1,000 valid contacts, assuming emails are on the
listing; closer to $Y if enrichment is needed. Initial 25,000 batch in N days."

Use ONLY the credibility facts and portfolio links provided. Never invent a client,
result, metric, or technology."""


# Appended to the user turn when the job post has screening questions, so they are
# answered in the SAME call as the proposal (saves a request on rate-limited tiers
# and keeps the answers consistent with the proposal).
SCREENING_TASK = """

--- SCREENING QUESTIONS (answer EVERY one) ---
{questions}

After the proposal (and any NEED FROM YOU block), add one final block under the
exact heading: SCREENING ANSWERS:
For each question above, output two lines:
Q: <the question, verbatim>
A: <the answer, 2 to 5 sentences, plain text, ready to paste into its own box>
Answer every question, in order, even if it means saying what you would do. Never
write "see cover letter". Never use a square-bracket placeholder; if a real number
is required and unknown, answer honestly with what you do know and one concrete next
step."""


def _skill_body() -> str:
    """The writer SKILL.md with its YAML frontmatter stripped."""
    text = knowledge.writer_skill()
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]
    return text.strip()


def build_prompt(analysis: JobAnalysis, job_post: str,
                 variant: str = "both") -> str:
    pos = knowledge.positioning()
    port = knowledge.portfolio()
    voice = knowledge.voice()
    wins = knowledge.wins()

    a = analysis
    facts = (
        f"NICHE: {a.niche} ({a.niche_label})\n"
        f"FAILURE MODE: {a.failure_mode}\n"
        f"NAMED SYMPTOM: {a.named_symptom or '(none)'}\n"
        f"CLIENT TYPE: {a.client_type}\n"
        f"URGENCY: {a.urgency}\n"
        f"BUDGET SIGNAL: {a.budget_signal}\n"
        f"RED FLAGS: {', '.join(a.red_flags) or 'none'}\n"
        f"CREDIBILITY FACT TO USE: {a.credibility_fact}\n"
        f"PORTFOLIO LINK (at most one): {a.portfolio_link}\n"
        f"ONE TRUE OBSERVATION: {a.one_true_observation}\n"
    )

    task = (
        "Write BOTH a SHORT variant (90-130 words) and a PROCESS variant "
        "(220-320 words) for this job. Label them clearly as "
        "'=== SHORT VARIANT ===' and '=== PROCESS VARIANT ==='. "
        "After each, output nothing else."
        if variant == "both"
        else f"Write ONE {variant.upper()} variant only "
             f"({'90-130' if variant == 'short' else '220-320'} words)."
    )

    return f"""{_skill_body()}

--- IDENTITY: POSITIONING (facts you may claim) ---
{pos}

--- IDENTITY: PORTFOLIO (links you may use) ---
{port}

--- VOICE RULEBOOK ---
{voice}

--- ANNOTATED WINNING PATTERNS (steal the move, never the sentence) ---
{wins}

--- ANALYSIS OF THIS JOB ---
{facts}

--- JOB POST ---
{job_post[:5000]}

--- TASK ---
{task}
"""


# ---------------------------------------------------------------- live write

def write_one(analysis: JobAnalysis, job_post: str, *,
              include_screening: bool = True,
              screening_questions: list | None = None) -> ProposalBundle:
    """
    Write ONE complete proposal, then it is ready for the 7-agent panel.

    This is the combined flow: a single, best-effort proposal (both parents'
    strengths merged) rather than two parallel drafts. The panel judges this one.

    If screening_questions are given, they are answered in the SAME LLM call so
    the answers stay consistent with the proposal and the run costs one request
    fewer (important on rate-limited free tiers).
    """
    questions = list(screening_questions or [])
    user = _one_prompt(analysis, job_post, questions or None)
    res = llm.ask(ONE_SYSTEM, user, temperature=0.75, max_tokens=4000)

    bundle = ProposalBundle(prompt=user)

    if res.ok and res.text.strip():
        bundle.used_llm = True
        text, answers = _split_screening(res.text)
        body, needs = _split_needs(text)
        body = _strip_placeholders(body)
        body = _enforce_filter(body, getattr(analysis, "must_open_with", ""))
        v = _variant("proposal", body)
        v.lint = lint(v.body)
        bundle.variants = [v]
        bundle.needs = needs
        bundle.screening_answers = answers
    else:
        bundle.notes = (
            "No live LLM. Below is a ready-to-paste prompt for opencode plus "
            "an editable scaffold you can refine, then run the panel on it. "
            "Set an API key for full prose."
        )
        v = _skeleton(analysis, "process")
        v.lint = lint(v.body)
        bundle.variants = [v]

    # Screening: if the model answered them inline, done. Otherwise (and only
    # if we have questions) fall back to a separate call, then placeholders.
    if include_screening and questions and not bundle.screening_answers:
        bundle.screening_answers = _screening_answers(
            analysis, job_post, res.ok, questions)
    elif include_screening and not questions:
        # discover questions from the post text and answer them
        guessed = _guess_questions(job_post)
        if guessed:
            bundle.screening_answers = _screening_answers(
                analysis, job_post, res.ok, guessed)

    return bundle


_NEEDS_MARKERS = ("NEED FROM YOU:", "NEED FROM YOU :", "NEEDS FROM YOU:",
                  "QUESTIONS:", "TO CONFIRM:", "[ADD")


def _split_needs(text: str) -> tuple[str, list[str]]:
    """
    Separate the ready-to-send proposal from the 'NEED FROM YOU' block.

    The proposal body must never carry [ADD] notes; they belong in a separate
    list the user fills before sending.
    """
    upper = text.upper()
    cut = len(text)
    for marker in _NEEDS_MARKERS:
        idx = upper.find(marker)
        if idx != -1:
            cut = min(cut, idx)
    body = text[:cut].strip()
    tail = text[cut:].strip()

    needs: list[str] = []
    if tail:
        for raw in tail.splitlines():
            line = raw.strip().lstrip("-*0123456789. ").strip()
            if not line:
                continue
            if line.upper().startswith(("NEED FROM YOU", "NEEDS FROM YOU",
                                        "QUESTIONS:", "TO CONFIRM:")):
                rest = line.split(":", 1)[-1].strip()
                if rest:
                    needs.append(rest)
                continue
            needs.append(line)
    # de-dup, keep order
    seen = set()
    out = []
    for n in needs:
        if n.lower() not in seen:
            seen.add(n.lower())
            out.append(n)
    return body, out


def _enforce_filter(body: str, word: str) -> str:
    """
    Guarantee an application filter word starts the body.

    Some posts require the proposal to begin with a specific word; if the model
    missed it, prepend it here so the filter can never silently fail.
    """
    if not word:
        return body
    stripped = body.lstrip()
    first = re.split(r"[\s.,;:!?]", stripped, maxsplit=1)[0] if stripped else ""
    if first.lower() == word.lower():
        return body
    return f"{word}. {stripped}"


def _strip_placeholders(text: str) -> str:
    """
    Remove any stray square-bracket placeholder or need-note that slipped into
    the body. Blanket safety: the body must be paste-ready.
    """
    # drop whole lines that are only a bracket note
    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            continue
        lines.append(line)
    text = "\n".join(lines)
    # remove inline [ADD: ...] / [ ... ] fragments and tidy the gap
    text = re.sub(r"\[[^\]]*\]", "", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _split_screening(text: str) -> tuple[str, list]:
    """
    Pull the 'SCREENING ANSWERS:' block out of the model output.

    Returns (text_without_block, [{"question":..., "answer":...}, ...]).
    """
    upper = text.upper()
    idx = upper.find("SCREENING ANSWERS:")
    if idx == -1:
        return text, []
    head = text[:idx].rstrip()
    tail = text[idx + len("SCREENING ANSWERS:"):]

    pairs = []
    cur_q = None
    for raw in tail.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.upper().startswith("Q:"):
            cur_q = line[2:].strip()
        elif line.upper().startswith("A:") and cur_q is not None:
            pairs.append({"question": cur_q, "answer": line[2:].strip()})
            cur_q = None
        elif cur_q is not None:
            # continuation of the question
            cur_q += " " + line
    return head, pairs


def _one_prompt(analysis: JobAnalysis, job_post: str,
                screening_questions: list | None = None) -> str:
    pos = knowledge.positioning()
    port = knowledge.portfolio()
    voice = knowledge.voice()
    wins = knowledge.wins()
    a = analysis
    facts = (
        f"NICHE: {a.niche} ({a.niche_label})\n"
        f"FAILURE MODE: {a.failure_mode}\n"
        f"NAMED SYMPTOM: {a.named_symptom or '(none)'}\n"
        f"CLIENT TYPE: {a.client_type}\n"
        f"URGENCY: {a.urgency}\n"
        f"BUDGET SIGNAL: {a.budget_signal}\n"
        f"RED FLAGS: {', '.join(a.red_flags) or 'none'}\n"
        f"CREDIBILITY FACT TO USE: {a.credibility_fact}\n"
        f"PORTFOLIO LINK (at most one): {a.portfolio_link}\n"
        f"ONE TRUE OBSERVATION: {a.one_true_observation}\n"
    )
    screening_block = ""
    if screening_questions:
        numbered = "\n".join(f"{i}. {q}" for i, q in enumerate(screening_questions, 1))
        screening_block = SCREENING_TASK.format(questions=numbered)

    filter_block = ""
    if getattr(a, "must_open_with", ""):
        filter_block = (
            f"\nAPPLICATION FILTER (MANDATORY): the client requires the proposal to "
            f'BEGIN with the exact word "{a.must_open_with}". The very first token of '
            f"the body must be {a.must_open_with}, followed by a period or comma, then "
            f"the normal opening. Missing this loses the job before it is read.\n"
        )

    return f"""{_skill_body()}

--- IDENTITY: POSITIONING (facts you may claim) ---
{pos}

--- IDENTITY: PORTFOLIO (links you may use) ---
{port}

--- VOICE RULEBOOK ---
{voice}

--- ANNOTATED WINNING PATTERNS (steal the move, never the sentence) ---
{wins}

--- ANALYSIS OF THIS JOB ---
{facts}
{filter_block}
--- JOB POST ---
{job_post[:5000]}

--- TASK ---
Write the ONE proposal now. Prose only, 180-280 words, no headings, no labels.
{screening_block}
"""


def _strip_labels(text: str) -> str:
    """Remove any === LABEL === lines the model may still emit."""
    text = re.sub(r"^\s*={2,}.*?={2,}\s*$", "", text, flags=re.M)
    text = re.sub(r"^\s*#+\s.*$", "", text, flags=re.M)
    return text.strip()


def write(analysis: JobAnalysis, job_post: str, *,
          include_screening: bool = True) -> ProposalBundle:
    """Backwards-compatible alias: now writes ONE proposal (the combined flow)."""
    return write_one(analysis, job_post, include_screening=include_screening)


def write_both(analysis: JobAnalysis, job_post: str) -> ProposalBundle:
    """Optional: two labelled variants, for when you want to pick by hand."""
    prompt = build_prompt(analysis, job_post, "both")
    res = llm.ask(SYSTEM, prompt, temperature=0.75, max_tokens=1800)

    bundle = ProposalBundle(prompt=prompt)
    if res.ok:
        bundle.used_llm = True
        bundle.variants = _split_variants(res.text)
    else:
        bundle.notes = "No live LLM; deterministic skeletons shown."
        bundle.variants = [
            _skeleton(analysis, "short"),
            _skeleton(analysis, "process"),
        ]
    for v in bundle.variants:
        v.lint = lint(v.body)
    bundle.screening_answers = _screening_answers(analysis, job_post, res.ok)
    return bundle


def _split_variants(text: str) -> list:
    out = []
    # split on the requested labels, tolerate variation
    parts = re.split(r"={2,}\s*(SHORT VARIANT|PROCESS VARIANT)\s*={2,}",
                     text, flags=re.I)
    # parts: [pre, LABEL, body, LABEL, body, ...]
    i = 1
    while i + 1 < len(parts) + 1 and i < len(parts):
        label = parts[i].strip().lower()
        body = parts[i + 1].strip() if i + 1 < len(parts) else ""
        if body:
            out.append(_variant(label, body))
        i += 2

    if not out:  # model didn't use labels; keep whole thing as one
        cleaned = text.strip()
        out.append(_variant("proposal", cleaned))
    return out[:2]


def _variant(label: str, body: str) -> Variant:
    title = "Short variant" if "short" in label else (
        "Process variant" if "process" in label else label.title())
    return Variant(
        label=label,
        title=title,
        body=body,
        word_count=len(body.split()),
    )


# ---------------------------------------------------------------- skeletons

def _skeleton(a: JobAnalysis, variant: str) -> Variant:
    """Deterministic, rule-compliant scaffold when no LLM is available."""
    obs = a.one_true_observation
    link = a.portfolio_link
    tech = _TECH_DETAIL.get(a.niche, _TECH_DETAIL["A"])
    closing = _CLOSING.get(a.niche, _CLOSING["A"])
    freeze = _FREEZE.get(a.niche, _FREEZE["A"])

    symptom_clause = (
        f'You named "{a.named_symptom}", which usually points at '
        if a.named_symptom else "That usually points at "
    )

    if variant == "short":
        body = (
            f"{a.failure_mode} {freeze} {tech} "
            f"Send one example and you'll know tonight whether it's a "
            f"two-hour job or a two-day one, free. {obs}\n\n"
            f"{closing}"
        )
        return Variant("short", "Short variant", body, len(body.split()))

    body = (
        f"{a.failure_mode}\n\n"
        f"Before quoting anything, I check the shape of your problem, not the "
        f"symptom. {symptom_clause}one specific layer, and it is rarely the "
        f"layer people assume. Getting that wrong costs you days.\n\n"
        f"{tech} {a.credibility_fact}\n\n"
        f"{obs}\n\n"
        f"One reference repo that matches: {link}\n\n"
        f"To scope this properly, one thing helps. {closing}"
    )
    return Variant("process", "Process variant", body, len(body.split()))


# A niche-aware reframe of the failure mode (the anti-bot "wall vs door" line
# only fits anti-bot jobs).
_FREEZE = {
    "A": "That is usually not a wall, it is the wrong door.",
    "B": "That usually isn't the first run, it's month three.",
    "C": "That is almost always a join-key problem before it's a chart problem.",
    "D": "That usually isn't the feature, it's what happens under load.",
    "E": "That is almost always a coverage problem before it's a volume problem.",
}

# A niche-aware closing question (five move 5).
_CLOSING = {
    "A": "What's the target, and what has already been tried?",
    "B": "What breaks most often today, the fetch or the hand-off?",
    "C": "What are the two sources, and roughly how many records are we joining?",
    "D": "What's the endpoint, and how many calls a day do you expect?",
    "E": "What's the source, and roughly how many records are we talking about?",
}


# A precise, niche-specific insider detail for the deterministic scaffold.
_TECH_DETAIL = {
    "A": ("On a hotel search API I worked, one endpoint answered 202 while the "
          "same endpoint with a trailing slash answered 200. Same data, "
          "different door."),
    "B": ("The failure mode that kills these is a field rename on the source "
          "site that nobody notices. So errors get logged with a reason and "
          "surfaced, never silently swallowed."),
    "C": ("The trap is joining two datasets on a column that looks the same and "
          "isn't. IDs, codes and labels drift between sources, so the join key "
          "gets checked before any list or chart is built."),
    "D": ("Serving under load usually breaks on the boring parts: connection "
          "pooling, health checks, and what happens when the upstream "
          "hiccups."),
    "E": ("One collection path that looked complete only reached about 14% of "
          "the catalogue, and the listings rotated. Coverage gets measured "
          "before volume is promised."),
}


# ---------------------------------------------------------------- lint

def lint(body: str) -> list:
    """Deterministic voice-rule check. Returns a list of {rule, detail}."""
    issues = []
    low = body.lower()

    # the body must be paste-ready: no placeholders, no to-do notes
    if re.search(r"\[[^\]]*\]", body):
        issues.append({"rule": "placeholder_left_in",
                       "detail": "square-bracket note in the body"})

    for phrase in BANNED_PHRASES:
        if phrase in low:
            issues.append({"rule": "banned_phrase", "detail": phrase})

    if "!" in body:
        issues.append({"rule": "exclamation", "detail": "exclamation point found"})

    if re.search(r"[—–]", body):
        issues.append({"rule": "em_dash", "detail": "em/en dash found"})

    if re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", body):
        issues.append({"rule": "emoji", "detail": "emoji found"})

    you = len(re.findall(r"\byou(r|rs)?\b|\byour\b", body, re.I))
    me = len(re.findall(r"\bi\b|\bmy\b|\bme\b", body, re.I))
    if me > you:
        issues.append({"rule": "pronoun_ratio",
                       "detail": f"'I/my'={me} outnumbers 'you/your'={you}"})

    for tell in AI_TELLS:
        if tell in low:
            # 'I have' can be legitimate; only flag 'I will' / 'I am' hard
            if tell in ("i will ", "i am "):
                issues.append({"rule": "ai_tell", "detail": tell.strip()})

    for w in ("passionate", "dynamic", "synergy", "seamless", "robust",
              "cutting-edge", "state-of-the-art", "best-in-class"):
        if w in low:
            issues.append({"rule": "marketing_word", "detail": w})

    words = len(body.split())
    if words < 70:
        issues.append({"rule": "too_short", "detail": f"{words} words"})
    if words > 420:
        issues.append({"rule": "too_long", "detail": f"{words} words"})

    return issues


# ---------------------------------------------------------------- screening

_SCREEN_SYSTEM = """You answer Upwork screening questions for Sandi Ridwan. Each
answer is short, specific, honest, and in the same voice as the proposal (contractions,
no exclamation points, no emoji). If the job post has no screening questions, return
an empty list. Return ONLY JSON: a list of objects with keys "question" and "answer".
Never invent facts; if a fact is missing, write [ADD: ...]."""


def _screening_answers(a: JobAnalysis, job_post: str, live: bool,
                       questions: list | None = None) -> list:
    if questions is None:
        questions = _guess_questions(job_post)
    if not questions:
        return []

    if live:
        user = (f"Job post:\n{job_post[:3000]}\n\n"
                f"Questions to answer:\n" +
                "\n".join(f"- {q}" for q in questions) +
                f"\n\nContext: niche={a.niche}, portfolio={a.portfolio_link}")
        res = llm.ask(_SCREEN_SYSTEM, user, temperature=0.5, max_tokens=2000)
        if res.ok:
            from .analyzer import _extract_json
            data = _extract_json(res.text)
            if isinstance(data, list) and data:
                return [d for d in data if isinstance(d, dict) and d.get("answer")]

    # fallback: honest placeholder answers
    return [{"question": q,
             "answer": "[ADD: your specific answer, kept under 2 sentences]"}
            for q in questions]


def _guess_questions(text: str) -> list:
    qs = []
    for m in re.finditer(r"^[\-\*\d\.\)\s]*([^\n?]{6,140}\?)", text, re.M):
        q = m.group(1).strip()
        if q and q not in qs:
            qs.append(q)
    return qs[:8]
