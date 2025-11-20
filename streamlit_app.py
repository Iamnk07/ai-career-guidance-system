import streamlit as st
from groq import Groq
from datetime import datetime
import time

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="AI Career Guidance",
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
# GLOBAL CSS (DARK SIDEBAR + RESPONSIVE LAYOUT)
# -----------------------------------------------------
CSS = """
<style>
body {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Main container */
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 3rem;
}

/* Dark corporate sidebar */
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

/* Main content root */
.app-root {
    max-width: 1180px;
    margin: 0 auto;
    padding: 0.5rem 1rem 4rem 1rem;
}

/* Splash */
.splash-layer {
    position: fixed;
    inset: 0;
    background:
        radial-gradient(circle at 10% 20%, rgba(37,99,235,0.9), transparent 55%),
        radial-gradient(circle at 90% 80%, rgba(14,165,233,0.9), transparent 55%),
        #020617;
    display:flex;
    align-items:center;
    justify-content:center;
    z-index:9999;
}
.splash-card {
    position: relative;
    text-align:center;
    color:#e5e7eb;
    padding: 2.2rem 2.6rem;
    border-radius:20px;
    background:rgba(15,23,42,0.96);
    border:1px solid rgba(148,163,184,0.6);
    min-width:260px;
    max-width:400px;
    overflow:hidden;
}
.splash-tetra {
    position:absolute;
    inset:-40%;
    opacity:0.35;
    background:
        conic-gradient(from 180deg, #2563eb, #22c55e, #f97316, #ec4899, #2563eb);
    clip-path: polygon(15% 0%, 85% 0%, 100% 40%, 85% 100%, 15% 100%, 0% 40%);
    animation: splash-rotate 14s linear infinite;
    transform-origin:50% 50%;
}
.splash-title {
    position:relative;
    font-size:clamp(1.6rem, 3vw, 2.1rem);
    font-weight:650;
    margin-bottom:0.4rem;
}
.splash-sub {
    position:relative;
    font-size:0.9rem;
    color:#9ca3af;
    margin-bottom:0.4rem;
}
.splash-author {
    position:relative;
    font-size:0.8rem;
    color:#cbd5f5;
    opacity:0.9;
}
@keyframes splash-rotate {
    0% { transform: rotate3d(1,1,0,18deg); }
    50% { transform: rotate3d(1,1,0,38deg); }
    100% { transform: rotate3d(1,1,0,18deg); }
}

/* Home header text */
.home-header-title {
    font-size:1.5rem;
    font-weight:600;
    margin-bottom:0.25rem;
}
.home-header-sub {
    font-size:0.9rem;
    color:#6b7280;
    margin-bottom:1.3rem;
}

/* Hero */
.hero {
    display:flex;
    flex-wrap:wrap;
    gap:1.8rem;
    align-items:center;
    margin-bottom:1.8rem;
}
.hero-left {
    flex:1 1 260px;
}
.hero-right {
    flex:1 1 260px;
    display:flex;
    align-items:center;
    justify-content:center;
}
.hero-left-title {
    font-size:clamp(1.7rem, 2.6vw, 2.1rem);
    font-weight:650;
    margin-bottom:0.4rem;
}
.hero-left-sub {
    font-size:0.95rem;
    color:#4b5563;
    max-width:460px;
}

/* 3D tetragon design on home */
.tetra-wrapper {
    display:flex;
    justify-content:center;
    align-items:center;
    padding:0.8rem 0;
}
.tetra-plate {
    width:220px;
    height:220px;
    border-radius:22px;
    background:
        conic-gradient(from 210deg, #2563eb, #22c55e, #f97316, #ec4899, #2563eb);
    position:relative;
    transform: rotate3d(1, 1, 0, 30deg);
    animation: tetra-wobble 10s ease-in-out infinite alternate;
    box-shadow:
        0 24px 60px rgba(15,23,42,0.7),
        0 0 80px rgba(37,99,235,0.5);
    overflow:hidden;
}
.tetra-inner {
    position:absolute;
    inset:18%;
    border-radius:18px;
    background:
        radial-gradient(circle at 0% 0%, rgba(15,23,42,0.9), transparent 55%),
        radial-gradient(circle at 100% 100%, rgba(15,118,110,0.8), transparent 45%),
        rgba(15,23,42,0.95);
    border:1px solid rgba(148,163,184,0.35);
    display:flex;
    align-items:center;
    justify-content:center;
    text-align:center;
    color:#e5e7eb;
    font-size:0.85rem;
}
.tetra-orb {
    position:absolute;
    border-radius:999px;
    background:radial-gradient(circle, #e5e7eb 0, #38bdf8 45%, transparent 70%);
    opacity:0.7;
    filter:blur(2px);
}
.tetra-orb.one { width:60px; height:60px; top:12%; left:10%; }
.tetra-orb.two { width:80px; height:80px; bottom:10%; right:12%; }
.tetra-orb.three { width:50px; height:50px; top:55%; left:65%; }

@keyframes tetra-wobble {
    0% { transform: rotate3d(1,1,0,28deg) translateY(0px); }
    50% { transform: rotate3d(1.2,0.8,0,34deg) translateY(-6px); }
    100% { transform: rotate3d(0.9,1.1,0,24deg) translateY(4px); }
}

/* Two cards row */
.two-box-row {
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
    gap:1rem;
    margin:1.4rem 0 1.8rem 0;
}
.card {
    border-radius:0.75rem;
    border:1px solid #e5e7eb;
    background:#ffffff;
    padding:1rem;
    font-size:0.9rem;
}

/* Section generic */
.section {
    margin: 1.8rem 0;
}
.section-title {
    font-size:1.05rem;
    font-weight:600;
    margin-bottom:0.4rem;
}
.section-sub {
    font-size:0.85rem;
    color:#6b7280;
    margin-bottom:0.8rem;
}

/* Top careers cards */
.top-careers-grid {
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap:0.8rem;
}
.top-career-card {
    border-radius:0.75rem;
    border:1px solid #e5e7eb;
    background:#ffffff;
    padding:0.8rem;
    font-size:0.85rem;
}

/* Footer */
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

/* Mobile tweaks */
@media (max-width: 640px) {
    .app-root {
        padding:0.3rem 0.8rem 3rem 0.8rem;
    }
    .hero {
        gap:1rem;
    }
    .tetra-plate {
        width:190px;
        height:190px;
    }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -----------------------------------------------------
# SPLASH (ONCE PER SESSION, 3D-ISH ANIMATED)
# -----------------------------------------------------
def show_splash():
    html = """
    <div class="splash-layer">
      <div class="splash-card">
        <div class="splash-tetra"></div>
        <div class="splash-title">Welcome to AI Career Guidance</div>
        <div class="splash-sub">Your AI companion for career clarity and growth.</div>
        <div class="splash-author">Created by Niyaz</div>
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
3. A simple "career chart" style text, like:
   - Stage 1: Where they are now
   - Stage 2: Next 1–2 roles
   - Stage 3: Senior roles
