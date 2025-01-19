import pandas as pd
import logging
import os

# ✅ Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ✅ Load and validate the local Excel file
def load_local_excel(file_path):
    if not os.path.exists(file_path):
        logging.error(f"❌ File not found: {file_path}")
        return None, None, None, None, None, None
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

# ✅ Load the data by calling load_data() directly
actuals, recurring_expenses, cash_inflow, vaults, start_balances, cc_payments = load_data()

# ✅ Debug: Confirm that CC Payments is loaded
if cc_payments is not None:
    print("✅ CC Payments data loaded successfully:")
    print(cc_payments.head())
else:
    print("❌ CC Payments data failed to load.")
