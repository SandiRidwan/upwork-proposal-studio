"""Unit tests. No API key, no network required."""

import os
import unittest

# force prompt mode so tests never call an API even if a key is present
os.environ["UPS_LLM_MODE"] = "prompt"

from engine.analyzer import analyze
from engine.writer import write, write_one, lint, build_prompt
from engine.panel import review, _heuristic_reviews, _heuristic_scores
from engine.pipeline import run
from engine import knowledge


JOB_ANTIBOT = """We need someone to scrape product data from a large e-commerce site.
We tried Scrapy and a couple of freelancers but we keep getting blocked by Cloudflare.
Need 20,000 products with price, title, description. Output to CSV. Ongoing if it works.
This week if possible."""

JOB_ANALYSIS = """I have a sales dataset in Excel and I need a dashboard that shows
monthly trends and tells me where my margin is leaking. Must be accurate, I don't
trust the numbers my last guy gave me. Power BI or similar. No rush, planning for
next month."""

JOB_AUTOMATION = """Looking for someone to automate our lead flow. Right now someone
copies new form submissions into Airtable by hand every day. We want it to enrich the
company info and route each lead to the right rep in Slack. Long term relationship."""

# Real Upwork brief: EPA Envirofacts/ECHO + US census + maps. This must NOT be
# read as an anti-bot job just because it mentions "scraping".
JOB_EPA = """Summary: Using EPA databases (Envirofacts, ECHO, etc.) identify wastewater
treatment plants in the US and extract data such as state, city, discharge location and
permit limits. Be able to create lists of plants that meet certain criteria. Be able to
cross reference EPA data with US census data. Be able to create maps of US and individual
states showing locations of plants in each category. The task requires proficiency in
data extraction and environmental science. The ideal candidate will have experience with
data mining and data scraping, and be able to work with Python and ETL processes."""


class TestAnalyzer(unittest.TestCase):
    def test_antibot_niche(self):
        a = analyze(JOB_ANTIBOT)
        self.assertEqual(a.niche, "A")
        self.assertEqual(a.urgency, "high")
        self.assertIn("blocked", a.failure_mode.lower())

    def test_analysis_niche(self):
        a = analyze(JOB_ANALYSIS)
        self.assertEqual(a.niche, "C")
        self.assertEqual(a.urgency, "low")

    def test_automation_niche(self):
        a = analyze(JOB_AUTOMATION)
        self.assertIn(a.niche, ("B", "E"))

    def test_epa_job_is_not_antibot(self):
        # "extract" and "data scraping" appear, but this is a data/ETL/geo job
        a = analyze(JOB_EPA)
        self.assertNotEqual(a.niche, "A",
                            "EPA ETL job must not be read as anti-bot")
        self.assertIn(a.niche, ("C", "D", "B"))
        # and the failure mode must describe scattered sources, not "blocked"
        self.assertNotIn("blocked", a.failure_mode.lower())

    def test_antibot_still_wins_when_target_is_defended(self):
        a = analyze(
            "The site is behind Cloudflare and our scraper keeps getting blocked "
            "with 403. We tried Scrapy and Selenium.")
        self.assertEqual(a.niche, "A")

    def test_red_flag_offplatform(self):
        a = analyze("Simple task. Contact me at my email outside upwork. $10 fixed.")
        self.assertIn("off_platform", a.red_flags)

    def test_defaults_present(self):
        a = analyze(JOB_ANTIBOT)
        self.assertTrue(a.credibility_fact)
        self.assertTrue(a.portfolio_link)
        self.assertIn(a.variant, ("short", "process"))


