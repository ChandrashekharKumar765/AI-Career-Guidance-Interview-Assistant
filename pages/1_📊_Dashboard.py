import streamlit as st

from database_manager import get_counts
from auth import require_login, show_logout


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="AI Career Guidance Dashboard",
    page_icon="🤖",
    layout="wide"
)


# =========================
# Login Protection
# =========================

require_login()
show_logout()


# =========================
# Get Logged-in User
# =========================

username = st.session_state.get("username", "User")


# =========================
# Get Real Data
# =========================

resume_count, career_count, interview_count = get_counts(username)


# =========================
# Custom Styling
# =========================

st.markdown("""
<style>

.main-title {
    font-size: 42px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #888888;
    margin-bottom: 30px;
}

.stat-card {
    padding: 22px;
    border-radius: 15px;
    text-align: center;
    border: 1px solid rgba(128,128,128,0.25);
    margin-bottom: 10px;
}

.stat-number {
    font-size: 32px;
    font-weight: bold;
}

.stat-title {
    font-size: 16px;
    margin-top: 5px;
}

.feature-card {
    padding: 22px;
    border-radius: 15px;
    min-height: 210px;
    border: 1px solid rgba(128,128,128,0.25);
}

.footer {
    text-align: center;
    color: #888888;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# Header
# =========================

st.markdown(
    "<div class='main-title'>🤖 AI Career Guidance & Interview Assistant</div>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='subtitle'>Your AI-powered platform for career planning, resume analysis and interview preparation</div>",
    unsafe_allow_html=True
)


# =========================
# Welcome Message
# =========================

st.success(
    f"👋 Welcome, **{username}**! Choose a module below to get started."
)


st.divider()


# =========================
# Statistics
# =========================

st.subheader("📊 Activity Overview")

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">📄 {resume_count}</div>
            <div class="stat-title">Resume Analyses</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">💼 {career_count}</div>
            <div class="stat-title">Career Reports</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-number">🎤 {interview_count}</div>
            <div class="stat-title">Interview Sessions</div>
        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# =========================
# Main Features
# =========================

st.subheader("🚀 AI Career Platform")


c1, c2, c3 = st.columns(3)


with c1:

    st.markdown(
        """
        <div class="feature-card">

        <h3>📄 Resume Analyzer</h3>

        <p>Upload your resume and get AI-powered analysis.</p>

        <ul>
        <li>Resume Score</li>
        <li>Strengths & Weaknesses</li>
        <li>Missing Skills</li>
        <li>Career Suggestions</li>
        <li>TXT & PDF Reports</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        """
        <div class="feature-card">

        <h3>💼 Career Guidance</h3>

        <p>Get personalized career recommendations using AI.</p>

        <ul>
        <li>Best Career Options</li>
        <li>Expected Salary</li>
        <li>Skills to Learn</li>
        <li>6-Month Roadmap</li>
        <li>Certifications & Companies</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        """
        <div class="feature-card">

        <h3>🎤 Interview Assistant</h3>

        <p>Prepare for technical interviews with Gemini AI.</p>

        <ul>
        <li>AI Interview Questions</li>
        <li>Expected Answers</li>
        <li>Interview Tips</li>
        <li>Common Mistakes</li>
        <li>TXT & PDF Reports</li>
        </ul>

        </div>
        """,
        unsafe_allow_html=True
    )


st.divider()


# =========================
# How It Works
# =========================

st.subheader("⚡ How It Works")

step1, step2, step3, step4 = st.columns(4)


with step1:

    st.info(
        "**1️⃣ Login**\n\nSecurely access your AI platform."
    )


with step2:

    st.info(
        "**2️⃣ Choose Module**\n\nResume, Career or Interview."
    )


with step3:

    st.info(
        "**3️⃣ Generate AI Result**\n\nGemini analyzes your information."
    )


with step4:

    st.info(
        "**4️⃣ Save & Download**\n\nResults are stored and available as reports."
    )


st.divider()


# =========================
# Footer
# =========================

st.markdown(
    """
    <div class="footer">
        <b>AI Career Guidance & Interview Assistant</b><br>
        Major Project 2026 | Developed by Chandra Shekhar<br>
        B.Tech Computer Science & Engineering
    </div>
    """,
    unsafe_allow_html=True
)