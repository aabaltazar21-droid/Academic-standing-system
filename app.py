import streamlit as st


class Student:

    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

    def compute_final_grade(self, components):

        final_grade = 0

        for component in components:

            try:
                earned, total = component["fraction"].split("/")

                earned = float(earned.strip())
                total = float(total.strip())

                percentage = (earned / total) * 100

                percentage += component["bonus"]

                contribution = percentage * component["weight"] / 100

                final_grade += contribution

            except:
                pass

        return final_grade

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
    layout="wide"
)

st.title("🎓 Academic Standing Status System")
st.write("Customize your syllabus, enter scores as fractions (ex. 45/50), then generate an academic report.")

# ---------------------------------------------------
# Student Information
# ---------------------------------------------------

st.header("Student Information")

student_id = st.text_input("Student ID")

student_name = st.text_input("Student Name")

# ---------------------------------------------------
# Session State
# ---------------------------------------------------

if "components" not in st.session_state:
    st.session_state.components = []

# ---------------------------------------------------
# Syllabus Builder
# ---------------------------------------------------

st.header("Syllabus Breakdown")

col1, col2 = st.columns(2)

with col1:
    if st.button("📋 Load Default Syllabus"):
        st.session_state.components = [
            {"name": "CO1", "weight": 15},
            {"name": "CO2", "weight": 15},
            {"name": "CO3", "weight": 10},
            {"name": "Coursera", "weight": 10},
            {"name": "Attendance / Recitation", "weight": 5},
            {"name": "Seatwork / Homework", "weight": 15},
            {"name": "Final Exam", "weight": 30},
        ]

with col2:
    if st.button("🗑 Clear Syllabus"):
        st.session_state.components = []

st.subheader("Add a Custom Component")

col1, col2 = st.columns([3, 1])

with col1:
    component_name = st.text_input(
        "Component Name",
        placeholder="Example: Quiz 1"
    )

with col2:
    component_weight = st.number_input(
        "Weight (%)",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=1.0
    )

if st.button("➕ Add Component"):

    if component_name.strip() == "":
        st.warning("Please enter a component name.")

    else:

        duplicate = False

        for c in st.session_state.components:
            if c["name"].lower() == component_name.lower():
                duplicate = True
                break

        if duplicate:
            st.warning("That component already exists.")

        else:
            st.session_state.components.append(
                {
                    "name": component_name,
                    "weight": component_weight
                }
            )

# ---------------------------------------------------
# Display Current Components
# ---------------------------------------------------

if len(st.session_state.components) > 0:

    st.subheader("Current Syllabus")

    total_weight = 0

    for i, component in enumerate(st.session_state.components, start=1):

        st.write(
            f"{i}. **{component['name']}** — {component['weight']}%"
        )

        total_weight += component["weight"]

    st.write(f"### Total Weight: **{total_weight:.1f}%**")

    if total_weight == 100:
        st.success("✔ Total weight equals 100%")

    elif total_weight < 100:
        st.warning(f"Add {100-total_weight:.1f}% more.")

    else:
        st.error(f"Remove {total_weight-100:.1f}%.")

else:

    st.info("Load the default syllabus or create your own components.")

# ---------------------------------------------------
# Enter Grades
# ---------------------------------------------------

if len(st.session_state.components) > 0 and total_weight == 100:

    st.header("Enter Grades")

    st.info(
        "Enter scores in the format Earned/Total (Example: 45/50 or 95/100).\n"
        "Additional Points are added after converting the fraction to a percentage."
    )

    for component in st.session_state.components:

        st.subheader(component["name"])

        col1, col2 = st.columns([3, 1])

        with col1:

            component["fraction"] = st.text_input(
                f'{component["name"]} Score',
                placeholder="Example: 45/50",
                key=f"fraction_{component['name']}"
            )

        with col2:

            component["bonus"] = st.number_input(
                "Additional Points",
                value=0.0,
                step=0.5,
                key=f"bonus_{component['name']}"
            )

        # Live Preview
        if component["fraction"] != "":

            try:

                earned, total = component["fraction"].split("/")

                earned = float(earned.strip())
                total = float(total.strip())

                if total <= 0:
                    st.error("Total score must be greater than zero.")
                else:

                    percentage = (earned / total) * 100
                    percentage += component["bonus"]

                    weighted = percentage * component["weight"] / 100

                    st.success(
                        f"Percentage: {percentage:.2f}%   |   "
                        f"Weighted Contribution: {weighted:.2f}"
                    )

            except:

                st.error("Please use the format: Earned/Total (Example: 45/50)")

