import os
import dropbox
from dotenv import load_dotenv	
import logging


# ✅ Load environment variables
load_dotenv()

def get_dropbox_client():
    """Initialize and return a Dropbox client using credentials from environment variables."""
    try:
        # Get credentials from environment variables
        app_key = os.getenv("DROPBOX_APP_KEY")
        app_secret = os.getenv("DROPBOX_APP_SECRET")
        refresh_token = os.getenv("DROPBOX_REFRESH_TOKEN")

        logging.info(f"App Key: {app_key}, App Secret: {app_secret}, Refresh Token: {refresh_token}")

        # Initialize Dropbox client using refresh token
        dbx = dropbox.Dropbox(
            app_key=app_key,
            app_secret=app_secret,
            oauth2_refresh_token=refresh_token
        )
        # Verify connection
        account = dbx.users_get_current_account()
        logging.info(f"✅ Connected to Dropbox as: {account.name.display_name}")
        return dbx
    except Exception as e:
        logging.error(f"❌ Failed to connect to Dropbox: {e}")
        return None