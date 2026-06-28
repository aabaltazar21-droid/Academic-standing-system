"""
parser.py

This module is responsible for converting user input into
usable numerical values.

Supported score formats:

    45/50
    18/20
    90
    87.5
    105/100

The parser DOES NOT perform grade calculations.

Its only responsibility is to convert text into a percentage.
"""

from __future__ import annotations

import re


class ScoreParser:
    """
    Utility class for parsing score input.

    Examples
    --------
    45/50     -> 90.0
    18/20     -> 90.0
    90        -> 90.0
    87.5      -> 87.5
    """

    # Accepts:
    #   45
    #   45.5
    #   45/50
    #   45.5/50
    _PATTERN = re.compile(
        r"""
        ^
        \s*
        (?P<earned>\d+(\.\d+)?)
        (
            \s*
            /
            \s*
            (?P<total>\d+(\.\d+)?)
        )?
        \s*
        $
        """,
        re.VERBOSE,
    )

    @classmethod
    def parse(cls, text: str) -> float | None:
        """
        Converts text into a percentage.

        Parameters
        ----------
        text : str

        Returns
        -------
        float
            Percentage

        None
            Invalid input
        """

        if text is None:
            return None

        text = text.strip()

        if text == "":
            return None

        match = cls._PATTERN.match(text)

        if not match:
            return None

        earned = float(match.group("earned"))
        total = match.group("total")

        # Percentage input
        if total is None:

            # Reject negative percentages
            if earned < 0:
                return None

            return earned

        total = float(total)

        # Division by zero
        if total <= 0:
            return None

        if earned < 0:
            return None

        return earned / total * 100

    @staticmethod
    def is_empty(text: str | None) -> bool:
        """
        Returns True if the score box is empty.
        """

        if text is None:
            return True

        return text.strip() == ""

    @classmethod
    def is_valid(cls, text: str | None) -> bool:
        """
        Returns True if the score can be parsed.
        """

        return cls.parse(text) is not None

    @classmethod
    def format_percentage(
        cls,
        percentage: float,
        decimals: int = 2,
    ) -> str:
        """
        Formats a percentage for display.

        Example

            87.5

        becomes

            87.50%
        """

        return f"{percentage:.{decimals}f}%"