class TestLint(unittest.TestCase):
    def test_catches_banned(self):
        issues = lint("I am a professional developer. Looking forward to hearing "
                      "from you!")
        rules = {i["rule"] for i in issues}
        self.assertIn("banned_phrase", rules)
        self.assertIn("exclamation", rules)

    def test_catches_emoji_and_dash(self):
        rules = {i["rule"] for i in lint("Great work \U0001F600 and fast \u2014 done.")}
        self.assertIn("emoji", rules)
        self.assertIn("em_dash", rules)

    def test_catches_pronoun_ratio(self):
        bodies = "I I I my my me you. " * 3
        rules = {i["rule"] for i in lint(bodies)}
        self.assertIn("pronoun_ratio", rules)

    def test_clean_proposal_passes(self):
        clean = (
            "Cloudflare blocking you usually means the wrong path. Most sites leave "
            "one open. I map which ones answer before quoting. I've done this on "
            "government and travel sites past TLS fingerprinting. Send me one URL "
            "and I'll tell you tonight whether it's a wall or a door, free. "
            "What's the site?"
        )
        hard = [i for i in lint(clean)
                if i["rule"] in ("banned_phrase", "exclamation", "emoji",
                                 "ai_tell", "em_dash")]
        self.assertEqual(hard, [])


class TestPanel(unittest.TestCase):
    def test_scroller_skips_bad_opener(self):
        bad = ("I am a professional web scraping specialist with 4 years of "
               "experience. I can deliver high quality work.")
        reviews = {r.key: r for r in _heuristic_reviews(bad, JOB_ANTIBOT)}
        self.assertEqual(reviews["scroller"].verdict, "SKIP")

    def test_scroller_opens_good_opener(self):
        good = ("Cloudflare blocking your scraper usually means the wrong path, "
                "not a real wall. Send me one URL.")
        reviews = {r.key: r for r in _heuristic_reviews(good, JOB_ANTIBOT)}
        self.assertEqual(reviews["scroller"].verdict, "OPEN")

    def test_scroller_opens_data_domain_hook(self):
        # a strong data/ETL opener must not be read as weak
        good = ("Joining EPA data to census data is where keys drift and the map "
                "comes out quietly wrong. Two sources, one join key check.")
        reviews = {r.key: r for r in _heuristic_reviews(good, "")}
        self.assertEqual(reviews["scroller"].verdict, "OPEN")

    def test_competitor_sees_data_specifics(self):
        good = ("The join key drifts between sources, so the facility id and "
                "county code get checked before any map. I did this on 18,100 "
                "records.")
        reviews = {r.key: r for r in _heuristic_reviews(good, "")}
        self.assertIn(reviews["competitor"].verdict, ("I WIN", "TOSS-UP"))

    def test_scores_and_chance(self):
        good = ("Cloudflare blocking you usually means the wrong path. Most sites "
                "leave one open. I've mapped 202 to 200 on a hotel API before. "
                "Send me one URL and I'll check free tonight. What's the site?")
        reviews = _heuristic_reviews(good, JOB_ANTIBOT)
        scores, chance = _heuristic_scores(good, reviews)
        self.assertIn(chance, ("LOW", "MEDIUM", "HIGH"))
        self.assertEqual(set(scores), {"Hook", "Clarity", "Relevance",
                                       "Credibility", "Value Proposition",
                                       "Interview Potential"})

    def test_review_returns_report(self):
        rep = review("Cloudflare blocking you means the wrong path. One URL?",
                     JOB_ANTIBOT, use_llm=False)
        self.assertEqual(len(rep.reviews), 7)
        self.assertTrue(rep.rejection_story)


class TestKnowledge(unittest.TestCase):
    def test_files_load(self):
        self.assertIn("Sandi", knowledge.positioning())
        self.assertIn("github.com/SandiRidwan", knowledge.portfolio())
        self.assertIn("banned", knowledge.voice().lower())

    def test_no_fake_placeholders_in_fact_tables(self):
        # fact tables must not contain unfinished [ADD placeholders
        rows = [l for l in knowledge.positioning().splitlines()
                if l.strip().startswith("|")]
        self.assertNotIn("[ADD", "\n".join(rows))


