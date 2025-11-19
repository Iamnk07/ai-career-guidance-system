import streamlit as st
from groq import Groq

# ---------- CONFIG ----------
st.set_page_config(
    page_title="AI Career Guidance",
    page_icon="🚀",
    layout="centered",
)

# ---------- LOAD CLIENT ----------
@st.cache_resource
def get_client():
    return Groq(api_key=st.secrets["GROQ_API_KEY"])

client = get_client()

# ---------- CLEAN INPUT ----------
def clean(text):
    return text.strip() if text else ""


# ---------- CALL GROQ ----------
def get_advice(interests, skills, education, goals):

    prompt = f"""
You are an AI career counselor for Indian students.

Interests: {interests}
Skills: {skills}
Education: {education}
Career Goals: {goals}

Provide a detailed, structured career guidance including:

1. Best 4 Career Options  
2. Required Skills  
3. Missing Skills & How to Improve  
4. Step-by-step Career Roadmap  
5. Salary Range (INR)  
6. Best Online Resources  
7. Resume Tips  
8. Interview Tips

Make the output clean, readable, and well formatted.
"""

    try:
        response = client.chat.completions.create(
            model="llama3-groq-8b-8192-tool-use-preview",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content
    
    except Exception as e:
        return f"❌ **Error:** {e}"


# -------------------------------------------------
# ------------------ USER INTERFACE ---------------
# -------------------------------------------------

# HERO SECTION
st.markdown("""
<div style="text-align:center; padding: 20px 0;">
    <h1 style="color:#4CAF50; margin-bottom:5px;">🚀 AI Career Guidance System</h1>
    <p style="color:#666; font-size:18px;">
        Get personalized, AI-powered career guidance based on your interests and skills.
    </p>
</div>
""", unsafe_allow_html=True)

st.write("")

# FORM CARD UI
with st.container():
    st.markdown("""
    <div style="
        background: #f7f7f7; 
        padding: 25px; 
        border-radius: 12px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    ">
    """, unsafe_allow_html=True)

    st.subheader("📝 Fill Your Details")

    name = st.text_input("Your Name")
    interests = st.text_input("Your Interests (e.g. Coding, Finance, Design)")
    skills = st.text_input("Your Skills (e.g. Python, Excel, Communication)")
    education = st.text_input("Your Education (e.g. B.Tech CSE, B.Com)")
    goals = st.text_input("Your Career Goals (e.g. Data Scientist, Software Engineer)")

    btn = st.button("✨ Get Career Guidance", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)


# ------------------ RESPONSE ------------------
if btn:
    if not all([name.strip(), interests.strip(), skills.strip(), education.strip(), goals.strip()]):
        st.error("⚠️ Please fill all fields!")
    else:
        with st.spinner("⏳ Analyzing your profile and generating expert guidance..."):
            advice = get_advice(
                clean(interests), clean(skills), clean(education), clean(goals)
            )

        st.markdown("---")
        st.subheader(f"📄 Career Guidance for **{name}**")

        st.markdown(
            f"""
            <div style="
                background:#ffffff; 
                border-left:6px solid #4CAF50; 
                padding:18px; 
                border-radius:8px;
                box-shadow:0 4px 10px rgba(0,0,0,0.08);
            ">
                {advice}
            </div>
            """,
            unsafe_allow_html=True
        )

