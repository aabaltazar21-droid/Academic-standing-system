from database import test_connection
from database import create_student, get_student
import streamlit as st
import pandas as pd


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
                percentage = 0

            else:
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
                        "Use examples like:\n"
                        "45/50\n"
                        "18/20\n"
                        "90\n"
                        "87.5"
                    )


            contribution = percentage * weight / 100

            final_grade += contribution

            breakdown.append(
                {
                    "Component": component,
                    "Score": score,
                    "Percentage": round(percentage, 2),
                    "Weight (%)": weight,
                    "Contribution": round(contribution, 2),
                }
            )

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


st.set_page_config(
    page_title="Academic Standing Status System",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 Academic Standing Status System")

if st.button("Test Database Connection"):

    try:

        result = test_connection()

        st.success("Successfully connected to Supabase!")

        st.write(result.data)

    except Exception as e:

        st.error(e)

st.write(
    "Create your own grading system or load the default syllabus."
)

st.divider()

# -----------------------------
# Student Information
# -----------------------------

student_id = st.text_input("Student ID")

student_name = st.text_input("Student Name")

st.divider()

DEFAULT_SYLLABUS = pd.DataFrame(
    {
        "Component": [
            "CO1",
            "CO2",
            "CO3",
            "Coursera",
            "Attendance",
            "Seatwork",
            "Final Exam",
        ],
        "Weight (%)": [
            15,
            15,
            10,
            10,
            5,
            15,
            30,
        ],
    }
)

if "syllabus" not in st.session_state:
    st.session_state.syllabus = DEFAULT_SYLLABUS.copy()

# ==========================================================
# SYLLABUS BUILDER
# ==========================================================

st.header("📚 Syllabus Builder")

col1, col2 = st.columns(2)

with col1:

    if st.button("📋 Load Default Syllabus", use_container_width=True):
        st.session_state.syllabus = DEFAULT_SYLLABUS.copy()
        st.rerun()

with col2:

    if st.button("🗑 Clear Syllabus", use_container_width=True):
        st.session_state.syllabus = pd.DataFrame(
            columns=[
                "Component",
                "Weight (%)"
            ]
        )
        st.rerun()

st.write(
    """
You may edit the syllabus directly.

• Add rows

• Delete rows

• Change component names

• Change weights

The total weight does NOT have to equal 100% while editing.
The report can only be generated once it reaches exactly 100%.
"""
)

syllabus_df = st.data_editor(
    st.session_state.syllabus,
    hide_index=True,
    use_container_width=True,
    num_rows="dynamic",
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
    key="editor",
)
# ============================================
# Target Grade
# ============================================

st.header("🎯 Target Grade")

st.caption(
    "Optional. Enter your desired final grade "
    "to see the average score needed on the "
    "remaining components."
)

target_grade_input = st.text_input(
    "Target Grade (%)",
    placeholder="Example: 75"
)

if target_grade_input.strip() == "":
    target_grade = None

else:

    try:

        target_grade = float(target_grade_input)

        if target_grade < 0:

            st.error("Target grade cannot be negative.")
            target_grade = None

    except ValueError:

        st.error("Target grade must be a valid number.")
        target_grade = None



# ----------------------------------------------------------
# CLEAN DATA
# ----------------------------------------------------------

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

# ----------------------------------------------------------
# VALIDATION
# ----------------------------------------------------------

duplicate_components = syllabus_df[
    "Component"
].duplicated()

if duplicate_components.any():

    st.error(
        "Duplicate component names were found.\n"
        "Each component must have a unique name."
    )

total_weight = syllabus_df["Weight (%)"].sum()

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
            f"Remaining Weight: {100-total_weight:.2f}%"
        )

    elif total_weight > 100:

        st.error(
            f"Exceeded by {total_weight-100:.2f}%"
        )

    else:

        st.success("Perfect! Total weight is exactly 100%.")

st.divider()

# ==========================================================
# GRADE ENTRY
# ==========================================================

