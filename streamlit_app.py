import streamlit as st
from groq import Groq
from datetime import datetime
from fpdf import FPDF
import io

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
        {"role": "assistant",
         "content": "Hi! I'm your AI career assistant. Ask me anything about careers, skills, or learning paths."}
    ]

# -----------------------------------------------------
# THEME / CSS
# -----------------------------------------------------
def apply_theme():
    theme = st.session_state.get("theme", "Dark")
    if theme == "Dark":
        bg_color = "#0e1117"
        card_bg = "#1e1e1e"
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
            model="openai/gpt-oss-20b",
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
    # remove very fancy characters to avoid font issues
    safe_advice = advice.replace("•", "-")
    pdf.multi_cell(0, 6, safe_advice)

    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer.read()

# -----------------------------------------------------
# SIDEBAR NAVIGATION
# -----------------------------------------------------
with st.sidebar:
    st.title("🎯 AI Career Guide")

    page = st.radio(
        "Navigate",
        ["Home", "Career Guidance", "Career Chat", "History",
         "Resume Tips", "Interview Tips", "Settings"],
        index=1,
    )

    st.markdown("---")
    st.caption("Built with Streamlit + Groq")

# -----------------------------------------------------
# PAGE RENDER FUNCTIONS
# -----------------------------------------------------
def render_home():
    st.markdown(
        """
        <div style="text-align:center; padding: 30px 10px;">
            <h1>🚀 Welcome to AI Career Guidance System</h1>
            <p style="font-size:18px; max-width:700px; margin: 0 auto;">
                This app helps you explore career paths, understand required skills, and
                plan your roadmap using AI. Use the sidebar to navigate:
                <br><br>
                <b>Career Guidance</b> – Get a full career plan from your details. <br>
                <b>Career Chat</b> – Chat with an AI about any career doubt. <br>
                <b>History</b> – See your previous results for this session.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_career_guidance():
    st.markdown(
        """
        <div style="text-align:center; padding: 10px 0 20px 0;">
            <h2>🧠 AI Career Guidance Form</h2>
            <p>Fill the form and get a complete career roadmap, skills, salary range & more.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container():
        st.subheader("📝 Enter Your Details")

        name = st.text_input("Your Name")
        interests = st.text_input("Your Interests (e.g. Coding, Finance, Design)")
        skills = st.text_input("Your Skills (e.g. Python, Excel, Communication)")
        education = st.text_input("Your Education (e.g. B.Tech CSE, B.Com)")
        goals = st.text_input("Your Career Goals (e.g. DevOps Engineer, Data Scientist)")

        submit = st.button("✨ Get Career Guidance", use_container_width=True)

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

        # Save to history
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

        # PDF download
        pdf_bytes = generate_pdf(name, interests, skills, education, goals, advice)
        st.download_button(
            label="📥 Download Guidance as PDF",
            data=pdf_bytes,
            file_name=f"career_guidance_{name.replace(' ', '_')}.pdf",
            mime="application/pdf",
        )


def render_chat():
    st.header("💬 Career Chat Assistant")
    st.write("Ask any question about careers, skills, learning paths, or tech roles.")

    for msg in st.session_state["chat_messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask your career question here...")
    if user_input:
        # show user message
        st.session_state["chat_messages"].append(
            {"role": "user", "content": user_input}
        )
        with st.chat_message("user"):
            st.markdown(user_input)

        # assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                reply = career_chat_reply(user_input)
                st.markdown(reply)

        st.session_state["chat_messages"].append(
            {"role": "assistant", "content": reply}
        )


def render_history():
    st.header("📚 Session History")

    history = st.session_state["history"]
    if not history:
        st.info("No history yet. Generate guidance from the **Career Guidance** page.")
        return

    for i, item in enumerate(reversed(history), start=1):
        with st.expander(
            f"{i}. {item['time']} — {item['name']} ({item['goals']})", expanded=False
        ):
            st.write(f"**Interests:** {item['interests']}")
            st.write(f"**Skills:** {item['skills']}")
            st.write(f"**Education:** {item['education']}")
            st.write(f"**Goals:** {item['goals']}")
            st.markdown("---")
            st.markdown(item["advice"])


def render_resume_tips():
    st.header("📄 Resume Tips (Static)")
    st.markdown(
        """
- Keep your resume **1 page** as a student / fresher.  
- Add a **strong summary** with your role target (e.g. “Aspiring DevOps Engineer”).  
- Highlight **Projects** with tech stack & outcomes.  
- Add **Skills** section: tools, languages, frameworks.  
- Use **action verbs**: built, implemented, automated, optimized.  
- Include **LinkedIn / GitHub** links.  
- Avoid long paragraphs. Use bullet points.
"""
    )


def render_interview_tips():
    st.header("🎤 Interview Tips (Static)")
    st.markdown(
        """
- Practice a short **self-introduction** (60–90 seconds).  
- Be ready to explain your **projects**: problem, solution, tech stack, impact.  
- Revise **CS fundamentals**: DSA basics, OOP, DBMS, OS (for tech roles).  
- Prepare for **behavioral questions** (“Tell me about a challenge…”)  
- Do mock interviews with friends or on platforms.  
- At the end, ask **1–2 smart questions** about the role or team.
"""
    )


def render_settings():
    st.header("⚙️ Settings")

    theme = st.radio("Theme", ["Dark", "Light"],
                     index=0 if st.session_state["theme"] == "Dark" else 1)
    st.session_state["theme"] = theme

    if st.button("Clear Session History"):
        st.session_state["history"] = []
        st.success("History cleared for this session.")

    if st.button("Reset Chat"):
        st.session_state["chat_messages"] = [
            {"role": "assistant",
             "content": "Hi! I'm your AI career assistant. Ask me anything about careers, skills, or learning paths."}
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
elif page == "Resume Tips":
    render_resume_tips()
elif page == "Interview Tips":
    render_interview_tips()
elif page == "Settings":
    render_settings()
