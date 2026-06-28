import streamlit as st
import pandas as pd

from student import Student
from database import (
    get_workspace,
    save_workspace,
)


def show_grading_page():

    # ======================================================
    # LOAD WORKSPACE (ONLY ONCE)
    # ======================================================

    if not st.session_state.workspace_loaded:

        workspace = get_workspace(
            st.session_state.selected_subject
        )

        if workspace:

            syllabus = workspace.get(
                "syllabus",
                []
            )

            grades = workspace.get(
                "grades",
                []
            )

            target = workspace.get(
                "target_grade",
                None
            )

            st.session_state.syllabus = pd.DataFrame(
                syllabus
            )

            st.session_state.saved_grades = pd.DataFrame(
                grades
            )

            st.session_state.target_grade = target

        st.session_state.workspace_loaded = True

    # ======================================================
    # DEFAULT SYLLABUS
    # ======================================================

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

    if st.session_state.syllabus.empty:

        st.session_state.syllabus = (
            DEFAULT_SYLLABUS.copy()
        )

    student = Student(
        st.session_state.student_id,
        st.session_state.student_name,
    )

    # ======================================================
    # SYLLABUS BUILDER
    # ======================================================

    st.header("📚 Syllabus Builder")

    col1, col2 = st.columns(2)

    with col1:

        if st.button(
            "📋 Load Default Syllabus",
            use_container_width=True,
        ):

            st.session_state.syllabus = (
                DEFAULT_SYLLABUS.copy()
            )

            st.rerun()

    with col2:

        if st.button(
            "🗑 Clear Syllabus",
            use_container_width=True,
        ):

            st.session_state.syllabus = pd.DataFrame(
                columns=[
                    "Component",
                    "Weight (%)",
                ]
            )

            st.rerun()

    syllabus_df = st.data_editor(
        st.session_state.syllabus,
        hide_index=True,
        use_container_width=True,
        num_rows="dynamic",
    )

    syllabus_df = syllabus_df.dropna(
        how="all"
    )

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

    total_weight = student.total_weight(
        syllabus_df
    )

    st.subheader("Weight Summary")

    left, right = st.columns(2)

    with left:

        st.metric(
            "Current Total Weight",
            f"{total_weight:.2f}%"
        )

    with right:

        if total_weight < 100:

            st.warning(
                f"Remaining: {100-total_weight:.2f}%"
            )

        elif total_weight > 100:

            st.error(
                f"Exceeded: {total_weight-100:.2f}%"
            )

        else:

            st.success(
                "Total weight is 100%"
            )

    st.divider()

    # ======================================================
    # TARGET GRADE
    # ======================================================

    st.header("🎯 Target Grade")

    target_input = st.text_input(
        "Target Grade (%)",
        value=""
        if st.session_state.target_grade is None
        else str(st.session_state.target_grade),
        placeholder="Optional",
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

    st.divider()

    # ======================================================
    # GRADE ENTRY
    # ======================================================

    st.header("📝 Enter Student Scores")

    st.info(
        """
The Score field accepts:

• 45/50
• 18/20
• 90
• 87.5
• 105/100
"""
    )

    grades = []

    previous = st.session_state.saved_grades

    for index, row in syllabus_df.iterrows():

        component = row["Component"]
        weight = row["Weight (%)"]

        st.subheader(
            f"{component} ({weight:.2f}%)"
        )

        default_score = ""

        if (
            not previous.empty
            and index < len(previous)
            and "Score" in previous.columns
        ):

            default_score = str(
                previous.iloc[index]["Score"]
            )

        score = st.text_input(
            "Score",
            value=default_score,
            placeholder="45/50 or 90",
            key=f"score_{index}",
        )

        if score.strip() != "":

            try:

                if "/" in score:

                    earned, total = score.split("/")

                    earned = float(earned.strip())
                    total = float(total.strip())

                    percentage = (
                        earned / total
                    ) * 100

                else:

                    percentage = float(score)

                contribution = (
                    percentage * weight / 100
                )

                st.success(
                    f"Percentage: {percentage:.2f}% | "
                    f"Contribution: {contribution:.2f}"
                )

            except:

                st.error(
                    "Invalid score format."
                )

        grades.append(
            {
                "Component": component,
                "Weight (%)": weight,
                "Score": score,
            }
        )

        st.divider()

    grades_df = pd.DataFrame(grades)

    st.session_state.saved_grades = (
        grades_df.copy()
    )

    # ======================================================
    # ACADEMIC REPORT
    # ======================================================

    st.header("📊 Academic Report")

    can_generate = (
        len(syllabus_df) > 0
        and student.validate_weights(syllabus_df)
    )

    if st.button(
        "Generate Academic Report",
        disabled=not can_generate,
        use_container_width=True,
    ):

        try:

            final_grade, breakdown = (
                student.compute_final_grade(
                    grades_df
                )
            )

            standing = (
                student.get_academic_standing(
                    final_grade
                )
            )

            st.success(
                "Academic Report Generated!"
            )

            st.divider()

            left, right = st.columns(2)

            with left:

                st.metric(
                    "Final Grade",
                    f"{final_grade:.2f}%"
                )

                st.progress(
                    min(final_grade / 100, 1.0)
                )

            with right:

                st.write(
                    f"**Student ID:** "
                    f"{student.student_id}"
                )

                st.write(
                    f"**Student Name:** "
                    f"{student.student_name}"
                )

                st.write(
                    f"**Academic Standing:** "
                    f"{standing}"
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

            # ============================================
            # TARGET GRADE ANALYSIS
            # ============================================

            if target_grade is not None:

                analysis = (
                    student.target_analysis(
                        grades_df,
                        final_grade,
                        target_grade,
                    )
                )

                st.divider()

                st.subheader(
                    "🎯 Target Grade Analysis"
                )

                st.write(
                    f"Target Grade: "
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
                        f"You need to average "
                        f"{required:.2f}% "
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
                        f"{required:.2f}% "
                        "which is above 100%."
                    )

        except Exception as e:

            st.error(str(e))

    # ======================================================
    # AUTO SAVE
    # ======================================================

    workspace = {
        "syllabus": syllabus_df.to_dict(
            orient="records"
        ),
        "grades": grades_df.to_dict(
            orient="records"
        ),
        "target_grade": target_grade,
    }

    if "_last_workspace" not in st.session_state:
        st.session_state._last_workspace = None

    if workspace != st.session_state._last_workspace:

        try:

            final_grade = None

            try:

                final_grade, _ = (
                    student.compute_final_grade(
                        grades_df
                    )
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

            st.session_state._last_workspace = workspace.copy()

        except Exception as e:

            st.warning(
                f"Auto Save Failed: {e}"
            )
