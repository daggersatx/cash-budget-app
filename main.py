import streamlit as st
import pandas as pd
import visualizations as viz
from forecast_engine import enhanced_forecast
from data_loader import load_data

# ✅ Load Data
actuals, recurring_expenses, cash_inflow, vaults, start_balances, cc_payments = load_data()

st.title("📊 Cash and Budget Forecasting App")

try:
    # ✅ Run the Forecast
    forecast_df, tasks_by_date, warnings = enhanced_forecast(
        actuals, recurring_expenses, cash_inflow, vaults, start_balances, cc_payments
    )

    # ✅ Plot the Balances
    viz.plot_balances(forecast_df)

    # ✅ Display Warnings
    viz.display_warnings(warnings)

    # ✅ Display Actionable Tasks
    viz.display_tasks(tasks_by_date)

    # ✅ Display Forecast Data Table
    viz.display_forecast_data(forecast_df)

except Exception as e:
    st.error(f"❌ An error occurred: {e}")

