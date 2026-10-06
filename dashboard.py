import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("data/sales_data.csv")

# -----------------------------
# HEADER
# -----------------------------

st.title("🍱 Smart Canteen Demand Prediction")
st.caption("AI-powered canteen sales, demand and food-waste dashboard")

st.divider()

# -----------------------------
# KEY METRICS
# -----------------------------

total_revenue = df["Revenue"].sum()
total_sold = df["Quantity_Sold"].sum()
total_prepared = df["Quantity_Prepared"].sum()
total_leftover = df["Leftover"].sum()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Revenue", f"₹{total_revenue:,.0f}")

with col2:
    st.metric("🍽️ Food Sold", f"{total_sold:,}")

with col3:
    st.metric("🥘 Food Prepared", f"{total_prepared:,}")

with col4:
    st.metric("🗑️ Leftover", f"{total_leftover:,}")

st.divider()

# -----------------------------
# CHARTS
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    st.subheader("📈 Revenue Trend")

    daily_revenue = (
        df.groupby("Date")["Revenue"]
        .sum()
        .reset_index()
    )

    st.line_chart(
        daily_revenue.set_index("Date")["Revenue"]
    )

with col2:
    st.subheader("🍽️ Food Sold")

    food_sales = (
        df.groupby("Food_Item")["Quantity_Sold"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(food_sales)

# -----------------------------
# FOOD SUMMARY
# -----------------------------

st.divider()

st.subheader("📊 Food Performance")

food_summary = (
    df.groupby("Food_Item")
    .agg(
        Prepared=("Quantity_Prepared", "sum"),
        Sold=("Quantity_Sold", "sum"),
        Leftover=("Leftover", "sum"),
        Revenue=("Revenue", "sum")
    )
    .sort_values("Sold", ascending=False)
)

st.dataframe(
    food_summary,
    use_container_width=True
)
