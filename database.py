from config import supabase


# ==========================================================
# Student Functions
# ==========================================================

def create_student(student_id, student_name):

    return (
        supabase.table("students")
        .insert(
            {
                "student_id": student_id,
                "student_name": student_name,
            }
        )
        .execute()
    )


def get_student(student_id):

    return (
        supabase.table("students")
        .select("*")
        .eq("student_id", student_id)
        .execute()
    )
