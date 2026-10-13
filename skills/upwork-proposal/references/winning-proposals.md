# The Winning Proposal Corpus

Every entry below is a **pattern** drawn from Sandi's real, checkable work, annotated the same way as the original corpus: the brief, the shape of what was sent, and the extractable move. As real jobs are won, replace a pattern with the actual proposal and the outcome.

**How to use this file.** Find the closest job type, steal the *move*, not the words. If a client ever received one of these, sending it again is a liability. Read the final section before finalizing anything.

## Contents

1. The site is impossible (anti-bot, small fixed-price)
2. The numbers can't be trusted (analysis)
3. It has to run itself (pipeline)
4. It's a mobile app, everyone says no (anti-bot, technical buyer)
5. Measure coverage, don't promise volume (lead gen / market intel)
6. The server just closes the connection (government / TLS)
7. What every winner has in common
8. The four failure patterns to avoid
9. Final rules

---

## 1. The site is impossible (anti-bot, small fixed-price)

**Brief.** "Need a scraper for [site]. I tried Scrapy and a couple of freelancers but we keep getting blocked. Cloudflare. 20,000 products."

**Shape of what was sent.**
> Blocked usually means attacking the watched door. Most of these sites leave one path open, and it's often the one the page itself calls for its own data. On a hotel search API I worked, one endpoint answered a 202 challenge while the same endpoint with a trailing slash answered 200. Same data, different door. Send me one URL and I'll map which paths are open on yours, free, before you spend anything. What's the site?

**The move.** The trailing-slash detail. It is so specific that the client knows instantly this is not copy-paste. Nobody who has not done it says it. It also reframes "I'm blocked" (hopeless) into "there's a door" (solvable), then hands them a free first step that costs almost nothing.

---

## 2. The numbers can't be trusted (analysis)

**Brief.** "I have a dataset and need a report/dashboard my team can trust. The last guy's numbers looked wrong."

**Shape of what was sent.**
> Before I chart anything, I check whether the columns mean what they're named. On a grocery set the visible price column was the "Was" price, and the real price was buried in a text field. Trusting the column would have overstated every number in the report, and the client would have caught it, not me. So my first pass is an audit. What's actually in each field, what's missing, what's lying. What's the source of the data and how was it collected?

**The move.** Name the risk the client did not know they had, then offer to catch it first. It proves the work is about correctness before beauty, which is the client's unspoken fear.

---

## 3. It has to run itself (pipeline, ongoing relationship)

**Brief.** "We need this workflow automated and running without us babysitting it."

**Shape of what was sent.**
> The hard part isn't the first run, it's month three when the site renames a field and nobody notices the reports are wrong. So I build for that. My pipelines alert on failure, keep an error code per failure class, and log the reason instead of silently falling back. One I run now does 7 sources into enrichment into a database into routing into a daily digest, with 302 tests and zero errors over weeks of uptime. What breaks most often for you today, the fetch or the hand-off to your team?

**The move.** Kill the "it'll break at 3am and I won't know" fear. The 302-tests figure is the single credibility line, placed mid-proposal. The closing question targets the client's actual pain.

---

## 4. It's a mobile app, everyone says no (anti-bot, technical buyer)

**Brief.** "Can you get data from this mobile app? Everyone says it's not possible."

**Shape of what was sent.**
> Mobile apps are a different problem from websites. There's no JavaScript sensor to get past. Every request is signed, and if the signature is wrong the server just ignores you. I've reproduced those signatures in Python before, on a major short-video app, and pulled around 20,000 records at about 590 requests a minute on under 1% CPU. No browser farm. What's the app, and is it Android or iOS?

**The move.** Name the *class* of anti-bot correctly (signature, not sensor). A technical buyer can tell within one sentence whether the person knows the work. "Everyone says it's not possible" plus a confident, accurate reclassification is the whole play.

---

## 5. Measure coverage, don't promise volume (lead gen / market intel)

**Brief.** "I need competitor pricing / leads scraped from [source]."

**Shape of what was sent.**
> The trap with competitor data is coverage. I've measured a source that looked fully scrapable and found one collection path only reached about 14% of listings, and the listings rotated between requests. If you build on that path you get a confident, wrong answer. So before quoting volume, I measure coverage. How much of the real catalogue any given path can actually reach. What's the source, and roughly how many products are we talking about?

**The move.** A free measurement offer, disguised as expertise. It turns "can I trust this quote?" into "let's find out together, cheaply", and it pre-empts the refund fight before it starts.

---

## 6. The server just closes the connection (government / TLS)

**Brief.** "Government site. Our developer says it's impossible, the connection just dies."

**Shape of what was sent.**
> The connection dying before any response is usually a fingerprint check at the TLS handshake, not a normal block. The server is looking at the shape of the ClientHello and dropping anything that isn't a browser. That's fixable. I pulled 56,000 cases off a court site that does exactly this, and it never returned a 403 because the connection never got that far. Which site is it, and has anyone tried with a browser fingerprint yet?

**The move.** Reclassify the symptom precisely. "Connection dies" sounds unfixable and hopeless; "fingerprint check at the handshake" sounds like a Tuesday. Then anchor it with one real number and ask the one question that scopes the job.

---

## 7. What every winner has in common

Six elements. Aim for all six on jobs worth the effort.

1. **Personalization.** Client's name. Client's own vocabulary mirrored back. Client's actual URL or asset referenced.
2. **Their pain restated in your words.** Not "I can do this." Instead, here is what is wrong and what it is costing you.
3. **Specific deliverables, not adjectives.** Map the paths, measure coverage, ship a CSV. Not "reliable, high-quality scraping".
4. **Confidence without overselling.** "That's exactly what I do." "I specialize in." No superlatives, no begging.
5. **Risk reduction.** A free sample, a mini audit, one measured endpoint, one checked column. This is the single highest-converting element in the entire corpus.
6. **A closing question the client can answer in one line.** Never "looking forward to hearing from you."

Plus one meta-pattern: **tone flexes with budget.** Three lines on a $45 fix. Storytelling on a platform build. Read the money and match the register.

---

## 8. The four failure patterns to avoid

1. **Soft openers.** "I'm interested in helping you with your scraping project" is dead on arrival. Replace with an observation, a consequence, or the client's own words. Compare: "Blocked usually means attacking the wrong door."
2. **Portfolio links without context.** A bare repo URL asks the client to do the work of understanding it. Give the link one line: what was hard, what was proved.
3. **Passive calls to action.** "Let me know" puts the burden on them. Use "Send me one URL and I'll check tonight, free." or "What's the source, and roughly what volume?"
4. **No results named.** Every proposal says what will be done. Almost none say what happened last time. Add a number when a real one exists. Never invent one.

---

## 9. Final rules

- **Steal the move, never the sentence.** These exact shapes have been sent. Reusing them across clients is how a portfolio of wins turns into a template.
- **The failure mode goes in line one.** Everything after it is evidence.
- **The one true observation beats the credibility line.** If you can only do one thing, make it true and specific about *their* problem.
