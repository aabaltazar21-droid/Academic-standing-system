from config import supabase


def get_student(student_id, student_name):

    response = (
        supabase
        .table("students")
        .select("*")
        .eq("student_id", student_id)
        .eq("student_name", student_name)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None
    
    response = (
        supabase
        .table("students")
        .select("*")
        .eq("student_id", student_id)
        .execute()
    )

    if response.data:
        return response.data[0]

    return None


def create_student(student_id, student_name):

    return (
        supabase
        .table("students")
        .insert(
            {
                "student_id": student_id,
                "student_name": student_name,
            }
        )
        .execute()
    )
