import os
import dropbox
from dotenv import load_dotenv

# ✅ Load environment variables
load_dotenv()

def get_dropbox_client():
    """Initialize and return a Dropbox client using credentials from environment variables."""
    try:
        dbx = dropbox.Dropbox(
            app_key=os.getenv('DROPBOX_APP_KEY'),
            app_secret=os.getenv('DROPBOX_APP_SECRET'),
            oauth2_refresh_token=os.getenv('DROPBOX_REFRESH_TOKEN')
        )
        account = dbx.users_get_current_account()
        print(f"✅ Connected to Dropbox as: {account.name.display_name}")
        return dbx
    except Exception as e:
        print(f"❌ Failed to connect to Dropbox: {e}")
        return None	