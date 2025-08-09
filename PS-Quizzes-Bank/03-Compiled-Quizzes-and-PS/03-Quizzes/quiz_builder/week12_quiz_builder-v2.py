import os
import math
from quiz_csv_builder_v2 import (
    QuestionBank,
    MultipleChoice,
    MCOption,
    Matching,
    MatchingPair,
    Ordering,
    OrderingItem,
)

# -*- coding: utf-8 -*-
"""
Quiz CSV Builder – Week 12 (political‑science version)
=====================================================
Mixed question types (MC + Matching + Ordering) with practical, survey/field‑experiment contexts.
Run from the same directory that contains *quiz_csv_builder.py*.
"""



bank = QuestionBank()

# ---------------------------------------------------------------------------
# Helper functions (internal only)
# ---------------------------------------------------------------------------


def pooled_z(n1, x1, n2, x2):
    """Two‑sample z for H₀: p₁ = p₂ (pooled SE)."""
    p_pool = (x1 + x2) / (n1 + n2)
    se0 = math.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    return (x1 / n1 - x2 / n2) / se0


def ci_diff95(n1, x1, n2, x2):
    """95 % CI for p₁ − p₂ (Wald)."""
    p1, p2 = x1 / n1, x2 / n2
    se = math.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    diff = p1 - p2
    z = 1.96
    return diff - z * se, diff + z * se


# ---------------------------------------------------------------------------
# Data sets used in Q 7 – Q 10
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Data sets used in questions (Simulated data)
# ---------------------------------------------------------------------------
# Dataset A: Vaccination Survey Data
A_n1, A_x1 = 400, 120  # Urban sample size and vaccinated count
A_n2, A_x2 = 500, 125  # Rural sample size and vaccinated count
A_p1, A_p2 = A_x1 / A_n1, A_x2 / A_n2  # Calculate sample proportions
A_diff = A_p1 - A_p2  # Calculate difference in sample proportions
A_ci_low, A_ci_high = (
    round(v, 3) for v in ci_diff95(A_n1, A_x1, A_n2, A_x2)
)  # Calculate 95% CI bounds
A_z = round(pooled_z(A_n1, A_x1, A_n2, A_x2), 2)  # Calculate pooled z-statistic

# Dataset B: Climate Bill SMS Experiment Data
B_n1, B_x1 = 800, 200  # Policy framing group size and support count
B_n2, B_x2 = 600, 180  # Neutral reminder group size and support count
B_p1, B_p2 = B_x1 / B_n1, B_x2 / B_n2  # Calculate sample proportions
B_diff = B_p1 - B_p2  # Calculate difference in sample proportions
B_ci_low, B_ci_high = (
    round(v, 3) for v in ci_diff95(B_n1, B_x1, B_n2, B_x2)
)  # Calculate 95% CI bounds
B_z = round(pooled_z(B_n1, B_x1, B_n2, B_x2), 2)  # Calculate pooled z-statistic

# ---------------------------------------------------------------------------
# Question 1: 95% CI Formula (Conceptual)
# ---------------------------------------------------------------------------
bank.add(
    MultipleChoice(
        title="95% CI formula",
        question_text="Which expression gives the 95% confidence interval for the difference of two population proportions (\\(\\scriptsize p_1 - p_2\\))?",
        options=[
            MCOption(
                "\\(\\scriptsize (\\hat{p}_1 - \\hat{p}_2) \\pm 1.96 \\times SE\\)", 100
            ),  # Correct formula using z=1.96 for 95%
            MCOption(
                "\\(\\scriptsize (\\hat{p}_1 - \\hat{p}_2) \\pm t^* \\times SE\\)", 0
            ),  # Incorrect: uses t* (for means or  scriptsize samples)
            MCOption(
                "\\(\\scriptsize (\\hat{p}_1 - \\hat{p}_2) \\pm 1.64 \\times SE\\)", 0
            ),  # Incorrect: z=1.64 is for 90% CI
            MCOption(
                "\\(\\scriptsize (\\hat{p}_1 - \\hat{p}_2) \\pm 2.58 \\times SE\\)", 0
            ),  # Incorrect: z=2.58 is for 99% CI
        ],
        points=2,
    )
)

# ---------------------------------------------------------------------------
# Question 2: CI Includes Zero Interpretation (Conceptual)
# ---------------------------------------------------------------------------
bank.add(
    MultipleChoice(
        title="CI Includes Zero Interpretation",
        question_text="A confidence interval for a difference (\\(\\scriptsize p_1 - p_2\\)) that *includes zero* indicates that zero is a plausible value for the true difference at the given confidence level.",
        options=[
            MCOption("True", 100),  # Correct interpretation
            MCOption(
                "False", 0
            ),  # Incorrect: It doesn't *prove* no difference, but suggests it's plausible.
        ],
        points=1,
    )
)

