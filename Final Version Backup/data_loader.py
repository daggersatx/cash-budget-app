import pandas as pd
import logging

# ✅ Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ✅ Load and validate the local Excel file
def load_local_excel(file_path):
    try:
        excel_data = pd.ExcelFile(file_path)
        logging.info(f"✅ Loaded local file: {file_path}")

        # ✅ Load each sheet into its respective DataFrame
        actuals = excel_data.parse('Actuals')
        logging.info("✅ Actuals data loaded.")
        
        recurring_expenses = excel_data.parse('Recurring Expenses')
        logging.info("✅ Recurring Expenses data loaded.")
        
        cash_inflow = excel_data.parse('Cash Inflow')
        logging.info("✅ Cash Inflow data loaded.")
        
        vaults = excel_data.parse('Vaults')
        logging.info("✅ Vaults data loaded.")
        
        start_balances = excel_data.parse('Start Balances')
        logging.info("✅ Start Balances data loaded.")
        
        cc_payments = excel_data.parse('CC Payments')
        logging.info("✅ CC Payments data loaded.")

        # ✅ Return all loaded DataFrames
        return actuals, recurring_expenses, cash_inflow, vaults, start_balances, cc_payments

    except Exception as e:
        logging.error(f"❌ Error loading or validating local file: {e}")
        return None, None, None, None, None, None

# ✅ Define the main data loading function
def load_data():
    file_path = 'C:\\Users\\karlh\\Dropbox\\Apps\\cash_budget_app\\Cash Budget Data.xlsx'
    return load_local_excel(file_path)

# ✅ Load the data by calling load_data() directly
actuals, recurring_expenses, cash_inflow, vaults, start_balances, cc_payments = load_data()

# ✅ Debug: Confirm that CC Payments is loaded
if cc_payments is not None:
    print("✅ CC Payments data loaded successfully:")
    print(cc_payments.head())
else:
    print("❌ CC Payments data failed to load.")
