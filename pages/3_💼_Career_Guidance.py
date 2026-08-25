import streamlit as st

from google import genai
from database_manager import save_career
from auth import require_login, show_logout

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="Career Guidance",
    page_icon="💼",
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

st.title("💼 AI Career Guidance")

st.write(
    "Get personalized AI-powered career guidance."
)


# =========================
# Student Details
# =========================

name = st.text_input(
    "Your Name"
)

degree = st.text_input(
    "Degree"
)

skills = st.text_area(
    "Your Skills"
)

interest = st.text_input(
    "Career Interest"
)


# =========================
# Generate Guidance
# =========================

if st.button(
    "Get Career Guidance",
    use_container_width=True
):

    # =========================
    # Validate Input
    # =========================

    if not name or not degree or not skills or not interest:

        st.warning(
            "⚠️ Please fill in all the details before generating guidance."
        )

        st.stop()


    # =========================
    # Loading Message
    # =========================

    with st.spinner(
        "🤖 AI is generating your career guidance..."
    ):

        # =========================
        # AI Prompt
        # =========================

        prompt = f"""
You are an AI Career Counselor.

Student:
Name: {name}
Degree: {degree}
Skills: {skills}
Career Interest: {interest}

Provide concise and practical career guidance in exactly these sections:

1. Best Career Option
2. Expected Salary Range
3. Top Skills to Learn
4. 6-Month Roadmap
5. Recommended Certifications
6. Suitable Companies
7. Interview Preparation Tips

Keep each section short and useful.
Use bullet points where appropriate.
Avoid unnecessary explanations.
"""


        # =========================
        # Gemini AI
        # =========================

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt
            )

        except Exception as e:

            st.error(
                "⚠️ Gemini AI is temporarily unavailable."
            )

            st.stop()


    # =========================
    # Check Response
    # =========================

    if response is None or not response.text:

        st.error(
            "⚠️ Gemini did not return a response. Please try again."
        )

        st.stop()


    # =========================
    # Save to Database
    # =========================

    save_career(
        username,
        name,
        degree,
        skills,
        interest,
        response.text
    )


    # =========================
    # Display Result
    # =========================

    st.divider()

    st.subheader(
        "💼 AI Career Guidance"
    )

    st.write(
        response.text
    )

    st.divider()

    st.success(
        "✅ Career Guidance Generated Successfully"
    )


    # =========================
    # TXT Download
    # =========================

    st.download_button(
        label="📥 Download Guidance (TXT)",
        data=response.text,
        file_name="Career_Guidance.txt",
        mime="text/plain"
    )


    # =========================
    # PDF REPORT
    # =========================

    pdf_file = "Career_Guidance.pdf"

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
            "AI Career Guidance Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 20)
    )


    # =========================
    # Student Information
    # =========================

    story.append(
        Paragraph(
            f"<b>Student Name:</b> {name}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 8)
    )


    story.append(
        Paragraph(
            f"<b>Degree:</b> {degree}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 8)
    )


    story.append(
        Paragraph(
            f"<b>Career Interest:</b> {interest}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 20)
    )


    # =========================
    # AI Guidance Heading
    # =========================

    story.append(
        Paragraph(
            "AI Career Guidance",
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
        label="📥 Download Guidance (PDF)",
        data=pdf_data,
        file_name="Career_Guidance.pdf",
        mime="application/pdf"
    )