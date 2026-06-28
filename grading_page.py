import streamlit as st
import pandas as pd

from student import Student
from database import save_workspace


# ==========================================================
# DEFAULT SYLLABUS
# ==========================================================

DEFAULT_SYLLABUS = pd.DataFrame(
    {
        "Component": [
            "CO1",
            "CO2",
            "CO3",
            "Attendance",
            "Seatwork",
            "Final Exam",
        ],
        "Weight (%)": [
            15,
            15,
            10,
            10,
            15,
            35,
        ],
    }
)


# ==========================================================
# MAIN PAGE
# ==========================================================

def show_grading_page():

    # ------------------------------------------------------
    # Initialize session state
    # ------------------------------------------------------

    if (
        st.session_state.syllabus is None
        or len(st.session_state.syllabus) == 0
    ):

        st.session_state.syllabus = DEFAULT_SYLLABUS.copy()

    if "saved_grades" not in st.session_state:

        st.session_state.saved_grades = pd.DataFrame()

    if "target_grade" not in st.session_state:

        st.session_state.target_grade = None

    st.header("📚 Syllabus Builder")

    syllabus_df = st.data_editor(

        st.session_state.syllabus,

        hide_index=True,

        use_container_width=True,

        num_rows="dynamic",

        key="syllabus_editor",

        column_config={

            "Component": st.column_config.TextColumn(

                "Component",

                required=True,

            ),

            "Weight (%)": st.column_config.NumberColumn(

                "Weight (%)",

                min_value=0.0,

                step=1.0,

                format="%.2f",

            ),

        },

    )

    # ------------------------------------------------------
    # Clean data
    # ------------------------------------------------------

    syllabus_df = syllabus_df.dropna(how="all")

    syllabus_df["Component"] = (

        syllabus_df["Component"]

        .fillna("")

        .astype(str)

        .str.strip()

    )

    syllabus_df = syllabus_df[

        syllabus_df["Component"] != ""

    ]

    syllabus_df["Weight (%)"] = pd.to_numeric(

        syllabus_df["Weight (%)"],

        errors="coerce",

    ).fillna(0)

    st.session_state.syllabus = syllabus_df.copy()

    # ------------------------------------------------------
    # Weight Summary
    # ------------------------------------------------------

    total_weight = syllabus_df["Weight (%)"].sum()

    st.subheader("Weight Summary")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            "Current Total Weight",

            f"{total_weight:.2f}%",

        )

    with col2:

        if total_weight < 100:

            st.warning(

                f"Remaining Weight: {100-total_weight:.2f}%"

            )

        elif total_weight > 100:

            st.error(

                f"Exceeded by {total_weight-100:.2f}%"

            )

        else:

            st.success(

                "Perfect! Total weight is exactly 100%."

            )

    st.divider()

    # ======================================================
    # TARGET GRADE
    # ======================================================

    st.header("🎯 Target Grade")

    target_input = st.text_input(

        "Target Grade (%)",

        value="" if st.session_state.target_grade is None else str(
            st.session_state.target_grade
        ),

    )

    try:

        target_grade = (

            float(target_input)

            if target_input.strip()

            else None

        )

    except:

        target_grade = None

    st.session_state.target_grade = target_grade

    # ======================================================
    # GRADE ENTRY
    # ======================================================

    st.header("📝 Grades")

    grades = []

    saved = st.session_state.saved_grades

    for index, row in syllabus_df.iterrows():

        default_score = ""

        if (

            not saved.empty

            and index < len(saved)

            and "Score" in saved.columns

        ):

            default_score = str(

                saved.iloc[index]["Score"]

            )

        score = st.text_input(

            f"{row['Component']} Score",

            value=default_score,

            key=f"score_{index}",

        )

        grades.append(

            {

                "Component": row["Component"],

                "Weight (%)": row["Weight (%)"],

                "Score": score,

            }

        )

    grades_df = pd.DataFrame(grades)

    st.session_state.saved_grades = grades_df.copy()

    # ======================================================
    # ACADEMIC REPORT
    # ======================================================

    st.divider()

    st.header("📊 Academic Report")

    can_generate = (
        len(syllabus_df) > 0
        and abs(total_weight - 100) < 0.0001
    )

    if st.button(
        "Generate Academic Report",
        use_container_width=True,
        disabled=not can_generate,
    ):

        try:

            student = Student(
                st.session_state.student_id,
                st.session_state.student_name,
            )

            final_grade, breakdown = (
                student.compute_final_grade(
                    grades_df
                )
            )

            standing = student.get_academic_standing(
                final_grade
            )

            st.success(
                "Academic Report Generated!"
            )

            st.divider()

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Final Grade",
                    f"{final_grade:.2f}%"
                )

                st.progress(
                    min(final_grade / 100, 1.0)
                )

            with col2:

                st.write(
                    f"**Student ID:** {st.session_state.student_id}"
                )

                st.write(
                    f"**Student Name:** {st.session_state.student_name}"
                )

                st.write(
                    f"**Academic Standing:** {standing}"
                )

            st.divider()

            st.subheader(
                "Grade Breakdown"
            )

            st.dataframe(
                breakdown,
                hide_index=True,
                use_container_width=True,
            )

            # ==========================================
            # TARGET ANALYSIS
            # ==========================================

            if target_grade is not None:

                analysis = student.target_analysis(
                    grades_df,
                    final_grade,
                    target_grade,
                )

                st.divider()

                st.subheader(
                    "🎯 Target Grade Analysis"
                )

                st.write(
                    f"**Target Grade:** "
                    f"{target_grade:.2f}%"
                )

                required = analysis[
                    "required_average"
                ]

                if required is None:

                    st.info(
                        "There are no remaining components."
                    )

                elif required <= 0:

                    st.success(
                        "🎉 You have already reached your target."
                    )

                elif required <= 100:

                    st.info(
                        f"You need an average of "
                        f"**{required:.2f}%** "
                        "on the remaining components."
                    )

                    st.write(
                        "Remaining Components:"
                    )

                    for component in analysis[
                        "remaining_components"
                    ]:

                        st.write(
                            f"• {component}"
                        )

                else:

                    st.error(
                        f"You would need "
                        f"**{required:.2f}%** "
                        "which is above 100%."
                    )

        except Exception as e:

            st.error(str(e))

    # ======================================================
    # AUTO SAVE
    # ======================================================

    current_workspace = {
        "syllabus": syllabus_df.to_dict("records"),
        "grades": grades_df.to_dict("records"),
        "target_grade": target_grade,
    }

    previous_workspace = st.session_state.get(
        "_last_saved_workspace"
    )

    if current_workspace != previous_workspace:

        try:

            final_grade = None

            try:

                student = Student(
                    st.session_state.student_id,
                    st.session_state.student_name,
                )

                final_grade, _ = student.compute_final_grade(
                    grades_df
                )

            except:
                pass

            save_workspace(
                st.session_state.selected_subject,
                syllabus_df,
                grades_df,
                target_grade,
                final_grade,
            )

            st.session_state._last_saved_workspace = (
                current_workspace
            )

        except Exception as e:

            st.warning(
                f"Auto-save failed: {e}"
            )
