import streamlit as st


class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

    def compute_final_grade(self, components):
        total = 0
        for component in components:
            total += component["grade"] * component["weight"] / 100
        return total

    def get_result(self, grade):
        if grade >= 90:
            return "Outstanding", "A"
        elif grade >= 85:
            return "Very Satisfactory", "B"
        elif grade >= 80:
            return "Satisfactory", "C"
        elif grade >= 75:
            return "Passing", "D"
        else:
            return "Needs Improvement", "F"


st.set_page_config(
    page_title="Academic Standing Status System",
    page_icon="🎓",
)

st.title("🎓 Academic Standing Status System")

# -------------------------------
# Student Information
# -------------------------------

st.header("Student Information")

student_id = st.text_input("Student ID")
student_name = st.text_input("Student Name")

# -------------------------------
# Initialize Session State
# -------------------------------

if "components" not in st.session_state:
    st.session_state.components = []

# -------------------------------
# Default Syllabus
# -------------------------------

st.header("Syllabus Breakdown")

col1, col2 = st.columns(2)

with col1:
    if st.button("Load Default Syllabus"):
        st.session_state.components = [
            {"name": "CO1", "weight": 15},
            {"name": "CO2", "weight": 15},
            {"name": "CO3", "weight": 10},
            {"name": "Coursera", "weight": 10},
            {"name": "Attendance", "weight": 5},
            {"name": "Seatwork", "weight": 15},
            {"name": "Final Exam", "weight": 30},
        ]

with col2:
    if st.button("Clear Syllabus"):
        st.session_state.components = []

st.subheader("Create Your Own Component")

new_name = st.text_input("Component Name")

new_weight = st.number_input(
    "Weight (%)",
    min_value=0.0,
    max_value=100.0,
    value=0.0,
)

if st.button("Add Component"):
    if new_name.strip() == "":
        st.warning("Please enter a component name.")
    else:
        st.session_state.components.append(
            {
                "name": new_name,
                "weight": new_weight,
            }
        )

# -------------------------------
# Input Grades
# -------------------------------

if len(st.session_state.components) > 0:

    st.header("Enter Grades")

    total_weight = 0

    for component in st.session_state.components:

        component["grade"] = st.number_input(
            f'{component["name"]} ({component["weight"]}%)',
            min_value=0.0,
            max_value=100.0,
            value=0.0,
            key=component["name"],
        )

        total_weight += component["weight"]

    st.write(f"**Total Weight:** {total_weight:.1f}%")

    if total_weight != 100:
        st.error("The total weight must equal 100%.")

    if st.button("Generate Academic Report"):

        if student_id == "" or student_name == "":
            st.error("Please enter Student ID and Student Name.")

        elif total_weight != 100:
            st.error("Weights must total exactly 100%.")

        else:

            student = Student(student_id, student_name)

            final_grade = student.compute_final_grade(
                st.session_state.components
            )

            standing, letter = student.get_result(final_grade)

            remark = "PASSED" if final_grade >= 75 else "FAILED"

            st.divider()

            st.header("Academic Report")

            st.success("Report Generated Successfully!")

            st.write(f"**Student ID:** {student.student_id}")
            st.write(f"**Student Name:** {student.name}")

            st.metric("Final Grade", f"{final_grade:.2f}")

            st.write(f"**Letter Grade:** {letter}")
            st.write(f"**Academic Standing:** {standing}")

            if remark == "PASSED":
                st.success("PASSED")
            else:
                st.error("FAILED")

            st.subheader("Grade Breakdown")

            for component in st.session_state.components:
                st.write(
                    f'{component["name"]}: '
                    f'{component["grade"]:.2f} '
                    f'({component["weight"]}%)'
                )

else:
    st.info("Load the default syllabus or add your own grading components to begin.")
