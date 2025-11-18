import streamlit as st
import google.generativeai as genai
import re
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

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
  4. **Steps to Achieve**: Provide a 3-5 step roadmap tailored to a B.Tech student in india (e.g., projects, internships, courses).
  5. **Market Insights**: Include average salary (INR), demand, and remote work options.
  6. **Challenges and Solutions**: Address obstacles (e.g., competition) with practical solutions.
- Provide general advice on:
  - Building a resume (e.g., GitHub, LinkedIn).
  - Networking (e.g., meetups, online platforms).
  - Skill development (e.g., free/paid resources like Coursera, YouTube).
  - Interview tips for Indian companies.
- Use a motivational tone to inspire confidence.
- Always Format with clear headings (##), bullet(**) and sub bullet points for readability.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: Unable to fetch advice ({str(e)}). Check your internet or API key."

# Page configuration and styles
st.set_page_config(page_title="AI Career Guide", page_icon="🚀", layout="centered")
st.markdown("""
    <style>
    /* Welcome Page Styles */
    @keyframes fadeIn {
        from {opacity: 0; transform: translateY(-20px);}
        to {opacity: 1; transform: translateY(0);}
    }
    
    @keyframes pulse {
        0% {transform: scale(1);}
        50% {transform: scale(1.05);}
        100% {transform: scale(1);}
    }
    
    .welcome-container {  
        text-align: center;
        padding: 90px 20px;
        animation: fadeIn 1s ease-out;
    }
    
    .welcome-title {
        font-size: 4rem;
        color: #001f5c;
        margin-bottom: 30px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .get-started-btn {
        animation: pulse 2s infinite;
        background: #0055b3 !important;
        border: none !important;
        padding: 15px 40px !important;
        font-size: 1.2rem !important;
        border-radius: 30px !important;
        transition: all 0.9s ease !important;
    }
    
    /* Main App Styles */
    .main {background-color: #ffff; padding: 20px; border-radius: 12px;}
    .stButton>button {background-color: #0055b3; color: white; border-radius: 10px; padding: 10px; font-weight: bold;}
    .stButton>button:hover {background-color: #003d82;}
    .stTextInput>div>input {border: 2px solid #0055b3; border-radius: 10px; padding: 8px;}
    h1 {color: #001f5c; text-align: center; font-size: 36px;}
    .stSpinner {text-align: center;}
    .response-box {background-color: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1);}
    .user-profile {color: #2c3e50; border-left: 4px solid #0055b3; padding-left: 15px; margin: 15px 0;}
    .sidebar-profile {background: #c10a0a; padding: 15px; border-radius: 8px; margin-top: 20px;}
    .sidebar-profile h3 {color: #0000; margin-bottom: 10px;}
    </style>
""", unsafe_allow_html=True)

# Session state initialization
if 'show_main' not in st.session_state:
    st.session_state.show_main = False
if 'history' not in st.session_state:
    st.session_state.history = []

# Welcome Page
if not st.session_state.show_main:
    st.markdown("""
        <div class="welcome-container">
            <h1 class="welcome-title">🚀AI Career Guidance System📖</h1>
            <p style="font-size: 1.2rem; color: #555; margin-bottom: 40px;">
                Discover your ideal career path with AI-powered guidance
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Get Started", key="start_btn", help="Begin your career journey"):
            st.session_state.show_main = True
            st.rerun()
    
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; margin-top: 50px;">
            <small>Powered by Team Rush Adrenalin</small>
        </div>
    """, unsafe_allow_html=True)
    st.stop()

# Main Application
st.title("🚀AI-Career Guidance System📖")
st.markdown("## Great career starts with great guidance & You are at right place")

with st.form("career_form"):
    user_name = st.text_input("Your Full Name", placeholder="Enter your name (e.g. Rohan Sharma)")
    interests = st.text_input("Interests (e.g., AI, Web development)", placeholder="Enter your area of interest..")
    skills = st.text_input("Skills (e.g., Python, teamwork)", placeholder="Enter your skills..")
    education = st.text_input("Education (e.g., B.Tech CS)", placeholder="Enter your education..")
    goals = st.text_input("Goals (e.g., software engineer)", placeholder="Enter your career goals..")
    submit = st.form_submit_button("Get Career Advice")

if submit:
    if not all([user_name, interests, skills, education, goals]):
        st.error("Please fill all fields to continue.")
    else:
        user_name = clean_input(user_name)
        interests = clean_input(interests)
        skills = clean_input(skills)
        education = clean_input(education)
        goals = clean_input(goals)

        with st.spinner("Crafting your career path..."):
            advice = get_career_advice(interests, skills, education, goals)
        
        st.session_state.history.append({
            "name": user_name,
            "inputs": {
                "interests": interests,
                "skills": skills,
                "education": education,
                "goals": goals
            },
            "advice": advice
        })

with st.sidebar:
    st.header("Career Tips")
    st.markdown("""
    - **Be Specific**: Mention exact skills (e.g., Python, Java)
    - **Explore Options**: Try different interests to discover new paths
    - **Act Fast**: Start projects or internships early in B.Tech!
    """)
    
    if st.session_state.history:
        latest_profile = st.session_state.history[-1]
        st.markdown("<div class='sidebar-profile'>", unsafe_allow_html=True)
        st.subheader(f"🙋Your Profile")
        st.markdown(f"**Full Name**: {latest_profile['name']}")
        st.markdown(f"**Education**: {latest_profile['inputs']['education']}")
        st.markdown(f"**Interests**: {latest_profile['inputs']['interests']}")
        st.markdown(f"**Goals**: {latest_profile['inputs']['goals']}")
        st.markdown("</div>", unsafe_allow_html=True)

if st.session_state.history:
    latest = st.session_state.history[-1]
    st.subheader(f"{latest['name']}'s Career Profile")
    st.markdown("<div class='user-profile'>", unsafe_allow_html=True)
    st.markdown(f"**Skills**: {latest['inputs']['skills']}")
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='response-box'>", unsafe_allow_html=True)
    st.markdown(latest['advice'], unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if len(st.session_state.history) > 1:
    st.subheader("Previous Career Plans")
    for i, entry in enumerate(st.session_state.history[:-1]):
        with st.expander(f"{entry['name']}'s Plan {i+1}"):
            st.markdown(f"**Education**: {entry['inputs']['education']}")
            st.markdown(f"**Goals**: {entry['inputs']['goals']}")
            st.markdown(entry['advice'], unsafe_allow_html=True)

st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; margin-top: 50px;'>
        Made with ❤️ By team Rush Adrenalin
    </div>
""", unsafe_allow_html=True)