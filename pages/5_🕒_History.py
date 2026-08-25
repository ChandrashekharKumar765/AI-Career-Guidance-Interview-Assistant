import streamlit as st

from database_manager import (
    get_resume_history,
    get_career_history,
    get_interview_history
)

from auth import require_login, show_logout


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="History",
    page_icon="🕒",
    layout="wide"
)


# =========================
# Login Protection
# =========================

require_login()
show_logout()

username = st.session_state.get("username", "User")


# =========================
# Header
# =========================

st.title("🕒 Activity History")

st.write(
    f"View your previous AI analysis and guidance, {username}."
)

st.divider()


# =========================
# Resume History
# =========================

st.subheader("📄 Resume Analysis History")

resume_history = get_resume_history(username)

if resume_history:

    for file_name, analysis, created_at in resume_history:

        with st.expander(
            f"📄 {file_name} — {created_at}"
        ):

            st.write(analysis)

else:

    st.info(
        "No Resume Analysis history available."
    )


st.divider()


# =========================
# Career History
# =========================

st.subheader("💼 Career Guidance History")

career_history = get_career_history(username)

if career_history:

    for name, degree, skills, interest, guidance, created_at in career_history:

        with st.expander(
            f"💼 {name} — {interest} — {created_at}"
        ):

            st.write("**Degree:**", degree)

            st.write("**Skills:**", skills)

            st.write(
                "**Career Interest:**",
                interest
            )

            st.divider()

            st.write(guidance)

else:

    st.info(
        "No Career Guidance history available."
    )


st.divider()


# =========================
# Interview History
# =========================

st.subheader("🎤 Interview History")

interview_history = get_interview_history(username)

if interview_history:

    for name, role, level, questions, created_at in interview_history:

        with st.expander(
            f"🎤 {name} — {role} — {level} — {created_at}"
        ):

            st.write(questions)

else:

    st.info(
        "No Interview history available."
    )


st.divider()


# =========================
# Security Message
# =========================

st.success(
    "🔐 Your activity history is private and visible only to your account."
)