import pandas as pd
import io
import logging
from dropbox_config import get_dropbox_client

# ✅ Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_excel_from_dropbox(file_path):
    """Download an Excel file from Dropbox and return its content as a Pandas ExcelFile object."""
    dbx = get_dropbox_client()
    if not dbx:
        logging.error("❌ Dropbox client initialization failed.")
        return None
    
    try:
        # Download the file from Dropbox
        metadata, res = dbx.files_download(file_path)
        file_content = res.content
        excel_data = pd.ExcelFile(io.BytesIO(file_content))
        logging.info(f"✅ Loaded file from Dropbox: {file_path}")
        return excel_data
    except Exception as e:
        logging.error(f"❌ Error downloading or reading the file from Dropbox: {e}")
        return None

def load_data_from_excel(excel_data):
    """Parse Excel data into DataFrames."""
    try:
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
        logging.error(f"❌ Error parsing the Excel file: {e}")
        return None, None, None, None, None, None

def load_data():
    """Main function to load data from Dropbox."""
    # ✅ Define the Dropbox file path
    dropbox_file_path = 'Cash Budget Data.xlsx'
    
    # ✅ Load Excel file from Dropbox
    excel_data = load_excel_from_dropbox(dropbox_file_path)
    if not excel_data:
        return None, None, None, None, None, None
    
    # ✅ Parse the Excel file into DataFrames
    return load_data_from_excel(excel_data)

# ✅ Load the data by calling load_data() directly
actuals, recurring_expenses, cash_inflow, vaults, start_balances, cc_payments = load_data()

# ✅ Debug: Confirm that CC Payments is loaded
if cc_payments is not None:
    print("✅ CC Payments data loaded successfully:")
    print(cc_payments.head())
else:
    print("❌ CC Payments data failed to load.")
