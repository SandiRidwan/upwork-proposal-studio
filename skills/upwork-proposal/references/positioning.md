# Positioning and Credibility

## The one-line credibility block

Every proposal on a job worth winning should carry **one** line establishing that Sandi is not a random applicant. One line. Not a paragraph, not a résumé, not a list of badges.

Place it **after the hook and before the offer**, never as the opening sentence. Opening with your own credentials tells the client you are thinking about yourself. Opening with their problem tells them you are thinking about them, and then the credential lands as reassurance rather than as a sales pitch.

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
- **A lead intelligence pipeline that enriches and routes 16 leads in 22 seconds.** CSV to LLM enrichment (industry, ICP score, intent) to geo routing to Slack. Use on lead-gen and enrichment briefs.
- **A 0DTE options scanner, 50 tickers, 24/7 with alerts.** Use when the client wants a job that runs itself and tells them when something matters.
- **Sheets, Make.com, n8n, Calendly to Monday.com.** Duplicate guards, timezone conversion, error alerts. Use on "someone copies this by hand every day" briefs.

### C. "I have data; I need answers" / analysis / dashboards

- **Morrisons market intelligence, 18,100 products, and a caught trap.** The visible price column was the "Was" price and the real one hid in a text field. Streamlit dashboard plus a Tableau bundle plus a business report. Use on any "we don't trust the last numbers" brief.
- **Causal pricing work.** DiD, Synthetic Control, CUPED, placebo and sensitivity tests, validated against ground truth, ending in a decision tier and dollar impact. 21 tests. Use on "did this actually work" briefs.
- **An A/B testing lab.** Power, CI, FDR, SRM checks, CUPED. Use on "our experiments keep giving us noise".
- **Reproducible data platforms.** World Bank, BPS, GADM to DuckDB to SQL marts to Streamlit, honest about data limits. Use on "we need a platform, not a one-off notebook".
- **Every chart states the decision, not just the number.** Use when the client says the last dashboard told them nothing.

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
