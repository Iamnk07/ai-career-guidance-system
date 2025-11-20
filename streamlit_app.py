import streamlit as st
from groq import Groq
from datetime import datetime

# -----------------------------------------------------
# BASIC PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="AI Career Guidance System",
    page_icon="🚀",
    layout="wide",
)

# -----------------------------------------------------
# SESSION DEFAULTS
# -----------------------------------------------------
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "Home"

if "history" not in st.session_state:
    st.session_state["history"] = []

# -----------------------------------------------------
# GLOBAL MINIMAL CSS (SIMPLE + OFFICIAL)
# -----------------------------------------------------
BASE_CSS = """
<style>
/* Font */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: "Inter", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Background */
.stApp {
    background: #f3f4f6;
}

/* Main container */
.app-wrapper {
    max-width: 1100px;
    margin: 0 auto;
    padding: 1.5rem 1rem 3rem 1rem;
}

/* Simple card */
.app-card {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.5rem 1.5rem;
    border: 1px solid #e5e7eb;
    box-shadow: 0 8px 20px rgba(15, 23, 42, 0.04);
}

/* Section titles */
.app-section-title {
    font-size: 1.1rem;
    font-weight: 600;
    margin-bottom: 0.15rem;
    color: #111827;
}
.app-section-subtitle {
    font-size: 0.85rem;
    color: #6b7280;
    margin-bottom: 0.8rem;
}

/* Home hero */
.hero-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #111827;
    margin-bottom: 0.25rem;
}
.hero-subtitle {
    font-size: 0.95rem;
    color: #4b5563;
    margin-bottom: 0.4rem;
}
.hero-tag {
    display: inline-block;
    padding: 0.18rem 0.75rem;
    font-size: 0.78rem;
    border-radius: 999px;
    background: #ecfeff;
    color: #0369a1;
    border: 1px solid #bae6fd;
    margin-bottom: 0.6rem;
}

/* Simple feature cards */
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 0.9rem;
    margin-top: 0.8rem;
}
.feature-card {
    border-radius: 10px;
    border: 1px solid #e5e7eb;
    padding: 0.9rem 1rem;
    background: #f9fafb;
    font-size: 0.85rem;
}
.feature-card-title {
    font-weight: 600;
    margin-bottom: 0.25rem;
    color: #111827;
}
.feature-card-text {
    font-size: 0.82rem;
    color: #6b7280;
}

/* Footer */
.footer {
    border-top: 1px solid #e5e7eb;
    margin-top: 2rem;
    padding-top: 1rem;
    font-size: 0.8rem;
    color: #6b7280;
}
.footer-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
    gap: 1rem;
}
.footer-title {
    font-weight: 600;
    color: #111827;
    margin-bottom: 0.25rem;
}
.footer-link a {
    color: #4b5563;
    text-decoration: none;
}
.footer-link a:hover {
    text-decoration: underline;
}

/* Mobile adjustments */
@media (max-width: 640px) {
    .app-wrapper {
        padding: 1rem 0.6rem 2.5rem 0.6rem;
    }
    .app-card {
        padding: 1.2rem 1.1rem;
    }
}
</style>
"""
st.markdown(BASE_CSS, unsafe_allow_html=True)

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
            model="openai/gpt-oss-20b",   # keep a stable model you can access
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

Provide structured, detailed career guidance including:

1. Best 4 Career Options  
2. Required Skills  
3. Missing Skills & How to Improve  
4. Step-by-step Career Roadmap  
5. Salary Range in INR  
6. Best Learning Resources  
7. Resume Tips  
8. Interview Preparation Tips

Use clear headings and bullet points.
"""
    return call_groq(prompt)

def get_career_chart_overview(name, skills, interests):
    prompt = f"""
You are an AI career mentor. Create a clear career chart overview.

Name: {name}
Skills: {skills}
Interests: {interests}

Provide:

