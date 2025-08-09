import os
from Module_quiz_csv_builder_py import (
    QuestionBank,
    MultipleChoice,
    MCOption,
    WrittenResponse,
)

# -*- coding: utf-8 -*-
"""
Created on Sun May 25 19:04:27 2025

@author: ignac
"""

path = r"F:\Dropbox\PhD SBU\06_Teaching\01a_POL201\03-Quizzes\quiz_builder"

os.chdir(path)

bank = QuestionBank()

# Probability Section
q1 = MultipleChoice(
    title="Probability of Watching Debates",
    question_text=r"""<p>In a recent poll, 30% of respondents say they watch political debates on TV, 25% say they follow debates online, and 10% say they do both.</p>
<p>If one person is selected at random, what is the probability they watch debates on TV or online?</p>""",
    points=3,
    html_used=True,
    options=[
        MCOption("0.55", 100, html_used=True),
        MCOption("0.45", 0, html_used=True),
        MCOption("0.475", 0, html_used=True),
        MCOption("0.075", 0, html_used=True),
    ],
)

q2 = MultipleChoice(
    title="Conditional Probability from Survey Table",
    question_text=r"""<p>A national survey of 700 adults asked two questions: whether they support implementing a federal carbon tax (support coded as 1, and do not support as 0) and how much they agree with the statement:</p>
<p><i>“Climate change poses a serious threat to the country’s future.”</i></p>
<p>Responses to the agreement statement were measured on a 5-point scale (from Strongly Disagree to Strongly Agree). The results are summarized below:</p>
<table>
<tr><th></th><th>Strongly Disagree</th><th>Disagree</th><th>Neutral</th><th>Somewhat Agree</th><th>Strongly Agree</th></tr>
<tr><td><b>Support Carbon Tax (1)</b></td><td>30</td><td>50</td><td>70</td><td>120</td><td>80</td></tr>
<tr><td><b>Do Not Support (0)</b></td><td>60</td><td>90</td><td>100</td><td>50</td><td>50</td></tr>
</table>
<p>What is the probability that a respondent supports a carbon tax, <b>given</b> that they answered “Somewhat Agree” or “Strongly Agree” to the climate threat statement?</p>""",
    points=3,
    html_used=True,
    options=[
        MCOption("0.29", 0, html_used=True),
        MCOption("0.5", 0, html_used=True),
        MCOption("0.57", 0, html_used=True),
        MCOption("0.67", 100, html_used=True),
    ],
)

# Descriptive Statistics Section
intro = WrittenResponse(
    title="Descriptive Statistics: Ideological Distribution Intro",
    question_text=r"""<p>In a public opinion study, respondents were asked to place themselves on an ideological spectrum from 1 (most liberal) to 11 (most conservative). Samples of 200 residents were collected from each of two cities in different states. The table below shows the absolute frequency of responses in each group (e.g., 22 respondents from City A placed themselves at score position of “1,” that is, “most liberal”). Basic summary statistics are also provided.</p>

<table>
<tr><th></th><th colspan=\"11\"><b>Ideological Placement</b></th></tr>
<tr><th></th><th>1</th><th>2</th><th>3</th><th>4</th><th>5</th><th>6</th><th>7</th><th>8</th><th>9</th><th>10</th><th>11</th></tr>
<tr><td><i>Absolute Frequencies</i></td><td colspan=\"11\"></td></tr>
<tr><td><b>City A</b></td><td>22</td><td>18</td><td>20</td><td>18</td><td>16</td><td>12</td><td>16</td><td>18</td><td>18</td><td>20</td><td>22</td></tr>
<tr><td><b>City B</b></td><td>17</td><td>18</td><td>16</td><td>19</td><td>18</td><td>21</td><td>17</td><td>19</td><td>18</td><td>17</td><td>18</td></tr>
</table>

<p><b>Summary statistics of the 1 to 11 ideological placement score variable:</b></p>
<ul>
<li><b>City A:</b> Mean = 6.01; Standard Deviation = 3.34</li>
<li><b>City B:</b> Mean = 6.03; Standard Deviation = 3.13</li>
</ul>""",
    points=0,
    html_used=True,
)

q3 = WrittenResponse(
    title="Draw Bar Charts for Each City",
    question_text=r"""<p>Create a bar chart (graph) for each city's ideological scores based on the frequency table above. Describe the general shape of each distribution.</p>""",
    points=3,
    html_used=True,
)