# ---------------------------------------------------
# Generate Academic Report
# ---------------------------------------------------

    st.divider()

    if st.button("📄 Generate Academic Report"):

        if student_id.strip() == "" or student_name.strip() == "":
            st.error("Please enter both the Student ID and Student Name.")

        else:

            valid = True

            # Validate all fraction inputs
            for component in st.session_state.components:

                try:
                    earned, total = component["fraction"].split("/")

                    earned = float(earned.strip())
                    total = float(total.strip())

                    if total <= 0:
                        valid = False

                except:
                    valid = False

            if not valid:

                st.error(
                    "One or more scores are invalid.\n\n"
                    "Please use the format: Earned/Total\n\n"
                    "Examples:\n"
                    "- 45/50\n"
                    "- 18/20\n"
                    "- 95/100"
                )

            else:

                student = Student(student_id, student_name)

                final_grade = student.compute_final_grade(
                    st.session_state.components
                )

                standing, letter = student.get_result(final_grade)

                remark = (
                    "PASSED"
                    if final_grade >= 75
                    else "FAILED"
                )

                st.divider()

                st.header("📋 Academic Report")

                st.metric(
                    "Final Grade",
                    f"{final_grade:.2f}"
                )

                if remark == "PASSED":
                    st.success("PASSED")
                else:
                    st.error("FAILED")

                st.write(f"**Student ID:** {student.student_id}")
                st.write(f"**Student Name:** {student.name}")

                st.write(f"**Letter Grade:** {letter}")
                st.write(f"**Academic Standing:** {standing}")

                st.divider()

                st.subheader("Detailed Computation")

                for component in st.session_state.components:

                    earned, total = component["fraction"].split("/")

                    earned = float(earned.strip())
                    total = float(total.strip())

                    percentage = (
                        earned / total
                    ) * 100

                    percentage += component["bonus"]

                    contribution = (
                        percentage *
                        component["weight"] /
                        100
                    )

                    st.write(
                        f"**{component['name']}**"
                    )

                    st.write(
                        f"Score: {earned}/{total}"
                    )

                    st.write(
                        f"Bonus: {component['bonus']:.2f}"
                    )

                    st.write(
                        f"Percentage: {percentage:.2f}%"
                    )

                    st.write(
                        f"Weight: {component['weight']}%"
                    )

                    st.write(
                        f"Contribution: {contribution:.2f}"
                    )

                    st.divider()

                st.subheader("Detailed Computation")

                for component in st.session_state.components:

                    earned, total = component["fraction"].split("/")

                    earned = float(earned.strip())
                    total = float(total.strip())

                    raw_percentage = (earned / total) * 100

                    final_percentage = raw_percentage + component["bonus"]

                    contribution = (
                        final_percentage *
                        component["weight"] / 100
                    )

                    with st.expander(component["name"], expanded=True):

                        st.write(
                            f"**Raw Score:** {earned}/{total}"
                        )

                        st.write(
                            f"**Raw Percentage:** {raw_percentage:.2f}%"
                        )

                        st.write(
                            f"**Bonus Points:** {component['bonus']:.2f}"
                        )

                        st.write(
                            f"**Final Percentage:** {final_percentage:.2f}%"
                        )

                        st.write(
                            f"**Weight:** {component['weight']}%"
                        )

                        st.write(
                            f"**Weighted Contribution:** {contribution:.2f}"
                        )

                st.success("Academic report generated successfully!")
