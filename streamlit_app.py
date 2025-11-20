import streamlit as st
from groq import Groq
from datetime import datetime
import time

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="AI Career Guidance System",
    page_icon="🚀",
    layout="wide",
)

# -----------------------------------------------------
# SESSION DEFAULTS
# -----------------------------------------------------
if "splash_done" not in st.session_state:
    st.session_state["splash_done"] = False

if "active_page" not in st.session_state:
    st.session_state["active_page"] = "Home"

if "history" not in st.session_state:
    st.session_state["history"] = []

# -----------------------------------------------------
# GLOBAL CSS – NEW PROFESSIONAL DESIGN
# -----------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap');

body {
    font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* App background: clean gradient */
.stApp {
    background: radial-gradient(circle at top left, #1d4ed8 0, transparent 55%),
                radial-gradient(circle at bottom right, #14b8a6 0, transparent 60%),
                #020617;
}
[data-testid="stAppViewContainer"] {
    background: transparent;
}

/* Subtle grid overlay */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(15,23,42,0.25) 1px, transparent 1px),
        linear-gradient(90deg, rgba(15,23,42,0.25) 1px, transparent 1px);
    background-size: 80px 80px;
    opacity: 0.25;
    pointer-events: none;
    z-index: -1;
}

/* Container padding */
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: rgba(15,23,42,0.96);
    border-right: 1px solid rgba(31,41,55,0.9);
    backdrop-filter: blur(22px);
}
section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}
.sidebar-header-title {
    font-size: 1.05rem;
    font-weight: 600;
    margin-bottom: 0.15rem;
}
.sidebar-header-sub {
    font-size: 0.78rem;
    color: #9ca3af;
    margin-bottom: 0.5rem;
}
.sidebar-separator {
    border-bottom: 1px solid #1f2937;
    margin: 0.4rem 0 0.8rem 0;
}
label[data-testid="stMetricLabel"] {
    color: #9ca3af !important;
}

/* Radio in sidebar */
[role="radiogroup"] > label {
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    margin-bottom: 0.25rem;
    font-size: 0.85rem;
}
[role="radiogroup"] > label:hover {
    background: rgba(31,41,55,0.95);
}
[role="radiogroup"] input:checked + div {
    font-weight: 600;
}

/* Root wrapper */
.app-root {
    max-width: 1120px;
    margin: 0 auto;
    padding: 0.5rem 0.8rem 4rem 0.8rem;
}

/* ---------------- SPLASH ----------------- */

