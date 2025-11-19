import streamlit as st
from groq import Groq

# Load API key from Streamlit Secrets
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

def clean_text(text):
    if not text:
        return ""
    return text.strip()

def get_career_advice(interests, skills, education, goals):

    if not all([interests, skills, education, goals]):
        return "⚠️ Please fill all fields."

    prompt = f"""
You are an AI career counselor for Indian students.
Provide detailed guidance based on:

Interests: {interests}
Skills: {skills}
Education: {education}
Career Goals: {goals}

Give:
- 4 career paths
- Required skills
- Skill gaps
- Roadmap steps
- Salary (INR)
- Learning resources
- Resume tips
- Interview tips
"""

    try:
        response = client.chat.completions.create(
            model="llama3.1-8b-instant",   # ✅ NEW WORKING MODEL
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {e}"


# UI
st.set_page_config(page_title="AI Career Guidance", page_icon="🚀")
st.title("🚀 AI Career Guidance System")

with st.form("career_form"):
    name = st.text_input("Your Name")
    interests = st.text_input("Your Interests")
    skills = st.text_input("Your Skills")
    education = st.text_input("Your Education")
    goals = st.text_input("Your Career Goals")
    submit = st.form_submit_button("Get Career Advice")

if submit:
    if not all([name.strip(), interests.strip(), skills.strip(), education.strip(), goals.strip()]):
        st.error("⚠️ Fill all fields!")
    else:
        st.success("Generating your personalized career guidance...")
        advice = get_career_advice(
            clean_text(interests),
            clean_text(skills),
            clean_text(education),
            clean_text(goals)
        )
        st.markdown(advice)
