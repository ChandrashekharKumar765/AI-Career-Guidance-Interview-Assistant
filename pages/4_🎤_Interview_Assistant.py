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
# Logged-in User
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
    "Generate AI-powered interview questions and preparation guidance "
    "for your selected job role."
)


# =========================
# Job Roles
# =========================

job_roles = [
    "Software Developer",
    "Python Developer",
    "Java Developer",
    "C++ Developer",
    "C# Developer",
    "JavaScript Developer",
    "Full Stack Developer",
    "Frontend Developer",
    "Backend Developer",
    "Web Developer",

    "Mobile App Developer",
    "Android Developer",
    "iOS Developer",
    "Flutter Developer",
    "React Native Developer",

    "AI Engineer",
    "Machine Learning Engineer",
    "Deep Learning Engineer",
    "Data Scientist",
    "Data Analyst",
    "Data Engineer",
    "Business Analyst",

    "Cloud Engineer",
    "Cloud Architect",
    "DevOps Engineer",
    "Site Reliability Engineer",

    "Cybersecurity Analyst",
    "Cybersecurity Engineer",
    "Ethical Hacker",
    "Security Engineer",

    "Network Engineer",
    "System Administrator",
    "Database Administrator",
    "IT Support Engineer",
    "Technical Support Engineer",
    "IT Consultant",

    "UI/UX Designer",
    "UX Designer",
    "UI Designer",
    "Product Designer",
    "Graphic Designer",

    "Product Manager",
    "Project Manager",
    "Program Manager",

    "QA Engineer",
    "Software Tester",
    "Automation Tester",
    "QA Analyst",

    "Blockchain Developer",
    "Web3 Developer",
    "Game Developer",
    "AR/VR Developer",

    "Embedded Systems Engineer",
    "IoT Engineer",
    "Robotics Engineer",

    "Electrical Engineer",
    "Mechanical Engineer",
    "Civil Engineer",
    "Electronics Engineer",

    "Digital Marketing Specialist",
    "SEO Specialist",
    "Social Media Manager",
    "Content Writer",
    "Content Strategist",

    "HR Executive",
    "HR Manager",
    "Recruiter",

    "Finance Analyst",
    "Financial Analyst",
    "Accountant",

    "Business Development Executive",
    "Sales Executive",
    "Marketing Executive",

    "Other / Custom Role"
]


# =========================
# User Details
# =========================

name = st.text_input(
    "👤 Your Name"
)


role = st.selectbox(
    "💼 Job Role",
    job_roles
)


# =========================
# Custom Role
# =========================

if role == "Other / Custom Role":

    custom_role = st.text_input(
        "✏️ Enter Your Job Role",
        placeholder="Example: Generative AI Specialist"
    )

    if custom_role.strip():

        role = custom_role.strip()


# =========================
# Difficulty
# =========================

level = st.selectbox(
    "📈 Difficulty Level",
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
    "🚀 Start Interview",
    use_container_width=True
):

    # =========================
    # Validation
    # =========================

    if not name.strip():

        st.warning(
            "⚠️ Please enter your name."
        )

        st.stop()


    if role == "Other / Custom Role":

        st.warning(
            "⚠️ Please enter your custom job role."
        )

        st.stop()


    # =========================
    # AI Prompt
    # =========================

    prompt = f"""
You are an expert technical interviewer and career coach.

Candidate Name:
{name}

Job Role:
{role}

Difficulty Level:
{level}

Create a detailed and professional interview preparation report.

The interview preparation must be specifically tailored
to the selected job role and difficulty level.

Include the following:

1. Interview Questions

Generate 10 important interview questions.

Include a mixture of:

- Technical questions
- Conceptual questions
- Practical questions
- Problem-solving questions
- Role-specific questions

For every question, provide a clear expected answer.

2. Interview Tips

Provide at least 5 useful interview tips
specific to the selected role.

3. Common Mistakes

Provide at least 5 common mistakes candidates
should avoid during the interview.

4. Final Preparation Advice

Provide a practical preparation strategy including:

- Topics to revise
- Skills to practice
- Projects to prepare
- How to answer questions
- How to approach the interview confidently

Use clear headings and numbering.

Give useful explanations rather than extremely short answers.

Make the content practical and suitable for a real interview.
"""


    # =========================
    # AI Response
    # =========================

    st.divider()

    st.subheader(
        "🎯 AI Interview Preparation"
    )

    response_placeholder = st.empty()

    full_response = ""


    # =========================
    # Generate Streaming Response
    # =========================

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
        full_response
    )


    # =========================
    # Success Message
    # =========================

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

    safe_name = (
        name
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    safe_role = (
        role
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


    story.append(
        Paragraph(
            f"<b>Candidate Name:</b> {safe_name}",
            styles["Normal"]
        )
    )

    story.append(
        Spacer(1, 8)
    )


    story.append(
        Paragraph(
            f"<b>Job Role:</b> {safe_role}",
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
    # PDF Heading
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
    # Add AI Response
    # =========================

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