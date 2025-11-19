import streamlit as st
import requests
import re

# ----------------------------
#  SETTINGS (PUT YOUR KEY HERE)
# ----------------------------
GROQ_API_KEY = "YOUR_GROQ_API_KEY"   # Replace with your real key
MODEL_NAME = "llama-3.1-70b-versatile"

API_URL = "https://api.groq.com/openai/v1/chat/completions"

# ----------------------------
# Helper Functions
# ----------------------------

def clean_input(text):
    return re.sub(r'[^\w\s]', '', text).strip() if text else ""

def get_career_advice(interests, skills, education, goals):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
You are an expert career counselor for Indian B.Tech students.

Give highly personalized, clear, practical career guidance based on:
- Interests: {interests}
- Skills: {skills}
- Education: {education}
- Career Goals: {goals}

Requirements:
1. Suggest **4 career paths** with:
   - Job role & description
   - Required skills
   - Missing skills based on user's input
   - Roadmap (3–5 steps)
   - Salary (INR)
   - Market demand in India
2. Add:
   - Resume advice
   - Projects ideas
   - Interview tips
   - Free learning resources
3. Format clearly with headings and bullet points.
"""

    data = {
        "model": MODEL_NAME,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.8
    }

    try:
        response = requests.post(API_URL, json=data, headers=headers)
        result = response.json()

        if "choices" in result:
            return result["choices"][0]["message"]["content"]
        else:
            return f"API Error: {result}"

    except Exception as e:
        return f"Error: {str(e)}"

# ----------------------------
# STREAMLIT UI
# ----------------------------

st.set_page_config(page_title="AI Career Guide", page_icon="🚀")

st.title("🚀 AI Career Guidance System")
st.subheader("Get personalized career suggestions powered by Llama-3")

with st.form("career_form"):
    user_name = st.text_input("Your Name")
    interests = st.text_input("Your Interests (AI, web dev, etc.)")
    skills = st.text_input("Your Skills (Python, teamwork)")
    education = st.text_input("Education (e.g., B.Tech CSE)")
    goals = st.text_input("Career Goals")

    submit = st.form_submit_button("Get Career Advice")

if submit:
    if not all([user_name, interests, skills, education, goals]):
        st.error("⚠ Please fill all fields")
    else:
        st.success("Career advice generated successfully ✔")

        interests = clean_input(interests)
        skills = clean_input(skills)
        education = clean_input(education)
        goals = clean_input(goals)

        with st.spinner("Generating advice..."):
            advice = get_career_advice(interests, skills, education, goals)

        st.markdown(advice)



