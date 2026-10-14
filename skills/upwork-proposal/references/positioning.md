# Positioning and Credibility

## The one-line credibility block

Every proposal on a job worth winning should carry **one** line establishing that Sandi is not a random applicant. One line. Not a paragraph, not a résumé, not a list of badges.

Place it **after the hook and before the offer**, never as the opening sentence. Opening with your own credentials tells the client you are thinking about yourself. Opening with their problem tells them you are thinking about them, and then the credential lands as reassurance rather than as a sales pitch.

## Experience: how to answer "N+ years" honestly

**Real figure: 3 years.** State it plainly when a post asks for more. Two rules:

1. **Never invent a number.** If the post asks for 5 and the real number is 3, say 3,
   and do not dodge with "it's hands-on throughout" (that reads as hiding something).
2. **State the real position, then anchor it with depth and volume in the same
   breath.** Approved shape:
   > "Three years, but production pipelines ship from here weekly and this exact
   > stack is what runs daily. The depth is in what's shipped, not the calendar."

The anchor must be true: repos, records processed, tests, uptime. A shorter honest
tenure with strong evidence beats a vague hedge, and it beats a number the client
can check against the profile.

**Never** claim 5+ years. Do not put a fabricated year count anywhere. The panel
flags it and clients verify.

## Rate card (set to real numbers)

| Service shape | Rate | Notes |
|---|---|---|
| Standard technical work | **$30 /hr** | scraping, pipelines, SQL, analysis, DQ |
| Short task / one-off fix | **$30 /hr** (min 2 hrs) | small, urgent, single deliverable |
| Scraper / extraction build | **$30 /hr**, or fixed by scope | quote after a coverage measurement |
| Pipeline / automation | **$30 /hr** | includes monitoring + alerting |
| Data analysis / dashboard | **$30 /hr** | includes a written summary |
| SQL / warehouse / DQ work | **$30 /hr** | tuning or modelling |
| Volume data (per 1,000 records) | **$60** per 1,000 valid rows | state the "valid" definition; $95 if enrichment needed |
| Availability | **25 hrs/week**, start within **2 days** | fixed-hour or milestone both fine |

Guidance: anchor at $30/hr; go up to $40 for senior/urgent scope, down to $25 only
for a small first job with a long-term signal. Never quote below $20 — it reads as
junior and attracts the wrong clients. On a fixed bid, estimate hours at $30/hr and
round up, not down.

If a client asks for a rate the card does not cover, use the closest row and scale.

## The verified facts to draw from

Use only what is true and only what is relevant to the brief in front of you. Every number here is checkable against a public repo.

### A. "The site blocks my scraper" / anti-bot / hard targets

- **Bypassed Akamai Bot Manager and DataDome + AWS WAF without a browser.** The strongest single signal for a "this site is impossible" brief. The method is the proof: found the unguarded twin endpoint instead of solving the challenge.
- **Connecticut Judicial Branch, 56,598 cases.** Past JA3 TLS fingerprinting that drops Python at the SSL handshake (`ConnectionResetError 10054`). Plus 187,590 party rows and 440,163 activity rows. Use on government, legal, and "the server just closes the connection" briefs.
- **SFDA, 8,760 drug records.** Behind TLS fingerprinting and hidden POST-based pagination. Shipped as a FastAPI + Docker service. Use on registry, compliance, and "the data is behind a login/bot wall" briefs.
- **TikTok mobile API, ~20K records, ~590 requests a minute, <1% CPU.** Request signatures (X-Gorgon / X-Argus / X-Ladon) reproduced in Python. Use when the target is a mobile app, not a website.
- **Method, stated plainly when asked:** map the guard per-path, then find the path they forgot to guard. A 202 challenge became a 200. A 403 became a 200. Use on any brief where the client is stuck or being quoted per-call API prices.

### B. "I need a pipeline, not just a scraper" / automation / enrichment