# ---------------------------------------------------------------------------
# Question 3: Standard Error Formula for H0 (Conceptual)
# ---------------------------------------------------------------------------
bank.add(
    MultipleChoice(
        title="Standard Error for Two-Proportion Test",
        question_text="When performing a z-test comparing two population proportions, which formula correctly represents the standard error of the difference (\\(\\scriptsize \\hat{p}_1 - \\hat{p}_2\\)) calculated *under the assumption that the null hypothesis \\(\\scriptsize H_0: p_1 = p_2\\) is true*?",
        options=[
            # Correct pooled SE formula used for hypothesis testing under H0
            MCOption(
                "\\(\\scriptsize SE_0 = \\sqrt{ \\hat{p}(1-\\hat{p}) (\\frac{1}{n_1} + \\frac{1}{n_2}) }\\)",
                100,
            ),
            # Unpooled SE formula used for confidence intervals
            MCOption(
                "\\(\\scriptsize SE = \\sqrt{ \\frac{\\hat{p}_1(1-\\hat{p}_1)}{n_1} + \\frac{\\hat{p}_2(1-\\hat{p}_2)}{n_2} }\\)",
                0,
            ),
            # Incorrect formula structure
            MCOption(
                "\\(\\scriptsize SE = \\sqrt{ \\frac{\\hat{p}_1 - \\hat{p}_2}{n_1 + n_2} }\\)",
                0,
            ),
            # Incorrect formula structure
            MCOption(
                "\\(\\scriptsize SE = \\sqrt{ \\frac{(\\hat{p}_1 - \\hat{p}_2)^2}{n_1 n_2} }\\)",
                0,
            ),
        ],
        points=2,
    )
)

# ---------------------------------------------------------------------------
# Question 4: Meaning of p-value (Conceptual)
# ---------------------------------------------------------------------------
bank.add(
    MultipleChoice(
        title="Meaning of p-value",
        question_text="What does the \\(\\scriptsize p\\)-value represent in a hypothesis test?",
        options=[
            MCOption(
                "The probability that the null hypothesis (\\(\\scriptsize H_0\\)) is true.",
                0,
            ),  # Common misconception
            MCOption(
                "The probability of observing the collected data (or data more extreme) if the null hypothesis (\\(\\scriptsize H_0\\)) were actually true.",
                100,
            ),  # Correct definition
            MCOption(
                "The probability that the alternative hypothesis (\\(\\scriptsize H_a\\)) is true.",
                0,
            ),  # Incorrect
            MCOption(
                "The chosen significance level (\\(\\scriptsize \\alpha\\)) for the test.",
                0,
            ),  # Incorrect, p-value is compared to alpha
        ],
        points=3,
    )
)

# ---------------------------------------------------------------------------
# Question 5: Matching Hypothesis Testing Terms (Conceptual)
# ---------------------------------------------------------------------------
pairs_q5 = [
    MatchingPair(
        1,
        "Null Hypothesis (\\(\\scriptsize H_0\\))",
        "The default assumption or claim being tested, often representing the status quo or 'no change'. ",
    ),
    MatchingPair(
        2,
        "Alternative Hypothesis (\\(\\scriptsize H_a\\))",
        "The research hypothesis; what we suspect might be true if the default assumption is rejected.",
    ),
    MatchingPair(
        3,
        "Critical Value",
        "The cut-off point on the test statistic's distribution that defines the rejection region for the null hypothesis.",
    ),
    MatchingPair(
        4,
        "Test Statistic",
        "A value calculated from sample data used to decide between the null and alternative hypotheses.",
    ),  # Added another relevant term
]
bank.add(
    Matching(
        title="Understanding Hypothesis Tests",
        question_text="Match the core concepts of hypothesis testing to their descriptions.",
        pairs=pairs_q5,
        scoring="EquallyWeighted",  # Changed scoring to allow partial credit
        points=4,  # Adjusted points for 4 pairs
    )
)

