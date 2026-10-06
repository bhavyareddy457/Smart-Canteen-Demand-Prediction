import streamlit as st
import pandas as pd

df = pd.read_csv("data/sales_data.csv")

st.title("🤖 AI Demand Prediction")
st.caption("Predict expected food demand using historical sales data")

st.divider()

# -----------------------------
# SELECT FOOD ITEM
# -----------------------------

food_items = sorted(df["Food_Item"].unique())

selected_food = st.selectbox(
    "🍱 Select Food Item",
    food_items
)

# -----------------------------
# HISTORICAL DATA
# -----------------------------

food_data = df[df["Food_Item"] == selected_food]

average_demand = food_data["Quantity_Sold"].mean()
maximum_demand = food_data["Quantity_Sold"].max()
minimum_demand = food_data["Quantity_Sold"].min()

# Simple demand prediction
predicted_demand = round(average_demand)

# -----------------------------
# RESULTS
# -----------------------------

st.subheader("🔮 Predicted Demand")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🤖 Predicted Quantity",
        f"{predicted_demand}"
    )

with col2:
    st.metric(
        "📊 Average Sold",
        f"{average_demand:.0f}"
    )

with col3:
    st.metric(
        "📈 Maximum Sold",
        f"{maximum_demand}"
    )

st.divider()

# -----------------------------
# RECOMMENDATION
# -----------------------------

st.subheader("💡 Preparation Recommendation")

recommended_quantity = round(predicted_demand * 1.10)

st.success(
    f"Prepare approximately **{recommended_quantity} portions** "
    f"of **{selected_food}**."
)

st.caption(
    "The recommendation includes a small safety buffer to help reduce "
    "the chance of running out during demand."
)

st.divider()

# -----------------------------
# HISTORICAL SALES
# -----------------------------

st.subheader(f"📈 Historical Sales — {selected_food}")

chart_data = (
    food_data.groupby("Date")["Quantity_Sold"]
    .sum()
)

st.line_chart(chart_data)

st.divider()

# -----------------------------
# FOOD PERFORMANCE
# -----------------------------

st.subheader("📊 Food Demand Statistics")

stats = pd.DataFrame({
    "Metric": [
        "Average Demand",
        "Minimum Demand",
        "Maximum Demand",
        "Recommended Preparation"
    ],
    "Quantity": [
        round(average_demand),
        minimum_demand,
        maximum_demand,
        recommended_quantity
    ]
})

st.dataframe(
    stats,
    use_container_width=True,
    hide_index=True
)