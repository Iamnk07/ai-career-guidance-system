import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import re

load_dotenv()

# Use API key
API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=API_KEY)

# FIXED MODEL (ONLY THIS WORKS)
model = genai.GenerativeModel("gemini-1.5-flash")

def clean_input(text):
    return re.sub(r'[^\w\s]', '', text).strip() if text else ""

def get_career_advice(interests, skills, education, goals):
    prompt = f"""
You are an expert career counselor mentoring Indian B.Tech students.

Interests: {interests}
Skills: {skills}
Education: {education}
Career Goals: {goals}

Give a full detailed career roadmap with:
- Job roles
- Required skills
- Skill gap analysis
- Salary (INR)
- Steps to achieve goals
- Certifications
- Projects
- Internship ideas
- Resume tips
"""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: Unable to fetch advice ({str(e)}). Check your API key or model name."
