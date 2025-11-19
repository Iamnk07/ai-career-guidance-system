import streamlit as st
from groq import Groq

# Load API key from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)

def get_career_advice(interests, skills, education, goals):
    prompt = f"""
You are an expert career counselor for Indian students.

Interests: {interests}
Skills: {skills}
Education: {education}
Career Goals: {goals}

Give detailed guidance including:
- Best 4 career paths
- Required skills
- Missing skill gaps
- Step-by-step roadmap
- Salary range in INR
- Free learning resources
- Interview tips
Use clear headings and bullet points.
"""

    try:
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ Error: {str(e)}"


# Streamlit UI
st.set_page_config(page_title="AI Career Guidance", page_icon="🚀")

st.title("🚀 AI Career Guidance System")

name = st.text_input("Your Name")
interests = st.text_input("Your Interests")
skills = st.text_input("Your Skills")
education = st.text_input("Your Education")
goals = st.text_input("Your Career Goals")

if st.button("Get Career Advice"):
    if not all([name, interests, skills, education, goals]):
        st.error("⚠ Please fill all the fields!")
    else:
        st.success("✨ Generating personalized career advice...")
        advice = get_career_advice(interests, skills, education, goals)
        st.markdown(advice)


