import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from datetime import datetime

# ✅ Plot Balances Function
def plot_balances(forecast_df):
    fig, ax = plt.subplots(figsize=(8, 4))  # Reduced size

    ax.bar(forecast_df['Date'], forecast_df['End Savings'], label='Savings', color='skyblue')
    ax.bar(forecast_df['Date'], forecast_df['End Cash'], bottom=forecast_df['End Savings'], label='Cash', color='orange')

    ax.set_xlabel('Date')
    ax.set_ylabel('Balance ($)')
    ax.set_title('Cash and Savings Over Time')
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

# ✅ Display Warnings
def display_warnings(warnings):
    if warnings:
        st.info(f"ℹ️ There are {len(warnings)} warning(s). Check Actionable Tasks for details.")
    else:
        st.success("ℹ️ No warnings detected.")

# ✅ Display Actionable Tasks Grouped by Month
def display_tasks(tasks_by_date):
    st.header("📋 Actionable Tasks")
    
    # Group tasks by month
    tasks_by_month = {}
    for date, tasks in tasks_by_date.items():
        month_year = pd.to_datetime(date).strftime("%B %Y")
        if month_year not in tasks_by_month:
            tasks_by_month[month_year] = {}
        tasks_by_month[month_year][date] = tasks

    # Display tasks grouped by month in collapsible sections
    for month_year, dates_with_tasks in tasks_by_month.items():
        with st.expander(f"📅 {month_year} Tasks", expanded=False):
            for date, tasks in dates_with_tasks.items():
                if len(tasks) == 1:
                    # Inline display for single task
                    st.markdown(f"**{date}:** {tasks[0]}")
                else:
                    # Bulleted list for multiple tasks
                    st.markdown(f"**{date}:**")
                    for task in tasks:
                        st.markdown(f"- {task}")

# ✅ Display Forecast Data Table (Restored)
def display_forecast_data(forecast_df):
    st.subheader("📄 Forecast Data")

    # Define columns to format as monetary
    monetary_columns = ['Start Cash', 'Daily Inflows', 'Daily Expenses', 'CC Payments', 'Sweep_to_Cash', 
                        'Sweep_to_Savings', 'End Cash', 'Start Savings', 'Vault Funding', 'End Savings', 
                        'Remaining Vault Budget']

    # Style function for zero values
    def style_zeros(val):
        return 'color: lightgrey;' if val == 0 else ''

    # Apply formatting and styling
    styled_df = forecast_df.style.format(
        {**{col: "${:,.0f}" for col in monetary_columns}, 'Date': lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else 'N/A'}
    ).applymap(style_zeros, subset=monetary_columns)

    st.dataframe(styled_df, use_container_width=True)
