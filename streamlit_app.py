import streamlit as st
import google.generativeai as genai
import os
import re

# ---------------------------
# 1️⃣  Configure API Key
# ---------------------------
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# ---------------------------
# 2️⃣  Use correct model name
# ---------------------------
model = genai.GenerativeModel("gemini-1.5-flash-latest")

def clean_input(text):
    return re.sub(r"[^\w\s]", "", text).strip() if text else ""

def get_career_advice(interests, skills, education, goals):
    prompt = f"""
You are an expert career counselor in India. Provide highly personalized, detailed career guidance.

Interests: {interests}
Skills: {skills}
Education: {education}
Career Goals: {goals}

Give output with clear headings and bullet points.
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: Unable to fetch advice ({str(e)}). Check your API key or model name."

# ---------------------------
# Streamlit UI
# ---------------------------
st.title("🚀 AI Career Guidance System")

name = st.text_input("Your Name")
interests = st.text_input("Your Interests")
skills = st.text_input("Your Skills")
education = st.text_input("Your Education")
goals = st.text_input("Your Career Goals")

if st.button("Get Career Advice"):
    if not all([name, interests, skills, education, goals]):
        st.error("Fill all fields!")
    else:
        st.success("Career advice generated successfully!")
        advice = get_career_advice(interests, skills, education, goals)
        st.markdown(advice)

