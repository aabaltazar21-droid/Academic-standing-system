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

            except ValueError:

                raise ValueError(
                    f"{component}: Invalid score format.\n\n"
                    "Accepted examples:\n"
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

        else:
            return "Needs Improvement"

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

            if str(row["Score"]).strip() == "":

                remaining_weight += float(row["Weight (%)"])

                remaining_components.append(
                    row["Component"]
                )

        if remaining_weight == 0:

            return {
                "required_average": None,
                "remaining_components": [],
                "remaining_weight": 0,
            }

        required_average = (
            (target_grade - current_grade)
            / remaining_weight
        ) * 100

        return {
            "required_average": required_average,
            "remaining_components": remaining_components,
            "remaining_weight": remaining_weight,
        }