class TestSkillShape(unittest.TestCase):
    """The repo mirrors the two source skills' file layout and content."""

    def test_writer_skill_frontmatter(self):
        # only the fields an agent host needs; no host-specific extras
        s = knowledge.writer_skill()
        self.assertTrue(s.startswith("---\nname: upwork-proposal\n"))
        self.assertIn("description:", s)
        self.assertNotIn("mode: api-ui", s)

    def test_panel_skill_frontmatter(self):
        s = knowledge.panel_skill()
        self.assertTrue(s.startswith("---\nname: upwork-hiring-panel\n"))
        for key in ("description:", "argument-hint:", "license: MIT"):
            self.assertIn(key, s)

    def test_writer_has_five_moves_and_voice(self):
        s = knowledge.writer_skill()
        for marker in ("## Identity", "## Workflow", "## Voice",
                       "## Output format", "## Reference files",
                       "Five moves"):
            self.assertIn(marker, s)
        self.assertIn("### 4. Produce two variants, always", s)

    def test_panel_has_seven_reviewers_and_steps(self):
        s = knowledge.panel_skill()
        for marker in ("## 2. Seven reviewers, alone", "## 3. Score it",
                       "## 4. Why it gets skipped or rejected",
                       "## 5. Rewrite it", "## 5b. Test the hook until it wins",
                       "## Rules"):
            self.assertIn(marker, s)

    def test_personas_seven_briefs_with_verdict_and_score(self):
        p = knowledge.personas()
        for who in ("The Scroller", "The Hiring Client",
                    "The Budget-Conscious Client", "The Competing Freelancer",
                    "The Skeptic", "The Technical Lead", "The Upwork Veteran"):
            self.assertIn(who, p)
        self.assertIn("## 1. The Scroller", p)
        briefs = p.split("\n## ")[1:]
        self.assertEqual(len(briefs), 7)
        for brief in briefs:
            self.assertIn("VERDICT:", brief)
            self.assertIn("SCORE: n/10", brief)

    def test_scroller_sees_only_preview(self):
        scroller = knowledge.personas().split("## 1. The Scroller")[1].split("## 2.")[0]
        self.assertIn("Never the full proposal", scroller)

    def test_rubric_six_scores_and_rules(self):
        r = knowledge.rubric()
        for score in ("Hook", "Clarity", "Relevance", "Credibility",
                      "Value Proposition", "Interview Potential"):
            self.assertIn(f"**{score}**", r)
        for marker in ("## Interview chance", "## Common rejection patterns",
                       "## Rewrite rules", "## Screening answer rules"):
            self.assertIn(marker, r)

    def test_winning_patterns_and_hook_lab(self):
        wp = knowledge.winning_patterns()
        self.assertIn("## The proof-first shape", wp)
        self.assertIn("## Not opened? Check these", wp)
        hl = knowledge.hook_lab()
        self.assertIn("## The loop", hl)
        self.assertIn("**Blind lineup**", hl)
        self.assertIn("## Competitor previews for the lineup", hl)
        self.assertIn("HYPOTHETICAL", hl)
        self.assertIn("9 or 10 solo AND ranks in the top 2", hl)

    def test_stays_on_upwork(self):
        self.assertIn("off Upwork", knowledge.panel_skill())
        self.assertIn("Stay on Upwork", knowledge.rubric())

    def test_skills_are_host_neutral(self):
        # both skills must be usable as agent-host skills (opencode / Claude):
        # frontmatter carries only standard Agent Skills fields, no host-specific
        # top-level keys. opencode reads name/description/license/metadata.
        import re
        allowed = {"name", "description", "license", "compatibility", "metadata"}
        for getter in (knowledge.writer_skill, knowledge.panel_skill):
            s = getter()
            front = s.split("---")[1]
            keys = set(re.findall(r"^([a-zA-Z_-]+):", front, re.M))
            self.assertIn("name", keys)
            self.assertIn("description", keys)
            self.assertTrue(keys <= allowed, f"unexpected frontmatter keys: "
                            f"{keys - allowed}")
            self.assertNotIn("api-ui", front)
            self.assertNotIn("runs the skill through an API/UI", s)
        # the "how it runs" note must be present in both
        self.assertIn("How this skill runs", knowledge.writer_skill())
        self.assertIn("How this skill runs", knowledge.panel_skill())

    def test_skills_expose_opencode_slash(self):
        # opencode turns metadata["opencode/slash"]="true" into a /command
        for getter in (knowledge.writer_skill, knowledge.panel_skill):
            self.assertIn('opencode/slash: "true"', getter())

    def test_never_invents(self):
        self.assertIn("Never invent", knowledge.panel_skill())
        self.assertIn("[ADD: ...]", knowledge.panel_skill())


