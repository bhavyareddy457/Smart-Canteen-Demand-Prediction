import streamlit as st
import pandas as pd

# Load data
df = pd.read_csv("data/sales_data.csv")

st.title("📦 Inventory Management")
st.caption("Manage prepared and sold quantities with automatic leftover calculation")

st.divider()

# -----------------------------
# SELECT DATE
# -----------------------------

dates = sorted(df["Date"].unique())

selected_date = st.selectbox(
    "📅 Select Date",
    dates
)

# Get selected date data
day_data = df[df["Date"] == selected_date].copy()

# -----------------------------
# PREPARE EDITABLE TABLE
# -----------------------------

inventory = day_data[
    ["Food_Item", "Quantity_Prepared", "Quantity_Sold", "Price"]
].copy()

inventory.columns = [
    "Food Item",
    "Prepared",
    "Sold",
    "Price"
]

# Editable columns
edited_inventory = st.data_editor(
    inventory,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Food Item": st.column_config.TextColumn(
            "🍱 Food Item",
            disabled=True
        ),
        "Prepared": st.column_config.NumberColumn(
            "🥘 Prepared",
            min_value=0,
            step=1
        ),
        "Sold": st.column_config.NumberColumn(
            "🍽️ Sold",
            min_value=0,
            step=1
        ),
        "Price": st.column_config.NumberColumn(
            "💰 Price",
            disabled=True
        )
    },
    disabled=["Food Item", "Price"]
)

st.divider()

# -----------------------------
# AUTOMATIC LEFTOVER
# -----------------------------

edited_inventory["Leftover"] = (
    edited_inventory["Prepared"]
    - edited_inventory["Sold"]
)

# -----------------------------
# VALIDATION
# -----------------------------

invalid_rows = edited_inventory[
    edited_inventory["Sold"] > edited_inventory["Prepared"]
]

if len(invalid_rows) > 0:

    st.error(
        "⚠️ Sold quantity cannot be greater than prepared quantity."
    )

else:

    # Display calculated leftover
    st.subheader("🗑️ Calculated Leftover")

    display_data = edited_inventory[
        ["Food Item", "Prepared", "Sold", "Leftover"]
    ]

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

    # -----------------------------
    # SAVE BUTTON
    # -----------------------------

    if st.button(
        "💾 Save Inventory Changes",
        type="primary",
        use_container_width=True
    ):

        for _, row in edited_inventory.iterrows():

            mask = (
                (df["Date"] == selected_date)
                & (df["Food_Item"] == row["Food Item"])
            )

            df.loc[mask, "Quantity_Prepared"] = row["Prepared"]
            df.loc[mask, "Quantity_Sold"] = row["Sold"]
            df.loc[mask, "Leftover"] = row["Leftover"]

            # Recalculate revenue
            df.loc[mask, "Revenue"] = (
                row["Sold"] * row["Price"]
            )

        # Save changes
        df.to_csv(
            "data/sales_data.csv",
            index=False
        )

        # Clear Streamlit cache
        st.cache_data.clear()

        st.success(
            "✅ Inventory updated successfully!"
        )

        st.rerun()

# -----------------------------
# SUMMARY
# -----------------------------

st.divider()

st.subheader("📊 Inventory Summary")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "🥘 Prepared",
        f"{edited_inventory['Prepared'].sum():,.0f}"
    )

with col2:
    st.metric(
        "🍽️ Sold",
        f"{edited_inventory['Sold'].sum():,.0f}"
    )

with col3:
    st.metric(
        "🗑️ Leftover",
        f"{edited_inventory['Leftover'].sum():,.0f}"
    )