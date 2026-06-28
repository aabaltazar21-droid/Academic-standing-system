from database import (
    get_student_by_id,
    login_student,
    create_student,
    get_subjects,
    create_subject,
    delete_subject,
    get_workspace,
    save_workspace,
)

from subject_page import show_subject_page
import streamlit as st
import pandas as pd


# ==========================================================
# STUDENT CLASS
# ==========================================================

class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

    def compute_final_grade(self, grades_df):

        final_grade = 0
        breakdown = []

        for _, row in grades_df.iterrows():

            component = str(row["Component"]).strip()
            weight = float(row["Weight (%)"])
            score = str(row["Score"]).strip()

            if score == "":
                continue

            try:

                if "/" in score:
                    earned, total = score.split("/")
                    earned = float(earned.strip())
                    total = float(total.strip())

                    if total <= 0:
                        raise ValueError

                    percentage = (earned / total) * 100

                else:
                    percentage = float(score)

            except ValueError:
                raise ValueError(
                    f"{component}: Invalid score format.\n"
                    "Use: 45/50, 18/20, 90, 87.5"
                )

            contribution = percentage * weight / 100
            final_grade += contribution

            breakdown.append({
                "Component": component,
                "Score": score,
                "Percentage": round(percentage, 2),
                "Weight (%)": weight,
                "Contribution": round(contribution, 2),
            })

        return final_grade, pd.DataFrame(breakdown)

    def get_result(self, grade):

        if grade >= 90:
            return "Outstanding"
        elif grade >= 85:
            return "Very Satisfactory"
        elif grade >= 80:
            return "Satisfactory"
        elif grade >= 75:
            return "Passing"
        else:
            return "Needs Improvement"


# ==========================================================
# PAGE SETUP
# ==========================================================

st.set_page_config(
    page_title="Academic Standing Status System",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Academic Standing Status System")
st.write("Create your own grading system or load the default syllabus.")
st.divider()


# ==========================================================
# SESSION STATE INIT
# ==========================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "student_id" not in st.session_state:
    st.session_state.student_id = ""

if "student_name" not in st.session_state:
    st.session_state.student_name = ""

if "selected_subject" not in st.session_state:
    st.session_state.selected_subject = None

if "syllabus" not in st.session_state:
    st.session_state.syllabus = pd.DataFrame()


# ==========================================================
# LOGIN
# ==========================================================

student_id = st.text_input("Student ID")
student_name = st.text_input("Student Name")

if st.button("Login"):

    if student_id.strip() == "" or student_name.strip() == "":
        st.error("Please enter both Student ID and Student Name.")

    else:

        existing = get_student_by_id(student_id)

        if existing is None:
            create_student(student_id, student_name)

        student = login_student(student_id, student_name)

        if student is None:
            st.error("Student ID and name do not match.")
        else:
            st.session_state.logged_in = True
            st.session_state.student_id = student_id
            st.session_state.student_name = student_name
            st.success(f"Welcome {student_name}!")


# ==========================================================
# SUBJECT PAGE
# ==========================================================

if not st.session_state.logged_in:
    st.stop()

if st.session_state.selected_subject is None:
    show_subject_page()
    st.stop()


# ==========================================================
# LOAD WORKSPACE (IMPORTANT FIX)
# ==========================================================

workspace = get_workspace(st.session_state.selected_subject)

if workspace:

    st.session_state.syllabus = pd.DataFrame(
        workspace.get("syllabus", [])
    )

    st.session_state.saved_grades = pd.DataFrame(
        workspace.get("grades", [])
    )

    target_grade = workspace.get("target_grade")

else:
    target_grade = None


# ==========================================================
# DEFAULT SYLLABUS
# ==========================================================

DEFAULT_SYLLABUS = pd.DataFrame({
    "Component": [
        "CO1", "CO2", "CO3",
        "Coursera", "Attendance",
        "Seatwork", "Final Exam"
    ],
    "Weight (%)": [15, 15, 10, 10, 5, 15, 30]
})

if st.session_state.syllabus.empty:
    st.session_state.syllabus = DEFAULT_SYLLABUS.copy()


# ==========================================================
# SYLLABUS EDITOR
# ==========================================================

st.header("📚 Syllabus Builder")

syllabus_df = st.data_editor(
    st.session_state.syllabus,
    use_container_width=True,
    num_rows="dynamic",
)

st.session_state.syllabus = syllabus_df


# ==========================================================
# TARGET GRADE
# ==========================================================

st.header("🎯 Target Grade")

target_input = st.text_input("Target Grade (%)")

try:
    target_grade = float(target_input) if target_input else None
except:
    target_grade = None


# ==========================================================
# GRADE INPUT
# ==========================================================

st.header("📝 Grades")

grades = []

for i, row in syllabus_df.iterrows():

    score = st.text_input(
        f"{row['Component']} Score",
        key=f"score_{i}"
    )

    grades.append({
        "Component": row["Component"],
        "Weight (%)": row["Weight (%)"],
        "Score": score
    })

grades_df = pd.DataFrame(grades)


# ==========================================================
# REPORT
# ==========================================================

st.header("📊 Academic Report")

if st.button("Generate Report"):

    try:

        student = Student(
            st.session_state.student_id,
            st.session_state.student_name
        )

        final_grade, breakdown = student.compute_final_grade(grades_df)
        standing = student.get_result(final_grade)

        st.success("Report Generated!")

        st.metric("Final Grade", f"{final_grade:.2f}%")

        st.write("Standing:", standing)

        st.dataframe(breakdown)

        # SAVE BUTTON (FIXED)
        if st.button("💾 Save Progress"):

            save_workspace(
                st.session_state.selected_subject,
                syllabus_df,
                grades_df,
                target_grade,
                final_grade
            )

            st.success("Saved successfully!")

    except Exception as e:
        st.error(str(e))
