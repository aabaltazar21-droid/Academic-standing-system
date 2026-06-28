from config import supabase


def test_connection():

    response = (
        supabase
        .table("students")
        .select("*")
        .limit(1)
        .execute()
    )

    return response
