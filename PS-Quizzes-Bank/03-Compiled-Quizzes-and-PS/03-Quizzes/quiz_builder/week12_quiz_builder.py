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
A_n1, A_x1 = 400, 120  # urban vaccinated
A_n2, A_x2 = 500, 125  # rural vaccinated
A_p1, A_p2 = A_x1 / A_n1, A_x2 / A_n2
A_diff = A_p1 - A_p2
A_ci_low, A_ci_high = (round(v, 3) for v in ci_diff95(A_n1, A_x1, A_n2, A_x2))
A_z = round(pooled_z(A_n1, A_x1, A_n2, A_x2), 2)

B_n1, B_x1 = 800, 200  # framing SMS
B_n2, B_x2 = 600, 180  # neutral SMS
B_p1, B_p2 = B_x1 / B_n1, B_x2 / B_n2
B_diff = B_p1 - B_p2
B_ci_low, B_ci_high = (round(v, 3) for v in ci_diff95(B_n1, B_x1, B_n2, B_x2))
B_z = round(pooled_z(B_n1, B_x1, B_n2, B_x2), 2)

# ---------------------------------------------------------------------------
# 1 – 6  (conceptual items)  – unchanged
# ---------------------------------------------------------------------------

## 1 ##
bank.add(
    MultipleChoice(
        title="95 % CI formula",
        question_text="Which expression gives the 95 % confidence interval for the difference of two population proportions (p₁ − p₂)?",
        options=[
            MCOption("(p̂₁ − p̂₂) ± 1.96 × SE", 100),
            MCOption("(p̂₁ − p̂₂) ± t* × SE", 0),
            MCOption("(p̂₁ − p̂₂) ± 1.64 × SE", 0),
            MCOption("(p̂₁ − p̂₂) ± 2.58 × SE", 0),
        ],
        points=2,
    )
)

## 2 ##
bank.add(
    MultipleChoice(
        title="CI Includes Zero",
        question_text="A confidence interval that *includes zero* proves, beyond any doubt, there is no difference between the two population proportions.",
        options=[
            MCOption("True", 0),
            MCOption("False", 100),
        ],
        points=1,
    )
)

## 3 ##
bank.add(
    MultipleChoice(
        title="Pooled Standard Error",
        question_text="Select the correct standard‑error formula under H₀: p₁ = p₂.",
        options=[
            MCOption("SE₀ = √[ p̂(1−p̂)(1/n₁ + 1/n₂) ]", 100),
            MCOption("SE₀ = √[ p̂₁(1−p̂₁)/n₁ + p̂₂(1−p̂₂)/n₂ ]", 0),
            MCOption("SE₀ = √[ (p̂₁ − p̂₂)/(n₁ + n₂) ]", 0),
            MCOption("SE₀ = √[ (p̂₁ − p̂₂)²/(n₁n₂) ]", 0),
        ],
        points=2,
    )
)

## 4 ##
bank.add(
    MultipleChoice(
        title="Meaning of p‑value",
        question_text="What does the *p‑value* represent in this test?",
        options=[
            MCOption("Probability H₀ is true", 0),
            MCOption(
                "Probability of the observed (or more extreme) data assuming H₀ is true",
                100,
            ),
            MCOption("1 − confidence level", 0),
            MCOption("Chosen significance level", 0),
        ],
        points=3,
    )
)

## 5 ##
pairs = [
    MatchingPair(
        1,
        "Null Hypothesis (H₀)",
        "The default assumption or claim being tested, often representing the status quo or 'no change'. ",
    ),
    MatchingPair(
        2,
        "Alternative Hypothesis (Hₐ)",
        "The research hypothesis; what we suspect might be true if the default assumption is rejected.",
    ),
    MatchingPair(
        3,
        "Critical Value",
        "The cut-off point on the test statistic's distribution that defines the rejection region for the null hypothesis.",
    ),
]
bank.add(
    Matching(
        title="Understanding Hypothesis Tests",
        question_text="Match the core concepts of hypothesis testing to their descriptions.",
        pairs=pairs,
        scoring="AllOrNothing",
        points=3,
    )
)

