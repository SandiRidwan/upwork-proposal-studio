# Winning Proposals (annotated corpus)

> The rule from the reference skill, kept exactly: **steal the *move*, never the
> sentence.** Reusing an identical proposal across clients is a failure mode, not a
> shortcut.
>
> Each entry below is a **pattern** extracted from Sandi's real capability stories.
> The "move that did the work" is annotated. As you win real jobs, add the actual
> proposal here with a note on which move landed — the file's value scales with how
> specific and real the entries are.

---

### Entry 1 — The unguarded door (anti-bot, small fixed-price job)

**Brief shape:** "Need a scraper for [site], I tried Scrapy/Selenium and got blocked."

**Proposal:**
> Blocked usually means attacking the watched door. Most of these sites leave one path
> open, and it's often the one the page itself calls for its own data. On a hotel site
> I worked, the search endpoint answered a 202 challenge while the same endpoint with a
> trailing slash answered 200. Same data, different door. Send me one URL and I'll map
> which paths are open on yours, free, before you spend anything. What's the site?

**Move that did the work:** Move 2 — the trailing-slash detail. It's so specific that
the client knows instantly this isn't a copy-paste. Nobody who hasn't done it says it.

**Why it works:** It reframes "I'm blocked" (hopeless) into "there's a door" (solvable),
then hands them a free first step that costs the freelancer almost nothing.

---

### Entry 2 — The trust problem (data analysis, mid-size job)

**Brief shape:** "I have a dataset and need a report/dashboard my team can trust."

**Proposal:**
> Before I chart anything, I check whether the columns mean what they're named. On a
> grocery set the visible price column was the "Was" price, and the real price was
> buried in a text field. Trusting the column would have overstated every number in the
> report, and the client would have caught it, not me. So my first pass is an audit:
> what's actually in each field, what's missing, what's lying. What's the source of the
> data and how was it collected?

**Move that did the work:** Move 2 again — the "Was" price trap. It proves the freelancer
thinks about correctness before beauty, which is exactly the client's unspoken fear.

**Why it works:** It names the risk the client didn't know they had, then offers to catch
it first. Closing question gathers real information (source + collection method).

---

### Entry 3 — The pipeline that runs itself (automation, ongoing relationship)

**Brief shape:** "We need this workflow automated and running without us babysitting it."

**Proposal:**
> The hard part isn't the first run, it's month three when the site changes a field name
> and nobody notices the reports are wrong. So I build for that. My pipelines alert on
> failure, keep an error code per failure class, and log the reason instead of silently
> falling back. One I run now does 7 sources -> enrichment -> database -> routing ->
> a daily digest, with 302 tests and zero errors over weeks of uptime. What breaks most
> often for you today, the fetch or the hand-off to your team?

**Move that did the work:** Move 4 — killing the "it'll break at 3am and I won't know"
fear. The 302-tests figure is the single credibility line, placed mid-proposal.

**Why it works:** It answers the real question behind "automate this" (will it stay
automated?), and the closing question targets the client's actual pain.

---

### Entry 4 — The impossible mobile app (anti-bot, technical buyer)

**Brief shape:** "Can you get data from this mobile app? Everyone says it's not possible."

**Proposal:**
> Mobile apps are a different problem from websites. There's no JavaScript sensor to
> get past. Instead every request is signed, and if the signature is wrong the server
> just ignores you. I've reproduced those signatures in Python before, on a major
> short-video app, and pulled around 20,000 records at ~590 requests a minute on under
> 1% CPU. No browser farm. What's the app, and is it Android or iOS?

**Move that did the work:** Move 2 — naming the *class* of anti-bot correctly (signature,
not sensor). A technical buyer can tell within one sentence whether the person knows
what they're talking about.

**Why it works:** "Everyone says it's not possible" + a confident, accurate
reclassification. The closing question scopes the next step immediately.

---

### Entry 5 — The free mini-audit (lead gen / market intel, competitive)

**Brief shape:** "I need competitor pricing / leads scraped from [source]."

**Proposal:**
> The trap with competitor data is coverage. I've measured a source that looked fully
> scrapable and found one collection path only reached about 14% of listings, and the
> listings rotated between requests. If you build on that path you get a confident,
> wrong answer. So before quoting volume, I measure coverage: how many of the real
> catalogue any given path can actually reach. What's the source, and roughly how many
> products are we talking about?

**Move that did the work:** Move 4 — the free measurement offer, disguised as expertise.
It turns "can I trust this quote?" into "let's find out together, cheaply".

**Why it works:** It pre-empts the refund/scope fight before it starts, and the closing
question gets the two numbers needed to quote honestly.

---

## The five moves (reference card)

1. **Open on their failure mode**, in their words. No greeting. Never credentials.
2. **Prove domain knowledge with one precise technical detail** only an insider would say.
3. **Land exactly one credibility line**, mid-proposal. Never the opener.
4. **Kill the hiring risk** — free sample, mini-audit, one redesigned panel.
5. **Close with a scoped, easy-to-answer question.** Never a sign-off.

## What made every entry work

- It never praised the client.
- It never listed skills.
- It named a risk the client didn't know they had.
- It offered something free and specific.
- It ended with a question that took 10 seconds to answer.
