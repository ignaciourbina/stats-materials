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

After running the above you will have a **my_quiz.csv** file you can
upload straight into Brightspace.
"""

"""
Quiz CSV Builder for D2L Brightspace
(… same header …)
"""
import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

BLANK4 = ["", "", "", ""]


@dataclass
class Question:
    new_question_code: str = field(init=False, default="")
    title: str
    question_text: str
    points: int = 1
    difficulty: Optional[int] = None
    image: Optional[str] = None
    hint: Optional[str] = None
    feedback: Optional[str] = None
    explicit_id: Optional[str] = None

    def _type_rows(self) -> List[List[str]]:
        raise NotImplementedError

    def to_rows(self) -> List[List[str]]:
        rows = [["NewQuestion", self.new_question_code, *BLANK4]]
        if self.explicit_id:
            rows.append(["ID", self.explicit_id, *BLANK4])
        rows += [
            ["Title", self.title, *BLANK4],
            ["QuestionText", self.question_text, *BLANK4],
            ["Points", str(self.points), *BLANK4],
        ]
        if self.difficulty is not None:
            rows.append(["Difficulty", str(self.difficulty), *BLANK4])
        if self.image:
            rows.append(["Image", self.image, *BLANK4])
        rows.extend(self._type_rows())
        if self.hint:
            rows.append(["Hint", self.hint, *BLANK4])
        if self.feedback:
            rows.append(["Feedback", self.feedback, *BLANK4])
        rows.append(["", "", "", "", ""])
        return rows


@dataclass
class WrittenResponse(Question):
    initial_text: Optional[str] = None
    answer_key: Optional[str] = None

    def __post_init__(self):
        self.new_question_code = "WR"

    def _type_rows(self):
        rows = []
        if self.initial_text is not None:
            rows.append(["InitialText", self.initial_text, *BLANK4])
        if self.answer_key is not None:
            rows.append(["AnswerKey", self.answer_key, *BLANK4])
        return rows


@dataclass
class ShortAnswer(Question):
    best_answer: str = ""
    regexp: bool = False
    case_sensitive: bool = False
    rows: int = 1
    cols: int = 40

    def __post_init__(self):
        if not self.best_answer:
            raise ValueError("best_answer required")
        self.new_question_code = "SA"

    def _type_rows(self):
        flag = (
            "regexp"
            if self.regexp
            else ("sensitive" if self.case_sensitive else "insensitive")
        )
        return [
            ["InputBox", str(self.rows), str(self.cols), "", ""],
            ["Answer", "", self.best_answer, flag, ""],
        ]


@dataclass
class MatchingPair:
    choice_no: int
    choice_text: str
    match_text: str


@dataclass
class Matching(Question):
    pairs: List[MatchingPair] = field(default_factory=list)
    scoring: str = "AllOrNothing"

    def __post_init__(self):
        self.new_question_code = "M"

    def _type_rows(self):
        rows = [["Scoring", self.scoring, *BLANK4]]
        for p in self.pairs:
            rows.append(["Choice", str(p.choice_no), p.choice_text, "", ""])
        for p in self.pairs:
            rows.append(["Match", str(p.choice_no), p.match_text, "", ""])
        return rows


@dataclass
class MCOption:
    text: str
    percent: int
    feedback: Optional[str] = None
    html_used: bool = False

    def to_row(self):
        html_flag = "HTML" if self.html_used else ""
        fb_flag = "HTML" if self.feedback and self.html_used else ""
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
    options: List[MCOption] = field(default_factory=list)

    def __post_init__(self):
        self.new_question_code = "MC"

    def _type_rows(self):
        return [o.to_row() for o in self.options]


@dataclass
class TFOption:
    is_true: bool
    credit: int
    feedback: Optional[str] = None

    def to_row(self):
        return [
            "True" if self.is_true else "False",
            str(self.credit),
            self.feedback or "",
            "",
            "",
        ]


@dataclass
class TrueFalse(Question):
    true_row: Optional[TFOption] = None
    false_row: Optional[TFOption] = None

    def __post_init__(self):
        # basic validation
        if self.true_row is None or self.false_row is None:
            raise ValueError("true_row and false_row must both be provided")
        if not self.true_row.is_true:
            raise ValueError("true_row must have is_true=True")
        if self.false_row.is_true:
            raise ValueError("false_row must have is_true=False")

        # correct assignment — no extra syntax!
        self.new_question_code = "TF"

    def _type_rows(self):
        # True row first, then False row — each already returns 6 columns
        return [self.true_row.to_row(), self.false_row.to_row()]


@dataclass
class MSOption:
    text: str
    correct: bool
    feedback: Optional[str] = None
    html_used: bool = False

    def to_row(self):
        html_flag = "HTML" if self.html_used else ""
        fb_flag = "HTML" if self.feedback and self.html_used else ""
        return [
            "Option",
            "1" if self.correct else "0",
            self.text,
            html_flag,
            self.feedback or "",
            fb_flag,
        ]


@dataclass
class MultiSelect(Question):
    options: List[MSOption] = field(default_factory=list)
    scoring: str = "AllOrNothing"

    def __post_init__(self):
        self.new_question_code = "MS"

    def _type_rows(self):
        rows = [["Scoring", self.scoring, *BLANK4]]
        rows.extend(o.to_row() for o in self.options)
        return rows


@dataclass
class OrderingItem:
    text: str
    feedback: Optional[str] = None
    html_used: bool = False

    def to_row(self):
        html_flag = "HTML" if self.html_used else ""
        fb_flag = "HTML" if self.feedback and self.html_used else ""
        return ["Item", self.text, html_flag, self.feedback or "", fb_flag]


@dataclass
class Ordering(Question):
    items: List[OrderingItem] = field(default_factory=list)
    scoring: str = "AllOrNothing"

    def __post_init__(self):
        self.new_question_code = "O"

    def _type_rows(self):
        rows = [["Scoring", self.scoring, *BLANK4]]
        rows.extend(i.to_row() for i in self.items)
        return rows


class QuestionBank:
    def __init__(self):
        self._questions: List[Question] = []

    def add(self, *questions: Question):
        self._questions.extend(questions)

    def export_csv(self, path: str | Path, encoding: str = "utf-8-sig") -> Path:
        p = Path(path).expanduser().resolve()
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open("w", newline="", encoding=encoding) as f:
            w = csv.writer(f)
            for q in self._questions:
                w.writerows(q.to_rows())
        return p

    def __iter__(self):
        return iter(self._questions)
