import pandas as pd


class Student:

    def __init__(self, student_id="", student_name=""):

        self.student_id = student_id
        self.student_name = student_name

    # ======================================================
    # COMPUTE FINAL GRADE
    # ======================================================

    def compute_final_grade(self, grades_df):

        final_grade = 0
        breakdown = []

        for _, row in grades_df.iterrows():

            component = str(row["Component"]).strip()
            weight = float(row["Weight (%)"])
            score = str(row["Score"]).strip()

            if score == "":
                continue

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

            except:

                raise ValueError(
                    f"{component}: Invalid score format.\n\n"
                    "Examples:\n"
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
                    "Weight (%)": weight,
                    "Score": score,
                    "Percentage": round(percentage, 2),
                    "Contribution": round(contribution, 2),
                }
            )

        return final_grade, pd.DataFrame(breakdown)

    # ======================================================
    # STANDING
    # ======================================================

    def get_academic_standing(self, grade):

        if grade >= 90:
            return "Outstanding"

        elif grade >= 85:
            return "Very Satisfactory"

        elif grade >= 80:
            return "Satisfactory"

        elif grade >= 75:
            return "Passing"

        return "Needs Improvement"

    # ======================================================
    # PASS / FAIL
    # ======================================================

    def get_remark(self, final_grade, passing_grade):

        if passing_grade is None:
            return None

        if final_grade >= passing_grade:
            return "PASSED"

        return "FAILED"

    # ======================================================
    # TARGET ANALYSIS
    # ======================================================

    def target_analysis(
        self,
        grades_df,
        current_grade,
        target_grade,
    ):

        remaining_weight = 0
        remaining_components = []

        for _, row in grades_df.iterrows():

            score = str(row["Score"]).strip()

            if score == "":

                remaining_weight += float(row["Weight (%)"])

                remaining_components.append(
                    row["Component"]
                )

        if remaining_weight == 0:

            return {
                "required_average": None,
                "remaining_weight": 0,
                "remaining_components": [],
            }

        required_average = (
            (target_grade - current_grade)
            / remaining_weight
        ) * 100

        return {
            "required_average": required_average,
            "remaining_weight": remaining_weight,
            "remaining_components": remaining_components,
        }

    # ======================================================
    # VALIDATE WEIGHTS
    # ======================================================

    def validate_weights(self, syllabus_df):

        total = syllabus_df["Weight (%)"].sum()

        return abs(total - 100) < 0.0001

    # ======================================================
    # TOTAL WEIGHT
    # ======================================================

    def total_weight(self, syllabus_df):

        return float(
            syllabus_df["Weight (%)"].sum()
        )
