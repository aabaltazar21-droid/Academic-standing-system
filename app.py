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
                raise ValueError(f"{component}: Invalid score format")

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
# SETUP
# ==========================================================

st.set_page_config(
    page_title="Academic System",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Academic Standing System")
st.divider()


# ==========================================================
# SESSION STATE
# ==========================================================

for key, default in {
    "logged_in": False,
    "student_id": "",
    "student_name": "",
    "selected_subject": None,
    "syllabus": pd.DataFrame(),
}.items():
    if key not in st.session_state:
        st.session_state[key] = default


# ==========================================================
# LOGIN
# ==========================================================

student_id = st.text_input("Student ID")
student_name = st.text_input("Student Name")

if st.button("Login"):

    if not student_id or not student_name:
        st.error("Fill all fields")

    else:
        if get_student_by_id(student_id) is None:
            create_student(student_id, student_name)

        student = login_student(student_id, student_name)

        if student:
            st.session_state.logged_in = True
            st.session_state.student_id = student_id
            st.session_state.student_name = student_name
            st.success("Logged in")
        else:
            st.error("Invalid login")


if not st.session_state.logged_in:
    st.stop()


# ==========================================================
# SUBJECT PAGE
# ==========================================================

if st.session_state.selected_subject is None:
    show_subject_page()
    st.stop()


# ==========================================================
# SUBJECT HEADER
# ==========================================================

subjects = get_subjects(st.session_state.student_id)

current = next(
    (s for s in subjects if s["id"] == st.session_state.selected_subject),
    None
)

if current:
    st.title(f"📘 {current['subject_name']}")
    st.divider()


# ==========================================================
# LOAD WORKSPACE
# ==========================================================

workspace = get_workspace(st.session_state.selected_subject)

if workspace:
    st.session_state.syllabus = pd.DataFrame(workspace.get("syllabus", []))
    target_grade = workspace.get("target_grade")
else:
    target_grade = None


DEFAULT = pd.DataFrame({
    "Component": ["CO1", "CO2", "CO3", "Attendance", "Exam"],
    "Weight (%)": [20, 20, 20, 10, 30]
})

if st.session_state.syllabus.empty:
    st.session_state.syllabus = DEFAULT


# ==========================================================
# SYLLABUS
# ==========================================================

st.header("📚 Syllabus")

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
    target = float(target_input) if target_input else None
except:
    target = None


# ==========================================================
# GRADES
# ==========================================================

st.header("📝 Grades")

grades = []

for i, row in syllabus_df.iterrows():

    score = st.text_input(f"{row['Component']} Score", key=f"s{i}")

    grades.append({
        "Component": row["Component"],
        "Weight (%)": row["Weight (%)"],
        "Score": score
    })

grades_df = pd.DataFrame(grades)


# ==========================================================
# REPORT
# ==========================================================

st.header("📊 Report")

if st.button("Generate"):

    student = Student(st.session_state.student_id, st.session_state.student_name)

    final, breakdown = student.compute_final_grade(grades_df)
    st.success("Generated")

    st.metric("Final Grade", f"{final:.2f}%")
    st.dataframe(breakdown)

    # ================= TARGET =================

    if target is not None:

        remaining_w = 0
        remaining = []

        for _, r in grades_df.iterrows():
            if str(r["Score"]).strip() == "":
                remaining_w += r["Weight (%)"]
                remaining.append(r["Component"])

        if remaining_w > 0:
            needed = (target - final) / remaining_w * 100

            st.divider()
            st.subheader("🎯 Target Analysis")

            if needed <= 0:
                st.success("Target already met")
            elif needed <= 100:
                st.info(f"You need {needed:.2f}% average")
                for c in remaining:
                    st.write("•", c)
            else:
                st.error("Impossible without bonus")


    # ================= SAVE =================

    if st.button("💾 Save"):

        save_workspace(
            st.session_state.selected_subject,
            syllabus_df,
            grades_df,
            target,
            final
        )

        st.success("Saved")


# ==========================================================
# AUTO SYNC (SAFE VERSION)
# ==========================================================

save_workspace(
    st.session_state.selected_subject,
    st.session_state.syllabus,
    grades_df,
    target,
    0
)
