import streamlit as st

from database import (
    get_subjects,
    create_subject,
    delete_subject,
    subject_exists,
)


def show_subject_page():

    st.title("📚 My Subjects")

    st.caption(
        f"Logged in as **{st.session_state.student_name}**"
    )

    st.divider()

    student_id = st.session_state.student_id

    subjects = get_subjects(student_id)

    # ==============================================
    # SEARCH
    # ==============================================

    search = st.text_input(
        "🔍 Search Subject",
        placeholder="Type subject name..."
    ).strip().lower()

    if search:

        subjects = [

            subject

            for subject in subjects

            if search in subject["subject_name"].lower()

        ]

    # ==============================================
    # SUBJECT LIST
    # ==============================================

    if len(subjects) == 0:

        st.info("No subjects found.")

    else:

        st.subheader("Subjects")

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

                        st.session_state.selected_subject = (
                            subject["id"]
                        )

                        st.session_state.workspace_loaded = False

                        st.rerun()

                    if st.button(
                        "🗑",
                        key=f"delete_{subject['id']}",
                        use_container_width=True,
                    ):

                        delete_subject(subject["id"])

                        st.rerun()

    st.divider()

    # ==============================================
    # CREATE SUBJECT
    # ==============================================

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
                "Subject already exists."
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
