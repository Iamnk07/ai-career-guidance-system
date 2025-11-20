import streamlit as st
from groq import Groq
import time
from datetime import datetime

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="AI Career Guidance System",
    page_icon="🚀",
    layout="wide",
)

# -----------------------------------------------------
# SPLASH SCREEN (4 seconds)
# -----------------------------------------------------
if "splash_done" not in st.session_state:
    st.session_state["splash_done"] = False

if not st.session_state["splash_done"]:
    splash_html = """
    <style>
        body {
            margin: 0;
            padding: 0;
        }
        .splash-container {
            position: fixed;
            inset: 0;
            background: black;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            color: white;
            font-family: 'Segoe UI', sans-serif;
            animation: fadein 1.5s ease-out forwards;
        }
        @keyframes fadein {
            0% {opacity: 0;}
            100% {opacity: 1;}
        }
        .splash-title {
            font-size: 2.3rem;
            font-weight: 700;
            background: linear-gradient(120deg, #38bdf8, #a855f7, #f97316);
            -webkit-background-clip: text;
            color: transparent;
            margin-bottom: 10px;
        }
        .splash-sub {
            font-size: 1rem;
            color: #d1d5db;
        }
    </style>

    <div class="splash-container">
        <div class="splash-title">Welcome to AI Career Guidance System</div>
        <div class="splash-sub">Created by Niyaz</div>
    </div>
    """

    st.markdown(splash_html, unsafe_allow_html=True)
    time.sleep(4)
    st.session_state["splash_done"] = True
    st.rerun()

# -----------------------------------------------------
# CUSTOM CSS (same as before but removed icon area & empty boxes)
# -----------------------------------------------------
st.markdown(
    """
    <style>
        .stApp {
            background: radial-gradient(circle at top left, #0f172a 0, #020617 45%, #020617 100%);
            color: #e5e7eb;
            font-family: 'Segoe UI', sans-serif;
        }

        .hero-title {
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: 0.05em;
            background: linear-gradient(120deg, #38bdf8, #a855f7, #f97316);
            -webkit-background-clip: text;
            color: transparent;
            margin-bottom: 0.4rem;
            text-align: center;
        }
        .hero-subtitle {
            text-align: center;
            font-size: 1rem;
            color: #cbd5f5;
            margin-top: -5px;
        }
        .pill {
            margin: 0 auto;
            margin-top: 12px;
            display: flex;
            justify-content: center;
            width: fit-content;
            padding: 5px 16px;
            border-radius: 999px;
            border: 1px solid rgba(148,163,184,0.3);
            background: rgba(15,23,42,0.5);
            font-size: 0.75rem;
        }

        .metric-card {
            background: rgba(15,23,42,0.85);
            padding: 1rem;
            border-radius: 16px;
            border: 1px solid rgba(148,163,184,0.2);
        }

        .ai-response {
            background: rgba(15,23,42,0.8);
            padding: 1.1rem;
            border-radius: 16px;
            margin-top: 1rem;
            border: 1px solid rgba(148,163,184,0.4);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------
# HEADER (NO LOGO)
# -----------------------------------------------------
st.markdown('<div class="pill">AI-Powered • Career Guidance System</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">AI Career Guidance System</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero-subtitle">Smart, personalised career direction for students & professionals.</div>',
    unsafe_allow_html=True,
)

st.write("")  
st.write("### 🎯 What do you want to figure out today?")

# -----------------------------------------------------
# GROQ CLIENT
# -----------------------------------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

SYSTEM_PROMPT = """
You are an AI Career Guidance Assistant...
"""

def get_response(msg):
    res = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": msg}
        ]
    )
    return res.choices[0].message.content

# -----------------------------------------------------
# TABS
# -----------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Career Direction", "Skill Gap & Roadmap", "Interview Prep"])

with tab1:
    st.subheader("Tell me about yourself")
    name = st.text_input("Your Name")
    edu = st.text_input("Education / Year")
    skills = st.text_input("Skills")
    roles = st.text_input("Target Role")

    if st.button("Generate Career Guidance 🚀"):
        msg = f"Name: {name}\nEducation: {edu}\nSkills: {skills}\nRoles: {roles}"
        with st.spinner("Thinking..."):
            out = get_response(msg)

        st.markdown(f"<div class='ai-response'>{out}</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# FOOTER
# -----------------------------------------------------
st.markdown(
    """
    <br><br>
    <div style="text-align:center; font-size:0.9rem; color:#9ca3af;">
        Powered by <b>Nexo AI</b> • Created by <b>Niyaz</b>
    </div>
    """,
    unsafe_allow_html=True,
)
