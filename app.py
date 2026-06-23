class Student:
    def __init__(self, student_id, name):
        self.student_id = student_id
        self.name = name
 
    def compute_final_grade(self, co1, co2, co3, coursera, attendance, seatwork, final_exam):
        return (
            co1 * 0.15 +
            co2 * 0.15 +
            co3 * 0.10 +
            coursera * 0.10 +
            attendance * 0.05 +
            seatwork * 0.15 +
            final_exam * 0.30
        )
 
 
# STDIN INPUT
student_id = input()
student_name = input()
 
co1 = float(input())
co2 = float(input())
co3 = float(input())
coursera = float(input())
attendance = float(input())
seatwork = float(input())
final_exam = float(input())
 
student = Student(student_id, student_name)
 
final_grade = student.compute_final_grade(
    co1, co2, co3, coursera, attendance, seatwork, final_exam
)
 
# Academic Standing
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
 
 
# OUTPUT
 
print("      ACADEMIC STANDING STATUS SYSTEM")
 
print("Student ID   :", student.student_id)
print("Student Name :", student.name)
 
print("\n        SYLLABUS BREAKDOWN")
print("CO1 (15%)                 :", co1)
print("CO2 (15%)                 :", co2)
print("CO3 (10%)                 :", co3)
print("Coursera (10%)            :", coursera)
print("Attendance/Recitation (5%):", attendance)
print("Seatwork/Homework (15%)   :", seatwork)
print("Final Exam (30%)          :", final_exam)
 
 
print()
print("             ACADEMIC REPORT")
 
print(f"Final Grade         : {final_grade:.2f}")
print(f"Letter Grade        : {letter}")
print(f"Academic Standing   : {standing}")
print(f"Remark              : {remark}")
 
