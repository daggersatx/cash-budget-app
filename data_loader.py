import os
import logging
import pandas as pd

# ✅ Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_local_excel(file_path):
    """Load and validate the local Excel file."""
    # Check if the file exists at the specified path
    if not os.path.exists(file_path):
        logging.error(f"❌ File not found: {file_path}")
        return None, None, None, None, None, None

    try:
        # Attempt to load the Excel file
        logging.info(f"✅ Attempting to load file: {file_path}")
        excel_data = pd.ExcelFile(file_path)

        # Parse each required sheet
        actuals = excel_data.parse('Actuals')
        recurring_expenses = excel_data.parse('Recurring Expenses')
        cash_inflow = excel_data.parse('Cash Inflow')
        vaults = excel_data.parse('Vaults')
        start_balances = excel_data.parse('Start Balances')
        cc_payments = excel_data.parse('CC Payments')

        logging.info("✅ Successfully parsed all sheets from the Excel file")
        return actuals, recurring_expenses, cash_inflow, vaults, start_balances, cc_payments
    except Exception as e:
        # Handle any error during file loading or parsing
        logging.error(f"❌ Error loading Excel file: {e}")
        return None, None, None, None, None, None

def load_data():
    """Main function for loading data."""
    file_path = os.path.join(os.path.dirname(__file__), 'Cash Budget Data.xlsx')
    logging.info(f"Looking for file at: {file_path}")
    return load_local_excel(file_path)
