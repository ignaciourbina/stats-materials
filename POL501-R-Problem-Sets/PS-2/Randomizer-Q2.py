import numpy as np
import pandas as pd

# Define the constraints
MIN_FIXED_COST = 15000  # Minimum fixed cost of the venue
MAX_FIXED_COST = 30000  # Maximum fixed cost of the venue
MIN_ATTENDEE_COST = 50  # Minimum cost per attendee
MAX_ATTENDEE_COST = 100  # Maximum cost per attendee
MIN_ATTENDEES = 50       # Minimum number of attendees
MAX_ATTENDEES = 300      # Maximum number of attendees
ATTENDEE_STEP = 25       # Step size between attendee levels
MIN_ATTENDEE_LEVELS = 4  # Minimum number of attendee levels
MAX_ATTENDEE_LEVELS = 7  # Maximum number of attendee levels

def generate_probabilities(num_levels):
    # Generate random probabilities for the different attendee levels
    # Ensure probabilities sum to 1
    probs = np.random.rand(num_levels)
    probs /= probs.sum()
    return probs

def generate_random_data():
    # Randomize the fixed cost
    fixed_cost = np.random.randint(MIN_FIXED_COST, MAX_FIXED_COST + 1)

    # Randomize the per-attendee cost
    cost_per_attendee = np.random.randint(MIN_ATTENDEE_COST, MAX_ATTENDEE_COST + 1)

    # Randomize the number of attendee levels
    num_levels = np.random.randint(MIN_ATTENDEE_LEVELS, MAX_ATTENDEE_LEVELS + 1)

    # Generate possible attendee numbers
    attendee_numbers = np.arange(MIN_ATTENDEES, MAX_ATTENDEES + 1, ATTENDEE_STEP)
    # Randomly select attendee levels
    attendee_values = np.sort(np.random.choice(attendee_numbers, num_levels, replace=False))

    # Generate probabilities for each attendee number
    probabilities = generate_probabilities(num_levels)

    # Create a DataFrame for the PMF of attendees
    pmf_table = pd.DataFrame({
        'Attendees (A)': attendee_values,
        'Probability P(A=a)': probabilities
    })

    # Adjust probabilities to ensure they sum exactly to 1 (due to floating-point arithmetic)
    pmf_table['Probability P(A=a)'] /= pmf_table['Probability P(A=a)'].sum()

    # Add rows for A < min and A > max attendees with zero probability
    pmf_table = pd.concat([
        pd.DataFrame({'Attendees (A)': [f'A < {attendee_values.min()}'], 'Probability P(A=a)': [0]}),
        pmf_table,
        pd.DataFrame({'Attendees (A)': [f'A > {attendee_values.max()}'], 'Probability P(A=a)': [0]})
    ], ignore_index=True)

    return fixed_cost, cost_per_attendee, pmf_table

def display_randomized_assignment():
    fixed_cost, cost_per_attendee, pmf_table = generate_random_data()

    # Display randomized values
    print(f"Randomized Fixed Cost of Venue Rental: ${fixed_cost}")
    print(f"Randomized Cost per Attendee: ${cost_per_attendee}\n")

    # Display the PMF table
    print("Randomized Probability Mass Function of Attendees:")
    print(pmf_table.to_string(index=False))

    # Return values for further use
    return fixed_cost, cost_per_attendee, pmf_table

# Run the function to generate a randomized version
fixed_cost, cost_per_attendee, pmf_table = display_randomized_assignment()

