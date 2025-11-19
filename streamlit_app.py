import streamlit as st
import os
import re
from google.genai import Client   # ✅ CORRECT new library

# ===========================
# Load API key
# ===========================
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY missing! Add it in Streamlit → Settings → Secrets.")
    st.stop()

client = Client(api_key=API_KEY)

MODEL_NAME = "gemini-1.5-flash-latest"


def clean_input(text):
    return re.sub(r"[^\w\s]", "", text).strip() if text else ""


def get_career_advice(interests, skills, education, goals):

    prompt = f"""
You are an expert career counselor in India. Provide detailed, personalized guidance.

### User Profile:
- **Interests:** {interests}
- **Skills:** {skills}
- **Education:** {education}
- **Career Goals:** {goals}

### Requirements:
1. Suggest 4 career paths with:
   - Job description
   - Required skills
   - Missing skills (Skill Gap)
   - Step-by-step roadmap
   - Salary (INR), demand, remote work
2. Give resume tips, interview tips, and free learning resources.
3. Tone must be motivational and formatted nicely.
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text

    except Exception as e:
        return f"❌ Error: {str(e)}"


# ===========================
# UI
# ===========================
st.set_page_config(page_title="AI Career Guidance", page_icon="🚀")
st.title("🚀 AI Career Guidance System")

name = st.text_input("Your Name")
interests = st.text_input("Your Interests")
skills = st.text_input("Your Skills")
education = st.text_input("Your Education")
goals = st.text_input("Your Career Goals")

if st.button("Get Career Advice"):
    if not all([name, interests, skills, education, goals]):
        st.error("⚠️ Please fill all fields!")
    else:
        st.success("Advice generated!")
        advice = get_career_advice(
            clean_input(interests),
            clean_input(skills),
            clean_input(education),
            clean_input(goals)
        )
        st.markdown(advice)