# ---------------------------------------------------------------------------
# Question 6: Ordering CI Steps (Conceptual)
# ---------------------------------------------------------------------------
steps_q6 = [
    OrderingItem(
        "Calculate sample proportions (\\(\\scriptsize \\hat{p}_1\\) and \\(\\scriptsize \\hat{p}_2\\))"
    ),
    OrderingItem(
        "Calculate the standard error (SE) of the difference"
    ),  # Using unpooled SE for CI
    OrderingItem(
        "Determine the critical value (\\(\\scriptsize z^*\\)) for the desired confidence level"
    ),
    OrderingItem(
        "Compute the margin of error (MOE = \\(\\scriptsize z^* \\times SE\\))"
    ),
    OrderingItem(
        "Form the interval: (\\(\\scriptsize \\hat{p}_1 - \\hat{p}_2\\)) \\(\\scriptsize \\pm\\) MOE"
    ),
]
bank.add(
    Ordering(
        title="Confidence Interval Steps (Difference in Proportions)",
        question_text="Place the steps for constructing a confidence interval for the difference between two population proportions (\\(\\scriptsize p_1 - p_2\\)) in the correct logical order.",
        items=steps_q6,
        scoring="AllOrNothing",
        points=3,  # Adjusted points for 5 steps
    )
)


# ---------------------------------------------------------------------------
# Question 7: Practical CI Calculation – Vaccination Survey (Applied)
# ---------------------------------------------------------------------------
bank.add(
    MultipleChoice(
        title="Vaccination Rate Confidence Interval",
        question_text=(
            "<p>A public health survey investigated vaccination coverage differences between populations. "
            f"In the urban sample, {A_x1} out of {A_n1} respondents reported being vaccinated "
            f"(yielding a sample proportion \\(\\scriptsize \\hat{{p}}_1 = {A_p1:.2f}\\)). In the rural sample, {A_x2} out of {A_n2} "
            f"respondents were vaccinated (\\(\\scriptsize \\hat{{p}}_2 = {A_p2:.2f}\\)).</p>"  # Using </p> for newline in f-string
            f"<p>The observed difference in these sample proportions is \\(\\scriptsize \\Delta = \\hat{{p}}_1 - \\hat{{p}}_2 = {A_diff:+.2f}\\).</p>"  # Using </p> for newline in f-string
            "<p>Based on this data, what is the plausible range for the *true difference* in vaccination proportions (\\(\\scriptsize p_1 - p_2\\)) between the underlying urban and rural populations? Select the correct \\(\\scriptsize 95\\%\\) confidence interval below, rounded to three decimal places.</p>"
        ),
        options=[
            # Correct CI calculated using ci_diff95 helper function
            MCOption(f"[ {A_ci_low:+.3f}, {A_ci_high:+.3f} ]", 100),
            # Plausible distractors
            MCOption("[ −0.050, +0.150 ]", 0),
            MCOption("[ +0.009, +0.109 ]", 0),
            MCOption("[ −0.109, +0.009 ]", 0),
        ],
        points=2,
    )
)

# ---------------------------------------------------------------------------
# Question 8: CI Interpretation – Climate Bill SMS Experiment (Applied)
# ---------------------------------------------------------------------------
bank.add(
    MultipleChoice(
        title="Interpreting Field Experiment Confidence Interval",
        question_text=(
            "<p>Field experiments test interventions in real-world settings to understand their causal effects. "
            "In this study, researchers wanted to see if the way information was framed could influence voter support for environmental policy.</p>"  # Using </p> for newline in f-string
            "<p>To estimate the effect of messaging on voter opinion, a randomized experiment was conducted. "
            f"Group 1 received an SMS message using a specific policy framing (e.g., highlighting potential job creation from the bill); out of {B_n1:,} voters in this group, "
            f"{B_x1} subsequently expressed support for a climate bill (sample proportion \\(\\scriptsize \\hat{{p}}_1 = {B_p1:.2f}\\)). "
            f"Group 2 (the control group) received a neutral reminder message (e.g., simply stating 'Vote on the climate bill next Tuesday'); out of {B_n2:,} voters, "
            f"{B_x2} supported the bill (sample proportion \\(\\scriptsize \\hat{{p}}_2 = {B_p2:.2f}\\)).</p>"  # Using </p> for newline in f-string
            f"<p>The observed difference in support rates (treatment - control) is \\(\\scriptsize \\Delta = \\hat{{p}}_1 - \\hat{{p}}_2 = {B_diff:+.2f}\\).</p>"  # Using </p> for newline in f-string
            f"<p>A \\(\\scriptsize 95\\%\\) confidence interval for the true difference in population proportions (\\(\\scriptsize p_1 - p_2\\)) was calculated as [ {B_ci_low:+.3f}, {B_ci_high:+.3f} ]. </p>"  # Using </p> for newline in f-string
            "<p>Based *only* on this confidence interval and using a \\(\\scriptsize 5\\%\\) significance level (\\(\\scriptsize \\alpha = 0.05\\)), what conclusion can be drawn about the effectiveness of the policy-framing message compared to the neutral reminder?</p>"
        ),
        options=[
            # This option should be correct if B_ci_low and B_ci_high are both negative
            MCOption(
                "The neutral reminder (Group 2) generated *significantly higher* support than the policy framing (Group 1).",
                100,
            ),
            # This option correct if the CI includes 0
            MCOption(
                "There is *no statistically significant difference* in support between the two message types.",
                0,
            ),
            # This option correct if the CI is entirely positive
            MCOption(
                "The policy framing (Group 1) generated *significantly higher* support than the neutral reminder (Group 2).",
                0,
            ),
            # Common misinterpretation of CI including zero
            MCOption(
                "The result is inconclusive because the confidence interval includes zero.",
                0,
            ),
        ],
        points=2,
    )
)

