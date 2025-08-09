import os

# path = r"C:\Users\Ignacio\Dropbox\PhD SBU\06_Teaching\01a_POL201\03-Quizzes\quiz_builder"
path = r"F:\Dropbox\PhD SBU\06_Teaching\01a_POL201\03-Quizzes\quiz_builder"  # Notebook path
os.chdir(path)

# smoke_test_quiz_csv_builder.py
from quiz_csv_builder import (
    QuestionBank,
    ShortAnswer,
    WrittenResponse,
    MultipleChoice,
    MCOption,
    TrueFalse,
    TFOption,
)

bank = QuestionBank()
bank.add(
    ShortAnswer(title="Dummy SA", question_text="Type ABC", best_answer="ABC"),
    WrittenResponse(
        title="Dummy WR", question_text="Explain something.", answer_key="Because."
    ),
    MultipleChoice(
        title="Dummy MC",
        question_text="Pick one.",
        options=[MCOption("A", 100), MCOption("B", 0)],
    ),
    TrueFalse(
        title="Dummy TF",
        question_text="The sky is blue.",
        true_row=TFOption(True, 100),
        false_row=TFOption(False, 0),
    ),
)

path = bank.export_csv("smoke_test.csv")
print("✅ Library OK – wrote", path)