- **7 scrapers to Groq scoring to PostgreSQL to 3-tier routing to a daily email digest.** 302 tests passing, 0 errors, 24/7. Use when the client says the word "reliable", "ongoing", or "we don't want to babysit it".
- **A production-shaped LLM agent, not a chatbot.** Typed Pydantic tools (a bad tool call is rejected, never executed), a router across OpenAI/Claude/Gemini, human-in-the-loop approval for sensitive actions, retries with backoff, and an auditable trace. Scored on real API tasks: **100% pass rate, 100% tool accuracy**. Use on any "AI agent / agent orchestration / tool calling / not just a prototype" brief.
- **A lead intelligence pipeline that enriches and routes 16 leads in 22 seconds.** CSV to LLM enrichment (industry, ICP score, intent) to geo routing to Slack. Use on lead-gen and enrichment briefs.
- **A 0DTE options scanner, 50 tickers, 24/7 with alerts.** Use when the client wants a job that runs itself and tells them when something matters.
- **Sheets, Make.com, n8n, Calendly to Monday.com.** Duplicate guards, timezone conversion, error alerts. Use on "someone copies this by hand every day" briefs.

### C. "I have data; I need answers" / analysis / dashboards

- **Morrisons market intelligence, 18,100 products, and a caught trap.** The visible price column was the "Was" price and the real one hid in a text field. Streamlit dashboard plus a Tableau bundle plus a business report. Use on any "we don't trust the last numbers" brief.
- **Causal pricing work.** DiD, Synthetic Control, CUPED, placebo and sensitivity tests, validated against ground truth, ending in a decision tier and dollar impact. 21 tests. Use on "did this actually work" briefs.
- **An A/B testing lab.** Power, CI, FDR, SRM checks, CUPED. Use on "our experiments keep giving us noise".
- **Reproducible data platforms.** World Bank, BPS, GADM to DuckDB to SQL marts to Streamlit, honest about data limits. Use on "we need a platform, not a one-off notebook".
- **Every chart states the decision, not just the number.** Use when the client says the last dashboard told them nothing.

### C2. "Advanced SQL / T-SQL / data modelling" / warehouse roles

- **Advanced SQL, measured not just written.** CTEs, `LAG`/`RANK`/`ROW_NUMBER`, window frames, gaps-and-islands, conditional-aggregate pivots, anti-joins — run on **PostgreSQL 18, SQL Server 2017 and DuckDB**. Use on any "advanced SQL" brief.
- **Query performance with the numbers attached.** On a real PostgreSQL row-store: pre-aggregation **472x**, correlated-subquery→join **56x** (8.8s→0.16s). On real SQL Server data: covering index **132x**, implicit-conversion fix **17.9x**, prefix-vs-wildcard `LIKE` **658x** — each with `EXPLAIN ANALYZE`/`SHOWPLAN` before and after. Use when the brief says "query performance improvement".
- **T-SQL for real.** 10 tuning cases executed on Microsoft SQL Server, not written on paper. Use when the brief names T-SQL or the Microsoft stack.
- **A dimensional model that survives change.** Star schema with a **TYPE-2 slowly-changing dimension**: 344 dimension versions for 270 regencies, so "what was this attribute in 2021?" still answers correctly. Use on data-modelling / warehouse briefs.
- **Data quality as a system.** 13 SQL checks → PASS/WARN/FAIL with a plain-English root cause per check, and it distinguishes a source limitation from a real break. Use on "monitor data quality" briefs.

### C3. The combination (the real differentiator)

Most analysts can either **get the data** or **analyse it**. Very few do both end to end. State it plainly when the brief is small-team or data-heavy: extraction at scale + automation + SQL + analysis in one person. Use on "one person who can own the data" briefs rather than pure reporting roles.

### D. "Deploy it and keep it running" / platform