# ---------------------------------------------------------------------------
# Question 9: Calculate z-statistic – Vaccination Survey (Applied)
# ---------------------------------------------------------------------------
bank.add(
    MultipleChoice(
        title="Vaccination Rate Comparison: z-statistic",
        question_text=(
            "<p>A public health department is investigating whether there is a statistically significant difference in COVID-19 vaccination rates between urban and rural populations in their jurisdiction. They collected the following sample data:</p>"
            f"<p>* Urban Sample: {A_x1} out of {A_n1} residents were vaccinated (\\(\\scriptsize \\hat{{p}}_1 = {A_p1:.2f}\\))</p>"
            f"<p>* Rural Sample: {A_x2} out of {A_n2} residents were vaccinated (\\(\\scriptsize \\hat{{p}}_2 = {A_p2:.2f}\\))</p>"
            "<p>To formally test the null hypothesis that the true population proportions are equal (\\(\\scriptsize H_0: p_1 = p_2\\), meaning \\(\\scriptsize p_1 - p_2 = 0\\)), calculate the appropriate *pooled two-proportion z-test statistic*. Assume the samples are independent.</p>"
            "<p>Select the value below that best matches your calculation, rounded to two decimal places.</p>"
        ),
        options=[
            # Correct z-statistic calculated using pooled_z helper function
            MCOption(f"{A_z:+.2f}", 100),
            # Plausible distractors (e.g., critical values or miscalculations)
            MCOption("+1.28", 0),
            MCOption("+2.33", 0),
            MCOption("−1.67", 0),
        ],
        points=2,
    )
)

# ---------------------------------------------------------------------------
# Question 10: Calculate z-statistic – Climate Bill SMS Experiment (Applied)
# ---------------------------------------------------------------------------
bank.add(
    MultipleChoice(
        title="Field Experiment: z-statistic Calculation",
        question_text=(
            "<p>Recall the randomized field experiment investigating voter support for a climate bill, comparing a policy-framing SMS message (Group 1) against a neutral reminder (Group 2). The sample data was:</p>"
            f"<p>* Group 1 (Policy Framing): {B_x1}/{B_n1:,} supported (\\(\\scriptsize \\hat{{p}}_1 = {B_p1:.2f}\\))</p>"
            f"<p>* Group 2 (Neutral Reminder): {B_x2}/{B_n2:,} supported (\\(\\scriptsize \\hat{{p}}_2 = {B_p2:.2f}\\))</p>"
            "<p>We previously constructed a confidence interval to estimate the difference between these groups (\\(\\scriptsize p_1 - p_2\\)). Now, let's calculate the test statistic needed to formally test the null hypothesis that there is no difference in the true population proportions (\\(\\scriptsize H_0: p_1 = p_2\\)) against the two-sided alternative (\\(\\scriptsize H_a: p_1 </p>eq p_2\\)).</p>"
            "<p>Compute the pooled two-proportion z-test statistic. Select the value below that best matches your result, rounded to two decimal places.</p>"
        ),
        options=[
            # Correct z-statistic calculated using pooled_z helper function
            MCOption(f"{B_z:+.2f}", 100),
            # Plausible distractors
            MCOption("−1.64", 0),
            MCOption("+2.08", 0),
            MCOption("−2.58", 0),
        ],
        points=2,
    )
)

# ---------------------------------------------------------------------------
# Write the CSV file
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    output_filename = "week12_quiz_polsci_latex.csv"
    try:
        csv_path = bank.export_csv(output_filename)
        print(f"✔ Brightspace-ready CSV written to: {csv_path}")
        print(f"Total questions generated: {len(list(bank))}")
    except Exception as e:
        print(f"Error exporting CSV: {e}")
