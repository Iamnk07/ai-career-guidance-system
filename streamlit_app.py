import os
import re
import streamlit as st
from google import genai
from dotenv import load_dotenv

# -----------------------------
# Load API key
# -----------------------------
load_dotenv()

# Try Streamlit secrets first, then environment variable
API_KEY = st.secrets.get("GEMINI_API_KEY", None) or os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error(
        "❌ GEMINI_API_KEY not found.\n\n"
        "Add it in Streamlit → My apps → … → Edit secrets:\n\n"
        'GEMINI_API_KEY = "your-real-key-here"'
    )
    st.stop()

# Configure Gemini client (new SDK)
client = genai.Client(api_key=API_KEY)

# Use latest general-purpose text model (free tier available)
MODEL_NAME = "gemini-2.5-flash"


# -----------------------------
# Helper functions
# -----------------------------
def clean_input(text: str) -> str:
    """Remove extra symbols/whitespace from user input."""
    return re.sub(r"[^\w\s]", "", text).strip() if text else ""


def get_career_advice(interests: str, skills: str, education: str, goals: str) -> str:
    """Call Gemini API to get personalized career advice."""
    prompt = f"""
You are an expert career counselor for Indian B.Tech students.

User profile:
- Interests: {interests}
- Skills: {skills}
- Education: {education}
- Career goals: {goals}

Requirements:
1. Suggest **4 suitable career paths**. For each path give:
   - Job Title
   - 3–4 line description (India context)
   - Required technical + soft skills
   - Missing skills for this user (skill gap)
   - 3–5 concrete steps to reach that role (projects, internships, courses)
   - Approx salary range in INR (fresher + 3–5 years)
   - Remote / hybrid possibilities in India.

2. General advice:
   - How this student should build resume + GitHub + LinkedIn
   - What type of projects to do
   - Interview preparation tips for Indian product / service companies.

Formatting:
- Use markdown headings (##, ###), bullet points and sub-bullets.
- Keep the tone motivating but realistic.
"""
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
        )
        return response.text
    except Exception as e:
        return (
            "Error: Unable to fetch advice "
            f"({str(e)}). Check your API key, model name, or network."
        )


# -----------------------------
# Streamlit UI setup
# -----------------------------
st.set_page_config(
    page_title="AI Career Guidance System",
    page_icon="🚀",
    layout="centered",
)

# Basic styling
st.markdown(
    """
<style>
body { background-color: #0e1117; }
.main { background-color: #0e1117; }
.response-box {
    background-color: #ffffff;
    padding: 1rem 1.2rem;
    border-radius: 0.6rem;
    box-shadow: 0 2px 5px rgba(0,0,0,0.3);
}
</style>
""",
    unsafe_allow_html=True,
)

# Session state
if "history" not in st.session_state:
    st.session_state.history = []


# -----------------------------
# Main app
# -----------------------------
st.title("🚀 AI Career Guidance System 📖")
st.markdown("### Great careers start with great guidance — you’re in the right place!")

with st.form("career_form"):
    user_name = st.text_input("Your Full Name", placeholder="e.g., Niyaz Khan")
    interests = st.text_input(
        "Interests (e.g., AI, Web development)",
        placeholder="e.g., DevOps, cloud, backend",
    )
    skills = st.text_input(
        "Skills (e.g., Python, teamwork)", placeholder="e.g., Python, Git, Linux"
    )
    education = st.text_input(
        "Education (e.g., B.Tech CS)", placeholder="e.g., B.Tech in Computer Science"
    )
    goals = st.text_input(
        "Goals (e.g., software engineer)", placeholder="e.g., DevOps engineer"
    )

    submitted = st.form_submit_button("Get Career Advice")

if submitted:
    if not all([user_name, interests, skills, education, goals]):
        st.error("⚠️ Please fill **all fields** before requesting advice.")
    else:
        with st.spinner("✨ Thinking about your best career options..."):
            advice = get_career_advice(
                clean_input(interests),
                clean_input(skills),
                clean_input(education),
                clean_input(goals),
            )

        st.session_state.history.append(
            {
                "name": clean_input(user_name),
                "inputs": {
                    "interests": interests,
                    "skills": skills,
                    "education": education,
                    "goals": goals,
                },
                "advice": advice,
            }
        )

# Sidebar – profile & tips
with st.sidebar:
    st.header("💡 Quick Career Tips")
    st.markdown(
        """
- Be specific about skills (e.g., *Python + FastAPI* not just *coding*)
- Build **2–3 solid projects** and put them on GitHub
- Start internships or freelance work as early as possible
- Keep your LinkedIn updated and active
"""
    )

    if st.session_state.history:
        latest = st.session_state.history[-1]
        st.subheader("🙋 Your latest profile")
        st.write(f"**Name:** {latest['name']}")
        st.write(f"**Education:** {latest['inputs']['education']}")
        st.write(f"**Interests:** {latest['inputs']['interests']}")
        st.write(f"**Goals:** {latest['inputs']['goals']}")


# Show current advice
if st.session_state.history:
    latest = st.session_state.history[-1]
    st.subheader("📌 Your Personalized Career Guidance:")
    st.markdown("<div class='response-box'>", unsafe_allow_html=True)
    st.markdown(latest["advice"], unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Older plans
if len(st.session_state.history) > 1:
    st.markdown("---")
    st.subheader("🕒 Previous career plans")
    for i, entry in enumerate(st.session_state.history[:-1], start=1):
        with st.expander(f"{entry['name']}'s plan #{i}"):
            st.write(f"**Education:** {entry['inputs']['education']}")
            st.write(f"**Goals:** {entry['inputs']['goals']}")
            st.markdown(entry["advice"], unsafe_allow_html=True)

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#888;'>Made with ❤️ for your college project</div>",
    unsafe_allow_html=True,
)

