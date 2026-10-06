import streamlit as st

st.set_page_config(
    page_title="Smart Canteen Demand Prediction",
    page_icon="🍱",
    layout="wide"
)

# -----------------------------
# TOP NAVIGATION
# -----------------------------

dashboard = st.Page(
    "dashboard.py",
    title="Dashboard",
    icon="🏠",
    default=True
)

sales = st.Page(
    "sales.py",
    title="Sales Analytics",
    icon="📊"
)

prediction = st.Page(
    "prediction.py",
    title="AI Prediction",
    icon="🤖"
)

inventory = st.Page(
    "inventory.py",
    title="Inventory",
    icon="📦"
)

waste = st.Page(
    "waste.py",
    title="Food Waste",
    icon="🗑️"
)

sales_data = st.Page(
    "sales_data.py",
    title="Sales Data",
    icon="📋"
)

food_management = st.Page(
    "food_management.py",
    title="Food Management",
    icon="🍱"
)

# Navigation appears at the TOP of the Streamlit app
pg = st.navigation(
    [
        dashboard,
        sales,
        prediction,
        inventory,
        waste,
        sales_data,
        food_management
    ],
    position="top"
)

pg.run()
