# Testing in opencode (no Gemini, model = whatever opencode runs)

Goal: prove that the skills work **inside opencode using opencode's own model**
(e.g. `deepseek-v4.1-flash:free`), with no Gemini and no engine involved.

## 1. Install the skills (once)

```powershell
cd F:\PROJECT\upwork-proposal-studio
python -m engine.install --host opencode
```

Confirm opencode sees them:

```powershell
opencode debug skill   # look for upwork-proposal and upwork-hiring-panel
```

## 2. Start a fresh opencode session

Open opencode (new session, so it re-reads the skills). Choose the model you want —
`deepseek-v4.1-flash:free` or any other.

## 3. Test A — write a proposal

Paste the whole job post from `examples/epa-wastewater-job.md`, then send:

```
/upwork-proposal
```

(or just say "write a proposal for this job post".)

**Pass if the reply:** opens on the join/scattered-data problem (not on Sandi),
names a real insider detail (NPDES / registry IDs / census tracts), lands exactly one
credibility line, offers a free mini-audit on one state, and closes on a question.

## 4. Test B — run the panel

Paste your proposal, then the job post, then:

```
/upwork-hiring-panel
```

**Pass if the reply:** gives the seven verdicts, the six scores (Hook, Clarity,
Relevance, Credibility, Value Proposition, Interview Potential), an interview chance,
a numbered problem list worst-first, and the rejection story in the client's voice.

## 5. Compare with the engine (optional)

To see the same job through the engine (which also has the deterministic linter and
panel as a backstop), using the SAME kind of model:

```powershell
python -m engine.cli --job-file examples\epa-wastewater-job.md --out result.json
```

The engine defaults to the `opencode` provider (reads opencode's own auth.json), so
it runs the same model family. Compare the two proposals by hand.

## Notes

- The skills are instructions, not code. Result quality depends on the model. A weak
  model may ignore the five-move structure or the voice rules.
- The engine adds what a bare agent cannot: a deterministic voice-rule linter, and a
  panel that still runs when the LLM call fails.
- If a model produces something off-brand, that is a signal about the model, not the
  skill — try another opencode model for the same job.
