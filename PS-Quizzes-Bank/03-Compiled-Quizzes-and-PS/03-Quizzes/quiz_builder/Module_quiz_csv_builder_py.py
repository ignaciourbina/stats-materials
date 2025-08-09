# -*- coding: utf-8 -*-
"""
Created on Mon Apr 28 12:48:20 2025

@author: Ignacio
"""

"""
Quiz CSV Builder for D2L Brightspace
===================================

This module lets you create any of the seven Brightspace‑supported
question types programmatically, add them to a bank, and then export the
whole set to a **CSV UTF‑8** file that is ready to import with the “Bulk
question upload” tool (Add/Edit Questions → Import → Upload a File).

It follows the exact column order/structure used in D2L’s sample
`Sample_Question_Import_UTF8.csv` so the resulting file is accepted
without manual tweaking.

Usage example
-------------
>>> bank = QuestionBank()
>>> q1 = WrittenResponse(
...     title="Short essay on oxidation",
...     question_text="Explain what happens during oxidation.",
...     points=3,
...     answer_key="Look for transfer of electrons",
... )
>>> bank.add(q1)
>>> q2 = MultipleChoice(
...     title="Boiling point of water",
...     question_text="What is the normal boiling point of water?",
...     options=[
...         MCOption("100 °C", 100),
...         MCOption("212 °F", 100),  # Accept either unit
...         MCOption("90 °C", 0),
...         MCOption("273 K", 0),
...     ],
... )
>>> bank.add(q2)
>>> bank.export_csv("my_quiz.csv")
"""

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

# Constant for blank columns in CSV rows
BLANK4 = ["", "", "", ""]


@dataclass
class Question:
    """Common scaffolding for all Brightspace question types."""

    new_question_code: str = field(init=False, default="")
    title: str
    question_text: str
    points: int = 1
    difficulty: Optional[int] = None
    image: Optional[str] = None
    hint: Optional[str] = None
    feedback: Optional[str] = None
    explicit_id: Optional[str] = None
    html_used: bool = False  # ← NEW: flag for HTML stems

    # ------------------------------- helpers --------------------------------
    def _type_rows(self) -> List[List[str]]:
        raise NotImplementedError("_type_rows must be implemented by subclasses")

    def _pad(self, row: List[str], width: int = 6) -> List[str]:
        """Return `row` extended with empty strings up to `width` columns."""
        return row + [""] * (width - len(row))

    # ------------------------------ exporter --------------------------------
    def to_rows(self) -> List[List[str]]:
        rows: List[List[str]] = []

        # 0. NewQuestion marker
        rows.append(self._pad(["NewQuestion", self.new_question_code]))

        # 1. Optional fixed ID
        if self.explicit_id:
            rows.append(self._pad(["ID", self.explicit_id]))

        # 2. Title
        rows.append(self._pad(["Title", self.title]))

        # 3. QuestionText  (column-C holds “HTML” when html_used=True)
        qt_row = ["QuestionText", self.question_text, "HTML" if self.html_used else ""]
        rows.append(self._pad(qt_row))

        # 4. Points
        rows.append(self._pad(["Points", str(self.points)]))

        # 5. Optional extras
        if self.difficulty is not None:
            rows.append(self._pad(["Difficulty", str(self.difficulty)]))
        if self.image:
            rows.append(self._pad(["Image", self.image]))

        # 6. Type-specific rows (override hook)
        rows.extend(self._type_rows())

        # 7. Hint / feedback
        if self.hint:
            rows.append(self._pad(["Hint", self.hint]))
        if self.feedback:
            rows.append(self._pad(["Feedback", self.feedback]))

        # 8. Blank spacer (exactly six empty cells)
        rows.append([""] * 6)
        return rows


@dataclass
class WrittenResponse(Question):
    """Written Response (WR) question type."""

    initial_text: Optional[str] = None  # Pre-filled text in the response box
    answer_key: Optional[str] = None  # Answer key for manual grading reference

    def __post_init__(self):
        """Sets the question type code after initialization."""
        self.new_question_code = "WR"

    def _type_rows(self):
        """Generates CSV rows specific to Written Response questions."""
        rows = []
        if self.initial_text is not None:
            rows.append(["InitialText", self.initial_text, *BLANK4])
        if self.answer_key is not None:
            rows.append(["AnswerKey", self.answer_key, *BLANK4])
        return rows