q4 = WrittenResponse(
    title="Interpret Similarity in Means and SDs",
    question_text=r"""<p>Both cities have almost the same mean ideological score and fairly similar standard deviations. Does this mean the ideological distributions are similar? Justify your response by interpreting each distribution's shape.</p>""",
    points=3,
    html_used=True,
)

q5 = WrittenResponse(
    title="Interpret Distribution Takeaways",
    question_text=r"""<p>In plain language, what can we learn about the distribution of ideological placements for each city? What are the main takeaways?</p>""",
    points=3,
    html_used=True,
)

flood_intro = WrittenResponse(
    title="Flood Damage Cost Distribution Intro",
    question_text=r"""<p>Floods can vary greatly in severity, from minor water intrusion to total property loss. Suppose the following table summarizes expert estimates for the <em>typical annual property damage</em> faced by uninsured homeowners in a flood-prone region. Each level reflects the amount a private homeowner might need to pay out-of-pocket for repairs or rebuilding in a given year.</p>
<p><em>The table below represents four possible outcomes, each with an associated cost and probability; together, they describe a random variable for annual flood-related damages.</em></p>
<table border="1">
<tr><th>Flood Severity</th><th>No Flood</th><th>Moderate Flood</th><th>Heavy Flood</th><th>Catastrophic Flood</th></tr>
<tr><td><b>Damage Cost (C)</b></td><td>$0</td><td>$5,000</td><td>$20,000</td><td>$100,000</td></tr>
<tr><td><b>Probability</b></td><td>0.70</td><td>0.20</td><td>0.08</td><td>0.02</td></tr>
</table>""",
    points=0,
    html_used=True,
)


# Random Variables Section
q6 = WrittenResponse(
    title="Expected Value of Flood Damage",
    question_text=r"""<p>Let C be the random variable representing the yearly flood-related <em>cost</em> for an uninsured property in this region. Compute the expected value E[C].</p>""",
    points=2,
    html_used=True,
)

q7 = WrittenResponse(
    title="Interpret Expected Value in Context",
    question_text=r"""<p>In plain language, explain what E[C] means in this context. What should a homeowner understand from this number, even if they don’t expect a flood every year?</p>""",
    points=2,
    html_used=True,
)

q8 = WrittenResponse(
    title="Flood Insurance Decision",
    question_text=r"""<p>Suppose a person is considering buying flood insurance for their home. They are willing to get insurance only if the <em>amount they pay each year</em> for it is less than the expected yearly cost of flood damage. If they are offered insurance that costs <strong>$4,000 per year</strong>, should they take it? Fully justify and explain your answer.</p>""",
    points=1,
    html_used=True,
)

# Intro
spicy_intro = WrittenResponse(
    title="Spicy Food Preference Survey Intro",
    question_text=r"""<p>Suppose a survey of <b>n = 2,000</b> U.S. adults asked whether they enjoy eating spicy food (recorded as “yes”) or not (recorded as “no”). Among the <b>600</b> respondents with <b>foreign-born parents</b>, <b>330</b> said “yes.” Among the <b>1,400</b> respondents with <b>U.S.-born parents</b>, <b>700</b> said “yes.”</p>""",
    points=0,
    html_used=True,
)


# Hypothesis Testing Section
q9 = WrittenResponse(
    title="State Hypotheses for Difference in Proportions",
    question_text=r"""<p>State appropriate null and alternative hypotheses to <em>test whether there is a difference in spicy food preference between adults with foreign-born parents and those with U.S.-born parents</em>. Use mathematical notation and define each term used in your notation.</p>""",
    points=10,
    html_used=True,
)

q10 = WrittenResponse(
    title="Conduct Two-Proportion Z-Test",
    question_text=r"""<p>Conduct a two-proportion z-test at the α = 0.05 significance level to evaluate the stated hypotheses.</p>
<p>Clearly show: <strong>(I)</strong> The formulas used, along with the substituted values; <strong>(II)</strong> The resulting z-statistic; <strong>(III)</strong> Either the critical value or the p-value (<strong>Choose only one</strong>); <strong>(IV)</strong> A clear conclusion: reject or fail to reject the null hypothesis.</p>""",
    points=10,
    html_used=True,
)

q11 = WrittenResponse(
    title="Interpret Hypothesis Test Result",
    question_text=r"""<p>Interpret the result in context. Is there convincing statistical evidence of a difference in preference for spicy food based on parental background? Explain in plain language.</p>""",
    points=5,
    html_used=True,
)

