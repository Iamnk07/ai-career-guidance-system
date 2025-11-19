import streamlit as st
from groq import Groq

# Load Groq API key
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)

def get_career_advice(interests, skills, education, goals):
    prompt = f"""
You are an AI career counselor for Indian students.

Interests: {interests}
Skills: {skills}
Education: {education}
Career Goals: {goals}

Provide detailed guidance including:
- 4 suitable career options
- Required skills
- Missing skills
- Roadmap (step-by-step)
- Salary in INR
- Free resources
- Resume & interview tips
Format neatly with bullet points.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-instruct",  # ✅ Correct working model
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error: {e}"


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
        st.error("⚠️ Please fill all fields!")
    else:
        st.success("Generating your personalized career guidance...")
        advice = get_career_advice(interests, skills, education, goals)
        st.markdown(advice)
