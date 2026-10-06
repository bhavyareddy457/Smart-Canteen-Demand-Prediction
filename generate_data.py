import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Reproducible results
np.random.seed(42)
random.seed(42)

# Food items and their approximate prices
food_items = {
    "Veg Biryani": 80,
    "Chicken Biryani": 120,
    "Fried Rice": 70,
    "Veg Meals": 90,
    "Samosa": 20,
    "Sandwich": 50,
    "Masala Dosa": 60,
    "Tea": 15,
    "Coffee": 20,
    "Juice": 40
}

# Start date and number of days
start_date = datetime(2026, 4, 1)
number_of_days = 180

data = []

for day_number in range(number_of_days):

    current_date = start_date + timedelta(days=day_number)

    day_name = current_date.strftime("%A")
    month = current_date.month

    # Saturday and Sunday treated as lower-demand days
    weekend = day_name in ["Saturday", "Sunday"]

    # Random holidays
    holiday = random.random() < 0.08

    # Random college events
    event = random.random() < 0.12

    for food_item, price in food_items.items():

        # Base demand for each item
        base_demand = {
            "Veg Biryani": 90,
            "Chicken Biryani": 70,
            "Fried Rice": 65,
            "Veg Meals": 85,
            "Samosa": 110,
            "Sandwich": 55,
            "Masala Dosa": 60,
            "Tea": 140,
            "Coffee": 100,
            "Juice": 75
        }[food_item]

        demand = base_demand

        # Weekday effect
        if weekend:
            demand *= 0.60
        else:
            demand *= 1.00

        # Holiday effect
        if holiday:
            demand *= 0.45

        # College event effect
        if event:
            demand *= 1.30

        # Small random variation
        demand *= np.random.uniform(0.85, 1.15)

        # Quantity prepared
        quantity_prepared = int(round(demand * np.random.uniform(1.05, 1.15)))

        # Actual quantity sold
        quantity_sold = int(
            min(
                quantity_prepared,
                max(0, round(demand + np.random.normal(0, 5)))
            )
        )

        # Leftover food
        leftover = quantity_prepared - quantity_sold

        # Revenue
        revenue = quantity_sold * price

        data.append({
            "Date": current_date.strftime("%Y-%m-%d"),
            "Food_Item": food_item,
            "Day": day_name,
            "Month": month,
            "Holiday": int(holiday),
            "College_Event": int(event),
            "Quantity_Prepared": quantity_prepared,
            "Quantity_Sold": quantity_sold,
            "Leftover": leftover,
            "Price": price,
            "Revenue": revenue
        })

# Create DataFrame
df = pd.DataFrame(data)

# Save CSV
df.to_csv("data/sales_data.csv", index=False)

print("Dataset created successfully!")
print(f"Total records: {len(df)}")
print("File saved at: data/sales_data.csv")

print("\nFirst 10 records:")
print(df.head(10))