- **A scraper API at 435 requests a minute, one instance, zero browsers, 277 MiB of 4 GiB.** 150K a day needs 104 requests a minute, so one machine, not a fleet. Use when the client is worried about cost or scale.
- **Production REST APIs** with validation, pagination, OpenAPI docs and health checks. 26 tests. Use on "I need an API my team can call".
- **Deploy discipline**: Dockerfile over Nixpacks, multi-stage builds, health checks, LF endings, IAM in the right order. Use on "it works on your laptop but breaks in prod".

### E. Lead gen and market intelligence

- **Meta Ad Library collector.** Hybrid Apify + Playwright, spend ranges and run dates to CSV and Sheets. Use on "we're guessing what competitors spend".
- **High-volume market scraping with honest back-tests.** Morrisons, Newegg, horse-racing (Australian proxy plus Nuxt SSR decode). Use on "we need the whole market, not a sample".
- **B2B lead pipelines.** Saudi, Spain, India, Houston real-estate, Vermont vets, Nairobi dental. Google Maps plus API reverse-engineering plus DNS email validation plus dedup. Use on "our list is stale and half-bounces".

## Additional anchors, used sparingly

- **"Zero browser" for anti-bot work.** The differentiator is that the expensive, fragile browser route was not needed. Use when the client is being quoted browser-farm prices.
- **"Measured coverage before promising volume"** on any lead-gen or market brief. Best on jobs where the client has already been burned by a sample that looked complete and wasn't.
- **"The trap was caught before it reached the client"** on analysis briefs with a trust problem.
- **Honest about limits.** Use when the client has been over-promised before.
- **Do not use a big number on a $45 fix.** It reads as posturing. On tiny jobs, credibility comes from speed and specificity.

## How to phrase it

Never write it as a badge list. Write it as a sentence a person would say.

**Weak.** "I am a web scraping expert with 4 years of experience in Python, Selenium and BeautifulSoup."

**Strong, anti-bot brief.**
> I've done this on two sites that most people call impossible, Akamai and DataDome, without a browser. The trick is almost never the sensor. It's finding the path they forgot to guard.

**Strong, "the site is impossible" brief.**
> On a court site I pulled 56,000 cases past a server that drops Python at the handshake. The site wasn't impossible, it just needed a fingerprint it recognised.

**Strong, mobile-app brief.**
> Mobile apps are a different problem from websites. There's no sensor to get past, every request is signed. I've reproduced those signatures in Python before, on a major short-video app, around 20,000 records at 590 requests a minute.

**Strong, pipeline brief.**
> The hard part isn't the first run, it's month three when the site renames a field and nobody notices the reports are wrong. One pipeline I run has 302 tests and alerts on its own failures.

**Strong, "we don't trust the numbers" brief.**
> On a grocery set the visible price column was the "Was" price, and the real one hid in a text field. Trusting the column would have overstated every number in the report. I caught it before it reached the client.

**Strong, rush or reliability-anxious brief.**
> I hit dates, and I'll tell you the truth about whether a job is a two-hour one or a two-day one before you spend anything.

## The Upwork-native signal

Clients hiring on Upwork care that you stand behind the work. Say so plainly and briefly.

Good phrasings:
- "I'd rather tell you it's a two-day job than take it and disappear."
- "Send one URL. If it's not solvable the way I think, you've lost nothing."

Do not stack more than one of these. Two credibility claims in a row start sounding defensive.

## Hard rules

- **One credibility line per proposal.** Two at absolute most, and only on high-value briefs.
- **Never open with it.** The client's problem opens the proposal. Always.
- **Never invent a number.** If a real figure exists, use it. If not, say nothing rather than inventing one. A fabricated metric is the fastest way to lose a client who checks.
- **Only claim tools actually used.** Claims that can be checked against a repo in one click must match it.
- **Match the claim to the brief.** The court case is fine on a government brief. It is not fine on a $50 form-scrape, where it reads as posturing.
- **Cut it entirely on tiny jobs.** On a three-line proposal for a $45 fix, credibility comes from speed and specificity, not from a résumé.
