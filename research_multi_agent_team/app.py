import os
import time
import threading
import streamlit as st
from crew import run_research

st.set_page_config(page_title="NEXUS | Research Intelligence", page_icon="✳️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --bg:#080b14; --panel:#111626; --line:#252d43; --muted:#9aa5bd; --text:#f4f6ff; --accent:#8b7cff; --cyan:#50d9ed; }
.stApp { background: radial-gradient(ellipse at 12% 0%, #1b1740 0%, #0b1020 35%, #080b14 72%); color:var(--text); font-family:'DM Sans',sans-serif; }
h1,h2,h3 {font-family:'Space Grotesk',sans-serif!important; letter-spacing:-.04em;}
.block-container {max-width:1240px; padding-top:2rem; padding-bottom:4rem;}
[data-testid="stSidebar"] {background:#0c1120;border-right:1px solid var(--line);}
.hero {padding:30px 32px;border:1px solid #343052;border-radius:24px;background:linear-gradient(125deg,rgba(139,124,255,.18),rgba(80,217,237,.06) 55%,rgba(17,22,38,.8));box-shadow:0 20px 70px #0003;margin-bottom:24px;}
.eyebrow {color:#a99eff;font-size:12px;font-weight:700;letter-spacing:.18em;text-transform:uppercase;}
.hero h1 {font-size:clamp(36px,5vw,58px);line-height:1.05;margin:12px 0;color:#fff;}
.hero p {color:#b8c1d8;font-size:16px;max-width:720px;}
.pill {display:inline-block;padding:7px 12px;border:1px solid #3c4561;border-radius:999px;color:#cbd4eb;font-size:12px;margin:5px 5px 0 0;background:#ffffff08;}
.panel {background:rgba(17,22,38,.86);border:1px solid var(--line);border-radius:20px;padding:22px;}
.agent {padding:13px 15px;border:1px solid #283149;border-radius:14px;background:#0d1322;margin:8px 0;}
.agent-active {border-color:#8b7cff;background:linear-gradient(110deg,#27204d,#111a2b);box-shadow:0 0 0 1px #8b7cff33;}
.agent-done {border-color:#236c62;background:#0d211f;}
.small {color:#9aa5bd;font-size:13px;}
div.stButton>button[kind="primary"] {background:linear-gradient(100deg,#8170ff,#4c9cff);border:0;border-radius:12px;color:white;font-weight:700;min-height:48px;box-shadow:0 8px 24px #6558d944;}
div.stButton>button[kind="primary"]:hover {border:0;filter:brightness(1.12);transform:translateY(-1px);}
.stTextArea textarea,.stTextInput input,.stSelectbox div[data-baseweb="select"] {background:#0d1322!important;border-color:#303953!important;color:#f4f6ff!important;border-radius:12px!important;}
[data-testid="stMetric"] {background:#111626;border:1px solid #252d43;padding:16px;border-radius:16px;}
hr {border-color:#252d43!important;}
</style>
""", unsafe_allow_html=True)

AGENTS = [
    ("01", "Research Planner", "Scopes the question and builds the research plan"),
    ("02", "Web Researcher", "Finds sources and extracts relevant evidence"),
    ("03", "Evidence Analyst", "Synthesizes findings and identifies gaps"),
    ("04", "Fact Checker", "Checks support, dates, and citation consistency"),
    ("05", "Report Writer", "Creates the final structured research brief"),
]

if "research_result" not in st.session_state:
    st.session_state.research_result = None
if "status" not in st.session_state:
    st.session_state.status = {"active": None, "completed": [], "messages": [], "done": False, "error": None}

st.markdown("""
<div class="hero">
 <div class="eyebrow">✳ NEXUS RESEARCH INTELLIGENCE</div>
 <h1>Turn questions into<br><span style="background:linear-gradient(90deg,#a99eff,#62dff0);-webkit-background-clip:text;color:transparent;">evidence-led insight.</span></h1>
 <p>A coordinated research team that searches the web, evaluates evidence, checks claims, and delivers a clear, source-linked report.</p>
 <span class="pill">CREWAI MULTI-AGENT</span><span class="pill">GROQ POWERED</span><span class="pill">LIVE AGENT STATUS</span>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ✳ NEXUS")
    st.caption("Research workspace")
    st.markdown("---")
    st.markdown("**Your research crew**")
    for num, name, desc in AGENTS:
        st.markdown(f"<div class='agent'><b>{num} · {name}</b><div class='small'>{desc}</div></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.caption("Research outputs are AI-generated. Always independently verify scientific and consequential claims.")

left, right = st.columns([1.55, 1], gap="large")
with left:
    st.markdown("### Define your research")
    with st.form("research_form"):
        topic = st.text_area("Research question or topic", placeholder="e.g., Recent mechanisms of antimicrobial resistance in poultry-associated Campylobacter...", height=145)
        c1, c2 = st.columns(2)
        with c1:
            depth = st.selectbox("Research depth", ["Standard", "Comprehensive", "Quick"])
        with c2:
            years = st.selectbox("Source timeframe", ["Last 5 years", "Last 12 months", "All available"])
        length = st.select_slider("Report length", options=["Concise", "Balanced", "Detailed"], value="Balanced")
        submitted = st.form_submit_button("✦  Start research", type="primary", use_container_width=True)

with right:
    st.markdown("### Research workflow")
    st.markdown("<div class='panel'><div class='eyebrow'>YOUR TEAM, IN ACTION</div><h3 style='margin:8px 0 4px'>Five specialists. One report.</h3><p class='small'>Each stage builds on the previous agent's work. Watch the active stage update while your research runs.</p></div>", unsafe_allow_html=True)
    status_box = st.empty()

def render_status(status):
    active = status.get("active")
    completed = status.get("completed", [])
    html = "<div class='panel'><div class='eyebrow'>LIVE AGENT STATUS</div>"
    for num, name, desc in AGENTS:
        if name in completed:
            cls, state = "agent-done", "✓ Complete"
        elif name == active:
            cls, state = "agent-active", "● Working now"
        else:
            cls, state = "agent", "Waiting"
        html += f"<div class='{cls}'><div style='display:flex;justify-content:space-between;gap:8px'><b>{num} · {name}</b><span class='small'>{state}</span></div><div class='small'>{desc}</div></div>"
    if status.get("error"):
        html += f"<p style='color:#ff9caa'>{status['error']}</p>"
    html += "</div>"
    status_box.markdown(html, unsafe_allow_html=True)

render_status(st.session_state.status)

if submitted:
    if not topic.strip():
        st.warning("Please enter a research topic first.")
    elif not st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY")):
        st.error("Add GROQ_API_KEY in Streamlit Cloud → App settings → Secrets.")
    elif not st.secrets.get("SERPER_API_KEY", os.getenv("SERPER_API_KEY")):
        st.error("Add SERPER_API_KEY in Streamlit Cloud → App settings → Secrets.")
    else:
        st.session_state.research_result = None
        st.session_state.status = {"active": AGENTS[0][1], "completed": [], "messages": [], "done": False, "error": None}
        render_status(st.session_state.status)
        progress = st.progress(0, text="Preparing your research crew...")
        result_slot = st.empty()
        try:
            # Crew callbacks update this shared object; UI polls it during execution.
            result = run_research(
                topic=topic.strip(), depth=depth, timeframe=years, report_length=length,
                status=st.session_state.status
            )
            st.session_state.research_result = str(result)
            st.session_state.status["active"] = None
            st.session_state.status["done"] = True
            progress.progress(100, text="Research complete")
            render_status(st.session_state.status)
        except Exception as e:
            st.session_state.status["error"] = f"Research failed: {e}"
            st.session_state.status["active"] = None
            render_status(st.session_state.status)
            st.exception(e)

if st.session_state.research_result:
    st.markdown("---")
    st.markdown("## Your research brief")
    st.download_button("⬇ Download Markdown report", st.session_state.research_result,
                       file_name="nexus_research_report.md", mime="text/markdown")
    st.download_button("⬇ Download TXT", st.session_state.research_result,
                       file_name="nexus_research_report.txt", mime="text/plain")
    st.markdown(st.session_state.research_result)
