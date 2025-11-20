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
# SPLASH SCREEN
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
            justify-content: flex-start;
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
        @keyframes fadeInUp {
            0% {opacity: 0; transform: translateY(10px);}
            100% {opacity: 1; transform: translateY(0);}
        }
    </style>

    <div class="splash-root">
        <div class="splash-top">
            <div style="font-size:1.1rem;font-weight:700;letter-spacing:0.08em;text-transform:uppercase;">
                Nexo AI
            </div>
        </div>
        <div class="splash-center">
            <div class="splash-title">Welcome to Nexo AI Career</div>
            <div class="splash-sub">Created by Niyaz</div>
        </div>
    </div>
    """
    st.markdown(splash_html, unsafe_allow_html=True)
    time.sleep(4)
    st.session_state["splash_done"] = True
    st.rerun()

# -----------------------------------------------------
# SESSION STATE
# -----------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

if "response_temperature" not in st.session_state:
    st.session_state.response_temperature = 0.6

if "theme" not in st.session_state:
    st.session_state.theme = "dark"  # "dark" or "light"

# -----------------------------------------------------
# THEME CSS
# -----------------------------------------------------
def inject_theme_css(theme: str):
    if theme == "light":
        bg = "#f8fafc"
        text = "#0f172a"
        muted = "#4b5563"
        card_bg = "#ffffff"
        card_border = "rgba(148,163,184,0.6)"
        response_bg = "#ffffff"
        response_border = "rgba(148,163,184,0.9)"
        tab_indicator = "#ef4444"
    else:
        bg = "radial-gradient(circle at top left, #020617 0, #020617 40%, #000000 100%)"
        text = "#e5e7eb"
        muted = "#9ca3af"
        card_bg = "rgba(15,23,42,0.95)"
        card_border = "rgba(31,41,55,0.9)"
        response_bg = "rgba(15,23,42,0.95)"
        response_border = "rgba(148,163,184,0.7)"
        tab_indicator = "#f97316"

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
        .top-brand-title {{
            font-size:1.3rem;
            font-weight:700;
            letter-spacing:0.12em;
            text-transform:uppercase;
        }}
        .top-brand-sub {{
            font-size:0.78rem;
            color:{muted};
        }}
        .top-right {{
            font-size:0.8rem;
            color:{muted};
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
            margin-bottom:0.4rem;
        }}
        .footer {{
            margin-top:1.5rem;
            font-size:0.8rem;
            color:{muted};
            text-align:center;
            border-top:1px solid rgba(148,163,184,0.4);
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
        /* highlight for active tab (underline color) */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.2rem;
        }}
        .stTabs [data-baseweb="tab"] {{
            padding: 0.5rem 0.9rem;
        }}
        .stTabs [data-baseweb="tab-highlight"] {{
            background-color: {tab_indicator};
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
# SIDEBAR NAVIGATION (TEXT ONLY)
# -----------------------------------------------------
with st.sidebar:
    st.markdown("### Nexo AI")
    st.caption("Career guidance assistant built by Niyaz.")

    nav = st.radio(
        "Navigation",
        ["Home", "About", "Contact", "Settings"],
        index=0,
    )

# -----------------------------------------------------
# GROQ CLIENT & LLM
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
# TOP BAR (ONLY TEXT LOGO, NO BOX)
# -----------------------------------------------------
st.markdown(
    f"""
    <div class="top-bar">
        <div>
            <div class="top-brand-title">Nexo AI</div>
            <div class="top-brand-sub">Career Assistant</div>
        </div>
        <div class="top-right">
            {datetime.now().strftime("%d %b %Y")} • Powered by <b>Nexo AI</b>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# =====================================================
# MAIN CONTENT ROUTING BASED ON SIDEBAR NAV
# =====================================================

