import numpy as np
import pandas as pd

# Define the constraints
MIN_FIXED_COST = 5000000    # Minimum fixed administrative cost
MAX_FIXED_COST = 10000000   # Maximum fixed administrative cost
MIN_BENEFIT_PER_PERSON = 100  # Minimum monthly benefit per participant
MAX_BENEFIT_PER_PERSON = 300  # Maximum monthly benefit per participant
MIN_PARTICIPANTS = 50000      # Minimum number of participants
MAX_PARTICIPANTS = 200000     # Maximum number of participants
PARTICIPANT_STEP = 25000      # Step size between participant levels
MIN_PARTICIPANT_LEVELS = 4    # Minimum number of participant levels
MAX_PARTICIPANT_LEVELS = 7    # Maximum number of participant levels

def generate_probabilities(num_levels):
    # Generate random probabilities for the different participant levels
    # Ensure probabilities sum to 1
    probs = np.random.rand(num_levels)
    probs /= probs.sum()
    return probs

def generate_random_data():
    # Randomize the fixed administrative cost
    fixed_cost = np.random.randint(MIN_FIXED_COST, MAX_FIXED_COST + 1)

    # Randomize the monthly benefit per participant
    benefit_per_person = np.random.randint(MIN_BENEFIT_PER_PERSON, MAX_BENEFIT_PER_PERSON + 1)

    # Randomize the number of participant levels
    num_levels = np.random.randint(MIN_PARTICIPANT_LEVELS, MAX_PARTICIPANT_LEVELS + 1)

    # Generate possible participant numbers
    participant_numbers = np.arange(MIN_PARTICIPANTS, MAX_PARTICIPANTS + 1, PARTICIPANT_STEP)
    # Randomly select participant levels
    participant_values = np.sort(np.random.choice(participant_numbers, num_levels, replace=False))

    # Generate probabilities for each participant level
    probabilities = generate_probabilities(num_levels)

    # Create a DataFrame for the PMF of participants
    pmf_table = pd.DataFrame({
        'Participants (P)': participant_values,
        'Probability P(P=p)': probabilities
    })

    # Adjust probabilities to ensure they sum exactly to 1
    pmf_table['Probability P(P=p)'] /= pmf_table['Probability P(P=p)'].sum()

    # Add rows for P < min and P > max participants with zero probability
    pmf_table = pd.concat([
        pd.DataFrame({'Participants (P)': [f'P < {participant_values.min()}'], 'Probability P(P=p)': [0]}),
        pmf_table,
        pd.DataFrame({'Participants (P)': [f'P > {participant_values.max()}'], 'Probability P(P=p)': [0]})
    ], ignore_index=True)

    return fixed_cost, benefit_per_person, pmf_table

def display_randomized_assignment():
    fixed_cost, benefit_per_person, pmf_table = generate_random_data()

    # Display randomized values
    print(f"Randomized Fixed Administrative Cost: ${fixed_cost}")
    print(f"Randomized Monthly Benefit per Participant: ${benefit_per_person}\n")

    # Display the PMF table
    print("Randomized Probability Mass Function of Participants:")
    print(pmf_table.to_string(index=False))

    # Return values for further use
    return fixed_cost, benefit_per_person, pmf_table

# Run the function to generate a randomized version
fixed_cost, benefit_per_person, pmf_table = display_randomized_assignment()
