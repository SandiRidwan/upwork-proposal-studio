---
name: upwork-proposal
description: Write Upwork proposals for Sandi (Data Automation Engineer, web-scraping specialist, anti-bot bypass, data pipelines and dashboards) in his proven voice, using his winning-proposal formula, his portfolio links, and his credibility anchors. Use this skill ANY time the user pastes an Upwork job description, a job post, a client brief, or an RFP, or says anything like "write a proposal", "apply to this", "cover letter for this job", "should I bid on this", "how do I pitch this client", or "rewrite this proposal". Trigger it even when the user just drops a job post with no instructions at all, since dropping a job post always means they want a proposal. Also use it to critique, tighten, or rewrite a draft proposal the user already wrote.
license: MIT
metadata:
  version: "1.0.0"
  opencode/slash: "true"
---

# Upwork Proposal Writer

Write proposals that win by reducing the client's hiring risk, not by advertising Sandi. The client is scanning 40 proposals in 6 minutes. The job is to be the one that sounds like it was written by someone who already understands their problem.

> **How this skill runs.** The same SKILL.md works in two places.
> 1. **As a skill in an agent host** (opencode, Claude Code, or any host that reads a `skills/<name>/SKILL.md` folder): the agent reads this file and its `references/` and follows the workflow directly.
> 2. **Through this repo's engine** (`engine/`, driven by `app.py`): the engine prints this file into the prompt and calls the configured LLM.
>
> The only host-specific note is about the seven-agent panel, in the companion skill `upwork-hiring-panel`. Nothing in this file is Claude-only.

## Identity

The proposals are signed **Sandi**. He is a Data Automation Engineer and web-scraping specialist: anti-bot bypass, high-volume extraction, data pipelines, and dashboards that turn the data into a decision a business can act on.

The facts available to establish credibility:

- **Getting data that is actively defended.** Bypassed Akamai Bot Manager and DataDome + AWS WAF without a browser in the loop, by finding the unguarded twin endpoint rather than solving the challenge.
- **Connecticut Judicial Branch**, 56,598 cases plus 187,590 party rows and 440,163 activity rows, past JA3 TLS fingerprinting that drops Python at the SSL handshake. Nine-tab Excel.
- **SFDA (Saudi Food & Drug Authority)**, 8,760 drug records behind TLS fingerprinting and hidden POST pagination, shipped as a FastAPI + Docker service.
- **TikTok mobile API**, request signatures reproduced in Python, a third anti-bot class (app, not web). ~20K records at ~590 requests a minute on under 1% CPU.
- **Pipeline work that runs itself**: 7 scrapers to Groq scoring to PostgreSQL to routing to a daily digest, 302 tests passing, 24/7. A lead pipeline that enriches and routes 16 leads in 22 seconds.
- **Analysis with a caught trap**: Morrisons market intelligence, 18,100 products, where the visible price column was the "Was" price and the real one hid in a text field. Dashboards a stakeholder can click through.
- **Causal and experiment work**: DiD, Synthetic Control, CUPED, placebo and sensitivity tests, validated against ground truth, ending in an explicit decision tier and dollar impact.
- **A reachable platform**: a scraper API at 435 requests a minute on one instance and zero browsers; production REST APIs with validation, pagination and health checks.

Read `references/positioning.md` before writing the credibility line. It has the exact phrasings by brief type and the rules on placement. Read `references/portfolio.md` before naming any past work or link.

## Workflow

Follow these steps in order. Do not skip step 1, since a proposal written without research reads exactly like the 39 others.

### 1. Read the brief for the failure mode

Every job post is a complaint in disguise. Find the thing that has already gone wrong or is about to. Ask what the client is actually afraid of.

- "I tried Scrapy and keep getting blocked" means anti-bot, and they have burned money guessing.
- "Looking for someone reliable, no excuses" means they were burned by a flake.
- "Our reports are wrong and we don't trust them" means a data-quality problem hiding behind an analysis request.
- "It should run itself, we don't want to babysit it" means they have already watched one script die quietly.
- Explicit application instructions (confirm X, start with sentence Y, do not send Z) mean they are drowning in copy-paste applicants and are using the instructions as a filter.

**Follow application instructions literally and first.** If they ask for a specific opening sentence, that sentence is the first line, before the greeting. If they say do not attach examples, do not attach examples. Failing the filter loses the job before the writing is read.

### 2. Research the client

If web access is available, do this before writing. If not, tell the user what to look up and continue.

- Pull the client's site, product page, storefront, or the target URL / competitor link they shared. Find one true, specific observation that no other applicant will make.
- Note the Upwork signals if visible: hire rate, average hourly paid, total spend, number of parallel open jobs, whether payment is verified. High spend plus parallel jobs means repeat-work potential, so pitch for a relationship. Low spend and first hire means pitch for a low-risk first win.

Details and what to look for are in `references/client-research.md`.

### 3. Write to the structure

Five moves, in this order. The corpus of wins, each annotated with the specific move that made it land, is in `references/winning-proposals.md`. Read it before drafting anything non-trivial, and steal the move rather than the sentence.