@dataclass
class ShortAnswer(Question):
    """Short Answer (SA) question type."""

    best_answer: str = ""  # The primary correct answer
    regexp: bool = False  # Use regular expression matching for the answer
    case_sensitive: bool = False  # Require case-sensitive matching
    rows: int = 1  # Number of rows for the input box
    cols: int = 40  # Number of columns for the input box

    def __post_init__(self):
        """Validates required fields and sets the question type code."""
        if not self.best_answer:
            raise ValueError("best_answer is required for ShortAnswer questions")
        self.new_question_code = "SA"

    def _type_rows(self):
        """Generates CSV rows specific to Short Answer questions."""
        # Determine the flag based on regexp and case sensitivity
        flag = (
            "regexp"
            if self.regexp
            else ("sensitive" if self.case_sensitive else "insensitive")
        )
        return [
            [
                "InputBox",
                str(self.rows),
                str(self.cols),
                "",
                "",
            ],  # Defines the input box size
            [
                "Answer",
                "100",
                self.best_answer,
                flag,
                "",
            ],  # Defines the correct answer and matching flags (100% weight)
        ]


@dataclass
class MatchingPair:
    """Represents a single choice-match pair for Matching questions."""

    choice_no: int  # Unique number identifying the choice
    choice_text: str  # Text displayed for the choice
    match_text: str  # Text displayed for the corresponding match


@dataclass
class Matching(Question):
    """Matching (M) question type."""

    pairs: List[MatchingPair] = field(
        default_factory=list
    )  # List of choice-match pairs
    scoring: str = (
        "AllOrNothing"  # Scoring method ("AllOrNothing", "RightMinusWrong", "EquallyWeighted")
    )

    def __post_init__(self):
        """Sets the question type code."""
        self.new_question_code = "M"

    def _type_rows(self):
        """Generates CSV rows specific to Matching questions."""
        rows = [["Scoring", self.scoring, *BLANK4]]  # Add scoring method row
        # Add rows for each choice text
        for p in self.pairs:
            rows.append(["Choice", str(p.choice_no), p.choice_text, "", ""])
        # Add rows for each match text
        for p in self.pairs:
            rows.append(["Match", str(p.choice_no), p.match_text, "", ""])
        return rows


@dataclass
class MCOption:
    """Represents a single option for Multiple Choice questions."""

    text: str  # Text of the option
    percent: int  # Percentage points awarded if this option is chosen (100 for correct, 0 for incorrect)
    feedback: Optional[str] = None  # Feedback specific to this option
    html_used: bool = False  # Indicates if the option text uses HTML

    def to_row(self):
        """Generates the CSV row for this option."""
        # Determine flags based on HTML usage
        html_flag = "HTML" if self.html_used else ""
        fb_flag = "HTML" if self.feedback and self.html_used else ""
        # Ensure 6 columns are returned
        return [
            "Option",
            str(self.percent),
            self.text,
            html_flag,
            self.feedback or "",
            fb_flag,
        ]


@dataclass
class MultipleChoice(Question):
    """Multiple Choice (MC) question type."""

    options: List[MCOption] = field(default_factory=list)  # List of options

    def __post_init__(self):
        """Sets the question type code."""
        self.new_question_code = "MC"

    def _type_rows(self):
        """Generates CSV rows for each option."""
        return [o.to_row() for o in self.options]


@dataclass
class TFOption:
    """Represents either the True or False row for True/False questions."""

    is_true: bool  # True if this represents the "True" answer, False otherwise
    credit: int  # Percentage credit (usually 100 for the correct one, 0 for incorrect)
    feedback: Optional[str] = None  # Feedback specific to choosing True/False

    def to_row(self):
        """Generates the CSV row for this True/False option."""
        # Ensure 6 columns are returned
        return [
            "True" if self.is_true else "False",
            str(self.credit),
            self.feedback or "",
            "",
            "",
            "",
        ]  # Added two blank strings


@dataclass
class TrueFalse(Question):
    """True/False (TF) question type."""

    true_row: Optional[TFOption] = None  # Represents the "True" choice configuration
    false_row: Optional[TFOption] = None  # Represents the "False" choice configuration

    def __post_init__(self):
        """Validates inputs and sets the question type code."""
        # Basic validation
        if self.true_row is None or self.false_row is None:
            raise ValueError(
                "true_row and false_row must both be provided for TrueFalse questions"
            )
        if not self.true_row.is_true:
            raise ValueError("true_row must have is_true=True")
        if self.false_row.is_true:
            raise ValueError("false_row must have is_true=False")

        # Set the question type code
        self.new_question_code = "TF"

    def _type_rows(self):
        """Generates CSV rows for True and False options."""
        # True row first, then False row
        return [self.true_row.to_row(), self.false_row.to_row()]


