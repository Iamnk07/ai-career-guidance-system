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

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {
            "role": "assistant",
            "content": "Hi, I'm your AI career assistant. Ask me anything about roles, skills, or roadmaps.",
        }
    ]

if "notes" not in st.session_state:
    st.session_state["notes"] = ""

# -----------------------------------------------------
# GLOBAL CSS (RESPONSIVE, CLEAN CORPORATE)
# -----------------------------------------------------
CSS = """
<style>
body {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    background: #f9fafb;
}

/* Root layout */
.app-root {
    max-width: 1180px;
    margin: 0 auto;
    padding: 1.5rem 1rem 4rem 1rem;
}

/* Navbar */
.navbar {
    position: sticky;
    top: 0;
    z-index: 50;
    backdrop-filter: blur(12px);
    background: rgba(15,23,42,0.96);
    border-bottom: 1px solid rgba(148,163,184,0.4);
    padding: 0.5rem 1rem;
}
.nav-inner {
    max-width: 1180px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    gap: 1rem;
}
.nav-left {
    display: flex;
    align-items: center;
    gap: 0.75rem;
}
.nav-logo {
    width: 34px;
    height: 34px;
    border-radius: 999px;
    background: linear-gradient(135deg,#2563eb,#38bdf8);
    display:flex;
    align-items:center;
    justify-content:center;
    color:white;
    font-size:0.9rem;
    font-weight:600;
}
.nav-brand-text {
    display:flex;
    flex-direction:column;
}
.nav-brand-title {
    font-size: 0.95rem;
    font-weight:600;
    color:#e5e7eb;
}
.nav-brand-subtitle {
    font-size:0.75rem;
    color:#9ca3af;
}

/* Menu radio will render next to brand using Streamlit columns */

/* Right auth */
.nav-right {
    display:flex;
    align-items:center;
    gap:0.4rem;
    font-size:0.8rem;
    color:#e5e7eb;
    justify-content:flex-end;
}
.nav-auth-link {
    cursor:pointer;
    opacity:0.9;
}
.nav-auth-sep {
    opacity:0.6;
}

/* Make radio horizontally scrollable on small screens */
div[data-testid="stHorizontalBlock"] > div {
    overflow-x: auto;
}

/* Header title in content */
.app-header-title {
    text-align:center;
    font-size:1.7rem;
    font-weight:600;
    margin-bottom:0.25rem;
}
.app-header-subtitle {
    text-align:center;
    font-size:0.9rem;
    color:#6b7280;
    margin-bottom:1.2rem;
}

/* Hero */
.hero {
    display:flex;
    flex-wrap:wrap;
    gap:2rem;
    align-items:center;
    margin: 1.5rem 0 2.5rem 0;
}
.hero-left {
    flex:1 1 260px;
}
.hero-title {
    font-size: clamp(1.9rem, 3vw, 2.3rem);
    font-weight: 650;
    margin-bottom:0.5rem;
}
.hero-subtitle {
    font-size:0.95rem;
    color:#6b7280;
    max-width:480px;
    margin-bottom:1.2rem;
}
.hero-buttons {
    display:flex;
    flex-wrap:wrap;
    gap:0.7rem;
}
.hero-right {
    flex:1 1 260px;
    min-height:220px;
    display:flex;
    align-items:center;
    justify-content:center;
}
.hero-visual {
    width:100%;
    max-width:320px;
    aspect-ratio:1/1;
    border-radius:24px;
    background:
      radial-gradient(circle at 0% 0%, #2563eb 0, transparent 60%),
      radial-gradient(circle at 100% 100%, #22c55e 0, transparent 60%),
      radial-gradient(circle at 50% 0%, #f97316 0, transparent 60%),
      #0b1120;
    position:relative;
    overflow:hidden;
    box-shadow:0 18px 50px rgba(15,23,42,0.6);
}
.hero-orb {
    position:absolute;
    border-radius:999px;
    background:radial-gradient(circle,#e5e7eb 0,#38bdf8 45%,transparent 70%);
    opacity:0.7;
    filter:blur(2px);
    animation: float 8s ease-in-out infinite alternate;
}
.hero-orb.small { width:60px; height:60px; top:18%; left:12%; }
.hero-orb.medium { width:90px; height:90px; bottom:10%; right:10%; animation-delay:1s;}
.hero-orb.large { width:130px; height:130px; top:45%; left:55%; animation-delay:2s;}
.hero-center-label {
    position:absolute;
    inset: 32% 18%;
    background:rgba(15,23,42,0.9);
    border-radius:16px;
    border: 1px solid rgba(148,163,184,0.4);
    display:flex;
    align-items:center;
    justify-content:center;
    text-align:center;
    color:#e5e7eb;
    font-size:0.9rem;
    padding:0.5rem;
}
@keyframes float {
    0% { transform: translate3d(0,0,0) scale(1); }
    50% { transform: translate3d(10px,-8px,0) scale(1.06); }
    100% { transform: translate3d(-8px,10px,0) scale(0.95); }
}

/* Sections */
.section {
    margin: 2rem 0;
}
.section-title {
    font-size:1.1rem;
    font-weight:600;
    margin-bottom:0.4rem;
}
.section-subtitle {
    font-size:0.85rem;
    color:#6b7280;
    margin-bottom:0.9rem;
}

/* How it works */
.how-grid {
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap:0.8rem;
}
.how-card {
    border-radius:0.75rem;
    border:1px solid #e5e7eb;
    padding:0.75rem 0.9rem;
    background:#ffffff;
    font-size:0.85rem;
}

/* Features */
.features-grid {
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
    gap:0.8rem;
}
.feature-card {
    border-radius:0.75rem;
    border:1px solid #e5e7eb;
    padding:0.9rem;
    background:#ffffff;
    font-size:0.85rem;
    min-height:90px;
}

/* Categories */
.categories-grid {
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap:0.8rem;
}
.category-card {
    border-radius:0.75rem;
    border:1px solid #e5e7eb;
    padding:0.9rem;
    background:#ffffff;
    font-size:0.85rem;
}
.category-roles {
    margin-top:0.4rem;
    font-size:0.8rem;
    color:#6b7280;
}

/* AI chat preview */
.chat-preview {
    border-radius:0.75rem;
    border:1px solid #e5e7eb;
    padding:0.9rem;
    background:#f9fafb;
    max-width:420px;
    font-size:0.85rem;
}

/* Popular careers */
.popular-grid {
    display:grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap:0.8rem;
}
.pop-card {
    border-radius:0.75rem;
    border:1px solid #e5e7eb;
    padding:0.9rem;
    background:#ffffff;
    font-size:0.85rem;
}

/* About section */
.about-grid {
    display:grid;
    grid-template-columns: minmax(0, 1.1fr) minmax(0, 1.4fr);
    gap:1rem;
}
.about-image {
    border-radius:0.75rem;
    background:radial-gradient(circle at 0% 0%, #2563eb 0, transparent 60%),
               radial-gradient(circle at 100% 100%, #22c55e 0, transparent 60%),
               #0b1120;
    min-height:180px;
}

/* Contact */
.contact-card {
    border-radius:0.75rem;
    border:1px solid #e5e7eb;
    padding:1rem;
    background:#ffffff;
}

/* Footer */
.footer {
    margin-top:3rem;
    background:#020617;
    color:#e5e7eb;
}
.footer-inner {
    max-width:1180px;
    margin:0 auto;
    padding:1.5rem 1rem 2rem 1rem;
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

/* Splash */
.splash-layer {
    position: fixed;
    inset: 0;
    background:
        radial-gradient(circle at 10% 20%, rgba(37,99,235,0.9), transparent 50%),
        radial-gradient(circle at 90% 80%, rgba(14,165,233,0.9), transparent 50%),
        #020617;
    display:flex;
    align-items:center;
    justify-content:center;
    z-index:9999;
}
.splash-content {
    text-align:center;
    color:#e5e7eb;
    padding: 1.8rem 2.2rem;
    border-radius:18px;
    background:rgba(15,23,42,0.94);
    border:1px solid rgba(148,163,184,0.5);
    min-width:260px;
}
.splash-title {
    font-size:clamp(1.6rem, 3vw, 2.1rem);
    font-weight:650;
    margin-bottom:0.4rem;
}
.splash-sub {
    font-size:0.9rem;
    color:#9ca3af;
    margin-bottom:0.4rem;
}
.splash-author {
    font-size:0.8rem;
    color:#cbd5f5;
    opacity:0.9;
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -----------------------------------------------------
# SPLASH SCREEN (FULLSCREEN, 4s)
# -----------------------------------------------------
def show_splash():
    html = """
    <div class="splash-layer">
      <div class="splash-content">
        <div class="splash-title">Welcome to AI Career Guidance</div>
        <div class="splash-sub">Smart career insights powered by AI.</div>
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
            model="openai/gpt-oss-20b",  # ✅ model your account has
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


