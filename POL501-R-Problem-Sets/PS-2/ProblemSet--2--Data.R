## Setting Up the Environment
install.packages(pacman) # Package Manager
pacman::p_load(dplyr, ggplot2, haven)

## Setting Up the Directory
setwd("C:/Users/Ignacio/Dropbox/PhD SBU/06_Teaching/00_POL-501/Problem Sets/PS-2/")

## Confirm the working directory
getwd()

## Loading the .sav Dataset
data <- read_sav("NPORS_2024_for_public_release.sav")

## View the first few rows of the dataset (glimpse is a function of the dyplr package)
glimpse(data)
str(data)

## Keep some variables
df_sub <- data %>%
  select(RESPID, PARTY, INTFREQ, RADIO, ECON1MOD, INFRASPEND, MOREGUNIMPACT, CRIMESAFE)

## View the first few rows of the dataset (glimpse is a function of the dyplr package)
glimpse(df_sub)
str(df_sub)

'1. Mutually Exclusive Events (Or Rule)
Question: Based on the survey data, calculate the probability that a randomly selected respondent identifies as either a Democrat or a Republican. Use the probability rule for mutually exclusive events.
'

'2. General Or Rule (Non-Mutually Exclusive)
Question: What is the probability that a respondent listens to the radio or uses the internet almost constantly?.'

'3. And Probability (Joint Probability)
Question: What is the probability that a respondent believes there would be more crime if more Americans owned guns and describes their community as somewhat safe or safer?'

'4. Conditional Probability
Question: Given that a respondent describes their community as somewhat safe or safer, what is the probability that a respondent believes there would be more crime if more Americans owned guns?'

'5. Conditional Probability
Question: Given that a respondent describes their community as not too safe or not at all safe, what is the probability that a respondent believes there would be more crime if more Americans owned guns?'

'6. Create a 2x2 table to examine the relationship between perceptions of economic conditions in the community (grouped as "Excellent/Good" and "Only fair/Poor") and support for increasing government spending on roads and bridges (grouped as "Increase a lot/little" and "Stay the same/Decrease"). Then, calculate the conditional probability that a respondent supports increased spending given that they perceive economic conditions as "Excellent" or "Good." '


# Drop missing values (coded as 99) for all variables except RESPID
df_clean <- df_sub %>%
  filter_at(vars(-RESPID), all_vars(. != 99))


# Save it as RData
save(df_clean, file = "dataframe-ps2.RData")

table(df_clean$PARTY)
table(df_clean$INTFREQ)
table(df_clean$RADIO)
table(df_clean$ECON1MOD)
table(df_clean$INFRASPEND)
table(df_clean$MOREGUNIMPACT)
table(df_clean$CRIMESAFE)


# Total number of valid respondents
n_total_q1 <- nrow(df_clean)

# Number who are Democrat (2) or Republican (1)
n_rep_dem <- df_clean %>%
  filter(PARTY == 1 | PARTY == 2) %>%
  nrow()

# Calculate probability
prob_rep_dem <- n_rep_dem / n_total_q1

# Display the result
print(paste("Probability of identifying as Democrat or Republican:",
            round(prob_rep_dem,2)))
