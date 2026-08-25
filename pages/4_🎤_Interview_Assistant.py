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

username = st.session_state.get("username", "User")


# =========================
# Page Header
# =========================

st.title("🎤 AI Interview Assistant")

st.write(
    "Generate detailed AI-powered interview questions and preparation guidance."
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

    if not name:

        st.warning(
            "⚠️ Please enter your name."
        )

        st.stop()


    # =========================
    # AI Prompt
    # =========================

    prompt = f"""
You are an expert technical interviewer.

Candidate Name: {name}
Job Role: {role}
Difficulty: {level}

Create a detailed interview preparation report.

Include:

1. 10 important interview questions
   - Give the expected answer after each question.
   - Include a mixture of conceptual, technical and practical questions.

2. Interview Tips
   - Give at least 5 useful tips.

3. Common Mistakes
   - Give at least 5 mistakes candidates should avoid.

4. Final Preparation Advice
   - Give a practical preparation strategy.

Make the questions relevant to the selected job role and difficulty.

Use clear headings, numbering and bullet points.
Give useful explanations rather than extremely short answers.
"""


    # =========================
    # Streaming Response
    # =========================

    st.divider()
    st.subheader("🎯 AI Interview Preparation")

    response_placeholder = st.empty()

    full_response = ""

    try:

        for chunk in client.models.generate_content_stream(
            model="gemini-3.5-flash-lite",
            contents=prompt
        ):

            if chunk.text:

                full_response += chunk.text

                response_placeholder.markdown(
                    full_response
                )

    except Exception as e:

        st.error(
            f"⚠️ Gemini AI Error: {e}"
        )

        st.stop()


    # =========================
    # Check Response
    # =========================

    if not full_response.strip():

        st.error(
            "⚠️ Gemini did not return a response."
        )

        st.stop()


    # =========================
    # Save to Database
    # =========================

    save_interview(
        username,
        name,
        role,
        level,
        full_response
    )


    st.divider()

    st.success(
        "✅ Interview Preparation Generated Successfully"
    )


    # =========================
    # TXT Download
    # =========================

    st.download_button(
        label="📥 Download Questions (TXT)",
        data=full_response,
        file_name="Interview_Questions.txt",
        mime="text/plain"
    )


    # =========================
    # PDF Report
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
            f"<b>Candidate Name:</b> {name}",
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

    for line in full_response.split("\n"):

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

    doc.build(story)

    with open(
        pdf_file,
        "rb"
    ) as file:

        pdf_data = file.read()

    st.download_button(
        label="📥 Download Questions (PDF)",
        data=pdf_data,
        file_name="Interview_Questions.pdf",
        mime="application/pdf"
    )