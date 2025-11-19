import streamlit as st
import os
import re
from google import genai  # ✅ NEW Google AI Library

# ===========================
# 🔐 Load API Key (from Streamlit Secrets)
# ===========================
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ GOOGLE_API_KEY missing! Add it in Streamlit → Settings → Secrets.")
    st.stop()

client = genai.Client(api_key=API_KEY)

# ===========================
# ✔ Correct Latest Model Name
# ===========================
MODEL_NAME = "gemini-1.5-flash-latest"


# ===========================
# 🧹 Clean User Input
# ===========================
def clean_input(text):
    return re.sub(r"[^\w\s]", "", text).strip() if text else ""


# ===========================
# 🤖 Generate AI Career Advice
# ===========================
def get_career_advice(interests, skills, education, goals):

    prompt = f"""
You are an expert career counselor in India. Provide detailed, personalized guidance.

### User Profile:
- **Interests:** {interests}
- **Skills:** {skills}
- **Education:** {education}
- **Career Goals:** {goals}

### Requirements:
1. Suggest **4 career paths** with:
   - Job description
   - Required skills
   - Missing skills (Skill Gap)
   - Step-by-step roadmap
   - Salary (INR), demand, remote work
2. Give resume tips, interview tips, and free learning resources.
3. Tone must be **motivational** and formatted with **headings & bullet points**.
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
# 🎨 Streamlit UI
# ===========================
st.set_page_config(page_title="AI Career Guidance", page_icon="🚀")

st.title("🚀 AI Career Guidance System")
st.write("Get personalized career suggestions powered by Google Gemini 🔥")

name = st.text_input("Your Name")
interests = st.text_input("Your Interests (e.g., AI, Web Dev)")
skills = st.text_input("Your Skills (e.g., Python)")
education = st.text_input("Your Education (e.g., B.Tech CSE)")
goals = st.text_input("Your Career Goals (e.g., Software Engineer)")

if st.button("Get Career Advice"):
    if not all([name, interests, skills, education, goals]):
        st.error("⚠️ Please fill all fields!")
    else:
        st.success("✅ Career advice generated successfully!")

        advice = get_career_advice(
            clean_input(interests),
            clean_input(skills),
            clean_input(education),
            clean_input(goals)
        )

        st.markdown(advice)


