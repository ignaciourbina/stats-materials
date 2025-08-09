library(ggplot2)
library(dplyr)

# Given dataset
data_list <- c(1, 3, 6, 10, 4, 2, 6, 3, 9, 7, 8, 6, 3, 6, 1, 10, 11, 4)
bins <- c(1, 3, 5, 7, 9, 11)
bin_labels <- c("[1 , 3)", "[3 , 5)", "[5 , 7)", "[7 , 9)", "[9 , 11]")

# Manually compute bin counts to match Python logic:
# For all but the last bin: [bin[i], bin[i+1])
# Last bin inclusive: [bin[i], bin[i+1]]
bin_counts <- sapply(seq_along(bins[-1]), function(i) {
  if(i < length(bins) - 1) {
    sum(data_list >= bins[i] & data_list < bins[i + 1])
  } else {
    sum(data_list >= bins[i] & data_list <= bins[i + 1])
  }
})

# Print table similar to Python output
cat("\nHistogram Bin Counts Table\n")
cat("-----------------------------------------------------------------\n")
cat(sprintf("%-10s %-15s %-15s %-10s %-10s %-10s\n",
            "Bin", "Lower Limit", "Upper Limit", "Width", "Bin Label", "Count"))
cat("-----------------------------------------------------------------\n")

for(i in seq_along(bin_counts)) {
  lower <- bins[i]
  upper <- bins[i + 1]
  width <- upper - lower
  cat(sprintf("Bin %-7d %-15d %-15d %-10d %-10s %-10d\n",
              i, lower, upper, width, bin_labels[i], bin_counts[i]))
}

# Prepare data for plotting:
hist_df <- data.frame(
  bin_lower = bins[-length(bins)],
  bin_upper = bins[-1],
  count = bin_counts
)

# Create bar plot with numeric x-axis to match Python's approach
ggplot(hist_df, aes(x = bin_lower, y = count)) +
  geom_bar(
    stat = "identity",
    width = 2,          # matches bin width in Python
    alpha = 0.7,
    fill = "skyblue",
    color = "black"
  ) +
  scale_x_continuous(
    name = "Value",
    breaks = bins        # tick marks at the bin boundaries
  ) +
  labs(y = "Frequency", title = "Histogram of Z") +
  theme_minimal()

#############
## Question 2
#############


library(ggplot2)
library(dplyr)

# -- Data creation (same as before) --------------------------------
set.seed(42)
n <- 2000

green1 <- rnorm(n/2, mean = -2, sd = 1)
green2 <- rnorm(n/2, mean = 2,  sd = 1)
sample_green <- c(green1, green2)

sample_red <- rnorm(n, mean = 0, sd = 1.5)
sample_blue <- runif(n, min = -3, max = 3)

noise_factor <- 0.1
sample_green <- sample_green + rnorm(n, sd = noise_factor)
sample_red   <- sample_red   + rnorm(n, sd = noise_factor)
sample_blue  <- sample_blue  + rnorm(n, sd = noise_factor)

rescale_0_100 <- function(x) {
  (x - min(x)) / (max(x) - min(x)) * 100
}

sample_green <- rescale_0_100(sample_green)
sample_red   <- rescale_0_100(sample_red)
sample_blue  <- rescale_0_100(sample_blue)

df <- data.frame(
  Value  = c(sample_green, sample_red, sample_blue),
  Sample = factor(rep(c("Sample Green", "Sample Red", "Sample Blue"), each = n),
                  levels = c("Sample Green", "Sample Red", "Sample Blue"))
)

# -- Adjust plot window size (one-time call) ------------------------
# If you are in RStudio, enlarge the "Plots" pane or do:
# windows(width = 15, height = 5)    # Windows
# quartz(width = 15, height = 5)     # macOS
# x11(width = 15, height = 5)        # Linux
# Or simply rely on ggsave at the end.

# -- Plot histograms with correct colors and dashed vertical lines --
ggplot(df, aes(x = Value, fill = Sample)) +
  # 1) Dashed vertical lines at each bin boundary
  geom_vline(
    xintercept = seq(0, 100, length.out = 31),
    linetype = "dashed",
    color = "black",
    size = 0.5,
    alpha = 0.5
  ) +
  # 2) Actual histograms
  geom_histogram(
    bins = 30,
    color = "black",
    alpha = 0.7,
    position = "identity"
  ) +
  # 3) Facet side by side, shared y-scale
  facet_wrap(~ Sample, ncol = 3, scales = "fixed") +
  # 4) Manual fill colors
  scale_fill_manual(values = c("Sample Green" = "green",
                               "Sample Red"   = "red",
                               "Sample Blue"  = "blue")) +
  labs(x = "Scaled Value (0-100)", y = "Frequency", title = "Histograms of Samples") +
  coord_cartesian(xlim = c(0, 100)) +
  theme_minimal() +
  theme(legend.position = "none") +
  theme(aspect.ratio = 9 / 16)  # Height / Width


# If you want to save directly to file with a wide layout:
# ggsave("three_samples_wide.png", width = 15, height = 5, units = "in", dpi = 300)
