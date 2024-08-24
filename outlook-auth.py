import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

import logging
import httpx
import msal

# Configure your IMAP server settings:
# https://support.microsoft.com/en-us/office/pop-imap-and-smtp-settings-for-outlook-com-d088b986-291d-42b8-9564-9c414e2aa040

# modern auth
# https://learn.microsoft.com/en-us/entra/identity-platform/quickstart-register-app

# Graph explorer
# https://developer.microsoft.com/en-us/graph/graph-explorer

logging.basicConfig(level=logging.INFO)


def auth():
    client_id = os.getenv("OUTLOOK_CLIENT_ID_1")
    client_secret = os.getenv("OUTLOOK_CLIENT_SECRET_1")

    authority = f"https://login.microsoftonline.com/consumers"
    scopes = ["https://graph.microsoft.com/.default"]

    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority,
        client_credential=client_secret,
    )
    # The pattern to acquire a token looks like this.
    result = None

    # First, the code looks up a token from the cache.
    # Because we're looking for a token for the current app, not for a user,
    # use None for the account parameter.
    result = app.acquire_token_silent(scopes, account=None)

    if not result:
        logging.info("No suitable token exists in cache. Let's get a new one.")
        result = app.acquire_token_for_client(scopes)

    if "access_token" in result:
        access_token = result["access_token"]
        logging.info(result)
    else:
        logging.error("Error acquiring token:", result.get("error_description"))

    return access_token


def get_me():
    access_token = auth()
    if not access_token:
        logging.error("Access token not acquired.")
        return

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }

    # Example API call using httpx
    with httpx.Client() as client:
        response = client.get(
            "https://graph.microsoft.com/v1.0/me",
            headers=headers,
        )

        if response.status_code == 200:
            print(response.json())
        else:
            print("Error:", response.text)


def main():
    # auth()
    get_me()


if __name__ == "__main__":
    main()
