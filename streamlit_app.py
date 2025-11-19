import streamlit as st
from groq import Groq
from datetime import datetime
from fpdf import FPDF
import io
import time

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="AI Career Guidance",
    page_icon="🚀",
    layout="centered"
)

# -----------------------------------------------------
# SESSION DEFAULTS
# -----------------------------------------------------
if "theme" not in st.session_state:
    st.session_state["theme"] = "Dark"

if "history" not in st.session_state:
    st.session_state["history"] = []

if "chat_messages" not in st.session_state:
    st.session_state["chat_messages"] = [
        {
            "role": "assistant",
            "content": "Hi! I'm your AI career assistant. Ask me anything about careers, skills, or learning paths."
        }
    ]

if "splash_done" not in st.session_state:
    st.session_state["splash_done"] = False

# -----------------------------------------------------
# THEME / GLOBAL CORPORATE CSS
# -----------------------------------------------------
def apply_theme():
    theme = st.session_state.get("theme", "Dark")

    if theme == "Dark":
        bg_color = "#0b1020"           # dark navy
        card_bg = "#141a2a"            # slightly lighter
        text_color = "#e5e7eb"         # light gray
        border_color = "#1f2937"
        accent = "#2563eb"             # corporate blue
    else:
        bg_color = "#f3f4f6"
        card_bg = "#ffffff"
        text_color = "#111827"
        border_color = "#e5e7eb"
        accent = "#2563eb"

    st.markdown(
        f"""
        <style>
            /* Global */
            body {{
                background-color: {bg_color};
                color: {text_color};
                font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            }}
            .main {{
                background-color: {bg_color};
            }}

            /* Page container for consistent width */
            .page-container {{
                max-width: 1100px;
                margin: 0 auto;
                padding: min(4vw, 32px);
            }}

            /* Cards & inputs */
            .stTextInput > div > div > input,
            .stTextArea > div > textarea {{
                background-color: {card_bg};
                color: {text_color};
                border-radius: 8px;
            }}

            .stButton > button {{
                border-radius: 999px;
                padding: 0.5rem 1.2rem;
                font-weight: 500;
            }}

            /* Top title + subtitle */
            .nav-title {{
                text-align:center;
                font-size: clamp(1.4rem, 2vw, 1.8rem);
                font-weight: 600;
                margin-bottom: 0.2rem;
            }}
            .nav-subtitle {{
                text-align:center;
                font-size: 0.9rem;
                opacity: 0.7;
                margin-bottom: 0.8rem;
            }}

            /* Make radio nav scrollable on small screens */
            .block-container {{
                padding-top: 1rem;
            }}
            div[data-testid="stHorizontalBlock"] > div {{
                overflow-x: auto;
            }}

            /* Chat message box tweak */
            [data-testid="stChatMessage"] {{
                max-width: 900px;
            }}

            /* Expander tweaks */
            details summary {{
                font-size: 0.95rem;
            }}

        </style>
        """,
        unsafe_allow_html=True,
    )

apply_theme()

# -----------------------------------------------------
# SPLASH SCREEN (4 SECONDS, CORPORATE STYLE)
# -----------------------------------------------------
def show_splash():
    splash_html = """
    <style>
    .splash-root {
        position: fixed;
        inset: 0;
        background: radial-gradient(circle at top left, #1d4ed8 0, transparent 45%),
                    radial-gradient(circle at bottom right, #0ea5e9 0, transparent 45%),
                    #020617;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 9999;
    }
    .splash-card {
        background: rgba(15,23,42,0.9);
        border-radius: 20px;
        border: 1px solid rgba(148,163,184,0.25);
        padding: 32px 40px;
        max-width: 480px;
        width: 90%;
        box-shadow:
            0 24px 60px rgba(15,23,42,0.6);
        text-align: left;
    }
    .splash-logo-circle {
        width: 48px;
        height: 48px;
        border-radius: 999px;
        background: linear-gradient(135deg,#2563eb,#38bdf8);
        display:flex;
        align-items:center;
        justify-content:center;
        color:white;
        font-weight:600;
        margin-bottom:16px;
    }
    .splash-heading {
        font-size: 1.4rem;
        font-weight: 600;
        color: #e5e7eb;
        margin-bottom: 4px;
    }
    .splash-subheading {
        font-size: 0.95rem;
        color: #9ca3af;
        margin-bottom: 14px;
    }
    .splash-meta {
        font-size: 0.8rem;
        color: #9ca3af;
        display:flex;
        align-items:center;
        gap:6px;
    }
    .splash-pill {
        display:inline-flex;
        align-items:center;
        padding: 2px 10px;
        border-radius: 999px;
        background: rgba(37,99,235,0.15);
        color: #bfdbfe;
        font-size: 0.75rem;
        margin-bottom: 10px;
    }
    @media (max-width: 600px) {
        .splash-card {{
            padding: 24px 20px;
        }}
        .splash-heading {{
            font-size: 1.2rem;
        }}
    }
    </style>

    <div class="splash-root">
      <div class="splash-card">
        <div class="splash-logo-circle">AI</div>
        <div class="splash-pill">Career Intelligence</div>
        <div class="splash-heading">Welcome to AI Career Guidance</div>
        <div class="splash-subheading">
          A simple, professional tool to help you discover roles, skills and a clear roadmap for your career.
        </div>
        <div class="splash-meta">
          <span>Powered by Groq · Streamlit</span>
        </div>
      </div>
    </div>
    """
    st.markdown(splash_html, unsafe_allow_html=True)

