"""
constants.py

This module stores application-wide constants.

Keeping constants in one place makes the program easier to
maintain. If the syllabus changes later, you only need to
edit this file instead of searching the entire project.
"""

from __future__ import annotations

import pandas as pd

# ----------------------------------------------------------
# DEFAULT SYLLABUS
# ----------------------------------------------------------

DEFAULT_SYLLABUS = pd.DataFrame(
    {
        "Component": [
            "CO1",
            "CO2",
            "CO3",
            "Coursera",
            "Attendance",
            "Seatwork",
            "Final Exam",
        ],
        "Weight (%)": [
            15.0,
            15.0,
            10.0,
            10.0,
            5.0,
            15.0,
            30.0,
        ],
    }
)

# ----------------------------------------------------------
# LETTER GRADE BOUNDARIES
# ----------------------------------------------------------

GRADE_SCALE = [
    (90.0, "Outstanding", "A"),
    (85.0, "Very Satisfactory", "B"),
    (80.0, "Satisfactory", "C"),
    (75.0, "Passing", "D"),
    (0.0, "Needs Improvement", "F"),
]

# ----------------------------------------------------------
# DEFAULT TARGET GRADE
# ----------------------------------------------------------

DEFAULT_TARGET_GRADE = 75.0

# ----------------------------------------------------------
# INPUT EXAMPLES
# ----------------------------------------------------------

SCORE_EXAMPLES = [
    "45/50",
    "18/20",
    "90",
    "87.5",
    "105/100",
]

# ----------------------------------------------------------
# UI STRINGS
# ----------------------------------------------------------

APP_TITLE = "🎓 Academic Standing Status System"

APP_DESCRIPTION = (
    "Calculate your current grade, customize the syllabus, "
    "and project the scores needed to reach your target grade."
)
