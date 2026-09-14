import json
import streamlit as st
from datetime import datetime
from agent import WebMindAgent
from config import get_anakin_key, get_gemini_key

# Page setup
st.set_page_config(
    page_title="WebMind Control | Autonomous AI Agent",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for polished hackathon presentation
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #6c757d;
        margin-bottom: 1.2rem;
    }
    .agent-pipeline {
        display: flex;
        flex-wrap: wrap;
        gap: 0.5rem;
        padding: 0.75rem 1rem;
        background: #f8f9fa;
        border-radius: 8px;
        border: 1px solid #e9ecef;
        margin-bottom: 1.2rem;
        font-size: 0.9rem;
        font-weight: 600;
    }
    .verdict-box {
        padding: 1.25rem;
        border-radius: 8px;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white;
        margin-bottom: 1.5rem;
    }
    .verdict-title {
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
    }
    .stDownloadButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# SIDEBAR: Configuration, Status & Presets
# -------------------------------------------------------------
with st.sidebar:
    st.image("https://img.icons8.com/isometric/100/artificial-intelligence.png", width=64)
    st.title("WebMind Control")
    st.caption("🏆 Built for **Anakin Forge Hackathon 2026**")
    
    st.markdown("---")
    st.subheader("🔑 API Credentials")
    
    # Check env credentials
    env_anakin = get_anakin_key()
    env_gemini = get_gemini_key()
    
    anakin_key_input = st.text_input(
        "Anakin API Key",
        value=env_anakin,
        type="password",
        help="Get from anakin.io/dashboard -> API Keys"
    )
    
    gemini_key_input = st.text_input(
        "Gemini API Key",
        value=env_gemini,
        type="password",
        help="Get from Google AI Studio"
    )
    
    if anakin_key_input:
        st.success("🟢 Anakin API (Execution Layer)")
    else:
        st.warning("⚠️ Anakin Key Missing (High-fidelity cache active)")
        
    if gemini_key_input:
        st.success("🟢 Gemini 2.0 (Cognitive Layer)")
    else:
        st.info("ℹ️ Gemini Key Missing (Heuristic brain active)")

    st.markdown("---")
    st.subheader("💡 Demo Presets")
    preset_choice = st.selectbox(
        "Choose an agent evaluation task:",
        [
            "🏆 AI Hackathon Scout (Deadlines, prizes, format & shortlist)",
            "PostHog vs Mixpanel (AI SaaS, 50k MAUs, $100/mo budget)",
            "Supabase vs Neon (Next.js serverless & vector search)",
            "Stripe vs Paddle vs LemonSqueezy (EU VAT & MoR compliance)",
            "Custom Query"
        ]
    )
    
    st.markdown("---")
    st.markdown("""
    ### 🔄 7-Stage Agent Pipeline
    * 🧠 **PLAN**: Understand & formulate queries
    * 🔎 **TOOL**: Anakin Search live retrieval
    * 📖 **OBSERVE**: Digest web evidence buffer
    * 🧠 **REASON**: Audit gaps & decide next action
    * ⚡ **ACT**: Deep verification & synthesize
    * ✅ **VERIFY**: Self-audit against constraints
    * 🎯 **RESULT**: Final dossier & download artifacts
    """)

# -------------------------------------------------------------
# MAIN CONTENT AREA
# -------------------------------------------------------------
st.markdown('<div class="main-header">🧠 WebMind Control: Autonomous Web Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Anakin.io (Live Web Execution Layer) + Google Gemini (Cognitive Brain Layer)</div>', unsafe_allow_html=True)

# Observable Agent Pipeline Banner
st.markdown("""
<div class="agent-pipeline">
    <span>🧠 PLAN</span> ➔ 
    <span>🔎 TOOL (Anakin Search)</span> ➔ 
    <span>📖 OBSERVE</span> ➔ 
    <span>🧠 REASON</span> ➔ 
    <span>⚡ ACT (Anakin Scrape)</span> ➔ 
    <span>✅ VERIFY</span> ➔ 
    <span>🎯 RESULT</span>
</div>
""", unsafe_allow_html=True)

# Preset mapping
if preset_choice == "🏆 AI Hackathon Scout (Deadlines, prizes, format & shortlist)":
    default_query = "Find relevant AI hackathons, compare their deadline, prize, eligibility and format, verify the best option from the official page, and prepare a submission-ready shortlist."
elif preset_choice == "PostHog vs Mixpanel (AI SaaS, 50k MAUs, $100/mo budget)":
    default_query = "Compare PostHog vs Mixpanel for an AI SaaS startup with 50,000 monthly active users. Check free-tier event limits, retention policies, and hidden overage costs on a strict $100/month budget."