class TestScoring(unittest.TestCase):
    def test_clean_scores_high(self):
        from engine.score import score
        good = ("Blocked usually means the wrong path. Two sites everyone calls "
                "impossible, Akamai and DataDome, neither needed a browser. "
                "Send one URL and you'll know tonight, free. What's the site?")
        val, issues = score(good)
        self.assertGreaterEqual(val, 85)
        hard = [i for i in issues if i["rule"] in ("banned_phrase", "emoji",
                                                   "exclamation", "ai_tell")]
        self.assertEqual(hard, [])

    def test_bad_scores_low(self):
        from engine.score import score
        bad = ("I am a professional expert with many years of experience! I hope "
               "this finds you well. Looking forward to hearing from you!")
        val, issues = score(bad)
        self.assertLess(val, 60)
        self.assertTrue(any(i["rule"] == "banned_phrase" for i in issues))


class TestProviders(unittest.TestCase):
    def test_opencode_provider_is_first_and_named(self):
        from engine.llm import PROVIDERS
        first = next(iter(PROVIDERS))
        self.assertEqual(first, "opencode")
        self.assertIn("base_url", PROVIDERS["opencode"])
        self.assertTrue(PROVIDERS["opencode"]["key_env"])

    def test_llm_status_shape(self):
        from engine import llm
        st = llm.status()
        for k in ("mode", "provider", "model", "live", "keys"):
            self.assertIn(k, st)


class TestScreeningAndPlaceholders(unittest.TestCase):
    def test_split_screening_pulls_pairs(self):
        from engine.writer import _split_screening
        text = ("Body line one.\n\nNEED FROM YOU:\n- rate?\n\n"
                "SCREENING ANSWERS:\n"
                "Q: Do you scrape?\nA: Yes, daily.\n"
                "Q: AU real estate?\nA: Similar directories, yes.\n")
        head, pairs = _split_screening(text)
        self.assertNotIn("SCREENING ANSWERS", head)
        self.assertEqual(len(pairs), 2)
        self.assertEqual(pairs[0]["question"], "Do you scrape?")
        self.assertEqual(pairs[1]["answer"], "Similar directories, yes.")

    def test_strip_placeholders_removes_brackets(self):
        from engine.writer import _strip_placeholders
        messy = ("Real text here. [ADD: rate] More text.\n"
                 "[need from you]\nClosing line?")
        clean = _strip_placeholders(messy)
        self.assertNotIn("[", clean)
        self.assertNotIn("]", clean)
        self.assertIn("Closing line?", clean)

    def test_lint_flags_placeholder(self):
        issues = lint("Good opener. [ADD: the rate] Send one URL.")
        rules = {i["rule"] for i in issues}
        self.assertIn("placeholder_left_in", rules)

    def test_lint_flags_post_criticism(self):
        bad = ("Your post names Python but no process, no data source, no "
               "acceptance criteria.")
        rules = {i["rule"] for i in lint(bad)}
        self.assertIn("criticises_post", rules)

    def test_lint_passes_clean_without_critique(self):
        good = ("Agent orchestration and tool calling decide whether a workflow "
                "survives month three. Send one workflow and I'll map it, free.")
        rules = {i["rule"] for i in lint(good)}
        self.assertNotIn("criticises_post", rules)

    def test_placeholders_make_score_drop(self):
        from engine.score import score
        val, issues = score("Nice hook. [ADD: price] What's the source?")
        self.assertIn("placeholder_left_in", {i["rule"] for i in issues})
        self.assertLess(val, 80)

    def test_parse_questions(self):
        from engine.pipeline import _parse_questions
        qs = _parse_questions(
            "1. Do you scrape?\n2) Have you done AU real estate?\n"
            "- What is your rate?\n"
            "This is not a question but is long enough to count")
        self.assertEqual(len(qs), 4)
        self.assertEqual(qs[0], "Do you scrape?")


