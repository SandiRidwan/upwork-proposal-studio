# Portfolio gap — AI Automation Developer (AI agents, orchestration, RAG)

When a client asks for **production AI agents, agent orchestration, tool calling,
RAG, multi-provider LLMs, human-in-the-loop**, and the bid uses pipeline/enrichment
repos, the panel scores it MEDIUM and the technical buyer does not click. This is a
**portfolio problem, not a wording problem**. Fix the portfolio and the same engine
produces a convincing bid.

## The gap, verified against the actual repos

| What the job tests | What the repos currently show | Verdict |
|---|---|---|
| Agent orchestration (multi-step, tool routing) | nothing — `data-aggregation-agent` is a pipeline, not an LLM agent | **missing** |
| Structured tool calling (typed schema, validation) | single-shot LLM enrichment calls | **missing** |
| Multi-provider (OpenAI + Claude + Gemini behind one interface) | Groq only | **missing** |
| RAG / vector store | nothing | **missing** |
| LangChain / LangGraph / MCP | nothing | **missing** |
| Human-in-the-loop approval for sensitive actions | nothing | **missing** |
| Retries, backoff, error taxonomy, monitoring for LLM paths | pipeline-level alerting exists, not LLM-level | partial |
| Prompt engineering with evaluation | ad-hoc prompts | partial |
| Python backend (FastAPI) | `public-data-api` exists (good) | **good** |
| Data/pipeline skills | strong (many repos) | **good** |
| n8n / Make / Zapier | `Autopilot-Market-Intel`, `calendly-monday-automation` | real, but thin |

**Strengths to keep and lead with:** Python backend + pipeline reliability + data
engineering + LLM enrichment. The missing piece is a *real agent system*.

---

## Project 1 — `agent-orchestrator-lab` (the anchor; highest priority)

**One-line:** A production-shaped AI agent system with a planner, typed tools, a
router across OpenAI/Claude/Gemini, a human-in-the-loop approval gate, retries with
backoff, and an audit log — plus an evaluation harness that scores the agent.

**Why it wins:** the client explicitly says "reliable solutions rather than only
building simple chatbot prototypes". This repo is the direct answer, and it names
the keywords they wrote (AI Agent Development, tool calling, agent orchestration,
multi-provider, human-in-the-loop, monitoring).

**Contents (each is a real, testable module):**

| Module | What it proves |
|---|---|
| `agent/planner.py` | a task is decomposed into steps, not one prompt |
| `agent/tools.py` | **typed tool schema** (Pydantic) + validation; a bad tool call is rejected, not executed |
| `agent/router.py` | one interface over **OpenAI, Claude and Gemini**; falls back on provider error; routes cheap vs strong model per step |
| `agent/approval.py` | **human-in-the-loop** gate: actions flagged sensitive pause for approval, with an audit record |
| `agent/reliability.py` | retries with backoff, per-step timeout, error taxonomy (retryable vs terminal), no silent failure |
| `agent/memory.py` | short-term conversation state + a persisted run log |
| `eval/` | a fixed task set with expected outcomes; score = pass rate, tool-call correctness, cost, latency |
| `api/` | FastAPI endpoint to run a task + stream the trace |
| `README` | an architecture diagram, a real run trace, and the eval scoreboard |

**The README must show a real run trace** — planner output, tool calls with args,
the approval pause, the retry on a provider error — because that trace is what
proves it is a system, not a wrapper. Include a failure case (malformed tool
output → caught, retried, logged).

**Skills it proves:** agent orchestration, structured tool calling, multi-provider
routing, HITL approval, reliability engineering, FastAPI, evaluation.

## Project 2 — `rag-knowledge-service`

**One-line:** A retrieval-augmented service over a **real public document set**
(not toy data): ingest → chunk → embed → vector store → answer with citations and
a "no answer found" path.

**Why it wins:** RAG is named in the job. Most candidates wire a tutorial; this one
shows the parts that matter — citation, refusal when the answer is not in the docs,
and an eval for retrieval quality.

**Contents:** a real corpus (e.g. a public docs set or a set of PDFs you already
have), chunking with overlap, embeddings, a vector store (pgvector on the
PostgreSQL you already run, or Chroma), a **grounded answer with source citations**,
an explicit "insufficient context" response, and a retrieval eval (hit rate@k on a
hand-labelled question set). Show it refusing to answer a question the corpus does
not cover.

## Project 3 — `n8n-ai-workflow-pack`

**One-line:** Three real n8n workflows that call an LLM with structured output,
handle errors, and pause for approval — exported as JSON with a screenshot each.

**Why it wins:** the job names n8n specifically, and your existing automation is
Make.com. This closes the named tool gap with something runnable.

**Contents:** (1) inbound email → classify with an LLM → route to the right channel;
(2) form submission → enrich → LLM score → create CRM record with a duplicate guard;
(3) a sensitive action (e.g. send/refund) that pauses for manual approval. Each
exported as `.json`, each with an error branch and a retry, each screenshotted.

## Project 4 — reframe an existing repo (no new code)

Take `lead-intelligence-pipeline` and add a top section: **"The reliability layer."**
The retry logic, the error taxonomy, the duplicate guard, the logging. Same repo,
now it answers "is this production or a demo?" instead of only "does it enrich?".

---

## Cheap profile fixes (do today)

1. **Headline**: add "AI Agents · LLM Orchestration · RAG · Python". Right now the
   first screen reads scraping/automation, which is the wrong match for this brief.
2. **Pinned repos**: pin `agent-orchestrator-lab` and `rag-knowledge-service` once
   built, so the AI story is the first thing a client sees.
3. **Every AI repo README gets an "architecture" section and a real trace**, because
   the client is buying a system, not a library call.
4. **Do not claim LangGraph/MCP/LangChain unless used.** The panel flags it and a
   technical buyer verifies in one click.

---

## Priority order

1. `agent-orchestrator-lab` — directly answers "not a chatbot prototype"; biggest return.
2. `rag-knowledge-service` — closes the RAG gap with proof of grounding + refusal.
3. `n8n-ai-workflow-pack` — closes the named-platform gap.
4. Reframe `lead-intelligence-pipeline` README — nearly free.

After 1 and 2, add them to `skills/upwork-proposal/references/portfolio.md` under a
new **"AI agents / LLM"** row and add a positioning line. Then the engine cites real
proof on AI-automation briefs and the panel stops scoring Credibility at 6.

---

## Honest note

For AI-automation roles you compete with people who ship agents professionally. Your
edge is the same as in the SQL work: **the rare combination** — you can get the data
(scraping/pipelines), store and query it (SQL/warehouse), *and* put an LLM agent on
top. Most "AI automation" freelancers cannot get the data at all. Build the two repos
above, then bid on briefs that need the whole chain, not on chatbot-only jobs.
