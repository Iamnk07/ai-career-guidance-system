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
# GLOBAL CSS (BANANI-LIKE + NEW PAGE CARDS)
# -----------------------------------------------------
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700&family=Fredoka:wght@400;600;700&display=swap');

body {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* App background: gradient + blurred circles */
.stApp {
    background: radial-gradient(circle at 10% 20%, #1d4ed8 0, transparent 55%),
                radial-gradient(circle at 80% 80%, #22c55e 0, transparent 55%),
                radial-gradient(circle at 0% 80%, #f97316 0, transparent 55%),
                #020617;
}
[data-testid="stAppViewContainer"] {
    background: transparent;
}

/* subtle grid overlay */
[data-testid="stAppViewContainer"]::before {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(15,23,42,0.35) 1px, transparent 1px),
        linear-gradient(90deg, rgba(15,23,42,0.35) 1px, transparent 1px);
    background-size: 60px 60px;
    opacity: 0.32;
    pointer-events: none;
    z-index: -1;
}

/* Container padding */
.block-container {
    padding-top: 1.0rem;
    padding-bottom: 3rem;
}

/* Sidebar (dark) */
section[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid #111827;
}
section[data-testid="stSidebar"] * {
    color: #e5e7eb !important;
}
.sidebar-header-title {
    font-size: 1.0rem;
    font-weight: 600;
    margin-bottom: 0.2rem;
}
.sidebar-header-sub {
    font-size: 0.75rem;
    color: #9ca3af;
    margin-bottom: 0.6rem;
}
.sidebar-separator {
    border-bottom: 1px solid #1f2937;
    margin: 0.4rem 0 0.6rem 0;
}

/* Root wrapper */
.app-root {
    max-width: 1180px;
    margin: 0 auto;
    padding: 0.5rem 1rem 4rem 1rem;
}

/* ---------------- SPLASH ----------------- */

.splash-layer {
    position: fixed;
    inset: 0;
    background:
        radial-gradient(circle at 10% 20%, rgba(37,99,235,0.9), transparent 55%),
        radial-gradient(circle at 90% 80%, rgba(34,197,94,0.85), transparent 55%),
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
    padding: 2.3rem 2.7rem;
    border-radius:24px;
    background:rgba(15,23,42,0.98);
    border:1px solid rgba(148,163,184,0.7);
    min-width:320px;
    max-width:640px;
    box-shadow:0 24px 60px rgba(0,0,0,0.85);
    overflow:hidden;
}
.splash-gradient-orb-left {
    position:absolute;
    width:340px; height:340px;
    border-radius:999px;
    background:radial-gradient(circle, rgba(56,189,248,0.9), transparent 65%);
    left:-160px; top:-160px;
    opacity:0.4;
}
.splash-gradient-orb-right {
    position:absolute;
    width:340px; height:340px;
    border-radius:999px;
    background:radial-gradient(circle, rgba(249,115,22,0.9), transparent 65%);
    right:-180px; bottom:-180px;
    opacity:0.4;
}
.splash-card-inner {
    position:relative;
}
.splash-pill {
    display:inline-flex;
    align-items:center;
    gap:0.4rem;
    padding:0.2rem 0.9rem;
    border-radius:999px;
    background:rgba(15,23,42,0.95);
    border:1px solid rgba(148,163,184,0.7);
    font-size:0.75rem;
    margin-bottom:0.9rem;
}
.splash-pill-dot {
    width:10px; height:10px;
    border-radius:999px;
    background:#22c55e;
}
.splash-welcome {
    font-family:"Baloo 2", system-ui;
    font-size:2.4rem;
    font-weight:800;
    letter-spacing:0.18em;
    margin-bottom:0.5rem;
}
.splash-title-main {
    font-family:"Fredoka", system-ui;
    font-size:1.4rem;
    font-weight:700;
    margin-bottom:0.3rem;
}
.splash-subline {
    font-size:0.95rem;
    color:#e5e7eb;
    margin-bottom:0.7rem;
}
.splash-desc {
    font-size:0.8rem;
    color:#9ca3af;
    margin-bottom:1.1rem;
}
.splash-buttons {
    display:flex;
    gap:0.7rem;
    flex-wrap:wrap;
    margin-bottom:0.9rem;
}
.splash-btn-primary {
    padding:0.45rem 1.35rem;
    border-radius:999px;
    border:none;
    background:#22c55e;
    color:#020617;
    font-size:0.85rem;
    font-weight:600;
}
.splash-btn-secondary {
    padding:0.45rem 1.0rem;
    border-radius:999px;
    border:none;
    background:transparent;
    color:#e5e7eb;
    font-size:0.8rem;
    text-decoration:underline;
}
.splash-footer-row {
    display:flex;
    align-items:center;
    justify-content:space-between;
    flex-wrap:wrap;
    gap:0.5rem;
    font-size:0.75rem;
    color:#9ca3af;
}
.splash-ready-pill {
    padding:0.25rem 0.9rem;
    border-radius:999px;
    background:rgba(15,23,42,0.95);
    border:1px solid rgba(34,197,94,0.7);
    font-size:0.75rem;
}

/* -------------- MAIN CARDS (HOME + PAGES) ---------------- */

.home-main-card,
.page-card {
    background:rgba(15,23,42,0.97);
    border-radius:24px;
    border:1px solid rgba(148,163,184,0.45);
    padding:1.7rem 1.9rem;
    color:#e5e7eb;
    box-shadow:0 22px 55px rgba(0,0,0,0.85);
}

.home-pill {
    display:inline-flex;
    align-items:center;
    gap:0.4rem;
    padding:0.18rem 0.9rem;
    border-radius:999px;
    background:rgba(15,23,42,0.95);
    border:1px solid rgba(148,163,184,0.6);
    font-size:0.75rem;
    margin-bottom:0.7rem;
}
.home-pill-dot {
    width:9px; height:9px;
    border-radius:999px;
    background:#22c55e;
}
.home-title-main {
    font-family:"Fredoka", system-ui;
    font-size:1.4rem;
    font-weight:700;
    margin-bottom:0.4rem;
}
.home-subline {
    font-size:0.95rem;
    color:#e5e7eb;
    margin-bottom:0.4rem;
}
.home-desc {
    font-size:0.8rem;
    color:#9ca3af;
    max-width:640px;
    margin-bottom:1.2rem;
}

/* feature cards row */
.home-feature-card {
    border-radius:14px;
    border:1px solid rgba(148,163,184,0.5);
    background:rgba(15,23,42,0.96);
    padding:0.9rem;
    font-size:0.82rem;
}
.home-feature-title {
    font-weight:600;
    margin-bottom:0.2rem;
}
.home-feature-desc {
    font-size:0.78rem;
    color:#9ca3af;
    margin-bottom:0.6rem;
}
.home-feature-btn {
    padding:0.4rem 0.9rem;
    border-radius:999px;
    border:none;
    background:#22c55e;
    color:#020617;
    font-size:0.8rem;
    font-weight:600;
}
.home-card-footer {
    display:flex;
    align-items:center;
    justify-content:space-between;
    flex-wrap:wrap;
    gap:0.5rem;
    font-size:0.75rem;
    color:#9ca3af;
    margin-top:0.5rem;
}
.home-card-ready-pill {
    padding:0.2rem 0.9rem;
    border-radius:999px;
    background:rgba(15,23,42,0.96);
    border:1px solid rgba(34,197,94,0.7);
}

/* section titles */
.section {
    margin: 1.8rem 0;
}
.section-title {
    font-size:1.0rem;
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
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap:0.9rem;
}
.top-career-card {
    border-radius:14px;
    border:1px solid rgba(148,163,184,0.45);
    background:rgba(15,23,42,0.97);
    padding:0.9rem;
    font-size:0.8rem;
    color:#e5e7eb;
}
.top-career-name-row {
    display:flex;
    justify-content:space-between;
    align-items:center;
    margin-bottom:0.2rem;
}
.top-career-role {
    font-weight:600;
}
.top-career-rating {
    font-size:0.75rem;
    color:#facc15;
}
.top-career-meta {
    font-size:0.75rem;
    color:#9ca3af;
    margin-bottom:0.5rem;
}
.progress-bar {
    width:100%;
    height:8px;
    border-radius:999px;
    background:rgba(15,23,42,0.9);
    overflow:hidden;
    margin-bottom:0.3rem;
}
.progress-fill {
    height:100%;
    border-radius:999px;
    background:linear-gradient(90deg,#22c55e,#a3e635);
}
.top-career-tag {
    font-size:0.7rem;
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
    background:rgba(15,23,42,0.97);
    padding:0.9rem;
    font-size:0.8rem;
    color:#e5e7eb;
}
.career-details-card ul {
    padding-left:1rem;
    margin:0.3rem 0 0 0;
}
.career-details-card li {
    margin-bottom:0.2rem;
}

/* form inputs inside cards */
.page-card .stTextInput > div > input,
.page-card .stTextArea > div > textarea {
    background: rgba(15,23,42,0.9);
    border-radius: 10px;
    border: 1px solid rgba(148,163,184,0.6);
    color: #e5e7eb;
}
.page-card .stTextInput > label,
.page-card .stTextArea > label {
    font-size: 0.8rem;
}

/* footer */
.footer {
    background:#020617;
    color:#e5e7eb;
}
.footer-inner {
    max-width:1180px;
    margin:0 auto;
    padding:1.4rem 1rem 2rem 1rem;
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap:1rem;
    font-size:0.8rem;
}
.footer-logo {
    font-weight:600;
    margin-bottom:0.25rem;
}
.footer-col-title {
    font-weight:600;
    margin-bottom:0.3rem;
}
.footer-link {
    color:#9ca3af;
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
        padding:0.6rem 0.6rem 3rem 0.6rem;
    }
    .home-main-card,
    .page-card {
        padding:1.1rem 1.2rem;
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
        <div class="splash-gradient-orb-left"></div>
        <div class="splash-gradient-orb-right"></div>
        <div class="splash-card-inner">
          <div class="splash-pill">
            <div class="splash-pill-dot"></div>
            <span>Created by <strong>Niyaz Khan</strong></span>
          </div>
          <div class="splash-welcome">WELCOME</div>
          <div class="splash-title-main">AI Career Guidance System</div>
          <div class="splash-subline">
            Welcome to AI Career Guidance System created by Niyaz Khan.
          </div>
          <div class="splash-desc">
            A smart, AI-powered guide to help you choose your path, grow your skills,
            and shape your career future.
          </div>
          <div class="splash-buttons">
            <button class="splash-btn-primary">Get Started</button>
            <button class="splash-btn-secondary">Learn more</button>
          </div>
          <div class="splash-footer-row">
            <span>AI-powered insights · Personalized roadmaps</span>
            <span class="splash-ready-pill">Ready when you are</span>
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

    # main card
    st.markdown('<div class="home-main-card">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="home-pill">
          <div class="home-pill-dot"></div>
          <span>Created by <strong>Niyaz Khan</strong></span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="home-title-main">AI Career Guidance System</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="home-subline">Welcome to AI Career Guidance System created by Niyaz Khan.</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="home-desc">
          A smart, AI-powered guide to help you explore options, make informed career decisions,
          and grow with confidence in a rapidly changing world of work.
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown('<div class="home-feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="home-feature-title">Career Chart</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="home-feature-desc">Ask questions, explore options, and talk to your AI mentor about roles, skills, and next steps in your path.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Get Career Chart", key="home_chart_btn"):
            st.session_state["active_page"] = "Career Chart"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="home-feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="home-feature-title">Career Guide</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="home-feature-desc">Follow a guided path with personalized roadmaps, milestones, and resources tailored to your goals.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Let\'s Guide", key="home_guide_btn"):
            st.session_state["active_page"] = "Career Guide"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
        <div class="home-card-footer">
          <span>AI-powered insights · Personalized roadmaps</span>
          <span class="home-card-ready-pill">Ready when you are</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)  # card

    # Top careers row
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Top Careers for You</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Balanced market demand, salary growth, and skill match.</div>',
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
            <div class="top-career-meta">Salary: 6–24 LPA · Skill growth</div>
            <div class="progress-bar"><div class="progress-fill" style="width:88%;"></div></div>
            <div class="top-career-tag">🚀 Strong demand across product & service companies.</div>
          </div>

          <div class="top-career-card">
            <div class="top-career-name-row">
              <span class="top-career-role">Data Analyst</span>
              <span class="top-career-rating">4.5 / 5 ⭐</span>
            </div>
            <div class="top-career-meta">Salary: 5–18 LPA · Work–life balance</div>
            <div class="progress-bar"><div class="progress-fill" style="width:82%;"></div></div>
            <div class="top-career-tag">📊 Great for analytical & business-leaning profiles.</div>
          </div>

          <div class="top-career-card">
            <div class="top-career-name-row">
              <span class="top-career-role">Product Manager</span>
              <span class="top-career-rating">4.3 / 5 ⭐</span>
            </div>
            <div class="top-career-meta">Salary: 10–35 LPA · Leadership track</div>
            <div class="progress-bar"><div class="progress-fill" style="width:78%;"></div></div>
            <div class="top-career-tag">🧭 Combines tech, business & communication.</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # career details section
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Career details & next steps</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">Why these careers fit you, and what you should do now.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="career-details-grid">
          <div class="career-details-card">
            <strong>Why these careers match you</strong>
            <ul>
              <li>Align with common CS / IT skills and learning style.</li>
              <li>Strong long-term demand in India & globally.</li>
              <li>Clear roadmap from beginner projects to advanced roles.</li>
            </ul>
          </div>
          <div class="career-details-card">
            <strong>What you should do next</strong>
            <ul>
              <li>Pick 2–3 core skills and build consistency for 2–3 months.</li>
              <li>Follow a curated playlist of tutorials + practice projects.</li>
              <li>Publish your work on GitHub & LinkedIn to build proof.</li>
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
    st.markdown('<div class="page-card">', unsafe_allow_html=True)

    st.markdown("#### 📊 AI Career Chart", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.85rem;color:#9ca3af;margin-top:-0.3rem;'>"
        "Get a quick, high-level view of your career direction based on your skills & interests."
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
    st.markdown('<div class="page-card">', unsafe_allow_html=True)

    st.markdown("#### 🧠 AI Career Guide", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.85rem;color:#9ca3af;margin-top:-0.3rem;'>"
        "Fill this once to get a full, detailed roadmap including roles, skills, salary and resources."
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
    st.markdown('<div class="page-card">', unsafe_allow_html=True)

    st.markdown("#### 📚 Learning Library", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.85rem;color:#9ca3af;margin-top:-0.3rem;'>"
        "Curated resources to learn faster. Later you can replace these with your own playlists."
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
- **Data Science** – Kaggle, fast.ai, Analytics Vidhya  
- **Web Development** – MDN, FreeCodeCamp, Frontend Mentor  
- **DevOps** – KodeKloud, Kubernetes docs, AWS free tier labs  
- **System Design** – Grokking System Design, Gaurav Sen, Hussein Nasser  
- **Interview Prep** – LeetCode, InterviewBit, Striver’s DSA Sheet  
        """
    )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# HISTORY
# -----------------------------------------------------
def page_history():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown('<div class="page-card">', unsafe_allow_html=True)

    st.markdown("#### 📚 Career Guidance History", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.85rem;color:#9ca3af;margin-top:-0.3rem;'>"
        "All guidance generated in this session is saved here so you can revisit it anytime."
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
    st.markdown('<div class="page-card">', unsafe_allow_html=True)

    st.markdown("#### ⚙️ Settings", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.85rem;color:#9ca3af;margin-top:-0.3rem;'>"
        "Manage your session data and future options here."
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
    st.markdown('<div class="page-card">', unsafe_allow_html=True)

    st.markdown("#### ℹ️ About this Project", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.85rem;color:#9ca3af;margin-top:-0.3rem;'>"
        "Built as a personal project by Niyaz Khan to guide students and freshers in tech careers."
        "</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
**AI Career Guidance System** is a personal project created by **Niyaz Khan** to help:

- Students exploring tech & business careers  
- Freshers choosing between roles like DevOps, Data, Backend, etc.  
- Professionals planning a career switch into IT / AI / Cloud  

It uses **Large Language Models (LLMs)** via **Groq**, with a modern
**Python + Streamlit** UI inspired by professional career platforms.
        """
    )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# CONTACT
# -----------------------------------------------------
def page_contact():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown('<div class="page-card">', unsafe_allow_html=True)

    st.markdown("#### 📬 Contact", unsafe_allow_html=True)
    st.markdown(
        "<p style='font-size:0.85rem;color:#9ca3af;margin-top:-0.3rem;'>"
        "Reach out to me or send feedback about this AI career guidance tool."
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
            st.success("✅ Message captured locally (you can connect this to email or DB later).")

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
                Smart, AI-powered suggestions to help you make better career decisions.
              </div>
            </div>
            <div>
              <div class="footer-col-title">Quick Links</div>
              <div class="footer-link">🏠 Home</div>
              <div class="footer-link">🧠 Career Guide</div>
              <div class="footer-link">📊 Career Chart</div>
              <div class="footer-link">📚 Library</div>
            </div>
            <div>
              <div class="footer-col-title">Support</div>
              <div class="footer-link">❓ Help</div>
              <div class="footer-link">📄 FAQ</div>
              <div class="footer-link">🔐 Privacy Policy</div>
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