def get_chat_reply(message: str) -> str:
    prompt = f"""
You are an AI career assistant for Indian students and early professionals.
Be clear, specific, and practical.

User question: {message}
"""
    return call_groq(prompt)

# -----------------------------------------------------
# NAVBAR (LOGO LEFT, MENU, LOGIN/SIGNUP RIGHT)
# -----------------------------------------------------
menu_items = [
    "Home",
    "AI Career Guidance",
    "Career Chat",
    "Library",
    "Notes",
    "Settings",
    "About",
    "Contact",
]

def render_navbar():
    st.markdown('<div class="navbar"><div class="nav-inner">', unsafe_allow_html=True)

    # Left logo & brand
    col_left, col_menu, col_right = st.columns([2, 6, 2])
    with col_left:
        st.markdown(
            """
            <div class="nav-left">
              <div class="nav-logo">AI</div>
              <div class="nav-brand-text">
                <div class="nav-brand-title">AI Career Guidance</div>
                <div class="nav-brand-subtitle">Plan your next step with AI</div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Center menu as radio
    with col_menu:
        active = st.radio(
            "Navigation",
            menu_items,
            horizontal=True,
            label_visibility="collapsed",
            index=menu_items.index(st.session_state["active_page"]),
            key="nav_radio",
        )
        st.session_state["active_page"] = active

    # Right auth text
    with col_right:
        st.markdown(
            """
            <div class="nav-right">
              <span class="nav-auth-link">Login</span>
              <span class="nav-auth-sep">|</span>
              <span class="nav-auth-link">Sign up</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div></div>", unsafe_allow_html=True)

# -----------------------------------------------------
# PAGES
# -----------------------------------------------------
def page_home():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)

    # Header
    st.markdown(
        """
        <div class="app-header-title">Find Your Best Career Path With AI</div>
        <div class="app-header-subtitle">
            Smart suggestions based on your skills & interests.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # HERO
    st.markdown('<div class="hero">', unsafe_allow_html=True)
    col_left, col_right = st.columns([1.2, 1], gap="large")

    with col_left:
        st.markdown(
            """
            <div class="hero-left">
                <div class="hero-title">Find Your Best Career Path With AI</div>
                <div class="hero-subtitle">
                    Get a clear, personalized roadmap based on your skills, interests,
                    and long-term goals. No more random career advice.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Start Career Test", use_container_width=True):
                st.session_state["active_page"] = "AI Career Guidance"
                st.rerun()
        with c2:
            if st.button("Explore Careers", use_container_width=True):
                st.session_state["active_page"] = "AI Career Guidance"
                st.rerun()

    with col_right:
        st.markdown(
            """
            <div class="hero-right">
              <div class="hero-visual">
                <div class="hero-orb small"></div>
                <div class="hero-orb medium"></div>
                <div class="hero-orb large"></div>
                <div class="hero-center-label">
                  AI analyzes your profile<br/>and suggests the best paths.
                </div>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)  # close hero

    # HOW IT WORKS
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-title">How it works</div>
        <div class="section-subtitle">Three simple steps to get your personalized roadmap.</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="how-grid">
          <div class="how-card">
            <strong>Step 1 – Take a 5-minute AI test</strong><br/>
            Answer a few questions about your skills, interests, and experience.
          </div>
          <div class="how-card">
            <strong>Step 2 – AI analyzes your profile</strong><br/>
            Your inputs are compared with modern roles and skill requirements.
          </div>
          <div class="how-card">
            <strong>Step 3 – Get your career roadmap</strong><br/>
            Receive a clear plan: roles, skills to learn, resources, and salary insights.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # FEATURES SECTION
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-title">What you can do inside</div>
        <div class="section-subtitle">All-in-one space for exploring and planning your career.</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="features-grid">
          <div class="feature-card"><strong>AI Career Test</strong><br/>Find matching roles based on your profile.</div>
          <div class="feature-card"><strong>Skill Strength Checker</strong><br/>See which skills are strong and which need work.</div>
          <div class="feature-card"><strong>Career Suggestions</strong><br/>Get a list of roles aligned with your interests.</div>
          <div class="feature-card"><strong>Career Roadmaps</strong><br/>See step-by-step plans to reach your goal role.</div>
          <div class="feature-card"><strong>Salary Prediction</strong><br/>View typical salary ranges in India for each role.</div>
          <div class="feature-card"><strong>Career Library</strong><br/>Access curated links, videos, and articles.</div>
          <div class="feature-card"><strong>Notes</strong><br/>Save your thoughts and guidance in one place.</div>
          <div class="feature-card"><strong>Settings/Profile</strong><br/>Customize your experience for future visits.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # CAREER CATEGORIES
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-title">Career categories</div>
        <div class="section-subtitle">Explore careers across different domains.</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="categories-grid">
          <div class="category-card">
            <strong>Software & IT</strong>
            <div class="category-roles">
              • Software Engineer<br/>
              • Backend Developer<br/>
              • DevOps Engineer
            </div>
          </div>
          <div class="category-card">
            <strong>Business & Finance</strong>
            <div class="category-roles">
              • Financial Analyst<br/>
              • Business Analyst<br/>
              • Investment Banking Analyst
            </div>
          </div>
          <div class="category-card">
            <strong>Arts & Design</strong>
            <div class="category-roles">
              • UI/UX Designer<br/>
              • Graphic Designer<br/>
              • Product Designer
            </div>
          </div>
          <div class="category-card">
            <strong>Science & Research</strong>
            <div class="category-roles">
              • Data Scientist<br/>
              • AI Researcher<br/>
              • Research Assistant
            </div>
          </div>
          <div class="category-card">
            <strong>Engineering</strong>
            <div class="category-roles">
              • Mechanical Engineer<br/>
              • Civil Engineer<br/>
              • Electrical Engineer
            </div>
          </div>
          <div class="category-card">
            <strong>Digital Marketing</strong>
            <div class="category-roles">
              • SEO Specialist<br/>
              • Performance Marketer<br/>
              • Social Media Manager
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # AI CHAT PREVIEW
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-title">AI career chat</div>
        <div class="section-subtitle">Ask questions like “Is DevOps good for me?” or “How to switch from mechanical to IT?”.</div>
        """,
        unsafe_allow_html=True,
    )
    col_chat, _ = st.columns([1.3, 1])
    with col_chat:
        st.markdown(
            """
            <div class="chat-preview">
              <strong>Ask me anything about your career!</strong><br/>
              <span style="font-size:0.8rem; color:#6b7280;">Example: "I am a B.Tech CSE student. Which is better for me: Data Engineer or Backend Developer?"</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open AI Career Chat", use_container_width=True):
            st.session_state["active_page"] = "Career Chat"
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # POPULAR CAREERS
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-title">Popular careers</div>
        <div class="section-subtitle">High-demand roles with strong future growth.</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="popular-grid">
          <div class="pop-card">
            <strong>Data Scientist</strong><br/>
            Salary Range: 8–30 LPA<br/>
            Difficulty: High<br/>
            Future Demand: ⭐⭐⭐⭐⭐
          </div>
          <div class="pop-card">
            <strong>AI Engineer</strong><br/>
            Salary Range: 10–40 LPA<br/>
            Difficulty: High<br/>
            Future Demand: ⭐⭐⭐⭐⭐
          </div>
          <div class="pop-card">
            <strong>Cloud Architect</strong><br/>
            Salary Range: 12–45 LPA<br/>
            Difficulty: High<br/>
            Future Demand: ⭐⭐⭐⭐☆
          </div>
          <div class="pop-card">
            <strong>UI/UX Designer</strong><br/>
            Salary Range: 5–20 LPA<br/>
            Difficulty: Medium<br/>
            Future Demand: ⭐⭐⭐⭐☆
          </div>
          <div class="pop-card">
            <strong>Financial Analyst</strong><br/>
            Salary Range: 6–20 LPA<br/>
            Difficulty: Medium<br/>
            Future Demand: ⭐⭐⭐⭐☆
          </div>
          <div class="pop-card">
            <strong>Cyber Security Engineer</strong><br/>
            Salary Range: 8–30 LPA<br/>
            Difficulty: High<br/>
            Future Demand: ⭐⭐⭐⭐⭐
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    # ABOUT SECTION
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-title">About CareerAI</div>
        <div class="section-subtitle">Why this project exists and how it helps you.</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="about-grid">', unsafe_allow_html=True)
    col_img, col_text = st.columns([1, 1.4])
    with col_img:
        st.markdown('<div class="about-image"></div>', unsafe_allow_html=True)
    with col_text:
        st.write(
            """
CareerAI is a personal project created by **Niyaz** to support students and early professionals
in making better, data-driven career decisions.

Instead of random suggestions, you get AI-based guidance that considers:
- Your interests and skills  
- Real-world roles and skill requirements  
- Practical roadmaps and resources  

**Technologies used**  
- Large Language Models (LLMs) via Groq  
- Python & Streamlit for the interface  
            """
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # CONTACT SECTION
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="section-title">Contact</div>
        <div class="section-subtitle">Share feedback, suggestions, or collaboration ideas.</div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="contact-card">', unsafe_allow_html=True)
    name = st.text_input("Your Name (Home Contact)")
    email = st.text_input("Your Email (Home Contact)")
    message = st.text_area("Your Message", height=120)
    if st.button("Send Message", use_container_width=True):
        if not name.strip() or not email.strip() or not message.strip():
            st.error("⚠️ Please fill all fields.")
        else:
            st.success("✅ Message captured locally (connect to email or DB later).")

    st.write("**Social Links** (update with your real links):")
    st.markdown("- 🔗 LinkedIn: *your-link-here*")
    st.markdown("- 🐙 GitHub: *your-link-here*")
    st.markdown("- 💬 WhatsApp: *your-number-here*")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # close app-root

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

def page_career_chat():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown("### 💬 AI Career Chat")
    st.write("Ask anything about careers, skills, transitions, or learning paths.")

    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Type your question here...")
    if user_input:
        st.session_state["chat_messages"].append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = get_chat_reply(user_input)
                st.markdown(reply)
        st.session_state["chat_messages"].append({"role": "assistant", "content": reply})

    st.markdown("</div>", unsafe_allow_html=True)

def page_library():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown("### 📚 Career Library")
    st.write("You can later replace these with your real curated resources.")
    st.markdown(
        """
- **Data Science** – Kaggle, fast.ai, Analytics Vidhya  
- **Web Development** – MDN Web Docs, FreeCodeCamp, Frontend Mentor  
- **DevOps** – KodeKloud, Kubernetes docs, AWS free tier labs  
- **System Design** – Grokking System Design, Gaurav Sen, Hussein Nasser  
- **Interview Prep** – LeetCode, InterviewBit, Striver’s DSA Sheet  
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

def page_notes():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown("### 📝 Notes")
    st.write("Keep your own notes about plans, ideas, or feedback from mentors.")
    text = st.text_area("Your notes", value=st.session_state["notes"], height=220)
    st.session_state["notes"] = text
    st.markdown("</div>", unsafe_allow_html=True)

def page_settings():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown("### ⚙️ Settings")

    if st.button("Clear Career Guidance History"):
        st.session_state["history"] = []
        st.success("History cleared for this session.")

    if st.button("Reset Career Chat"):
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": "Hi, I'm your AI career assistant. Ask me anything about roles, skills, or roadmaps.",
            }
        ]
        st.success("Chat reset.")

    st.markdown("</div>", unsafe_allow_html=True)