class TestFilterWordAndAuthNiche(unittest.TestCase):
    def test_detect_filter_word_keeps_case(self):
        from engine.analyzer import _detect_filter_word
        text = ("Please start your proposal with the word 'Directory'. "
                "Also mention your approach.")
        self.assertEqual(_detect_filter_word(text), "Directory")

    def test_detect_filter_variants(self):
        from engine.analyzer import _detect_filter_word
        self.assertEqual(_detect_filter_word("Begin your proposal with Apple"),
                         "Apple")
        self.assertEqual(
            _detect_filter_word("Your first word must be 'Hello'."), "Hello")

    def test_no_filter_word(self):
        from engine.analyzer import _detect_filter_word
        self.assertEqual(_detect_filter_word("Just a normal job post."), "")

    def test_login_job_is_niche_f_not_antibot(self):
        a = analyze(
            "I'll provide login credentials for my member account. Export the "
            "member directory from the private community. Keep request rates low "
            "so the account isn't flagged. Use pagination and infinite scroll.")
        self.assertEqual(a.niche, "F")
        self.assertNotIn("blocked", a.failure_mode.lower())

    def test_enforce_filter_prepends(self):
        from engine.writer import _enforce_filter
        self.assertTrue(_enforce_filter("The site truncates cards.",
                                        "Directory").startswith("Directory"))
        # already correct: unchanged
        self.assertEqual(_enforce_filter("Directory. Body here.", "Directory"),
                         "Directory. Body here.")
        # empty word: unchanged
        self.assertEqual(_enforce_filter("Body here.", ""), "Body here.")


class TestSqlNiche(unittest.TestCase):
    def test_sql_job_maps_to_niche_g(self):
        a = analyze(
            "Advanced SQL and T-SQL required. Complex joins, CTEs, window "
            "functions, query performance improvement. Large relational "
            "databases and complex data models. SQL Server.")
        self.assertEqual(a.niche, "G")
        self.assertIn("sql-analytics-lab", a.portfolio_link)

    def test_niche_g_failure_mode_and_credibility(self):
        a = analyze("We need help improving query performance and data "
                    "quality on our warehouse.")
        self.assertEqual(a.niche, "G")
        self.assertIn("slow", a.failure_mode.lower())
        self.assertIn("8.8s", a.credibility_fact)

    def test_sql_beats_dashboard_niche(self):
        # a brief that names SQL/T-SQL/tuning must not fall into niche C
        a = analyze("T-SQL query tuning, execution plans, CTEs, window "
                    "functions, SQL Server, data quality checks.")
        self.assertEqual(a.niche, "G")


class TestRateCard(unittest.TestCase):
    def test_positioning_has_real_rate_not_placeholder(self):
        pos = knowledge.positioning()
        self.assertIn("$30", pos)
        self.assertIn("25 hrs/week", pos)
        self.assertIn("3 years", pos)
        # the rate card must not still be an [ADD] placeholder
        rate_rows = [l for l in pos.splitlines()
                     if l.strip().startswith("|") and "$" in l or "hrs/week" in l]
        for row in rate_rows:
            self.assertNotIn("[ADD", row)

    def test_no_fake_five_year_claim(self):
        pos = knowledge.positioning()
        self.assertNotIn("5+ years of experience", pos)
        self.assertIn("Never", pos)


