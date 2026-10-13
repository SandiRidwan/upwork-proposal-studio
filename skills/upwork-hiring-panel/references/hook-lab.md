# Hook lab: test the preview until clients open it

The first two lines decide whether the proposal is ever opened, and a single model score is easy to fool (one panel gave 8/10 to a clever opener that real clients skipped). So the hook is tested two ways, with The Scroller only, and iterated until it wins.

## The loop

1. **Write 4 or 5 hook candidates** (each the first two lines, about 200 characters), all from the proof bank. Vary one idea per candidate: which proof leads, whether the client's own words are used, where the stack or method goes, whether "one URL and I'll check tonight" is promised. Keep the best candidate from the last round in the next round.
2. **Solo test**: one fresh Scroller sub-agent per candidate, in parallel, with the brief from `personas.md` (job title plus the first lines of the job post, the profile card, and only that candidate's preview).
3. **Blind lineup**: one more Scroller sub-agent sees all candidates mixed with 6 competitor previews, unlabelled and shuffled, and picks the 5 it would open, ranked, with a 3-word reason for each skip. Use the lineup brief below.
4. **Keep score** in a table: candidate, solo verdict and score, lineup rank (or "skipped" and why).
5. **Read the reasons, not just the numbers.** Every reviewer usually asks for the same missing thing. Write the next round to answer it, using true facts only.
6. **Stop** when a candidate scores **9 or 10 solo AND ranks in the top 2 of the lineup** (where only a competitor who has already solved the exact same problem may rank above it). Also stop after **3 rounds**, or when two rounds in a row gain nothing. The ceiling is information too: report it honestly.

Run at most 3 rounds by default (about 18 short sub-agent calls). Show the user the score table after every round.

## Competitor previews for the lineup

Write 6 previews for this job, one of each type, so the lineup looks like a real proposal list:

1. **The specialist**: has already solved this exact kind of problem on this stack, with a repo or demo. (Usually ranks #1. If it does, no wording beats it; only proof does.)
2. **The near-match**: solved several similar problems on a neighbouring stack, with links.
3. **The template**: "Hello Dear, I am a senior … with 8+ years … I have carefully read your job description …"
4. **The skill list**: a list of technologies and "can start immediately".
5. **The consultant**: an analysis of the client's problem with no proof.
6. **The enthusiast**: emoji, "I'd love to help bring your … to life", no real projects.

Keep the same 6 competitors across rounds so ranks are comparable.

## Lineup brief (copy word for word, then append the job and the lettered previews)

> You posted a job on Upwork three hours ago and already have 40+ proposals. You are on your phone between meetings. In the proposal list Upwork shows you each freelancer's photo, name, title, rate, Job Success Score and the first two lines of their cover letter. That is all you see. You give each one three seconds and click on maybe five. You are not a writing critic and clever lines do not impress you. You click when the card and line one tell you this person has already done work like yours (your kind of target, your words, your stack) and there is something you can check. You skip when the title on the card does not match your job, when line one is about the freelancer in general (years of experience, a list of skills) without naming your kind of work, or when line one is an analysis of your project with no sign they have done one. A short "Hi," does not bother you.
>
> Below are proposal previews from different freelancers (profile cards not shown). Pick exactly the 5 you would open, ranked 1 to 5, and say in one short line why for each. Then list the others and a 3-word reason each was skipped.
>
> Shared rules: Stay in character. Be blunt and specific. Judge like a real Upwork client, not like a writing critic: real clients skim, and they reward a clear match to their kind of work and proof they can check (live repos, demos, real numbers) far more than clever analysis, long plans or polished prose. Do not reward length. Do not use any tools; just answer.

Answer format:
```
OPEN (ranked):
1. <letter>: reason
...
5. <letter>: reason
SKIPPED:
<letter>: reason
```

## Honesty rules

- Every candidate uses only facts from the proof bank. Never imply a matching project, feature or link the freelancer does not have.
- A **hypothetical** candidate (for example "I mapped three of your endpoints already: [link]") may be tested to show the user what a piece of proof would be worth. Label it HYPOTHETICAL in every table, and never put it in the paste-ready proposal unless the user confirms they did it.
- If the best honest hook plateaus below the target, say so, give its score and rank, and name the one piece of proof that would break the ceiling.

## What the lab has found so far

Patterns that repeat across technical jobs:

| Hook idea | Solo | Lineup |
|---|---|---|
| "I'm a web scraping expert with 4 years of experience in Python and Selenium." | SKIP 3 | skipped: "generic, no target named" |
| "I can scrape any website and deliver high-quality data on time." | SKIP 4 | skipped: "unprovable, no proof" |
| "Cloudflare blocking you usually means the wrong path, not a real wall." | OPEN 8 | #3 |
| "Blocked usually means attacking the watched door. Send one URL, I'll map which paths are open, free tonight." | **OPEN 9** | **#2** (best honest) |
| HYPOTHETICAL: "I checked your site on my own time: three endpoints, one unguarded. [short demo]…" | **OPEN 9** | **#1** |

Lessons:
1. **Name the client's problem in the first words, not yourself.** "Cloudflare blocking you usually means…" beat "I'm a scraping expert and I've built…".
2. **Use the client's own words** (Cloudflare, blocked, 403) so the match is obvious.
3. **Promise something checkable**: hooks ending "send one URL and I'll map it tonight, free" ranked; the same hook without it was skipped.
4. **Do not spend the preview on a credential** (years, project count) or on a claim that you "fit".
5. **When you lack the exact target experience, a measured first pass on their actual target is the strongest lever**, stronger than any wording. If the job is worth it, do the pass; otherwise pick jobs where your proof already matches.
6. **The specialist always wins the lineup.** No hook beats a competitor who has already solved the exact problem; choose jobs accordingly.
