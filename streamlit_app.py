import streamlit as st
from groq import Groq
from datetime import datetime
import time

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="Nexo AI Career",
    page_icon="🚀",
    layout="wide",
)

# -----------------------------------------------------
# SPLASH SCREEN (WELCOME PAGE)
# -----------------------------------------------------
if "splash_done" not in st.session_state:
    st.session_state["splash_done"] = False

if not st.session_state["splash_done"]:
    splash_html = """
    <style>
        .splash-root {
            position: fixed;
            inset: 0;
            background: radial-gradient(circle at top left, #0f172a 0, #020617 50%, #000000 100%);
            display: flex;
            flex-direction: column;
            padding: 18px 26px;
            box-sizing: border-box;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            color: #e5e7eb;
            z-index: 9999;
        }
        .splash-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        .splash-logo {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 4px 10px;
            border-radius: 999px;
            border: 1px solid rgba(148,163,184,0.4);
            background: rgba(15,23,42,0.85);
            box-shadow: 0 10px 30px rgba(15,23,42,0.9);
        }
        .splash-logo-icon {
            width: 22px;
            height: 22px;
            border-radius: 999px;
            background: radial-gradient(circle at top, #38bdf8 0, #0ea5e9 40%, #0b1120 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9rem;
        }
        .splash-logo-text-main {
            font-size: 0.9rem;
            font-weight: 600;
            letter-spacing: 0.06em;
            text-transform: uppercase;
        }
        .splash-logo-text-sub {
            font-size: 0.7rem;
            color: #9ca3af;
        }
        .splash-center {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .splash-title {
            font-size: 2.2rem;
            font-weight: 700;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            background: linear-gradient(120deg, #38bdf8, #a855f7, #f97316);
            -webkit-background-clip: text;
            color: transparent;
            margin-bottom: 10px;
            animation: fadeInUp 1.3s ease-out forwards;
        }
        .splash-sub {
            font-size: 1rem;
            color: #cbd5f5;
            animation: fadeInUp 1.6s ease-out forwards;
        }
        .splash-footer {
            font-size: 0.75rem;
            color: #9ca3af;
            text-align: right;
            margin-top: 10px;
        }
        @keyframes fadeInUp {
            0% {opacity: 0; transform: translateY(10px);}
            100% {opacity: 1; transform: translateY(0);}
        }
    </style>

    <div class="splash-root">
        <div class="splash-top">
            <div class="splash-logo">
                <div class="splash-logo-icon">N</div>
                <div>
                    <div class="splash-logo-text-main">Nexo AI</div>
                    <div class="splash-logo-text-sub">Career Intelligence</div>
                </div>
            </div>
        </div>
        <div class="splash-center">
            <div class="splash-title">Welcome to Nexo AI Career</div>
            <div class="splash-sub">Created by Niyaz</div>
        </div>
        <div class="splash-footer">
            Initialising personalised guidance...
        </div>
    </div>
    """

    st.markdown(splash_html, unsafe_allow_html=True)
    time.sleep(4)
    st.session_state["splash_done"] = True
    st.rerun()

# -----------------------------------------------------
# SESSION STATE DEFAULTS
# -----------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "response_temperature" not in st.session_state:
    st.session_state.response_temperature = 0.6

if "theme" not in st.session_state:
    st.session_state.theme = "dark"   # "dark" or "light"


