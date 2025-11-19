import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

# Load API Key (Streamlit Cloud loads from Secrets)
API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configure Gemini API
genai.configure(api_key=API_KEY)

# Use correct model name
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def clean_input(text):
    return re.sub(r"[^\w\s]", "", text).strip()

def get_career_advice(interests, skills, education, goals):
    prompt = f"""
    You are an AI career counselor for Indian B.Tech students. Provide detailed,
    realistic and step-by-step career guidance based on:

    Interests: {interests}
    Skills: {skills}
    Education: {education}
    Goals: {goals}

    Include:
    1. Best career paths (4 options)
    2. Required skills and certifications
    3. Salary in INR, job demand in India
    4. Step-by-step roadmap (courses, projects, internships)
    5. Free learning resources (YouTube, Coursera, etc.)
    6. Resume, LinkedIn & Interview guidance

    Format using headings, bullet points and tables.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ Error: Unable to fetch advice ({str(e)})"

# Streamlit UI
st.title("🚀 AI Career Guidance System")
st.write("Get personalized career advice based on your profile.")

with st.form("career_form"):
    name = st.text_input("Your Name")
    interests = st.text_input("Your Interests")
    skills = st.text_input("Your Skills")
    education = st.text_input("Your Education")
    goals = st.text_input("Your Career Goals")
    submit = st.form_submit_button("Get Career Advice")

if submit:
    if not all([name, interests, skills, education, goals]):
        st.error("Please fill all fields.")
    else:
        with st.spinner("⏳ Generating your career plan..."):
            advice = get_career_advice(interests, skills, education, goals)
            st.success("Career advice generated successfully!")
            st.markdown("### 📌 Your Personalized Career Guidance:")
            st.markdown(advice)

