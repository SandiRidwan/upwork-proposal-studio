"""
One-call pipeline: job post in, full result out.

    result = run(job_post, client_info="", bid="", screening="")

Everything the UI needs in one dict, so both the UI and the CLI (and opencode
itself) call the same code path.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .analyzer import analyze, JobAnalysis
from .writer import write, ProposalBundle
from .panel import review, PanelReport, before_after


@dataclass
class RunResult:
    analysis: JobAnalysis
    proposal: ProposalBundle
    panels: list = field(default_factory=list)  # one PanelReport per variant
    meta: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "analysis": self.analysis.to_dict(),
            "proposal": self.proposal.to_dict(),
            "panels": [p.to_dict() for p in self.panels],
            "meta": self.meta,
        }


def run(
    job_post: str,
    *,
    client_info: str = "",
    bid: str = "",
    screening: str = "",
    use_llm: bool = True,
    review_variants: bool = True,
    rewrite: bool = False,
) -> RunResult:
    """Run the full pipeline on a job post."""
    combined = job_post
    if client_info:
        combined += f"\n\n[CLIENT INFO]\n{client_info}"
    if screening:
        combined += f"\n\n[SCREENING QUESTIONS]\n{screening}"
    if bid:
        combined += f"\n\n[BID / RATE]\n{bid}"

    analysis = analyze(combined, use_llm=use_llm)
    proposal = write(analysis, combined, include_screening=True)

    panels = []
    if review_variants:
        for v in proposal.variants:
            p = review(v.body, combined, analysis,
                       use_llm=use_llm, with_rewrite=rewrite)
            if p.rewrite:
                p.before_after = before_after(v.body, p.rewrite, analysis)
            panels.append(p)

    from . import llm as _llm
    meta = {
        "llm": _llm.status(),
        "analyzer_used_llm": analysis.used_llm,
        "writer_used_llm": proposal.used_llm,
    }

    return RunResult(analysis=analysis, proposal=proposal, panels=panels,
                     meta=meta)
