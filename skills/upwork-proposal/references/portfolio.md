# Portfolio — Sandi Ridwan

> Portfolio links, organized by category, with a rule for when to use each.
> **Only public, live, verifiable links go here.** Anything private or local is
> expressed as a capability in `positioning.md`, never as a link.
>
> GitHub: https://github.com/SandiRidwan
>
> Rule: **link at most one portfolio item per proposal.** A wall of links reads as
> "I have no focus." One precise link that mirrors the client's problem reads as
> "I have done exactly this."

---

## A. Anti-bot / hard-target scraping

| Repo | One-line proof | Link |
|---|---|---|
| `ct-appellate-court-scraper` | 56,598 cases past JA3 TLS fingerprinting, ASP.NET VIEWSTATE skipped, 9-tab Excel | https://github.com/SandiRidwan/ct-appellate-court-scraper |
| `sfda-scraper-api` | 8,760 drugs behind TLS fingerprint + hidden POST pagination -> FastAPI + Docker | https://github.com/SandiRidwan/sfda-scraper-api |
| `akamai-nudata-bypass-adobe` | Akamai Bot Manager + NuData bypass via TLS spoofing + behavioural sim, 90% on Adobe.com | https://github.com/SandiRidwan/akamai-nudata-bypass-adobe |
| `horse-racing-analytics` | AU residential proxy + Nuxt SSR decode, zero-browser, honest value-bet backtest | https://github.com/SandiRidwan/horse-racing-analytics |
| `meta-ad-collector` | Meta Ad Library collector, hybrid Apify + Playwright | https://github.com/SandiRidwan/meta-ad-collector |
| `tiktok-hotel-search-aggregator` | Hotel + live OTA prices from TikTok in-app Places, mitmproxy capture, SQLite | https://github.com/SandiRidwan/tiktok-hotel-search-aggregator |

## B. Data automation & pipelines

| Repo | One-line proof | Link |
|---|---|---|
| `data-aggregation-agent` | 7 scrapers -> Groq -> PostgreSQL -> Airtable routing -> SendGrid, 302 tests, 24/7 | https://github.com/SandiRidwan/data-aggregation-agent |
| `lead-intelligence-pipeline` | CSV -> Groq enrichment -> geo routing -> Slack alerts, 16 leads / 22 s | https://github.com/SandiRidwan/lead-intelligence-pipeline |
| `option-scanner` | 0DTE scanner + AI signal bot, 50 tickers, Discord alerts, 24/7 Railway | https://github.com/SandiRidwan/option-scanner |
| `automated-lead-pipeline` | Google Sheets <-> external APIs, Python + Make.com | https://github.com/SandiRidwan/automated-lead-pipeline |
| `calendly-monday-automation` | Calendly -> Monday.com realtime, dup guard, timezone conversion, error alerts | https://github.com/SandiRidwan/calendly-monday-automation |
| `Autopilot-Market-Intel-Brand-Mentions-Logger` | Make.com + Groq brand-mention logger -> Sheets (share of voice) | https://github.com/SandiRidwan/Autopilot-Market-Intel-Brand-Mentions-Logger |

## C. Data analysis & dashboards

| Repo | One-line proof | Link |
|---|---|---|
| `morrisons-market-intelligence` | 18,100 products -> caught a silent price trap -> Streamlit + Tableau + report | https://github.com/SandiRidwan/morrisons-market-intelligence |
| `causal-pricing-decisions` | DiD, Synthetic Control, CUPED, placebo -> explicit decision tier + $ impact, 21 tests | https://github.com/SandiRidwan/causal-pricing-decisions |
| `ab-testing-lab` | Power, CI, FDR, SRM, CUPED in DuckDB + Streamlit | https://github.com/SandiRidwan/ab-testing-lab |
| `food-price-intelligence` | World Bank + DuckDB + SQL marts + Streamlit, reproducible + honest about limits | https://github.com/SandiRidwan/food-price-intelligence |
| `geo-access-atlas` | BPS + GADM + OSM -> DuckDB -> marts -> Folium map | https://github.com/SandiRidwan/geo-access-atlas |
| `indonesia-economy-intelligence` | 60+ years, 17 indicators, cross-era analysis + forecasting + Streamlit | https://github.com/SandiRidwan/indonesia-economy-intelligence |
| `document-intelligence-lab` | PDF extraction + accuracy validation (honest about limits) | https://github.com/SandiRidwan/document-intelligence-lab |

## C1. AI agents / LLM orchestration (AI automation evidence)

| Repo | One-line proof | Link |
|---|---|---|
| `agent-orchestrator-lab` | Production-shaped LLM agent: typed Pydantic tools, multi-provider router (OpenAI/Claude/Gemini/Groq), human-in-the-loop approval that defaults to deny, retries + timeout + error taxonomy, auditable trace. Scored on 4 real API tasks: **100% pass rate, 100% tool accuracy**, with a committed real run trace. | https://github.com/SandiRidwan/agent-orchestrator-lab |