if not st.session_state["splash_done"]:
    show_splash()
    time.sleep(4)
    st.session_state["splash_done"] = True
    st.rerun()

# -----------------------------------------------------
# GROQ CLIENT
# -----------------------------------------------------
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

# -----------------------------------------------------
# HELPERS
# -----------------------------------------------------
def clean_text(text: str) -> str:
    return text.strip() if text else ""


def call_groq(prompt: str) -> str:
    """Core function to call Groq chat completion."""
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",  # ✅ model your account can use
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ **API Error:** {e}"


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


def career_chat_reply(user_message: str) -> str:
    base = """
You are an AI career assistant for Indian students and early professionals.
Answer briefly but helpfully. Be specific with skills, tools, and resources.
"""
    prompt = base + "\nUser question: " + user_message
    return call_groq(prompt)


def generate_pdf(name, interests, skills, education, goals, advice) -> bytes:
    """Generate a simple PDF and return it as bytes."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "AI Career Guidance Report", ln=1)

    pdf.set_font("Arial", "", 12)
    pdf.ln(4)
    pdf.cell(0, 8, f"Name: {name}", ln=1)
    pdf.cell(0, 8, f"Interests: {interests}", ln=1)
    pdf.cell(0, 8, f"Skills: {skills}", ln=1)
    pdf.cell(0, 8, f"Education: {education}", ln=1)
    pdf.cell(0, 8, f"Goals: {goals}", ln=1)

    pdf.ln(6)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Guidance:", ln=1)

    pdf.set_font("Arial", "", 11)
    safe_advice = advice.replace("•", "-")
    pdf.multi_cell(0, 6, safe_advice)

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer.read()

# -----------------------------------------------------
# TOP TITLE + NAV (CORPORATE STYLE)
# -----------------------------------------------------
with st.container():
    st.markdown('<div class="page-container">', unsafe_allow_html=True)

    st.markdown('<div class="nav-title">AI Career Guidance</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="nav-subtitle">A focused, professional assistant to help you plan your next career move.</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "",
        ["Home", "Career Guidance", "Career Chat", "History", "About", "Contact", "Settings"],
        horizontal=True,
        key="main_nav",
    )

    st.write("")  # small spacing

# -----------------------------------------------------
# PAGE RENDER FUNCTIONS
# -----------------------------------------------------
def render_home():
    st.markdown(
        """
        <div class="page-container">
            <div style="background:rgba(15,23,42,0.6); border-radius:16px; padding:20px 22px; border:1px solid rgba(148,163,184,0.25);">
                <h3 style="margin-top:0;margin-bottom:6px;">Welcome</h3>
                <p style="font-size:0.95rem; opacity:0.9;">
                    Use this tool to explore roles, understand the skills you need, and get a step-by-step plan.
                    Start with <b>Career Guidance</b> for a full report, or use <b>Career Chat</b> for quick doubts.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✨ Go to Career Guidance", use_container_width=True):
            st.session_state["main_nav"] = "Career Guidance"
            st.rerun()
    with col2:
        if st.button("💬 Open Career Chat", use_container_width=True):
            st.session_state["main_nav"] = "Career Chat"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


