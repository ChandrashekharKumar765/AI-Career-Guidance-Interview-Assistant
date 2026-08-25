import streamlit as st
from google import genai

from database_manager import create_database, get_counts



# =========================
# Load Environment
# =========================



# Create database and tables
create_database()

# Gemini Client
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="AI Career Guidance & Interview Assistant",
    page_icon="🤖",
    layout="wide"
)


# =========================
# Custom CSS
# =========================

st.markdown("""
<style>

.main-title {
    font-size: 45px;
    font-weight: bold;
    color: #4CAF50;
    text-align: center;
}

.sub-title {
    font-size: 20px;
    text-align: center;
    color: gray;
}

</style>
""", unsafe_allow_html=True)


# =========================
# Header
# =========================

st.markdown(
    "<h1 class='main-title'>🤖 AI Career Guidance & Interview Assistant</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='sub-title'>Powered by Gemini AI | Python | Streamlit</p>",
    unsafe_allow_html=True
)


st.divider()


# =========================
# Get Database Counts
# =========================

resume_count, career_count, interview_count = get_counts()


# =========================
# Dashboard Statistics
# =========================

st.subheader("📊 Project Dashboard")

col1, col2, col3 = st.columns(3)


with col1:
    st.metric(
        "📄 Resume Analyses",
        resume_count
    )


with col2:
    st.metric(
        "💼 Career Reports",
        career_count
    )


with col3:
    st.metric(
        "🎤 Interviews",
        interview_count
    )


st.divider()


# =========================
# Features
# =========================

st.subheader("🚀 Available Features")

c1, c2, c3 = st.columns(3)


with c1:

    st.info("""
    ### 📄 Resume Analyzer

    - AI Resume Review
    - Resume Score
    - Strengths & Weaknesses
    - Missing Skills
    - PDF Report
    """)


with c2:

    st.success("""
    ### 💼 Career Guidance

    - Best Career Options
    - Salary Range
    - Skills to Learn
    - 6 Month Roadmap
    - PDF Report
    """)


with c3:

    st.warning("""
    ### 🎤 Interview Assistant

    - AI Interview Questions
    - Expected Answers
    - Interview Tips
    - Common Mistakes
    - PDF Report
    """)


st.divider()


# =========================
# Welcome Section
# =========================

st.header("🚀 Welcome")

st.write("""
This AI application helps students to:

✅ Analyze Resume

✅ Get Personalized Career Guidance

✅ Prepare Interview Questions

✅ Identify Missing Skills

✅ Generate AI Suggestions

✅ Download AI Reports as PDF

✅ Store Previous Activities in Database
""")


st.divider()


# =========================
# How It Works
# =========================

st.subheader("⚙️ How It Works")

step1, step2, step3 = st.columns(3)


with step1:

    st.write("""
    ### 1️⃣ Upload / Enter Details

    Provide your resume or career information.
    """)


with step2:

    st.write("""
    ### 2️⃣ Gemini AI Analysis

    Gemini AI analyzes your information and generates personalized suggestions.
    """)


with step3:

    st.write("""
    ### 3️⃣ Save & Download

    Results are saved in SQLite database and can be downloaded as PDF/TXT.
    """)


st.divider()


# =========================
# Footer
# =========================

st.markdown("""
<center>

<h4>Developed By</h4>

<b>Chandra Shekhar</b><br>

B.Tech Computer Science & Engineering<br>

Major Project 2026

</center>
""", unsafe_allow_html=True)