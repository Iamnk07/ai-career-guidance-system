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
# THEME / CSS
# -----------------------------------------------------
def apply_theme():
    theme = st.session_state.get("theme", "Dark")
    if theme == "Dark":
        bg_color = "#050814"
        card_bg = "#101320"
        text_color = "#e4e4e4"
    else:
        bg_color = "#f5f5f5"
        card_bg = "#ffffff"
        text_color = "#222222"

    st.markdown(
        f"""
        <style>
            body {{
                background-color: {bg_color};
                color: {text_color};
            }}
            .main {{
                background-color: {bg_color};
            }}
            .stTextInput > div > div > input,
            .stTextArea > div > textarea {{
                background-color: {card_bg};
                color: {text_color};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

apply_theme()

# -----------------------------------------------------
# SPLASH SCREEN (4 SECONDS)
# -----------------------------------------------------
def show_splash():
    splash_html = """
    <style>
    .splash-container {
        position: fixed;
        inset: 0;
        background: radial-gradient(circle at top left, #4f46e5, transparent 40%),
                    radial-gradient(circle at bottom right, #ec4899, transparent 40%),
                    #020617;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        z-index: 9999;
    }
    .splash-content {
        text-align: center;
        color: #e5e7eb;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }
    .splash-title {
        font-size: 2.6rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.5rem;
    }
    .splash-subtitle {
        font-size: 1rem;
        opacity: 0.8;
        max-width: 420px;
        margin: 0 auto;
    }

    .orb {
        position: absolute;
        border-radius: 999px;
        filter: blur(18px);
        opacity: 0.7;
        mix-blend-mode: screen;
        background: conic-gradient(from 180deg at 50% 50%, #22d3ee, #4f46e5, #a855f7, #22d3ee);
        animation: float 9s ease-in-out infinite alternate;
    }
    .orb.small {
        width: 160px;
        height: 160px;
    }
    .orb.medium {
        width: 260px;
        height: 260px;
    }
    .orb.large {
        width: 360px;
        height: 360px;
    }
    .orb.one { top: -60px; left: -40px; animation-delay: 0s; }
    .orb.two { bottom: -80px; right: -40px; animation-delay: 1.5s; }
    .orb.three { top: 40%; left: 65%; animation-delay: 3s; }

    @keyframes float {
        0%   { transform: translate3d(0, 0, 0) scale(1); }
        50%  { transform: translate3d(30px, -25px, 40px) scale(1.1); }
        100% { transform: translate3d(-20px, 30px, -40px) scale(0.95); }
    }

    .glow-ring {
        width: 220px;
        height: 220px;
        border-radius: 50%;
        border: 1px solid rgba(148,163,184,0.25);
        box-shadow:
            0 0 60px rgba(129,140,248,0.4),
            0 0 120px rgba(236,72,153,0.3);
        margin: 0 auto 1.6rem auto;
        display: flex;
        align-items: center;
        justify-content: center;
        position: relative;
        overflow: hidden;
    }
    .ring-inner {
        width: 70%;
        height: 70%;
        border-radius: 999px;
        background: radial-gradient(circle at 0% 0%, #22c55e, transparent 40%),
                    radial-gradient(circle at 100% 100%, #38bdf8, transparent 40%),
                    #020617;
        opacity: 0.9;
    }
    </style>

    <div class="splash-container">
        <div class="orb small one"></div>
        <div class="orb medium two"></div>
        <div class="orb large three"></div>

        <div class="splash-content">
            <div class="glow-ring">
                <div class="ring-inner"></div>
            </div>
            <div class="splash-title">WELCOME TO</div>
            <div class="splash-title" style="font-size:2rem; letter-spacing:0.18em;">
                AI CAREER GUIDANCE
            </div>
            <p class="splash-subtitle">
                Smart, personalized roadmap for your future career — powered by AI.
            </p>
        </div>
    </div>
    """
    st.markdown(splash_html, unsafe_allow_html=True)

# show splash only once per session
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
            model="openai/gpt-oss-20b",  # ✅ model you have access to
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
# NAVBAR (TOP)
# -----------------------------------------------------
st.markdown(
    """
    <style>
    .nav-container {
        display: flex;
        justify-content: center;
        margin-bottom: 1.2rem;
    }
    .nav-title {
        text-align:center;
        font-size: 1.6rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .nav-subtitle {
        text-align:center;
        font-size: 0.9rem;
        opacity: 0.7;
        margin-bottom: 0.6rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="nav-title">🚀 AI Career Guidance</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="nav-subtitle">Plan your career path with AI – simple, fast, personalized.</div>',
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
        <div style="text-align:center; padding: 20px 10px;">
            <h2>👋 Welcome!</h2>
            <p style="font-size:16px; max-width:720px; margin: 0 auto;">
                This platform helps you explore career options, understand required skills,
                and build a roadmap using AI. <br><br>
                Start with <b>Career Guidance</b> to get a full AI-generated plan, or use
                <b>Career Chat</b> to ask any career question.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("✨ Go to Career Guidance", use_container_width=True):
            st.session_state["main_nav"] = "Career Guidance"
            st.rerun()
    with col2:
        if st.button("💬 Open Career Chat", use_container_width=True):
            st.session_state["main_nav"] = "Career Chat"
            st.rerun()


def render_career_guidance():
    st.subheader("🧠 AI Career Guidance Form")

    name = st.text_input("Your Name")
    interests = st.text_input("Your Interests (e.g. Coding, Finance, Design)")
    skills = st.text_input("Your Skills (e.g. Python, Excel, Communication)")
    education = st.text_input("Your Education (e.g. B.Tech CSE, B.Com)")
    goals = st.text_input("Your Career Goals (e.g. DevOps Engineer, Data Scientist)")

    submit = st.button("🚀 Generate Career Guidance", use_container_width=True)

    if submit:
        if not all([name.strip(), interests.strip(), skills.strip(), education.strip(), goals.strip()]):
            st.error("⚠️ Please fill all fields!")
            return

        with st.spinner("⏳ Analyzing your profile and generating guidance..."):
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
        st.subheader(f"📄 Career Guidance for **{name}**")

        st.markdown(
            f"""
            <div style="
                background:#ffffff10; 
                border-left:6px solid #4CAF50; 
                padding:20px; 
                border-radius:10px;
                box-shadow:0 4px 10px rgba(0,0,0,0.4);
                color:#eee;
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


def render_chat():
    st.subheader("💬 Career Chat Assistant")
    st.write("Ask anything about tech roles, salaries, skills, roadmaps, or study plans.")

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


def render_history():
    st.subheader("📚 Session History")

    history = st.session_state["history"]
    if not history:
        st.info("No history yet. Generate guidance from the **Career Guidance** tab.")
        return

    for i, item in enumerate(reversed(history), start=1):
        with st.expander(f"{i}. {item['time']} — {item['name']} ({item['goals']})"):
            st.write(f"**Interests:** {item['interests']}")
            st.write(f"**Skills:** {item['skills']}")
            st.write(f"**Education:** {item['education']}")
            st.write(f"**Goals:** {item['goals']}")
            st.markdown("---")
            st.markdown(item["advice"])


def render_about():
    st.subheader("ℹ️ About")
    st.markdown(
        """
This AI Career Guidance System helps students and early professionals:

- Discover relevant **career options**
- Understand **required & missing skills**
- Get a **step-by-step roadmap**
- Prepare for **resume** and **interviews**

It is built using:

- **Python + Streamlit** for the UI  
- **Groq API (`openai/gpt-oss-20b`)** for AI  
- Deployed on **Streamlit Community Cloud**
"""
    )


def render_contact():
    st.subheader("📬 Contact")
    st.markdown(
        """
You can customize this section with your real contact info.

**Example layout:**

- 📧 Email: `yourmail@example.com`  
- 💼 LinkedIn: `https://linkedin.com/in/your-profile`  
- 🐙 GitHub: `https://github.com/your-username`  

Update these values directly in the code to match your real details.
"""
    )


def render_settings():
    st.subheader("⚙️ Settings")

    theme = st.radio(
        "Theme",
        ["Dark", "Light"],
        index=0 if st.session_state["theme"] == "Dark" else 1,
    )
    st.session_state["theme"] = theme

    if st.button("🧹 Clear Session History"):
        st.session_state["history"] = []
        st.success("History cleared for this session.")

    if st.button("🔁 Reset Chat Assistant"):
        st.session_state["chat_messages"] = [
            {
                "role": "assistant",
                "content": "Hi! I'm your AI career assistant. Ask me anything about careers, skills, or learning paths.",
            }
        ]
        st.success("Chat reset.")

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

