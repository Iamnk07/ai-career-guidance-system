import streamlit as st
from groq import Groq

# -----------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------
st.set_page_config(
    page_title="AI Career Guidance",
    page_icon="🚀",
    layout="centered"
)

# -----------------------------------------------------
# LOAD CLIENT (CACHED)
# -----------------------------------------------------
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

# -----------------------------------------------------
# CLEAN TEXT
# -----------------------------------------------------
def clean_text(text):
    return text.strip() if text else ""

# -----------------------------------------------------
# CALL GROQ API (USING THE ONLY MODEL YOU HAVE ACCESS TO)
# -----------------------------------------------------
def get_career_advice(interests, skills, education, goals):

    prompt = f"""
You are an expert AI career counselor for Indian students.

Interests: {interests}
Skills: {skills}
Education: {education}
Career Goals: {goals}

Provide a structured, detailed career guidance including:

1. Best 4 Career Options  
2. Required Skills  
3. Missing Skills & How to Improve  
4. Step-by-step Career Roadmap  
5. Salary Range in INR  
6. Best Learning Resources  
7. Resume Tips  
8. Interview Preparation Tips

Format output cleanly using headings and bullet points.
"""

    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",  # ✅ YOUR AVAILABLE MODEL
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"❌ **API Error:** {e}"


# -----------------------------------------------------
# USER INTERFACE
# -----------------------------------------------------

st.markdown("""
<div style="text-align:center; padding: 20px 0;">
    <h1 style="color:#4CAF50; margin-bottom:5px;">🚀 AI Career Guidance System</h1>
    <p style="color:#bbb; font-size:17px;">
        Enter your details and receive personalized, AI-generated career guidance.
    </p>
</div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown("""
    <div style="
        background: #1e1e1e; 
        padding: 25px; 
        border-radius: 12px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
    ">
    """, unsafe_allow_html=True)

    st.subheader("📝 Enter Your Details", divider="rainbow")

    name = st.text_input("Your Name")
    interests = st.text_input("Your Interests (e.g. Coding, Finance, Design)")
    skills = st.text_input("Your Skills (e.g. Python, Excel, Communication)")
    education = st.text_input("Your Education (e.g. B.Tech CSE, B.Com)")
    goals = st.text_input("Your Career Goals (e.g. Software Developer, DevOps Engineer)")

    submit = st.button("✨ Get Career Guidance", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)

# -----------------------------------------------------
# RESULT SECTION
# -----------------------------------------------------
if submit:
    if not all([name.strip(), interests.strip(), skills.strip(), education.strip(), goals.strip()]):
        st.error("⚠️ Please fill all fields!")
    else:
        with st.spinner("⏳ Analyzing your profile and generating guidance..."):
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
                background:#ffffff10; 
                border-left:6px solid #4CAF50; 
                padding:20px; 
                border-radius:10px;
                box-shadow:0 4px 10px rgba(0,0,0,0.4);
                color:#eee;
            ">
                {advice}
            </div>
            """,
            unsafe_allow_html=True
        )