def render_career_guidance():
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.subheader("🧠 AI Career Guidance")

    name = st.text_input("Your Name")
    interests = st.text_input("Your Interests (e.g. Coding, Finance, Design)")
    skills = st.text_input("Your Skills (e.g. Python, Excel, Communication)")
    education = st.text_input("Your Education (e.g. B.Tech CSE, B.Com)")
    goals = st.text_input("Your Career Goals (e.g. DevOps Engineer, Data Scientist)")

    submit = st.button("Generate Career Guidance", use_container_width=True)

    if submit:
        if not all([name.strip(), interests.strip(), skills.strip(), education.strip(), goals.strip()]):
            st.error("⚠️ Please fill all fields!")
            st.markdown('</div>', unsafe_allow_html=True)
            return

        with st.spinner("Analyzing your profile and preparing a detailed guidance..."):
            advice = get_career_advice(
                clean_text(interests),
                clean_text(skills),
                clean_text(education),
                clean_text(goals),
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

        st.markdown("---")
        st.subheader(f"📄 Career Guidance for {name}")

        st.markdown(
            f"""
            <div style="
                background:#111827; 
                border-left:4px solid #2563eb; 
                padding:18px; 
                border-radius:10px;
                box-shadow:0 12px 30px rgba(15,23,42,0.65);
                color:#e5e7eb;
                font-size:0.95rem;
            ">
                {advice}
            </div>
            """,
            unsafe_allow_html=True,
        )

        pdf_bytes = generate_pdf(name, interests, skills, education, goals, advice)
        st.download_button(
            label="📥 Download Guidance as PDF",
            data=pdf_bytes,
            file_name=f"career_guidance_{name.replace(' ', '_')}.pdf",
            mime="application/pdf",
        )

    st.markdown('</div>', unsafe_allow_html=True)


def render_chat():
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.subheader("💬 Career Chat Assistant")
    st.write("Ask anything about roles, skills, tech stacks, salaries, or study plans.")

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
                reply = career_chat_reply(user_input)
                st.markdown(reply)

        st.session_state["chat_messages"].append({"role": "assistant", "content": reply})

    st.markdown('</div>', unsafe_allow_html=True)


def render_history():
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.subheader("📚 Session History")

    history = st.session_state["history"]
    if not history:
        st.info("No history yet. Generate guidance from the Career Guidance tab.")
        st.markdown('</div>', unsafe_allow_html=True)
        return

    for i, item in enumerate(reversed(history), start=1):
        with st.expander(f"{i}. {item['time']} — {item['name']} ({item['goals']})"):
            st.write(f"**Interests:** {item['interests']}")
            st.write(f"**Skills:** {item['skills']}")
            st.write(f"**Education:** {item['education']}")
            st.write(f"**Goals:** {item['goals']}")
            st.markdown("---")
            st.markdown(item["advice"])

    st.markdown('</div>', unsafe_allow_html=True)


def render_about():
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.subheader("ℹ️ About")

    st.markdown(
        """
This AI Career Guidance tool is designed to support students and early professionals in India by providing:

- A shortlist of relevant **career options**
- A breakdown of **required vs current skills**
- A **step-by-step roadmap** you can follow
- Basic **resume** and **interview** pointers

**Tech stack:**

- Python + Streamlit for the application  
- Groq API (`openai/gpt-oss-20b`) for the AI layer  
- Deployed on Streamlit Community Cloud
"""
    )

    st.markdown('</div>', unsafe_allow_html=True)


def render_contact():
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.subheader("📬 Contact")

    st.markdown(
        """
Update this section with your real details when you're ready to share publicly.

**Example layout:**

- 📧 Email: `youremail@example.com`  
- 💼 LinkedIn: `https://linkedin.com/in/your-profile`  
- 🐙 GitHub: `https://github.com/your-username`  

You can change the text directly in the code.
"""
    )
    st.markdown('</div>', unsafe_allow_html=True)


def render_settings():
    st.markdown('<div class="page-container">', unsafe_allow_html=True)
    st.subheader("⚙️ Settings")

    theme = st.radio(
        "Theme",
        ["Dark", "Light"],
        index=0 if st.session_state["theme"] == "Dark" else 1,
    )
    st.session_state["theme"] = theme

    if st.button("Clear Session History"):
        st.session_state["history"] = []
        st.success("History cleared for this session.")

    if st.button("Reset Chat Assistant"):
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": "Hi! I'm your AI career assistant. Ask me anything about careers, skills, or learning paths.",
            }
        ]
        st.success("Chat reset.")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------
# ROUTER
# -----------------------------------------------------
if page == "Home":
    render_home()
elif page == "Career Guidance":
    render_career_guidance()
elif page == "Career Chat":
    render_chat()
elif page == "History":
    render_history()
elif page == "About":
    render_about()
elif page == "Contact":
    render_contact()
elif page == "Settings":
    render_settings()

# close global page-container opened near nav
st.markdown('</div>', unsafe_allow_html=True)