.splash-layer {
    position: fixed;
    inset: 0;
    background:
        radial-gradient(circle at 0% 0%, rgba(59,130,246,0.9), transparent 60%),
        radial-gradient(circle at 100% 100%, rgba(45,212,191,0.8), transparent 60%),
        #020617;
    display:flex;
    align-items:center;
    justify-content:center;
    z-index:9999;
}
.splash-card {
    position: relative;
    text-align:left;
    color:#e5e7eb;
    padding: 2.4rem 2.7rem;
    border-radius:28px;
    background:rgba(15,23,42,0.96);
    border:1px solid rgba(148,163,184,0.55);
    min-width:320px;
    max-width:720px;
    box-shadow:0 26px 70px rgba(0,0,0,0.9);
    overflow:hidden;
}
.splash-accent-orb {
    position:absolute;
    width:360px; height:360px;
    border-radius:999px;
    background:radial-gradient(circle, rgba(56,189,248,0.7), transparent 65%);
    right:-160px; top:-160px;
    opacity:0.4;
}
.splash-card-inner {
    position:relative;
}
.splash-pill {
    display:inline-flex;
    align-items:center;
    gap:0.45rem;
    padding:0.2rem 0.9rem;
    border-radius:999px;
    background:rgba(15,23,42,0.98);
    border:1px solid rgba(148,163,184,0.55);
    font-size:0.75rem;
    margin-bottom:0.9rem;
}
.splash-pill-dot {
    width:10px; height:10px;
    border-radius:999px;
    background:#22c55e;
}
.splash-welcome {
    font-family:"Plus Jakarta Sans", system-ui;
    font-size:2.4rem;
    font-weight:700;
    letter-spacing:0.16em;
    margin-bottom:0.4rem;
}
.splash-title-main {
    font-family:"Plus Jakarta Sans", system-ui;
    font-size:1.4rem;
    font-weight:700;
    margin-bottom:0.35rem;
}
.splash-subline {
    font-size:0.94rem;
    color:#e5e7eb;
    margin-bottom:0.6rem;
}
.splash-desc {
    font-size:0.82rem;
    color:#9ca3af;
    margin-bottom:1.15rem;
    max-width:480px;
}
.splash-buttons {
    display:flex;
    gap:0.7rem;
    flex-wrap:wrap;
    margin-bottom:1.0rem;
}
.splash-btn-primary {
    padding:0.55rem 1.5rem;
    border-radius:999px;
    border:none;
    background:linear-gradient(135deg,#4f46e5,#22c55e);
    color:#f9fafb;
    font-size:0.9rem;
    font-weight:600;
}
.splash-btn-secondary {
    padding:0.5rem 1.1rem;
    border-radius:999px;
    border:1px solid rgba(148,163,184,0.6);
    background:transparent;
    color:#e5e7eb;
    font-size:0.8rem;
}
.splash-footer-row {
    display:flex;
    align-items:center;
    justify-content:space-between;
    flex-wrap:wrap;
    gap:0.5rem;
    font-size:0.78rem;
    color:#9ca3af;
}
.splash-ready-pill {
    padding:0.25rem 0.9rem;
    border-radius:999px;
    background:rgba(15,23,42,0.98);
    border:1px solid rgba(34,197,94,0.8);
    font-size:0.75rem;
}

/* -------------- MAIN CARDS (HOME + PAGES) ---------------- */

.surface-card {
    background:rgba(15,23,42,0.98);
    border-radius:22px;
    border:1px solid rgba(148,163,184,0.40);
    padding:1.6rem 1.8rem;
    color:#e5e7eb;
    box-shadow:0 18px 50px rgba(0,0,0,0.75);
}

/* home header */
.home-badge {
    display:inline-flex;
    align-items:center;
    gap:0.45rem;
    padding:0.22rem 0.9rem;
    border-radius:999px;
    background:rgba(15,23,42,0.98);
    border:1px solid rgba(148,163,184,0.55);
    font-size:0.77rem;
    margin-bottom:0.75rem;
}
.home-badge-dot {
    width:9px; height:9px;
    border-radius:999px;
    background:#22c55e;
}
.home-title {
    font-family:"Plus Jakarta Sans", system-ui;
    font-size:1.6rem;
    font-weight:700;
    margin-bottom:0.25rem;
}
.home-subtitle {
    font-size:0.95rem;
    color:#e5e7eb;
    margin-bottom:0.5rem;
}
.home-desc {
    font-size:0.82rem;
    color:#9ca3af;
    max-width:640px;
    margin-bottom:1.2rem;
}

/* feature cards row */
.feature-grid {
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(220px,1fr));
    gap:0.9rem;
}
.feature-card {
    border-radius:14px;
    border:1px solid rgba(148,163,184,0.45);
    background:rgba(15,23,42,0.98);
    padding:0.9rem 1rem;
    font-size:0.82rem;
}
.feature-title {
    font-weight:600;
    margin-bottom:0.2rem;
}
.feature-desc {
    font-size:0.78rem;
    color:#9ca3af;
    margin-bottom:0.7rem;
}
.feature-btn {
    padding:0.4rem 0.95rem;
    border-radius:999px;
    border:none;
    background:#22c55e;
    color:#020617;
    font-size:0.8rem;
    font-weight:600;
}

