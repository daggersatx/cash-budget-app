import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict

# Utility function to clean column names
def clean_column_names(df):
    df.columns = df.columns.str.strip().str.title()  # Remove extra spaces and standardize capitalization
    return df

def enhanced_forecast(actuals, recurring_expenses, cash_inflow, vaults, start_balances, cc_payments):
    today = pd.to_datetime(datetime.now())
    next_month_end = (today + pd.offsets.MonthEnd(2)).normalize()

    # Clean all DataFrames
    for df in [recurring_expenses, cash_inflow, vaults, cc_payments, start_balances, actuals]:
        df = clean_column_names(df)
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])

    start_balances = clean_column_names(start_balances)

    tasks_by_date = defaultdict(list)
    warnings = []
    forecast_records = []

    start_date = (today + timedelta(days=1)).date()
    end_date = next_month_end.date()

    # Initialize Cash and Savings from Start Balances (Day 1)
    ending_cash = float(start_balances.loc[start_balances['Account'] == 'Cash', 'Amount'].values[0])
    ending_savings = float(start_balances.loc[start_balances['Account'] == 'Savings', 'Amount'].values[0])

    # Retrieve desired budget for monthly constraint
    forecast_month = today.month
    forecast_year = today.year

    matching_budget = actuals[
        (actuals['Date'].dt.month == forecast_month) &
        (actuals['Date'].dt.year == forecast_year)
    ]

    if not matching_budget.empty:
        desired_budget = matching_budget['Desired Budget'].iloc[-1]
        if pd.isna(desired_budget):
            warnings.append(f"❌ Desired Budget for {forecast_month}/{forecast_year} is NaN. Defaulting to $0.")
            desired_budget = 0
    else:
        warnings.append(f"❌ No Desired Budget found for {forecast_month}/{forecast_year}. Defaulting to $0.")
        desired_budget = 0

    filtered_actuals = actuals[actuals['Date'] < today.replace(day=1)]  # Exclude current month
    mean_recurring_expenses = filtered_actuals['Recurring Expenses'].mean() if not filtered_actuals.empty else 0
    mean_other_expenses = filtered_actuals['Net Other Expenses'].mean() if not filtered_actuals.empty else 0

    # Step 1: Filter prior funding for the current month
    if today.day > 1:  # Only if today is not the 1st day of the month
        prior_funding = vaults[
            (vaults['Date'].dt.month == today.month) &
            (vaults['Date'].dt.year == today.year) &
            (vaults['Date'] < today)
        ]['Amount'].sum()
    else:
        prior_funding = 0

    # Step 2: Adjust remaining_vault_budget
    remaining_vault_budget = max(0, desired_budget - mean_recurring_expenses - mean_other_expenses - prior_funding)

    for day in pd.date_range(start=start_date, end=end_date):
        day_only = day.date()
        start_cash = ending_cash
        start_savings = ending_savings

        # Apply daily cash inflows, expenses, and CC payments
        daily_inflows = cash_inflow[cash_inflow['Date'].dt.date == day_only]['Amount'].sum()
        ending_cash += daily_inflows

        daily_expenses = recurring_expenses[recurring_expenses['Date'].dt.date == day_only]['Amount'].sum()
        ending_cash -= daily_expenses

        daily_cc_payment_amount = cc_payments[cc_payments['Date'].dt.date == day_only]['Amount'].sum()
        ending_cash -= daily_cc_payment_amount

        # Vault Funding Logic
        vault_funding = 0
        daily_vault_requests = vaults[vaults['Date'].dt.date == day_only]

        for _, vault_request in daily_vault_requests.iterrows():
            vault_name = vault_request['Vault']
            vault_amount = vault_request['Amount']

            if vault_amount <= remaining_vault_budget and vault_amount <= ending_savings:
                ending_savings -= vault_amount
                remaining_vault_budget -= vault_amount
                vault_funding += vault_amount
                tasks_by_date[str(day_only)].append(f"✅ Funded {vault_name} with ${vault_amount:,.2f}")
            else:
                warning_message = f"❌ Insufficient funds for {vault_name} on {day_only} (Remaining vault budget = ${remaining_vault_budget:,.2f}, Savings = ${ending_savings:,.2f})"
                tasks_by_date.setdefault(str(day_only), []).append(warning_message)
                warnings.append(warning_message)

        # Reset Remaining Vault Budget Monthly
        if day_only.day == 1:
            matching_budget = actuals[
                (actuals['Date'].dt.month == day_only.month) &
                (actuals['Date'].dt.year == day_only.year)
            ]
            if not matching_budget.empty:
                desired_budget = matching_budget['Desired Budget'].iloc[-1]
                if pd.isna(desired_budget):
                    warnings.append(f"❌ Desired Budget for {day_only.month}/{day_only.year} is NaN. Defaulting to $0.")
                    desired_budget = 0
            else:
                warnings.append(f"❌ No Desired Budget found for {day_only.month}/{day_only.year}. Defaulting to $0.")
                desired_budget = 0

            remaining_vault_budget = max(0, desired_budget - mean_recurring_expenses - mean_other_expenses)

        # Sweep Logic
        sweep_to_cash = 0
        sweep_to_savings = 0

        upper_limit = 750
        lower_limit = 250

        if ending_cash < lower_limit:
            sweep_to_cash = upper_limit - ending_cash
            if ending_savings >= sweep_to_cash:
                ending_savings -= sweep_to_cash
                ending_cash += sweep_to_cash
                tasks_by_date.setdefault(str(day_only), []).append(f"🔄 Swept ${sweep_to_cash:,.2f} to Cash")
        elif ending_cash > upper_limit:
            sweep_to_savings = ending_cash - upper_limit
            ending_cash -= sweep_to_savings
            ending_savings += sweep_to_savings
            tasks_by_date.setdefault(str(day_only), []).append(f"🔄 Swept ${sweep_to_savings:,.2f} to Savings")

        # Record Daily Forecast
        forecast_records.append({
            'Date': day_only,
            'Start Cash': start_cash,
            'Daily Inflows': daily_inflows,
            'Daily Expenses': daily_expenses,
            'CC Payments': daily_cc_payment_amount,
            'Sweep_to_Cash': sweep_to_cash,
            'Sweep_to_Savings': sweep_to_savings,
            'End Cash': ending_cash,
            'Start Savings': start_savings,
            'Vault Funding': vault_funding,
            'End Savings': ending_savings,
            'Remaining Vault Budget': remaining_vault_budget
        })

    forecast_df = pd.DataFrame(forecast_records)
    return forecast_df, tasks_by_date, warnings