# Inference Concepts and Applications Section
q12 = MultipleChoice(
    title="Confidence Interval Interpretation",
    question_text=r"""<p>A political scientist constructs a 90% confidence interval for the proportion of voters who are against a proposed policy and finds the interval is (0.41, 0.49). Which of the following conclusions is justified based on the information provided about the interval?</p>""",
    points=10,
    html_used=True,
    options=[
        MCOption(
            "There is a 95% chance that the true proportion is between 0.41 and 0.49.",
            0,
        ),
        MCOption(
            "The estimated sample proportion of voters who opposed the policy is 0.45, since it is in the middle of the interval.",
            100,
        ),
        MCOption(
            "At least 90% of all voters are against the policy.",
            0,
        ),
        MCOption(
            "We are 95% confident that the true population proportion of voters supporting the policy is between 0.51 and 0.59.",
            0,
        ),
    ],
)

q13 = MultipleChoice(
    title="Confidence Interval with Standard Error",
    question_text=r"""<p>A pollster reports that 62% of respondents in a representative sample support Candidate Y in an upcoming election. The pollster also reports a <strong>standard error (SE)</strong> of 1.9 percentage points (that is, SE=0.019). Based on this information, which of the following is the correct statement for the corresponding 95% confidence interval?</p>""",
    points=10,
    html_used=True,
    options=[
        MCOption(
            "Between 60.1% and 63.9% of all voters support Candidate Y.",
            100,
        ),
        MCOption(
            "Based on the interval, candidate Y will surely win because more than half of the voters support them.",
            0,
        ),
        MCOption(
            "Between 57% and 67% of all voters support Candidate Y.",
            0,
        ),
        MCOption(
            "Between 58.3% and 65.7% of all voters support Candidate Y.",
            0,
        ),
    ],
)

q14 = MultipleChoice(
    title="Hypotheses for Mean Comparison",
    question_text=r"""<p>A researcher wants to test whether there is a difference in average weekly cereal spending between households with children (group 1) and households without children (group 2). Which is the correct null and alternative hypothesis for this test?</p>""",
    points=10,
    html_used=True,
    options=[
        MCOption(
            "H₀: x̄₁ = x̄₂, Hₐ: x̄₁ ≠ x̄₂",
            0,
        ),
        MCOption(
            "H₀: μ₁ = μ₂, Hₐ: μ₁ ≠ μ₂",
            100,
        ),
        MCOption(
            "H₀: μ₁ ≠ μ₂, Hₐ: μ₁ = μ₂",
            0,
        ),
        MCOption(
            "H₀: p₁ = p₂, Hₐ: p₁ ≠ p₂",
            0,
        ),
    ],
)

coffee_intro = WrittenResponse(
    title="Coffee Consumption Sampling Intro",
    question_text=r"""<p>A human resources analyst at a mid-sized tech company wants to estimate the average number of cups of coffee employees drink per day. The company has 120 employees. The analyst randomly samples 10 employees and records the following number of cups consumed on a typical workday:</p>
<p><b>Data:</b> { 2, 3, 1, 4, 2, 3, 2, 5, 3, 4 }</p>""",
    points=0,
    html_used=True,
)


# Confidence Intervals Section
q15 = WrittenResponse(
    title="Sample Mean and Standard Deviation",
    question_text=r"""<p>Compute the sample mean x̄ and the sample standard deviation s for these 10 employees.</p>
<p><b>Data:</b> { 2, 3, 1, 4, 2, 3, 2, 5, 3, 4 }</p>""",
    points=10,
    html_used=True,
)

q16 = WrittenResponse(
    title="99% Confidence Interval for Mean",
    question_text=r"""<p>Construct a 99% confidence interval for the <em>population mean</em> number of cups of coffee consumed per day by employees at the company. Use the t-distribution.</p>
<p>Clearly show: <strong>(I)</strong> The formulas used, along with the substituted values; <strong>(II)</strong> Degrees of freedom (df) used; <strong>(III)</strong> The appropriate Critical t-value used to construct the interval; <strong>(IV)</strong> Your final confidence interval.</p>""",
    points=10,
    html_used=True,
)

q17 = WrittenResponse(
    title="Interpret Confidence Interval",
    question_text=r"""<p>Provide an intuitive interpretation of the confidence interval using plain language.</p>""",
    points=5,
    html_used=True,
)

# Add all to bank
bank.add(
    q1,
    q2,
    intro,
    q3,
    q4,
    q5,
    flood_intro,
    q6,
    q7,
    q8,
    spicy_intro,
    q9,
    q10,
    q11,
    q12,
    q13,
    q14,
    coffee_intro,
    q15,
    q16,
    q17,
)

# Export the full quiz to CSV
bank.export_csv("full_quiz.csv")
