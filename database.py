from config import supabase


# ==========================================================
# STUDENT FUNCTIONS
# ==========================================================

def get_student_by_id(student_id):

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


def login_student(student_id, student_name):

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


# ==========================================================
# SUBJECT FUNCTIONS
# ==========================================================

def get_subjects(student_id):

    response = (
        supabase
        .table("subjects")
        .select("*")
        .eq("student_id", student_id)
        .order("subject_name")
        .execute()
    )

    return response.data


def create_subject(student_id, subject_name):

    return (
        supabase
        .table("subjects")
        .insert(
            {
                "student_id": student_id,
                "subject_name": subject_name,
            }
        )
        .execute()
    )


def delete_subject(subject_id):

    return (
        supabase
        .table("subjects")
        .delete()
        .eq("id", subject_id)
        .execute()
    )


def load_workspace(subject_id):

    response = (
        supabase
        .table("subjects")
        .select("workspace")
        .eq("id", subject_id)
        .single()
        .execute()
    )

    return response.data


def save_workspace(subject_id, workspace):

    return (
        supabase
        .table("subjects")
        .update(
            {
                "workspace": workspace
            }
        )
        .eq("id", subject_id)
        .execute()
    )

def get_workspace(subject_id):

    response = (
        supabase
        .table("subjects")
        .select("workspace")
        .eq("id", subject_id)
        .single()
        .execute()
    )

    if response.data:
        return response.data["workspace"]

    return None

def save_workspace(subject_id, syllabus_df, grades_df, target_grade, final_grade):

    workspace = {
        "syllabus": syllabus_df.to_dict(orient="records"),
        "grades": grades_df.to_dict(orient="records"),
        "target_grade": target_grade,
        "final_grade": final_grade
    }

    return (
        supabase
        .table("subjects")
        .update({"workspace": workspace})
        .eq("id", subject_id)
        .execute()
    )
