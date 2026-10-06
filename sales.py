import streamlit as st
import pandas as pd

df = pd.read_csv("data/sales_data.csv")

st.title("📊 Sales Analytics")
st.caption("Analyze canteen sales and revenue performance")

st.divider()

# Metrics
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("💰 Total Revenue", f"₹{df['Revenue'].sum():,.0f}")

with col2:
    st.metric("🍽️ Total Sold", f"{df['Quantity_Sold'].sum():,}")

with col3:
    st.metric("🍱 Food Items", df["Food_Item"].nunique())

st.divider()

# Revenue by food
st.subheader("💰 Revenue by Food Item")

revenue = (
    df.groupby("Food_Item")["Revenue"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(revenue)

st.divider()

# Quantity sold
st.subheader("🍽️ Quantity Sold by Food Item")

sold = (
    df.groupby("Food_Item")["Quantity_Sold"]
    .sum()
    .sort_values(ascending=False)
)

st.bar_chart(sold)

st.divider()

# Daily revenue
st.subheader("📈 Daily Revenue")

daily = df.groupby("Date")["Revenue"].sum()

st.line_chart(daily)