4. Key skills they should focus on  
5. Suggested learning plan (bullet points)

Use headings and bullet points. Keep it concise but useful.
"""
    return call_groq(prompt)

# -----------------------------------------------------
# SIDEBAR NAV (DARK CORPORATE)
# -----------------------------------------------------
nav_items = [
    "Home",
    "Career Chart",
    "AI Career Guidance",
    "Library",
    "History",
    "Settings",
    "About",
    "Contact",
]

with st.sidebar:
    st.markdown('<div class="sidebar-header-title">AI Career Guidance</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-header-sub">Powered by AI · Designed by Niyaz</div>', unsafe_allow_html=True)
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

    # Header
    st.markdown(
        """
        <div class="home-header-title">Welcome to AI Career Guidance</div>
        <div class="home-header-sub">
            Discover your best career path with AI-powered insights based on your interests and skills.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hero
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    col_left, col_right = st.columns([1.2, 1], gap="large")

    with col_left:
        st.markdown(
            """
            <div class="hero-left">
              <div class="hero-left-title">
                Find your next step with confidence.
              </div>
              <div class="hero-left-sub">
                Start with a quick overview of your career options using the Career Chart,
                then use AI Career Guidance for a detailed roadmap tailored to your goals.
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_right:
        st.markdown(
            """
            <div class="hero-right">
              <div class="tetra-wrapper">
                <div class="tetra-plate">
                    <div class="tetra-orb one"></div>
                    <div class="tetra-orb two"></div>
                    <div class="tetra-orb three"></div>
                    <div class="tetra-inner">
                        3D Career<br/>Intelligence
                    </div>
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)  # close hero

    # Two cards row: Career Chart + AI Guidance
    st.markdown('<div class="two-box-row">', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 📊 Career Chart", unsafe_allow_html=True)
        st.write(
            """
Get a high-level view of your possible career paths based on your
current skills and interests.

Use this when you want a quick overview of where you can go.
            """
        )
        if st.button("Open Career Chart", key="home_career_chart_btn", use_container_width=True):
            st.session_state["active_page"] = "Career Chart"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("### 🧠 AI Career Guidance", unsafe_allow_html=True)
        st.write(
            """
Let the AI analyze your profile and generate a full career guidance report:
roles, skills, roadmap, salary range, and resources.
            """
        )
        if st.button("Start AI Guidance", key="home_ai_btn", use_container_width=True):
            st.session_state["active_page"] = "AI Career Guidance"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close two-box-row

    # Top careers section
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-title">Top careers right now</div>
        <div class="section-sub">High-demand roles you can explore today.</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="top-careers-grid">
          <div class="top-career-card">
            <strong>Data Scientist</strong><br/>
            Salary: 8–30 LPA<br/>
            Difficulty: High<br/>
            Rating: ⭐⭐⭐⭐⭐
          </div>
          <div class="top-career-card">
            <strong>AI / ML Engineer</strong><br/>
            Salary: 10–40 LPA<br/>
            Difficulty: High<br/>
            Rating: ⭐⭐⭐⭐⭐
          </div>
          <div class="top-career-card">
            <strong>Cloud / DevOps Engineer</strong><br/>
            Salary: 8–35 LPA<br/>
            Difficulty: High<br/>
            Rating: ⭐⭐⭐⭐☆
          </div>
          <div class="top-career-card">
            <strong>Cyber Security Engineer</strong><br/>
            Salary: 8–30 LPA<br/>
            Difficulty: High<br/>
            Rating: ⭐⭐⭐⭐⭐
          </div>
          <div class="top-career-card">
            <strong>Full Stack Developer</strong><br/>
            Salary: 6–25 LPA<br/>
            Difficulty: Medium<br/>
            Rating: ⭐⭐⭐⭐☆
          </div>
          <div class="top-career-card">
            <strong>UI/UX Designer</strong><br/>
            Salary: 5–20 LPA<br/>
            Difficulty: Medium<br/>
            Rating: ⭐⭐⭐⭐☆
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)  # close section

    st.markdown("</div>", unsafe_allow_html=True)  # close app-root

