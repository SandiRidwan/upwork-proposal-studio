# Portfolio Gap Analysis — for SQL / Data Analyst roles

When a job asks for **advanced SQL / T-SQL, window functions, query tuning** and you
bid with a scraping-heavy portfolio, the panel scores it LOW. This is honest, and it
is a portfolio problem, not a wording problem. Fix the portfolio and the same engine
produces a convincing proposal.

Below: what the gap is, and the exact repos to build to close it. Each is small,
finishable in a weekend, and written so the README proves the skill in one screen.

---

## The gap, stated plainly

| What SQL-analyst jobs test | What the current portfolio shows | Verdict |
|---|---|---|
| Advanced SQL (CTEs, window functions, joins at grain) | Occasional SQL in DuckDB marts, never the headline | weak |
| T-SQL / Microsoft stack | nothing | missing |
| Query performance tuning | nothing (perf stories are scraping/caching, not SQL) | missing |
| Data validation / root-cause on data quality | the "price trap" story, but told as scraping | partial |
| Large relational models | DuckDB, but framed as a scraping byproduct | partial |
| Stakeholder / turning data into decisions | narrated, not evidenced | weak |
| Python automation | strong | **good** |
| Dashboards / insight | strong (Streamlit, Tableau) | **good** |

**Strength you should NOT hide:** extraction, pipelines, "runs itself". Many SQL jobs
also want automation. Lead with automation *plus* a SQL credential, not automation
instead of it.

---

## Projects that close it (build these; then the engine cites them)

Each one below is designed so a single README table proves the skill. Name them so a
recruiter scanning your profile sees the keyword.

### 1. `sql-analytics-lab` — the anchor repo (highest priority)

**One-line:** A set of 25+ business questions answered in advanced SQL, in several
dialects (PostgreSQL, T-SQL, DuckDB), each with the query, the result, and the
execution plan before/after optimisation.

**Why it wins:** it directly names CTE, window functions, joins, T-SQL, EXPLAIN.
A recruiter looking for "advanced SQL" finds the exact words.

**Contents (README table, one row per question):**

| # | Question | Dialect | Techniques | Rows | Plan before → after |
|---|---|---|---|---|---|
| 1 | Month-over-month revenue growth | PostgreSQL | LAG, window, CTE | 240k | 1.9s → 40ms |
| 2 | Running 12-month average | PostgreSQL / T-SQL | window frame | 240k | 2.2s → 55ms |
| 3 | Top-N per group (top 3 per region) | T-SQL | ROW_NUMBER, RANK | 240k | 1.4s → 30ms |
| 4 | De-duplicate at grain | T-SQL | ROW_NUMBER dedup | 1.2M | 3.0s → 120ms |
| 5 | Cohort retention table | PostgreSQL | conditional agg, CTE | 90k | 2.5s → 90ms |
| 6 | Gaps and islands (streaks) | T-SQL | ROW_NUMBER diff | 500k | 4.0s → 150ms |
| 7 | Find the fan-out (grain bug) | any | join vs count check | — | demo of the trap |
| ... | (to 25) | | | | |

Also include: `EXPLAIN ANALYZE` output before/after, an index that fixed it, and a
one-paragraph "what the number means for the business" under each query.

**Skills it proves:** CTEs, window functions (LAG, ROW_NUMBER, RANK, frames),
aggregations, joins at grain, data validation, query tuning (index, plan), T-SQL,
PostgreSQL.

### 2. `tsql-performance-lab`

**One-line:** Ten slow queries on a sample Microsoft-style schema, each with the
problem, the fix, and the measured before/after.

**Why it wins:** T-SQL is a hard requirement you currently cannot evidence at all.

**Contents:** SQL Server (or Azure SQL free tier). Each case: query, execution plan
screenshot/notes, the index or rewrite, new timing. Topics: SARGability, covering
index, parameter sniffing, implicit conversion, key vs included columns, statistics.

### 3. `data-quality-operations`

**One-line:** A monitoring job that runs SQL validation checks on a warehouse, logs
failures, and opens a ticket-style report.

**Why it wins:** the job asks to "monitor data quality, find errors, identify root
causes". This is that, in code.

**Contents:** checks like null-rate, row-count drift, referential integrity, duplicate
keys, orphaned FKs, freshness. Each produces a pass/fail + a sample of offending rows
+ a plain-English cause. Runs on a schedule; a Streamlit page shows the last 30 days.

### 4. `analytics-warehouse` (dimensional model)

**One-line:** A small star schema (fact + 4 dims) built from a real public dataset,
with the SQL that loads it and the business queries on top.

**Why it wins:** "large relational databases and complex data models" becomes
concrete. Shows you know grain, keys, SCD basics, and why the model makes queries
fast.

### 5. Re-frame one existing repo for SQL

Take `morrisons-market-intelligence` (or `food-price-intelligence`) and add a
top-level section: **"The SQL behind the insight"** — the CTEs, window functions, and
validations that produced each chart, with timings. Same repo, now it answers the SQL
question instead of only the scraping one.

---

## Also fix these, cheaply

1. **Pin the profile headline** to include "SQL · T-SQL · Python · Analytics" so the
   first screen matches the keyword search.
2. **Add a `sql/` folder to every analytics repo** with the queries used, even if the
   project was Python-first. Reviewers grep for `.sql`.
3. **One legend line per repo README**: "Techniques: CTE, window functions, joins at
   grain, EXPLAIN tuning, T-SQL" so the keyword is present for search and for the
   proposal writer to cite.
4. **Don't claim 5+ years if it's not true.** The panel flags it, and clients check.
   Instead, lead with years you can defend and the density of real work.

---

## How this feeds the proposal engine

Once `sql-analytics-lab` exists, add it to `skills/upwork-proposal/references/portfolio.md`
under a new **"SQL / analytics"** row, and add a line to `positioning.md`:

> Answered 25+ business questions in advanced SQL (CTEs, window functions, joins at
> grain) across PostgreSQL and T-SQL, with query plans measured before and after
> tuning.

Then `python -m engine.cli` on a SQL-analyst brief will cite it, the panel will see a
matching proof link, and the interview chance moves from LOW to real.

Until then, the honest move on SQL-heavy briefs is to bid on the automation + analysis
half of the job, not the SQL-only half.
