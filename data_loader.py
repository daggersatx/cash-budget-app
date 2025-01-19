import os
import logging
import pandas as pd

# ✅ Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ✅ Load and validate the local Excel file
def load_data():
    # Resolve the file path relative to the script
    file_path = os.path.join(os.path.dirname(__file__), 'Cash Budget Data.xlsx')
    logging.info(f"Looking for file at: {file_path}")
    return load_local_excel(file_path)
    try:
        excel_data = pd.ExcelFile(file_path)
        logging.info(f"✅ Loaded local file: {file_path}")
        actuals = excel_data.parse('Actuals')
        recurring_expenses = excel_data.parse('Recurring Expenses')
        cash_inflow = excel_data.parse('Cash Inflow')
        vaults = excel_data.parse('Vaults')
        start_balances = excel_data.parse('Start Balances')
        cc_payments = excel_data.parse('CC Payments')
        return actuals, recurring_expenses, cash_inflow, vaults, start_balances, cc_payments
    except Exception as e:
        logging.error(f"❌ Error loading or validating local file: {e}")
        return None, None, None, None, None, None

# ✅ Main function for loading data
def load_data():
    file_path = 'Cash Budget Data.xlsx'
    return load_local_excel(file_path)