1. Short profile summary  
2. 3–5 suitable career paths  
3. A simple career chart:
   - Stage 1: Where they are now
   - Stage 2: Next 1–2 roles
   - Stage 3: Senior roles
4. Key skills to focus on  
5. Suggested learning plan (bullet points)

Keep it concise but useful.
"""
    return call_groq(prompt)

# -----------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------
NAV_ITEMS = [
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
    st.markdown("### AI Career Guidance")
    st.caption("Created by **Niyaz Khan**")
    st.write("---")

    choice = st.radio(
        "Navigation",
        NAV_ITEMS,
        index=NAV_ITEMS.index(st.session_state["active_page"]),
    )
    st.session_state["active_page"] = choice

# -----------------------------------------------------
# PAGES
# -----------------------------------------------------
def page_home():
    st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)

    st.markdown('<div class="hero-tag">AI-powered career planning for students & freshers in India</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">AI Career Guidance System</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-subtitle">Get career options, growth paths, skills to learn, and learning resources – all from one place.</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <p style="font-size:0.86rem; color:#4b5563; margin-top:0.4rem;">
        Start with a quick career chart, or generate a detailed AI career guidance report.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Quick feature overview
    st.markdown('<div class="feature-grid">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-card-title">📊 Career Chart</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="feature-card-text">High-level view of your path: entry role, mid-level roles, and senior positions.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Open Career Chart", key="go_chart"):
            st.session_state["active_page"] = "Career Chart"
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-card-title">🧠 Career Guide</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="feature-card-text">Detailed report with 4 best-fit roles, skills, salary bands, and learning plan.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Open Career Guide", key="go_guide"):
            st.session_state["active_page"] = "Career Guide"
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown('<div class="feature-card-title">📚 Library</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="feature-card-text">List of reference resources for Data, Web, DevOps, DSA, and System Design.</div>',
            unsafe_allow_html=True,
        )
        if st.button("Open Library", key="go_library"):
            st.session_state["active_page"] = "Library"
            st.experimental_rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)  # feature-grid

    st.markdown("</div>", unsafe_allow_html=True)  # app-card
    st.markdown("</div>", unsafe_allow_html=True)  # app-wrapper


def page_career_chart():
    st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)

    st.markdown('<div class="app-section-title">📊 AI Career Chart</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-section-subtitle">Get a high-level view of your career path from today to senior roles.</div>',
        unsafe_allow_html=True,
    )

    name = st.text_input("Your Name (optional)")
    skills = st.text_area("Your Key Skills", placeholder="e.g. Python, SQL, problem solving, communication")
    interests = st.text_area("Your Interests", placeholder="e.g. building apps, finance, design, research")

    if st.button("Generate Career Chart", use_container_width=True):
        if not skills.strip() or not interests.strip():
            st.error("⚠️ Please fill at least skills and interests.")
        else:
            with st.spinner("Generating your AI career chart..."):
                overview = get_career_chart_overview(
                    name.strip() or "User",
                    skills.strip(),
                    interests.strip(),
                )
            st.markdown("### Your Career Chart Overview")
            st.write(overview)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def page_career_guide():
    st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)

    st.markdown('<div class="app-section-title">🧠 Full AI Career Guidance</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-section-subtitle">Fill this form once to generate a detailed career guidance report.</div>',
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
            with st.spinner("Analyzing your profile and preparing guidance..."):
                advice = get_career_advice(
                    interests.strip(),
                    skills.strip(),
                    education.strip(),
                    goals.strip(),
                )

            st.session_state["history"].append(
                {
                    "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "name": name.strip(),
                    "interests": interests.strip(),
                    "skills": skills.strip(),
                    "education": education.strip(),
                    "goals": goals.strip(),
                    "advice": advice,
                }
            )

            st.markdown("### Your AI Career Guidance")
            st.write(advice)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def page_library():
    st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)

    st.markdown('<div class="app-section-title">📚 Learning Library</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-section-subtitle">Basic list of resources. You can replace these with your own curated list later.</div>',
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


def page_history():
    st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)

    st.markdown('<div class="app-section-title">📁 Career Guidance History</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-section-subtitle">Reports generated in this session are listed here.</div>',
        unsafe_allow_html=True,
    )

    hist = st.session_state["history"]
    if not hist:
        st.info("No history yet. Use the AI Career Guide page to generate your first report.")
    else:
        for i, item in enumerate(reversed(hist), start=1):
            label = f"{i}. {item['time']} — {item['name']} ({item['goals']})"
            with st.expander(label):
                st.write(f"**Interests:** {item['interests']}")
                st.write(f"**Skills:** {item['skills']}")
                st.write(f"**Education:** {item['education']}")
                st.write(f"**Target Role:** {item['goals']}")
                st.markdown("---")
                st.write(item["advice"])

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def page_settings():
    st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)

    st.markdown('<div class="app-section-title">⚙️ Settings</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-section-subtitle">Manage data stored in this session.</div>',
        unsafe_allow_html=True,
    )

    if st.button("Clear Career Guidance History", use_container_width=True):
        st.session_state["history"] = []
        st.success("History cleared for this session.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def page_about():
    st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)

    st.markdown('<div class="app-section-title">ℹ️ About This Project</div>', unsafe_allow_html=True)
    st.markdown(
        """
