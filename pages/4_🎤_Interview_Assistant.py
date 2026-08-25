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
# Get Logged-in User
# =========================

username = st.session_state.get(
    "username",
    "User"
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

name = st.text_input(
    "Your Name"
)

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

    # =========================
    # Validate Input
    # =========================

    if not name:

        st.warning(
            "⚠️ Please enter your name before starting the interview."
        )

        st.stop()


    # =========================
    # AI Prompt
    # =========================

    prompt = f"""
You are a professional AI Interviewer.

Candidate Name: {name}
Job Role: {role}
Difficulty Level: {level}

Create a practical interview preparation guide specifically for this
job role and difficulty level.

Use exactly these sections:

1. Important Interview Questions
Generate 5 important questions.

For each question provide:
- Interview Question
- Expected Answer
- One short explanation of what the interviewer is looking for

Include questions appropriate to the selected difficulty level.

2. Interview Tips
Give 3 practical tips specifically useful for this role.

3. Common Mistakes to Avoid
Give 3 common mistakes candidates make in this type of interview
and explain briefly how to avoid them.

4. Final Preparation Tips
Give 3 practical things the candidate should do before the interview.

Make the questions role-specific rather than generic.

For technical roles, include a good balance of:
- Technical concepts
- Programming/problem-solving
- Projects
- Practical application

Keep the response focused and easy to study,
but provide enough detail for the candidate to actually prepare.

Use clear headings, numbered questions and bullet points.
Do not give unnecessary motivational content.
"""


    # =========================
    # Gemini AI
    # =========================

    with st.spinner(
        "🤖 AI is preparing your interview..."
    ):

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

        except Exception as e:

            st.error(
                "⚠️ Gemini AI is temporarily unavailable. "
                "Please try again."
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

    save_interview(
        username,
        name,
        role,
        level,
        response.text
    )


    # =========================
    # Display Result
    # =========================

    st.divider()

    st.subheader(
        "🎯 AI Interview Preparation"
    )

    st.write(
        response.text
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


    # =========================
    # PDF Title
    # =========================

    story.append(
        Paragraph(
            "AI Interview Preparation Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 20)
    )


    # =========================
    # Candidate Information
    # =========================

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


    # =========================
    # AI Preparation Heading
    # =========================

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

    with open(
        pdf_file,
        "rb"
    ) as file:

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