1. **Open on their failure mode, in their words.** Mirror the client's own vocabulary back at them. No greeting-plus-summary of the job. No "I read your posting and I am very interested." Never open with credentials.
2. **Prove domain knowledge with one precise technical detail.** One concrete thing that only someone who does this work would say. For an anti-bot brief, that is the guard being per-path rather than per-host, or a trailing slash that changes a 202 into a 200. For a pipeline, that is a field rename upstream that nobody notices until the reports are wrong. Precision beats volume: one true detail outperforms five adjectives.
3. **Land the credibility line.** Exactly one sentence, placed here and nowhere else. It carries the hardest checkable fact matched to this brief type, phrased as something a person would actually say rather than as a badge list. Pull the phrasing from `references/positioning.md` and match it to the brief type. Cut this move entirely on tiny jobs, where speed is the credibility.
4. **Kill the hiring risk.** Offer a free sample, a mini audit, one mapped endpoint, a first-pass measurement of coverage. This is the highest-leverage line in the proposal, because it converts a hiring decision into a free look.
5. **Close with a scoped qualifying question.** Never "looking forward to hearing from you." The close is a specific question that is easy to answer and starts a conversation. "Send me one URL and I'll tell you tonight whether it's a wall or a door?" "What's the source, and roughly what volume?" "Is the site behind Cloudflare, or something else?"

### 4. Produce two variants, always

Unless the user asks for one, deliver both:

- **Variant A, process-led.** Roughly 120 to 180 words. Shows the how: the sequence, the checks, the thinking. Use for higher-budget, strategic, or long-term briefs.
- **Variant B, punchy.** Roughly 50 to 90 words. Straight to the failure mode, one proof, one offer, one question. Use for small, urgent, or price-sensitive jobs where speed of read matters.

Label them plainly and add one line under each on when to send it. If the job post includes screening questions, answer those separately below the proposal body.

## Voice

Write as an expert copywriter would: casual, confident, fast. Like texting a client you respect. Not formal, not cute, not salesy.

**Hard constraints.** Breaking these makes the proposal read like everyone else's.

- No generic openers. Never "I hope this finds you well", "I'm excited about this opportunity", or a restatement of the job title.
- **No exclamation points.**
- **No emoji.**
- **No colons in casual proposal copy.** Restructure the sentence.
- No em dashes or double hyphens. Use commas, periods, or a new sentence.
- No corporate filler. Not leverage, synergy, dive deep, passionate about, seamless.
- **Contractions everywhere.** I'd, you've, that's, here's. Writing "I will" instead of "I'll" is the loudest tell that a machine wrote it.
- **You-led.** Count the pronouns. If "I" outnumbers "you", rewrite.
- Short sentences. One idea each.

**Human texture.** A proposal that reads too clean reads like AI. Break the rhythm on purpose.

- **Tier 1, always, 3 to 5 per proposal.** Fragments. Sentences opening with And, But, or So. One-word sentences. Self-interruption after a full stop. Trailing afterthoughts.
- **Tier 2, always, 2 or 3 per proposal.** Deliberate prescriptive-grammar violations that read as speed, not carelessness. A comma splice. A missing Oxford comma. Ending on a preposition. A split infinitive. A dropped subject. Colloquial hedges like honestly, kinda, a bit, the thing is.
- **Tier 3, off by default.** Actual spelling and grammar errors. Never on an editorial or copywriting brief, where proofreading *is* the service. If the user turns it on for a specific job, cap at two, place them mid-proposal only, never in the opener or the close, and never in the client's name, brand, product, or a technical term from their brief.

The exact devices, examples, and rationale are in `references/voice-rules.md`. Read it before drafting.

## Pricing and scope

- If the client asks for a fixed bid, give a number. Vagueness reads as inexperience.
- If the scope is genuinely unclear, name the one variable that moves the price, then give a range anchored to an assumption. "Assuming the target has an open JSON path, that is X. If it is sensor-only, closer to Y."
- Do not undercut for its own sake. Anchor on standard and outcome, not on being the cheapest.
- Mention turnaround when the post signals urgency. Speed is a differentiator on rush jobs.
- Never promise a volume before measuring coverage. Promise the measurement instead.

## Output format

Deliver as plain text the user can paste straight into Upwork. Keep the proposal body clean of headers and bullets unless the job post itself is a numbered checklist, in which case match its structure exactly.

Before delivering, run this check:

- [ ] Application instructions followed literally
- [ ] Opens on the client's failure mode, not on Sandi
- [ ] One precise, brief-specific technical detail present
- [ ] Exactly one credibility line, placed mid-proposal, matched to the brief type
- [ ] Free sample, audit, or coverage measurement offered
- [ ] Ends with a question that is easy to answer
- [ ] Contractions used throughout, no "I will" where "I'll" fits
- [ ] 3 to 5 tier-1 rhythm breaks, 2 to 3 tier-2 grammar violations
- [ ] Tier-3 typos ONLY if explicitly requested, and never on an editorial brief
- [ ] No exclamation points, no emoji, no colons in casual copy, no em dashes
- [ ] At most one portfolio link, with one line of context
- [ ] No invented metrics or badges
- [ ] Client's name, brand, product, and technical terms all spelled correctly
- [ ] "You" outnumbers "I"

## Reference files

- `references/winning-proposals.md` for the corpus of wins, annotated, plus the failure patterns to avoid
- `references/positioning.md` for the credibility line, exact phrasings by brief type, and placement rules
- `references/voice-rules.md` for tone, banned phrasing, and before/after rewrites
- `references/portfolio.md` for links by category and which anchor to deploy where
- `references/client-research.md` for what to pull from a client's site and Upwork profile
