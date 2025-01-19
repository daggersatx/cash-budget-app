import pandas as pd
import logging
import io
from dropbox_config import get_dropbox_client

# ✅ Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# ✅ Initialize Dropbox client
dbx = get_dropbox_client()

def load_excel_from_dropbox(file_path):
    """Download an Excel file from Dropbox and parse it."""
    try:
        # Download the file from Dropbox
        metadata, res = dbx.files_download(file_path)
        logging.info(f"✅ File downloaded from Dropbox: {file_path}")

        # Parse the file content
        excel_data = pd.ExcelFile(io.BytesIO(res.content))
        logging.info("✅ Excel file parsed successfully!")
        return excel_data
    except Exception as e:
        logging.error(f"❌ Error downloading or parsing file from Dropbox: {e}")
        return None

def load_data_from_excel(excel_data):
    """Parse the Excel data into DataFrames."""
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
    # ✅ Define the Dropbox file path (relative to the app's root folder)
    dropbox_file_path = 'Cash Budget Data.xlsx'

    # ✅ Download the Excel file from Dropbox
    excel_data = load_excel_from_dropbox(dropbox_file_path)
    if not excel_data:
        return None, None, None, None, None, None

    # ✅ Parse the Excel data into DataFrames
    return load_data_from_excel(excel_data)

# ✅ Load the data by calling load_data() directly
if __name__ == "__main__":
    actuals, recurring_expenses, cash_inflow, vaults, start_balances, cc_payments = load_data()

    # ✅ Debug: Confirm that CC Payments is loaded
    if cc_payments is not None:
        logging.info("✅ CC Payments data loaded successfully:")
        print(cc_payments.head())
    else:
        logging.error("❌ CC Payments data failed to load.")