## 6 ##
steps = [
    OrderingItem("Compute p̂₁ and p̂₂"),
    OrderingItem("Find the standard error (SE)"),
    OrderingItem("Multiply SE by z* to get the margin of error"),
    OrderingItem("Form (p̂₁ − p̂₂) ± MOE"),
]
bank.add(
    Ordering(
        title="CI steps",
        question_text="Put the steps for building a confidence interval in order.",
        items=steps,
        scoring="AllOrNothing",
        points=2,
    )
)

# ---------------------------------------------------------------------------
# 7. Practical CI – Vaccination survey
# ---------------------------------------------------------------------------
bank.add(
    MultipleChoice(
        title="Vaccination Rate Confidence Interval",  # Slightly more descriptive title
        question_text=(
            # Adds context about the survey's purpose
            "A public health survey investigated vaccination coverage differences between populations. "
            # Clarifies sample details and defines sample proportions
            f"In the urban sample, **{A_x1}** out of **{A_n1}** respondents reported being vaccinated "
            f"(yielding a sample proportion p̂₁ = {A_p1:.2f}). In the rural sample, **{A_x2}** out of **{A_n2}** "
            f"respondents were vaccinated (p̂₂ = {A_p2:.2f}).\n\n"
            # Explicitly states the observed difference calculation
            f"The observed difference in these sample proportions is Δ = p̂₁ - p̂₂ = {A_diff:+.2f}.\n\n"
            # Reframes the question to emphasize estimating the true population difference
            "Based on this data, what is the plausible range for the *true difference* in vaccination proportions ($p_1 - p_2$) between the underlying urban and rural populations? Select the correct 95% confidence interval below, rounded to three decimal places."
        ),
        options=[
            MCOption(
                f"[ {A_ci_low:+.3f}, {A_ci_high:+.3f} ]", 100
            ),  # Added spaces for readability
            MCOption("[ −0.050, +0.150 ]", 0),
            MCOption("[ +0.009, +0.109 ]", 0),
            MCOption("[ −0.109, +0.009 ]", 0),
        ],
        points=2,
    )
)

# ---------------------------------------------------------------------------
# 8. CI interpretation – Climate‑bill SMS experiment
# ---------------------------------------------------------------------------
bank.add(
    MultipleChoice(
        title="Interpreting Field Experiment Confidence Interval",
        question_text=(
            "Field experiments test interventions in real-world settings to understand their causal effects. "
            "In this study, researchers wanted to see if the way information was framed could influence voter support for environmental policy.\n\n"
            "To estimate the effect of messaging on voter opinion, a randomized experiment was conducted. "
            # Added description for policy framing
            f"Group 1 received an SMS message using a **specific policy framing** (e.g., highlighting potential job creation from the bill); out of {B_n1:,} voters in this group, "
            f"**{B_x1}** subsequently expressed support for a climate bill (sample proportion p̂₁ = {B_p1:.2f}). "
            # Added description for neutral reminder
            f"Group 2 (the control group) received a neutral reminder message (e.g., simply stating 'Vote on the climate bill next Tuesday'); out of {B_n2:,} voters, "
            f"**{B_x2}** supported the bill (sample proportion p̂₂ = {B_p2:.2f}).\n\n"
            f"The observed difference in support rates (treatment - control) is Δ = p̂₁ - p̂₂ = {B_diff:+.2f}.\n\n"
            f"A 95% confidence interval for the true difference in population proportions ($p_1 - p_2$) was calculated as **[ {B_ci_low:+.3f}, {B_ci_high:+.3f} ]**. "
            "Based *only* on this confidence interval and using a 5% significance level (α = 0.05), what conclusion can be drawn about the effectiveness of the policy-framing message compared to the neutral reminder?"
        ),
        options=[
            MCOption(
                "The neutral reminder (Group 2) generated *significantly higher* support than the policy framing (Group 1).",
                100,
            ),
            MCOption(
                "There is *no statistically significant difference* in support between the two message types.",
                0,
            ),
            MCOption(
                "The policy framing (Group 1) generated *significantly higher* support than the neutral reminder (Group 2).",
                0,
            ),
            MCOption(
                "The result is inconclusive because the confidence interval includes zero.",
                0,
            ),
        ],
        points=2,
    )
)