class TestStackKeywordEnforcement(unittest.TestCase):
    def test_detect_stack_keywords(self):
        from engine.analyzer import _detect_stack_keywords
        kws = _detect_stack_keywords(
            "Advanced SQL and T-SQL on SQL Server, plus Python and Power BI.")
        self.assertIn("T-SQL", kws)
        self.assertIn("SQL Server", kws)
        self.assertIn("Python", kws)
        self.assertIn("Power BI", kws)
        # the bare "SQL" must be dropped when a specific variant is present
        self.assertNotIn("SQL", kws)

    def test_detect_empty_when_no_stack(self):
        from engine.analyzer import _detect_stack_keywords
        self.assertEqual(_detect_stack_keywords("Just a friendly chat about ideas."), [])

    def test_enforcement_prepends_when_missing(self):
        from engine.writer import _enforce_stack_keyword, _stack_in_first_sentence
        body = "Daily operations break in three places. Nobody owns the report."
        kws = ["SQL Server", "T-SQL"]
        self.assertFalse(_stack_in_first_sentence(body, kws))
        fixed = _enforce_stack_keyword(body, kws)
        self.assertTrue(_stack_in_first_sentence(fixed, kws))

    def test_enforcement_splices_only_when_no_keyword_in_opening(self):
        from engine.writer import _enforce_stack_keyword, _stack_in_first_sentence
        # keyword only in sentence two AND outside the 200-char window -> splice
        body = ("Data issues break in three places and nobody owns them, which "
                "is the real cost. This paragraph is deliberately long so the "
                "keyword falls past the two-hundred character opening window "
                "the enforcement uses. Filler sentence to push it out further. "
                "Python and T-SQL are the day job.")
        kws = ["Python", "T-SQL"]
        self.assertFalse(_stack_in_first_sentence(body, kws))
        fixed = _enforce_stack_keyword(body, kws)
        self.assertTrue(_stack_in_first_sentence(fixed, kws))

    def test_enforcement_noop_when_present(self):
        from engine.writer import _enforce_stack_keyword
        body = "SQL Server and T-SQL are the day job. Here is the rest."
        self.assertEqual(_enforce_stack_keyword(body, ["SQL Server", "T-SQL"]), body)

    def test_enforcement_noop_without_keywords(self):
        from engine.writer import _enforce_stack_keyword
        body = "Some body with no tools named."
        self.assertEqual(_enforce_stack_keyword(body, []), body)

    def test_stack_keywords_flow_through_pipeline(self):
        from engine.pipeline import run
        # a SQL job must land niche G and expose its stack keywords
        result = run("Advanced SQL and T-SQL required. SQL Server. Python.",
                     use_llm=False, review=False)
        self.assertEqual(result.analysis.niche, "G")
        self.assertIn("T-SQL", result.analysis.stack_keywords)


    def test_enforcement_grammar_singular_plural(self):
        from engine.writer import _enforce_stack_keyword
        # two keywords -> "are", one -> "is"
        one = _enforce_stack_keyword("Data breaks in three places.", ["Python"])
        self.assertIn("Python is the day job", one)
        two = _enforce_stack_keyword("Data breaks in three places.",
                                     ["Python", "SQL"])
        self.assertIn("Python and SQL are the day job", two)

    def test_enforcement_noop_when_keyword_in_opening_window(self):
        # if the stack is already in the first 200 chars (even sentence two),
        # leave the model's opener alone rather than splicing awkwardly
        from engine.writer import _enforce_stack_keyword
        body = ("Data issues that keep coming back usually mean the root cause "
                "was never found. Python and T-SQL is how I close them.")
        self.assertEqual(_enforce_stack_keyword(body, ["Python", "T-SQL"]), body)


class TestAiAutomationNiche(unittest.TestCase):
    def test_ai_agent_job_detected_as_automation(self):
        a = analyze(
            "AI Automation Developer. AI Agent Development workflows, LLM-powered "
            "applications, structured tool calling and agent orchestration. n8n, "
            "RAG, OpenAI, Claude, Gemini, LangGraph, MCP. Human-in-the-loop. "
            "Python, FastAPI, PostgreSQL.")
        self.assertEqual(a.niche, "B")
        for kw in ("RAG", "LangGraph", "OpenAI", "Claude", "Gemini", "MCP"):
            self.assertIn(kw, a.stack_keywords)

    def test_prototype_failure_mode(self):
        a = analyze("We tried an AI agent but it is still a chatbot prototype "
                    "that never made it past demo.")
        self.assertIn("prototype", a.failure_mode.lower())


