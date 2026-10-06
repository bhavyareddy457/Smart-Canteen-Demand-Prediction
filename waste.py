import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("data/sales_data.csv")

st.title("🗑️ Food Waste")
st.caption("Monitor leftover food and identify items with high waste")

st.divider()

# -----------------------------
# OVERALL WASTE
# -----------------------------

total_prepared = df["Quantity_Prepared"].sum()
total_leftover = df["Leftover"].sum()

if total_prepared > 0:
    waste_percentage = (total_leftover / total_prepared) * 100
else:
    waste_percentage = 0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🥘 Total Prepared",
        f"{total_prepared:,.0f}"
    )

with col2:
    st.metric(
        "🗑️ Total Leftover",
        f"{total_leftover:,.0f}"
    )

with col3:
    st.metric(
        "📉 Waste Percentage",
        f"{waste_percentage:.1f}%"
    )

st.divider()

# -----------------------------
# WASTE BY FOOD ITEM
# -----------------------------

st.subheader("🍱 Leftover by Food Item")

waste_by_food = (
    df.groupby("Food_Item")["Leftover"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(waste_by_food)

st.divider()

# -----------------------------
# WASTE PERCENTAGE BY FOOD
# -----------------------------

st.subheader("📊 Waste Percentage by Food")

food_waste = (
    df.groupby("Food_Item")
    .agg(
        Prepared=("Quantity_Prepared", "sum"),
        Leftover=("Leftover", "sum")
    )
)

food_waste["Waste %"] = (
    food_waste["Leftover"]
    / food_waste["Prepared"]
    * 100
)

food_waste = food_waste.sort_values(
    "Waste %",
    ascending=False
)

st.dataframe(
    food_waste,
    use_container_width=True
)

st.divider()

# -----------------------------
# WASTE RECOMMENDATION
# -----------------------------

highest_waste_food = waste_by_food.index[0]
highest_waste_amount = waste_by_food.iloc[0]

st.subheader("💡 Waste Reduction Recommendation")

st.warning(
    f"**{highest_waste_food}** has the highest leftover quantity "
    f"with **{highest_waste_amount:.0f} portions**. "
    "Consider reducing its preparation quantity or improving demand prediction."
)