# ---------------------------------------------------------------------------
# 9. Calculate z – Vaccination survey
# ---------------------------------------------------------------------------
bank.add(
    MultipleChoice(
        title="Vaccination Rate Comparison: z-statistic",  # Slightly more descriptive title
        question_text=(
            # Added context about the goal: testing for a significant difference
            "A public health department is investigating whether there is a statistically significant difference in COVID-19 vaccination rates between urban and rural populations in their jurisdiction. They collected the following sample data:\n"
            # Used Markdown list for clarity
            f"* **Urban Sample:** {A_x1} out of {A_n1} residents were vaccinated (p̂₁ = {A_p1:.2f})\n"
            f"* **Rural Sample:** {A_x2} out of {A_n2} residents were vaccinated (p̂₂ = {A_p2:.2f})\n\n"
            # Clarified the hypothesis and the specific statistic needed
            "To formally test the null hypothesis that the true population proportions are equal (H₀: $p_1 = p_2$, meaning $p_1 - p_2 = 0$), calculate the appropriate *pooled two-proportion z-test statistic*. Assume the samples are independent.\n\n"
            # Maintained the final instruction
            "Select the value below that best matches your calculation, rounded to two decimal places."
        ),
        options=[
            MCOption(f"{A_z:+.2f}", 100),
            MCOption("+1.28", 0),
            MCOption("+2.33", 0),
            MCOption("−1.67", 0),
        ],
        points=2,
    )
)

# ---------------------------------------------------------------------------
# 10. Calculate z – Climate‑bill SMS experiment
# ---------------------------------------------------------------------------. Calculate z – Climate‑bill SMS experiment
# ---------------------------------------------------------------------------
bank.add(
    MultipleChoice(
        title="Field Experiment: z-statistic Calculation",  # Adjusted title
        question_text=(
            # Explicitly refers back to the experiment and its context
            "Recall the randomized field experiment investigating voter support for a climate bill, comparing a **policy-framing SMS message** (Group 1) against a **neutral reminder** (Group 2). The sample data was:\n"
            # Restates the data for convenience
            f"* Group 1 (Policy Framing): {B_x1}/{B_n1:,} supported (p̂₁ = {B_p1:.2f})\n"
            f"* Group 2 (Neutral): {B_x2}/{B_n2:,} supported (p̂₂ = {B_p2:.2f})\n\n"
            # Connects to prior analysis (CI) and sets up the hypothesis test
            "We previously constructed a confidence interval to estimate the difference between these groups ($p_1 - p_2$). Now, let's calculate the **test statistic** needed to formally test the null hypothesis that there is no difference in the true population proportions ($H_0: p_1 = p_2$) against the two-sided alternative ($H_a: p_1 \\neq p_2$).\n\n"
            # Specifies the required calculation
            "Compute the pooled two-proportion z-test statistic. Select the value below that best matches your result, rounded to two decimal places."
        ),
        options=[
            MCOption(f"{B_z:+.2f}", 100),
            MCOption("−1.64", 0),
            MCOption("+2.08", 0),
            MCOption("−2.58", 0),
        ],
        points=2,
    )
)

# ---------------------------------------------------------------------------
# Write the CSV
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    csv_path = bank.export_csv("week12_quiz_final.csv")
    print(
        f"✔  Brightspace‑ready CSV written to: {csv_path}\nQuestions: {len(list(bank))}"
    )