# -----------------------------------------------------
# CAREER CHART PAGE (AI GENERATED)
# -----------------------------------------------------
def page_career_chart():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown("### 📊 AI Career Chart")

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

# -----------------------------------------------------
# AI CAREER GUIDANCE PAGE
# -----------------------------------------------------
def page_ai_career_guidance():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown("### 🧠 AI Career Guidance")

    name = st.text_input("Your Name")
    interests = st.text_input("Your Interests (e.g. Coding, Finance, Design)")
    skills = st.text_input("Your Skills (e.g. Python, Excel, Communication)")
    education = st.text_input("Your Education (e.g. B.Tech CSE, B.Com)")
    goals = st.text_input("Your Career Goals (e.g. DevOps Engineer, Data Scientist)")

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

# -----------------------------------------------------
# LIBRARY PAGE
# -----------------------------------------------------
def page_library():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown("### 📚 Library")
    st.write("Later you can replace these with your real curated resources.")
    st.markdown(
        """
- **Data Science** – Kaggle, fast.ai, Analytics Vidhya  
- **Web Development** – MDN, FreeCodeCamp, Frontend Mentor  
- **DevOps** – KodeKloud, Kubernetes docs, AWS free tier labs  
- **System Design** – Grokking System Design, Gaurav Sen, Hussein Nasser  
- **Interview Prep** – LeetCode, InterviewBit, Striver’s DSA Sheet  
        """
    )
    st.markmarkdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# HISTORY PAGE
# -----------------------------------------------------
def page_history():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown("### 📚 Career Guidance History")

    hist = st.session_state["history"]
    if not hist:
        st.info("No history yet. Use AI Career Guidance to generate your first report.")
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

    st.markmarkdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# SETTINGS PAGE
# -----------------------------------------------------
def page_settings():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Settings")

    if st.button("Clear Career Guidance History", use_container_width=True):
        st.session_state["history"] = []
        st.success("History cleared for this session.")

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# ABOUT PAGE
# -----------------------------------------------------
def page_about():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown("### ℹ️ About")

    st.markdown(
        """
**AI Career Guidance** is a personal project created by **Niyaz** to help:

- Students exploring tech & business careers  
- Freshers choosing between roles like DevOps, Data, Backend, etc.  
- Professionals planning a career switch into IT / AI / Cloud  

It uses **Large Language Models (LLMs)** via **Groq**, with a simple
**Python + Streamlit** interface so anyone can access AI-powered career help.
        """
    )

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# CONTACT PAGE
# -----------------------------------------------------
def page_contact():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown("### 📬 Contact")

    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message", height=150)

    if st.button("Send", use_container_width=True):
        if not name.strip() or not email.strip() or not message.strip():
            st.error("⚠️ Please fill all fields.")
        else:
            st.success("✅ Message captured locally (you can connect to email or DB later).")

    st.markdown("#### My Contact Details")
    st.markdown("- 📧 **Email**: [Niyaz.kofficials@gmail.com](mailto:Niyaz.kofficials@gmail.com)")
    st.markdown("- 📱 **Phone**: [+91 7751931035](tel:+917751931035)")
    st.markdown("- 🔗 **LinkedIn**: [linkedin.com/in/iamnk7](https://linkedin.com/in/iamnk7)")
    st.markdown("- 🐙 **GitHub**: [github.com/Iamnk07](https://github.com/Iamnk07)")

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# FOOTER (Quick Links + Contact + Social Icons)
# -----------------------------------------------------
def render_footer():
    st.markdown(
        """
        <div class="footer">
          <div class="footer-inner">
            <div>
              <div class="footer-logo">AI Career Guidance</div>
              <div class="footer-link">
                Smart, AI-powered suggestions to help you make better career decisions.
              </div>
            </div>
            <div>
              <div class="footer-col-title">Quick Links</div>
              <div class="footer-link">🏠 Home</div>
              <div class="footer-link">🧠 AI Career Guidance</div>
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
              <div class="footer-link">📧 <a href="mailto:Niyaz.kofficials@gmail.com">Niyaz.kofficials@gmail.com</a></div>
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
elif page == "AI Career Guidance":
    page_ai_career_guidance()
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
