"""
models.py

Contains the data models used throughout the application.

These classes only STORE data.

They DO NOT perform calculations.
"""

from __future__ import annotations

from dataclasses import dataclass


# ==========================================================
# STUDENT
# ==========================================================

@dataclass(slots=True)
class Student:
    """
    Stores student information.
    """

    student_id: str
    name: str


# ==========================================================
# GRADE COMPONENT
# ==========================================================

@dataclass(slots=True)
class GradeComponent:
    """
    Represents one grading component in the syllabus.

    Example

        Component:
            Quiz 1

        Weight:
            15%

        Score:
            18/20

        Bonus:
            2

    Percentage is computed after parsing.
    """

    component: str

    weight: float

    raw_score: str = ""

    bonus: float = 0.0

    percentage: float | None = None

    completed: bool = False

    contribution: float = 0.0


# ==========================================================
# CURRENT GRADE RESULT
# ==========================================================

@dataclass(slots=True)
class GradeResult:
    """
    Result returned after computing
    the student's current grade.
    """

    current_grade: float

    remaining_weight: float

    letter_grade: str

    standing: str

    remark: str


# ==========================================================
# TARGET GRADE PROJECTION
# ==========================================================

@dataclass(slots=True)
class ProjectionResult:
    """
    Stores the result of the
    Target Grade Projection.
    """

    target_grade: float

    required_percentage: float

    maximum_possible_grade: float

    target_possible: bool

    target_already_reached: bool


# ==========================================================
# LETTER GRADE
# ==========================================================

@dataclass(slots=True)
class LetterGrade:
    """
    Represents the descriptive
    grade.

    Example

        Outstanding

        A
    """

    standing: str

    letter: str