# -----------------------------------------------------
# THEME CSS
# -----------------------------------------------------
def inject_theme_css(theme: str):
    if theme == "light":
        bg = "#f3f4f6"
        text = "#020617"
        card_bg = "#ffffff"
        card_border = "rgba(148,163,184,0.5)"
        response_bg = "#ffffff"
        response_border = "rgba(148,163,184,0.8)"
        top_bg = "#e5e7eb"
    else:  # dark
        bg = "radial-gradient(circle at top left, #020617 0, #020617 40%, #000000 100%)"
        text = "#e5e7eb"
        card_bg = "rgba(15,23,42,0.88)"
        card_border = "rgba(31,41,55,0.8)"
        response_bg = "rgba(15,23,42,0.9)"
        response_border = "rgba(148,163,184,0.4)"
        top_bg = "rgba(15,23,42,0.85)"

    css = f"""
    <style>
        .stApp {{
            background: {bg};
            color: {text};
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }}
        .top-bar {{
            display:flex;
            align-items:center;
            justify-content:space-between;
            margin-bottom:0.8rem;
        }}
        .top-logo {{
            display:inline-flex;
            align-items:center;
            gap:8px;
            padding:4px 11px;
            border-radius:999px;
            border:1px solid rgba(148,163,184,0.4);
            background:{top_bg};
        }}
        .top-logo-icon {{
            width:22px;height:22px;border-radius:999px;
            background:radial-gradient(circle at top,#38bdf8 0,#0ea5e9 40%,#0b1120 100%);
            display:flex;align-items:center;justify-content:center;
            font-size:0.9rem;
        }}
        .top-logo-main {{
            font-size:0.9rem;font-weight:600;letter-spacing:0.06em;text-transform:uppercase;
        }}
        .top-logo-sub {{
            font-size:0.7rem;color:#9ca3af;
        }}
        .top-right {{
            font-size:0.75rem;
            color:#9ca3af;
        }}
        .card {{
            background:{card_bg};
            padding:1rem 1.2rem;
            border-radius:18px;
            border:1px solid {card_border};
        }}
        .ai-response {{
            background:{response_bg};
            padding:1.1rem 1.2rem;
            border-radius:18px;
            border:1px solid {response_border};
            margin-top:0.8rem;
            font-size:0.95rem;
            line-height:1.55;
        }}
        .section-title {{
            font-size:1.05rem;
            font-weight:600;
            margin-bottom:0.5rem;
        }}
        .sidebar-card {{
            background:{card_bg};
            padding:0.8rem 0.9rem;
            border-radius:14px;
            border:1px solid {card_border};
            font-size:0.85rem;
        }}
        .sidebar-title {{
            font-size:0.9rem;
            font-weight:600;
            margin-bottom:0.3rem;
        }}
        .sidebar-subtitle {{
            font-size:0.75rem;
            color:#9ca3af;
        }}
        .footer {{
            margin-top:1.4rem;
            font-size:0.8rem;
            color:#9ca3af;
            text-align:center;
            border-top:1px solid rgba(31,41,55,0.5);
            padding-top:0.7rem;
        }}
        .resource-chip {{
            display:inline-flex;
            padding:4px 10px;
            border-radius:999px;
            border:1px solid rgba(148,163,184,0.4);
            margin-right:6px;
            margin-bottom:6px;
            font-size:0.75rem;
        }}
        a {{
            text-decoration:none;
        }}
        a:hover {{
            text-decoration:underline;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


inject_theme_css(st.session_state.theme)

# -----------------------------------------------------
# SIDEBAR (COLLAPSIBLE)
# -----------------------------------------------------
with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-card" style="margin-bottom:0.7rem;">
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:0.3rem;">
                <div class="top-logo-icon">N</div>
                <div>
                    <div class="sidebar-title">Nexo AI</div>
                    <div class="sidebar-subtitle">Career Assistant</div>
                </div>
            </div>
            <div style="font-size:0.78rem;">
                Smart guidance for students and freshers,
                powered by large language models.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card" style="margin-bottom:0.7rem;">
            <div class="sidebar-title">About Niyaz</div>
            <div style="font-size:0.8rem;">
                <b>Niyaz Khan</b><br/>
                B.Tech CSE • Aspiring engineer & builder of Nexo AI.
            </div>
            <hr style="border:none;border-top:1px solid rgba(148,163,184,0.4);margin:6px 0 4px 0;">
            <div style="font-size:0.8rem;line-height:1.5;">
                📧 <a href="mailto:niyaz.kofficials@gmail.com">niyaz.kofficials@gmail.com</a><br/>
                💼 <a href="https://linkedin.com/in/iamnk7" target="_blank">linkedin.com/in/iamnk7</a><br/>
                💻 <a href="https://github.com/Iamnk07" target="_blank">github.com/Iamnk07</a><br/>
                📱 <a href="tel:+917751931035">+91 7751931035</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="sidebar-card" style="margin-bottom:0.7rem;">
            <div class="sidebar-title">Settings</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    theme_choice = st.radio(
        "Theme",
        options=["Dark", "Light"],
        index=0 if st.session_state.theme == "dark" else 1,
    )
    st.session_state.theme = "dark" if theme_choice == "Dark" else "light"

    temp = st.slider(
        "Creativity (temperature)",
        min_value=0.0,
        max_value=1.0,
        value=float(st.session_state.response_temperature),
        step=0.1,
        help="Lower = more strict and deterministic; Higher = more creative.",
    )
    st.session_state.response_temperature = temp

    if st.button("Clear history"):
        st.session_state.history = []
        st.success("History cleared for this session.")

# re-inject CSS after possible theme change
inject_theme_css(st.session_state.theme)

# -----------------------------------------------------
# GROQ CLIENT
# -----------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_groq_client()

SYSTEM_PROMPT = """
You are Nexo AI, an AI Career Guidance Assistant.
You:
- Give clear, structured and practical career guidance.
- Focus on short-term (0–3 months), mid-term (3–12 months) and long-term (1–3 years) actions.
- Understand student/fresher tech profiles (CSE, IT, etc.) very well.
- Can also help with interview prep: topics, strategy, and sample questions.
Return clean markdown with headings and bullet points.
Keep language simple, supportive and specific.
"""

def get_guidance(user_message: str, mode: str):
    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"Mode: {mode}\n\n{user_message}",
            },
        ],
        temperature=st.session_state.response_temperature,
        max_tokens=2048,
    )
    return completion.choices[0].message.content

# -----------------------------------------------------
# TOP BAR (NO EMPTY BOXES ANYMORE)
# -----------------------------------------------------
st.markdown(
    f"""
    <div class="top-bar">
        <div class="top-logo">
            <div class="top-logo-icon">N</div>
            <div>
                <div class="top-logo-main">Nexo AI</div>
                <div class="top-logo-sub">Career Assistant</div>
            </div>
        </div>
        <div class="top-right">
            {datetime.now().strftime("%d %b %Y")} • Powered by <b>Nexo AI</b>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------
