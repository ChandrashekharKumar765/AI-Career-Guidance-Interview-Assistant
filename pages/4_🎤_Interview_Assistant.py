import streamlit as st

from google import genai
from database_manager import save_interview
from auth import require_login, show_logout

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="Interview Assistant",
    page_icon="🎤",
    layout="wide"
)


# =========================
# Login Protection
# =========================

require_login()
show_logout()


# =========================
# Gemini Configuration
# =========================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# =========================
# Page Header
# =========================

st.title("🎤 AI Interview Assistant")

st.write(
    "Generate AI-powered interview questions and preparation guidance."
)


# =========================
# User Details
# =========================

name = st.text_input("Your Name")

role = st.selectbox(
    "Job Role",
    [
        "Machine Learning Engineer",
        "Data Scientist",
        "Python Developer",
        "AI Engineer",
        "Data Analyst"
    ]
)

level = st.selectbox(
    "Difficulty",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)


# =========================
# Start Interview
# =========================

if st.button(
    "Start Interview",
    use_container_width=True
):

    prompt = f"""
You are an AI Interviewer.

Candidate Name:
{name}

Role:
{role}

Difficulty:
{level}

Generate:

1. 10 Interview Questions
2. Expected Answers
3. Interview Tips
4. Common Mistakes
5. Final Preparation Advice

Give the response in a clear and structured format.
"""


    # =========================
    # Gemini AI
    # =========================

    response = None

    try:

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

    except Exception as e:

        st.error(
            f"⚠️ Gemini AI is temporarily unavailable.\n\n"
            f"Error: {e}"
        )

        st.stop()


    # =========================
    # Check Response
    # =========================

    if response is None or not response.text:

        st.error(
            "⚠️ Gemini did not return a response. "
            "Please try again."
        )

        st.stop()


    # =========================
    # Save to Database
    # =========================

    username = st.session_state.get("username", "User")

    save_interview(
        username,
        name or "Unknown",
        role,
        level,
        response.text
)


    # =========================
    # Display Result
    # =========================

    st.divider()

    st.subheader("🎯 AI Interview Preparation")

    st.write(response.text)

    st.divider()

    st.success(
        "✅ Interview Preparation Generated Successfully"
    )


    # =========================
    # TXT Download
    # =========================

    st.download_button(
        label="📥 Download Questions (TXT)",
        data=response.text,
        file_name="Interview_Questions.txt",
        mime="text/plain"
    )


    # =========================
    # Create PDF
    # =========================

    pdf_file = "Interview_Questions.pdf"

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []


    story.append(
        Paragraph(
            "AI Interview Preparation Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 20)
    )


    story.append(
        Paragraph(
            f"<b>Candidate Name:</b> {name or 'Unknown'}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 8)
    )


    story.append(
        Paragraph(
            f"<b>Job Role:</b> {role}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 8)
    )


    story.append(
        Paragraph(
            f"<b>Difficulty:</b> {level}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 20)
    )


    story.append(
        Paragraph(
            "AI Interview Preparation",
            styles["Heading2"]
        )
    )

    story.append(
        Spacer(1, 10)
    )


    # =========================
    # Add AI Response to PDF
    # =========================

    for line in response.text.split("\n"):

        line = line.strip()

        if line:

            safe_line = (
                line
                .replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
            )

            story.append(
                Paragraph(
                    safe_line,
                    styles["Normal"]
                )
            )

            story.append(
                Spacer(1, 8)
            )


    # =========================
    # Build PDF
    # =========================

    doc.build(story)


    # =========================
    # Read PDF
    # =========================

    with open(pdf_file, "rb") as file:

        pdf_data = file.read()


    # =========================
    # PDF Download
    # =========================

    st.download_button(
        label="📥 Download Questions (PDF)",
        data=pdf_data,
        file_name="Interview_Questions.pdf",
        mime="application/pdf"
    )