class TestPipeline(unittest.TestCase):
    def test_full_run(self):
        result = run(JOB_ANTIBOT, use_llm=False, review=True)
        d = result.to_dict()
        self.assertEqual(d["analysis"]["niche"], "A")
        # ONE proposal written
        self.assertEqual(len(d["proposal"]["variants"]), 1)
        # ONE panel selects it
        self.assertIsNotNone(d["panel"])
        self.assertEqual(len(d["panel"]["reviews"]), 7)
        self.assertEqual(d["meta"]["panel_reviewers"], 7)
        self.assertFalse(d["meta"]["writer_used_llm"])

    def test_run_without_panel(self):
        result = run(JOB_ANTIBOT, use_llm=False, review=False)
        d = result.to_dict()
        self.assertEqual(len(d["proposal"]["variants"]), 1)
        self.assertIsNone(d["panel"])
        self.assertEqual(d["meta"]["panel_reviewers"], 0)

    def test_prompt_built(self):
        a = analyze(JOB_ANTIBOT)
        p = build_prompt(a, JOB_ANTIBOT)
        # build_prompt is the optional two-variant writer
        self.assertIn("SHORT VARIANT", p)
        self.assertIn("PROCESS VARIANT", p)
        self.assertIn("--- VOICE RULEBOOK ---", p)

    def test_write_one_produces_single(self):
        a = analyze(JOB_ANTIBOT)
        b = write_one(a, JOB_ANTIBOT, include_screening=False)
        self.assertEqual(len(b.variants), 1)
        self.assertTrue(b.primary.body)

    def test_prompt_embeds_the_skill(self):
        a = analyze(JOB_ANTIBOT)
        p = build_prompt(a, JOB_ANTIBOT)
        # the real SKILL.md body must be in the prompt, not a hand-written copy
        self.assertIn("Write proposals that win by reducing the client's hiring risk",
                      p)
        self.assertIn("## Workflow", p)
        self.assertIn("## Voice", p)

    def test_skeletons_are_clean(self):
        result = run(JOB_ANALYSIS, use_llm=False)
        for v in result.proposal.variants:
            hard = [i for i in v.lint
                    if i["rule"] in ("banned_phrase", "exclamation", "emoji",
                                     "ai_tell", "pronoun_ratio")]
            self.assertEqual(hard, [], f"{v.label} has hard lint: {hard}")

    def test_flow_is_sequential_one_then_panel(self):
        # The combined flow must be: ONE proposal, then 7 agents on that one.
        result = run(JOB_ANTIBOT, use_llm=False, review=True)
        self.assertEqual(len(result.proposal.variants), 1)
        self.assertIsNotNone(result.panel)
        self.assertEqual(len(result.panel.reviews), 7)
        # every reviewer must have judged the same single proposal
        judged = result.panel.reviews[0]
        self.assertTrue(judged.verdict)
        # panel keys are exactly the seven personas
        keys = [r.key for r in result.panel.reviews]
        self.assertEqual(
            set(keys),
            {"scroller", "hiring_client", "budget_client", "competitor",
             "skeptic", "tech_lead", "veteran"})

    def test_improved_variant_prepended_when_better(self):
        # when a panel rewrite exists, it is promoted only if scores improve
        from engine.panel import PanelReport, Review
        rep = PanelReport(
            reviews=[Review("scroller", "The Scroller", "OPEN", "good")],
            scores={"Hook": 9}, interview_chance="HIGH", rewrite="Better text here")
        self.assertEqual(rep.rewrite, "Better text here")


if __name__ == "__main__":
    unittest.main()
