import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("data/sales_data.csv")

st.title("🍱 Food Management")
st.caption("Manage and analyze the food items available in the canteen")

st.divider()

# -----------------------------
# FOOD ITEMS
# -----------------------------

food_items = sorted(df["Food_Item"].unique())

st.subheader("🍽️ Available Food Items")

cols = st.columns(3)

for i, food in enumerate(food_items):
    with cols[i % 3]:
        food_data = df[df["Food_Item"] == food]

        sold = food_data["Quantity_Sold"].sum()
        revenue = food_data["Revenue"].sum()
        leftover = food_data["Leftover"].sum()

        with st.container(border=True):
            st.markdown(f"### 🍱 {food}")
            st.write(f"**Sold:** {sold:,.0f}")
            st.write(f"**Leftover:** {leftover:,.0f}")
            st.write(f"**Revenue:** ₹{revenue:,.0f}")

st.divider()

# -----------------------------
# FOOD PERFORMANCE
# -----------------------------

st.subheader("📊 Food Performance")

food_summary = (
    df.groupby("Food_Item")
    .agg(
        Total_Sold=("Quantity_Sold", "sum"),
        Total_Prepared=("Quantity_Prepared", "sum"),
        Total_Leftover=("Leftover", "sum"),
        Total_Revenue=("Revenue", "sum")
    )
    .sort_values(
        "Total_Sold",
        ascending=False
    )
)

st.dataframe(
    food_summary,
    use_container_width=True
)

st.divider()

# -----------------------------
# BEST SELLING FOOD
# -----------------------------

best_food = food_summary["Total_Sold"].idxmax()
best_food_sales = food_summary.loc[
    best_food,
    "Total_Sold"
]

st.subheader("🏆 Best-Selling Food")

st.success(
    f"**{best_food}** is currently the best-selling food item "
    f"with **{best_food_sales:,.0f} portions sold**."
)