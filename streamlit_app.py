import streamlit as st
from groq import Groq

# Load API key from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)

# Function to safely clean user input
def clean_text(text):
    if not text:
        return ""
    return text.strip()

def get_career_advice(interests, skills, education, goals):

    # Ensure no empty fields
    if not all([interests, skills, education, goals]):
        return "⚠️ All fields must be filled before generating advice."

    prompt = f"""
You are an AI career counselor for Indian students.

Interests: {interests}
Skills: {skills}
Education: {education}
Career Goals: {goals}

Provide:

- 4 Career options
- Required skills
- Skill gaps
- Step-by-step roadmap
- Salary (INR)
- Resources for learning
- Resume tips
- Interview preparation
"""

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {e}"



# ---------------------- UI ----------------------------

st.set_page_config(page_title="AI Career Guidance", page_icon="🚀")
st.title("🚀 AI Career Guidance System")

st.write("Enter your details to get AI powered career guidance")

with st.form("career_form"):
    name = st.text_input("Your Name")
    interests = st.text_input("Your Interests")
    skills = st.text_input("Your Skills")
    education = st.text_input("Your Education")
    goals = st.text_input("Your Career Goals")

    submit = st.form_submit_button("Get Career Advice")

if submit:
    # Validation BEFORE sending to Groq
    if not all([name.strip(), interests.strip(), skills.strip(), education.strip(), goals.strip()]):
        st.error("⚠️ Please fill all fields before submitting.")
    else:
        st.success("Generating your personalized career guidance...")
        advice = get_career_advice(
            clean_text(interests),
            clean_text(skills),
            clean_text(education),
            clean_text(goals)
        )
        st.markdown(advice)