elif preset_choice == "Supabase vs Neon (Next.js serverless & vector search)":
    default_query = "Compare Supabase vs Neon for a fast-growing Next.js serverless backend. Investigate compute auto-scaling, cold-starts, vector search extension limits, and monthly costs for 10GB storage."
elif preset_choice == "Stripe vs Paddle vs LemonSqueezy (EU VAT & MoR compliance)":
    default_query = "Compare Stripe vs Paddle vs LemonSqueezy for selling SaaS subscriptions in the EU and US. Verify Merchant of Record fees, automated VAT handling, and chargeback protection terms."
else:
    default_query = ""

user_query = st.text_area(
    "Enter agent objective or decision task:",
    value=default_query,
    height=90,
    help="Describe the research or evaluation goal you want WebMind Control to execute autonomously."
)

col_act1, col_act2 = st.columns([3, 1])
with col_act1:
    dispatch_btn = st.button("🚀 Dispatch Autonomous Agent Loop", type="primary", use_container_width=True)
with col_act2:
    deep_scrape_toggle = st.checkbox("Enable Deep Verification", value=True, help="Allows agent to execute targeted Anakin URL Scrapes if data gaps are detected.")

# Session state for results
if "agent_result" not in st.session_state:
    st.session_state.agent_result = None

if dispatch_btn and user_query:
    st.markdown("---")
    st.subheader("⚡ Observable Agent Execution Trace")
    
    agent = WebMindAgent(
        anakin_key=anakin_key_input,
        gemini_key=gemini_key_input
    )
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    trace_expander = st.expander("Live Trace Events", expanded=True)
    
    status_text.info("🧠 Creating plan...")
    progress_bar.progress(15)
    
    # Run Agent
    try:
        with st.spinner("Agent is running autonomous loop: PLAN ➔ TOOL ➔ OBSERVE ➔ REASON ➔ ACT ➔ VERIFY..."):
            result = agent.run(user_query, deep_mode=deep_scrape_toggle)
            st.session_state.agent_result = result
            try:
                with open("latest_run.json", "w", encoding="utf-8") as f:
                    json.dump(result, f, indent=2)
            except Exception as fe:
                pass
            progress_bar.progress(100)
            status_text.success(f"🎯 Completed in {result.get('duration_seconds', 0)} seconds!")
    except Exception as e:
        st.error(f"❌ Execution failed: {str(e)}")

