
import sqlite3


# ==========================================================
# Connect to the database
# ==========================================================

def connect_db():

    connection = sqlite3.connect("academic.db")

    return connection


# ==========================================================
# Create all required tables
# ==========================================================

def create_tables():

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS students (

            student_id TEXT PRIMARY KEY,

            student_name TEXT

        )
        """
    )

    connection.commit()

    connection.close()


# ==========================================================
# Save or update a student
# ==========================================================

def save_student(student_id, student_name):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO students
        (student_id, student_name)

        VALUES (?, ?)
        """,
        (
            student_id,
            student_name,
        ),
    )

    connection.commit()

    connection.close()


# ==========================================================
# Load a student
# ==========================================================

def load_student(student_id):

    connection = connect_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT student_name

        FROM students

        WHERE student_id = ?
        """,
        (student_id,),
    )

    result = cursor.fetchone()

    connection.close()

    return result