# MAIN TABS
# -----------------------------------------------------
tab_career, tab_interview, tab_library, tab_history = st.tabs(
    ["Career Direction", "Interview Prep", "Library", "History"]
)

# -----------------------------------------------------
# CAREER DIRECTION TAB
# -----------------------------------------------------
with tab_career:
    left, right = st.columns([0.63, 0.37])

    with left:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Career Direction</div>', unsafe_allow_html=True)
        st.caption("Describe your current situation so Nexo AI can suggest a path.")

        with st.form("career_form"):
            name = st.text_input("Name (optional)", placeholder="Niyaz Khan")
            education = st.text_input(
                "Education",
                placeholder="B.Tech CSE, Final year",
            )
            skills = st.text_area(
                "What skills / technologies do you know?",
                placeholder="e.g. Python, DSA, HTML/CSS, JS, basic ML…",
                height=90,
            )
            interests = st.text_area(
                "What are you most interested in?",
                placeholder="e.g. web dev, data science, ML, cloud, startups…",
                height=80,
            )
            target_roles = st.text_input(
                "Target role(s)",
                placeholder="e.g. SDE-1, Data Scientist, ML Engineer…",
            )
            notes = st.text_area(
                "Other information (optional)",
                placeholder="Internships, projects, constraints, dream companies etc.",
                height=90,
            )

            submit_career = st.form_submit_button("Generate Career Plan 🚀")

        if submit_career:
            user_msg = f"""
Name: {name}
Education: {education}
Skills: {skills}
Interests: {interests}
Target roles: {target_roles}
Extra info: {notes}

Create a step-by-step career direction plan.
"""
            with st.spinner("Nexo AI is analysing your profile..."):
                try:
                    answer = get_guidance(user_msg, mode="career_direction")
                except Exception as e:
                    answer = f"❌ Error while contacting the model:\n\n`{e}`"

            st.markdown(f"<div class='ai-response'>{answer}</div>", unsafe_allow_html=True)

            st.session_state.history.append(
                {
                    "mode": "Career Direction",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "summary": f"{education} | {target_roles}",
                    "input": user_msg,
                    "output": answer,
                }
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Quick tips</div>', unsafe_allow_html=True)
        st.markdown(
            """
- Be honest about your **current level**.  
- Mention **2–3 roles** you are curious about.  
- Tell Nexo AI your **time availability** (e.g. 2 hrs/day).  
- Add your **favourite companies** or type (startup, MNC, remote).
            """
        )
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# INTERVIEW PREP TAB
# -----------------------------------------------------
with tab_interview:
    left_i, right_i = st.columns([0.63, 0.37])

    with left_i:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Interview Preparation</div>', unsafe_allow_html=True)
        st.caption("Get topics, strategy and sample questions for your next interview.")

        with st.form("interview_form"):
            role = st.text_input(
                "Target role",
                placeholder="e.g. SDE-1, Data Analyst, DevOps Engineer…",
            )
            company = st.text_input(
                "Company / type of company",
                placeholder="e.g. Product company, TCS NQT, Infosys, JP Morgan virtual, any…",
            )
            experience = st.text_input(
                "Experience level",
                placeholder="Final year / Fresher / 1 year exp…",
            )
            strong_areas = st.text_area(
                "Strong areas",
                placeholder="e.g. DSA, DBMS, projects in web dev / ML, communication…",
                height=80,
            )
            weak_areas = st.text_area(
                "Weak areas",
                placeholder="e.g. system design, probability & stats, confidence in English…",
                height=80,
            )
            upcoming = st.text_input(
                "Upcoming interview / exam (optional)",
                placeholder="e.g. TCS NQT on 5 Dec, JP Morgan test, college placement drive…",
            )

            submit_interview = st.form_submit_button("Generate Interview Plan 🎙️")

        if submit_interview:
            user_msg_int = f"""
Target role: {role}
Company / type: {company}
Experience: {experience}
Strong areas: {strong_areas}
Weak areas: {weak_areas}
Upcoming: {upcoming}

Create:
1) Topics to revise (with priority),
2) Daily/weekly plan till interview,
3) Behavioural questions and how to answer,
4) 8–10 sample technical questions with short answer outlines.
"""
            with st.spinner("Nexo AI is preparing your interview strategy..."):
                try:
                    ans_int = get_guidance(user_msg_int, mode="interview_prep")
                except Exception as e:
                    ans_int = f"❌ Error while contacting the model:\n\n`{e}`"

            st.markdown(f"<div class='ai-response'>{ans_int}</div>", unsafe_allow_html=True)

            st.session_state.history.append(
                {
                    "mode": "Interview Prep",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "summary": f"{role} | {company}",
                    "input": user_msg_int,
                    "output": ans_int,
                }
            )

        st.markdown("</div>", unsafe_allow_html=True)

    with right_i:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Checklist</div>', unsafe_allow_html=True)
        st.markdown(
            """
- At least **1–2 projects** you can explain well.  
- Basics of **DSA, OOP, DBMS, OS** (for SDE roles).  
- Practice **HR answers**: intro, strengths, failures, why this company.  
- Note down Nexo AI’s plan and tick items as you complete them.
            """
        )
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# LIBRARY TAB
# -----------------------------------------------------
with tab_library:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Library</div>', unsafe_allow_html=True)
    st.caption("Curated sections to help you explore common paths. (Static text, no external links from AI.)")

    col_l1, col_l2 = st.columns(2)

    with col_l1:
        st.markdown("##### Roadmaps")
        st.markdown(
            """
- **SDE / Web Developer**  
  1. Programming + DSA  
  2. HTML, CSS, JavaScript  
  3. One frontend framework (React)  
  4. Backend (Node / Django / Spring)  
  5. Database + basic system design  

- **Data Analyst / Scientist**  
  1. Python + pandas/NumPy  
  2. Statistics & probability basics  
  3. SQL  
  4. Data visualization  
  5. ML basics (regression, classification, evaluation)
            """
        )

    with col_l2:
        st.markdown("##### Interview Essentials")
        st.markdown(
            """
- **Core CS areas (for SDE):**  
  DSA, OOP, DBMS, OS, CN basics.  

- **Behavioural questions:**  
  - Tell me about yourself  
  - Strengths & weaknesses  
  - Biggest challenge / failure  
  - Why this role / company  

- **Projects:**  
  - Problem & motivation  
  - Tech stack  
  - Your contributions  
  - Challenges and learnings
            """
        )

    st.markdown("##### Quick Chips")
    st.markdown(
        """
        <span class="resource-chip">SDE Roadmap</span>
        <span class="resource-chip">Data Science Starter</span>
        <span class="resource-chip">Interview Patterns</span>
        <span class="resource-chip">System Design Basics</span>
        <span class="resource-chip">SQL for Freshers</span>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# HISTORY TAB
# -----------------------------------------------------
with tab_history:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">History</div>', unsafe_allow_html=True)

    if not st.session_state.history:
        st.info("No history yet. Use **Career Direction** or **Interview Prep** and results will appear here.")
    else:
        for i, item in enumerate(reversed(st.session_state.history), start=1):
            st.markdown(f"**#{i} – {item['mode']}**  ·  _{item['timestamp']}_")
            st.caption(item.get("summary", ""))
            with st.expander("View response"):
                st.markdown(item["output"])
            st.markdown("---")

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# FOOTER
# -----------------------------------------------------
st.markdown(
    """
    <div class="footer">
        Nexo AI Career • Created by <b>Niyaz</b> • Powered by <b>Nexo AI</b>
    </div>
    """,
    unsafe_allow_html=True,
)
