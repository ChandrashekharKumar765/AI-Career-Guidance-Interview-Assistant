import sqlite3
import os
import hashlib


# =========================
# Database Configuration
# =========================

DB_DIR = "database"
DB_NAME = os.path.join(DB_DIR, "project.db")

os.makedirs(DB_DIR, exist_ok=True)


# =========================
# Password Hashing
# =========================

def hash_password(password):
    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()


# =========================
# Database Migration Helper
# =========================

def add_column_if_missing(cursor, table_name, column_name, column_type):

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    columns = [
        column[1]
        for column in cursor.fetchall()
    ]

    if column_name not in columns:

        cursor.execute(
            f"""
            ALTER TABLE {table_name}
            ADD COLUMN {column_name} {column_type}
            """
        )


# =========================
# Create Database
# =========================

def create_database():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # =========================
    # Resume History
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resume_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        file_name TEXT,
        analysis TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # Career History
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS career_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        name TEXT,
        degree TEXT,
        skills TEXT,
        interest TEXT,
        guidance TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # Interview History
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interview_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        name TEXT,
        role TEXT,
        level TEXT,
        questions TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # Users
    # =========================

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # =========================
    # Automatic Migration
    # =========================

    add_column_if_missing(
        cursor,
        "resume_history",
        "username",
        "TEXT"
    )

    add_column_if_missing(
        cursor,
        "career_history",
        "username",
        "TEXT"
    )

    add_column_if_missing(
        cursor,
        "interview_history",
        "username",
        "TEXT"
    )

    conn.commit()
    conn.close()


# =========================
# Register User
# =========================

def register_user(username, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    password_hash = hash_password(password)

    try:

        cursor.execute(
            """
            INSERT INTO users
            (username, password)
            VALUES (?, ?)
            """,
            (
                username,
                password_hash
            )
        )

        conn.commit()

        return True, "Registration successful."

    except sqlite3.IntegrityError:

        return False, "Username already exists."

    finally:

        conn.close()


# =========================
# Verify Login
# =========================

def verify_user(username, password):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    password_hash = hash_password(password)

    cursor.execute(
        """
        SELECT username
        FROM users
        WHERE username = ?
        AND password = ?
        """,
        (
            username,
            password_hash
        )
    )

    user = cursor.fetchone()

    conn.close()

    return user is not None


# =========================
# Save Resume
# =========================

def save_resume(
    username,
    file_name,
    analysis
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO resume_history
        (username, file_name, analysis)
        VALUES (?, ?, ?)
        """,
        (
            username,
            file_name,
            analysis
        )
    )

    conn.commit()
    conn.close()


# =========================
# Save Career
# =========================

def save_career(
    username,
    name,
    degree,
    skills,
    interest,
    guidance
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO career_history
        (username, name, degree, skills, interest, guidance)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            username,
            name,
            degree,
            skills,
            interest,
            guidance
        )
    )

    conn.commit()
    conn.close()


# =========================
# Save Interview
# =========================

def save_interview(
    username,
    name,
    role,
    level,
    questions
):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interview_history
        (username, name, role, level, questions)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            username,
            name,
            role,
            level,
            questions
        )
    )

    conn.commit()
    conn.close()


# =========================
# Dashboard Counts
# =========================

def get_counts(username):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM resume_history
        WHERE username = ?
        """,
        (username,)
    )

    resume_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM career_history
        WHERE username = ?
        """,
        (username,)
    )

    career_count = cursor.fetchone()[0]

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM interview_history
        WHERE username = ?
        """,
        (username,)
    )

    interview_count = cursor.fetchone()[0]

    conn.close()

    return (
        resume_count,
        career_count,
        interview_count
    )


# =========================
# Resume History
# =========================

def get_resume_history(username):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT file_name, analysis, created_at
        FROM resume_history
        WHERE username = ?
        ORDER BY id DESC
        """,
        (username,)
    )

    data = cursor.fetchall()

    conn.close()

    return data


# =========================
# Career History
# =========================

def get_career_history(username):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name, degree, skills, interest, guidance, created_at
        FROM career_history
        WHERE username = ?
        ORDER BY id DESC
        """,
        (username,)
    )

    data = cursor.fetchall()

    conn.close()

    return data


# =========================
# Interview History
# =========================

def get_interview_history(username):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT name, role, level, questions, created_at
        FROM interview_history
        WHERE username = ?
        ORDER BY id DESC
        """,
        (username,)
    )

    data = cursor.fetchall()

    conn.close()

    return data