import pandas as pd
import io
import logging
from dropbox_config import get_dropbox_client

# ✅ Set up logging for debugging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_excel_from_dropbox(file_path):
    """Download an Excel file from Dropbox and parse it."""
    dbx = get_dropbox_client()
    if not dbx:
        logging.error("❌ Dropbox client initialization failed.")
        return None

    try:
        logging.info(f"🔍 Attempting to download file: {file_path}")
        metadata, res = dbx.files_download(file_path)
        logging.info(f"✅ File downloaded: {metadata.name}")
        logging.info(f"File size: {len(res.content)} bytes")
        return pd.ExcelFile(io.BytesIO(res.content))
    except dropbox.exceptions.ApiError as api_error:
        logging.error(f"❌ Dropbox API error: {api_error}")
    except Exception as e:
        logging.error(f"❌ Error downloading or parsing file from Dropbox: {e}")
    return None
def load_data():
    """Main function to load data from Dropbox."""
    dropbox_file_path = '/Cash Budget Data.xlsx'
    excel_data = load_excel_from_dropbox(dropbox_file_path)
    if not excel_data:
        return None, None, None, None, None, None

    try:
        # Parse sheets into DataFrames
        actuals = excel_data.parse('Actuals')
        recurring_expenses = excel_data.parse('Recurring Expenses')
        cash_inflow = excel_data.parse('Cash Inflow')
        vaults = excel_data.parse('Vaults')
        start_balances = excel_data.parse('Start Balances')
        cc_payments = excel_data.parse('CC Payments')

        logging.info("✅ All data loaded successfully.")
        return actuals, recurring_expenses, cash_inflow, vaults, start_balances, cc_payments
    except Exception as e:
        logging.error(f"❌ Error parsing the Excel file: {e}")
        return None, None, None, None, None, None
