"""
The hiring panel.

Seven reviewers judge a proposal, each alone, then scores are merged and a
rejection story is written in the client's voice. Adapted from the
`upwork-hiring-panel-skill` structure (itself adapted from Alex Chen's
hiring-panel-skill, MIT).

Personas:
  1. The Scroller            - only first two lines        -> Hook
  2. The Hiring Client       - everything vs the post      -> Relevance
  3. The Budget Client       - scope/timeline/price        -> Value proposition
  4. The Competing Freelancer- as a rival on the same job  -> Differentiation
  5. The Skeptic             - proof vs claims             -> Credibility
  6. The Technical Lead      - approach and understanding  -> Clarity
  7. The Upwork Veteran      - template tells, rules       -> Interview potential

Works with or without an LLM: heuristic scoring always runs; LLM adds the
qualitative rejection story and rewrite when available.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field, asdict

from . import llm
from .analyzer import JobAnalysis
from .writer import lint

PERSONAS = {
    "scroller": {
        "name": "The Scroller",
        "reads": "Only the first two lines, like a busy client scanning the list.",
        "judges": "Hook",
        "verdicts": ["OPEN", "SKIP"],
    },
    "hiring_client": {
        "name": "The Hiring Client",
        "reads": "Everything, side by side with the job post.",
        "judges": "Relevance, interview potential",
        "verdicts": ["INTERVIEW", "MAYBE", "NO"],
    },
    "budget_client": {
        "name": "The Budget-Conscious Client",
        "reads": "Scope, timeline, price.",
        "judges": "Value proposition",
        "verdicts": ["WORTH IT", "NOT SURE", "TOO EXPENSIVE"],
    },
    "competitor": {
        "name": "The Competing Freelancer",
        "reads": "Your proposal as a rival on the same job.",
        "judges": "Differentiation",
        "verdicts": ["THEY WIN", "TOSS-UP", "I WIN"],
    },
    "skeptic": {
        "name": "The Skeptic",
        "reads": "Proof versus claims.",
        "judges": "Credibility",
        "verdicts": ["TRUST", "UNSURE", "DISTRUST"],
    },
    "tech_lead": {
        "name": "The Technical Lead",
        "reads": "Approach and understanding.",
        "judges": "Clarity",
        "verdicts": ["KNOWS IT", "VAGUE", "WRONG"],
    },
    "veteran": {
        "name": "The Upwork Veteran",
        "reads": "Template tells, length, screening answers, platform rules.",
        "judges": "Interview potential",
        "verdicts": ["SHORTLIST", "ARCHIVE", "DECLINE"],
    },
}

SCORE_DIMENSIONS = ["Hook", "Clarity", "Relevance", "Credibility",
                    "Value Proposition", "Interview Potential"]


@dataclass
class Review:
    key: str
    name: str
    verdict: str
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class PanelReport:
    reviews: list = field(default_factory=list)
    scores: dict = field(default_factory=dict)
    interview_chance: str = "LOW"
    problems: list = field(default_factory=list)
    rejection_story: str = ""
    rewrite: str = ""
    before_after: dict = field(default_factory=dict)
    used_llm: bool = False

    def to_dict(self) -> dict:
        return {
            "reviews": [r.to_dict() for r in self.reviews],
            "scores": self.scores,
            "interview_chance": self.interview_chance,
            "problems": self.problems,
            "rejection_story": self.rejection_story,
            "rewrite": self.rewrite,
            "before_after": self.before_after,
            "used_llm": self.used_llm,
        }


# ---------------------------------------------------------------- heuristic panel

def review(proposal: str, job_post: str, analysis: JobAnalysis | None = None,
           *, use_llm: bool = True, with_rewrite: bool = False) -> PanelReport:
    proposal = (proposal or "").strip()
    report = PanelReport()
    report.reviews = _heuristic_reviews(proposal, job_post)
    report.scores, report.interview_chance = _heuristic_scores(proposal, report.reviews)
    report.problems = _merge_problems(report.reviews, proposal)

    if use_llm and llm.is_live():
        _llm_enrich(report, proposal, job_post, analysis, with_rewrite)

    if not report.rejection_story:
        report.rejection_story = _heuristic_rejection(report, proposal)

    return report


def _first_two_lines(text: str) -> str:
    lines = [l for l in text.splitlines() if l.strip()]
    return " ".join(lines[:2])[:300]


def _heuristic_reviews(proposal: str, job_post: str) -> list:
    out = []
    low = proposal.lower()
    opening = _first_two_lines(proposal).lower()

    # 1 Scroller
    hook_bad = any(b in opening for b in [
        "i am a", "i'm a", "i have", "i've been", "my name", "hello",
        "hi,", "dear", "i read", "i came across", "as a professional"])
    strong_hook = bool(re.search(
        r"\b(block|wall|door|trap|wrong|fail|stuck|break|risk|problem)\b",
        opening))
    scroller = "SKIP" if (hook_bad or not strong_hook or len(opening) < 25) else "OPEN"
    out.append(Review(
        "scroller", "The Scroller", scroller,
        "Opens on the client's problem." if scroller == "OPEN"
        else "Opens on the writer, or the first two lines don't name a problem."))

    # 2 Hiring client
    mentions_their = any(w in low for w in
                         ["you", "your", "you're", "you've"])
    has_question = proposal.strip().endswith("?")
    if mentions_their and has_question:
        hc = "INTERVIEW"
    elif mentions_their:
        hc = "MAYBE"
    else:
        hc = "NO"
    out.append(Review(
        "hiring_client", "The Hiring Client", hc,
        "Speaks to the client and asks a closing question."
        if hc == "INTERVIEW" else
        "Talks about the writer more than the client's problem."))

    # 3 Budget client
    value_terms = ["free", "no cost", "sample", "audit", "first pass",
                   "before you", "tonight", "one url", "one page",
                   "no commitment"]
    has_value = any(t in low for t in value_terms)
    scope_terms = ["hours", "days", "week", "timeline", "scope", "first step",
                   "step one", "phase"]
    has_scope = any(t in low for t in scope_terms)
    bc = "WORTH IT" if (has_value and has_scope) else (
        "NOT SURE" if has_value else "NOT SURE")
    out.append(Review(
        "budget_client", "The Budget-Conscious Client", bc,
        "Offers a concrete free first step with an implied scope."
        if bc == "WORTH IT" else
        "No clear first step or scope for the money."))

    # 4 Competitor
    specific = bool(re.search(r"\b(200|202|403|405|/_next|viewstate|tls|ja3|"
                              r"signature|slug|trailing slash|endpoint|"
                              r"price column|coverage|sitemap|api)\b", low))
    cred = bool(re.search(r"\d{2,}", proposal))  # a real number somewhere
    comp = "I WIN" if (specific and cred) else (
        "TOSS-UP" if specific else "THEY WIN")
    out.append(Review(
        "competitor", "The Competing Freelancer", comp,
        "More specific than a typical competitor." if comp != "THEY WIN"
        else "A generic competitor could send this same text."))

    # 5 Skeptic
    invented = bool(re.search(r"\b(i (guarantee|will 100%|always|never fail))\b", low))
    sk = "DISTRUST" if invented else ("TRUST" if cred else "UNSURE")
    out.append(Review(
        "skeptic", "The Skeptic", sk,
        "Claims are backed by specifics, not promises." if sk == "TRUST"
        else "Claims are not backed by anything checkable."))

    # 6 Technical lead
    tech = "KNOWS IT" if specific else ("VAGUE" if len(proposal.split()) > 60
                                        else "VAGUE")
    out.append(Review(
        "tech_lead", "The Technical Lead", tech,
        "Speaks the domain's language with a precise detail." if tech == "KNOWS IT"
        else "No concrete technical signal that this person knows the work."))

    # 7 Veteran
    li = lint(proposal)
    hard = [i for i in li if i["rule"] in
            ("banned_phrase", "exclamation", "emoji", "ai_tell", "pronoun_ratio")]
    va = "SHORTLIST" if not hard else "ARCHIVE"
    out.append(Review(
        "veteran", "The Upwork Veteran", va,
        "Reads like a human wrote it in a hurry, not a template."
        if va == "SHORTLIST" else
        f"{len(hard)} template tell(s) found."))

    return out


def _heuristic_scores(proposal: str, reviews: list) -> tuple:
    vmap = {r.key: r.verdict for r in reviews}
    words = len(proposal.split())

    def band(good, mid, bad, val):
        return good if val == good else (mid if val == mid else bad)

    hook = 9 if vmap.get("scroller") == "OPEN" else 3
    clarity = 8 if vmap.get("tech_lead") == "KNOWS IT" else 4
    relevance = band("INTERVIEW", "MAYBE", "NO", vmap.get("hiring_client"))
    relevance = {"INTERVIEW": 9, "MAYBE": 6, "NO": 3}[relevance]
    credibility = {"TRUST": 8, "UNSURE": 5, "DISTRUST": 3}[vmap.get("skeptic")]
    value = 8 if vmap.get("budget_client") == "WORTH IT" else 5
    interview = {"I WIN": 9, "TOSS-UP": 6, "THEY WIN": 3}[vmap.get("competitor")]

    scores = {
        "Hook": hook,
        "Clarity": clarity,
        "Relevance": relevance,
        "Credibility": credibility,
        "Value Proposition": value,
        "Interview Potential": interview,
    }
    avg = sum(scores.values()) / len(scores)
    chance = "HIGH" if avg >= 7.5 else ("MEDIUM" if avg >= 5.5 else "LOW")
    return scores, chance


def _merge_problems(reviews: list, proposal: str) -> list:
    problems = []
    for r in reviews:
        if r.key == "scroller" and r.verdict == "SKIP":
            problems.append(
                "The first two lines don't name the client's problem, so a busy "
                "client never reaches the rest.")
        if r.key == "hiring_client" and r.verdict == "NO":
            problems.append(
                "The proposal is about the writer, not the client, and doesn't "
                "end on a question.")
        if r.key == "competitor" and r.verdict == "THEY WIN":
            problems.append(
                "Nothing here a generic competitor couldn't also write.")
        if r.key == "skeptic" and r.verdict == "UNSURE":
            problems.append(
                "Claims are unbacked. No number, no repo, no proof.")
        if r.key == "tech_lead" and r.verdict == "VAGUE":
            problems.append(
                "No precise technical detail, so it reads as generic.")
        if r.key == "veteran" and r.verdict == "ARCHIVE":
            problems.append(
                "Template tells are present (per the voice rules).")
    return problems


def _heuristic_rejection(report: PanelReport, proposal: str) -> str:
    if report.interview_chance == "HIGH":
        return ("I'd probably reply to this one. The opening names my problem, "
                "there's a specific detail I didn't know, and the ask at the end "
                "is easy to answer.")
    first = _first_two_lines(proposal) or "(empty)"
    # Name the strongest actual weakness, so the story matches the verdicts.
    weak = []
    for r in report.reviews:
        if r.key == "scroller" and r.verdict == "SKIP":
            weak.append("the first two lines don't name my problem")
        if r.key == "competitor" and r.verdict == "THEY WIN":
            weak.append("it reads like the other forty")
        if r.key == "skeptic" and r.verdict in ("UNSURE", "DISTRUST"):
            weak.append("nothing in it I can actually check")
        if r.key == "tech_lead" and r.verdict == "VAGUE":
            weak.append("no detail that proves they've done this before")
        if r.key == "hiring_client" and r.verdict == "NO":
            weak.append("it's about them, not me")

    if report.interview_chance == "MEDIUM":
        lead = "It's close. I got past the first line, which already puts it ahead."
    else:
        lead = f"I opened it and read: \"{first}\". That's where most of them lose me."

    if weak:
        tail = ("But " + " and ".join(weak[:3]) +
                ", so I couldn't tell it apart from the rest. I saved my Connects "
                "and moved on.")
    else:
        tail = "Still, there was nothing that made me stop and reply."
    return f"{lead} {tail}"


# ---------------------------------------------------------------- LLM enrich

_PANEL_SYSTEM = """You are running a 7-reviewer hiring panel on an Upwork proposal.
Each reviewer reads the proposal alone and gives a verdict plus one sentence of
reason. Then you write the rejection story in the CLIENT's voice (first person, plain,
under 90 words) and a merge of problems, worst first.

