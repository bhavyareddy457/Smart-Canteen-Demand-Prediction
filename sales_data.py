import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("data/sales_data.csv")

st.title("📋 Sales Data")
st.caption("View and filter all canteen sales records")

st.divider()

# -----------------------------
# FILTERS
# -----------------------------

col1, col2 = st.columns(2)

with col1:
    food_items = ["All"] + sorted(df["Food_Item"].unique())

    selected_food = st.selectbox(
        "🍱 Food Item",
        food_items
    )

with col2:
    dates = ["All"] + sorted(df["Date"].unique())

    selected_date = st.selectbox(
        "📅 Date",
        dates
    )

# -----------------------------
# APPLY FILTERS
# -----------------------------

filtered_df = df.copy()

if selected_food != "All":
    filtered_df = filtered_df[
        filtered_df["Food_Item"] == selected_food
    ]

if selected_date != "All":
    filtered_df = filtered_df[
        filtered_df["Date"] == selected_date
    ]

# -----------------------------
# SUMMARY
# -----------------------------

st.subheader("📊 Sales Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "🍽️ Sold",
        f"{filtered_df['Quantity_Sold'].sum():,.0f}"
    )

with col2:
    st.metric(
        "🥘 Prepared",
        f"{filtered_df['Quantity_Prepared'].sum():,.0f}"
    )

with col3:
    st.metric(
        "🗑️ Leftover",
        f"{filtered_df['Leftover'].sum():,.0f}"
    )

with col4:
    st.metric(
        "💰 Revenue",
        f"₹{filtered_df['Revenue'].sum():,.0f}"
    )

st.divider()

# -----------------------------
# DATA TABLE
# -----------------------------

st.subheader("📋 Sales Records")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)

st.caption(
    f"Showing {len(filtered_df):,} records"
)