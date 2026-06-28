import streamlit as st

from database import (
    get_subjects,
    create_subject,
    delete_subject,
    get_workspace,
    subject_exists,
)


def show_subject_page():

    student_id = st.session_state.student_id

    st.title("📚 My Subjects")
    st.caption(
        f"Logged in as **{st.session_state.student_name}** "
        f"({student_id})"
    )

    st.divider()

    # ======================================================
    # SEARCH
    # ======================================================

    search = st.text_input(
        "🔍 Search Subject",
        placeholder="Type a subject name..."
    ).strip().lower()

    subjects = get_subjects(student_id)

    if search != "":

        subjects = [
            subject
            for subject in subjects
            if search in subject["subject_name"].lower()
        ]

    # ======================================================
    # SUBJECT LIST
    # ======================================================

    if len(subjects) == 0:

        st.info(
            "No subjects found."
        )

    else:

        st.subheader("Saved Subjects")

        for subject in subjects:

            with st.container(border=True):

                left, right = st.columns([5, 1])

                with left:

                    st.markdown(
                        f"### 📘 {subject['subject_name']}"
                    )

                with right:

                    if st.button(
                        "Open",
                        key=f"open_{subject['id']}",
                        use_container_width=True,
                    ):

                        workspace = get_workspace(
                            subject["id"]
                        )

                        st.session_state.selected_subject = (
                            subject["id"]
                        )

                        st.session_state.subject_name = (
                            subject["subject_name"]
                        )

                        if workspace:

                            import pandas as pd

                            st.session_state.syllabus = (
                                pd.DataFrame(
                                    workspace.get(
                                        "syllabus",
                                        []
                                    )
                                )
                            )

                            st.session_state.saved_grades = (
                                pd.DataFrame(
                                    workspace.get(
                                        "grades",
                                        []
                                    )
                                )
                            )

                            st.session_state.target_grade = (
                                workspace.get(
                                    "target_grade",
                                    None
                                )
                            )

                        else:

                            st.session_state.syllabus = None
                            st.session_state.saved_grades = None
                            st.session_state.target_grade = None

                        st.rerun()

                    if st.button(
                        "🗑",
                        key=f"delete_{subject['id']}",
                        use_container_width=True,
                    ):

                        delete_subject(
                            subject["id"]
                        )

                        st.rerun()

    st.divider()

    # ======================================================
    # CREATE SUBJECT
    # ======================================================

    st.subheader("➕ Create Subject")

    subject_name = st.text_input(
        "Subject Name",
        placeholder="Example: Physics"
    )

    if st.button(
        "Create Subject",
        use_container_width=True,
    ):

        subject_name = subject_name.strip()

        if subject_name == "":

            st.error(
                "Please enter a subject name."
            )

        elif subject_exists(
            student_id,
            subject_name,
        ):

            st.warning(
                "A subject with that name already exists."
            )

        else:

            create_subject(
                student_id,
                subject_name,
            )

            st.success(
                "Subject created successfully."
            )

            st.rerun()