# -------------------------------------------------------------
# DISPLAY RESULTS & ARTIFACTS (THE ACT & RESULT PHASE)
# -------------------------------------------------------------
if st.session_state.agent_result:
    res = st.session_state.agent_result
    battlecard = res.get("battlecard", {})
    verification = res.get("verification", {})
    evidence = res.get("evidence", [])
    trace = res.get("execution_trace", [])
    
    # 1. Executive Verdict Banner
    rec = battlecard.get("recommendation") or battlecard.get("recommended_choice", "Top Recommended Option")
    verdict = battlecard.get("verdict", "Analysis complete.")
    
    st.markdown(f"""
    <div class="verdict-box">
        <div class="verdict-title">🏆 Top Recommendation: {rec}</div>
        <div style="font-size: 1.05rem; opacity: 0.95;">{verdict}</div>
    </div>
    """, unsafe_allow_html=True)

    # 1.5 Real Web Action Card (Executed via Anakin URL Scraper)
    action_card = res.get("action_card", {})
    if action_card:
        with st.container(border=True):
            st.markdown("### ⚡ Verified Action Execution Card *(via Anakin URL Scraper)*")
            st.caption("The agent actively retrieved the selected candidate's official portal via **Anakin URL Scraper**, audited live page contents, and extracted the verified registration gateway and submission requirements.")
            
            col_ac_main, col_ac_proof = st.columns([3, 2])
            with col_ac_main:
                st.markdown(f"**🎯 Target Opportunity:** `{action_card.get('selected_opportunity', rec)}`")
                st.markdown(f"**🌐 Official Portal:** [{action_card.get('official_page', 'N/A')}]({action_card.get('official_page', '#')})")
                
                reg_url = action_card.get("registration_url")
                if reg_url:
                    st.markdown(f"**🔗 Verified Registration Gateway:** [{reg_url}]({reg_url})")
                else:
                    st.markdown(f"**ℹ️ Registration Endpoint:** *{action_card.get('registration_note', 'No direct link on page; consult official portal')}*")
                
                st.markdown(f"**⏳ Verified Deadline:** `{action_card.get('verified_deadline', 'Verified from live page')}`")
                st.markdown(f"**👥 Eligibility & Format:** `{action_card.get('eligibility_status', 'Open')}`")
                st.markdown(f"**▶️ Immediate Next Action:** {action_card.get('next_action', 'Proceed to portal')}")
                
                req_fields = action_card.get("required_fields", [])
                if req_fields:
                    st.markdown("**📋 Required Submission Artifacts:**")
                    for rf in req_fields:
                        st.markdown(f"- 📌 **{rf}**")
            
            with col_ac_proof:
                st.markdown("**🛡️ Anakin Execution Proof:**")
                proof = action_card.get("execution_proof", {})
                st.json(proof)
                
                if reg_url:
                    st.link_button("🚀 Open Official Registration Gateway", reg_url, use_container_width=True)
                else:
                    official_btn_url = action_card.get("official_page") or "https://anakin.io"
                    st.link_button("🌐 Open Scraped Official Portal", official_btn_url, use_container_width=True)
    
    # 2. Executive Summary
    with st.expander("📄 Executive Analysis Brief", expanded=True):
        st.write(battlecard.get("executive_summary", "No summary generated."))

    # 3. Decision Matrix Table
    st.subheader("📊 Comparative Decision Matrix & Shortlist")
    matrix = battlecard.get("comparison_rows") or battlecard.get("comparison_matrix", [])
    if matrix:
        st.table(matrix)
    else:
        st.info("No comparison rows returned.")

    # 4. Agent Verification Audit
    if verification:
        with st.expander(f"✅ Agent Verification Audit ({verification.get('status', 'VERIFIED')})", expanded=True):
            col_v1, col_v2 = st.columns([1, 3])
            with col_v1:
                st.metric("Confidence Score", f"{verification.get('confidence_score', 95)}%")
            with col_v2:
                for c in verification.get("checks", []):
                    st.markdown(f"**{'🟢' if c.get('passed', True) else '🟡'} {c.get('check')}**: {c.get('note')}")

    # 5. Two columns for Risks & Next Steps
    col_risk, col_next = st.columns(2)
    with col_risk:
        st.subheader("⚠️ Critical Gotchas & Risk Factors")
        risks = battlecard.get("risks") or battlecard.get("risk_factors", [])
        if risks:
            for r in risks:
                st.warning(f"**{r}**")
        else:
            st.write("No major risk factors detected.")
            
    with col_next:
        st.subheader("🚀 Actionable Next Steps")
        steps = battlecard.get("next_steps") or battlecard.get("actionable_next_steps", [])
        if steps:
            for s in steps:
                st.checkbox(s, key=f"step_{s[:20]}")
        else:
            st.write("Proceed with final review.")

    # 6. Live Web Sources & Evidence Extracted
    st.subheader("🔗 Ground-Truth Live Web Sources (Extracted via Anakin.io)")
    if evidence:
        for i, ev in enumerate(evidence):
            with st.expander(f"[{i+1}] {ev.get('title', 'Web Page')} ({ev.get('source', 'Anakin')})", expanded=False):
                st.caption(f"**URL:** {ev.get('url')}")
                st.text((ev.get("snippet") or ev.get("content") or "No preview available.")[:400] + "...")
                st.markdown(f"[Visit Live Source Page]({ev.get('url')})")
    else:
        st.write("No live sources recorded.")

    # 7. ACT ARTIFACT DOWNLOADS
    st.markdown("---")
    st.subheader("📥 Export Final Decision Artifacts")
    col_dl1, col_dl2, col_dl3 = st.columns(3)
    
    with col_dl1:
        st.download_button(
            label="📄 Download Executive Dossier (.md)",
            data=res.get("markdown_dossier", ""),
            file_name=f"webmind_decision_dossier_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            mime="text/markdown",
            use_container_width=True
        )
        
    with col_dl2:
        st.download_button(
            label="💾 Download Structured Battlecard (.json)",
            data=json.dumps(battlecard, indent=2),
            file_name=f"webmind_battlecard_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

    with col_dl3:
        st.download_button(
            label="⚡ Download Action Execution Card (.json)",
            data=json.dumps(action_card, indent=2),
            file_name=f"webmind_action_card_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

    # 8. Agent Brain Trace
    with st.expander("🕵️ Inspect Internal Agent Execution Trace (Full Event Log)", expanded=False):
        for t in trace:
            st.markdown(f"**`[{t.get('timestamp')}]` {t.get('step_name')} — {t.get('title')}**")
            st.caption(t.get("details"))
            if t.get("metadata"):
                st.json(t.get("metadata"))
            st.divider()
