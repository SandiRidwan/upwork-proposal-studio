# Upwork Proposal Studio

A personal tool that turns an Upwork job post into **one proposal in your real
voice**, then runs **seven independent agents** that select it — and tell you why it
would get skipped, before you spend a Connect.

Built by [Sandi Ridwan](https://github.com/SandiRidwan) by merging the two ideas into
one flow:

- [`fahadqaseem/upwork-proposal-writing-skill`](https://github.com/fahadqaseem/upwork-proposal-writing-skill)
  — the five-move structure, the voice rulebook, the annotated corpus. **(the writer)**
- [`aaksa/upwork-hiring-panel-skill`](https://github.com/aaksa/upwork-hiring-panel-skill)
  — the seven independent reviewer personas, the run-on-one-proposal selection, the
  rejection-story rewrite. **(the panel)**

The two are joined sequentially, exactly as intended: **the proposal is written
first, then it is put in front of the panel.** One proposal in, one verdict out.

They are kept **as close to the originals as possible**: both `SKILL.md` files and
all their `references/` live here in the same folder layout, and the engine reads
them on every run. The **only** differences are how they are invoked.

| | Source repos | This repo |
|---|---|---|
| **Invocation** | Claude `/command` in Claude Code | API + Streamlit UI (`app.py`, `engine/cli.py`) |
| **Sub-agents** | 7 parallel Claude sub-agents | 7 reviewers in one LLM call, or a deterministic panel with no key |
| **Wins file** | `~/.claude/upwork-hiring-panel/wins.md` | `knowledge/wins.md` |

Everything else (the five moves, the voice tiers, the seven personas, the rubric,
the hook lab, the proof-first shape) is the same, file for file.

Works with **or without** an API key.

---

## What it does

You paste a job post. The studio:

1. **Analyzes the brief** — detects the niche (anti-bot / automation / analysis /
   platform / lead-gen), the *failure mode* (every job post is a complaint in
   disguise), the client type, urgency, and red/green flags.
2. **Writes ONE complete proposal** — a single, best-effort draft that blends a
   process-led body with a direct read of the client's fear, following the fixed
   **five-move structure** and the voice rulebook.
3. **Lints its own output** — deterministic checks for banned phrases, exclamation
   points, emoji, em dashes, pronoun ratio, AI tells, and length.
4. **Puts that one proposal in front of 7 agents** — each reviewer reads it *alone*
   (nobody sees the others), gives an independent verdict, and the scores merge into
   Hook, Clarity, Relevance, Credibility, Value Proposition, and Interview Potential,
   plus a rejection story in the client's voice.
5. **Optionally rewrites** — same facts, and if the rewrite scores higher it becomes
   the shipped proposal, with the before/after verdict shown.

The flow, in one line:

```
job post -> analyze -> write ONE proposal -> 7 agents select it -> verdict (+ rewrite)
```

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
run in opencode or any chat, plus editable scaffolds. For full prose, put a key in
`.env` (copy `.env.example`):

```bash
GEMINI_API_KEY=...        # Google, free tier available
# or any one of:
OPENAI_API_KEY=sk-...
GROQ_API_KEY=gsk_...
OPENROUTER_API_KEY=sk-or-...
# or a local model
UPS_PROVIDER=ollama
UPS_MODEL=llama3.1
```

Keys are read automatically from `./.env`, then `../clipper-tools/.env`. A real
shell variable always wins over the file. If several keys are listed under
`GEMINI_API_KEYS` (comma/space separated), the studio rotates them on a rate limit.

Extra controls:

```bash
UPS_LLM_MODE=prompt     # never call an API, always return the prompt
UPS_LLM_MODE=provider   # require a provider
UPS_BASE_URL=...        # custom OpenAI-compatible endpoint
UPS_ENV_FILE=...        # point at a different .env path
```

### CLI

```bash
python -m engine.cli --job-file job.txt --out result.json
python -m engine.cli --job-file job.txt --rewrite --json
python -m engine.cli --save-win winning-proposal.txt   # add a hired win
type job.txt | python -m engine.cli
```

---

## Use in opencode (or Claude Code)

The two skills are **not** only for the UI. They use the standard
`skills/<name>/SKILL.md` layout, which **opencode reads natively** (same as Claude
Code). The repo ships an installer:

```bash
python -m engine.install --list              # show target folders
python -m engine.install                     # auto-detect opencode / claude
python -m engine.install --host opencode
python -m engine.install --project .         # into ./.opencode/skills (this repo only)
python -m engine.install --target <dir>
```

It copies `skills/upwork-proposal` and `skills/upwork-hiring-panel` into the host's
skills folder — `~/.config/opencode/skills` for opencode, `~/.claude/skills` for
Claude. Opencode finds skills in all of these places (documented):

- `.opencode/skills/<name>/SKILL.md` (project-local)
- `~/.config/opencode/skills/<name>/SKILL.md` (global)
- `.claude/skills/...` and `~/.claude/skills/...` (Claude-compatible)
- `.agents/skills/...` and `~/.agents/skills/...` (agent-compatible)

Start a new session afterwards. Confirm the host sees them:

```bash
opencode debug skill        # lists upwork-proposal and upwork-hiring-panel
```

**In opencode, both skills expose a slash command** (via
`metadata["opencode/slash"] = "true"`), so you can just type them:

```
/upwork-proposal        ← then paste the job post
/upwork-hiring-panel    ← paste your proposal + the job post
```

They also auto-invoke: paste a job post with no command and saying "write a
proposal" is enough, because the skill's `description` tells the agent when to load
it. Either way the agent reads `SKILL.md` + `references/` and follows the workflow
itself.

**Same skill, three ways to run it:**

| Where | How it runs |
|---|---|
| opencode / Claude Code | The agent host reads `SKILL.md` + `references/` (slash command or auto-invoke) |
| This repo's UI | `streamlit run app.py` → `engine/` prints the SKILL.md into the prompt |
| This repo's CLI | `python -m engine.cli --job-file job.txt` |

No conversion is needed. The only host-specific difference is the agent *sub-agent
mechanism* (opencode plays the seven reviewers itself; the engine sends one LLM
call), noted in `skills/upwork-hiring-panel/SKILL.md`.

---

## Make it yours

The engine is identity-agnostic. Everything specific to a person lives in the two
skill folders, kept in the **same layout the source skills use**, so the reference
files are edited in place exactly as a Claude Skill would be:

| File | What it holds |
|---|---|
| `skills/upwork-proposal/SKILL.md` | The writer skill: identity, workflow, voice, output |
| `skills/upwork-proposal/references/positioning.md` | Your verifiable facts, by brief type, + placement rules |
| `skills/upwork-proposal/references/portfolio.md` | Your links, by category, + when to use each |
| `skills/upwork-proposal/references/voice-rules.md` | Banned phrasing, human-texture tiers, before/after |
| `skills/upwork-proposal/references/winning-proposals.md` | Annotated patterns that won (steal the move, not the sentence) |
| `skills/upwork-proposal/references/client-research.md` | What to pull before writing |
| `skills/upwork-hiring-panel/SKILL.md` | The panel skill: mode, seven reviewers, score, rewrite |
| `skills/upwork-hiring-panel/references/personas.md` | The seven reviewer briefs, word for word |
| `skills/upwork-hiring-panel/references/rubric.md` | Scores, interview chance, rejection patterns, rewrite + screening rules |
| `skills/upwork-hiring-panel/references/winning-patterns.md` | Grounding in what clients actually see; overrides taste |
| `skills/upwork-hiring-panel/references/hook-lab.md` | The hook loop and the blind lineup |

There is **no structural difference** from the source skills: the same `SKILL.md`
plus `references/` layout, which opencode and Claude Code both read. The only
difference is *how they are invoked* — as a skill by an agent host, or through this
repo's engine (UI / CLI, with the seven reviewers played by one LLM call or by the
deterministic panel in `engine/panel.py` when no key is set).

**Hard rule the engine enforces:** it never invents a client, a result, or a metric.
If a required fact is missing, it writes `[ADD: ...]` and asks.

## Learn from your wins

The panel skill says the freelancer's own hired proposals are the strongest evidence.
Drop them in and the writer and panel both use them:

```bash
python -m engine.cli --job-file job.txt --save-win proposal.txt
```

That appends the job post and the winning proposal to `knowledge/wins.md`, dated,
ready to be reused as a pattern.

---

## Layout

```
upwork-proposal-studio/
├── app.py                    Streamlit UI (input + analysis + panel)
├── engine/
│   ├── __init__.py
│   ├── analyzer.py           job post -> niche, failure mode, flags
│   ├── writer.py             runs the writer SKILL.md, linter
│   ├── panel.py              7-agent selection, rejection story, rewrite
│   ├── pipeline.py           analyze -> write one -> 7 agents select
│   ├── knowledge.py          loads skills/ (the two SKILL.md + references)
│   ├── llm.py                provider abstraction (openai/groq/openrouter/ollama)
│   └── cli.py                command-line entry
├── skills/                   the two skills, same layout as the sources
│   ├── upwork-proposal/SKILL.md + references/
│   └── upwork-hiring-panel/SKILL.md + references/
├── knowledge/
│   └── wins.md               your own hired proposals (optional, added over time)
├── prompts/                  standalone prompt templates
├── examples/                 a sample job post + a weak proposal to judge
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
