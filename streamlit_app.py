import streamlit as st
import google.generativeai as genai
import os
import re

API_KEY = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=API_KEY)

# ✅ ONLY WORKING MODEL FOR YOUR ACCOUNT
model = genai.GenerativeModel("gemini-pro")

def clean_input(text):
    return re.sub(r"[^\w\s]", "", text).strip()

def get_career_advice(interests, skills, education, goals):
    prompt = f"""
You are an Indian career counselor...
Interests: {interests}
Skills: {skills}
Education: {education}
Goals: {goals}
Provide step-by-step detailed guidance.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

st.title("AI Career Guidance System")

name = st.text_input("Name")
interests = st.text_input("Interests")
skills = st.text_input("Skills")
education = st.text_input("Education")
goals = st.text_input("Career Goals")

if st.button("Get Career Advice"):
    if not all([name, interests, skills, education, goals]):
        st.error("Fill all fields.")
    else:
        advice = get_career_advice(interests, skills, education, goals)
        st.markdown(advice)
