import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from datetime import datetime

# ✅ Plot Balances Function (Resized)
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

# ✅ Removed Plot Vault Funding Chart

# ✅ Display Actionable Tasks (with Warnings)
def display_tasks(tasks_by_date):
    st.subheader("📝 Actionable Tasks")

    # Group tasks by month
    tasks_by_month = {}
    for date, tasks in tasks_by_date.items():
        month_key = pd.to_datetime(date).strftime("%B %Y")
        if month_key not in tasks_by_month:
            tasks_by_month[month_key] = {}
        tasks_by_month[month_key][date] = tasks

    # Display tasks grouped by month in expanders
    for month, month_tasks in tasks_by_month.items():
        with st.expander(month):
            for date, tasks in month_tasks.items():
                # If there's only one task, display the date and task on the same line with the date in bold
                if len(tasks) == 1:
                    task = tasks[0]
                    task = task.replace("Funded", "Fund").replace("Vault", "Vault")
                    if "Fund" in task and "Vault" not in task:
                        task = task.replace("Fund", "Fund") + " Vault"
                    elif "Swept" in task:
                        task = task.replace("Swept", "Sweep")
                    st.write(f"**{date}**: {task}")
                else:
                    # Display the date in bold, followed by tasks
                    st.write(f"**{date}**")
                    for task in tasks:
                        task = task.replace("Funded", "Fund").replace("Vault", "Vault")
                        if "Fund" in task and "Vault" not in task:
                            task = task.replace("Fund", "Fund") + " Vault"
                        elif "Swept" in task:
                            task = task.replace("Swept", "Sweep")
                        st.write(f"- {task}")

# ✅ Display Warnings (Fixed Argument)
def display_warnings(warnings):
    # If there are no warnings, display "No warnings detected"
    if not warnings:
        st.success("No warnings detected.")

# ✅ Display Forecast Data
def display_forecast_data(forecast_df):
    st.subheader("📄 Forecast Data")

    # Create a derived 'Sweep' column
    forecast_df['Sweep'] = forecast_df['Sweep to Cash'] - forecast_df['Sweep to Savings']

    # Drop 'Sweep to Cash' and 'Sweep to Savings' to exclude them from the table
    forecast_df = forecast_df.drop(columns=['Sweep to Cash', 'Sweep to Savings'])

    # Filter rows where at least one specified column is not zero
    columns_to_check = ['Daily Inflows', 'Daily Expenses', 'CC Payments', 'Vault Funding', 'Sweep']
    forecast_df = forecast_df[(forecast_df[columns_to_check] != 0).any(axis=1)]

    # Reorder columns for display
    column_order = [
        'Date',
        'Start Cash',
        'Daily Inflows',
        'Daily Expenses',
        'CC Payments',
        'End Cash',
        'Sweep',
        'Start Savings',
        'Vault Funding',
        'End Savings'
    ]
    forecast_df = forecast_df[column_order]

    # Define the monetary columns to format
    monetary_columns = [
        'Start Cash',
        'Daily Inflows',
        'Daily Expenses',
        'CC Payments',
        'End Cash',
        'Sweep',
        'Start Savings',
        'Vault Funding',
        'End Savings'
    ]

    # Define a function to apply light grey styling to $0 values
    def highlight_zero(val):
        if isinstance(val, (int, float)) and val == 0:
            return 'color: lightgrey;'
        return None

    # Apply the styling
    styled_df = forecast_df.style.format(
        {col: "${:,.2f}" for col in monetary_columns}
    ).applymap(highlight_zero, subset=monetary_columns)

    # Display the styled dataframe in Streamlit
    st.dataframe(styled_df, use_container_width=True)