**AI Career Guidance System** is a personal project by **Niyaz Khan**  
to help Indian students and freshers explore realistic tech and tech-aligned careers.
        """
    )
    st.markdown(
        """
The app is useful for:

- Students exploring software, data, cloud, and business-aligned roles  
- Freshers confused between options like DevOps, Data, Backend, etc.  
- Professionals planning a career switch into IT / AI / Cloud  

Technology used:

- **Python + Streamlit** for the interface  
- **Groq (LLMs)** for generating guidance  
        """
    )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def page_contact():
    st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="app-card">', unsafe_allow_html=True)

    st.markdown('<div class="app-section-title">📬 Contact</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="app-section-subtitle">Share feedback or connect for collaboration.</div>',
        unsafe_allow_html=True,
    )

    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message", height=150)

    if st.button("Send Message", use_container_width=True):
        if not name.strip() or not email.strip() or not message.strip():
            st.error("⚠️ Please fill all fields.")
        else:
            # You can later integrate email or DB here
            st.success("✅ Message captured (locally). You can connect this to email or a database later.")

    st.markdown("---")
    st.markdown("#### My Contact & Social")
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
    st.markdown('<div class="app-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="footer">', unsafe_allow_html=True)

    st.markdown('<div class="footer-grid">', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown('<div class="footer-title">AI Career Guidance System</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="footer-link">Built by <strong>Niyaz Khan</strong> · AI-powered planning for students & early-career professionals.</div>',
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown('<div class="footer-title">Pages</div>', unsafe_allow_html=True)
        st.markdown('<div class="footer-link">Home</div>', unsafe_allow_html=True)
        st.markdown('<div class="footer-link">Career Chart</div>', unsafe_allow_html=True)
        st.markdown('<div class="footer-link">Career Guide</div>', unsafe_allow_html=True)
        st.markdown('<div class="footer-link">Library</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="footer-title">Contact</div>', unsafe_allow_html=True)
        st.markmarkdown(
            '<div class="footer-link"><a href="mailto:niyaz.kofficials@gmail.com">niyaz.kofficials@gmail.com</a></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="footer-link"><a href="tel:+917751931035">+91 7751931035</a></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="footer-link"><a href="https://linkedin.com/in/iamnk7" target="_blank">LinkedIn</a></div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            '<div class="footer-link"><a href="https://github.com/Iamnk07" target="_blank">GitHub</a></div>',
            unsafe_allow_html=True,
        )

    st.markdown('</div>', unsafe_allow_html=True)  # footer-grid
    st.markdown('</div>', unsafe_allow_html=True)  # footer
    st.markdown('</div>', unsafe_allow_html=True)  # app-wrapper

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
