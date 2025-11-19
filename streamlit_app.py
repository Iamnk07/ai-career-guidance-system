import streamlit as st
import google.generativeai as genai
import os
import re

# Load API key from secrets
API_KEY = st.secrets["GOOGLE_API_KEY"]

genai.configure(api_key=API_KEY)

# WORKING model for your account + old SDK
model = genai.GenerativeModel("gemini-pro")

def clean_input(text):
    return re.sub(r"[^\w\s]", "", text).strip()

def get_career_advice(interests, skills, education, goals):
    prompt = f"""
    You are a career counselor in India.
    Interests: {interests}
    Skills: {skills}
    Education: {education}
    Goals: {goals}
    Give detailed career paths, skill gaps, salary, steps.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

st.title("AI Career Guidance System")

name = st.text_input("Your Name")
interests = st.text_input("Your Interests")
skills = st.text_input("Your Skills")
education = st.text_input("Your Education")
goals = st.text_input("Your Career Goals")

if st.button("Get Advice"):
    if not all([name, interests, skills, education, goals]):
        st.error("Fill all fields.")
    else:
        advice = get_career_advice(interests, skills, education, goals)
        st.write(advice)

