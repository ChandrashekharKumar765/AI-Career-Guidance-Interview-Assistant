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
You are a professional AI Career Counselor helping college students
choose a realistic career path.

Student Information:
Name: {name}
Degree: {degree}
Skills: {skills}
Career Interest: {interest}

Analyze the student's current skills and interests and provide
personalized, practical and realistic career guidance.

Use exactly these sections:

1. Best Career Option
- Recommend the most suitable career.
- Explain briefly why it matches the student's background.
- Mention 2-3 suitable entry-level job roles.

2. Expected Salary Range
- Give a realistic fresher salary range in India.
- Mention that salary depends on skills, location, company and experience.

3. Top Skills to Learn
- List the most important technical and professional skills.
- Prioritize the skills in the order they should be learned.

4. 6-Month Roadmap
- Month 1
- Month 2
- Month 3
- Month 4
- Month 5
- Month 6

Give practical learning goals and project work for each month.

5. Recommended Certifications
- Suggest relevant certifications or courses.
- Mention which ones are useful for beginners.

6. Suitable Companies
- Suggest companies where the student could eventually apply.
- Include both service-based and product-based companies where appropriate.

7. Interview Preparation Tips
- Give practical interview preparation advice.
- Mention technical, HR and project-related preparation.

Make the guidance detailed enough to be genuinely useful to a student,
but keep it focused and easy to read.

Use clear headings and bullet points.
Do not give generic motivational statements.
Base the recommendations on the student's provided degree, skills and interest.
"""

        # =========================
        # Gemini AI
        # =========================

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