Return ONLY JSON:
{
  "reviews": [{"key": "...", "verdict": "...", "reason": "..."} x7],
  "rejection_story": "...",
  "problems": ["...", "..."]
}
Use these exact keys and allowed verdicts:
  scroller: OPEN|SKIP
  hiring_client: INTERVIEW|MAYBE|NO
  budget_client: WORTH IT|NOT SURE|TOO EXPENSIVE
  competitor: THEY WIN|TOSS-UP|I WIN
  skeptic: TRUST|UNSURE|DISTRUST
  tech_lead: KNOWS IT|VAGUE|WRONG
  veteran: SHORTLIST|ARCHIVE|DECLINE

Never invent facts about the client. Be blunt. Reviewers do not see each other."""


def _llm_enrich(report: PanelReport, proposal: str, job_post: str,
                analysis, with_rewrite: bool) -> None:
    user = (
        f"JOB POST:\n{job_post[:3000]}\n\n"
        f"PROPOSAL:\n{proposal[:4000]}\n\n"
        f"Deterministic lint findings: "
        f"{[p for p in report.problems]}"
    )
    res = llm.ask(_PANEL_SYSTEM, user, temperature=0.4, max_tokens=1200)
    if not res.ok:
        return
    from .analyzer import _extract_json
    data = _extract_json(res.text)
    if not isinstance(data, dict):
        return
    report.used_llm = True

    # merge LLM reviews (keep hueristic scores, replace reasons)
    llm_reviews = {r.get("key"): r for r in data.get("reviews", [])
                   if isinstance(r, dict)}
    for r in report.reviews:
        lr = llm_reviews.get(r.key)
        if lr:
            allowed = PERSONAS[r.key]["verdicts"]
            v = lr.get("verdict")
            if v in allowed:
                r.verdict = v
            if lr.get("reason"):
                r.reason = str(lr["reason"])[:300]

    # refresh scores from possibly-updated verdicts
    report.scores, report.interview_chance = _heuristic_scores(
        proposal, report.reviews)

    if data.get("rejection_story"):
        report.rejection_story = str(data["rejection_story"])[:800]
    if data.get("problems"):
        report.problems = [str(p)[:300] for p in data["problems"]][:10]

    if with_rewrite:
        report.rewrite = _rewrite(proposal, job_post, analysis)


_REWRITE_SYSTEM = """Rewrite the proposal using the same facts (never invent anything).
Apply the five moves and the voice rules. Keep it 120-220 words. Return only the
proposal text, no headings or commentary."""


def _rewrite(proposal: str, job_post: str, analysis) -> str:
    user = (f"JOB POST:\n{job_post[:2500]}\n\n"
            f"ORIGINAL:\n{proposal[:3000]}\n\n"
            f"Use this credibility fact if it fits: "
            f"{getattr(analysis, 'credibility_fact', '')}\n"
            f"Use at most this link: "
            f"{getattr(analysis, 'portfolio_link', '')}")
    res = llm.ask(_REWRITE_SYSTEM, user, temperature=0.6, max_tokens=900)
    return res.text.strip() if res.ok else ""


def before_after(original: str, rewritten: str, analysis) -> dict:
    """Re-run the Scroller and Hiring Client on the rewrite."""
    if not rewritten:
        return {}
    before = _heuristic_reviews(original, "")
    after = _heuristic_reviews(rewritten, "")
    b = {r.key: r.verdict for r in before}
    a = {r.key: r.verdict for r in after}
    return {
        "scroller": {"before": b.get("scroller"), "after": a.get("scroller")},
        "hiring_client": {"before": b.get("hiring_client"),
                          "after": a.get("hiring_client")},
        "scores_before": _heuristic_scores(original, before)[0],
        "scores_after": _heuristic_scores(rewritten, after)[0],
    }
