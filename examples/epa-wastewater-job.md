# Job post — EPA wastewater plants (real Upwork brief)

Use this to test the skills (in opencode via `/upwork-proposal`, or through the
engine). It is a real public-sector data job: EPA Envirofacts + ECHO, US census,
maps, ETL. Notes at the bottom show what a good result looks like.

---

Summary: Using EPA databases (Envirofacts, ECHO, etc.) identify wastewater treatment
plants in the US and extract data such as state, city, discharge location and permit
limits. Be able to create lists of plants that meet certain criteria. Be able to cross
reference EPA data with US census data. Be able to create maps of US and individual
states showing locations of plants in each category. The task requires proficiency in
data extraction and environmental science. The ideal candidate will have experience
with data mining and data scraping, and be able to work with Python and ETL processes.

---

## What a good result looks like

- **Niche:** data analysis (C), not anti-bot. "scraping" and "extract" appear, but the
  target is public APIs, so the anti-bot keyword must not win.
- **Failure mode:** the join, not the fetch. Records live in separate sources with
  different keys.
- **The insider detail (move 2):** naming the real join problem — NPDES permit IDs and
  registry IDs in EPA vs census tracts / block groups — and entity resolution before
  any list or map. That single detail is what proves competence here.
- **Proof:** the Morrisons market-intelligence repo is the closest match (a data trap
  caught before it reached the client, then a dashboard).
- **Risk-kill (move 4):** a free mini-audit on one state — resolve the IDs, show how
  many plants survive the join and how many quietly fall out.
- **Close (move 5):** which permit parameters decide a category, and one national map
  or a per-state set.
