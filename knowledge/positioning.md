# Positioning — Sandi Ridwan

> The identity layer. This file holds the **facts** the writer is allowed to claim, and
> the **rule** for which fact to lead with for which brief type.
>
> Hard rule (from the reference skill, kept): **credentials never open a proposal.**
> These facts land mid-proposal, one at a time, and only when they answer the client's
> actual risk. If a fact cannot be verified in a public repo or a shipped deliverable,
> it does not go in a proposal.

---

## 1. Who this is

**Sandi Ridwan** — Data Automation Engineer & Web Scraping Specialist. Palu, Indonesia.
Solo operator. Builds the full chain: get hard-to-reach data -> clean it -> turn it into
a decision a business can act on.

Two rare things sit next to each other on this profile and usually don't:

1. **Getting data that is actively defended.** Anti-bot bypass at the TLS layer and by
   finding the unguarded path — not by brute-forcing sensors.
2. **Making the data mean something.** Parsing, analysis, dashboards a stakeholder
   can click through.

Most freelancers do one or the other. The proposals should say so — but never as a
brag. As a reason the client's problem has one owner instead of three.

---

## 2. Credibility facts by brief type

Lead with the fact that matches the **risk the client is actually afraid of**.
Never lead with the whole list.

### A. "The site blocks my scraper" / anti-bot / hard targets

| Fact | The risk it kills |
|---|---|
| Bypassed **Akamai Bot Manager** and **DataDome + AWS WAF** without a browser in the loop — by finding the unguarded twin endpoint, not by solving the challenge. | "Everyone I hire says the site is impossible / needs expensive browser farms." |
| **Connecticut Judicial Branch**: 56,598 cases + 187,590 party rows + 440,163 activity rows, past **JA3 TLS fingerprinting** that drops Python at the SSL handshake (`ConnectionResetError 10054`). 41.2 MB, 9-tab Excel, ~11 h with 5 workers. | "Government sites are a wall." |
| **SFDA (Saudi Food & Drug Authority)**: 8,760 drug records behind TLS fingerprinting + **hidden POST pagination** discovered via Playwright intercept. FastAPI + Docker, 33 min runtime. | "The data is behind a login/anti-bot and nobody can touch it." |
| **TikTok mobile API**: reproduced request signatures (X-Gorgon / X-Argus / X-Ladon) in Python — a *third* anti-bot class (app, not web). ~20K shops, 593 req/min, <1% CPU. | "Mobile app data can't be scraped." |
| Method: **map the guard per-path, find the path they forgot to guard.** Turned a 202 WAF challenge into a 200, and 403 into 200. | "We're stuck paying per-call APIs." |

### B. "I need a pipeline, not just a scraper" / automation / enrichment

| Fact | The risk it kills |
|---|---|
| **data-aggregation-agent**: 7 scrapers -> Groq LLaMA scoring -> PostgreSQL -> Airtable 3-tier routing -> SendGrid digest. 302 tests passing, 0 errors, 24/7 on Railway. | "I don't want a script that dies at 3am." |
| **lead-intelligence-pipeline**: CSV -> Groq LLM enrichment (industry, ICP score, intent) -> geo routing -> weighted scoring -> Slack alerts. 16 leads in 22 seconds. | "We need the data enriched and routed, not just dumped in a sheet." |
| **option-scanner**: 0DTE options scanner, 50 tickers, 698+ contracts scored by Delta/Vol-OI/Gamma, AI explanation, Discord alerts 3x/day, deployed 24/7 with PostgreSQL logging. | "It has to run itself and tell us when something matters." |
| **Made.com, n8n, Calendly->Monday.com, Google Sheets->API** automations shipping with duplicate guards, timezone conversion, and error alerts. | "Manual copy-paste is eating our week." |

### C. "I have data; I need answers" / analysis / dashboards

| Fact | The risk it kills |
|---|---|
| **Morrisons Market Intelligence**: 18,100 products scraped -> parsed -> **caught a silent price-column trap** (the visible price was the "Was" price) -> Streamlit dashboard + Tableau bundle + business report. | "The last analyst gave me numbers I couldn't trust." |
| **CFPB-style causal work**: DiD, Synthetic Control, CUPED, placebo + sensitivity tests, validated against ground truth, ending in an explicit decision tier + $ impact. 21 tests. | "We need to know if this actually worked, not just a pretty chart." |
| **A/B Testing Lab**: power, CI, FDR, SRM checks, CUPED in DuckDB + Streamlit. | "Our experiments keep giving us noise." |
| **Food Price / Poverty & Access / Indonesia Economy intelligence**: World Bank + BPS + GADM -> DuckDB -> SQL marts -> Streamlit. Honest about data limits. | "We need a reproducible platform, not a one-off notebook." |
| Every chart carries a **Kenapa / Tujuan / Dampak** (why / goal / impact) box — analysis that states the decision, not just the number. | "Dashboards that look busy but tell us nothing." |

### D. "Deploy / infra / keep it running" / platform

| Fact | The risk it kills |
|---|---|
| **Cloud Run + GCS**: scraper API at **435 req/min, 1 instance, 0 browsers, 277 MiB/4 GiB**. 150K/day needs 104 req/min — one machine, not a fleet. | "This looks like it needs a server farm and a big bill." |
| **public-data-api**: production REST API (FastAPI + Pydantic + DuckDB) with OpenAPI docs, validation, pagination, auth. 26 tests. | "I need an API my team can actually call." |
| Checklist discipline: Dockerfile (not Nixpacks), multi-stage builds, health checks, `.gitattributes` for LF, IAM done in the right order. | "It works on your laptop but breaks in prod." |

### E. "Lead gen / market intel / competitor tracking"

| Fact | The risk it kills |
|---|---|
| **meta-ad-collector**: hybrid Apify + Playwright, competitor ad data (spend ranges, run dates, impressions, platforms) -> CSV + Sheets. | "We're guessing what competitors spend." |
| **Morrisons / Newegg / horse-racing (Racenet, AU proxy + Nuxt SSR decode)**: high-volume competitive + market intelligence, honestly back-tested. | "We need the whole market, not a sample." |
| **B2B lead pipelines**: Saudi, Spain, India, Houston real-estate, Vermont vets, Nairobi dental — Google Maps + API reverse-engineering + DNS email validation + dedup + Excel/WhatsApp export. | "Our list is stale and half-bounces." |

---

## 3. Placement rules (non-negotiable)

1. **Never open with a credential.** The opener is the client's problem, in their words.
2. **Exactly one credibility line per proposal**, placed after move 2 (the technical proof).
3. **Match the fact to the fear**, not to the job title. A "scraper" job that's really
   about a dying pipeline gets the automation fact, not the anti-bot fact.
4. **Numbers must be real and checkable.** 56,598 — not "50,000+". 8,760 — not "thousands".
5. If the brief needs a fact not in this file, the writer writes `[ADD: ...]` and asks.
   It never invents a client, a result, or a metric.

---

## 4. Signature phrases (use sparingly, vary them)

These are earned one-liners, not openers. Rotate; never repeat the same one twice in a row.

- "If the data is trapped behind a wall, getting it out is the part I'm known for."
- "I'd rather find the door they left open than pick the lock they're watching."
- "The data is only half the job. The other half is making it change a decision."
- "Send me the URL. I'll tell you in one pass whether it's a wall or a door."

---

## 5. What this profile does NOT claim

So the writer never overreaches:

- Not a full-stack web app developer (no React/Next product work claimed).
- Not a graphic designer or video editor.
- Not a paid-ads manager — collects ad data, doesn't run campaigns.
- No claim of a specific client's revenue lift unless it's in a shipped deliverable.
