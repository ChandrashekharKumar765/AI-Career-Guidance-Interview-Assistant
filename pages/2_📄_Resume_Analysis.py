import streamlit as st

from google import genai
from PyPDF2 import PdfReader
from database_manager import save_resume
from auth import require_login, show_logout

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


# =========================
# Page Configuration
# =========================

st.set_page_config(
    page_title="Resume Analysis",
    page_icon="📄",
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

st.title("📄 AI Resume Analysis")

st.write(
    "Upload your Resume (PDF) and get detailed AI-powered analysis."
)


# =========================
# Upload PDF
# =========================

uploaded_file = st.file_uploader(
    "Choose Resume (PDF)",
    type=["pdf"]
)


if uploaded_file is not None:

    st.success("✅ Resume Uploaded Successfully")

    st.info(
        f"📄 File Name: {uploaded_file.name}"
    )

    st.info(
        f"📦 File Size: {round(uploaded_file.size / 1024, 2)} KB"
    )

    if st.button(
        "🤖 Analyze Resume",
        use_container_width=True
    ):

        # =========================
        # Read PDF
        # =========================

        reader = PdfReader(uploaded_file)

        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text() or ""

        if not resume_text.strip():

            st.error(
                "⚠️ Could not extract text from this PDF."
            )

            st.stop()


        # =========================
        # AI Prompt
        # =========================

        prompt = f"""
You are an expert Resume Analyzer and Career Consultant.

Analyze the following resume carefully.

Provide a detailed, practical and professional report.

Include these sections:

1. Resume Score out of 100
   Explain why the resume received this score.

2. Strengths
   Explain the strongest parts of the resume.

3. Weaknesses
   Explain what needs improvement.

4. Missing or Recommended Skills
   Include technical and soft skills.

5. Career Suggestions
   Suggest suitable career roles and explain why they fit.

6. Resume Improvement Suggestions
   Give specific suggestions for projects, skills,
   formatting, achievements and overall presentation.

7. Interview Preparation
   Mention important technical and HR topics to prepare.

8. Final Action Plan
   Give practical next steps for improving the candidate's profile.

Use clear headings and bullet points.
Give useful explanations rather than one-line answers.

Resume:

{resume_text}
"""


        # =========================
        # Streaming Response
        # =========================

        st.divider()
        st.subheader("🤖 AI Resume Analysis")

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

        save_resume(
            username,
            uploaded_file.name,
            full_response
        )


        st.divider()

        st.success(
            "✅ Resume Analysis Completed Successfully"
        )


        # =========================
        # TXT Download
        # =========================

        st.download_button(
            label="📥 Download Analysis (TXT)",
            data=full_response,
            file_name="AI_Resume_Analysis.txt",
            mime="text/plain"
        )


        # =========================
        # PDF Report
        # =========================

        pdf_file = "AI_Resume_Analysis.pdf"

        doc = SimpleDocTemplate(
            pdf_file,
            pagesize=A4
        )

        styles = getSampleStyleSheet()

        story = []

        story.append(
            Paragraph(
                "AI Resume Analysis Report",
                styles["Title"]
            )
        )

        story.append(
            Spacer(1, 20)
        )

        safe_file_name = (
            uploaded_file.name
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

        story.append(
            Paragraph(
                f"<b>Resume:</b> {safe_file_name}",
                styles["Normal"]
            )
        )

        story.append(
            Spacer(1, 20)
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
            label="📥 Download Analysis (PDF)",
            data=pdf_data,
            file_name="AI_Resume_Analysis.pdf",
            mime="application/pdf"
        )