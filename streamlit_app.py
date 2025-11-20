import streamlit as st
from groq import Groq
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
# CUSTOM CSS FOR PRO UI
# -----------------------------------------------------
st.markdown(
    """
    <style>
        /* Global styles */
        .stApp {
            background: radial-gradient(circle at top left, #0f172a 0, #020617 45%, #020617 100%);
            color: #e5e7eb;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text",
                         "Segoe UI", sans-serif;
        }

        /* Main container */
        .main-block {
            background: rgba(15, 23, 42, 0.9);
            border-radius: 24px;
            padding: 1.8rem 2rem;
            border: 1px solid rgba(148, 163, 184, 0.25);
            box-shadow: 0 22px 45px rgba(15, 23, 42, 0.9);
        }

        /* Title area */
        .hero-title {
            font-size: 2.1rem;
            font-weight: 700;
            letter-spacing: 0.04em;
            background: linear-gradient(120deg, #38bdf8, #a855f7, #f97316);
            -webkit-background-clip: text;
            color: transparent;
            margin-bottom: 0.4rem;
        }

        .hero-subtitle {
            font-size: 0.95rem;
            color: #cbd5f5;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.25rem 0.7rem;
            border-radius: 999px;
            font-size: 0.75rem;
            background: rgba(15, 23, 42, 0.9);
            border: 1px solid rgba(148, 163, 184, 0.45);
            color: #e5e7eb;
        }

        .pill-dot {
            width: 8px;
            height: 8px;
            border-radius: 999px;
            background: #22c55e;
            box-shadow: 0 0 12px #22c55e;
        }

        .metric-card {
            background: radial-gradient(circle at top left, #1f2937 0, #020617 70%);
            border-radius: 18px;
            padding: 0.9rem 1rem;
            border: 1px solid rgba(31, 41, 55, 0.7);
        }

        .metric-label {
            font-size: 0.75rem;
            color: #9ca3af;
        }

        .metric-value {
            font-size: 1.1rem;
            font-weight: 600;
            color: #e5e7eb;
        }

        .metric-badge {
            font-size: 0.7rem;
            padding: 0.15rem 0.55rem;
            border-radius: 999px;
            background: rgba(22, 163, 74, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.35);
            color: #bbf7d0;
        }

        /* Chat-like response box */
        .ai-response {
            background: radial-gradient(circle at top left, #0b1120 0, #020617 70%);
            border-radius: 18px;
            padding: 1rem 1.15rem;
            border: 1px solid rgba(148, 163, 184, 0.55);
            margin-top: 0.75rem;
            font-size: 0.92rem;
            line-height: 1.55;
        }

        .ai-header {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            margin-bottom: 0.5rem;
            font-size: 0.8rem;
            color: #9ca3af;
        }

        .ai-avatar {
            width: 26px;
            height: 26px;
            border-radius: 999px;
            background: radial-gradient(circle at top, #38bdf8 0, #0f172a 70%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.85rem;
            color: #e5e7eb;
            border: 1px solid rgba(148, 163, 184, 0.7);
        }

        /* Tabs */
        button[data-baseweb="tab"] {
            font-size: 0.85rem !important;
        }

        /* Footer */
        .footer {
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid rgba(31, 41, 55, 0.8);
            font-size: 0.8rem;
            color: #9ca3af;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            row-gap: 0.5rem;
        }

        .footer-links {
            display: flex;
            gap: 0.9rem;
            flex-wrap: wrap;
        }

        .footer a {
            color: #e5e7eb;
            text-decoration: none;
            font-size: 0.8rem;
        }

        .footer a:hover {
            text-decoration: underline;
        }

        @media (max-width: 768px) {
            .hero-title {
                font-size: 1.6rem;
            }
            .main-block {
                padding: 1.2rem 1.15rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------
# INIT SESSION
# -----------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []

# -----------------------------------------------------
# GROQ CLIENT
# -----------------------------------------------------
@st.cache_resource(show_spinner=False)
def get_groq_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])


client = get_groq_client()

# -----------------------------------------------------
# LLM CALLER
# -----------------------------------------------------
SYSTEM_PROMPT = """
You are an AI Career Guidance Assistant created for students and early-career professionals.
You must be:
- Specific, practical and structured.
- Clear about SHORT-TERM (0–3 months), MID-TERM (3–12 months) and LONG-TERM (1–3 years) steps.
- Focused on tech roles like Software Engineer, Data Scientist, ML Engineer, DevOps, etc., but able to advise any knowledge role.
Return answers in clean markdown with headings, bullet points, and tables when useful.
Keep language friendly, simple and motivating.
"""

def get_career_guidance(user_profile: dict, mode: str = "career") -> str:
    """
    mode:
      - 'career'   : overall direction + roadmap
      - 'skills'   : skill gap and learning plan
      - 'interview': interview prep tips & sample Qs
    """
    profile_text = f"""
Name: {user_profile.get("name") or "Not provided"}
Current Education: {user_profile.get("education")}
Degree / Branch: {user_profile.get("degree")}
Year / Experience: {user_profile.get("year_or_exp")}
Key Skills: {", ".join(user_profile.get("skills", [])) or "Not specified"}
Other Skills (text): {user_profile.get("skills_text") or "Not specified"}
Interests: {", ".join(user_profile.get("interests", [])) or "Not specified"}
Preferred Roles: {user_profile.get("preferred_roles") or "Not specified"}
Target Domain: {user_profile.get("target_domain") or "Not specified"}
Location Preference: {user_profile.get("location_pref") or "Not specified"}
Work Style: {user_profile.get("work_style") or "Not specified"}
Risk Preference: {user_profile.get("risk_pref") or "Not specified"}
Priority: {user_profile.get("priority") or "Not specified"}
Extra Notes: {user_profile.get("notes") or "None"}
    """

    if mode == "career":
        task = "Give a detailed, practical career guidance plan and next steps."
    elif mode == "skills":
        task = (
            "Do a skill-gap analysis for the target roles and suggest a structured "
            "learning roadmap with resources categories (not links)."
        )
    else:  # interview
        task = (
            "Help with interview preparation: key topics, how to tell their story, "
            "and 8–10 targeted sample questions with strong answer outlines."
        )

    user_message = f"""{task}

User Profile:
{profile_text}
"""

    completion = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        temperature=0.6,
        max_tokens=2048,
    )
    return completion.choices[0].message.content


# -----------------------------------------------------
# HEADER / HERO
# -----------------------------------------------------
col_logo, col_title = st.columns([0.18, 0.82])
with col_logo:
    st.markdown(
        """
        <div style="width:70px;height:70px;border-radius:24px;
                    background:radial-gradient(circle at top,#38bdf8,#1d4ed8,#020617);
                    display:flex;align-items:center;justify-content:center;
                    border:1px solid rgba(148,163,184,0.7);">
            <span style="font-size:1.8rem;">🧭</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col_title:
    st.markdown(
        """
        <div class="pill">
            <span class="pill-dot"></span>
            <span>AI-Powered • Career Guidance System</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="hero-title">AI Career Guidance System</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">'
        'Smart, personalised career direction for students & early-career professionals — '
        'built with Groq, Streamlit and LLMs.'
        "</div>",
        unsafe_allow_html=True,
    )

st.markdown("")  # spacing

left_metrics, right_metrics = st.columns([0.55, 0.45])

with left_metrics:
    st.markdown('<div class="main-block">', unsafe_allow_html=True)
    st.markdown("#### 🎯 What do you want to figure out today?")
    st.write(
        "Use the tabs below to get a **career roadmap**, discover **skill gaps**, "
        "or prepare for **interviews** – all tailored to your profile."
    )
    st.markdown("</div>", unsafe_allow_html=True)

with right_metrics:
    st.markdown('<div class="main-block">', unsafe_allow_html=True)
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Focus Area</div>
                <div class="metric-value">Tech Careers</div>
                <div class="metric-badge">Students & Freshers</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-label">Guidance Style</div>
                <div class="metric-value">Action-Oriented</div>
                <div class="metric-badge">Roadmaps & Steps</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">Session</div>
                <div class="metric-value">{datetime.now().strftime("%b %d")}</div>
                <div class="metric-badge">Powered by Groq</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("")  # spacing

# -----------------------------------------------------
# TABS LAYOUT
# -----------------------------------------------------
tab1, tab2, tab3 = st.tabs(
    ["🧭 Career Direction", "🧩 Skill Gap & Roadmap", "🎙️ Interview Prep"]
)

# Common fields
EDU_OPTIONS = [
    "B.Tech / B.E.",
    "B.Sc",
    "BCA",
    "M.Tech / M.E.",
    "M.Sc",
    "MCA",
    "Diploma",
    "Working Professional",
    "Other",
]

INTEREST_OPTIONS = [
    "Software Development",
    "Web Development",
    "Mobile Apps",
    "Data Science / Analytics",
    "Machine Learning / AI",
    "DevOps / Cloud",
    "Cyber Security",
    "Product Management",
    "UI/UX & Design",
]

SKILL_OPTIONS = [
    "Python",
    "Java",
    "C++",
    "JavaScript",
    "HTML/CSS",
    "React",
    "Node.js",
    "SQL",
    "MongoDB",
    "Data Structures & Algorithms",
    "Machine Learning",
    "Deep Learning",
    "Cloud (AWS / GCP / Azure)",
    "Docker / Kubernetes",
    "Linux",
    "Power BI / Tableau",
]

# -----------------------------------------------------
# TAB 1 – CAREER DIRECTION
# -----------------------------------------------------
with tab1:
    left, right = st.columns([0.55, 0.45])

    with left:
        st.subheader("Tell me about yourself")
        with st.form("career_form"):
            name = st.text_input("Name (optional)", placeholder="Niyaz Khan")
            education = st.selectbox("Current education level", EDU_OPTIONS, index=0)
            degree = st.text_input(
                "Degree / Branch / Major",
                placeholder="B.Tech in Computer Science",
            )
            year_or_exp = st.text_input(
                "Current year or experience",
                placeholder="Final year / Fresher / 1 year exp, etc.",
            )

            skills = st.multiselect(
                "Your current skills",
                options=SKILL_OPTIONS,
            )
            skills_text = st.text_area(
                "Other skills (optional)",
                placeholder="e.g. Git, problem solving, communication, leadership…",
                height=80,
            )

            interests = st.multiselect(
                "What are you interested in?",
                options=INTEREST_OPTIONS,
            )

            preferred_roles = st.text_input(
                "What kind of roles are you thinking about?",
                placeholder="e.g. Software Engineer, Data Scientist, ML Engineer…",
            )
            target_domain = st.text_input(
                "Target domain / industry (optional)",
                placeholder="e.g. FinTech, AI startups, MNC, Remote product company…",
            )

            col_a, col_b, col_c = st.columns(3)
            with col_a:
                location_pref = st.selectbox(
                    "Location preference",
                    ["No preference", "Tier-1 cities", "Remote", "Abroad"],
                )
            with col_b:
                work_style = st.selectbox(
                    "Work style",
                    ["No preference", "Office", "Hybrid", "Remote"],
                )
            with col_c:
                risk_pref = st.selectbox(
                    "Risk preference",
                    ["Balanced", "Risk-taking (startups)", "Stable (MNC / service)"],
                )

            priority = st.selectbox(
                "What is your top priority right now?",
                [
                    "Get my first job / internship",
                    "Build strong fundamentals",
                    "Switch domain / role",
                    "Higher studies planning",
                ],
            )

            notes = st.text_area(
                "Anything else I should know?",
                placeholder="Share your constraints, dreams, companies you like, etc.",
            )

            submitted = st.form_submit_button("Generate Career Guidance 🚀")

        if submitted:
            profile = {
                "name": name,
                "education": education,
                "degree": degree,
                "year_or_exp": year_or_exp,
                "skills": skills,
                "skills_text": skills_text,
                "interests": interests,
                "preferred_roles": preferred_roles,
                "target_domain": target_domain,
                "location_pref": location_pref,
                "work_style": work_style,
                "risk_pref": risk_pref,
                "priority": priority,
                "notes": notes,
            }

            with st.spinner("Thinking about your profile and building a roadmap..."):
                try:
                    answer = get_career_guidance(profile, mode="career")
                    st.session_state.history.append(
                        {"mode": "career", "profile": profile, "answer": answer}
                    )
                except Exception as e:
                    answer = f"❌ There was an error while contacting the model:\n\n`{e}`"

            st.markdown(
                """
                <div class="ai-response">
                    <div class="ai-header">
                        <div class="ai-avatar">AI</div>
                        <div>AI Career Guide • Personalised plan</div>
                    </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown(answer)
            st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.subheader("Session History")
        if not st.session_state.history:
            st.info(
                "No sessions yet. Submit the form on the left to generate your first "
                "career guidance plan."
            )
        else:
            for i, item in enumerate(reversed(st.session_state.history[-5:]), start=1):
                st.markdown(f"**#{i}. {item['mode'].title()} guidance**")
                small_profile = item["profile"]
                st.caption(
                    f"{small_profile.get('education', '')} | "
                    f"{small_profile.get('degree', '')} | "
                    f"{small_profile.get('year_or_exp', '')}"
                )

# -----------------------------------------------------
# TAB 2 – SKILL GAP & ROADMAP
# -----------------------------------------------------
with tab2:
    st.subheader("Understand your skill gap and build a focused learning plan")

    with st.form("skills_form"):
        edu2 = st.selectbox("Current education / status", EDU_OPTIONS, key="edu2")
        role_target = st.text_input(
            "Target role(s)",
            placeholder="e.g. Data Scientist, Backend Engineer, DevOps Engineer…",
        )
        skills2 = st.multiselect(
            "Current skills",
            options=SKILL_OPTIONS,
            key="skills2",
        )
        skills2_text = st.text_area(
            "Other skills / tools you know",
            placeholder="e.g. pandas, NumPy, FastAPI, Firebase…",
            height=80,
            key="skills2_text",
        )
        time_per_week = st.slider(
            "How many hours per week can you study?",
            min_value=3,
            max_value=40,
            value=10,
            step=1,
        )
        duration = st.selectbox(
            "Planning horizon",
            ["1 month", "3 months", "6 months"],
            index=1,
        )

        notes2 = st.text_area(
            "Constraints / preferences (optional)",
            placeholder="e.g. Only free resources, can’t buy paid courses, weak in maths…",
            key="notes2",
        )

        submit_skills = st.form_submit_button("Generate Skill Gap Analysis 📚")

    if submit_skills:
        profile2 = {
            "name": None,
            "education": edu2,
            "degree": "",
            "year_or_exp": "",
            "skills": skills2,
            "skills_text": skills2_text,
            "interests": [],
            "preferred_roles": role_target,
            "target_domain": "",
            "location_pref": "",
            "work_style": "",
            "risk_pref": "",
            "priority": f"Skill growth over {duration}, {time_per_week} hrs/week",
            "notes": notes2,
        }
        with st.spinner("Identifying gaps and designing a learning roadmap..."):
            try:
                answer2 = get_career_guidance(profile2, mode="skills")
                st.session_state.history.append(
                    {"mode": "skills", "profile": profile2, "answer": answer2}
                )
            except Exception as e:
                answer2 = f"❌ There was an error while contacting the model:\n\n`{e}`"

        st.markdown(
            """
            <div class="ai-response">
                <div class="ai-header">
                    <div class="ai-avatar">AI</div>
                    <div>Skill Gap Analysis • Learning Plan</div>
                </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(answer2)
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# TAB 3 – INTERVIEW PREP
# -----------------------------------------------------
with tab3:
    st.subheader("Prepare for interviews with targeted guidance")

    with st.form("interview_form"):
        role_int = st.text_input(
            "Target role",
            placeholder="e.g. SDE-1, Data Analyst, DevOps Engineer…",
        )
        company_type = st.selectbox(
            "Company type",
            ["Product (FAANG / MAANG style)", "Service (TCS / Infosys etc.)", "Startup", "Any"],
        )
        experience_int = st.text_input(
            "Experience level",
            placeholder="e.g. Final year / Fresher / 1 year experience…",
        )
        strong_areas = st.text_area(
            "Strong areas",
            placeholder="e.g. DSA, DBMS, OS, OOP, projects in web dev / ML…",
            height=80,
        )
        weak_areas = st.text_area(
            "Weak areas",
            placeholder="e.g. System design, probability & stats, communication…",
            height=80,
        )
        upcoming = st.text_input(
            "Any upcoming interview / company? (optional)",
            placeholder="e.g. TCS NQT, Infosys, J.P. Morgan virtual internship, etc.",
        )

        submit_int = st.form_submit_button("Generate Interview Prep Plan 🎙️")

    if submit_int:
        profile3 = {
            "name": None,
            "education": "",
            "degree": "",
            "year_or_exp": experience_int,
            "skills": [],
            "skills_text": strong_areas,
            "interests": [],
            "preferred_roles": role_int,
            "target_domain": company_type,
            "location_pref": "",
            "work_style": "",
            "risk_pref": "",
            "priority": "Interview preparation",
            "notes": f"Weak areas: {weak_areas}\nUpcoming: {upcoming}",
        }
        with st.spinner("Designing interview strategy, topics and sample questions..."):
            try:
                answer3 = get_career_guidance(profile3, mode="interview")
                st.session_state.history.append(
                    {"mode": "interview", "profile": profile3, "answer": answer3}
                )
            except Exception as e:
                answer3 = f"❌ There was an error while contacting the model:\n\n`{e}`"

        st.markdown(
            """
            <div class="ai-response">
                <div class="ai-header">
                    <div class="ai-avatar">AI</div>
                    <div>Interview Prep • Strategy & Sample Qs</div>
                </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(answer3)
        st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# FOOTER WITH YOUR CONTACTS / SOCIALS
# -----------------------------------------------------
st.markdown(
    """
    <div class="footer">
        <div>© 2025 AI Career Guidance • Built with ❤️ by Niyaz</div>
        <div class="footer-links">
            <span>📧 <a href="mailto:niyaz.kofficials@gmail.com">niyaz.kofficials@gmail.com</a></span>
            <span>📱 <a href="tel:+917751931035">+91 7751931035</a></span>
            <span>💼 <a href="https://linkedin.com/in/iamnk7" target="_blank">linkedin.com/in/iamnk7</a></span>
            <span>💻 <a href="https://github.com/Iamnk07" target="_blank">github.com/Iamnk07</a></span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
