"""
upwork-proposal-studio engine.

A two-engine tool:
  - writer  : analyze a job post, write two proposal variants (5-move structure)
  - panel   : 7 reviewers judge the proposal, score it, explain why it gets skipped

Works with or without an API key. Without a key it produces a ready-to-paste
prompt (for opencode or any chat) plus deterministic scaffolds.
"""

from .analyzer import analyze, JobAnalysis
from .writer import (write, write_one, write_both, lint, build_prompt,
                     ProposalBundle)
from .panel import review, PanelReport, before_after
from . import llm, knowledge
from .pipeline import run

__version__ = "1.1.0"
__all__ = [
    "analyze", "JobAnalysis",
    "write", "write_one", "write_both", "lint", "build_prompt",
    "ProposalBundle",
    "review", "PanelReport", "before_after",
    "run", "llm", "knowledge",
]