/* footer note inside main card */
.surface-footer-row {
    display:flex;
    align-items:center;
    justify-content:space-between;
    flex-wrap:wrap;
    gap:0.5rem;
    margin-top:0.9rem;
    font-size:0.78rem;
    color:#9ca3af;
}
.surface-footer-pill {
    padding:0.2rem 0.85rem;
    border-radius:999px;
    background:rgba(15,23,42,0.96);
    border:1px solid rgba(34,197,94,0.8);
}

/* section titles */
.section {
    margin: 1.7rem 0;
}
.section-title {
    font-size:0.98rem;
    font-weight:600;
    color:#e5e7eb;
    margin-bottom:0.25rem;
}
.section-sub {
    font-size:0.8rem;
    color:#cbd5f5;
    margin-bottom:0.6rem;
}

/* top careers row */
.top-careers-grid {
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap:0.9rem;
}
.top-career-card {
    border-radius:14px;
    border:1px solid rgba(148,163,184,0.45);
    background:rgba(15,23,42,0.98);
    padding:0.9rem;
    font-size:0.8rem;
    color:#e5e7eb;
}
.top-career-name-row {
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:0.25rem;
}
.top-career-role {
    font-weight:600;
}
.top-career-rating {
    font-size:0.75rem;
    color:#facc15;
}
.top-career-meta {
    font-size:0.76rem;
    color:#9ca3af;
    margin-bottom:0.55rem;
}
.progress-bar {
    width:100%;
    height:7px;
    border-radius:999px;
    background:rgba(15,23,42,0.9);
    overflow:hidden;
    margin-bottom:0.35rem;
}
.progress-fill {
    height:100%;
    border-radius:999px;
    background:linear-gradient(90deg,#22c55e,#a3e635);
}
.top-career-tag {
    font-size:0.72rem;
    color:#a5b4fc;
}

/* career details row */
.career-details-grid {
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap:0.9rem;
}
.career-details-card {
    border-radius:14px;
    border:1px solid rgba(148,163,184,0.45);
    background:rgba(15,23,42,0.98);
    padding:0.95rem;
    font-size:0.8rem;
    color:#e5e7eb;
}
.career-details-card ul {
    padding-left:1rem;
    margin:0.3rem 0 0 0;
}
.career-details-card li {
    margin-bottom:0.22rem;
}

/* form inputs inside page cards */
.surface-card .stTextInput > div > input,
.surface-card .stTextArea > div > textarea {
    background: rgba(15,23,42,0.96);
    border-radius:10px;
    border:1px solid rgba(148,163,184,0.6);
    color:#e5e7eb;
    font-size:0.86rem;
}
.surface-card .stTextInput > label,
.surface-card .stTextArea > label {
    font-size:0.8rem;
}

/* footer */
.footer {
    background:#020617;
    color:#e5e7eb;
}
.footer-inner {
    max-width:1120px;
    margin:0 auto;
    padding:1.4rem 0.9rem 2rem 0.9rem;
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap:1rem;
    font-size:0.8rem;
}
.footer-logo {
    font-weight:600;
    margin-bottom:0.3rem;
}
.footer-col-title {
    font-weight:600;
    margin-bottom:0.35rem;
}
.footer-link {
    color:#9ca3af;
    margin-bottom:0.18rem;
}
.footer-link a {
    color:#9ca3af;
    text-decoration:none;
}
.footer-link a:hover {
    text-decoration:underline;
}

/* mobile */
@media (max-width: 640px) {
    .app-root {
        padding:0.6rem 0.4rem 3rem 0.4rem;
    }
    .surface-card {
        padding:1.2rem 1.2rem;
    }
    .splash-card {
        margin:0 1rem;
        padding:1.8rem 1.6rem;
    }
    .splash-title-main {
        font-size:1.25rem;
    }
    .splash-welcome {
        font-size:2.0rem;
    }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -----------------------------------------------------
# SPLASH (WELCOME)
# -----------------------------------------------------
def show_splash():
    html = """
    <div class="splash-layer">
      <div class="splash-card">
        <div class="splash-accent-orb"></div>
        <div class="splash-card-inner">
          <div class="splash-pill">
            <div class="splash-pill-dot"></div>
            <span>Created by <strong>Niyaz Khan</strong></span>
          </div>
          <div class="splash-welcome">WELCOME</div>
          <div class="splash-title-main">AI Career Guidance System</div>
          <div class="splash-subline">
            Smart, AI-powered career guidance for students, freshers, and career switchers.
          </div>
          <div class="splash-desc">
            Get personalised career paths, skill roadmaps, and learning suggestions –
            all generated by AI based on your goals, skills, and interests.
          </div>
          <div class="splash-buttons">
            <button class="splash-btn-primary">Get started</button>
            <button class="splash-btn-secondary">View dashboard</button>
          </div>
          <div class="splash-footer-row">
            <span>AI-powered insights · Skill-first planning · India focused</span>
            <span class="splash-ready-pill">Ready whenever you are</span>
          </div>
        </div>
      </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)

if not st.session_state["splash_done"]:
    show_splash()
    time.sleep(4)
    st.session_state["splash_done"] = True
    st.rerun()

# -----------------------------------------------------
# GROQ CLIENT & HELPERS
# -----------------------------------------------------
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

def call_groq(prompt: str) -> str:
    try:
        resp = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[{"role": "user", "content": prompt}],
        )
        return resp.choices[0].message.content
    except Exception as e:
        return f"❌ API Error: {e}"

def get_career_advice(interests, skills, education, goals):
    prompt = f"""
You are an expert AI career counselor for Indian students.

Interests: {interests}
Skills: {skills}
Education: {education}
Career Goals: {goals}

Provide a structured, detailed career guidance including:

1. Best 4 Career Options  
2. Required Skills  
3. Missing Skills & How to Improve  
4. Step-by-step Career Roadmap  
5. Salary Range in INR  
6. Best Learning Resources  
7. Resume Tips  
8. Interview Preparation Tips

Format the output clearly using headings and bullet points.
"""
    return call_groq(prompt)

def get_career_chart_overview(name, skills, interests):
    prompt = f"""
You are an AI career mentor. Create a friendly, clear career chart overview for this user.

Name: {name}
Skills: {skills}
Interests: {interests}

Provide:

1. A short summary of their profile  
2. 3–5 suitable career paths  
3. A simple "career chart" text:
   - Stage 1: Where they are now
   - Stage 2: Next 1–2 roles
   - Stage 3: Senior roles
4. Key skills they should focus on  
5. Suggested learning plan (bullet points)

Use headings and bullet points. Keep it concise but useful.
"""
    return call_groq(prompt)

# -----------------------------------------------------
# SIDEBAR NAV
# -----------------------------------------------------
nav_items = [
    "Home",
    "Career Chart",
    "Career Guide",
    "Library",
    "History",
    "Settings",
    "About",
    "Contact",
]

with st.sidebar:
    st.markdown('<div class="sidebar-header-title">AI Career Navigator</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-header-sub">Guided by AI insights</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-separator"></div>', unsafe_allow_html=True)

    choice = st.radio(
        "Navigation",
        nav_items,
        label_visibility="collapsed",
        index=nav_items.index(st.session_state["active_page"]),
    )
    st.session_state["active_page"] = choice

# -----------------------------------------------------
# HOME PAGE
# -----------------------------------------------------
def page_home():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)

    st.markdown('<div class="surface-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="home-badge">
          <div class="home-badge-dot"></div>
          <span>Career assistant by <strong>Niyaz Khan</strong></span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="home-title">AI Career Guidance System</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="home-subtitle">Plan your next career move with data-backed, AI-generated suggestions.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="home-desc">
          Answer a few questions, get curated role suggestions, growth paths, and learning plans
          based on your skills, interests, and target role – built specially for Indian students
          and freshers entering tech.
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">🎯 Career Chart</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="feature-desc">High-level map of your options: stages, possible roles, and the direction you should move in.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Open Career Chart", key="home_chart_btn"):
            st.session_state["active_page"] = "Career Chart"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-title">🧠 Full Career Guide</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="feature-desc">Detailed report with 4 best-fit roles, skills to build, salary ranges, and learning resources.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Open Career Guide", key="home_guide_btn"):
            st.session_state["active_page"] = "Career Guide"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="surface-footer-row">
          <span>AI-powered insights · Built for CS/IT, analytics & tech-aligned roles</span>
          <span class="surface-footer-pill">Start with one profile today</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)  # surface-card

    # Top careers row
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Top careers we usually recommend</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Based on demand, growth, and entry options for Indian graduates.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="top-careers-grid">
          <div class="top-career-card">
            <div class="top-career-name-row">
              <span class="top-career-role">Software Engineer</span>
              <span class="top-career-rating">4.7 / 5 ⭐</span>
            </div>
            <div class="top-career-meta">6–24 LPA · Strong product & service demand</div>
            <div class="progress-bar"><div class="progress-fill" style="width:88%;"></div></div>
            <div class="top-career-tag">Good if you enjoy coding, problem solving, and building products.</div>
          </div>

          <div class="top-career-card">
            <div class="top-career-name-row">
              <span class="top-career-role">Data Analyst</span>
              <span class="top-career-rating">4.5 / 5 ⭐</span>
            </div>
            <div class="top-career-meta">5–18 LPA · Business + analytics hybrid</div>
            <div class="progress-bar"><div class="progress-fill" style="width:82%;"></div></div>
            <div class="top-career-tag">Great fit if you like numbers, dashboards, and business insights.</div>
          </div>

          <div class="top-career-card">
            <div class="top-career-name-row">
              <span class="top-career-role">DevOps / Cloud Engineer</span>
              <span class="top-career-rating">4.4 / 5 ⭐</span>
            </div>
            <div class="top-career-meta">7–28 LPA · High growth & infra-focused</div>
            <div class="progress-bar"><div class="progress-fill" style="width:80%;"></div></div>
            <div class="top-career-tag">Best for people who enjoy automation, reliability, and tooling.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # career details section
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">How to use this tool effectively</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Use the guide as a starting point – then iterate based on your learning speed and interest.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="career-details-grid">
          <div class="career-details-card">
            <strong>What the AI does for you</strong>
            <ul>
              <li>Maps your skills & interests to realistic job roles.</li>
              <li>Highlights missing skills instead of only telling you what you already know.</li>
              <li>Suggests learning paths that are achievable in 3–6 months.</li>
            </ul>
          </div>
          <div class="career-details-card">
            <strong>What you should focus on now</strong>
            <ul>
              <li>Pick one target role and commit for at least 8–12 weeks.</li>
              <li>Build 2–3 small projects and share them on GitHub & LinkedIn.</li>
              <li>Track progress weekly instead of comparing with others daily.</li>
            </ul>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # app-root

# -----------------------------------------------------
# CAREER CHART PAGE
# -----------------------------------------------------
def page_career_chart():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown('<div class="surface-card">', unsafe_allow_html=True)

    st.markdown("#### 📊 AI Career Chart", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.84rem;color:#9ca3af;margin-top:-0.25rem;'>"
        "Get a high-level view of your possible path from today to senior roles."
        "</p>",
        unsafe_allow_html=True,
    )

    name = st.text_input("Your Name (optional)")
    skills = st.text_area("Your key skills", placeholder="e.g. Python, SQL, problem solving, communication")
    interests = st.text_area("Your interests", placeholder="e.g. building apps, finance, design, research")

    if st.button("Generate Career Chart", use_container_width=True):
        if not skills.strip() or not interests.strip():
            st.error("⚠️ Please fill at least skills and interests.")
        else:
            with st.spinner("AI is creating your career chart overview..."):
                overview = get_career_chart_overview(
                    name.strip() or "User",
                    skills.strip(),
                    interests.strip(),
                )
            st.markdown("### 📄 Your AI Career Chart Overview")
            st.write(overview)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# CAREER GUIDE (FULL REPORT)
# -----------------------------------------------------
def page_career_guide():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown('<div class="surface-card">', unsafe_allow_html=True)

    st.markdown("#### 🧠 Full AI Career Guide", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.84rem;color:#9ca3af;margin-top:-0.25rem;'>"
        "Fill this once to generate a detailed report with roles, skills, salary ranges and learning resources."
        "</p>",
        unsafe_allow_html=True,
    )

    name = st.text_input("Your Name")
    interests = st.text_input("Your Interests (e.g. Coding, Finance, Design)")
    skills = st.text_input("Your Skills (e.g. Python, Excel, Communication)")
    education = st.text_input("Your Education (e.g. B.Tech CSE, B.Com)")
    goals = st.text_input("Your Target Role (e.g. DevOps Engineer, Data Scientist)")

    if st.button("Generate Career Guidance", use_container_width=True):
        if not all([name.strip(), interests.strip(), skills.strip(), education.strip(), goals.strip()]):
            st.error("⚠️ Please fill all fields.")
        else:
            with st.spinner("Analyzing your profile and generating guidance..."):
                advice = get_career_advice(
                    interests.strip(),
                    skills.strip(),
                    education.strip(),
                    goals.strip(),
                )
            st.session_state["history"].append(
                {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "name": name,
                    "interests": interests,
                    "skills": skills,
                    "education": education,
                    "goals": goals,
                    "advice": advice,
                }
            )
            st.markdown("### 📄 Your AI Career Guidance")
            st.write(advice)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# LIBRARY
# -----------------------------------------------------
def page_library():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown('<div class="surface-card">', unsafe_allow_html=True)

    st.markdown("#### 📚 Learning Library", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.84rem;color:#9ca3af;margin-top:-0.25rem;'>"
        "Starter list of resources. Later you can replace these with your own curated playlists."
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
- **Data Science / ML** – Kaggle, fast.ai, Analytics Vidhya  
- **Web Development** – MDN Docs, FreeCodeCamp, Frontend Mentor  
- **DevOps & Cloud** – KodeKloud labs, Kubernetes docs, AWS free tier  
- **System Design** – Grokking System Design, Gaurav Sen, Hussein Nasser  
- **DSA & Interviews** – LeetCode, InterviewBit, Striver’s DSA Sheet  
        """
    )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# HISTORY
# -----------------------------------------------------
def page_history():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown('<div class="surface-card">', unsafe_allow_html=True)

    st.markdown("#### 📁 Career Guidance History", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.84rem;color:#9ca3af;margin-top:-0.25rem;'>"
        "All reports generated in this session are stored here."
        "</p>",
        unsafe_allow_html=True,
    )

    hist = st.session_state["history"]
    if not hist:
        st.info("No history yet. Use AI Career Guide to generate your first report.")
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        return

    for i, item in enumerate(reversed(hist), start=1):
        with st.expander(f"{i}. {item['time']} — {item['name']} ({item['goals']})"):
            st.write(f"**Interests:** {item['interests']}")
            st.write(f"**Skills:** {item['skills']}")
            st.write(f"**Education:** {item['education']}")
            st.write(f"**Goals:** {item['goals']}")
            st.markdown("---")
            st.write(item["advice"])

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# SETTINGS
# -----------------------------------------------------
def page_settings():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown('<div class="surface-card">', unsafe_allow_html=True)

    st.markdown("#### ⚙️ Settings", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.84rem;color:#9ca3af;margin-top:-0.25rem;'>"
        "Control what is stored in your current session."
        "</p>",
        unsafe_allow_html=True,
    )

    if st.button("Clear Career Guidance History", use_container_width=True):
        st.session_state["history"] = []
        st.success("History cleared for this session.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# ABOUT
# -----------------------------------------------------
def page_about():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown('<div class="surface-card">', unsafe_allow_html=True)

    st.markdown("#### ℹ️ About this Project", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.84rem;color:#9ca3af;margin-top:-0.25rem;'>"
        "Built as a personal project by Niyaz Khan to guide Indian students and freshers in tech careers."
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
**AI Career Guidance System** is designed to help:

- Students exploring tech & business-aligned roles  
- Freshers confused between DevOps, Data, Backend, etc.  
- Professionals planning a career switch into IT / AI / Cloud  

The app uses **Large Language Models (LLMs)** via **Groq** with a
modern **Python + Streamlit** frontend.
        """
    )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# CONTACT
# -----------------------------------------------------
def page_contact():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown('<div class="surface-card">', unsafe_allow_html=True)

    st.markdown("#### 📬 Contact", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.84rem;color:#9ca3af;margin-top:-0.25rem;'>"
        "Send feedback or collaborate on improving this career guidance system."
        "</p>",
        unsafe_allow_html=True,
    )

    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message", height=150)

    if st.button("Send", use_container_width=True):
        if not name.strip() or not email.strip() or not message.strip():
            st.error("⚠️ Please fill all fields.")
        else:
            st.success("✅ Message captured locally (you can connect this to email or a database later).")

    st.markdown("---")
    st.markdown("##### My Contact Details")
    st.markdown("- 📧 **Email**: [niyaz.kofficials@gmail.com](mailto:niyaz.kofficials@gmail.com)")
    st.markdown("- 📱 **Phone**: [+91 7751931035](tel:+917751931035)")
    st.markdown("- 🔗 **LinkedIn**: [linkedin.com/in/iamnk7](https://linkedin.com/in/iamnk7)")
    st.markdown("- 🐙 **GitHub**: [github.com/Iamnk07](https://github.com/Iamnk07)")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# FOOTER
# -----------------------------------------------------
def render_footer():
    st.markdown(
        """
        <div class="footer">
          <div class="footer-inner">
            <div>
              <div class="footer-logo">AI Career Guidance System</div>
              <div class="footer-link">
                Built by Niyaz Khan · AI-powered planning for students & early-career professionals.
              </div>
            </div>
            <div>
              <div class="footer-col-title">Navigation</div>
              <div class="footer-link">🏠 Home</div>
              <div class="footer-link">🧠 Career Guide</div>
              <div class="footer-link">📊 Career Chart</div>
              <div class="footer-link">📚 Library</div>
            </div>
            <div>
              <div class="footer-col-title">Support</div>
              <div class="footer-link">❓ Help (coming soon)</div>
              <div class="footer-link">📄 FAQ (coming soon)</div>
              <div class="footer-link">🔐 Privacy Policy (coming soon)</div>
            </div>
            <div>
              <div class="footer-col-title">Contact & Social</div>
              <div class="footer-link">📧 <a href="mailto:niyaz.kofficials@gmail.com">niyaz.kofficials@gmail.com</a></div>
              <div class="footer-link">📱 <a href="tel:+917751931035">+91 7751931035</a></div>
              <div class="footer-link">🔗 <a href="https://linkedin.com/in/iamnk7" target="_blank">linkedin.com/in/iamnk7</a></div>
              <div class="footer-link">🐙 <a href="https://github.com/Iamnk07" target="_blank">github.com/Iamnk07</a></div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------
# ROUTER
# -----------------------------------------------------
page = st.session_state["active_page"]

if page == "Home":
    page_home()
elif page == "Career Chart":
    page_career_chart()
elif page == "Career Guide":
    page_career_guide()
elif page == "Library":
    page_library()
elif page == "History":
    page_history()
elif page == "Settings":
    page_settings()
elif page == "About":
    page_about()
elif page == "Contact":
    page_contact()

render_footer()
