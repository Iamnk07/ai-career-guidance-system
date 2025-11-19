import os
import re

import streamlit as st
from dotenv import load_dotenv

# NEW official SDK
from google import genai

# --------------------------------------------------
# 1. LOAD API KEY (from env or Streamlit secrets)
# --------------------------------------------------
load_dotenv()  # loads .env locally (not used on Streamlit Cloud)

API_KEY = (
    os.getenv("GOOGLE_API_KEY")
    or st.secrets.get("GOOGLE_API_KEY", "")
)

if not API_KEY:
    st.error(
        "🚨 GOOGLE_API_KEY is missing.\n\n"
        "Add it in Streamlit → Settings → Secrets as:\n"
        'GOOGLE_API_KEY="your_real_key_here"'
    )
    st.stop()

# Create Gemini client
client = genai.Client(api_key=API_KEY)

# Use a **current free-tier model**
MODEL_NAME = "gemini-2.5-flash"   # from official models list


# --------------------------------------------------
# 2. HELPER FUNCTIONS
# --------------------------------------------------
def clean_input(text: str) -> str:
    """Remove extra symbols and spaces from user input."""
    return re.sub(r"[^\w\s]", "", text).strip() if text else ""


def get_career_advice(interests: str, skills: str, education: str, goals: str) -> str:
    """Call Gemini API and return formatted career advice."""
    prompt = f"""
You are an expert career counselor mentoring a B.Tech student in India.

User profile:
- Interests: {interests}
- Skills: {skills}
- Education: {education}
- Career goals: {goals}

TASK:
1. Suggest **4 specific career paths** suitable for this profile.
   For EACH career path, include:
   - Job Title
   - Short description (India context)
   - Required technical skills
   - Required soft skills
   - Skill gap: what is missing from current skills
   - 3–5 step roadmap (projects, courses, internships)
   - Average salary in INR (junior level, approximate)
   - Remote / onsite / hybrid options

2. Then give **General Guidance**:
   - How to improve skills (free + paid resources)
   - Resume & GitHub tips for freshers
   - Networking tips (LinkedIn, hackathons, meetups)
   - Interview preparation tips for Indian companies

FORMAT:
- Use Markdown with proper headings (##, ###).
- Use bullet points (•) and sub-bullets where helpful.
- Be clear, practical and motivating.
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
            f"({str(e)}). Check your API key, model name, or internet."
        )


# --------------------------------------------------
# 3. STREAMLIT PAGE CONFIG + STYLES
# --------------------------------------------------
st.set_page_config(page_title="AI Career Guidance System", page_icon="🚀", layout="centered")

st.markdown(
    """
    <style>
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(-20px);}
        to {opacity: 1; transform: translateY(0);}
    }
    .welcome-container {
        text-align: center;
        padding: 90px 20px 40px 20px;
        animation: fadeIn 0.8s ease-out;
    }
    .welcome-title {
        font-size: 3rem;
        color: #ffffff;
        margin-bottom: 0.5rem;
    }
    .welcome-subtitle {
        font-size: 1.1rem;
        color: #dddddd;
    }
    .main-block {
        background-color: #111827;
        padding: 20px;
        border-radius: 16px;
    }
    .response-box {
        background-color: #020617;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #1f2937;
    }
    .user-profile-box {
        border-left: 4px solid #3b82f6;
        padding-left: 10px;
        margin: 10px 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --------------------------------------------------
# 4. SESSION STATE
# --------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = []


# --------------------------------------------------
# 5. HEADER
# --------------------------------------------------
st.markdown(
    """
    <div class="welcome-container">
        <h1 class="welcome-title">🚀 AI Career Guidance System 📖</h1>
        <p class="welcome-subtitle">
            Discover your ideal career path with AI-powered guidance, tailored for B.Tech students.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='main-block'>", unsafe_allow_html=True)

st.subheader("Tell us about yourself")

# --------------------------------------------------
# 6. FORM
# --------------------------------------------------
with st.form("career_form"):
    name = st.text_input("Your Full Name", placeholder="e.g., Niyaz Khan")
    interests = st.text_input("Interests (e.g., AI, Web Development, DevOps)")
    skills = st.text_input("Skills (e.g., Python, teamwork, problem solving)")
    education = st.text_input("Education (e.g., B.Tech in Computer Science)")
    goals = st.text_input("Career Goals (e.g., DevOps Engineer, Data Scientist)")
    submitted = st.form_submit_button("Get Career Advice")

if submitted:
    if not all([name, interests, skills, education, goals]):
        st.error("Please fill **all fields** before generating advice.")
    else:
        # Clean input
        name_clean = clean_input(name)
        interests_clean = clean_input(interests)
        skills_clean = clean_input(skills)
        education_clean = clean_input(education)
        goals_clean = clean_input(goals)

        with st.spinner("✨ Crafting your personalized career roadmap..."):
            advice_text = get_career_advice(
                interests_clean, skills_clean, education_clean, goals_clean
            )

        st.session_state.history.append(
            {
                "name": name_clean,
                "inputs": {
                    "interests": interests_clean,
                    "skills": skills_clean,
                    "education": education_clean,
                    "goals": goals_clean,
                },
                "advice": advice_text,
            }
        )
        st.success("Career advice generated successfully! 🎉")

# --------------------------------------------------
# 7. SIDEBAR – PROFILE SNAPSHOT
# --------------------------------------------------
with st.sidebar:
    st.header("Quick Tips 💡")
    st.markdown(
        """
        - Be **specific** with your skills (e.g., *Python, React, Docker*).
        - Try **different interests** to explore more career paths.
        - Start **projects & internships early** in B.Tech!
        """
    )

    if st.session_state.history:
        latest = st.session_state.history[-1]
        st.markdown("### Your Profile")
        st.markdown(f"**Name:** {latest['name']}")
        st.markdown(f"**Education:** {latest['inputs']['education']}")
        st.markdown(f"**Interests:** {latest['inputs']['interests']}")
        st.markdown(f"**Goals:** {latest['inputs']['goals']}")

# --------------------------------------------------
# 8. MAIN RESULT DISPLAY
# --------------------------------------------------
if st.session_state.history:
    latest = st.session_state.history[-1]

    st.markdown("## 📌 Your Personalized Career Guidance:")
    st.markdown(
        f"<div class='user-profile-box'><b>Skills:</b> {latest['inputs']['skills']}</div>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='response-box'>", unsafe_allow_html=True)
    st.markdown(latest["advice"], unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Show previous plans if multiple
    if len(st.session_state.history) > 1:
        st.markdown("### Previous Career Plans")
        for i, entry in enumerate(st.session_state.history[:-1], start=1):
            with st.expander(f"{entry['name']}'s Plan #{i}"):
                st.markdown(f"**Education:** {entry['inputs']['education']}")
                st.markdown(f"**Goals:** {entry['inputs']['goals']}")
                st.markdown(entry["advice"], unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close main-block

st.markdown(
    """
    <div style="text-align:center; color:#9ca3af; margin-top:20px;">
        Made with ❤️ by Team Rush Adrenalin
    </div>
    """,
    unsafe_allow_html=True,
)
