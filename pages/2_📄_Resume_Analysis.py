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
# Load API Key
# =========================

client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)


# =========================
# Page Header
# =========================

st.title("📄 AI Resume Analysis")

st.write(
    "Upload your Resume (PDF) and get AI powered analysis."
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
        f"📄 File Name : {uploaded_file.name}"
    )

    st.info(
        f"📦 File Size : {round(uploaded_file.size / 1024, 2)} KB"
    )


    # =========================
    # Analyze Resume
    # =========================

    if st.button(
        "🤖 Analyze Resume",
        use_container_width=True
    ):

        # Read PDF
        reader = PdfReader(uploaded_file)

        resume_text = ""

        for page in reader.pages:
            resume_text += page.extract_text() or ""


        # =========================
        # AI Prompt
        # =========================

        prompt = f"""
You are an expert Resume Analyzer.

Analyze the following resume and provide:

1. Resume Score out of 100
2. Strengths
3. Weaknesses
4. Missing Skills
5. Career Suggestions
6. Interview Preparation Tips

Resume:

{resume_text}
"""


        # =========================
        # Gemini AI
        # =========================

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )


        # =========================
        # Save to Database
        # =========================

        username = st.session_state.get("username", "User")

        save_resume(
            username,
            uploaded_file.name,
            response.text
)


        st.divider()

        st.subheader("🤖 AI Resume Analysis")

        st.write(response.text)

        st.divider()

        st.success(
            "✅ Analysis Completed Successfully"
        )


        # =========================
        # TXT Download
        # =========================

        st.download_button(
            label="📥 Download Analysis (TXT)",
            data=response.text,
            file_name="AI_Resume_Analysis.txt",
            mime="text/plain"
        )


        # =========================
        # PDF REPORT
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


        story.append(
            Paragraph(
                f"<b>Resume:</b> {uploaded_file.name}",
                styles["Normal"]
            )
        )

        story.append(
            Spacer(1, 20)
        )


        # Add AI response to PDF
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


        # Build PDF
        doc.build(story)


        # Read PDF
        with open(pdf_file, "rb") as file:

            pdf_data = file.read()


        # =========================
        # PDF Download
        # =========================

        st.download_button(
            label="📥 Download Analysis (PDF)",
            data=pdf_data,
            file_name="AI_Resume_Analysis.pdf",
            mime="application/pdf"
        )