def page_about():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markdown("### ℹ️ About CareerAI")
    st.markdown(
        """
**CareerAI** is a personal project created by **Niyaz** to help students and early professionals:

- Discover roles that match their interests and strengths  
- Understand real-world skill expectations  
- Get a practical roadmap instead of random advice  

**Tech stack:**

- Python & Streamlit for the web interface  
- Groq API (`openai/gpt-oss-20b`) for AI  
- Deployed on Streamlit Community Cloud  
        """
    )
    st.markdown("</div>", unsafe_allow_html=True)

def page_contact():
    st.markdown('<div class="app-root">', unsafe_allow_html=True)
    st.markmarkdown("### 📬 Contact")
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    msg = st.text_area("Your Message", height=150)

    if st.button("Send", use_container_width=True):
        if not name.strip() or not email.strip() or not msg.strip():
            st.error("⚠️ Please fill all fields.")
        else:
            st.success("✅ Message captured locally (later connect to backend or email).")

    st.markdown("#### Social Links")
    st.markdown("- 🔗 LinkedIn: *your-link-here*")
    st.markdown("- 🐙 GitHub: *your-link-here*")
    st.markdown("- 💬 WhatsApp: *your-number-here*")
    st.markdown("</div>", unsafe_allow_html=True)

def render_footer():
    st.markdown(
        """
        <div class="footer">
          <div class="footer-inner">
            <div>
              <div class="footer-logo">AI Career Guidance</div>
              <div class="footer-link">Smart career suggestions powered by AI.</div>
            </div>
            <div>
              <div class="footer-col-title">Quick Links</div>
              <div class="footer-link">Home</div>
              <div class="footer-link">AI Career Guidance</div>
              <div class="footer-link">Library</div>
            </div>
            <div>
              <div class="footer-col-title">Support</div>
              <div class="footer-link">Help</div>
              <div class="footer-link">FAQ</div>
              <div class="footer-link">Privacy Policy</div>
            </div>
            <div>
              <div class="footer-col-title">Contact</div>
              <div class="footer-link">Email: youremail@example.com</div>
              <div class="footer-link">WhatsApp: +91-XXXXXXXXXX</div>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------------------------------
# MAIN
# -----------------------------------------------------
render_navbar()

page = st.session_state["active_page"]

if page == "Home":
    page_home()
elif page == "AI Career Guidance":
    page_ai_career_guidance()
elif page == "Career Chat":
    page_career_chat()
elif page == "Library":
    page_library()
elif page == "Notes":
    page_notes()
elif page == "Settings":
    page_settings()
elif page == "About":
    page_about()
elif page == "Contact":
    page_contact()

render_footer()
