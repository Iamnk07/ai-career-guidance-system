import streamlit as st
from groq import Groq

# -----------------------------------------------------
# CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="AI Career Guidance",
    page_icon="🚀",
    layout="centered"
)

# -----------------------------------------------------
# LOAD CLIENT (CACHED FOR SPEED)
# -----------------------------------------------------
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()


# -----------------------------------------------------
# CLEAN INPUT
# -----------------------------------------------------
def clean_text(text):
    return text.strip() if text else ""


# -----------------------------------------------------
# CALL GROQ API
# -----------------------------------------------------
def get_career_advice(interests, skills, education, goals):

    prompt = f"""
You are an expert AI career counselor for Indian students.

Interests: {interests}
Skills: {skills}
Education: {education}
Career Goals: {goals}

Provide a structured guidance including:

1. Best 4 Career Options  
2. Required Skills  
3. Missing Skills & How to Improve  
4. Step-by-step Roadmap  
5. Salary Range (INR)  
6. Best Online Resources  
7. Resume Tips  
8. Interview Prep Tips

Format the output cleanly with headings and bullet points.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # ✅ Correct MODEL
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ **API Error:** {e}"


# -----------------------------------------------------
# USER INTERFACE (ENHANCED UI)
# -----------------------------------------------------

st.markdown("""
<div style="text-align:center; padding: 20px 0;">
    <h1 style="color:#4CAF50; margin-bottom:5px;">🚀 AI Career Guidance System</h1>
    <p style="color:#666; font-size:18px;">
        Get personalized, AI-powered career guidance based on your interests and skills.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

with st.container():
    st.markdown("""
    <div style="
        background: #f7f7f7; 
        padding: 25px; 
        border-radius: 12px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    ">
    """, unsafe_allow_html=True)

    st.subheader("📝 Enter Your Details")

    name = st.text_input("Your Name")
    interests = st.text_input("Your Interests (e.g. Coding, Finance, Design)")
    skills = st.text_input("Your Skills (e.g. Python, Excel, Communication)")
    education = st.text_input("Your Education (e.g. B.Tech CSE, B.Com)")
    goals = st.text_input("Your Career Goals (e.g. Data Scientist, Software Developer)")

    submit = st.button("✨ Get Career Guidance", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# -----------------------------------------------------
# SHOW RESULT
# -----------------------------------------------------
if submit:

    if not all([name.strip(), interests.strip(), skills.strip(), education.strip(), goals.strip()]):
        st.error("⚠️ Please fill all fields!")
    else:

        with st.spinner("⏳ Analyzing your profile..."):
            advice = get_career_advice(
                clean_text(interests),
                clean_text(skills),
                clean_text(education),
                clean_text(goals)
            )

        st.markdown("---")
        st.subheader(f"📄 Career Guidance for **{name}**")

        st.markdown(
            f"""
            <div style="
                background:#ffffff; 
                border-left:6px solid #4CAF50; 
                padding:20px; 
                border-radius:10px;
                box-shadow:0 4px 10px rgba(0,0,0,0.08);
            ">
                {advice}
            </div>
            """,
            unsafe_allow_html=True
        )
