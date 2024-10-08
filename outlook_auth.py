import os
from dotenv import load_dotenv

load_dotenv()

import logging

logging.basicConfig(level=logging.INFO)

import msal

from file_token_cache import FileTokenCache


def auth_device_flow():
    """
    Authenticates the user using the device code flow for Microsoft Entra app.

    This function retrieves the necessary configurations for the Entra app, including the client ID and authority.
    It then initializes a token cache and sets up an MSAL client application with the provided configurations.

    The function checks if there are any existing accounts in the token cache. If so, it attempts to acquire a token silently using the first account.
    If the token is successfully acquired from the cache, it logs a message and returns the access token.

    If there are no existing accounts or the token cannot be acquired from the cache, the function initiates the device code flow by calling the `initiate_device_flow` method of the MSAL client application.
    It then acquires the token by calling the `acquire_token_by_device_flow` method with the obtained flow.

    The function saves the token cache and logs the result. If the access token is present in the result, it logs a success message and returns the access token.
    Otherwise, it logs an error message and returns `None`.

    Returns:
        str: The access token if successfully acquired, or `None` if there was an error acquiring the token.
    """
    # The Entra app's configurations. -> See: https://entra.microsoft.com/
    client_id = os.getenv("OUTLOOK_CLIENT_ID_2")
    authority = "https://login.microsoftonline.com/common"
    scopes = [
        "https://outlook.office.com/IMAP.AccessAsUser.All",
        "https://outlook.office.com/SMTP.Send",
    ]

    token_cache = FileTokenCache()

    # Set up MSAL client
    app = msal.PublicClientApplication(
        client_id=client_id,
        authority=authority,
        token_cache=token_cache,
    )

    result = None

    accounts = app.get_accounts()
    if accounts:
        result = app.acquire_token_silent(scopes=scopes, account=accounts[0])
        if result:
            logging.info("🔐 Token acquired from cache")
            return result["access_token"]
        else:
            logging.info("🔐 Token NOT found in cache")
    else:
        logging.info("No accounts found in cache")

    # Else, Initiate device code flow
    flow = app.initiate_device_flow(scopes=scopes)
    if "user_code" not in flow:
        logging.error("❌ Error initiating device flow")
        logging.error(flow.get("error"))
        logging.error(flow.get("error_description"))
        return None

    logging.info("🔑 Device code flow initiated")
    print(flow["message"])
    print("\n----------------------------------------------------")
    print(f"Open: {flow['verification_uri']}")
    print(f"Code: {flow['user_code']}")
    print("----------------------------------------------------\n")

    result = app.acquire_token_by_device_flow(flow)

    if "access_token" in result:
        logging.info(f"🔐 Token acquired from remote")
        token_cache.save_cache()
        return result["access_token"]
    else:
        logging.error("❌ Error acquiring token.")
        logging.error(result.get("error"))
        logging.error(result.get("error_description"))
        return None


if __name__ == "__main__":
    print("Usage: from outlook_auth import auth_device_flow")
