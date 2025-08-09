###############
## Question 1
##############

import numpy as np
import matplotlib.pyplot as plt

# Given dataset
data_list = np.array([1, 3, 6, 10, 4, 2, 6, 3, 9, 7, 8, 6, 3, 6, 1, 10, 11, 4])
# Sample A: 1, 3, 6, 10, 4, 2, 6, 3, 9, 7, 8, 6, 3, 6, 1, 10, 11, 4
# Sample B: 2, 3, 1, 5, 4, 2, 6, 11, 3, 9, 6, 4, 8, 3, 6

# Define bin edges and labels
bins = np.array([1, 3, 5, 7, 9, 11])
bin_labels = np.array(["[1 , 3)", "[3 , 5)", "[5 , 7)", "[7 , 9)", "[9 , 11]"])

# Compute bin counts using NumPy
bin_counts = [
    np.sum((data_list >= bins[i]) & (data_list < bins[i + 1])) if i < len(bins) - 2
    else np.sum((data_list >= bins[i]) & (data_list <= bins[i + 1])) 
    for i in range(len(bins) - 1)
]

# Print table in readable format
print("\nHistogram Bin Counts Table")
print("-----------------------------------------------------------------")
print(f"{'Bin':<10}{'Lower Limit':<15}{'Upper Limit':<15}{'Width':<10}{'Bin Label':<10}{'Count':<10}")
print("-----------------------------------------------------------------")
for i in range(len(bins) - 1):
    print(f"Bin {i+1:<7}{bins[i]:<15}{bins[i+1]:<15}{2:<10}{bin_labels[i]:<10}{bin_counts[i]:<10}")

# Create bar plot for histogram representation
plt.figure(figsize=(8, 5))
plt.bar(bins[:-1], bin_counts, width=2, edgecolor='black', align='edge', alpha=0.7)

# Labeling
plt.xlabel('Value')
plt.ylabel('Frequency')
plt.title('Histogram of Z')
plt.xticks(bins)
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Show plot
plt.show()

# Compute classical summary statistics
mean_value = np.mean(data_list)
median_value = np.median(data_list)
variance_value = np.var(data_list, ddof=1)  # Sample variance
std_dev_value = np.std(data_list, ddof=1)  # Sample standard deviation
range_value = np.ptp(data_list)  # Range (max - min)
quartiles = np.percentile(data_list, [25, 50, 75])  # Q1, Q2 (median), Q3
iqr_value = quartiles[2] - quartiles[0]  # Interquartile range (IQR)

# Print summary statistics
print("\nClassical Sample Summary Statistics")
print("-------------------------------------------------")
print(f"{'Statistic':<15}{'Value':<15}")
print("-------------------------------------------------")
print(f"{'Mean':<15}{mean_value:<15.2f}")
print(f"{'Median':<15}{median_value:<15.2f}")
print(f"{'Variance':<15}{variance_value:<15.2f}")
print(f"{'Std Deviation':<15}{std_dev_value:<15.2f}")
print(f"{'Range':<15}{range_value:<15.2f}")
print(f"{'Q1 (25%)':<15}{quartiles[0]:<15.2f}")
print(f"{'Q2 (50%)':<15}{quartiles[1]:<15.2f}")
print(f"{'Q3 (75%)':<15}{quartiles[2]:<15.2f}")
print(f"{'IQR':<15}{iqr_value:<15.2f}")
print("-------------------------------------------------")



##############
## Question 2
##############

import numpy as np
import matplotlib.pyplot as plt

# Set seed for reproducibility
np.random.seed(42)

# Sample size
n = 2000

# Generate Sample Green: Bimodal, symmetric
green1 = np.random.normal(loc=-2, scale=1, size=n//2)
green2 = np.random.normal(loc=2, scale=1, size=n//2)
sample_green = np.concatenate([green1, green2])

# Generate Sample Red: Unimodal, symmetric
sample_red = np.random.normal(loc=0, scale=1.5, size=n)

# Generate Sample Blue: Uniform
sample_blue = np.random.uniform(low=-3, high=3, size=n)

# Add random noise to all samples
noise_factor = 0.1
sample_green += np.random.normal(scale=noise_factor, size=n)
sample_red += np.random.normal(scale=noise_factor, size=n)
sample_blue += np.random.normal(scale=noise_factor, size=n)

# Function to rescale each sample to a 0-100 range
def rescale_0_100(sample):
    return 100 * (sample - np.min(sample)) / (np.max(sample) - np.min(sample))

# Apply rescaling
sample_green = rescale_0_100(sample_green)
sample_red = rescale_0_100(sample_red)
sample_blue = rescale_0_100(sample_blue)

# Dictionary with rescaled samples
scaled_samples = {
    "Sample Green": sample_green,
    "Sample Red": sample_red,
    "Sample Blue": sample_blue
}

# Define colors
colors = ["green", "red", "blue"]

# Plot histograms with transparent dashed vertical lines
fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

for ax, (label, sample), color in zip(axes, scaled_samples.items(), colors):
    counts, bins, patches = ax.hist(sample, bins=30, color=color, edgecolor='black', histtype='stepfilled', alpha=0.7)

    # Add transparent dashed vertical lines between bars
    for b in bins:
        ax.axvline(b, color='black', linestyle='dashed', linewidth=0.5, alpha=0.5)

    ax.set_title(label)
    ax.set_xlabel("Scaled Value (0-100)")
    ax.set_ylabel("Frequency")
    ax.set_xlim(0, 100)  # Ensure the x-axis is from 0 to 100

plt.tight_layout()
plt.show()
