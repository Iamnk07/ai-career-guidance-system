import streamlit as st
from groq import Groq

# Load API key from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

client = Groq(api_key=GROQ_API_KEY)

def get_career_advice(interests, skills, education, goals):
    prompt = f"""
You are an expert career counselor for Indian students.

Interests: {interests}
Skills: {skills}
Education: {education}
Career Goals: {goals}

Give:
- 4 career options
- required skills
- missing skills
- roadmap steps
- salary in INR
- online resources
- interview tips
Format with headings and bullet points.
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


st.title("🚀 AI Career Guidance System")

name = st.text_input("Your Name")
interests = st.text_input("Your Interests")
skills = st.text_input("Your Skills")
education = st.text_input("Your Education")
goals = st.text_input("Your Career Goals")

if st.button("Get Career Advice"):
    if not all([name, interests, skills, education, goals]):
        st.error("Please fill all fields")
    else:
        st.success("Generating your personalized career advice...")
        advice = get_career_advice(interests, skills, education, goals)
        st.markdown(advice)




