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

    # ======================================================
    # EMPTY STATE
    # ======================================================

    if not subjects:

        st.info("You don't have any subjects yet.")
        st.caption("Create your first subject below 👇")

    else:

        st.subheader("Saved Subjects")

        # ==================================================
        # SUBJECT CARDS
        # ==================================================

        for subject in subjects:

            with st.container(border=True):

                col1, col2 = st.columns([4, 1])

                with col1:
                    st.markdown(f"### 📘 {subject['subject_name']}")
                    st.caption(f"Subject ID: {subject['id']}")

                with col2:

                    if st.button(
                        "Open",
                        key=f"open_{subject['id']}",
                        use_container_width=True
                    ):
                        st.session_state.selected_subject = subject["id"]
                        st.rerun()

                    if st.button(
                        "🗑 Delete",
                        key=f"delete_{subject['id']}",
                        use_container_width=True
                    ):
                        delete_subject(subject["id"])
                        st.rerun()

            st.divider()

    # ======================================================
    # CREATE NEW SUBJECT
    # ======================================================

    st.subheader("➕ Create New Subject")

    subject_name = st.text_input(
        "Subject Name",
        placeholder="e.g. Mathematics"
    )

    if st.button(
        "Create Subject",
        use_container_width=True
    ):

        if subject_name.strip() == "":
            st.error("Please enter a subject name.")

        else:
            create_subject(student_id, subject_name)
            st.success("Subject created successfully!")
            st.rerun()
