import streamlit as st
from groq import Groq
import re

# Load API Key from Streamlit Secrets
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Initialize Groq Client
client = Groq(api_key=GROQ_API_KEY)

def clean_text(text):
    return re.sub(r"[^\w\s]", "", text).strip()

def get_career_advice(name, interests, skills, education, goals):
    prompt = f"""
You are an expert AI Career Counselor for Indian students and professionals.

User Profile:
Name: {name}
Interests: {interests}
Skills: {skills}
Education: {education}
Career Goals: {goals}

Give detailed career guidance including:
1️⃣ 4 Best Suitable Career Paths
2️⃣ Required Skills & Missing Skill Gap
3️⃣ Step-by-step Roadmap (Courses, Internships, Certifications, Projects)
4️⃣ Average Salary (INR) & Job Demand in India
5️⃣ Interview Preparation Tips (HR + Technical)
6️⃣ Free Learning Resources (YouTube, Coursera, Udemy)
7️⃣ Motivational guidance to stay focused

Format your answer using:
- Headings
- Bullet points
- Numbered steps
- Short paragraphs
- Bold for important text

Make it personalized and motivational.
"""
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # Free & Fast Model
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


# -------------------- STREAMLIT APP UI --------------------

st.set_page_config(page_title="AI Career Guidance", page_icon="🚀", layout="centered")

st.title("🚀 AI Career Guidance System")
st.write("Get personalized career advice based on your skills, education & goals")

with st.form("career_form"):
    name = st.text_input("👤 Your Name")
    interests = st.text_input("🎯 Interests (e.g., AI, Web Dev, Finance)")
    skills = st.text_input("🛠 Skills (e.g., Python, Java, Teamwork)")
    education = st.text_input("🎓 Education (e.g., B.Tech CSE, Diploma)")
    goals = st.text_input("🚀 Career Goals (e.g., Data Scientist, Software Engineer)")

    submit = st.form_submit_button("🔍 Get Career Advice")

if submit:
    if not all([name, interests, skills, education, goals]):
        st.error("⚠️ Please fill all fields before submitting!")
    else:
        with st.spinner("✨ Generating personalized career guidance..."):
            advice = get_career_advice(
                clean_text(name),
                clean_text(interests),
                clean_text(skills),
                clean_text(education),
                clean_text(goals),
            )
        st.success("🎯 Career Advice Generated Successfully!")
        st.markdown(advice)

st.markdown("---")
st.write("Made with ❤️ using Groq LLaMA3 and Streamlit")