> Use this FIRST on any brief that says AI agent, agent orchestration, tool
> calling, LLM workflow, RAG, prompt engineering, multi-provider, or "not just a
> chatbot". The committed trace (plan -> typed tool calls -> approval-gated write
> -> answer) is the proof.

## C2. SQL, T-SQL & warehousing (advanced SQL evidence)

| Repo | One-line proof | Link |
|---|---|---|
| `sql-analytics-lab` | Advanced SQL (CTEs, `LAG`/`RANK`/`ROW_NUMBER`) run on PostgreSQL + DuckDB + SQL Server; measured tuning on PostgreSQL row-store: pre-aggregation **472x**, correlated-subquery→join **56x**, with `EXPLAIN ANALYZE` before/after | https://github.com/SandiRidwan/sql-analytics-lab |
| `tsql-performance-lab` | 10 T-SQL tuning cases on real SQL Server data; covering index **132x**, implicit-conversion fix **17.9x**, prefix-vs-wildcard LIKE **658x**; equality test proves the tuned query returns the same rows | https://github.com/SandiRidwan/tsql-performance-lab |
| `data-quality-operations` | 13 SQL DQ checks on real data → PASS/WARN/FAIL + root cause + run history; distinguishes "source limitation" from "real break" | https://github.com/SandiRidwan/data-quality-operations |
| `analytics-warehouse` | Star schema + **TYPE-2 SCD** on real BPS data (344 dim rows / 270 regencies); surrogate keys, conformed dims, 10 model-integrity tests | https://github.com/SandiRidwan/analytics-warehouse |

> Use these when a brief names **advanced SQL, T-SQL, window functions, query
> performance, data modelling, or data quality**. Lead with `sql-analytics-lab` or
> `tsql-performance-lab` for query work; `analytics-warehouse` for modelling;
> `data-quality-operations` for monitoring/root-cause.

## D. Lead gen & market intelligence

| Repo | One-line proof | Link |
|---|---|---|
| `saudi-b2b-leads-validator` | Google Maps + DNS email validation + LinkedIn dorking, SA market | https://github.com/SandiRidwan/saudi-b2b-leads-validator |
| `spain-business-leads-scraper` | Selenium Google Maps leads, pagination + dedup + Excel | https://github.com/SandiRidwan/spain-business-leads-scraper |
| `LeadFlow-India` | B2B decision-maker finder + email pattern matching | https://github.com/SandiRidwan/LeadFlow-India |
| `Houston-Lead-Machine` | n8n + Puppeteer + ScrapingBee real-estate lead pipeline | https://github.com/SandiRidwan/Houston-Lead-Machine |
| `morrisons-product-scraper` | 15K+ products, API reverse engineering, Playwright | https://github.com/SandiRidwan/morrisons-product-scraper |
| `Newegg-Market-Intelligence-Bot` | 4,000+ products across 100 categories, checkpointing | https://github.com/SandiRidwan/Newegg-Market-Intelligence-Bot |

## E. Platform / API / infra

| Repo | One-line proof | Link |
|---|---|---|
| `public-data-api` | FastAPI + Pydantic + DuckDB production REST API, OpenAPI, 26 tests | https://github.com/SandiRidwan/public-data-api |
| `report-automation-engine` | Multi-sheet Excel with native charts + formulas, scheduled | https://github.com/SandiRidwan/report-automation-engine |
| `ttm-scanner` | Behavioural + network tracking-tag detector, 9 tags, 5 layers, 100% | https://github.com/SandiRidwan/ttm-scanner |

---

## When to use which

| If the brief is about... | Lead the portfolio with... |
|---|---|
| "The site blocks me" | `ct-appellate-court-scraper` (government + TLS) or `sfda-scraper-api` |
| "Big anti-bot brand" | `akamai-nudata-bypass-adobe` |
| "I need a scraper that runs itself" | `option-scanner` or `data-aggregation-agent` |
| "Enrich and route my leads" | `lead-intelligence-pipeline` |
| "Get me leads / a list" | `saudi-b2b-leads-validator` or `spain-business-leads-scraper` |
| "Analyse this data" | `morrisons-market-intelligence` (has the price-trap story) |
| "Did our change work?" | `causal-pricing-decisions` |
| "Build me an API" | `public-data-api` |
| "Automate my sheets/CRM" | `calendly-monday-automation` or `automated-lead-pipeline` |
| "Competitor / ad tracking" | `meta-ad-collector` |

**Never** paste more than one link in a single proposal. Pick the closest match and
let the repo's README do the talking.