if len(st.session_state.syllabus) > 0:

    st.header("📝 Enter Student Scores")

    st.info(
        """
The Score field accepts BOTH formats.

Examples:
• 45/50
• 18/20
• 90
• 87.5
• 105/100
"""
    )

    grades = []

    for index, row in st.session_state.syllabus.iterrows():

        component = row["Component"]
        weight = row["Weight (%)"]

        st.subheader(f"{component} ({weight:.2f}%)")


        score = st.text_input(
            "Score",
            placeholder="Examples: 45/50 or 90",
            key=f"score_{index}"
        )
        # -----------------------------
        # Live Preview
        # -----------------------------

        if score.strip() != "":

            try:

                if "/" in score:

                    earned, total = score.split("/")

                    earned = float(earned.strip())
                    total = float(total.strip())

                    if total <= 0:
                        raise Exception

                    percentage = (earned / total) * 100

                else:

                    percentage = float(score)


                contribution = percentage * weight / 100

                st.success(
                    f"Percentage: {percentage:.2f}%   |   "
                    f"Contribution: {contribution:.2f}"
                )

            except:

                st.error(
                    "Invalid score. Examples:\n"
                    "45/50\n"
                    "18/20\n"
                    "90"
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

else:

    grades_df = pd.DataFrame()

    st.info("Please create your syllabus first.")

# ==========================================================
# ACADEMIC REPORT
# ==========================================================


st.header("📊 Academic Report")

can_generate = True

# Validate syllabus
if len(st.session_state.syllabus) == 0:
    can_generate = False

total_weight = st.session_state.syllabus["Weight (%)"].sum()

if total_weight != 100:
    can_generate = False

if st.button(
    "Generate Academic Report",
    use_container_width=True,
    disabled=not can_generate,
):

    try:

        student = Student(student_id, student_name)

        final_grade, breakdown = student.compute_final_grade(
            grades_df
        )

        standing = student.get_result(final_grade)

        remark = None

        if target_grade is not None:

            remark = (
                "PASSED"
                if final_grade >= target_grade
                else "FAILED"
            )

        # ============================================
        # 🎯 Target Grade Analysis
        # ============================================

        required_average = None
        remaining_weight = 0
        remaining_components = []

        if target_grade is not None:

            for _, row in grades_df.iterrows():

                score = str(row["Score"]).strip()

                if score == "":

                    remaining_weight += float(row["Weight (%)"])
                    remaining_components.append(
                        str(row["Component"])
                    )

            if remaining_weight > 0:

                points_needed = target_grade - final_grade

                required_average = (
                    points_needed / remaining_weight
                ) * 100

#====================================================================================



        st.success("Academic Report Generated!")

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
    f"**Student ID:** "
    f"{student.student_id if student.student_id.strip() else 'Not Provided'}"
)

            st.write(
                f"**Student Name:** "
                f"{student.name if student.name.strip() else 'Not Provided'}"
            )
           
            st.write(f"**Academic Standing:** {standing}")

            if remark is not None:

                if remark == "PASSED":
                    st.success(remark)
                else:
                    st.error(remark)

        st.divider()

        st.subheader("Grade Breakdown")

        st.dataframe(
            breakdown,
            use_container_width=True,
            hide_index=True,
        )


        # ============================================
        # 🎯 Target Grade Analysis Report
        # ============================================

        if target_grade is not None:

            st.divider()

            st.subheader("🎯 Target Grade Analysis")

            st.write(f"**Target Grade:** {target_grade:.2f}%")

            if required_average is None:

                st.info(
                    "There are no remaining components."
                )

            elif required_average <= 0:

                st.success(
                    "🎉 Your current grade already meets or exceeds your target."
                )

            elif required_average <= 100:

                st.info(
                    f"You need to average **{required_average:.2f}%** "
                    "on all remaining components."
                )

                st.write("Remaining components:")

                for component in remaining_components:

                    st.write(f"• {component}")

            else:

                st.error(
                    f"You would need an average of **{required_average:.2f}%**, "
                    "which is above 100%."
                )

                st.warning(
                    "Even perfect scores are not enough. "
                    "You would need additional bonus points or "
                    "special consideration to reach your target."
                )
    

    except Exception as e:

        st.error(str(e))
