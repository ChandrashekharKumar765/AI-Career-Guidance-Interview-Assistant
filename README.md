# 🤖 AI Career Guidance & Interview Assistant using Gemini AI

An AI-powered career assistance platform designed to help students with resume analysis, career guidance, and interview preparation using Google's Gemini AI.

---

## 📌 Project Overview

The **AI Career Guidance & Interview Assistant** is a web-based application developed using Python and Streamlit.

The system uses Gemini AI to provide personalized career-related assistance to students. It allows users to analyze their resumes, receive career guidance, generate interview preparation material, and view their previous activities.

The application also uses SQLite for storing user activity and ReportLab for generating PDF reports.

---

## 🎯 Objectives

- Analyze resumes using Artificial Intelligence.
- Provide personalized career recommendations.
- Generate interview questions and expected answers.
- Help students identify missing skills.
- Provide career roadmaps and preparation guidance.
- Store previous activities in a database.
- Generate downloadable TXT and PDF reports.
- Provide secure login and logout functionality.

---

## ✨ Key Features

### 🔐 User Login & Authentication
- Username and password based login.
- Protected application pages.
- Logout functionality.

### 📊 Dashboard
- Displays total resume analyses.
- Displays total career guidance reports.
- Displays total interview sessions.
- Provides an overview of the complete platform.

### 📄 AI Resume Analysis
Users can upload a PDF resume and receive:

- Resume Score
- Strengths
- Weaknesses
- Missing Skills
- Career Suggestions
- Interview Preparation Tips

The generated analysis can be downloaded as TXT and PDF.

### 💼 AI Career Guidance

Students can enter:

- Name
- Degree
- Skills
- Career Interest

The AI provides:

- Best Career Option
- Expected Salary Range
- Skills to Learn
- 6-Month Roadmap
- Certifications
- Companies to Target
- Interview Preparation Tips

### 🎤 AI Interview Assistant

Users can select:

- Job Role
- Difficulty Level

The system generates:

- 10 Interview Questions
- Expected Answers
- Interview Tips
- Common Mistakes
- Final Preparation Advice

Interview preparation can be downloaded as TXT and PDF.

### 🕒 Activity History

The system stores and displays:

- Resume Analysis History
- Career Guidance History
- Interview History

---

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Streamlit | Web application interface |
| Google Gemini AI | AI-generated analysis and guidance |
| SQLite | Database management |
| PyPDF2 | PDF resume text extraction |
| ReportLab | PDF report generation |
| python-dotenv | Environment variable management |

---

## 📂 Project Structure

```text
AI Career Guidance & Interview Assistant
│
├── app.py
├── auth.py
├── database_manager.py
├── requirements.txt
├── README.md
├── .env
│
├── database
│   └── project.db
│
├── pages
│   ├── 1_Dashboard.py
│   ├── 2_Resume_Analysis.py
│   ├── 3_Career_Guidance.py
│   ├── 4_Interview_Assistant.py
│   ├── 5_History.py
│   └── 6_Login.py
│
├── assets
└── uploads