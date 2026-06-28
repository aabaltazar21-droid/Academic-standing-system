import streamlit as st
from database import (
    get_subjects,
    create_subject,
    delete_subject,
)


def show_subject_page():

    st.header("📚 My Subjects")

    student_id = st.session_state.student_id

    subjects = get_subjects(student_id)

    if len(subjects) == 0:

        st.info(
            "You haven't created any subjects yet."
        )

    else:

        st.subheader("Saved Subjects")

        for subject in subjects:

            col1, col2 = st.columns([5, 1])

            with col1:

                if st.button(
                    subject["subject_name"],
                    key=f"open_{subject['id']}",
                    use_container_width=True,
                ):

                    st.session_state.selected_subject = subject["id"]

                    st.success(
                        f"Opened {subject['subject_name']}"
                    )

            with col2:

                if st.button(
                    "🗑",
                    key=f"delete_{subject['id']}",
                ):

                    delete_subject(subject["id"])

                    st.rerun()

    st.divider()

    st.subheader("Create Subject")

    subject_name = st.text_input(
        "Subject Name"
    )

    if st.button(
        "Create Subject",
        use_container_width=True,
    ):

        if subject_name.strip() == "":

            st.error(
                "Please enter a subject name."
            )

        else:

            create_subject(
                student_id,
                subject_name
            )

            st.rerun()
