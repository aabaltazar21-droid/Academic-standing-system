"""
validators.py

Contains all validation logic for the application.

Nothing in this module performs calculations.

It only answers questions like:

• Is the syllabus valid?
• Are student details complete?
• Are the entered scores valid?
"""

from __future__ import annotations

from typing import Iterable

import pandas as pd

from parser import ScoreParser
from models import Student, GradeComponent


class Validator:
    """
    Collection of validation methods.
    """

    # ======================================================
    # STUDENT
    # ======================================================

    @staticmethod
    def validate_student(student: Student) -> list[str]:
        """
        Returns a list of validation errors.

        An empty list means the student data is valid.
        """

        errors: list[str] = []

        if student.student_id.strip() == "":
            errors.append("Student ID is required.")

        if student.name.strip() == "":
            errors.append("Student Name is required.")

        return errors

    # ======================================================
    # SYLLABUS
    # ======================================================

    @staticmethod
    def validate_syllabus(df: pd.DataFrame) -> list[str]:

        errors: list[str] = []

        if df.empty:
            errors.append("The syllabus is empty.")
            return errors

        # Duplicate component names
        duplicates = (
            df["Component"]
            .astype(str)
            .str.strip()
            .duplicated()
        )

        if duplicates.any():
            errors.append(
                "Duplicate component names are not allowed."
            )

        # Negative weights
        if (df["Weight (%)"] < 0).any():
            errors.append(
                "Weights cannot be negative."
            )

        total = float(df["Weight (%)"].sum())

        if abs(total - 100.0) > 0.0001:
            errors.append(
                f"Total syllabus weight must equal 100%. "
                f"(Current: {total:.2f}%)"
            )

        return errors

    # ======================================================
    # GRADE COMPONENTS
    # ======================================================

    @staticmethod
    def validate_components(
        components: Iterable[GradeComponent]
    ) -> list[str]:

        errors: list[str] = []

        for component in components:

            score = component.raw_score.strip()

            # Empty score is allowed.
            if score == "":
                continue

            if not ScoreParser.is_valid(score):

                errors.append(
                    f"Invalid score format for "
                    f"'{component.component}'."
                )

        return errors

    # ======================================================
    # TARGET GRADE
    # ======================================================

    @staticmethod
    def validate_target(
        target: float | None
    ) -> list[str]:

        errors: list[str] = []

        if target is None:
            return errors

        if target < 0:
            errors.append(
                "Target grade cannot be negative."
            )

        return errors

    # ======================================================
    # DISPLAY
    # ======================================================

    @staticmethod
    def show_errors(
        errors: list[str]
    ) -> None:
        """
        Displays validation errors
        using Streamlit.
        """

        import streamlit as st

        for error in errors:
            st.error(error)
