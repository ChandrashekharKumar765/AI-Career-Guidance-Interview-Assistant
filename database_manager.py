import sqlite3
import os

DB_DIR = "database"
DB_NAME = os.path.join(DB_DIR, "project.db")

os.makedirs(DB_DIR, exist_ok=True)


def create_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        file_name TEXT,
        analysis TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS career_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        degree TEXT,
        skills TEXT,
        interest TEXT,
        guidance TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT,
        level TEXT,
        questions TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


def save_resume(file_name, analysis):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO resume_history (file_name, analysis) VALUES (?, ?)",
        (file_name, analysis)
    )

    conn.commit()
    conn.close()


def save_career(name, degree, skills, interest, guidance):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO career_history
    (name, degree, skills, interest, guidance)
    VALUES (?, ?, ?, ?, ?)
    """, (name, degree, skills, interest, guidance))

    conn.commit()
    conn.close()


def save_interview(name, role, level, questions):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO interview_history
    (name, role, level, questions)
    VALUES (?, ?, ?, ?)
    """, (name, role, level, questions))

    conn.commit()
    conn.close()


def get_counts():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM resume_history")
    resume_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM career_history")
    career_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM interview_history")
    interview_count = cursor.fetchone()[0]

    conn.close()

    return resume_count, career_count, interview_count


# =========================
# HISTORY FUNCTIONS
# =========================

def get_resume_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT file_name, analysis, created_at
    FROM resume_history
    ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return data


def get_career_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, degree, skills, interest, guidance, created_at
    FROM career_history
    ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return data


def get_interview_history():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, role, level, questions, created_at
    FROM interview_history
    ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()

    return data