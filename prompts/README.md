# Standalone prompts

If you'd rather not run the Python engine, these prompt templates work on their own
in opencode or any chat. They are the same instructions the engine uses.

## 01 — Analyze a job post

```
Role: You are helping me understand an Upwork job post before I write a proposal.

Read the post below and return ONLY a small JSON object:
{
  "niche": "A|B|C|D|E",   // A=anti-bot scraping, B=automation, C=analysis, D=platform/API, E=lead-gen
  "failure_mode": "one sentence: what went wrong for this client before",
  "named_symptom": "the exact symptom words they used",
  "client_type": "first_timer|serial|enterprise|startup|agency|unspecified",
  "urgency": "high|medium|low",
  "budget_signal": "what you can infer",
  "red_flags": ["..."],
  "green_flags": ["..."],
  "one_true_observation": "a specific, true observation an expert would make; if too vague, start with [ADD:",
  "credibility_fact": "which fact to use (I will paste my positioning file)",
  "portfolio_link": "at most one"
}
Every job post is a complaint in disguise. Do not invent client names or numbers.

JOB POST:
<paste here>
```

## 02 — Write the proposal

```
Write an Upwork proposal using EXACTLY this five-move structure, in order:
1. Open on the client's FAILURE MODE, in their words. No greeting. Never credentials.
2. Prove domain knowledge with ONE precise technical detail only an insider would say.
3. Land EXACTLY ONE credibility line, mid-proposal. Never the opener. Never a list.
4. Kill the hiring risk: a free sample, mini-audit, or one concrete first step.
5. Close with a scoped, easy-to-answer question. Never a sign-off.

VOICE RULES (hard):
- Contractions everywhere ("I'll", never "I will").
- No exclamation points, no emoji, no em dashes, no colons in casual copy.
- "you"/"your" must outnumber "I"/"my".
- 3-5 deliberate rhythm breaks (fragments, sentences starting with And/But, one-word).
- 2-3 minor, intentional grammar relaxations max.
- Numbers must be exact and real. Never invent a client, result, or metric.
- If a fact is needed and missing, write [ADD: ...] and ask.

Write BOTH a SHORT variant (90-130 words) and a PROCESS variant (220-320 words).
Label them "=== SHORT VARIANT ===" and "=== PROCESS VARIANT ===".

My positioning (facts I may claim):
<paste skills/upwork-proposal/references/positioning.md>

My portfolio (links I may use, at most one):
<paste skills/upwork-proposal/references/portfolio.md>

Job analysis:
<paste output of prompt 01>

JOB POST:
<paste here>
```

## 03 — Run the hiring panel

```
You are running a 7-reviewer hiring panel on an Upwork proposal. Each reviewer reads
the proposal ALONE and gives a verdict plus one sentence of reason. Reviewers do not
see each other.

  scroller:       OPEN | SKIP                       (only the first two lines)
  hiring_client:  INTERVIEW | MAYBE | NO            (everything vs the post)
  budget_client:  WORTH IT | NOT SURE | TOO EXPENSIVE
  competitor:     THEY WIN | TOSS-UP | I WIN
  skeptic:        TRUST | UNSURE | DISTRUST
  tech_lead:      KNOWS IT | VAGUE | WRONG
  veteran:        SHORTLIST | ARCHIVE | DECLINE

Then score Hook, Clarity, Relevance, Credibility, Value Proposition, Interview
Potential (1-10) and give an interview chance LOW|MEDIUM|HIGH. Merge the problems
worst-first and write the REJECTION STORY in the client's voice, first person, under
90 words.

Return JSON:
{ "reviews": [{"key":"...","verdict":"...","reason":"..."} x7],
  "scores": {...}, "interview_chance":"...", "problems":["..."],
  "rejection_story":"..." }

JOB POST:
<paste here>

PROPOSAL:
<paste here>
```

## 04 — Pre-send checklist

```
Check my proposal against every rule. Report each violation with the exact text.
1. Opener names the client's problem, not me. (No "I am", "I have", "Hello".)
2. Exactly one credibility line, placed after the technical detail.
3. At most one portfolio link.
4. All numbers exact and real, no invented clients/results.
5. Ends with a scoped, easy-to-answer question, not a sign-off.
6. No exclamation points, no emoji, no em dashes, no colons in casual copy.
7. Contractions used throughout ("I'll", not "I will").
8. "you"/"your" outnumbers "I"/"my".
9. 3-5 rhythm breaks present; 2-3 minor grammar relaxations max.
10. Length fits the job (90-130 short / 220-320 process).

PROPOSAL:
<paste here>
```
