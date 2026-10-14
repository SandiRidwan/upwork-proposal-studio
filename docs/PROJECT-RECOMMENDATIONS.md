# Project Recommendations — Sandi

Rewritten after reading the actual repos. The earlier gap doc assumed the SQL was
missing. It is not. `food-price-intelligence/sql/transform.sql` already has multi-CTE,
`LAG() OVER (PARTITION BY ...)`, `RANK() OVER (...)`, `stddev_pop`, conditional
aggregation, and `count(DISTINCT)`. The skill is there. **The problem is that it is
buried inside a Python repo, and two things a SQL job always tests are genuinely
absent: query performance tuning, and T-SQL.**

So the recommendations change: less building, more surfacing, plus two small new repos.

---

## The real gap (corrected)

| What SQL jobs test | Where it lives today | Action |
|---|---|---|
| CTEs, window functions, joins at grain | Already in `food-price-intelligence`, `ab-testing-lab`, `causal-pricing-decisions` | **Surface it** in a dedicated repo |
| Aggregations, data validation | Already in the SQL above | Surface it |
| Query performance tuning (index, EXPLAIN, before/after) | Not shown anywhere | **Build small** |
| T-SQL / SQL Server | Absent | **Build small** |
| Data quality / root cause | The "price trap" story, told as scraping | Reframe |
| Python automation | Strong | Keep |
| Dashboards | Strong | Keep |

---

## Project 1 — `sql-analytics-lab` (the one that matters)

Not a from-scratch build. It is a **curated home for the SQL you already wrote**, plus
the patterns a SQL interview actually probes.

**What goes in:**

- The `transform.sql` from `food-price-intelligence` (YoY with `LAG`, `RANK` within
  year, indicator pivot, volatility with `stddev_pop`). Already real work.
- The equivalent from `ab-testing-lab` and `causal-pricing-decisions`.
- Add the patterns that are missing and always tested:

| # | Question | Dialect | Technique | Why it's here |
|---|---|---|---|---|
| 1 | Month-over-month growth | PG + T-SQL | `LAG` window | you have this |
| 2 | 12-month running average | PG + T-SQL | window frame `ROWS` | you have this |
| 3 | Top-3 per region | T-SQL | `ROW_NUMBER` / `RANK` | partially |
| 4 | De-duplicate keeping latest | T-SQL | `ROW_NUMBER` dedup | new, always asked |
| 5 | Gaps and islands (streaks) | T-SQL | `ROW_NUMBER` diff | new, classic test |
| 6 | Cohort / retention table | PG | conditional agg + CTE | new |
| 7 | Find the fan-out (grain bug) | any | join vs count check | your price-trap, as SQL |

- **For 3 of them, add the tuning story**: the query, `EXPLAIN ANALYZE`, the index or
  rewrite, and the before → after timing. This single addition answers "query
  performance improvement", the one requirement you cannot currently evidence.

**README:** one table, one row per question, columns = question / dialect /
techniques / rows / plan before→after. A recruiter greps `.sql`, lands here, and the
first screen proves CTE + window + tuning + T-SQL.

**Effort:** small. Most queries exist; you are moving and annotating them.

---

## Project 2 — `tsql-performance-lab`

T-SQL is the only hard requirement with zero evidence. This is the smallest real fix.

**Contents:** SQL Server Developer (free) or Azure SQL free tier. Ten slow queries on
a sample schema, each with: the query, the plan, the fix, the new time.

Topics to cover (pick 8-10): SARGability (function on a column kills the index),
covering vs key index, included columns, parameter sniffing, implicit conversion
(varchar vs nvarchar), avoiding `SELECT *`, `EXISTS` vs `IN` on large sets, statistics.

**Why it wins:** the word T-SQL appears in your profile next to a real repo. Done.

---

## Project 3 — `data-quality-ops`

The job says "monitor data quality and key data flows, find errors, identify root
causes". You already caught a silent data trap in real life. Make it a system.

**Contents:** SQL validation checks on a warehouse — null rate, row-count drift,
referential integrity, duplicate keys, orphaned FKs, freshness. Each check: pass/fail,
a sample of offending rows, a plain-English cause. A Streamlit page shows the last 30
days. Schedule it.

**Why it wins:** it is the "operational Data Analyst" half of these roles, in code, and
it reuses the automation strength you already have.

---

## Project 4 — reframe one existing repo (no new code)

Take `morrisons-market-intelligence` and add a top section: **"The SQL behind the
insight."** The CTEs, window functions and validations that produced each chart, with
timings. Same repo, now answers the SQL question instead of only the scraping one.

This is the cheapest win: a README section, no new build.

---

## Cheap profile fixes (do these today)

1. **Headline**: put "SQL · T-SQL · Python · Analytics" in the Upwork headline and the
   GitHub bio. Right now the first screen reads "scraping", which is the wrong match
   for SQL roles and the right match for scraping roles.
2. **Every analytics repo gets a `sql/` folder** with the queries used, even if the
   project is Python-first. Reviewers and the proposal engine both look for `.sql`.
3. **One legend line per README**: "Techniques: CTE, window functions, joins at grain,
   EXPLAIN tuning". Present for search, and for the writer to cite.
4. **Do not claim 5+ years** unless true. The panel flags it and clients check.

---

## Priority order

1. `sql-analytics-lab` (surface + tuning) — biggest return, least new work.
2. `tsql-performance-lab` — closes the only zero-evidence requirement.
3. Reframe `morrisons` README — nearly free.
4. `data-quality-ops` — strongest "operational analyst" story.
5. Profile headline + `sql/` folders — five minutes each.

After 1 and 2, add the repo to `skills/upwork-proposal/references/portfolio.md` under
a new SQL row and add the positioning line. Then the engine cites real proof on SQL
briefs and the panel stops scoring Credibility at 6.

---

## Honest note

For SQL-heavy full-time roles, even with these repos you are competing against career
analysts with years inside companies. Your edge is the rare combination: **extraction
at scale + automation + SQL + analysis**. Bid on roles that want that combination
(small teams, data-heavy startups, "one person who can get the data and analyse it"),
not on pure "Excel and dashboards" analyst roles. Lead with the combination.
