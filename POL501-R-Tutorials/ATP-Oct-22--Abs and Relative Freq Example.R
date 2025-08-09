# Create a data frame with the initial percentages
data <- data.frame(
  Confidence = c("Very confident", "Somewhat confident", "Not too confident", "Not at all confident", "No answer"),
  `Oct_10_16.2022` = c(21, 38, 24, 16, 1),
  `Sep_30_Oct_5.2020` = c(17, 38, 28, 16, 1)
)
# Quick look
head(data)

# Duplicate the Dataframe
data.freq <- data
# Keep the first two col
data.freq <- data.freq[,c(1:2)]

# Convert percentages to actual numbers for Oct 10-16, 2022 using N = 2544
data.freq$Oct_10_16.2022 <- (data.freq$Oct_10_16.2022/100) * 2544
# Round the data to get absolute freq
data.freq$Oct_10_16.2022 <- round(data.freq$Oct_10_16.2022,0)

# Print the updated data frame
print(data.freq)

# Check we get the correct sum
sum(data.freq$Oct_10_16.2022)
