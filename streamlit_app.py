import streamlit as st
from groq import Groq

# ✅ Cache the Groq client so it loads only once
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

def clean_text(text):
    if not text:
        return ""
    return text.strip()

def get_career_advice(interests, skills, education, goals):

    if not all([interests, skills, education, goals]):
        return "⚠️ Please fill all fields."

    prompt = f"""
You are an AI career counselor for Indian students.

Interests: {interests}
Skills: {skills}
Education: {education}
Career Goals: {goals}

Provide:
- 4 career options
- required skills
- missing skills
- roadmap steps
- salary in INR
- resources
- resume tips
- interview tips
"""

    try:
        response = client.chat.completions.create(
            model="llama3-groq-8b-8192-tool-use-preview",
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
        advice = get_career_advice(
            clean_text(interests),
            clean_text(skills),
            clean_text(education),
            clean_text(goals)
        )
        st.markdown(advice)

