# Client Research

> What to pull before writing a single line. The proposal's credibility is built
> almost entirely here, in the 60 seconds of research the other 40 applicants skip.
>
> Rule: **every job post is a complaint in disguise.** The client is not describing
> what they want. They are describing what went wrong last time.

---

## 1. Read the job post for the failure mode

Ask, in order:

| Question | What it tells you |
|---|---|
| What did they try that failed? | The real problem. "I tried Scrapy and got blocked" -> anti-bot. |
| What is the *symptom* they named? | Steer the technical detail in move 2 to that exact symptom. |
| What's the deadline pressure? | Picks short vs long variant. "ASAP", "this week" -> short. |
| What's the budget signal? | Hourly vs fixed, "simple task" vs "ongoing partnership". |
| What are they afraid of? | Ghosting, no-show, a scraper that breaks, data they can't trust. |
| Which niche is this really? | A, B, C, D or E in `positioning.md`. That picks the credibility fact. |

### Red flags to name gently (or avoid the job)

- "Simple task, $5" but actually needs a bypass.
- "Need 1M records, no budget" — flag scope vs price honestly.
- Asks to move off Upwork / pay outside — declines; mentions platform terms.
- Wants something against a site's ToS in a way that's clearly harmful. Decline.

### Green flags to acknowledge

- A concrete URL or sample.
- A real business goal ("we price against competitors weekly").
- Willing to share access to their own data.
- Past freelancer mentioned ("the last guy couldn't...") — the door is open.

---

## 2. Research the client (if it has web access / the user pastes it)

| Source | Pull |
|---|---|
| The job post itself | Company name, location, timezone, a specific product/page mentioned |
| Their website / storefront | One true, specific observation nobody else will make |
| Their Upwork profile | Spend, hire rate, verification, country, member since |
| The listing / product | A detail that proves you opened it (a category, a SKU, a broken page) |

### The one true observation

This is the highest-leverage sentence in the whole proposal. It must be:

- **True** (checkable, not guessed)
- **Specific** (not "I see you sell products")
- **Useful** (implies a next step)

Good: "Your alcohol category has 60% of SKUs on promotion but the pages don't show the
promo price in the listing, so a price tracker reading the visible field would be wrong
most of the time."

Bad: "I visited your website and it looks great."

---

## 3. Client-type heuristics (how the pitch changes)

| Client type | Signals | Pitch adjustment |
|---|---|---|
| **First-timer** | 0 hires, low spend, job posted once | Reassure with process. Offer a free sample. Short variant often better. |
| **Serial hirer** | 10+ hires, high spend | Skip reassurance. Lead with the technical edge. They've seen 50 proposals. |
| **Enterprise / agency** | Big spend, polished post, NDAs | Process variant. Mention reliability, tests, deploy discipline. |
| **Startup / solo founder** | Buzzwords, "we're building", urgency | Short variant. Speak their language. Offer one concrete first step. |
| **Agency middleman** | "I need a VA/dev for my client" | Reliability + white-label. Process variant. |

---

## 4. The client's private scorecard

Before sending, the writer assumes the client is asking:

1. Does this person understand my problem? (move 1 + 2)
2. Can they actually do it? (move 2 + 3)
3. What happens if they hire me and it goes wrong? (move 4)
4. What's the next step, and is it easy? (move 5)

If any answer is missing, the proposal loses. The panel in `engine/panel.py` scores
exactly these.

---

## 5. Output of research (internal, before writing)

The analyzer produces a small dict the writer consumes:

```json
{
  "niche": "A | B | C | D | E",
  "failure_mode": "one sentence, in the client's words",
  "named_symptom": "the exact thing they said",
  "client_type": "first_timer | serial | enterprise | startup | agency",
  "urgency": "high | medium | low",
  "budget_signal": "...",
  "red_flags": ["..."],
  "one_true_observation": "the specific detail | [ADD: ...] if missing",
  "credibility_fact": "which fact from positioning.md",
  "portfolio_link": "at most one, from portfolio.md",
  "variant": "short | process"
}
```
