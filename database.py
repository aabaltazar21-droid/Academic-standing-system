import sqlite3


# ==========================================================
# Connect to the SQLite Database
# ==========================================================

DATABASE_NAME = "academic.db"


def connect_db():

    connection = sqlite3.connect(DATABASE_NAME)

    return connection


# ==========================================================
# Create All Database Tables
# ==========================================================

def create_tables():

    connection = connect_db()

    cursor = connection.cursor()

    # ------------------------------------------------------
    # STUDENTS TABLE
    # One row per student.
    # ------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (

            student_id TEXT PRIMARY KEY,

            student_name TEXT NOT NULL

        )
        """
    )

    # ------------------------------------------------------
    # SUBJECTS TABLE
    # One student can own many subjects.
    # ------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS subjects (

            subject_id INTEGER PRIMARY KEY AUTOINCREMENT,

            student_id TEXT NOT NULL,

            subject_name TEXT NOT NULL,

            FOREIGN KEY(student_id)
                REFERENCES students(student_id)

        )
        """
    )

    # ------------------------------------------------------
    # WORKSPACES TABLE
    # Stores everything inside one subject.
    # ------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS workspaces (

            subject_id INTEGER PRIMARY KEY,

            target_grade REAL,

            syllabus_json TEXT,

            grades_json TEXT,

            FOREIGN KEY(subject_id)
                REFERENCES subjects(subject_id)

        )
        """
    )

    connection.commit()

    connection.close()
