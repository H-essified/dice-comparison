from collections import defaultdict
import itertools

def roll_dice(die: dict) -> dict:
    """
    Finds all possible outcomes of rolling n dice with any given .

    Args:
        die -> dict: a dictionary containing the minimum and maximum value of a fair die,
        the number of times that die is rolled and a modifier added to the result

    Returns:
        A dictionary with the number of ways to roll each possible outcome
    """

    requried_fields = ["min", "max", "count"]
    if not all(field in die.keys() for field in requried_fields):
        raise KeyError("Mising required parameters in die definitions")
    
    if not "modifier" in die.keys():
        die["modifier"] = 0

    # Create a list of possible outcomes for a single die
    die_outcomes = range(die["min"], die["max"] + 1)

    # Generate all possible combinations of n dice outcomes
    outcomes = list(itertools.product(die_outcomes, repeat=die["count"]))

    # Create counts of each outcome
    outcomes_summary = defaultdict(lambda: 0)
    for outcome in outcomes:
        result = sum(outcome) + die["modifier"]
        outcomes_summary[result] += 1

    return outcomes_summary, len(outcomes)

# Definitions of the dice being compared
d1 = {"min": 1, "max": 10, "count": 2}
d2 = {"min": 1, "max": 20, "count": 1, "modifier": 0}

# Create dictionaries of the outcomes and their frequency for each die
d1_out, d1_count = roll_dice(d1)
d2_out, d2_count = roll_dice(d2)

# Initialise competitive outcomes
outcomes = defaultdict(lambda: 0)

# Brute force each roll comparison
for value, count in d2_out.items():
    outcomes["d1_wins"] += sum([d1_out[winning_key] for winning_key in [key for key in d1_out.keys() if key > value]]) * count
    outcomes["d2_wins"] += sum([d1_out[winning_key] for winning_key in [key for key in d1_out.keys() if key < value]]) * count
    outcomes["draws"] += sum([d1_out[winning_key] for winning_key in [key for key in d1_out.keys() if key == value]]) * count

total_combos = d1_count * d2_count

print("d1 wins:", str(outcomes["d1_wins"] / total_combos))
print("d2 wins:", str(outcomes["d2_wins"] / total_combos))
print("Draw:", str(outcomes["draws"] / total_combos))