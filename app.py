import streamlit as st


class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name

    def compute_final_grade(
        self,
        co1,
        co2,
        co3,
        coursera,
        attendance,
        seatwork,
        final_exam
    ):
        return (
            co1 * 0.15 +
            co2 * 0.15 +
            co3 * 0.10 +
            coursera * 0.10 +
            attendance * 0.05 +
            seatwork * 0.15 +
            final_exam * 0.30
        )


st.set_page_config(
    page_title="Academic Standing Status System",
    page_icon="🎓"
)

st.title("🎓 Academic Standing Status System")

st.subheader("Student Information")

student_id = st.text_input("Student ID")
student_name = st.text_input("Student Name")

st.subheader("Syllabus Breakdown")

co1 = st.number_input("CO1 (15%)", 0.0, 100.0)
co2 = st.number_input("CO2 (15%)", 0.0, 100.0)
co3 = st.number_input("CO3 (10%)", 0.0, 100.0)
coursera = st.number_input("Coursera (10%)", 0.0, 100.0)
attendance = st.number_input("Attendance / Recitation (5%)", 0.0, 100.0)
seatwork = st.number_input("Seatwork / Homework (15%)", 0.0, 100.0)
final_exam = st.number_input("Final Exam (30%)", 0.0, 100.0)

if st.button("Generate Academic Report"):

    student = Student(student_id, student_name)

    final_grade = student.compute_final_grade(
        co1,
        co2,
        co3,
        coursera,
        attendance,
        seatwork,
        final_exam
    )

    if final_grade >= 90:
        standing = "Outstanding"
        letter = "A"
    elif final_grade >= 85:
        standing = "Very Satisfactory"
        letter = "B"
    elif final_grade >= 80:
        standing = "Satisfactory"
        letter = "C"
    elif final_grade >= 75:
        standing = "Passing"
        letter = "D"
    else:
        standing = "Needs Improvement"
        letter = "F"

    remark = "PASSED" if final_grade >= 75 else "FAILED"

    st.header("Academic Report")

    st.write("Student ID:", student.student_id)
    st.write("Student Name:", student.name)

    st.write(f"Final Grade: {final_grade:.2f}")
    st.write(f"Letter Grade: {letter}")
    st.write(f"Academic Standing: {standing}")
    st.write(f"Remark: {remark}")
