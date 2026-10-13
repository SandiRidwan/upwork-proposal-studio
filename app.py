"""
Upwork Proposal Studio - Streamlit UI.

Paste a job post -> analyze -> two proposals + 7-persona panel verdict.
Works with or without an API key.

    streamlit run app.py
"""

from __future__ import annotations

import json
from datetime import datetime

import streamlit as st

from engine import run, llm
from engine.panel import PERSONAS, SCORE_DIMENSIONS

st.set_page_config(
    page_title="Upwork Proposal Studio",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

SAMPLE = """We need someone to scrape product data from a large e-commerce site.
We tried Scrapy and a couple of freelancers but we keep getting blocked.
The site uses Cloudflare and we need about 20,000 products with price, title,
description and image URLs. Output to CSV or Google Sheets. Ongoing if it works well.
Budget is modest but we're realistic. Need it done this week if possible."""


# ---------------------------------------------------------------- styling

st.markdown("""
<style>
  .block-container { padding-top: 1.4rem; }
  .metric-card {
    background: #0f172a; border: 1px solid #1e293b; border-radius: 10px;
    padding: 12px 14px; text-align: center;
  }
  .metric-card h3 { margin: 0; font-size: 1.5rem; color: #38bdf8; }
  .metric-card p { margin: 0; color: #94a3b8; font-size: .75rem;
    text-transform: uppercase; letter-spacing: .05em; }
  .verdict { font-weight: 700; padding: 2px 8px; border-radius: 6px;
    font-size: .8rem; }
  .v-good { background:#064e3b; color:#6ee7b7; }
  .v-mid  { background:#78350f; color:#fcd34d; }
  .v-bad  { background:#7f1d1d; color:#fca5a5; }
  .prop-box { background:#0b1220; border:1px solid #1e293b; border-radius:10px;
    padding:16px 18px; white-space:pre-wrap; line-height:1.5; }
  .lint-ok { color:#6ee7b7; }
  .lint-bad { color:#fca5a5; }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------- sidebar

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    status = llm.status()
    if status["live"]:
        st.success(f"LLM live: **{status['provider']}** · {status['model']}")
    else:
        st.warning(
            "No API key detected. The studio still works: it produces a "
            "ready-to-paste prompt plus editable scaffolds.\n\n"
            "Set `OPENAI_API_KEY`, `GROQ_API_KEY`, `OPENROUTER_API_KEY`, or "
            "`UPS_PROVIDER=ollama` for full prose."
        )

    use_llm = st.toggle("Use LLM when available", value=True)
    do_review = st.toggle("Run 7-persona panel", value=True)
    do_rewrite = st.toggle("Panel also rewrites (slower)", value=False)

    st.divider()
    st.markdown("### 🧠 Identity")
    st.caption(
        "Facts come from `knowledge/positioning.md` and `knowledge/portfolio.md`. "
        "Edit those files to change what the tool may claim."
    )
    with st.expander("Checklist before sending"):
        st.markdown("""
- Opener names their problem, not you
- Exactly one credibility line, mid-proposal
- One (max) portfolio link
- Numbers are exact and real
- Ends on an easy-to-answer question
- No exclamation points, no emoji, no em dashes
""")


# ---------------------------------------------------------------- header

st.title("🎯 Upwork Proposal Studio")
st.caption(
    "Paste a job post. Get two proposals in your real voice, plus a 7-reviewer "
    "panel that tells you why it would get skipped, before you spend a Connect."
)

tab_write, tab_review, tab_knowledge = st.tabs(
    ["✍️ Write", "🧑‍⚖️ Panel review", "📚 Knowledge"])


# ---------------------------------------------------------------- write tab

with tab_write:
    c1, c2 = st.columns([3, 2])
    with c1:
        job_post = st.text_area(
            "Upwork job post", height=260, placeholder="Paste the full job post...",
            key="job_post")
    with c2:
        client_info = st.text_area(
            "Client info (optional)", height=110,
            placeholder="Their site, Upwork profile, spend, location...",
            key="client_info")
        screening = st.text_area(
            "Screening questions (optional)", height=110,
            placeholder="One per line, if the post lists them...",
            key="screening")
        bid = st.text_input("Your bid / rate (optional)", key="bid")

    b1, b2, _ = st.columns([1, 1, 3])
    run_clicked = b1.button("🚀 Analyze & write", type="primary",
                            use_container_width=True)
    load_sample = b2.button("Load sample", use_container_width=True)

    if load_sample:
        st.session_state["job_post"] = SAMPLE
        st.rerun()

    if run_clicked:
        if not job_post.strip():
            st.error("Paste a job post first.")
        else:
            with st.spinner("Analyzing, writing, and convening the panel..."):
                st.session_state["result"] = run(
                    job_post,
                    client_info=client_info,
                    screening=screening,
                    bid=bid,
                    use_llm=use_llm,
                    review_variants=do_review,
                    rewrite=do_rewrite,
                ).to_dict()
            st.session_state["ran_at"] = datetime.now().strftime("%H:%M:%S")

    result = st.session_state.get("result")
    if result:
        a = result["analysis"]

        st.divider()
        m = st.columns(5)
        cards = [
            ("Niche", f"{a['niche']}"),
            ("Urgency", a["urgency"].title()),
            ("Client type", a["client_type"].replace("_", " ").title()),
            ("Variant bias", a["variant"].title()),
            ("LLM", "live" if result["meta"]["writer_used_llm"] else "prompt"),
        ]
        for col, (label, val) in zip(m, cards):
            col.markdown(
                f"<div class='metric-card'><h3>{val}</h3><p>{label}</p></div>",
                unsafe_allow_html=True)

        st.markdown("#### 🔍 Analysis")
        ca, cb = st.columns(2)
        with ca:
            st.markdown(f"**Niche:** {a['niche']} — {a['niche_label']}")
            st.markdown(f"**Failure mode:** {a['failure_mode']}")
            st.markdown(f"**Named symptom:** `{a['named_symptom'] or '—'}`")
            st.markdown(f"**Budget signal:** {a['budget_signal']}")
        with cb:
            st.markdown(f"**Credibility fact:** {a['credibility_fact']}")
            st.markdown(f"**Portfolio link:** {a['portfolio_link']}")
            st.markdown(f"**One true observation:** {a['one_true_observation']}")
            if a["red_flags"]:
                st.error("Red flags: " + ", ".join(a["red_flags"]))
            if a["green_flags"]:
                st.success("Green flags: " + ", ".join(a["green_flags"]))

        if not result["meta"]["writer_used_llm"]:
            st.info(result["proposal"].get("notes", ""))

        st.markdown("#### ✍️ Proposals")
        variants = result["proposal"]["variants"]
        vcols = st.columns(len(variants)) if variants else []
        for col, v in zip(vcols, variants):
            with col:
                st.markdown(f"**{v['title']}** · {v['word_count']} words")
                st.markdown(
                    f"<div class='prop-box'>{v['body']}</div>",
                    unsafe_allow_html=True)
                if v["lint"]:
                    for issue in v["lint"]:
                        st.markdown(
                            f"<span class='lint-bad'>⚠ {issue['rule']}: "
                            f"{issue['detail']}</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span class='lint-ok'>✓ voice rules pass</span>",
                                unsafe_allow_html=True)
                st.download_button(
                    "Download .txt", v["body"],
                    file_name=f"proposal_{v['label']}.txt", key=f"dl_{v['label']}")

        if result["proposal"]["screening_answers"]:
            st.markdown("#### 📝 Screening answers")
            for qa in result["proposal"]["screening_answers"]:
                st.markdown(f"**Q:** {qa['question']}")
                st.code(qa["answer"], language=None)

        if result["proposal"].get("prompt") and not result["meta"]["writer_used_llm"]:
            with st.expander("📋 Ready-to-paste prompt (run this in opencode)"):
                st.code(result["proposal"]["prompt"], language="markdown")

        with st.expander("⬇️ Export full result (JSON)"):
            st.download_button(
                "Download result.json",
                json.dumps(result, indent=2, ensure_ascii=False),
                file_name="proposal_result.json")


# ---------------------------------------------------------------- review tab

with tab_review:
    result = st.session_state.get("result")
    if not result or not result.get("panels"):
        st.info("Run the writer first (or enable the panel) to see the review.")
    else:
        for idx, panel in enumerate(result["panels"]):
            vlabel = result["proposal"]["variants"][idx]["title"]
            st.markdown(f"### {vlabel}")

            chance = panel["interview_chance"]
            color = {"HIGH": "green", "MEDIUM": "orange", "LOW": "red"}[chance]
            st.markdown(
                f"**Interview chance:** :{color}[{chance}] "
                f"· {'LLM panel' if panel['used_llm'] else 'heuristic panel'}")

            sc = panel["scores"]
            cols = st.columns(len(SCORE_DIMENSIONS))
            for col, dim in zip(cols, SCORE_DIMENSIONS):
                val = sc.get(dim, 0)
                col.metric(dim, f"{val}/10")

            st.markdown("#### 🧑‍⚖️ Reviewers")
            for r in panel["reviews"]:
                style = ("v-good" if r["verdict"] in
                         ("OPEN", "INTERVIEW", "WORTH IT", "I WIN", "TRUST",
                          "KNOWS IT", "SHORTLIST")
                         else "v-mid" if r["verdict"] in
                         ("MAYBE", "NOT SURE", "TOSS-UP", "UNSURE", "VAGUE",
                          "ARCHIVE")
                         else "v-bad")
                st.markdown(
                    f"**{r['name']}** — "
                    f"<span class='verdict {style}'>{r['verdict']}</span><br>"
                    f"<span style='color:#94a3b8;font-size:.9rem'>{r['reason']}</span>",
                    unsafe_allow_html=True)

            if panel["problems"]:
                st.markdown("#### ⚠️ Problems, worst first")
                for i, p in enumerate(panel["problems"], 1):
                    st.markdown(f"{i}. {p}")

            st.markdown("#### 🗣️ The rejection story (in the client's voice)")
            st.info(panel["rejection_story"])

            if panel.get("rewrite"):
                st.markdown("#### ♻️ Suggested rewrite")
                st.markdown(
                    f"<div class='prop-box'>{panel['rewrite']}</div>",
                    unsafe_allow_html=True)
                ba = panel.get("before_after", {})
                if ba:
                    cc = st.columns(2)
                    cc[0].markdown(
                        f"**Scroller:** {ba.get('scroller',{}).get('before')} "
                        f"→ {ba.get('scroller',{}).get('after')}")
                    cc[1].markdown(
                        f"**Hiring Client:** "
                        f"{ba.get('hiring_client',{}).get('before')} "
                        f"→ {ba.get('hiring_client',{}).get('after')}")

            st.divider()


# ---------------------------------------------------------------- knowledge tab

with tab_knowledge:
    from engine import knowledge as kb
    st.caption(
        "These files are the identity + rule layer. Edit them to change what the "
        "tool may claim and how it writes. The writer reads them every run.")
    tabs = st.tabs(["Positioning", "Portfolio", "Voice rules",
                    "Winning patterns", "Client research"])
    files = [kb.positioning(), kb.portfolio(), kb.voice(), kb.wins(),
             kb.research()]
    for t, content in zip(tabs, files):
        with t:
            st.markdown(content)