# -----------------------------------------------------
# NAV: HOME  ->  TABS
# -----------------------------------------------------
if nav == "Home":
    tab_career, tab_interview, tab_library, tab_history = st.tabs(
        ["Career Direction", "Interview Prep", "Library", "History"]
    )

    # ---------- CAREER DIRECTION ----------
    with tab_career:
        left, right = st.columns([0.63, 0.37])

        with left:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-title">Career Direction</div>',
                unsafe_allow_html=True,
            )
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

                st.markdown(
                    f"<div class='ai-response'>{answer}</div>",
                    unsafe_allow_html=True,
                )

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
            st.markdown(
                '<div class="section-title">Quick tips</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                """
- Be honest about your **current level**.  
- Mention **2–3 roles** you are curious about.  
- Tell Nexo AI your **time availability** (e.g. 2 hrs/day).  
- Add your **favourite companies** or type (startup, MNC, remote).
                """
            )
            st.markdown("</div>", unsafe_allow_html=True)

    # ---------- INTERVIEW PREP ----------
    with tab_interview:
        left_i, right_i = st.columns([0.63, 0.37])

        with left_i:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="section-title">Interview Preparation</div>',
                unsafe_allow_html=True,
            )
            st.caption(
                "Get topics, strategy and sample questions for your next interview."
            )

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

                submit_interview = st.form_submit_button(
                    "Generate Interview Plan 🎙️"
                )

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

                st.markdown(
                    f"<div class='ai-response'>{ans_int}</div>",
                    unsafe_allow_html=True,
                )

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
            st.markdown(
                '<div class="section-title">Checklist</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                """
- At least **1–2 projects** you can explain well.  
- Basics of **DSA, OOP, DBMS, OS** (for SDE roles).  
- Practice **HR answers**: intro, strengths, failures, why this company.  
- Note down Nexo AI’s plan and tick items as you complete them.
                """
            )
            st.markdown("</div>", unsafe_allow_html=True)

    # ---------- LIBRARY ----------
    with tab_library:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title">Library</div>',
            unsafe_allow_html=True,
        )
        st.caption("Official docs and high-quality learning resources.")

        col_l1, col_l2 = st.columns(2)

        with col_l1:
            st.markdown("##### Core Programming & Web")
            st.markdown(
                """
- [Python Official Docs](https://docs.python.org/3/)  
- [JavaScript MDN Guide](https://developer.mozilla.org/en-US/docs/Web/JavaScript)  
- [React Official Docs](https://react.dev/)  
- [Node.js Docs](https://nodejs.org/en/docs)  
- [HTML & CSS – MDN](https://developer.mozilla.org/en-US/docs/Web)  
- [FreeCodeCamp](https://www.freecodecamp.org/)
                """
            )

            st.markdown("##### Data / ML")
            st.markdown(
                """
- [pandas Documentation](https://pandas.pydata.org/docs/)  
- [NumPy Docs](https://numpy.org/doc/)  
- [Scikit-learn Docs](https://scikit-learn.org/stable/)  
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course)  
- [IBM Data Science Learning Path](https://www.ibm.com/training/data-science)
                """
            )

        with col_l2:
            st.markdown("##### Cloud / DevOps")
            st.markdown(
                """
- [AWS Documentation](https://docs.aws.amazon.com/)  
- [Azure Docs](https://learn.microsoft.com/azure/)  
- [Google Cloud Docs](https://cloud.google.com/docs)  
- [Docker Docs](https://docs.docker.com/)  
- [Kubernetes Docs](https://kubernetes.io/docs/home/)
                """
            )

            st.markdown("##### Coding Practice & CS")
            st.markdown(
                """
- [LeetCode](https://leetcode.com/)  
- [GeeksforGeeks](https://www.geeksforgeeks.org/)  
- [HackerRank](https://www.hackerrank.com/)  
- [NPTEL Courses](https://nptel.ac.in/)  
- [TCS NQT Prep (Official)](https://learning.tcsionhub.in/hub/national-qualifier-test)
                """
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # ---------- HISTORY ----------
    with tab_history:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(
            '<div class="section-title">History</div>',
            unsafe_allow_html=True,
        )

        if not st.session_state.history:
            st.info(
                "No history yet. Use **Career Direction** or **Interview Prep** and results will appear here."
            )
        else:
            for i, item in enumerate(reversed(st.session_state.history), start=1):
                st.markdown(
                    f"**#{i} – {item['mode']}**  ·  _{item['timestamp']}_"
                )
                st.caption(item.get("summary", ""))
                with st.expander("View response"):
                    st.markdown(item["output"])
                st.markdown("---")

        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# NAV: ABOUT
# -----------------------------------------------------
elif nav == "About":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">About Nexo AI</div>', unsafe_allow_html=True)
    st.markdown(
        """
**Nexo AI** is a personal AI career assistant built by **Niyaz Khan**.

It helps students and freshers:

- Understand possible **career paths** in tech  
- Plan **short-term, mid-term and long-term** actions  
- Prepare for **interviews** in a structured way  
- Explore high-quality **learning resources** without confusion  
        """
    )
    st.markdown("---")
    st.markdown("#### About Niyaz")
    st.markdown(
        """
- **Name:** Niyaz Khan  
- **Degree:** B.Tech in Computer Science Engineering  
- **Interests:** AI, careers, web apps, and building real products.  

> Nexo AI is one of his projects to help students like him get clear guidance.
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# NAV: CONTACT
# -----------------------------------------------------
elif nav == "Contact":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Contact</div>', unsafe_allow_html=True)
    st.markdown("You can reach out to Niyaz for feedback or collaboration:")
    st.markdown(
        """
- 📧 Email: **[niyaz.kofficials@gmail.com](mailto:niyaz.kofficials@gmail.com)**  
- 💼 LinkedIn: **[linkedin.com/in/iamnk7](https://linkedin.com/in/iamnk7)**  
- 💻 GitHub: **[github.com/Iamnk07](https://github.com/Iamnk07)**  
- 📱 Phone / WhatsApp: **+91 7751931035**
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# NAV: SETTINGS
# -----------------------------------------------------
elif nav == "Settings":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Settings</div>', unsafe_allow_html=True)

    st.markdown("##### Theme")
    theme_choice = st.radio(
        "Choose theme",
        ["Dark", "Light"],
        index=0 if st.session_state.theme == "dark" else 1,
    )
    new_theme = "dark" if theme_choice == "Dark" else "light"
    if new_theme != st.session_state.theme:
        st.session_state.theme = new_theme
        st.rerun()

    st.markdown("##### Response Style")
    temp = st.slider(
        "Creativity (temperature)",
        min_value=0.0,
        max_value=1.0,
        value=float(st.session_state.response_temperature),
        step=0.1,
        help="Lower = more strict and deterministic; higher = more creative.",
    )
    st.session_state.response_temperature = temp

    st.markdown("##### History")
    if st.button("Clear all history"):
        st.session_state.history = []
        st.success("History cleared for this session.")

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
