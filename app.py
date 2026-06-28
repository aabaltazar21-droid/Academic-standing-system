import streamlit as st
import pandas as pd

from database import (
    get_student_by_id,
    login_student,
    create_student,
)

from subject_page import show_subject_page
from grading_page import show_grading_page


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Academic Standing Status System",
    page_icon="🎓",
    layout="wide",
)


# ==========================================================
# SESSION STATE
# ==========================================================

DEFAULT_SESSION = {

    "logged_in": False,

    "student_id": "",

    "student_name": "",

    "selected_subject": None,

    "workspace_loaded": False,

    "syllabus": pd.DataFrame(),

    "saved_grades": pd.DataFrame(),

    "target_grade": None,

    "_last_workspace": None,

}

for key, value in DEFAULT_SESSION.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ==========================================================
# TITLE
# ==========================================================

st.title("🎓 Academic Standing Status System")

st.caption(
    "Create your own grading system and monitor your academic standing."
)

st.divider()


# ==========================================================
# LOGIN
# ==========================================================

if not st.session_state.logged_in:

    student_id = st.text_input(
        "Student ID"
    )

    student_name = st.text_input(
        "Student Name"
    )

    if st.button(
        "Login",
        use_container_width=True,
    ):

        student_id = student_id.strip()
        student_name = student_name.strip()

        if student_id == "" or student_name == "":

            st.error(
                "Please enter both Student ID and Student Name."
            )

            st.stop()

        existing = get_student_by_id(
            student_id
        )

        if existing is None:

            create_student(
                student_id,
                student_name,
            )

        student = login_student(
            student_id,
            student_name,
        )

        if student is None:

            st.error(
                "Student ID and Name do not match."
            )

            st.stop()

        st.session_state.logged_in = True

        st.session_state.student_id = student_id

        st.session_state.student_name = student_name

        st.rerun()

    st.stop()

# ==========================================================
# TOP BAR
# ==========================================================

left, right = st.columns([5, 1])

with left:

    st.write(
        f"Welcome **{st.session_state.student_name}**"
    )

with right:

    if st.button(
        "Logout",
        use_container_width=True,
    ):

        for key, value in DEFAULT_SESSION.items():

            if isinstance(value, pd.DataFrame):
                st.session_state[key] = pd.DataFrame()

            else:
                st.session_state[key] = value

        st.rerun()


st.divider()


# ==========================================================
# SUBJECT PAGE
# ==========================================================

if st.session_state.selected_subject is None:

    show_subject_page()

    st.stop()


# ==========================================================
# BACK BUTTON
# ==========================================================

if st.button("⬅ Back to Subjects"):

    st.session_state.selected_subject = None

    st.session_state.workspace_loaded = False

    st.session_state.syllabus = pd.DataFrame()

    st.session_state.saved_grades = pd.DataFrame()

    st.session_state.target_grade = None

    st.session_state._last_workspace = None

    st.rerun()


st.divider()

# ==========================================================
# GRADING PAGE
# ==========================================================

show_grading_page()
