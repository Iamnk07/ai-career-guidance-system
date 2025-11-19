import streamlit as st
import google.generativeai as genai
import re
import os
from dotenv import load_dotenv

# Load API key from Streamlit Secrets / .env
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure API
genai.configure(api_key=API_KEY)

# Use free model (works WITHOUT billing)
model = genai.GenerativeModel("gemini-pro")

def clean_input(text):
    return re.sub(r'[^\w\s]', '', text).strip() if text else ""

def get_career_advice(interests, skills, education, goals):
    prompt = f"""
You are an expert career counselor mentoring a B.Tech or other students in India. Provide highly personalized, realistic, and actionable career advice based on:
- Interests: {interests}
- Skills: {skills}
- Education: {education}
- Career Goals: {goals}

**Requirements**:
- Suggest 4 career paths relevant to the user’s profile, each including:
  1. **Job Title and Description**: Describe the role and its impact in India’s job market.
  2. **Required Skills**: List technical and soft skills, with tools or certifications.
  3. **Skill Gaps**: Compare user's current skills with required skills for each suggested career path, highlighting key areas for improvement.
  4. **Steps to Achieve**: Provide a 3-5 step roadmap tailored to B.Tech students in India (e.g., projects, internships, courses).
  5. **Market Insights**: Include average salary (INR), demand, and remote work options.
  6. **Challenges and Solutions**: Address obstacles (e.g., competition) with practical solutions.
- Provide additional advice on :
  - Resume Building
  - LinkedIn Profile
  - GitHub Projects
  - Interview Tips (India-specific)
- Use headings (##), bullet points (**) for clean formatting.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: Unable to fetch advice ({str(e)}). Check your internet or API key."

# Streamlit Page Settings
st.set_page_config(page_title="AI Career Guide", page_icon="🚀", layout="centered")

# CSS Styling
st.markdown("""
    <style>
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(-20px);}
        to {opacity: 1; transform: translateY(0);}
    }
    .welcome-container {text-align: center; padding: 90px 20px; animation: fadeIn 1s ease-out;}
    .welcome-title {font-size: 3.5rem; color: #002855; margin-bottom: 30px;}
    .main {background-color: #f8f9fa; padding: 20px; border-radius: 12px;}
    .stButton>button {background-color: #0055b3; color: white; border-radius: 10px; padding: 10px; font-weight: bold;}
    .stButton>button:hover {background-color: #003d82;}
    .stTextInput>div>input {border: 2px solid #0055b3; border-radius: 10px; padding: 8px;}
    h1 {color: #002855; text-align: center; font-size: 36px;}
    .response-box {background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
    </style>
""", unsafe_allow_html=True)

# Session State
if 'show_main' not in st.session_state:
    st.session_state.show_main = False
if 'history' not in st.session_state:
    st.session_state.history = []

# Welcome Page
if not st.session_state.show_main:
    st.markdown("""
        <div class="welcome-container">
            <h1 class="welcome-title">🚀 AI Career Guidance System 📖</h1>
            <p style="font-size: 1.2rem; color: #555;">
                Discover your ideal career path with AI-powered guidance
            </p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Get Started", key="start_btn"):
        st.session_state.show_main = True
        st.rerun()
    st.stop()

# Main App Form
st.title("🚀 AI-Career Guidance System 📖")
st.markdown("## Great career starts with great guidance & You are at right place")

with st.form("career_form"):
    user_name = st.text_input("Your Full Name")
    interests = st.text_input("Interests (e.g., AI, Web development)")
    skills = st.text_input("Skills (e.g., Python, teamwork)")
    education = st.text_input("Education (e.g., B.Tech CS)")
    goals = st.text_input("Goals (e.g., software engineer)")
    submit = st.form_submit_button("Get Career Advice")

if submit:
    if not all([user_name, interests, skills, education, goals]):
        st.error("Please fill all fields.")
    else:
        with st.spinner("Crafting your personalized career path..."):
            advice = get_career_advice(
                clean_input(interests),
                clean_input(skills),
                clean_input(education),
                clean_input(goals)
            )
        st.success("Career advice generated successfully!")
        st.markdown("### 📌 Your Personalized Career Guidance:")
        st.markdown(advice, unsafe_allow_html=True)
