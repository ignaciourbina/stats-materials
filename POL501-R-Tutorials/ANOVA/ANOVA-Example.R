# Load necessary library
library(tidyverse)

# Set seed for reproducibility
set.seed(123)

# Simulate data
group_size <- 30  # Number of observations per group
group_labels <- c("Group1", "Group2", "Group3")  # Names of groups

# Generate data for each group
group1 <- rnorm(group_size, mean = 50, sd = 5)  # Group 1: mean 50, sd 5
group2 <- rnorm(group_size, mean = 55, sd = 5)  # Group 2: mean 55, sd 5
group3 <- rnorm(group_size, mean = 60, sd = 5)  # Group 3: mean 60, sd 5

# Combine into a data frame
data <- data.frame(
  Value = c(group1, group2, group3),
  Group = factor(rep(group_labels, each = group_size))
)

# Preview the dataset
print(head(data))

# Run ANOVA
anova_result <- aov(Value ~ Group, data = data)

# Print ANOVA summary
summary(anova_result)

# Visualize the data (optional)
ggplot(data, aes(x = Group, y = Value)) +
  geom_boxplot() +
  labs(title = "Boxplot of Groups", x = "Group", y = "Value")


# Load necessary library
library(tidyverse)

# Simulate example dataset similar to the one described
set.seed(123)
data <- data.frame(
  Score = c(
    rnorm(58, mean = 75.1, sd = 13.61),  # Lecture A
    rnorm(55, mean = 72.0, sd = 13.61),  # Lecture B
    rnorm(51, mean = 78.9, sd = 13.61)   # Lecture C
  ),
  Lecture = factor(rep(c("A", "B", "C"), times = c(58, 55, 51)))
)

# Conduct ANOVA
anova_result <- aov(Score ~ Lecture, data = data)
summary(anova_result)

# Pairwise t-tests with Bonferroni correction
pairwise_result <- pairwise.t.test(
  data$Score,               # Numeric data
  data$Lecture,             # Grouping factor
  p.adjust.method = "bonferroni"  # Apply Bonferroni correction
)

# Print pairwise t-test results
print(pairwise_result)

# Optional: Visualize the data
ggplot(data, aes(x = Lecture, y = Score)) +
  geom_boxplot() +
  labs(title = "Scores by Lecture Group", x = "Lecture", y = "Score")




The example context involves analyzing the midterm scores of students in three different lectures (A, B, and C) of the same statistics course. The goal is to determine whether there are significant differences in the average midterm scores between these lecture groups.

### Key Details of the Context:

1. **Dataset**:
  - The dataset consists of midterm scores for students in three different lecture groups:
  - **Lecture A**: 58 students, mean score = 75.1, standard deviation = 13.9.
- **Lecture B**: 55 students, mean score = 72.0, standard deviation = 13.8.
- **Lecture C**: 51 students, mean score = 78.9, standard deviation = 13.1.

2. **Initial Analysis**:
  - An ANOVA was performed to test the null hypothesis:
  - \( H_0 \): All three lectures have the same mean midterm score.
- \( H_A \): At least one lecture has a different mean midterm score.
- The ANOVA results showed a p-value of 0.033, which is below the standard significance level of 0.05. This suggests rejecting \( H_0 \), indicating evidence of differences in the mean midterm scores among the lectures.

3. **Follow-Up Analysis**:
  - After rejecting \( H_0 \), the next step is to identify which specific pairs of lectures have significantly different means.
- Pairwise comparisons are conducted using t-tests with the **Bonferroni correction** to control the overall Type I error rate due to multiple comparisons.

4. **Bonferroni Correction**:
  - With three lecture groups, there are \( K = \frac{3(3-1)}{2} = 3 \) pairwise comparisons:
  - Lecture A vs. Lecture B.
- Lecture A vs. Lecture C.
- Lecture B vs. Lecture C.
- The Bonferroni correction adjusts the significance level for each test to \( \alpha/K \), where \( \alpha = 0.05 \). For this example, \( \alpha_{\text{adjusted}} = 0.05 / 3 = 0.0167 \).

5. **Results**:
  - Pairwise t-tests, adjusted for Bonferroni correction, help identify specific differences:
  - **Lecture A vs. Lecture B**: No significant difference (p > 0.0167).
- **Lecture A vs. Lecture C**: No significant difference (p > 0.0167).
- **Lecture B vs. Lecture C**: Significant difference (p < 0.0167).

### Summary:
The analysis shows that while ANOVA detected overall differences among the lectures, pairwise comparisons revealed that only Lectures B and C have a statistically significant difference in their mean midterm scores. This finding highlights the importance of post-hoc tests to identify specific group differences after rejecting the null hypothesis in ANOVA.
