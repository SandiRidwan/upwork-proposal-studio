"""
One-call pipeline: job post in, full result out.

The flow mirrors the two source skills joined into one:

    job post  ->  analyze  ->  write ONE proposal
                                    |
                                    v
                        7 agents select that ONE proposal
                        (each reads it alone, then scores merge)
                                    |
                                    v
                        verdict + rejection story + optional rewrite

    result = run(job_post, client_info="", bid="", screening="")

Everything the UI needs in one dict, so both the UI and the CLI (and opencode
itself) call the same code path.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .analyzer import analyze, JobAnalysis
from .writer import write_one, ProposalBundle
from .panel import review as _panel_review, PanelReport, before_after


@dataclass
class RunResult:
    analysis: JobAnalysis
    proposal: ProposalBundle
    panel: PanelReport | None = None       # the 7-agent selection on the proposal
    meta: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "analysis": self.analysis.to_dict(),
            "proposal": self.proposal.to_dict(),
            "panel": self.panel.to_dict() if self.panel else None,
            "meta": self.meta,
        }


def run(
    job_post: str,
    *,
    client_info: str = "",
    bid: str = "",
    screening: str = "",
    use_llm: bool = True,
    review: bool = True,          # run the 7-agent selection
    rewrite: bool = False,
) -> RunResult:
    """
    Full pipeline: analyze -> write ONE proposal -> 7 agents select it.

    Set review=False to skip the panel and just get the draft.
    """
    combined = job_post
    if client_info:
        combined += f"\n\n[CLIENT INFO]\n{client_info}"
    if screening:
        combined += f"\n\n[SCREENING QUESTIONS]\n{screening}"
    if bid:
        combined += f"\n\n[BID / RATE]\n{bid}"

    # split the screening block into individual questions so they can be answered
    # one by one (each has its own input box on Upwork)
    screening_qs = _parse_questions(screening) if screening else []

    analysis = analyze(combined, use_llm=use_llm)
    proposal = write_one(analysis, combined, include_screening=True,
                         screening_questions=screening_qs or None)

    panel = None
    if review:
        panel = _run_panel(proposal, combined, analysis,
                           use_llm=use_llm, rewrite=rewrite)

    from . import llm as _llm
    meta = {
        "llm": _llm.status(),
        "analyzer_used_llm": analysis.used_llm,
        "writer_used_llm": proposal.used_llm,
        "panel_used_llm": bool(panel and panel.used_llm),
        "panel_panel_error": (panel.llm_error if panel else ""),
        "panel_reviewers": 7 if panel else 0,
        "screening_questions": len(proposal.screening_answers),
    }

    return RunResult(analysis=analysis, proposal=proposal, panel=panel,
                     meta=meta)


def _parse_questions(text: str) -> list:
    """Split a pasted screening block into individual questions."""
    import re
    qs = []
    for line in (text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        # strip leading numbering / bullets
        line = re.sub(r"^[\-\*\d\.\)\s]+", "", line).strip()
        if line.endswith("?"):
            qs.append(line)
        elif len(line) > 12:  # a question without a question mark
            qs.append(line)
    # de-dup, keep order
    seen = set()
    out = []
    for q in qs:
        if q.lower() not in seen:
            seen.add(q.lower())
            out.append(q)
    return out


def _run_panel(proposal: ProposalBundle, job_post: str, analysis,
               *, use_llm: bool, rewrite: bool) -> PanelReport:
    """
    Run the panel on ONE proposal, and if it rewrites, loop until the rewrite
    no longer regresses (one pass), then keep the better version.

    This is the 'select the one proposal with 7 agents' step.
    """
    primary = proposal.primary
    panel = _panel_review(primary.body, job_post, analysis,
                          use_llm=use_llm, with_rewrite=rewrite)

    if panel.rewrite:
        panel.before_after = before_after(primary.body, panel.rewrite, analysis)
        # If the rewrite scores higher, promote it as the shipped proposal.
        after = panel.before_after.get("scores_after") or {}
        before = panel.before_after.get("scores_before") or {}
        if after and before and (sum(after.values()) > sum(before.values())):
            from .writer import Variant, lint
            improved = Variant(
                label="improved",
                title="Panel-improved",
                body=panel.rewrite,
                word_count=len(panel.rewrite.split()),
            )
            improved.lint = lint(improved.body)
            proposal.variants.insert(0, improved)

    return panel
