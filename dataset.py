import pandas as pd
import random

random.seed(42)

education_levels = ["No formal education", "5th pass", "8th pass", "10th pass", "12th pass"]
family_occupations = ["Farming", "Weaving", "Tailoring", "Carpentry", "None"]
mobility_levels = ["Low", "Medium", "High"]
interest_areas = ["Tailoring", "Electrical work", "Carpentry", "Food Processing"]
trades = ["Tailoring", "Electrician", "Carpenter", "Food Processing"]

def assign_label(row):
    for trade in trades:
        if trade.lower() in row["interest_area"].lower():
            return trade
    for trade in trades:
        if trade.lower() in row["family_occupation"].lower():
            return trade
    return random.choice(trades)

def generate_row():
    row = {
        "education_level": random.choice(education_levels),
        "family_occupation": random.choice(family_occupations),
        "mobility_constraint": random.choice(mobility_levels),
        "interest_area": random.choice(interest_areas),
    }
    row["NSQF_trade_label"] = assign_label(row)
    return row

data = [generate_row() for _ in range(200)]
df = pd.DataFrame(data)
df.to_csv("beneficiary_data.csv", index=False)
print(df.head())
print("Saved beneficiary_data.csv with", len(df), "rows")