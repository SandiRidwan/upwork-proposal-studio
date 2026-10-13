# Upwork Proposal Studio

A personal tool that turns an Upwork job post into **two proposals in your real
voice**, then runs a **7-reviewer hiring panel** that tells you why it would get
skipped — before you spend a Connect.

Built by [Sandi Ridwan](https://github.com/SandiRidwan) by adapting the ideas in two
excellent open-source skills:

- [`fahadqaseem/upwork-proposal-writing-skill`](https://github.com/fahadqaseem/upwork-proposal-writing-skill)
  — the five-move structure, the voice rulebook, the annotated corpus.
- [`aaksa/upwork-hiring-panel-skill`](https://github.com/aaksa/upwork-hiring-panel-skill)
  — the seven independent reviewer personas and the rejection-story rewrite.

It is **not** a Claude Skill. It runs as a normal repo: a Python engine, a Streamlit
UI, and a set of Markdown knowledge files that define who you are and how you write.
Works with **or without** an API key.

---

## What it does

You paste a job post. The studio:

1. **Analyzes the brief** — detects the niche (anti-bot / automation / analysis /
   platform / lead-gen), the *failure mode* (every job post is a complaint in
   disguise), the client type, urgency, and red/green flags.
2. **Writes two proposals** — a short, punchy variant and a process-led variant,
   following the fixed **five-move structure** and the voice rulebook.
3. **Lints its own output** — deterministic checks for banned phrases, exclamation
   points, emoji, em dashes, pronoun ratio, AI tells, and length.
4. **Convenes the hiring panel** — seven reviewers read the proposal *alone* and
   score Hook, Clarity, Relevance, Credibility, Value Proposition, and Interview
   Potential, then write the rejection story in the client's voice.
5. **Optionally rewrites** — same facts, and shows the before/after verdict.

## The five moves

Every proposal follows the same five moves, in order:

1. Open on **their failure mode**, in their words. No greeting. Never credentials.
2. Prove domain knowledge with **one precise technical detail** only an insider knows.
3. Land **exactly one** credibility line, mid-proposal.
4. **Kill the hiring risk** — a free sample, mini-audit, or one concrete first step.
5. Close with a **scoped, easy-to-answer question**. Never a sign-off.

## The panel

| # | Reviewer | Reads | Judges | Verdict |
|---|----------|-------|--------|---------|
| 1 | The Scroller | Only the first two lines | Hook | OPEN / SKIP |
| 2 | The Hiring Client | Everything, next to the post | Relevance | INTERVIEW / MAYBE / NO |
| 3 | The Budget-Conscious Client | Scope, timeline, price | Value proposition | WORTH IT / NOT SURE / TOO EXPENSIVE |
| 4 | The Competing Freelancer | Your proposal as a rival | Differentiation | THEY WIN / TOSS-UP / I WIN |
| 5 | The Skeptic | Proof vs claims | Credibility | TRUST / UNSURE / DISTRUST |
| 6 | The Technical Lead | Approach and understanding | Clarity | KNOWS IT / VAGUE / WRONG |
| 7 | The Upwork Veteran | Template tells, length, rules | Interview potential | SHORTLIST / ARCHIVE / DECLINE |

Each reviewer sees nobody else's notes. Scores merge into an interview chance
(LOW / MEDIUM / HIGH) and a single rejection story.

---

## Quick start

```bash
git clone https://github.com/SandiRidwan/upwork-proposal-studio.git
cd upwork-proposal-studio
pip install -r requirements.txt

streamlit run app.py
```

Then paste a job post, click **Analyze & write**.

### Optional: live LLM prose

Without a key, the studio still works — it produces a ready-to-paste prompt you can
run in opencode or any chat, plus editable scaffolds. For full prose, set one key:

```bash
# any one of these
set OPENAI_API_KEY=sk-...
set GROQ_API_KEY=gsk_...
set OPENROUTER_API_KEY=sk-or-...
# or a local model
set UPS_PROVIDER=ollama
set UPS_MODEL=llama3.1
```

Extra controls:

```bash
set UPS_LLM_MODE=prompt     # never call an API, always return the prompt
set UPS_LLM_MODE=provider   # require a provider
set UPS_BASE_URL=...        # custom OpenAI-compatible endpoint
```

### CLI (works inside opencode)

```bash
python -m engine.cli --job-file job.txt --out result.json
python -m engine.cli --job-file job.txt --rewrite --json
type job.txt | python -m engine.cli
```

---

## Make it yours

The engine is identity-agnostic. Everything specific to a person lives in
`knowledge/`. Swap these and the tool is yours:

| File | What it holds |
|---|---|
| `knowledge/positioning.md` | Your verifiable facts, by brief type, + placement rules |
| `knowledge/portfolio.md` | Your links, by category, + when to use each |
| `knowledge/voice-rules.md` | Banned phrases, human-texture rules, before/after |
| `knowledge/winning-proposals.md` | Annotated patterns that won (steal the move, not the sentence) |
| `knowledge/client-research.md` | What to pull before writing |

**Hard rule the engine enforces:** it never invents a client, a result, or a metric.
If a required fact is missing, it writes `[ADD: ...]` and asks.

---

## Layout

```
upwork-proposal-studio/
├── app.py                    Streamlit UI (input + analysis + panel)
├── engine/
│   ├── __init__.py
│   ├── analyzer.py           job post -> niche, failure mode, flags
│   ├── writer.py             5-move structure, two variants, linter
│   ├── panel.py              7-persona review + rejection story + rewrite
│   ├── pipeline.py           one-call orchestration
│   ├── knowledge.py          loads knowledge/
│   ├── llm.py                provider abstraction (openai/groq/openrouter/ollama)
│   └── cli.py                command-line entry
├── knowledge/                the identity + rule layer (edit these)
├── prompts/                  standalone prompt templates
├── examples/                 a sample job post + expected shape
├── tests/                    unit tests (no key needed)
├── requirements.txt
└── README.md
```

## Run the tests

```bash
python -m unittest discover -s tests
```

No API key, no network. Tests cover the analyzer, linter, panel verdicts, and a
full pipeline run.

## Notes

- It never invents clients, results, numbers, or portfolio items.
- It flags any attempt to move contact or payment off Upwork.
- It is a structured second opinion. It does not guarantee an interview or a hire.
- Not affiliated with Upwork.

## License

MIT — see [LICENSE](LICENSE). The workflow and panel structure are adapted from the
two MIT-licensed skills credited above; the identity layer is Sandi Ridwan's.
