import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import httpx
import msal

# Configure your IMAP server settings:
# https://support.microsoft.com/en-us/office/pop-imap-and-smtp-settings-for-outlook-com-d088b986-291d-42b8-9564-9c414e2aa040

# modern auth
# https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app

# Graph explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer


def auth():
    client_id = os.getenv("OUTLOOK_CLIENT_ID")
    client_secret = os.getenv("OUTLOOK_CLIENT_SECRET")

    authority = f"https://login.microsoftonline.com/consumers"
    scopes = ["https://graph.microsoft.com/.default"]

    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
    )

    result = app.acquire_token_for_client(scopes=scopes)

    if "access_token" in result:
        access_token = result["access_token"]
        print(f"Access token acquired: {access_token}")
        print(result)
    else:
        print("Error acquiring token:", result.get("error_description"))


def main():
    auth()


if __name__ == "__main__":
    main()
