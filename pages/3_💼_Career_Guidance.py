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

username = st.session_state.get("username", "User")


# =========================
# Page Header
# =========================

st.title("💼 AI Career Guidance")

st.write(
    "Get personalized and detailed AI-powered career guidance."
)


# =========================
# Student Details
# =========================

name = st.text_input("Your Name")

degree = st.text_input("Degree")

skills = st.text_area("Your Skills")

interest = st.text_input("Career Interest")


# =========================
# Generate Guidance
# =========================

if st.button(
    "Get Career Guidance",
    use_container_width=True
):

    if not name or not degree or not skills or not interest:

        st.warning(
            "⚠️ Please fill in all the details."
        )

        st.stop()


    # =========================
    # AI Prompt
    # =========================

    prompt = f"""
You are an expert AI Career Counselor.

Student Information:

Name: {name}
Degree: {degree}
Skills: {skills}
Career Interest: {interest}

Create a detailed and practical personalized career report.

Include:

1. Best Career Options
   Explain the most suitable roles and why they fit the student.

2. Expected Salary Range
   Give realistic entry-level and experienced salary ranges.

3. Skills to Learn
   Explain the important technical and soft skills.

4. 6-Month Roadmap
   Divide the roadmap month-by-month with clear learning goals,
   projects and practice.

5. Recommended Certifications
   Suggest useful certifications and explain their relevance.

6. Suitable Companies
   Suggest companies that hire for the recommended roles.

7. Project Suggestions
   Suggest practical projects that can strengthen the student's resume.

8. Interview Preparation
   Explain what the student should prepare for interviews.

9. Final Career Advice
   Give clear actionable next steps.

Use headings, bullet points and useful explanations.
Make the report detailed enough to be genuinely useful.
"""


    # =========================
    # Streaming Response
    # =========================

    st.divider()
    st.subheader("💼 AI Career Guidance")

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

    save_career(
        username,
        name,
        degree,
        skills,
        interest,
        full_response
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
        data=full_response,
        file_name="Career_Guidance.txt",
        mime="text/plain"
    )


    # =========================
    # PDF Report
    # =========================

    pdf_file = "Career_Guidance.pdf"

    doc = SimpleDocTemplate(
        pdf_file,
        pagesize=A4
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "AI Career Guidance Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 20)
    )

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

    story.append(
        Paragraph(
            "AI Career Guidance",
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
        label="📥 Download Guidance (PDF)",
        data=pdf_data,
        file_name="Career_Guidance.pdf",
        mime="application/pdf"
    )