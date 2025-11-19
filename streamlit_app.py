import streamlit as st
import google.generativeai as genai
import os
import re

# Load API key from Streamlit Secrets
API_KEY = st.secrets["GOOGLE_API_KEY"]

# Configure Google API
genai.configure(api_key=API_KEY)

# Use correct FREE model
MODEL_NAME = "gemini-1.5-flash"


def clean_text(text):
    return re.sub(r"[^\w\s]", "", text).strip()


def get_career_advice(name, skills, education, goals):
    prompt = f"""
    You are an expert career counselor for Indian students.

    Name: {name}
    Skills: {skills}
    Education: {education}
    Goals: {goals}

    Provide:
    - 4 career paths with job description
    - Required skills
    - Skill gaps
    - Step-by-step roadmap
    - Salary (INR)
    - Market insights
    - Challenges and solutions
    - Motivational advice
    """

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"


# Streamlit UI
st.title("🚀 AI Career Guidance System")

name = st.text_input("Your Name")
skills = st.text_input("Your Skills")
education = st.text_input("Your Education")
goals = st.text_input("Your Career Goal")

if st.button("Get Career Advice"):
    if not (name and skills and education and goals):
        st.error("Please fill all fields.")
    else:
        with st.spinner("Generating career advice..."):
            output = get_career_advice(
                clean_text(name), clean_text(skills),
                clean_text(education), clean_text(goals)
            )
        st.success("Career advice generated!")
        st.write(output)