@dataclass
class MSOption:
    """Represents a single option for Multi-Select questions."""

    text: str  # Text of the option
    correct: bool  # True if this option is part of the correct answer set
    feedback: Optional[str] = None  # Feedback specific to this option
    html_used: bool = False  # Indicates if the option text uses HTML

    def to_row(self):
        """Generates the CSV row for this option."""
        html_flag = "HTML" if self.html_used else ""
        fb_flag = "HTML" if self.feedback and self.html_used else ""
        # Ensure 6 columns are returned
        return [
            "Option",
            "100" if self.correct else "0",
            self.text,
            html_flag,
            self.feedback or "",
            fb_flag,
        ]  # Changed "1"/"0" to "100"/"0" for clarity


@dataclass
class MultiSelect(Question):
    """Multi-Select (MS) question type."""

    options: List[MSOption] = field(default_factory=list)  # List of options
    scoring: str = (
        "AllOrNothing"  # Scoring method ("AllOrNothing", "RightMinusWrong", "RightOnly")
    )

    def __post_init__(self):
        """Sets the question type code."""
        self.new_question_code = "MS"

    def _type_rows(self):
        """Generates CSV rows for scoring and each option."""
        rows = [["Scoring", self.scoring, *BLANK4]]  # Add scoring method row
        rows.extend(o.to_row() for o in self.options)  # Add rows for each option
        return rows


@dataclass
class OrderingItem:
    """Represents a single item to be ordered in Ordering questions."""

    text: str  # Text of the item
    feedback: Optional[str] = (
        None  # Feedback specific to this item's position (rarely used)
    )
    html_used: bool = False  # Indicates if the item text uses HTML

    def to_row(self):
        """Generates the CSV row for this item."""
        html_flag = "HTML" if self.html_used else ""
        fb_flag = "HTML" if self.feedback and self.html_used else ""
        # Ensure 6 columns are returned
        return [
            "Item",
            self.text,
            html_flag,
            self.feedback or "",
            "",
            "",
        ]  # Added two blank strings


@dataclass
class Ordering(Question):
    """Ordering (O) question type."""

    items: List[OrderingItem] = field(
        default_factory=list
    )  # List of items in the correct order
    scoring: str = (
        "AllOrNothing"  # Scoring method ("AllOrNothing", "RightMinusWrong", "EquallyWeighted")
    )

    def __post_init__(self):
        """Sets the question type code."""
        self.new_question_code = "O"

    def _type_rows(self):
        """Generates CSV rows for scoring and each item."""
        rows = [["Scoring", self.scoring, *BLANK4]]  # Add scoring method row
        rows.extend(
            i.to_row() for i in self.items
        )  # Add rows for each item (in correct order)
        return rows


class QuestionBank:
    """Manages a collection of questions and exports them to CSV."""

    def __init__(self):
        """Initializes an empty question bank."""
        self._questions: List[Question] = []

    def add(self, *questions: Question):
        """Adds one or more questions to the bank."""
        self._questions.extend(questions)

    def export_csv(self, path: str | Path, encoding: str = "utf-8-sig") -> Path:
        """
        Exports all questions in the bank to a CSV file compatible with
        D2L Brightspace bulk question import.

        Args:
            path: The file path (string or Path object) where the CSV will be saved.
            encoding: The file encoding to use (defaults to 'utf-8-sig' which includes BOM,
                      often needed by Excel/Brightspace).

        Returns:
            The resolved Path object of the created CSV file.
        """
        p = Path(path).expanduser().resolve()
        # Create parent directories if they don't exist
        p.parent.mkdir(parents=True, exist_ok=True)

        # Open the file and write CSV data
        with p.open("w", newline="", encoding=encoding) as f:
            # Use csv.writer for proper CSV formatting (quoting, delimiters)
            w = csv.writer(f)
            # Iterate through each question and write its rows
            for q in self._questions:
                w.writerows(q.to_rows())
        return p

    def __iter__(self):
        """Allows iterating over the questions in the bank."""
        return iter(self._questions)

    def __len__(self):
        """Returns the number of questions in the bank."""
        return len(self._questions)
