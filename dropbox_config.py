import dropbox
import os

# ✅ Retrieve the Dropbox Access Token from the environment variable
DROPBOX_ACCESS_TOKEN = os.getenv('DROPBOX_ACCESS_TOKEN')  # Access token from environment variable

def get_dropbox_client():
    """Establish a Dropbox connection using the static access token."""
    if not DROPBOX_ACCESS_TOKEN:
        print("❌ Dropbox Access Token is missing or invalid.")
        return None
    
    try:
        dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
        account = dbx.users_get_current_account()
        print(f"✅ Connected to Dropbox as: {account.name.display_name}")
        return dbx
    except dropbox.exceptions.AuthError as e:
        print(f"❌ Dropbox authentication failed: {e}")
        return None
    except Exception as e:
        print(f"❌ Error connecting to Dropbox: {e}")
        return None

# ✅ Initialize Dropbox Client
db_client = get_dropbox_client()
